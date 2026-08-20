import pytest
from services.researcher.interceptor import StreamContextInterceptor, ChunkWindowBuffer
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_cross_chunk_boundary_phrase_matching():
    buf = ChunkWindowBuffer()
    # "by the way" split across two chunks
    out1 = buf.append("Please acknowledge by the ")
    out2 = buf.append("way as soon as possible.")
    out3 = buf.flush()

    full_output = out1 + out2 + out3
    assert "btw" in full_output
    assert "asap" in full_output
    assert "by the way" not in full_output

def test_streaming_generator_processing():
    interceptor = StreamContextInterceptor()
    chunks = [
        "In my opinion, ",
        "the authentication gateway verifies credentials ",
        "and sends logs ",
        "to the storage repository.\n",
    ]

    compressed = list(interceptor.process_stream(iter(chunks)))
    result = "".join(compressed)
    assert "imo" in result
    assert "§0" in result
    assert "§2" in result

def test_10k_token_stream_benchmark_and_latency():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    interceptor = StreamContextInterceptor(db=db, bridge=bridge)

    para = (
        "The authentication gateway verifies credentials and the audit logger records "
        "persistent trace logs to the storage repository by the way as soon as possible.\n"
    )

    # Generate 500 chunks simulating a 10,000+ token real-time stream
    stream_chunks = []
    for _ in range(50):
        # Split paragraph into 10 small streaming chunks (2-5 words each)
        words = para.split(" ")
        for i in range(0, len(words), 2):
            stream_chunks.append(" ".join(words[i : i + 2]) + " ")

    assert len(stream_chunks) >= 500

    res = interceptor.benchmark_stream(
        stream_chunks=stream_chunks,
        cycle_id=13,
        stream_name="10k_streaming_simulation",
    )

    # Sub-millisecond latency requirement (< 0.5ms per chunk)
    assert res["avg_chunk_latency_ms"] < 0.5
    assert res["benchmarks"]["o200k_base"]["reduction_percent"] > 40.0

    # Verify SQLite logging
    latest = db.get_latest_metric("stream-interceptor-tier13", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 40.0
