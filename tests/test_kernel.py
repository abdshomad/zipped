import pytest
from services.researcher.kernel import SelfSustainingEvolutionKernel
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_evolution_kernel_health_and_invariants():
    kernel = SelfSustainingEvolutionKernel()
    health = kernel.verify_health()

    assert health["status"] == "healthy"
    assert health["lossless_invariant_verified"] is True
    assert "o200k_base" in health["tokenizers_ready"]
    assert health["total_db_runs"] > 0

def test_evolution_kernel_continuous_loop_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    kernel = SelfSustainingEvolutionKernel(db=db, bridge=bridge)

    para = (
        "In modern distributed architectures, the centralized authentication gateway verifies security tokens "
        "and the audit logger records persistent trace records to long-term storage."
    )
    corpus = "\n".join([para] * 30)

    candidate_phrases = [
        "In modern distributed architectures",
        "the centralized authentication gateway verifies security tokens",
        "and the audit logger records persistent trace records",
        "to long-term storage",
    ]

    res = kernel.run_continuous_loop(
        corpus=corpus,
        candidate_phrases=candidate_phrases,
        steps=3,
        cycle_id=19,
    )

    assert res["total_steps"] == 3
    assert res["final_best_reduction_pct"] > 30.0

    # Verify SQLite logging
    latest = db.get_latest_metric("evo-arena-tier5", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 30.0
