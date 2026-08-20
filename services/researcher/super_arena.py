from typing import Dict, List, Any, Optional
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

class SuperArenaCoordinator:
    """Coordinates global multi-tier tournaments and Pareto frontier telemetry dashboards."""

    def __init__(self, db: Optional[BenchmarkDB] = None, bridge: Optional[MultiTokenizerBridge] = None):
        self.db = db or BenchmarkDB()
        self.bridge = bridge or MultiTokenizerBridge()

    def run_tournament(self, test_suites: Dict[str, Dict[str, str]], cycle_id: int = 10) -> Dict[str, Any]:
        """
        Executes a tournament across multiple test suites (raw vs compressed representations),
        recording all multi-tokenizer metrics to BenchmarkDB.
        """
        results = {}
        for suite_name, data in test_suites.items():
            raw = data["original"]
            compact = data["compressed"]
            codec_id = data.get("codec_id", f"suite-{suite_name}")
            tier_level = data.get("tier_level", 10)
            fidelity = data.get("fidelity", 1.0)

            bench = self.bridge.benchmark_compression(raw, compact)
            self.db.record_run(
                cycle_id=cycle_id,
                feature_name=f"Super-Arena Tournament ({suite_name})",
                codec_id=codec_id,
                tier_level=tier_level,
                metrics_by_tokenizer=bench,
                dataset_name=suite_name,
                fidelity_score=fidelity,
            )
            results[suite_name] = {
                "codec_id": codec_id,
                "tier_level": tier_level,
                "benchmarks": bench,
            }

        return results

    def generate_dashboard_report(self) -> Dict[str, Any]:
        """Collect aggregated Pareto metrics and leaderboard summary."""
        leaderboard = self.db.get_leaderboard()
        summary = self.db.get_summary_stats()
        return {
            "summary": summary,
            "leaderboard": leaderboard,
            "pareto_count": len(leaderboard),
        }

    def render_ascii_dashboard(self) -> str:
        """Render a formatted ASCII dashboard visualization."""
        report = self.generate_dashboard_report()
        summary = report["summary"]
        leaderboard = report["leaderboard"]

        lines = [
            "==================================================================",
            "             ZIPPED GLOBAL PARETO FRONTIER DASHBOARD              ",
            "==================================================================",
            f"Total Benchmark Runs: {summary['total_runs']} | Metrics: {summary['total_metrics_evaluated']}",
            f"Average Token Reduction: {summary['avg_reduction_pct']}% | Peak Reduction: {summary['max_reduction_pct']}%",
            "------------------------------------------------------------------",
            f"{'Tier':<6} | {'Codec ID':<26} | {'Best Reduction':<15} | {'Fidelity':<8}",
            "------------------------------------------------------------------",
        ]

        for entry in leaderboard:
            tier_str = f"Tier {entry['tier_level']}"
            reduct_str = f"{entry['best_reduction_pct']:.2f}%"
            fid_str = f"{entry['best_fidelity_score']:.2f}"
            lines.append(f"{tier_str:<6} | {entry['codec_id']:<26} | {reduct_str:<15} | {fid_str:<8}")

        lines.append("==================================================================")
        return "\n".join(lines)
