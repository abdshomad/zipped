# Sub-Plan 5.1.1 — Autonomous Evolutionary Arena & Mutation Loop

## Objective & Quantifiable Measure
- **Target:** Implement autonomous evolutionary search loop in `services/researcher/arena.py` integrating `autoresearch/evo`, `karpathy-autoresearch`, and `autoloop`.
- **Mechanism:** Automated genetic mutation of token dictionaries, running multi-tokenizer evaluations against `data/benchmarks.sqlite`, and preserving Pareto frontier representations.
- **Quantifiable Benchmark:** Automatically discover at least 3 novel Pareto-optimal representations exceeding baseline compression ratios by $\ge 15\%$.

## Implementation Tasks
1. `5.1.1`: Build genetic mutation and crossover operators for token substitution tables.
2. `5.1.2`: Connect evolutionary loop to `BenchmarkDB` for automatic delta logging.
3. `5.1.3`: E2E self-evolution test run.
