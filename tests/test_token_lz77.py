import pytest
from services.researcher.token_lz77 import TokenLZ77Codec
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_token_lz77_turn_compression_and_decompression():
    codec = TokenLZ77Codec()

    turn0 = (
        "Agent: Executed routine node inspection.\n"
        "System: The authentication gateway verifies user credentials."
    )
    turn1 = "Agent: Checked status update."
    turn2 = (
        "Agent: Executed routine node inspection.\n"
        "System: The authentication gateway verifies user credentials."
    )

    turns = [turn0, turn1, turn2]
    comp_turns = codec.compress_turns(turns)

    # Turn 2 should contain a relative back-reference to Turn 0 (delta = 2)
    assert comp_turns[2] == "§-2"

    # Decompression must be exact
    restored = codec.decompress_turns(comp_turns)
    assert restored == turns

def test_token_lz77_50_turn_benchmark_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    codec = TokenLZ77Codec(db=db, bridge=bridge)

    system_header = "System: The distributed cluster supervisor monitors worker nodes and reports health heartbeats."
    dialogue_template = (
        "Agent: Executed routine node inspection.\n"
        "User: Confirm status update.\n"
        f"{system_header}"
    )

    turns = [dialogue_template for _ in range(50)]

    res = codec.benchmark_lz77_session(
        turns=turns,
        cycle_id=21,
        dataset_name="50_turn_lz77_session",
    )

    assert res["total_turns"] == 50
    bench = res["benchmarks"]
    assert bench["o200k_base"]["reduction_percent"] > 75.0
    assert bench["cl100k_base"]["reduction_percent"] > 75.0

    # Full text roundtrip verification
    raw_text = "\n\n".join(turns)
    comp_text = codec.compress(raw_text)
    restored_text = codec.decompress(comp_text)
    assert restored_text == raw_text

    # Verify SQLite logging
    latest = db.get_latest_metric("token-lz77-tier21", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 75.0
