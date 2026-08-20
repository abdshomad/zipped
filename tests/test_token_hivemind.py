import pytest
from services.researcher.hivemind import TokenHiveMind, SwarmAgentWorker, MacroProposal
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_swarm_agent_worker_discovery():
    worker = SwarmAgentWorker("agent_alpha")
    text = (
        "the authentication gateway verifies user credentials for access control. "
        "the authentication gateway verifies user credentials for access control."
    )
    proposals = worker.discover_candidates(text)
    assert len(proposals) > 0
    assert any("the authentication gateway" in p.phrase for p in proposals)

def test_token_hivemind_consensus_promotion():
    hivemind = TokenHiveMind()

    p1 = MacroProposal("distributed multi-agent system", "§H0", 10, "worker_1")
    p2 = MacroProposal("distributed multi-agent system", "§H0", 10, "worker_2")
    p3 = MacroProposal("rare one-off phrase", "§H1", 2, "worker_3")

    hivemind.submit_proposals([p1, p3])
    hivemind.submit_proposals([p2])

    consensus = hivemind.reach_consensus(min_votes=2)
    assert "distributed multi-agent system" in consensus
    assert "rare one-off phrase" not in consensus

def test_10_agent_swarm_hivemind_evolution_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    hivemind = TokenHiveMind(db=db, bridge=bridge)

    para = (
        "In modern cloud infrastructure, the distributed authentication gateway verifies credentials "
        "and the centralized audit logger persists transaction trace records to persistent storage."
    )
    corpus = "\n".join([para] * 20)

    # Spawn 10 swarm agents
    agents = [SwarmAgentWorker(f"agent_{i}") for i in range(10)]

    res = hivemind.run_swarm_evolution(
        agents=agents,
        corpus=corpus,
        cycle_id=17,
        dataset_name="10_agent_swarm_evolution",
    )

    assert res["consensus_macros_count"] > 0
    bench = res["benchmarks"]
    assert bench["o200k_base"]["reduction_percent"] > 40.0

    # Test roundtrip decompression
    compressed = hivemind.compress(corpus)
    restored = hivemind.decompress(compressed)
    assert restored == corpus

    # Verify SQLite logging
    latest = db.get_latest_metric("token-hivemind-tier17", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 40.0
