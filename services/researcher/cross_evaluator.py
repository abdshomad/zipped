from typing import Dict, List, Any, Optional
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge
from services.evaluator.db import BenchmarkDB

class CrossModelFrontierEvaluator:
    """Joint multi-model optimizer evaluating token reduction simultaneously across all model tokenizers."""

    def __init__(self, db: Optional[BenchmarkDB] = None, bridge: Optional[MultiTokenizerBridge] = None):
        self.db = db or BenchmarkDB()
        self.bridge = bridge or MultiTokenizerBridge()

    def evaluate_representation(self, original: str, compressed: str) -> Dict[str, Any]:
        """Evaluates token reduction across all registered tokenizers."""
        bench = self.bridge.benchmark_compression(original, compressed)
        joint_score = self.compute_joint_score(bench)
        return {
            "benchmarks": bench,
            "joint_score": joint_score,
            "min_reduction_pct": min(b["reduction_percent"] for b in bench.values()),
            "avg_reduction_pct": sum(b["reduction_percent"] for b in bench.values()) / max(len(bench), 1),
        }

    @staticmethod
    def compute_joint_score(benchmarks: Dict[str, Dict[str, Any]]) -> float:
        """
        Computes the harmonic mean of token reduction percentages across all tokenizers.
        Harmonic mean heavily penalizes single-tokenizer over-fitting / regressions.
        """
        reductions = [max(0.01, b["reduction_percent"]) for b in benchmarks.values()]
        if not reductions:
            return 0.0
        # Harmonic mean: N / sum(1/x)
        inv_sum = sum(1.0 / r for r in reductions)
        harmonic_mean = len(reductions) / inv_sum
        return round(harmonic_mean, 2)

    def filter_pareto_dominant(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters a candidate pool to return only non-dominated Pareto frontier representations."""
        pareto_front = []
        for i, cand_a in enumerate(candidates):
            dominated = False
            for j, cand_b in enumerate(candidates):
                if i == j:
                    continue
                # cand_b dominates cand_a if b >= a on all tokenizers and b > a on at least one
                bench_a = cand_a["benchmarks"]
                bench_b = cand_b["benchmarks"]

                tok_names = set(bench_a.keys()).intersection(set(bench_b.keys()))
                all_ge = all(bench_b[t]["reduction_percent"] >= bench_a[t]["reduction_percent"] for t in tok_names)
                any_gt = any(bench_b[t]["reduction_percent"] > bench_a[t]["reduction_percent"] for t in tok_names)

                if all_ge and any_gt:
                    dominated = True
                    break
            if not dominated:
                pareto_front.append(cand_a)

        pareto_front.sort(key=lambda c: c["joint_score"], reverse=True)
        return pareto_front

    def benchmark_frontier_selection(
        self,
        candidates: List[Dict[str, Any]],
        cycle_id: int = 16,
        dataset_name: str = "multi_model_frontier_set",
    ) -> Dict[str, Any]:
        """Evaluates candidate pool, extracts Pareto frontier, and records elite candidate to BenchmarkDB."""
        frontier = self.filter_pareto_dominant(candidates)
        elite = frontier[0] if frontier else candidates[0]

        self.db.record_run(
            cycle_id=cycle_id,
            feature_name=f"Cross-Model Frontier Pareto Elite ({elite.get('candidate_id', 'elite')})",
            codec_id="cross-model-tier16",
            tier_level=16,
            metrics_by_tokenizer=elite["benchmarks"],
            dataset_name=dataset_name,
            fidelity_score=elite.get("fidelity", 1.0),
        )

        return {
            "frontier_count": len(frontier),
            "elite_candidate": elite,
            "pareto_frontier": frontier,
        }
