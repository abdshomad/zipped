import pytest
from services.researcher.daemon import ContextCompressionDaemon, SlidingContextBuffer
from services.evaluator.db import BenchmarkDB

def test_sliding_context_buffer_pinning():
    buffer = SlidingContextBuffer(token_budget=500)
    system_msg = buffer.add_message("system", "You are the central coordinator agent.", pinned=True)
    turn1 = buffer.add_message("user", "Please verify the author who writes the written document in the repository by the way.")
    turn2 = buffer.add_message("assistant", "Acknowledged and verified status update.")
    turn3 = buffer.add_message("user", "Next task: review the logs.")

    res = buffer.compact()

    # Pinned system message must remain unmodified
    assert system_msg.compressed is None
    # Turn 1 should be compacted with Z-Lang / shorthand
    assert turn1.compressed is not None
    assert "+write" in turn1.compressed
    assert "btw" in turn1.compressed
    # Turn 2 ack should be collapsed
    assert turn2.compressed == "§ACK:ok"

def test_50_turn_agent_simulation_and_budget_enforcement():
    db = BenchmarkDB()
    daemon = ContextCompressionDaemon(db=db, token_budget=1000)

    # 1. Pinned core instructions
    daemon.process_turn("system", "Core Directive: Coordinate multi-agent tasks with zero hallucination.", pinned=True)

    # 2. Simulate 49 conversational multi-agent turns
    for turn in range(1, 50):
        if turn % 2 == 1:
            content = f"Turn {turn}: The author who writes the written document in the repository must send to the logging service by the way."
            daemon.process_turn("user", content)
        else:
            content = f"Turn {turn}: The logging service received status update and the audit logs in the database storage are acknowledged and verified."
            daemon.process_turn("assistant", content)

    # Inspect final compaction state
    active_tokens = daemon.buffer.count_tokens()
    raw_tokens = daemon.buffer.count_uncompressed_tokens()

    # Active token footprint must stay strictly within budget (< 1000 tokens)
    assert active_tokens["o200k_base"] <= 1000
    assert raw_tokens["o200k_base"] > 1200

    # Record benchmark in SQLite
    bench = daemon.record_session_benchmark(cycle_id=9, session_id="50_turn_simulation")
    assert bench["o200k_base"]["compressed_tokens"] < bench["o200k_base"]["original_tokens"]

    # Verify SQLite record exists
    latest = db.get_latest_metric("context-daemon-tier9", "o200k_base")
    assert latest is not None
