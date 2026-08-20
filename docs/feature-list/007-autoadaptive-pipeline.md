# 007 — Multi-Tier Auto-Adaptive Pipeline & Global Context Streaming

**Package:** `@zipped/core`
**Module:** `packages/core/src/pipeline.ts`
**Strategy ID:** `adaptive-pipeline-tier7`
**Tier:** Tier 7 (Multi-Tier Auto-Adaptive Router & Pipeline)
**Status:** ✅ Verified (Cycle 7)

## Feature Summary
Intelligent multi-tier payload classifier and compression router. Inspects incoming prompt characteristics (JSON syntax, Semitic Z-Lang patterns, n-gram frequency distributions, graph topologies, and colloquial abbreviations) and automatically routes data to the Pareto-optimal compression tier (Level 1 Shorthand, Level 2 Schema Zip, Level 3 Token Zip, Tier 4 Z-Lang, or Tier 6 HyperGraph).

Achieves **77.60% average token reduction** across complex heterogeneous multi-modal prompt corpuses with 100% losslessness.

## Key Components
| File | Description |
| :--- | :--- |
| `packages/core/src/pipeline.ts` | `AdaptivePipelineRouter`, `classify()`, `routeAndCompress()`, `compressBatch()` |
| `packages/core/src/index.ts` | `ZippedEngine.autoCompress()` and unified engine export |
| `packages/core/tests/pipeline.spec.ts` | Classification & autoCompress unit tests |
| `tests/test_token_compression.py` | 4-tier heterogeneous multi-tokenizer benchmark test |

## Benchmark Evidence
- `o200k_base`: 4,517 → 1,012 tokens (**77.60%** reduction)
- `cl100k_base`: 4,518 → 1,021 tokens (**77.40%** reduction)
- Fidelity score: **1.00** (Full multi-tier lossless reconstruction)
- Recorded in `data/benchmarks.sqlite`
