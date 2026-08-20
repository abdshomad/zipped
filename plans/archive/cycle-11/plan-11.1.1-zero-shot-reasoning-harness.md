# Sub-Plan 11.1.1 — Multi-Model Zero-Shot Reasoning Harness & Hyper-Frontier Evaluator

## Objective & Quantifiable Measure
- **Target:** Implement direct in-context reasoning evaluator (`services/evaluator/reasoning_evaluator.py`) testing whether LLMs can perform factual extraction, query answering, and logical inference directly on compressed representations without prior decompression.
- **Mechanism:** Deterministic reasoning test cases querying attributes, relationships, numerical constraints, and state transitions over compressed contexts (Level 1 Shorthand, Level 2 Schema Zip, Level 3 Token Zip, Tier 4 Z-Lang, Tier 6 HyperGraph).
- **Quantifiable Benchmark:** $\ge 99\%$ factual extraction and zero-shot reasoning accuracy on compressed contexts across standard problem sets.

## Implementation Tasks
1. `11.1.1`: Create `ZeroShotReasoningEvaluator` in `services/evaluator/reasoning_evaluator.py`.
2. `11.1.2`: Implement query answering and factual attribute extraction parsers over compressed ASTs and frames.
3. `11.1.3`: E2E zero-shot reasoning benchmark test suite in `tests/test_reasoning_evaluator.py` logging to `data/benchmarks.sqlite`.
