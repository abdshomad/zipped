# 021 — Token-LZ77 Sliding Window & Relative Pointer Codec

**Module:** `services/researcher/token_lz77.py`
**Strategy ID:** `token-lz77-tier21`
**Tier:** Tier 21 (Token-LZ77 Relative Pointer Sliding Window)
**Status:** ✅ Verified (Cycle 21)

## Feature Summary
Token-LZ77 sliding-window compression codec translating classical LZ77 algorithms from `ref/r-lib-zip` and `ref/kuba-zip` into LLM conversation turn space.

Scans backward across recent conversation turns and replaces identical turns or multi-token lines with compact relative back-references (`§-delta` or `§-delta.pos`), drastically reducing multi-turn memory footprint with 100% exact roundtrip restoration.

## Key Components
| File | Description |
| :--- | :--- |
| `services/researcher/token_lz77.py` | `TokenLZ77Codec`, `compress_turns()`, `decompress_turns()`, `benchmark_lz77_session()` |
| `tests/test_token_lz77.py` | Turn compression, line-level pointers, 50-turn benchmark, and SQLite logging |
| `data/benchmarks.sqlite` | Token-LZ77 sliding window metrics tracking |

## Benchmark Evidence
- 50-turn agent session corpus: **84.55% token reduction** on `o200k_base` and **85.00%** on `cl100k_base`.
- 100% exact string decompression equality verified.
