import pytest
from services.researcher.neural_prefix import BytePackedNeuralPrefixEngine
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_neural_prefix_compression_and_roundtrip():
    engine = BytePackedNeuralPrefixEngine()
    prompt = (
        "You are a helpful, obedient, and precise AI assistant. Follow all instructions meticulously. "
        "Never hallucinate facts. Always respond with accurate structured output.\n\n"
        "User: Please summarize the latest logs."
    )

    compressed = engine.compress(prompt)
    assert "§P0" in compressed
    assert "You are a helpful, obedient" not in compressed

    restored = engine.decompress(compressed)
    assert restored == prompt

def test_custom_prefix_registration():
    engine = BytePackedNeuralPrefixEngine()
    custom_block = "<agent_rules>\nRule A: Do not modify submodules.\nRule B: No git push.\n</agent_rules>"
    engine.register_prefix("§P9", custom_block)

    text = f"{custom_block}\nTask: Start cycle 15."
    compressed = engine.compress(text)
    assert compressed == "§P9\nTask: Start cycle 15."

    decompressed = engine.decompress(compressed)
    assert decompressed == text

def test_50k_token_long_context_prefix_benchmark():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    engine = BytePackedNeuralPrefixEngine(db=db, bridge=bridge)

    p0 = engine.DEFAULT_PREFIX_REGISTRY["§P0"]
    p1 = engine.DEFAULT_PREFIX_REGISTRY["§P1"]
    p2 = engine.DEFAULT_PREFIX_REGISTRY["§P2"]
    prefix_block = f"{p0}\n\n{p1}\n\n{p2}"

    # Generate 50 multi-agent prompts with repetitive system instructions
    contexts = [f"{prefix_block}\n\nTurn {i}: Process agent task payload." for i in range(50)]

    res = engine.benchmark_prefix_compression(
        long_contexts=contexts,
        cycle_id=15,
        dataset_name="50_agent_sessions_prefix_benchmark",
    )

    bench = res["benchmarks"]
    assert bench["o200k_base"]["reduction_percent"] > 80.0
    assert bench["cl100k_base"]["reduction_percent"] > 80.0

    # Verify SQLite logging
    latest = db.get_latest_metric("neural-prefix-tier15", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 80.0
