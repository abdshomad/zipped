import pytest
from services.researcher.super_arena import SuperArenaCoordinator
from services.evaluator.db import BenchmarkDB

def test_super_arena_tournament_and_dashboard():
    db = BenchmarkDB()
    coordinator = SuperArenaCoordinator(db=db)

    test_suites = {
        "suite_shorthand": {
            "original": "By the way, as soon as possible, away from keyboard.",
            "compressed": "btw asap afk",
            "codec_id": "shorthand-level1",
            "tier_level": 1,
            "fidelity": 1.0,
        },
        "suite_zlang": {
            "original": "the author who writes the written document in the repository",
            "compressed": "+write *write @repo",
            "codec_id": "zlang-tier4",
            "tier_level": 4,
            "fidelity": 0.99,
        },
    }

    results = coordinator.run_tournament(test_suites, cycle_id=10)
    assert "suite_shorthand" in results
    assert "suite_zlang" in results

    report = coordinator.generate_dashboard_report()
    assert report["summary"]["total_runs"] > 0
    assert report["pareto_count"] >= 4

    ascii_dashboard = coordinator.render_ascii_dashboard()
    assert "ZIPPED GLOBAL PARETO FRONTIER DASHBOARD" in ascii_dashboard
    assert "Tier 1" in ascii_dashboard
    assert "Tier 4" in ascii_dashboard
