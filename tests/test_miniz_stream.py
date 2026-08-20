import pytest
from services.researcher.miniz_stream import MinizStreamingBuffer
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_miniz_streaming_chunk_compression_and_latency():
    stream_buf = MinizStreamingBuffer()

    chunk1 = "In modern deployments, the authentication gateway verifies user credentials "
    chunk2 = "and persists transaction trace records to storage by the way."

    c1 = stream_buf.append_chunk(chunk1)
    c2 = stream_buf.append_chunk(chunk2)

    assert "§S0" in c1.compressed_text
    assert "§S1" in c2.compressed_text
    assert "btw" in c2.compressed_text
    assert c1.latency_ms < 1.0  # Sub-millisecond execution

    flushed = stream_buf.flush()
    restored = stream_buf.decompress_stream(flushed)
    assert restored == (chunk1 + chunk2)

def test_miniz_streaming_continuous_benchmark_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    stream_buf = MinizStreamingBuffer(db=db, bridge=bridge)

    chunk_pool = [
        "the authentication gateway verifies user credentials ",
        "and persists transaction trace records to storage. ",
        "the distributed cluster supervisor monitors nodes ",
        "and reports periodic health verification heartbeats. ",
        "as soon as possible, in my opinion. ",
    ]

    # Generate 100 streaming chunks
    stream_chunks = [chunk_pool[i % len(chunk_pool)] for i in range(100)]

    res = stream_buf.benchmark_stream(
        stream_chunks=stream_chunks,
        cycle_id=24,
        dataset_name="100_chunk_continuous_stream",
    )

    assert res["total_chunks"] == 100
    assert res["avg_latency_ms"] < 0.1  # Fast streaming throughput

    bench = res["benchmarks"]
    assert bench["o200k_base"]["reduction_percent"] > 45.0
    assert bench["cl100k_base"]["reduction_percent"] > 45.0

    # Verify SQLite logging
    latest = db.get_latest_metric("miniz-stream-tier24", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 45.0
