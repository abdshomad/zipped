from typing import Dict, List, Any, Optional
import random
from services.researcher.arena import TokenGenome, EvolutionaryArena
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge
from services.evaluator.db import BenchmarkDB

class SelfSustainingEvolutionKernel:
    """Perpetual autonomous evolutionary kernel orchestrating continuous token optimization and invariant verification."""

    def __init__(self, db: Optional[BenchmarkDB] = None, bridge: Optional[MultiTokenizerBridge] = None):
        self.db = db or BenchmarkDB()
        self.bridge = bridge or MultiTokenizerBridge()
        self.arena = EvolutionaryArena(db=self.db, tokenizer_bridge=self.bridge)
        self.step_count = 0
        self.best_reduction_pct = 0.0

    def run_evolution_step(
        self,
        population: List[TokenGenome],
        corpus: str,
        candidate_phrases: List[str],
        cycle_id: int = 19,
    ) -> Dict[str, Any]:
        """Executes a single generational evolution step."""
        self.step_count += 1

        # Run 2 generations of genetic search
        result = self.arena.run_evolution_cycle(
            population=population,
            corpus=corpus,
            candidate_phrases=candidate_phrases,
            generations=2,
            cycle_id=cycle_id,
        )

        red = result["best_reduction_pct"]
        if red > self.best_reduction_pct:
            self.best_reduction_pct = red

        return {
            "step": self.step_count,
            "best_genome_id": result["best_genome_id"],
            "step_reduction_pct": red,
            "global_best_reduction_pct": self.best_reduction_pct,
            "pareto_size": len(result["pareto_frontier"]),
        }

    def run_continuous_loop(
        self,
        corpus: str,
        candidate_phrases: List[str],
        steps: int = 5,
        cycle_id: int = 19,
    ) -> Dict[str, Any]:
        """Runs a continuous evolutionary loop across multiple steps."""
        # Initialize seed population
        population = [
            TokenGenome(f"seed_{i}", {candidate_phrases[i % len(candidate_phrases)]: f"§{i}"})
            for i in range(min(4, len(candidate_phrases)))
        ]

        step_history = []
        for step in range(steps):
            step_res = self.run_evolution_step(
                population=population,
                corpus=corpus,
                candidate_phrases=candidate_phrases,
                cycle_id=cycle_id,
            )
            step_history.append(step_res)

        return {
            "total_steps": steps,
            "final_best_reduction_pct": self.best_reduction_pct,
            "history": step_history,
        }

    def verify_health(self) -> Dict[str, Any]:
        """Executes self-health checks and verifies system invariants."""
        # 1. Test tokenizer bridge
        tok_test = self.bridge.count_tokens("Zipped test payload")
        assert "o200k_base" in tok_test
        assert "cl100k_base" in tok_test

        # 2. Test database connectivity
        summary = self.db.get_summary_stats()
        assert summary["total_runs"] > 0

        # 3. Test lossless roundtrip invariant
        genome = TokenGenome("health_check_genome", {"lossless invariant": "§0"})
        sample = "Testing lossless invariant verification."
        comp = genome.compress(sample)
        decomp = genome.decompress(comp)
        assert decomp == sample

        return {
            "status": "healthy",
            "tokenizers_ready": list(tok_test.keys()),
            "total_db_runs": summary["total_runs"],
            "lossless_invariant_verified": True,
        }
