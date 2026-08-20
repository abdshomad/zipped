# Sub-Plan 25.1.1 — Query-Aware Perplexity & Document Budgeting

## Objective & Quantifiable Measure
- **Target:** Implement query-aware information-theoretic token pruning and multi-document budget allocation (`services/researcher/perplexity_budget.py`) synthesizing `microsoft/LLMLingua` coarse-to-fine entropy pruning and `Supercompress/Supercompress` query-salience scoring.
- **Mechanism:**
  1. Never compresses the user query (keeps exact intent).
  2. Calculates sentence/block information entropy and query-term relevance scores.
  3. Preserves high-salience query evidence, converts key relational facts to Z-Lang, and dynamically drops zero-entropy boilerplate.
- **Quantifiable Benchmark:** $\ge 80\%$ token reduction across multi-document RAG and prompt contexts with 100% preservation of query-critical factual evidence.

## Implementation Tasks
1. `25.1.1`: Create `QueryAwareBudgetAllocator` and `DocumentBlock` in `services/researcher/perplexity_budget.py`.
2. `25.1.2`: Implement entropy-based surprisal estimation, query-salience scoring, and dynamic budget allocation.
3. `25.1.3`: E2E multi-document RAG benchmark in `tests/test_perplexity_budget.py` logging to `data/benchmarks.sqlite`.
