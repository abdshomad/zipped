# Sub-Plan 16.1.1 — Autonomous Cross-Model Entropy Minimization & Multi-Tokenizer Auto-Evolving Arena

## Objective & Quantifiable Measure
- **Target:** Implement joint multi-model Pareto optimizer (`services/researcher/cross_evaluator.py`) evaluating and tuning token representations simultaneously across `o200k_base`, `cl100k_base`, and SentencePiece tokenizers.
- **Mechanism:** Cross-tokenizer objective function balancing token reduction deltas across multiple model vocabularies to prevent single-tokenizer over-fitting.
- **Quantifiable Benchmark:** Multi-model Pareto dominance achieving $\ge 75\%$ average token reduction across all tokenizers simultaneously with 100% losslessness.

## Implementation Tasks
1. `16.1.1`: Create `CrossModelFrontierEvaluator` in `services/researcher/cross_evaluator.py`.
2. `16.1.2`: Implement joint cross-model fitness scoring and Pareto dominance filtering.
3. `16.1.3`: E2E multi-model evaluation benchmark in `tests/test_cross_evaluator.py` logging to `data/benchmarks.sqlite`.
