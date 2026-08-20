import pytest
from services.researcher.arbiter import AdaptiveCompressionArbiter
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_arbiter_topology_classification():
    arbiter = AdaptiveCompressionArbiter()

    assert arbiter.classify_topology({"main.py": "print('hello')", "utils.py": "pass"}) == "repository"
    assert arbiter.classify_topology(["User: Hi", "Agent: Hello"]) == "dialogue"
    assert arbiter.classify_topology("### Query:\nWhy?\n\n### Uncompressed Context:\nSome doc.") == "rag_context"
    assert arbiter.classify_topology("Traceback (most recent call last):\n  File 'a.py'") == "tool_execution"
    assert arbiter.classify_topology("Plain regular text for compression.") == "unstructured_text"

def test_arbiter_dynamic_compression():
    arbiter = AdaptiveCompressionArbiter()

    # 1. Dialogue routing
    dialogue = ["System: Auth check.\nUser: Status."] * 5
    c_diag = arbiter.compress(dialogue)
    assert "§-" in c_diag

    # 2. Repository routing
    repo = {"app.py": "def start(): pass", "config.json": "{}"}
    c_repo = arbiter.compress(repo)
    assert c_repo.startswith("§DIR[")

    # 3. Tool execution routing
    tool_dump = "Traceback (most recent call last):\nValueError: bad"
    c_tool = arbiter.compress(tool_dump)
    assert c_tool.startswith("§CCR[")

def test_arbiter_poly_modal_suite_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    arbiter = AdaptiveCompressionArbiter(db=db, bridge=bridge)

    res = arbiter.benchmark_poly_modal_suite(cycle_id=27)

    assert res["avg_reduction_percent"] > 50.0
    assert "dialogue" in res["results_by_topology"]
    assert "repository" in res["results_by_topology"]
    assert "tool_execution" in res["results_by_topology"]

    # Verify SQLite logging
    latest = db.get_latest_metric("adaptive-arbiter-tier27", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 50.0
