# Sub-Plan 23.1.1 — Central Directory Manifest & Random-Access Multi-File Index

## Objective & Quantifiable Measure
- **Target:** Implement Central Directory manifest indexing (`services/researcher/central_directory.py`) inspired by `ref/alexmullins-zip`, indexing multi-file repositories into compact header manifests `§DIR[f1:size:offset;f2:size:offset]`.
- **Mechanism:** Allows LLM agents to perform targeted random-access file reads and selective in-context expansion instead of ingesting entire redundant repository contexts.
- **Quantifiable Benchmark:** $\ge 85\%$ token reduction on multi-file repository workloads with 100% exact random-access file content restoration.

## Implementation Tasks
1. `23.1.1`: Create `CentralDirectoryManifestCodec` and `DirectoryEntry` in `services/researcher/central_directory.py`.
2. `23.1.2`: Implement random-access file extraction and selective manifest expansion.
3. `23.1.3`: E2E 20-file repository benchmark in `tests/test_central_directory.py` logging to `data/benchmarks.sqlite`.
