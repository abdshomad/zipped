from typing import Dict, Any
import difflib

class SemanticLosslessnessEvaluator:
    """Evaluates semantic fidelity and reconstruction accuracy for compressed representations."""

    def evaluate_exact_losslessness(self, original: str, reconstructed: str) -> Dict[str, Any]:
        """Check exact byte/token roundtrip reconstruction."""
        matcher = difflib.SequenceMatcher(None, original.strip(), reconstructed.strip())
        similarity = matcher.ratio()

        return {
            "is_exact_match": original.strip() == reconstructed.strip(),
            "similarity_score": round(similarity, 4),
            "fidelity_passed": similarity >= 0.99,
        }
