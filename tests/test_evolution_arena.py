import pytest
from services.researcher.arena import EvolutionaryArena, TokenGenome
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_genome_compression_and_losslessness():
    mappings = {
        "the quick brown fox": "§0",
        "in machine learning": "§1",
    }
    genome = TokenGenome("g1", mappings)
    original = "in machine learning, the quick brown fox is used."
    compressed = genome.compress(original)
    decompressed = genome.decompress(compressed)

    assert "§0" in compressed
    assert "§1" in compressed
    assert decompressed == original

def test_mutation_and_crossover():
    arena = EvolutionaryArena()
    g1 = TokenGenome("p1", {"alpha": "§0", "beta": "§1"})
    g2 = TokenGenome("p2", {"gamma": "§2", "delta": "§3"})

    # Crossover test
    child = arena.crossover(g1, g2)
    assert len(child.mappings) > 0
    assert any(k in ["alpha", "beta", "gamma", "delta"] for k in child.mappings)

    # Mutation test
    candidates = ["epsilon", "zeta"]
    mutant = arena.mutate(g1, candidates)
    assert mutant.genome_id.endswith("_mut")

def test_evolution_cycle_discovers_pareto_elite():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    arena = EvolutionaryArena(db=db, tokenizer_bridge=bridge)

    para = (
        "In distributed multi-agent systems, the authentication gateway verifies credentials "
        "and the audit logger records persistent trace logs to the storage repository."
    )
    corpus = "\n".join([para] * 30)

    candidate_phrases = [
        "In distributed multi-agent systems",
        "the authentication gateway verifies credentials",
        "the audit logger records persistent trace logs",
        "to the storage repository",
    ]

    initial_population = [
        TokenGenome("seed_1", {candidate_phrases[0]: "§0", candidate_phrases[1]: "§1"}),
        TokenGenome("seed_2", {candidate_phrases[2]: "§2", candidate_phrases[3]: "§3"}),
        TokenGenome("seed_3", {candidate_phrases[0]: "§0", candidate_phrases[2]: "§2"}),
        TokenGenome("seed_4", {candidate_phrases[1]: "§1", candidate_phrases[3]: "§3"}),
    ]

    result = arena.run_evolution_cycle(
        population=initial_population,
        corpus=corpus,
        candidate_phrases=candidate_phrases,
        generations=4,
        cycle_id=5,
    )

    assert result["best_genome_id"] is not None
    assert result["best_reduction_pct"] > 30.0
    assert result["best_fidelity"] >= 0.99
    assert len(result["pareto_frontier"]) > 0

    # Verify SQLite record
    latest = db.get_latest_metric("evo-arena-tier5", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 30.0
