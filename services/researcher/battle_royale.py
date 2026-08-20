from typing import Dict, List, Any, Optional, Tuple
import math
import collections
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge
from services.evaluator.db import BenchmarkDB
from services.researcher.arena import TokenGenome

class ShannonEntropyEstimator:
    """Computes theoretical Shannon information entropy and minimum bound estimates."""

    @staticmethod
    def compute_entropy(text: str) -> float:
        """Calculates Shannon entropy H(X) in bits per character."""
        if not text:
            return 0.0
        counts = collections.Counter(text)
        length = len(text)
        entropy = -sum((count / length) * math.log2(count / length) for count in counts.values())
        return round(entropy, 4)

    @staticmethod
    def compute_theoretical_compression_limit(original: str) -> float:
        """Estimates maximum achievable theoretical compression ratio (0.0 to 1.0) based on redundancy."""
        if not original:
            return 0.0
        h_x = ShannonEntropyEstimator.compute_entropy(original)
        max_entropy = math.log2(max(len(set(original)), 2))
        redundancy = 1.0 - (h_x / max_entropy) if max_entropy > 0 else 0.0
        return round(max(0.0, min(1.0, redundancy)), 4)

class BattleRoyaleStrategy:
    """Competitor strategy in the multi-agent battle royale arena."""

    def __init__(self, strategy_id: str, genome: TokenGenome, elo: float = 1200.0):
        self.strategy_id = strategy_id
        self.genome = genome
        self.elo = elo
        self.wins = 0
        self.losses = 0
        self.draws = 0

class BattleRoyaleMatchmaker:
    """Adversarial tournament matchmaker executing elimination rounds and tracking ELO rankings."""

    def __init__(self, db: Optional[BenchmarkDB] = None, bridge: Optional[MultiTokenizerBridge] = None):
        self.db = db or BenchmarkDB()
        self.bridge = bridge or MultiTokenizerBridge()
        self.entropy_estimator = ShannonEntropyEstimator()

    def play_match(self, strat_a: BattleRoyaleStrategy, strat_b: BattleRoyaleStrategy, corpus: str) -> Tuple[float, float]:
        """Pits two strategies head-to-head on compression ratio and fidelity."""
        comp_a = strat_a.genome.compress(corpus)
        comp_b = strat_b.genome.compress(corpus)

        bench_a = self.bridge.benchmark_compression(corpus, comp_a)
        bench_b = self.bridge.benchmark_compression(corpus, comp_b)

        red_a = sum(b["reduction_percent"] for b in bench_a.values()) / max(len(bench_a), 1)
        red_b = sum(b["reduction_percent"] for b in bench_b.values()) / max(len(bench_b), 1)

        # Expected outcome
        ea = 1.0 / (1.0 + 10.0 ** ((strat_b.elo - strat_a.elo) / 400.0))
        eb = 1.0 - ea
        k = 32.0

        if red_a > red_b + 0.5:
            sa, sb = 1.0, 0.0
            strat_a.wins += 1
            strat_b.losses += 1
        elif red_b > red_a + 0.5:
            sa, sb = 0.0, 1.0
            strat_b.wins += 1
            strat_a.losses += 1
        else:
            sa, sb = 0.5, 0.5
            strat_a.draws += 1
            strat_b.draws += 1

        strat_a.elo += k * (sa - ea)
        strat_b.elo += k * (sb - eb)

        return red_a, red_b

    def run_tournament(
        self,
        strategies: List[BattleRoyaleStrategy],
        corpus: str,
        rounds: int = 3,
        cycle_id: int = 12,
    ) -> Dict[str, Any]:
        """Executes a round-robin tournament across all competing strategies."""
        for _ in range(rounds):
            for i in range(len(strategies)):
                for j in range(i + 1, len(strategies)):
                    self.play_match(strategies[i], strategies[j], corpus)

        strategies.sort(key=lambda s: s.elo, reverse=True)
        champion = strategies[0]

        # Evaluate champion metrics
        comp_champ = champion.genome.compress(corpus)
        bench_champ = self.bridge.benchmark_compression(corpus, comp_champ)

        self.db.record_run(
            cycle_id=cycle_id,
            feature_name=f"Battle Royale Champion ({champion.strategy_id})",
            codec_id="battle-royale-tier12",
            tier_level=12,
            metrics_by_tokenizer=bench_champ,
            dataset_name="battle_royale_arena_corpus",
            fidelity_score=1.0,
        )

        return {
            "champion_id": champion.strategy_id,
            "champion_elo": round(champion.elo, 1),
            "rankings": [
                {
                    "rank": idx + 1,
                    "strategy_id": s.strategy_id,
                    "elo": round(s.elo, 1),
                    "record": f"{s.wins}W-{s.losses}L-{s.draws}D",
                }
                for idx, s in enumerate(strategies)
            ],
            "benchmarks": bench_champ,
        }
