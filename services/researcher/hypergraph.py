from typing import Dict, List, Any, Optional
import re

class HyperGraphNode:
    def __init__(self, node_id: str, node_type: str, attributes: Optional[Dict[str, str]] = None):
        self.node_id = str(node_id)
        self.node_type = node_type
        self.attributes = attributes or {}

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.node_id, "type": self.node_type, "attributes": self.attributes}

class ZHyperGraph:
    """Non-linear pointer-indexed hypergraph representation for zero-redundancy context passing."""

    def __init__(self):
        self.nodes: Dict[str, HyperGraphNode] = {}
        self.edges: List[Dict[str, Any]] = []

    def add_node(self, node_id: str, node_type: str, **attributes) -> "ZHyperGraph":
        self.nodes[str(node_id)] = HyperGraphNode(node_id, node_type, attributes)
        return self

    def add_edge(self, source_id: str, action: str, target_id: str, condition: Optional[str] = None) -> "ZHyperGraph":
        self.edges.append({
            "source": str(source_id),
            "action": action,
            "target": str(target_id),
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

    @classmethod
    def decode(cls, encoded_str: str) -> "ZHyperGraph":
        """Reconstruct structured graph from encoded representation."""
        graph = cls()
        tokens = encoded_str.strip().split()

        for t in tokens:
            # Node pattern: §ID:Type~k:v
            if t.startswith("§"):
                m = re.match(r"^§([^:~]+):([^~]+)(.*)$", t)
                if m:
                    n_id, n_type, rest = m.group(1), m.group(2), m.group(3)
                    attrs = {}
                    if rest:
                        for pair in re.findall(r"~([^:]+):([^~]+)", rest):
                            attrs[pair[0]] = pair[1]
                    graph.add_node(n_id, n_type, **attrs)
            # Edge pattern: (#src)>act>(#tgt)⌁cond
            elif ">" in t:
                m = re.match(r"^\(#([^)]+)\)>([^>]+)>\(#([^)]+)\)(?:⌁(.*))?$", t)
                if m:
                    src, act, tgt, cond = m.group(1), m.group(2), m.group(3), m.group(4)
                    graph.add_edge(src, act, tgt, condition=cond)

        return graph

class EigenTokenMapper:
    """Latent Eigen-Token centroid clustering and projection engine."""

    EIGEN_SIGILS = ["Ω1", "Ω2", "Ω3", "Ω4", "Ω5", "Ω6", "Ω7", "Ω8", "Ω9"]

    def compress_topology(self, topologies: List[str]) -> str:
        """Extract recurrent topology centroids and map into Ω eigen-tokens."""
        freq: Dict[str, int] = {}
        for top in topologies:
            freq[top] = freq.get(top, 0) + 1

        sorted_tops = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        eigen_dict: Dict[str, str] = {}
        for idx, (top, count) in enumerate(sorted_tops):
            if idx < len(self.EIGEN_SIGILS) and count >= 2:
                sigil = self.EIGEN_SIGILS[idx]
                eigen_dict[sigil] = top

        header_entries = [f"{k}:{v}" for k, v in eigen_dict.items()]
        header = f"Ω{{{';'.join(header_entries)}}}" if header_entries else ""

        body_parts = []
        for i, top in enumerate(topologies):
            replaced = False
            for sigil, pattern in eigen_dict.items():
                if top == pattern:
                    body_parts.append(f"§{i+1}:{sigil}")
                    replaced = True
                    break
            if not replaced:
                body_parts.append(f"§{i+1}:{top}")

        body = " ".join(body_parts)
        return f"{header} {body}" if header else body

    def decompress_topology(self, compressed_str: str) -> List[str]:
        """Expand latent eigen-tokens back into full graph representations."""
        if not compressed_str.startswith("Ω{") or "} " not in compressed_str:
            return [compressed_str]

        header_end = compressed_str.index("} ")
        header = compressed_str[2:header_end]
        body = compressed_str[header_end + 2:]

        eigen_dict = {}
        for entry in header.split(";"):
            if ":" in entry:
                sigil, val = entry.split(":", 1)
                eigen_dict[sigil.strip()] = val.strip()

        expanded = []
        for item in body.split():
            if ":" in item:
                _, val = item.split(":", 1)
                expanded.append(eigen_dict.get(val, val))
            else:
                expanded.append(eigen_dict.get(item, item))

        return expanded
