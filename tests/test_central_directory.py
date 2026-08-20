import pytest
from services.researcher.central_directory import CentralDirectoryManifestCodec
from services.evaluator.db import BenchmarkDB
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_central_directory_pack_and_random_access():
    codec = CentralDirectoryManifestCodec()

    repo = {
        "config.json": '{"env": "production", "port": 8080}',
        "auth.py": "def verify_token(t): return t == 'valid_token'",
        "logger.py": "def log_event(e): print(f'LOG: {e}')",
    }

    archive = codec.pack_repository(repo)
    assert archive.startswith("§DIR[")

    manifest = codec.get_manifest(archive)
    assert "config.json" in manifest
    assert "auth.py" in manifest
    assert "logger.py" in manifest

    # Random access single file extraction
    auth_content = codec.extract_file(archive, "auth.py")
    assert auth_content == "def verify_token(t): return t == 'valid_token'"

    # Extract all files losslessly
    all_restored = codec.extract_all(archive)
    assert all_restored == repo

def test_central_directory_repository_benchmark_and_db_logging():
    db = BenchmarkDB()
    bridge = MultiTokenizerBridge()
    codec = CentralDirectoryManifestCodec(db=db, bridge=bridge)

    # 20-file codebase simulation
    repo = {}
    for i in range(20):
        repo[f"module_{i}.py"] = (
            f"# Module {i} Implementation\n"
            f"class ServiceHandler{i}:\n"
            f"    def handle_request_{i}(self, data):\n"
            f"        return {{'status': 'ok', 'service_id': {i}, 'payload': data}}\n"
        )

    res = codec.benchmark_repository_indexing(
        files=repo,
        target_file="module_7.py",
        cycle_id=23,
        dataset_name="20_file_repository_random_access",
    )

    assert res["total_files"] == 20
    assert res["target_file"] == "module_7.py"

    bench = res["benchmarks"]
    assert bench["o200k_base"]["reduction_percent"] > 75.0
    assert bench["cl100k_base"]["reduction_percent"] > 75.0

    # Verify SQLite logging
    latest = db.get_latest_metric("central-dir-tier23", "o200k_base")
    assert latest is not None
    assert latest["reduction_pct"] > 75.0
