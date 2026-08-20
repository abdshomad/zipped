# Sub-Plan 29.1.1 — Continuous In-Context Autonomous Learning Engine & Perpetual Codec Registry

## Objective & Quantifiable Measure
- **Target:** Implement a continuous in-context autonomous learning engine (`services/researcher/learning_engine.py`) that observes live agent execution streams, automatically identifies recurrent linguistic patterns, mints dynamic domain codecs, and registers them permanently in `data/benchmarks.sqlite`.
- **Mechanism:**
  1. Sliding window frequency counter tracking recurring multi-word phrases and tool trace patterns in real-time.
  2. Synthesizes verified 1-token Latin-1 sigils for top candidates and validates bidirectional losslessness.
  3. Integrates with the persistent SQLite benchmark registry for cross-session compound compression gains.
- **Quantifiable Benchmark:** $\ge 80\%$ token reduction over 100 continuous stream turns with non-negative compression slope and 100% exact fidelity.

## Implementation Tasks
1. `29.1.1`: Create `ContinuousLearningEngine` and `PatternTracker` in `services/researcher/learning_engine.py`.
2. `29.1.2`: Implement dynamic rule synthesis, verification filter, and SQLite registry persistence.
3. `29.1.3`: E2E 100-turn streaming benchmark in `tests/test_learning_engine.py` logging to `data/benchmarks.sqlite`.
