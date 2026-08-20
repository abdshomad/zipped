import pytest
from services.researcher.agent_cache_proxy import AgentCacheProxy
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_agent_cache_proxy_interception_and_retrieval():
    proxy = AgentCacheProxy()

    large_tool_output = (
        "Traceback (most recent call last):\n"
        "  File 'server.py', line 142, in process_request\n"
        "    handler.execute()\n"
        "ValueError: Invalid database connection credentials."
    )

    handle = proxy.intercept_tool_output("run_command", large_tool_output)
    assert handle.startswith("§CCR[")
    assert "FAIL:" in handle

    # Extract handle id
    handle_id = handle.split("[")[1].split(":")[0]
    restored = proxy.retrieve_cached_context(handle_id)
    assert restored == large_tool_output

def test_agent_template_absorption():
    proxy = AgentCacheProxy()
    template = "You are an autonomous AI coding agent designed to solve complex software engineering tasks."
    absorbed = proxy.absorb_prompt_template(template)
    assert absorbed.startswith("§TPL[")

def test_agent_cache_proxy_50_tool_session_benchmark_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    proxy = AgentCacheProxy(db=db, bridge=bridge)

    tool_executions = []
    for i in range(50):
        if i % 3 == 0:
            payload = "\n".join([f'{{"file_{j}.py": {{"size": {j * 100}, "status": "active"}}}}' for j in range(10)])
            tool_executions.append(("list_dir", payload))
        elif i % 3 == 1:
            payload = f"Database log record {i}: Transaction commit confirmed with hash sha256_{i * 9999}"
            tool_executions.append(("run_command", payload))
        else:
            payload = f"Traceback (most recent call last):\n  File 'worker_{i}.py', line 22\nAssertionError: Invariant failed at step {i}"
            tool_executions.append(("run_command", payload))

    res = proxy.benchmark_agent_session(
        tool_executions=tool_executions,
        cycle_id=26,
        dataset_name="50_tool_execution_agent_session",
    )

    assert res["total_tool_calls"] == 50
    assert res["cached_records_count"] <= 50

    bench = res["benchmarks"]
    assert bench["o200k_base"]["reduction_percent"] > 75.0
    assert bench["cl100k_base"]["reduction_percent"] > 75.0

    # Verify SQLite logging
    latest = db.get_latest_metric("agent-cache-proxy-tier26", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 75.0
