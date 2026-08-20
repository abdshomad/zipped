import pytest
from services.researcher.codebook import LatentVectorCodebook
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_codebook_registration_and_roundtrip():
    codebook = LatentVectorCodebook()
    anchor = codebook.register_concept(
        "vector_search",
        r"the approximate nearest neighbor high-dimensional vector search index",
        "the approximate nearest neighbor high-dimensional vector search index",
    )

    sample = (
        "In production deployment, the distributed authentication and authorization gateway module connects to "
        "the approximate nearest neighbor high-dimensional vector search index."
    )

    compressed = codebook.compress(sample)
    assert "§C0" in compressed
    assert anchor in compressed

    restored = codebook.decompress(compressed)
    assert restored == sample

def test_codebook_distillation_benchmark_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    codebook = LatentVectorCodebook(db=db, bridge=bridge)

    para = (
        "In mission-critical enterprise systems, the distributed authentication and authorization gateway module verifies requests. "
        "Subsequently, the centralized audit logger transaction persistence engine writes traces to "
        "the fault-tolerant distributed relational database storage cluster through "
        "the asynchronous message broker and event stream coordinator while validating "
        "the bidirectional 100% lossless invariant verification assertion check."
    )

    corpus = "\n\n".join([f"Session {i}:\n{para}" for i in range(30)])

    res = codebook.benchmark_codebook(
        corpus=corpus,
        cycle_id=20,
        dataset_name="domain_knowledge_distillation_corpus",
    )

    bench = res["benchmarks"]
    assert bench["o200k_base"]["reduction_percent"] > 40.0
    assert bench["cl100k_base"]["reduction_percent"] > 40.0

    # Verify SQLite logging
    latest = db.get_latest_metric("codebook-tier20", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 40.0
