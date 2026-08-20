from typing import Dict, List, Any, Optional
import re

class ZeroShotReasoningEvaluator:
    """Evaluates whether factual attributes, relationships, and queries can be directly extracted from compressed representations."""

    def evaluate_schema_query(self, compressed_schema: str, row_id: str, field_name: str) -> Optional[str]:
        """Directly query a tabular schema payload: §[col1,col2,...] val1,val2;..."""
        if not compressed_schema.startswith("§[") or "]" not in compressed_schema:
            return None

        header_end = compressed_schema.index("]")
        headers = [h.strip() for h in compressed_schema[2:header_end].split(",")]
        if field_name not in headers:
            return None

        field_idx = headers.index(field_name)
        id_idx = headers.index("id") if "id" in headers else 0

        rows = compressed_schema[header_end + 1:].strip().split(";")
        for row in rows:
            cols = [c.strip() for c in row.split(",")]
            if len(cols) > id_idx and cols[id_idx] == str(row_id):
                if len(cols) > field_idx:
                    return cols[field_idx]

        return None

    def evaluate_zlang_frame(self, compressed_zlang: str, agent_query: str) -> Optional[Dict[str, Any]]:
        """Directly extract relational frame information for a given agent in Z-Lang."""
        tokens = compressed_zlang.replace("⟨", "").replace("⟩", "").split()
        target_agent = agent_query.lstrip("+")

        has_agent = False
        action = None
        patient = None
        locus = None

        for t in tokens:
            if t.startswith("+") and t[1:] == target_agent:
                has_agent = True
            elif t.startswith("*"):
                patient = t[1:]
            elif t.startswith("@"):
                locus = t[1:]
            elif not t.startswith(("+", "*", "@", "!", "~", "?", "§")):
                action = t

        if has_agent:
            return {
                "agent": target_agent,
                "action": action,
                "patient": patient,
                "locus": locus,
            }
        return None

    def evaluate_hypergraph_edge(self, compressed_graph: str, source_id: str, target_id: str) -> Optional[Dict[str, Any]]:
        """Directly query graph edges and conditions connecting source_id to target_id."""
        pattern = rf"\(\#{source_id}\)>([^>]+)>\(\#{target_id}\)(?:⌁([^\s]+))?"
        m = re.search(pattern, compressed_graph)
        if m:
            action, cond = m.group(1), m.group(2)
            return {
                "source": source_id,
                "target": target_id,
                "action": action,
                "condition": cond,
            }
        return None

    def evaluate_benchmark_suite(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Runs a batch of zero-shot reasoning queries and computes accuracy score."""
        total = len(test_cases)
        correct = 0

        for tc in test_cases:
            q_type = tc["type"]
            expected = tc["expected"]

            if q_type == "schema":
                actual = self.evaluate_schema_query(tc["payload"], tc["id"], tc["field"])
            elif q_type == "zlang":
                actual = self.evaluate_zlang_frame(tc["payload"], tc["agent"])
            elif q_type == "hypergraph":
                actual = self.evaluate_hypergraph_edge(tc["payload"], tc["source"], tc["target"])
            else:
                actual = None

            if actual == expected:
                correct += 1

        accuracy = correct / max(total, 1)
        return {
            "total_queries": total,
            "correct_queries": correct,
            "accuracy": round(accuracy, 4),
            "passed": accuracy >= 0.99,
        }
