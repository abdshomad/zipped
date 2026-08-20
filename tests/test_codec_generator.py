import pytest
from services.researcher.codec_generator import AutonomousCodecGenerator, EvolvedCodec
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_codec_generator_population_and_mutation():
    gen = AutonomousCodecGenerator()
    pop = gen.generate_initial_population(size=4)
    assert len(pop) == 4

    parent = pop[0]
    mutant = gen.mutate(parent, gen=1)
    assert mutant.generation == 1
    assert len(mutant.rules) > 0

    # Lossless verification
    test_text = "In enterprise cloud computing environments, the authentication gateway verifies user credentials."
    c = mutant.compress(test_text)
    d = mutant.decompress(c)
    assert d == test_text

def test_codec_generator_evolution_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    generator = AutonomousCodecGenerator(db=db, bridge=bridge)

    corpus = (
        "In enterprise cloud computing environments, the authentication gateway verifies user credentials "
        "and persists transaction trace records to storage asserting bidirectional lossless invariants across all test runs. "
        "The distributed cluster supervisor monitors nodes and reports periodic health verification heartbeats "
        "as soon as possible by the way in my opinion."
    ) * 10

    res = generator.benchmark_evolution(
        corpus=corpus,
        generations=10,
        cycle_id=28,
        dataset_name="evolved_codec_generation_suite",
    )

    assert res["rules_count"] >= 3
    bench = res["benchmarks"]
    assert bench["o200k_base"]["reduction_percent"] > 40.0
    assert bench["cl100k_base"]["reduction_percent"] > 40.0

    # Verify SQLite logging
    latest = db.get_latest_metric("evolved-codec-tier28", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 40.0
