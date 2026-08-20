# Sub-Plan 26.1.1 — Content-Aware Agent Proxy & Reversible Tool-Dump Cache

## Objective & Quantifiable Measure
- **Target:** Implement content-aware agent proxy interception and reversible tool-dump caching (`services/researcher/agent_cache_proxy.py`) synthesizing `headroomlabs-ai/headroom` (Cached Context Retrieval - CCR) and `microsoft/PromptIntern` (template and example absorption).
- **Mechanism:**
  1. Intercepts verbose tool execution dumps (e.g. `list_dir`, `grep_search`, test logs, large JSON payloads).
  2. Compresses repeated tool outputs into compact semantic summary handles `§CCR[id:key_summary]`.
  3. Caches original outputs in an in-memory / local LRU store for instantaneous reversible lookup on demand.
- **Quantifiable Benchmark:** $\ge 85\%$ token reduction on heavy multi-turn agent tool traces with 100% exact retrieval capability and $< 0.05\text{ms}$ interceptor overhead.

## Implementation Tasks
1. `26.1.1`: Create `AgentCacheProxy` and `CachedContextRecord` in `services/researcher/agent_cache_proxy.py`.
2. `26.1.2`: Implement content-aware tool dump compression and reversible `retrieve_cached_context()` lookup.
3. `26.1.3`: E2E 50-tool execution agent loop benchmark in `tests/test_agent_cache_proxy.py` logging to `data/benchmarks.sqlite`.
