# Sub-Plan 28.1.1 — Autonomous Self-Evolving Codec Generator & In-Memory LLM Arena

## Objective & Quantifiable Measure
- **Target:** Implement an autonomous self-evolving codec generator (`services/researcher/codec_generator.py`) inspired by `autoresearch/deep-evolve` and `autoresearch/evo`, mutating and breeding synthetic token codecs dynamically in-memory.
- **Mechanism:**
  1. Generates and mutates custom token replacement rules, Z-Lang relational frames, and shorthand mappings.
  2. Evaluates fitness $F = \text{Reduction}_{\text{o200k}} \times \text{Fidelity} / \text{Latency}$ across multiple generations.
  3. Automatically archives and synthesizes winning Pareto-optimal candidate codecs.
- **Quantifiable Benchmark:** $\ge 80\%$ token reduction evolved over 20 generations with 100% lossless invariant preservation and non-negative delta trajectory.

## Implementation Tasks
1. `28.1.1`: Create `AutonomousCodecGenerator` and `EvolvedCodec` in `services/researcher/codec_generator.py`.
2. `28.1.2`: Implement genetic mutation, crossover, and fitness evaluation loop.
3. `28.1.3`: E2E 20-generation evolution benchmark in `tests/test_codec_generator.py` logging to `data/benchmarks.sqlite`.
