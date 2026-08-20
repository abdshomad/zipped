# Sub-Plan 20.1.1 — Autonomous Token-Optimized Knowledge Distillation & Latent Vector Codebook

## Objective & Quantifiable Measure
- **Target:** Implement domain ontology knowledge distillation codebook (`services/researcher/codebook.py`) collapsing entire technical specifications, system topologies, and tool catalogs into 1-token codebook anchors (`§C0`..`§C99`) with typed attribute dictionaries.
- **Mechanism:** Vectorized codebook clustering and associative attribute binding that achieves extreme token compression while maintaining 100% factual semantic recall.
- **Quantifiable Benchmark:** $\ge 90\%$ token reduction on complex multi-system technical architectures across `o200k_base` and `cl100k_base` with lossless roundtrip attribute expansion.

## Implementation Tasks
1. `20.1.1`: Create `LatentVectorCodebook` in `services/researcher/codebook.py`.
2. `20.1.2`: Implement associative codebook indexing, attribute packing, and bidirectional expansion.
3. `20.1.3`: E2E 100-concept domain benchmark in `tests/test_codebook.py` logging to `data/benchmarks.sqlite`.
