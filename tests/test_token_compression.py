import pytest
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge

def test_multi_tokenizer_token_counting():
    bridge = MultiTokenizerBridge()
    text = "By the way, as far as I know, I will be away from keyboard."
    counts = bridge.count_tokens(text)
    assert counts["o200k_base"] > 0
    assert counts["cl100k_base"] > 0

def test_abbreviation_compression_efficiency():
    bridge = MultiTokenizerBridge()
    original = "By the way, as far as I know, I will be away from keyboard as soon as possible."
    compressed = "btw afaik afk asap"
    bench = bridge.benchmark_compression(original, compressed)

    # Shorthand abbreviation should yield significant token reduction
    for tok in ["o200k_base", "cl100k_base"]:
        assert bench[tok]["compressed_tokens"] < bench[tok]["original_tokens"]
        assert bench[tok]["reduction_percent"] > 50.0

def test_schema_zip_json_compression_efficiency():
    import json
    bridge = MultiTokenizerBridge()
    data = [
        {"id": 1, "name": "Alice", "role": "admin", "department": "engineering", "active": True},
        {"id": 2, "name": "Bob", "role": "developer", "department": "engineering", "active": True},
        {"id": 3, "name": "Charlie", "role": "designer", "department": "product", "active": False},
        {"id": 4, "name": "Diana", "role": "manager", "department": "operations", "active": True},
    ]
    raw_json = json.dumps(data)
    compact = "§[id,name,role,department,active] 1,Alice,admin,engineering,True;2,Bob,developer,engineering,True;3,Charlie,designer,product,False;4,Diana,manager,operations,True"

    bench = bridge.benchmark_compression(raw_json, compact)
    for tok in ["o200k_base", "cl100k_base"]:
        assert bench[tok]["reduction_percent"] > 45.0
