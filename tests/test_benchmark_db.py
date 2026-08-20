import pytest
import os
from services.evaluator.db import BenchmarkDB

def test_benchmark_db_lifecycle(tmp_path):
    test_db = str(tmp_path / "test_metrics.sqlite")
    db = BenchmarkDB(test_db)

    # Record first run (baseline)
    metrics_run1 = {
        "o200k_base": {"original_tokens": 100, "compressed_tokens": 60, "reduction_percent": 40.0},
        "cl100k_base": {"original_tokens": 100, "compressed_tokens": 58, "reduction_percent": 42.0},
    }
    res1 = db.record_run(1, "shorthand-v1", "shorthand-level1", 1, metrics_run1)
    assert res1["o200k_base"]["delta_pct"] == 40.0

    # Record second run (improved version)
    metrics_run2 = {
        "o200k_base": {"original_tokens": 100, "compressed_tokens": 45, "reduction_percent": 55.0},
        "cl100k_base": {"original_tokens": 100, "compressed_tokens": 44, "reduction_percent": 56.0},
    }
    res2 = db.record_run(2, "shorthand-v2", "shorthand-level1", 1, metrics_run2)
    # Delta should be +15.0% for o200k_base
    assert res2["o200k_base"]["delta_pct"] == 15.0
    assert res2["cl100k_base"]["delta_pct"] == 14.0
