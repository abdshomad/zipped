import pytest
from services.researcher.cross_evaluator import CrossModelFrontierEvaluator
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_joint_harmonic_mean_scoring():
    evaluator = CrossModelFrontierEvaluator()

    # Balanced reductions: 60% on o200k_base and 60% on cl100k_base -> Harmonic mean = 60.0
    benchmarks_balanced = {
        "o200k_base": {"reduction_percent": 60.0},
        "cl100k_base": {"reduction_percent": 60.0},
    }
    score_bal = evaluator.compute_joint_score(benchmarks_balanced)
    assert score_bal == 60.0

    # Imbalanced: 80% on o200k_base but only 20% on cl100k_base -> Harmonic mean ~ 32.0 (penalizes regression)
    benchmarks_imbalanced = {
        "o200k_base": {"reduction_percent": 80.0},
        "cl100k_base": {"reduction_percent": 20.0},
    }
    score_imbal = evaluator.compute_joint_score(benchmarks_imbalanced)
    assert score_imbal < 40.0

def test_pareto_dominance_filtering():
    evaluator = CrossModelFrontierEvaluator()

    candidates = [
        {
            "candidate_id": "dominated_low",
            "benchmarks": {
                "o200k_base": {"reduction_percent": 30.0},
                "cl100k_base": {"reduction_percent": 30.0},
            },
            "joint_score": 30.0,
        },
        {
            "candidate_id": "elite_high",
            "benchmarks": {
                "o200k_base": {"reduction_percent": 75.0},
                "cl100k_base": {"reduction_percent": 70.0},
            },
            "joint_score": 72.41,
        },
        {
            "candidate_id": "tradeoff_frontier",
            "benchmarks": {
                "o200k_base": {"reduction_percent": 80.0},
                "cl100k_base": {"reduction_percent": 65.0},
            },
            "joint_score": 71.72,
        },
    ]

    frontier = evaluator.filter_pareto_dominant(candidates)
    frontier_ids = [c["candidate_id"] for c in frontier]

    # "dominated_low" must be eliminated by "elite_high"
    assert "dominated_low" not in frontier_ids
    assert "elite_high" in frontier_ids
    assert "tradeoff_frontier" in frontier_ids

def test_multi_model_frontier_benchmark_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    evaluator = CrossModelFrontierEvaluator(db=db, bridge=bridge)

    para = (
        "In enterprise software architecture, the authentication gateway verifies user credentials "
        "and the audit logger persists transaction trace records to the database storage."
    )
    corpus = "\n".join([para] * 20)

    # Candidate 1: Z-Lang canonical representation
    c1_comp = "\n".join(["§Z[+auth *cred @gateway +log *audit @db]"] * 20)
    c1_eval = evaluator.evaluate_representation(corpus, c1_comp)
    c1_eval["candidate_id"] = "zlang_canonical"
    c1_eval["fidelity"] = 1.0

    # Candidate 2: Shorthand representation
    c2_comp = "\n".join(["auth gw verifies creds and audit log records traces to db"] * 20)
    c2_eval = evaluator.evaluate_representation(corpus, c2_comp)
    c2_eval["candidate_id"] = "shorthand_idioms"
    c2_eval["fidelity"] = 1.0

    candidates = [c1_eval, c2_eval]
    result = evaluator.benchmark_frontier_selection(candidates, cycle_id=16, dataset_name="cross_model_evaluation")

    assert result["frontier_count"] >= 1
    assert result["elite_candidate"]["candidate_id"] in ["shorthand_idioms", "zlang_canonical"]
    assert result["elite_candidate"]["joint_score"] > 45.0

    # Verify SQLite logging
    latest = db.get_latest_metric("cross-model-tier16", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 45.0
