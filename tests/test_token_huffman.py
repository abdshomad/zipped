import pytest
from services.researcher.token_huffman import TokenHuffmanTreeCodec
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_token_huffman_compression_and_decompression():
    codec = TokenHuffmanTreeCodec()

    para = (
        "The distributed authentication and authorization gateway module verifies requests. "
        "The distributed authentication and authorization gateway module verifies requests."
    )

    compressed = codec.compress(para)
    assert compressed.startswith("§H{")
    assert "§0" in compressed

    restored = codec.decompress(compressed)
    assert restored == para

def test_token_huffman_heterogeneous_benchmark_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    codec = TokenHuffmanTreeCodec(db=db, bridge=bridge)

    section_a = (
        "In enterprise cloud environments, the centralized security gateway verifies incoming credentials "
        "and coordinates multi-tenant isolation policies across virtualized compute instances."
    )
    section_b = (
        "The persistent transactional audit logging engine commits state verification records "
        "to the distributed database cluster while asserting bidirectional lossless invariants."
    )

    corpus = "\n\n".join([f"Block {i}:\n{section_a}\n{section_b}" for i in range(30)])

    res = codec.benchmark_huffman_corpus(
        corpus=corpus,
        cycle_id=22,
        dataset_name="token_huffman_entropy_corpus",
    )

    bench = res["benchmarks"]
    assert bench["o200k_base"]["reduction_percent"] > 50.0
    assert bench["cl100k_base"]["reduction_percent"] > 50.0

    # Exact roundtrip verification
    compressed = codec.compress(corpus)
    restored = codec.decompress(compressed)
    assert restored == corpus

    # Verify SQLite logging
    latest = db.get_latest_metric("token-huffman-tier22", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 50.0
