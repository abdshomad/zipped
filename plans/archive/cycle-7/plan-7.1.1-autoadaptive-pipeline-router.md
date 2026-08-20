# Sub-Plan 7.1.1 — Multi-Tier Auto-Adaptive Pipeline & Global Context Streaming

## Objective & Quantifiable Measure
- **Target:** Implement intelligent multi-tier pipeline router (`@zipped/core` + `packages/core/src/pipeline.ts`) that analyzes incoming payload entropy and AST structure, dynamically selecting the highest-performing codec tier.
- **Mechanism:** Fast entropy scoring + type heuristics (JSON -> Level 2 Schema Zip; Repetitive Prose -> Level 3 Token Zip; Multi-Agent Workflows -> Tier 4 Z-Lang; Complex Topologies -> Tier 6 HyperGraph).
- **Quantifiable Benchmark:** $\ge 70\%$ average token reduction across heterogeneous prompt corpuses with $100\%$ lossless / $\ge 99\%$ semantic preservation.

## Implementation Tasks
1. `7.1.1`: Create `AdaptivePipelineRouter` in `packages/core/src/pipeline.ts` with entropy analyzer and codec dispatch.
2. `7.1.2`: Expose unified streaming & batch pipeline API in `@zipped/core`.
3. `7.1.3`: Multi-tier heterogeneous corpus benchmark verification across `o200k_base` and `cl100k_base`.
