from typing import Dict, List, Any
import re

class HyperGraphNode:
    def __init__(self, node_id: str, node_type: str, attributes: Dict[str, str] = None):
        self.node_id = node_id
        self.node_type = node_type
        self.attributes = attributes or {}

class ZHyperGraph:
    """Non-linear pointer-indexed hypergraph representation for zero-redundancy context passing."""

    def __init__(self):
        self.nodes: Dict[str, HyperGraphNode] = {}
        self.edges: List[Dict[str, Any]] = []

    def add_node(self, node_id: str, node_type: str, **attributes) -> "ZHyperGraph":
        self.nodes[node_id] = HyperGraphNode(node_id, node_type, attributes)
        return self

    def add_edge(self, source_id: str, action: str, target_id: str, condition: str = None) -> "ZHyperGraph":
        self.edges.append({
            "source": source_id,
            "action": action,
            "target": target_id,
            "condition": condition,
        })
        return self

    def encode(self) -> str:
        """Serialize graph to ultra-compact single-token sigil format."""
        parts = []
        for n in self.nodes.values():
            attrs = "".join([f"~{k}:{v}" for k, v in n.attributes.items()])
            parts.append(f"§{n.node_id}:{n.node_type}{attrs}")

        for e in self.edges:
            cond = f"⌁{e['condition']}" if e['condition'] else ""
            parts.append(f"(#{e['source']})>{e['action']}>(#{e['target']}){cond}")

        return " ".join(parts)
