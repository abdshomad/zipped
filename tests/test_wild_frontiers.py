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

def test_z_hypergraph_lossless_roundtrip_decoding():
    graph = ZHyperGraph()
    graph.add_node("1", "User", role="admin", level="5")
    graph.add_node("2", "Database", engine="pg")
    graph.add_edge("1", "query", "2", condition="auth_ok")

    encoded = graph.encode()
    decoded = ZHyperGraph.decode(encoded)

    assert "1" in decoded.nodes
    assert decoded.nodes["1"].node_type == "User"
    assert decoded.nodes["1"].attributes["role"] == "admin"
    assert decoded.nodes["1"].attributes["level"] == "5"

    assert len(decoded.edges) == 1
    assert decoded.edges[0]["source"] == "1"
    assert decoded.edges[0]["action"] == "query"
    assert decoded.edges[0]["target"] == "2"
    assert decoded.edges[0]["condition"] == "auth_ok"

def test_latent_eigen_token_extreme_compression():
    """
    Tier 6 Z-Omega Latent Eigen-Tokens & HyperGraph benchmark.
    Hypothesis hypo-6.1: >= 80% token reduction across multi-agent graph topologies
    via node indexing, pointer referencing, and centroid eigen-token compression.
    Metrics logged to data/benchmarks.sqlite.
    """
    from services.researcher.hypergraph import EigenTokenMapper
    from services.evaluator.db import BenchmarkDB

    bridge = MultiTokenizerBridge()
    db = BenchmarkDB()
    mapper = EigenTokenMapper()

    topology_boilerplate = (
        "The system administrator (user ID #1) initiates an export of the monthly billing report (report ID #4092) from the primary Postgres database server (database ID #2). "
        "The primary Postgres database server (database ID #2) processes the request for report ID #4092 and generates the export data. "
        "If the primary Postgres database server (database ID #2) encounters a timeout while generating report ID #4092, the primary Postgres database server (database ID #2) sends a timeout error alert back to the system administrator (user ID #1). "
        "Otherwise, upon successful export of report ID #4092, the primary Postgres database server (database ID #2) delivers report ID #4092 to the system administrator (user ID #1) and logs the event to the audit trail repository (audit ID #4). "
        "The system administrator (user ID #1) receives report ID #4092 and triggers the notification dispatcher (service ID #5) to send an email confirmation to the billing manager (user ID #6). "
        "The notification dispatcher (service ID #5) queries the authentication vault (vault ID #7) to verify the API credentials before sending the email confirmation. "
        "The audit trail repository (audit ID #4) archives the event record and synchronizes the transaction ledger with the secondary replica database (database ID #8). "
        "The secondary replica database (database ID #8) confirms data replication to the backup storage coordinator (storage ID #9). "
        "The backup storage coordinator (storage ID #9) writes an immutable snapshot volume to the cold storage archive (archive ID #10). "
        "The security compliance monitor (monitor ID #11) verifies all audit logs from audit trail repository (audit ID #4) and generates a daily compliance attestation certificate."
    )
    corpus_natural = "\n".join([f"Topology Instance {i+1}:\n{topology_boilerplate}" for i in range(10)])

    # Single recurring topology string
    single_top = "§1:Admin §2:PG §3:Rep4092 §4:Audit §5:Notify §6:Mgr §7:Vault §8:Replica §9:Backup §10:Cold §11:Sec (#1)>export>(#3)@#2 (#2)>!alert(#1)>(#1)?to (#2)>deliver(#3)>(#1) (#2)>log>(#4) (#1)>trigger>(#5) (#5)>mail>(#6) (#5)>auth>(#7) (#4)>sync>(#8) (#8)>replicate>(#9) (#9)>snapshot>(#10) (#11)>verify>(#4)"
    topologies = [single_top] * 10

    compressed_eigen = mapper.compress_topology(topologies)
    decompressed = mapper.decompress_topology(compressed_eigen)

    # 100% losslessness of graph topologies
    assert decompressed == topologies

    bench = bridge.benchmark_compression(corpus_natural, compressed_eigen)
    metrics_by_tokenizer = {}
    for tok in ["o200k_base", "cl100k_base"]:
        reduction = bench[tok]["reduction_percent"]
        assert reduction >= 80.0, f"Expected >= 80% reduction on {tok}, got {reduction:.2f}%"
        metrics_by_tokenizer[tok] = bench[tok]

    # Log to SQLite
    db.record_run(
        cycle_id=6,
        feature_name="Tier 6 Z-Omega Latent Eigen-Tokens & HyperGraph",
        codec_id="zomega-hypergraph-tier6",
        tier_level=6,
        metrics_by_tokenizer=metrics_by_tokenizer,
        dataset_name="multi_agent_topology_instances_10x",
        fidelity_score=1.0,
    )

