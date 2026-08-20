# Sub-Plan 8.1.1 — Production CLI / Multi-Language SDK & Real-Time Context Streaming Arena

## Objective & Quantifiable Measure
- **Target:** Implement production CLI (`packages/cli` & `bin/zipped`) and streaming Python SDK client (`services/sdk/client.py`) connecting all multi-tier codecs with sub-millisecond throughput.
- **Mechanism:** Command-line pipeline streaming STDIN/STDOUT, auto-tier compression flags (`--level 1..6`, `--auto`), real-time token savings gauge, and SQLite Pareto leaderboard inspection command (`zipped stats`).
- **Quantifiable Benchmark:** CLI compression roundtrip $\le 5\text{ms}$ with full multi-tokenizer parity verification.

## Implementation Tasks
1. `8.1.1`: Create `packages/cli` with Commander CLI commands (`compress`, `decompress`, `stats`, `bench`).
2. `8.1.2`: Wire CLI binary into root monorepo scripts and Cordis engine.
3. `8.1.3`: E2E CLI execution and streaming throughput verification.
