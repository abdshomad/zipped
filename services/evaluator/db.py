import sqlite3
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

DB_PATH = os.environ.get("ZIPPED_DB_PATH", "data/benchmarks.sqlite")

class BenchmarkDB:
    """Manages SQLite storage for historical benchmark metrics, deltas, and Pareto leaderboards."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS benchmark_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cycle_id INTEGER NOT NULL,
                feature_name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                git_commit TEXT,
                metadata TEXT
            );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS token_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                codec_id TEXT NOT NULL,
                tokenizer_name TEXT NOT NULL,
                dataset_name TEXT NOT NULL,
                original_tokens INTEGER NOT NULL,
                compressed_tokens INTEGER NOT NULL,
                reduction_pct REAL NOT NULL,
                delta_prev_pct REAL NOT NULL,
                fidelity_score REAL NOT NULL,
                latency_ms REAL,
                FOREIGN KEY (run_id) REFERENCES benchmark_runs(id)
            );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS pareto_leaderboard (
                codec_id TEXT PRIMARY KEY,
                tier_level INTEGER NOT NULL,
                best_reduction_pct REAL NOT NULL,
                best_fidelity_score REAL NOT NULL,
                last_updated TEXT NOT NULL
            );
            """)
            conn.commit()

    def get_latest_metric(self, codec_id: str, tokenizer_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve the most recent benchmark metric for a codec and tokenizer."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT tm.* FROM token_metrics tm
            JOIN benchmark_runs br ON tm.run_id = br.id
            WHERE tm.codec_id = ? AND tm.tokenizer_name = ?
            ORDER BY br.id DESC LIMIT 1
            """, (codec_id, tokenizer_name))
            row = cursor.fetchone()
            return dict(row) if row else None

    def record_run(
        self,
        cycle_id: int,
        feature_name: str,
        codec_id: str,
        tier_level: int,
        metrics_by_tokenizer: Dict[str, Dict[str, Any]],
        dataset_name: str = "standard_eval",
        fidelity_score: float = 1.0,
        git_commit: str = ""
    ) -> Dict[str, Any]:
        """Record a benchmark run, calculate deltas against previous run, and update leaderboard."""
        now = datetime.now(timezone.utc).isoformat()
        results = {}

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO benchmark_runs (cycle_id, feature_name, timestamp, git_commit)
            VALUES (?, ?, ?, ?)
            """, (cycle_id, feature_name, now, git_commit))
            run_id = cursor.lastrowid

            for tok_name, data in metrics_by_tokenizer.items():
                orig = data["original_tokens"]
                comp = data["compressed_tokens"]
                reduct = data["reduction_percent"]

                # Check previous best
                prev = self.get_latest_metric(codec_id, tok_name)
                prev_reduct = prev["reduction_pct"] if prev else 0.0
                delta = round(reduct - prev_reduct, 2)

                cursor.execute("""
                INSERT INTO token_metrics (
                    run_id, codec_id, tokenizer_name, dataset_name,
                    original_tokens, compressed_tokens, reduction_pct, delta_prev_pct, fidelity_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (run_id, codec_id, tok_name, dataset_name, orig, comp, reduct, delta, fidelity_score))

                results[tok_name] = {
                    "reduction_pct": reduct,
                    "previous_reduction_pct": prev_reduct,
                    "delta_pct": delta,
                    "fidelity_score": fidelity_score,
                }

            # Update Pareto Leaderboard
            avg_reduction = sum([d["reduction_percent"] for d in metrics_by_tokenizer.values()]) / max(len(metrics_by_tokenizer), 1)
            cursor.execute("""
            INSERT INTO pareto_leaderboard (codec_id, tier_level, best_reduction_pct, best_fidelity_score, last_updated)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(codec_id) DO UPDATE SET
                best_reduction_pct = MAX(best_reduction_pct, excluded.best_reduction_pct),
                best_fidelity_score = MAX(best_fidelity_score, excluded.best_fidelity_score),
                last_updated = excluded.last_updated
            """, (codec_id, tier_level, avg_reduction, fidelity_score, now))

            conn.commit()

        return results
