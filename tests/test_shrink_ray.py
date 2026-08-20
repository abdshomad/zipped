import pytest
from services.researcher.shrink_ray import UniversalContextShrinkRay
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_shrink_ray_cascading_compression():
    shrink_ray = UniversalContextShrinkRay()

    p0 = shrink_ray.prefix_engine.DEFAULT_PREFIX_REGISTRY["§P0"]
    input_text = (
        f"{p0}\n\n"
        "The author who writes the written document in the repository by the way as soon as possible.\n"
        '[{"id": 1, "name": "Alice", "role": "admin"}, {"id": 2, "name": "Bob", "role": "dev"}]'
    )

    compressed = shrink_ray.compress(input_text)

    # Must contain neural prefix macro
    assert "§P0" in compressed
    # Must contain Z-Lang sigils
    assert "+write" in compressed
    assert "*write" in compressed
    assert "@repo" in compressed
    # Must contain colloquial shorthand
    assert "btw" in compressed
    assert "asap" in compressed
    # Must contain tabular schema
    assert "§[id,name,role]" in compressed

def test_shrink_ray_master_corpus_benchmark_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    shrink_ray = UniversalContextShrinkRay(db=db, bridge=bridge)

    p0 = shrink_ray.prefix_engine.DEFAULT_PREFIX_REGISTRY["§P0"]
    p1 = shrink_ray.prefix_engine.DEFAULT_PREFIX_REGISTRY["§P1"]
    system_header = f"{p0}\n\n{p1}\n\n"

    turn_template = (
        "The author who writes the written document in the repository by the way as soon as possible.\n"
        '[{"id": 101, "event": "auth_login", "status": "ok"}, {"id": 102, "event": "audit_write", "status": "ok"}]\n'
        "In my opinion, too long didn't read, with respect to the storage repository."
    )

    # Construct comprehensive multi-modal corpus
    full_corpus = system_header + "\n\n".join([f"Turn {i}:\n{turn_template}" for i in range(50)])

    res = shrink_ray.benchmark_shrink_ray(
        corpus=full_corpus,
        cycle_id=18,
        dataset_name="master_100k_token_corpus",
    )

    bench = res["benchmarks"]
    assert bench["o200k_base"]["reduction_percent"] > 40.0
    assert bench["cl100k_base"]["reduction_percent"] > 40.0

    # Verify SQLite logging
    latest = db.get_latest_metric("shrink-ray-tier18", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 40.0
