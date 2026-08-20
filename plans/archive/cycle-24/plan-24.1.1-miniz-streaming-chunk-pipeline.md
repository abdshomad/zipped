# Sub-Plan 24.1.1 — Miniz-Style Streaming On-The-Fly Chunk Pipeline

## Objective & Quantifiable Measure
- **Target:** Implement miniz-inspired on-the-fly streaming chunk compression (`services/researcher/miniz_stream.py`) adapting `ref/kuba-zip` streaming append buffers to compress real-time LLM token emissions incrementally.
- **Mechanism:** Streaming sliding window buffer with incremental back-referencing and dynamic symbol substitution executing with sub-millisecond per-chunk latency.
- **Quantifiable Benchmark:** $\ge 80\%$ token reduction across 10,000-token continuous streaming sessions with $< 0.05\text{ms}$ per-chunk execution overhead and 100% losslessness.

## Implementation Tasks
1. `24.1.1`: Create `MinizStreamingBuffer` and `StreamChunk` in `services/researcher/miniz_stream.py`.
2. `24.1.2`: Implement on-the-fly incremental compression and zero-latency chunk emission.
3. `24.1.3`: E2E 10,000-token stream benchmark in `tests/test_miniz_stream.py` logging to `data/benchmarks.sqlite`.
