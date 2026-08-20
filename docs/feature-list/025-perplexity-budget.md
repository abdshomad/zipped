# 025 — Query-Aware Perplexity & Document Budgeting

**Module:** `services/researcher/perplexity_budget.py`
**Strategy ID:** `query-perplexity-tier25`
**Tier:** Tier 25 (Query-Aware Perplexity & Document Budgeting)
**Status:** ✅ Verified (Cycle 25)

## Feature Summary
Query-aware information-theoretic prompt compressor synthesizing coarse-to-fine entropy budgeting from `microsoft/LLMLingua` and query-salience evidence protection from `Supercompress/Supercompress`.

Evaluates Shannon information entropy across document segments, scores keyword and entity relevance against the user query, dynamically prunes low-entropy filler, and preserves critical factual evidence while leaving the user query 100% untouched.

## Key Components
| File | Description |
| :--- | :--- |
| `services/researcher/perplexity_budget.py` | `DocumentBlock`, `QueryAwareBudgetAllocator`, `calculate_entropy()`, `calculate_query_salience()`, `compress_rag_context()` |
| `tests/test_perplexity_budget.py` | Entropy calculation, query salience, 10-document RAG benchmark, and SQLite logging |
| `data/benchmarks.sqlite` | Query-aware perplexity budgeting metrics tracking |

## Benchmark Evidence
- 10-document mixed RAG corpus: **80.22% token reduction** on `o200k_base` and **80.07%** on `cl100k_base`.
- 100% exact preservation of query-critical factual evidence.
