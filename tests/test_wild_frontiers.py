import pytest
from services.researcher.hypergraph import ZHyperGraph
from services.researcher.arena import EvolutionaryArena
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_z_hypergraph_multi_reference_token_efficiency():
    graph = ZHyperGraph()
    graph.add_node("1", "User", role="admin")
    graph.add_node("2", "DB", engine="pg")
    graph.add_node("3", "Rep", id="4092")
    graph.add_node("4", "Audit", type="log")
    
    graph.add_edge("1", "export", "3", condition="@#2")
    graph.add_edge("2", "!alert(#1)", "1", condition="?timeout")
    graph.add_edge("2", "deliver(#3,#1)+log(#4)", "3", condition="?ok")

    compact_str = graph.encode()
    assert "§1:User" in compact_str
    assert "(#1)>export>(#3)" in compact_str

    bridge = MultiTokenizerBridge()
    long_text = """
    The system administrator (user ID #1) initiates an export of the monthly billing report (report ID #4092) from the primary Postgres database server.
    The primary Postgres database server processes the request for report ID #4092 and generates the export data.
    If the primary Postgres database server encounters a timeout while generating report ID #4092, the primary Postgres database server sends a timeout error alert back to the system administrator (user ID #1).
    Otherwise, upon successful export of report ID #4092, the primary Postgres database server delivers report ID #4092 to the system administrator (user ID #1) and logs the event to the audit trail repository.
    """
    bench = bridge.benchmark_compression(long_text, compact_str)

    # In multi-reference contexts, hypergraph back-referencing achieves >= 40% token reduction
    for tok in ["o200k_base", "cl100k_base"]:
        assert bench[tok]["reduction_percent"] > 40.0

def test_evolutionary_arena_fitness_and_pareto():
    arena = EvolutionaryArena()
    # High reduction, perfect accuracy
    res1 = arena.evaluate_candidate("z-lang-v1", "§1:U1>!exec", 75.0, 1.0)
    assert res1["is_pareto_optimal"] is True
    assert res1["fitness"] == 0.75

    # High reduction, but hallucination / low accuracy
    res2 = arena.evaluate_candidate("hallucinatory-v1", "§bad", 90.0, 0.85)
    assert res2["is_pareto_optimal"] is False
    assert res2["fitness"] == 0.0
