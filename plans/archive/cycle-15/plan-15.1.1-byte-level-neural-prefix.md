# Sub-Plan 15.1.1 — Autonomous Self-Synthesizing Byte-Level Neural Prefix & Extreme Entropy Compression

## Objective & Quantifiable Measure
- **Target:** Implement byte-level neural prefix optimizer (`services/researcher/neural_prefix.py`) compressing massive repetitive prompt boilerplate (system prompts, XML tags, tool definitions, rules blocks) into single-token Latin-1 prefix macros (`§P0`..`§P9`).
- **Mechanism:** Context-prefix caching with dynamic macro synthesis and byte-boundary-aligned token packing that replaces multi-line system prompts with 1-token prefix anchors.
- **Quantifiable Benchmark:** $\ge 85\%$ token reduction on long system prompt and instruction-heavy context windows across `o200k_base` and `cl100k_base` with 100% losslessness.

## Implementation Tasks
1. `15.1.1`: Create `BytePackedNeuralPrefixEngine` and prefix macro synthesizer in `services/researcher/neural_prefix.py`.
2. `15.1.2`: Implement context prefix cache and exact macro expansion runtime.
3. `15.1.3`: E2E long-context prefix compression benchmark in `tests/test_neural_prefix.py` logging to `data/benchmarks.sqlite`.
