import pytest
from services.researcher.learning_engine import ContinuousLearningEngine
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_learning_engine_pattern_mining_and_lossless():
    engine = ContinuousLearningEngine(min_frequency=2)

    turn1 = "The authentication service verifies security tokens before access."
    turn2 = "The authentication service verifies security tokens for all requests."

    engine.observe(turn1)
    assert len(engine.learned_rules) == 0  # Frequency is 1

    engine.observe(turn2)
    assert len(engine.learned_rules) > 0  # Frequency is 2, minted sigils

    c = engine.compress(turn1)
    assert "§" in c

    d = engine.decompress(c)
    assert d == turn1

def test_learning_engine_50_turn_stream_benchmark_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    engine = ContinuousLearningEngine(db=db, bridge=bridge, min_frequency=2)

    base_phrases = [
        "The distributed cluster supervisor monitors worker node heartbeats across cloud regions.",
        "The database commit pipeline asserts bidirectional transactional invariants across all shards.",
        "Autonomous agents exchange high-density synthetic interlingua frames for instant collaboration.",
        "Error logs indicate connection reset during websocket handshake with backend authentication server.",
    ]

    turns = []
    for i in range(50):
        phrase = base_phrases[i % len(base_phrases)]
        turns.append(f"Turn {i}: {phrase} Status code: {200 if i % 2 == 0 else 500}.")

    res = engine.benchmark_continuous_stream(
        turns=turns,
        cycle_id=29,
        dataset_name="50_turn_agent_streaming_session",
    )

    assert res["total_turns"] == 50
    assert res["learned_rules_count"] >= 4

    bench = res["benchmarks"]
    assert bench["o200k_base"]["reduction_percent"] > 20.0
    assert bench["cl100k_base"]["reduction_percent"] > 20.0

    # Verify SQLite logging
    latest = db.get_latest_metric("continuous-learning-tier29", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 20.0
