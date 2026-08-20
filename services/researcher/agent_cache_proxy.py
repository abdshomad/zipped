from typing import Dict, List, Any, Optional, Tuple
import hashlib
import json
import re
from services.evaluator.tokenizer_bridge import MultiTokenizerBridge
from services.evaluator.db import BenchmarkDB

class CachedContextRecord:
    """A cached tool execution record for on-demand reversible retrieval."""
    def __init__(self, handle_id: str, tool_name: str, raw_payload: str, summary: str):
        self.handle_id = handle_id
        self.tool_name = tool_name
        self.raw_payload = raw_payload
        self.summary = summary

class AgentCacheProxy:
    """Content-aware agent proxy and reversible tool-dump cache synthesizing Headroom and PromptIntern."""

    def __init__(self, db: Optional[BenchmarkDB] = None, bridge: Optional[MultiTokenizerBridge] = None):
        self.db = db or BenchmarkDB()
        self.bridge = bridge or MultiTokenizerBridge()
        self.cache_store: Dict[str, CachedContextRecord] = {}

    def _generate_handle_id(self, tool_name: str, payload: str) -> str:
        h = hashlib.md5(f"{tool_name}:{payload}".encode("utf-8")).hexdigest()[:8]
        return f"ccr_{h}"

    def intercept_tool_output(self, tool_name: str, payload: str) -> str:
        """Intercepts verbose tool outputs (JSON, file lists, command logs) and emits compact §CCR handles."""
        handle_id = self._generate_handle_id(tool_name, payload)

        # Generate smart semantic summary
        lines = [l.strip() for l in payload.split("\n") if l.strip()]
        if tool_name in ("list_dir", "find_by_name"):
            summary = f"{len(lines)} files listed"
        elif "error" in payload.lower() or "exception" in payload.lower():
            err_line = next((l for l in lines if "error" in l.lower() or "fail" in l.lower()), lines[0] if lines else "Error")
            summary = f"FAIL: {err_line[:40]}"
        elif len(lines) > 5:
            summary = f"{len(lines)} lines; first: {lines[0][:30]}..."
        else:
            summary = lines[0][:40] if lines else "empty"

        record = CachedContextRecord(handle_id, tool_name, payload, summary)
        self.cache_store[handle_id] = record

        return f"§CCR[{handle_id}:{tool_name}:{summary}]"

    def retrieve_cached_context(self, handle_id: str) -> Optional[str]:
        """Reversibly retrieves the exact uncompressed payload for a given handle ID."""
        record = self.cache_store.get(handle_id)
        return record.raw_payload if record else None

    def absorb_prompt_template(self, template: str) -> str:
        """Internalizes recurrent prompt templates into compact §TPL anchors (PromptIntern style)."""
        h = hashlib.md5(template.encode("utf-8")).hexdigest()[:6]
        return f"§TPL[{h}]"

    def benchmark_agent_session(
        self,
        tool_executions: List[Tuple[str, str]],
        cycle_id: int = 26,
        dataset_name: str = "agent_tool_dump_session",
    ) -> Dict[str, Any]:
        """Benchmarks token reduction across multi-turn agent tool executions and logs to BenchmarkDB."""
        raw_parts = []
        comp_parts = []

        for tool_name, payload in tool_executions:
            raw_parts.append(f"Tool `{tool_name}` output:\n```\n{payload}\n```")
            comp_handle = self.intercept_tool_output(tool_name, payload)
            comp_parts.append(comp_handle)

        raw_session = "\n\n".join(raw_parts)
        comp_session = "\n".join(comp_parts)

        bench = self.bridge.benchmark_compression(raw_session, comp_session)

        self.db.record_run(
            cycle_id=cycle_id,
            feature_name="Content-Aware Agent Proxy & Reversible Tool-Dump Cache",
            codec_id="agent-cache-proxy-tier26",
            tier_level=26,
            metrics_by_tokenizer=bench,
            dataset_name=dataset_name,
            fidelity_score=1.0,
        )

        return {
            "total_tool_calls": len(tool_executions),
            "benchmarks": bench,
            "cached_records_count": len(self.cache_store),
        }
