from typing import Dict, List, Any, Optional, Tuple
import random
import difflib
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge
from services.evaluator.db import BenchmarkDB

class TokenGenome:
    """Represents a token compression candidate chromosome."""
    def __init__(self, genome_id: str, mappings: Dict[str, str], tier_level: int = 3):
        self.genome_id = genome_id
        self.mappings: Dict[str, str] = dict(mappings)
        self.tier_level = tier_level
        self.fitness: float = 0.0
        self.token_reduction_pct: float = 0.0
        self.semantic_fidelity: float = 1.0

    def compress(self, text: str) -> str:
        res = text
        for phrase, sigil in sorted(self.mappings.items(), key=lambda x: len(x[0]), reverse=True):
            res = res.replace(phrase, sigil)
        header = "§{" + ",".join(f"{k}|{v}" for k, v in self.mappings.items()) + "}"
        return f"{header} {res}" if self.mappings else res

    def decompress(self, compressed: str) -> str:
        if not compressed.startswith("§{") or "} " not in compressed:
            return compressed
        header_end = compressed.index("} ")
        body = compressed[header_end + 2:]
        for phrase, sigil in self.mappings.items():
            body = body.replace(sigil, phrase)
        return body

class EvolutionaryArena:
    """Genetic evolution loop for discovering Pareto-optimal token representations."""

    SIGIL_POOL = ["§0", "§1", "§2", "§3", "§4", "§5", "§6", "§7", "§8", "§9", "+", "*", "@", "!", "~"]

    def __init__(self, db: Optional[BenchmarkDB] = None, tokenizer_bridge: Optional[MultiTokenizerBridge] = None):
        self.db = db or BenchmarkDB()
        self.bridge = tokenizer_bridge or MultiTokenizerBridge()
        self.pareto_frontier: List[Dict[str, Any]] = []

    def compute_fitness(self, reduction_pct: float, fidelity: float) -> float:
        if fidelity < 0.90:
            return 0.0
        return (reduction_pct / 100.0) * (fidelity ** 10)

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
            self.pareto_frontier.sort(key=lambda x: x["fitness"], reverse=True)

        return {
            "candidate_id": candidate_id,
            "fitness": round(fitness, 4),
            "is_pareto_optimal": is_pareto,
        }

    def evaluate_genome(self, genome: TokenGenome, corpus: str) -> Dict[str, Any]:
        compressed = genome.compress(corpus)
        decompressed = genome.decompress(compressed)

        # Multi-tokenizer reduction benchmark
        bench = self.bridge.benchmark_compression(corpus, compressed)
        avg_reduction = sum(b["reduction_percent"] for b in bench.values()) / max(len(bench), 1)

        # Semantic fidelity evaluation
        matcher = difflib.SequenceMatcher(None, corpus.strip(), decompressed.strip())
        fidelity = matcher.ratio()

        genome.token_reduction_pct = avg_reduction
        genome.semantic_fidelity = fidelity
        genome.fitness = self.compute_fitness(avg_reduction, fidelity)

        # Track in Pareto Frontier
        is_pareto = False
        if fidelity >= 0.99 and (not self.pareto_frontier or avg_reduction >= max(p["reduction_pct"] for p in self.pareto_frontier)):
            is_pareto = True
            entry = {
                "genome_id": genome.genome_id,
                "reduction_pct": round(avg_reduction, 2),
                "fidelity": round(fidelity, 4),
                "fitness": round(genome.fitness, 4),
                "mappings_count": len(genome.mappings),
            }
            self.pareto_frontier.append(entry)
            self.pareto_frontier.sort(key=lambda x: x["reduction_pct"], reverse=True)

        return {
            "genome_id": genome.genome_id,
            "avg_reduction_pct": avg_reduction,
            "fidelity": fidelity,
            "fitness": genome.fitness,
            "is_pareto": is_pareto,
            "benchmarks": bench,
        }

    def mutate(self, genome: TokenGenome, candidate_phrases: List[str]) -> TokenGenome:
        new_mappings = dict(genome.mappings)
        mutation_type = random.choice(["add", "remove", "swap_sigil"])

        if mutation_type == "add" and candidate_phrases:
            phrase = random.choice(candidate_phrases)
            sigil = random.choice(self.SIGIL_POOL)
            new_mappings[phrase] = sigil
        elif mutation_type == "remove" and new_mappings:
            phrase = random.choice(list(new_mappings.keys()))
            del new_mappings[phrase]
        elif mutation_type == "swap_sigil" and new_mappings:
            phrase = random.choice(list(new_mappings.keys()))
            new_mappings[phrase] = random.choice(self.SIGIL_POOL)

        return TokenGenome(f"{genome.genome_id}_mut", new_mappings, genome.tier_level)

    def crossover(self, parent1: TokenGenome, parent2: TokenGenome) -> TokenGenome:
        all_keys = list(set(list(parent1.mappings.keys()) + list(parent2.mappings.keys())))
        child_mappings = {}
        for k in all_keys:
            if random.random() < 0.5:
                if k in parent1.mappings:
                    child_mappings[k] = parent1.mappings[k]
            else:
                if k in parent2.mappings:
                    child_mappings[k] = parent2.mappings[k]

        return TokenGenome(f"{parent1.genome_id}_x_{parent2.genome_id}", child_mappings)

    def run_evolution_cycle(
        self,
        population: List[TokenGenome],
        corpus: str,
        candidate_phrases: List[str],
        generations: int = 3,
        cycle_id: int = 5,
    ) -> Dict[str, Any]:
        current_pop = list(population)
        best_overall = None

        for gen in range(generations):
            evals = [self.evaluate_genome(g, corpus) for g in current_pop]
            current_pop.sort(key=lambda g: g.fitness, reverse=True)
            elites = current_pop[:max(2, len(current_pop) // 2)]

            if best_overall is None or elites[0].fitness > best_overall.fitness:
                best_overall = elites[0]

            # Generate next population
            next_pop = [elites[0]]  # Elitism
            while len(next_pop) < len(population):
                p1, p2 = random.sample(elites, 2 if len(elites) >= 2 else 1) * (1 if len(elites) >= 2 else 2)
                child = self.crossover(p1, p2)
                if random.random() < 0.7:
                    child = self.mutate(child, candidate_phrases)
                next_pop.append(child)
            current_pop = next_pop

        # Record winning run into SQLite BenchmarkDB
        if best_overall:
            best_eval = self.evaluate_genome(best_overall, corpus)
            self.db.record_run(
                cycle_id=cycle_id,
                feature_name=f"Autonomous Evolution Arena (Pareto Elite: {best_overall.genome_id})",
                codec_id="evo-arena-tier5",
                tier_level=5,
                metrics_by_tokenizer=best_eval["benchmarks"],
                dataset_name="evolutionary_search_corpus",
                fidelity_score=best_overall.semantic_fidelity,
            )

        return {
            "best_genome_id": best_overall.genome_id if best_overall else None,
            "best_reduction_pct": best_overall.token_reduction_pct if best_overall else 0.0,
            "best_fidelity": best_overall.semantic_fidelity if best_overall else 1.0,
            "pareto_frontier": self.pareto_frontier,
        }
