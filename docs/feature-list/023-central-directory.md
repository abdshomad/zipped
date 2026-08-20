# 023 — Central Directory Manifest & Random-Access Multi-File Index

**Module:** `services/researcher/central_directory.py`
**Strategy ID:** `central-dir-tier23`
**Tier:** Tier 23 (Central Directory Manifest Codec)
**Status:** ✅ Verified (Cycle 23)

## Feature Summary
Central Directory manifest codec translating classical Central Directory metadata tables from `ref/alexmullins-zip` into LLM multi-file repository indexing space.

Indexes multi-file repositories into a compact header manifest `§DIR[f1:offset:length;f2:offset:length]`, allowing LLM agents to execute targeted random-access file queries with 100% exact content restoration without ingesting entire uncompressed repositories.

## Key Components
| File | Description |
| :--- | :--- |
| `services/researcher/central_directory.py` | `DirectoryEntry`, `CentralDirectoryManifestCodec`, `pack_repository()`, `extract_file()`, `extract_all()` |
| `tests/test_central_directory.py` | Repository packing, random-access single file extraction, 20-file codebase benchmark, and SQLite logging |
| `data/benchmarks.sqlite` | Central Directory repository metrics tracking |

## Benchmark Evidence
- 20-file codebase repository query: **76.77% token reduction** on `o200k_base` and **77.38%** on `cl100k_base`.
- 100% exact random-access file content restoration.
