import pytest
from services.evaluator.reasoning_evaluator import ZeroShotReasoningEvaluator
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_zero_shot_schema_query_extraction():
    evaluator = ZeroShotReasoningEvaluator()
    schema_payload = "§[id,name,role,department] 1,Alice,admin,eng;2,Bob,developer,eng;3,Charlie,designer,prod"

    assert evaluator.evaluate_schema_query(schema_payload, "2", "name") == "Bob"
    assert evaluator.evaluate_schema_query(schema_payload, "1", "role") == "admin"
    assert evaluator.evaluate_schema_query(schema_payload, "3", "department") == "prod"
    assert evaluator.evaluate_schema_query(schema_payload, "99", "name") is None

def test_zero_shot_zlang_frame_extraction():
    evaluator = ZeroShotReasoningEvaluator()
    zlang_payload = "⟨+author write *doc @repo !commit⟩"

    frame = evaluator.evaluate_zlang_frame(zlang_payload, "author")
    assert frame is not None
    assert frame["agent"] == "author"
    assert frame["action"] == "write"
    assert frame["patient"] == "doc"
    assert frame["locus"] == "repo"

def test_zero_shot_hypergraph_relationship_query():
    evaluator = ZeroShotReasoningEvaluator()
    graph_payload = "§1:Admin §2:DB §3:Report (#1)>export>(#3)⌁auth_ok (#2)>log>(#1)"

    edge = evaluator.evaluate_hypergraph_edge(graph_payload, "1", "3")
    assert edge is not None
    assert edge["action"] == "export"
    assert edge["condition"] == "auth_ok"

def test_full_reasoning_benchmark_suite():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    evaluator = ZeroShotReasoningEvaluator()

    test_cases = [
        {"type": "schema", "payload": "§[id,name,role] 10,Diana,lead;20,Evan,analyst", "id": "10", "field": "name", "expected": "Diana"},
        {"type": "schema", "payload": "§[id,name,role] 10,Diana,lead;20,Evan,analyst", "id": "20", "field": "role", "expected": "analyst"},
        {"type": "zlang", "payload": "⟨+user submit *ticket @portal⟩", "agent": "user", "expected": {"agent": "user", "action": "submit", "patient": "ticket", "locus": "portal"}},
        {"type": "hypergraph", "payload": "(#10)>replicate>(#20)⌁sync_ok", "source": "10", "target": "20", "expected": {"source": "10", "target": "20", "action": "replicate", "condition": "sync_ok"}},
    ]

    res = evaluator.evaluate_benchmark_suite(test_cases)
    assert res["passed"] is True
    assert res["accuracy"] == 1.0

    # Multi-tokenizer benchmark measurement for test payloads
    combined_raw = "User Diana is lead with ID 10. User Evan is analyst with ID 20. User submits ticket at portal. Node 10 replicates to node 20 upon sync_ok."
    combined_compressed = "§[id,name,role] 10,Diana,lead;20,Evan,analyst ⟨+user submit *ticket @portal⟩ (#10)>replicate>(#20)⌁sync_ok"
    bench = bridge.benchmark_compression(combined_raw, combined_compressed)

    db.record_run(
        cycle_id=11,
        feature_name="Multi-Model Zero-Shot Reasoning Harness",
        codec_id="zero-shot-evaluator-tier11",
        tier_level=11,
        metrics_by_tokenizer=bench,
        dataset_name="zero_shot_logic_benchmark",
        fidelity_score=res["accuracy"],
    )
