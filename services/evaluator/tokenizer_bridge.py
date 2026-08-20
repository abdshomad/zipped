from typing import Dict, Any
import tiktoken

class MultiTokenizerBridge:
    """Provides exact token counting across major LLM tokenizers."""

    def __init__(self):
        # OpenAI GPT-4o tokenizer
        self.o200k = tiktoken.get_encoding("o200k_base")
        # OpenAI GPT-4 / ChatGPT tokenizer
        self.cl100k = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> Dict[str, int]:
        """Count tokens across configured tokenizers."""
        return {
            "o200k_base": len(self.o200k.encode(text)),
            "cl100k_base": len(self.cl100k.encode(text)),
        }

    def benchmark_compression(self, original_text: str, compressed_text: str) -> Dict[str, Any]:
        """Compute exact token reduction percentage and ratio."""
        orig_counts = self.count_tokens(original_text)
        comp_counts = self.count_tokens(compressed_text)

        metrics = {}
        for tok_name, orig_val in orig_counts.items():
            comp_val = comp_counts[tok_name]
            reduction_pct = ((orig_val - comp_val) / orig_val * 100.0) if orig_val > 0 else 0.0
            ratio = (comp_val / orig_val) if orig_val > 0 else 1.0
            metrics[tok_name] = {
                "original_tokens": orig_val,
                "compressed_tokens": comp_val,
                "reduction_percent": round(reduction_pct, 2),
                "token_ratio": round(ratio, 4),
            }

        return metrics
