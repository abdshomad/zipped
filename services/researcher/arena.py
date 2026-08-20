from typing import Dict, List, Any
import math

class EvolutionaryArena:
    """Adversarial arena to evaluate and rank synthetic token representations against Shannon entropy limits."""

    def __init__(self):
        self.pareto_frontier: List[Dict[str, Any]] = []

    def compute_fitness(self, token_reduction_pct: float, semantic_accuracy: float) -> float:
        """
        Fitness formula severely penalizes any accuracy drop below 99%
        while rewarding aggressive token reduction.
        """
        if semantic_accuracy < 0.90:
            return 0.0
        # Exponential scaling for accuracy combined with linear token reduction
        return (token_reduction_pct / 100.0) * (semantic_accuracy ** 10)

    def evaluate_candidate(
        self, candidate_id: str, representation: str, token_reduction_pct: float, semantic_accuracy: float
    ) -> Dict[str, Any]:
        fitness = self.compute_fitness(token_reduction_pct, semantic_accuracy)
        is_pareto = False

        if semantic_accuracy >= 0.99:
            is_pareto = True
            self.pareto_frontier.append({
                "candidate_id": candidate_id,
                "representation": representation,
                "token_reduction_pct": token_reduction_pct,
                "semantic_accuracy": semantic_accuracy,
                "fitness": round(fitness, 4),
            })
            # Keep top candidates sorted by fitness
            self.pareto_frontier.sort(key=lambda x: x["fitness"], reverse=True)

        return {
            "candidate_id": candidate_id,
            "fitness": round(fitness, 4),
            "is_pareto_optimal": is_pareto,
        }
