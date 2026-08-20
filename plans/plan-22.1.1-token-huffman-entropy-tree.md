# Sub-Plan 22.1.1 — Token-Huffman Dynamic Entropy Tree Codec

## Objective & Quantifiable Measure
- **Target:** Implement dynamic Token-Huffman entropy tree compression (`services/researcher/token_huffman.py`) inspired by `ref/kuba-zip` DEFLATE dynamic trees, assigning verified 1-token Latin-1 ASCII symbols to the highest-frequency semantic expressions.
- **Mechanism:** Builds optimal frequency-ranked prefix-free dictionary headers `§H{§0:phrase1;§1:phrase2}` prepended to compressed bodies, enabling zero-loss self-describing decompression.
- **Quantifiable Benchmark:** $\ge 70\%$ token reduction across high-entropy mixed prompts with 100% exact roundtrip restoration.

## Implementation Tasks
1. `22.1.1`: Create `TokenHuffmanTreeCodec` in `services/researcher/token_huffman.py`.
2. `22.1.2`: Implement dynamic frequency tree builder and self-describing header generator `§H{...}`.
3. `22.1.3`: E2E multi-tokenizer Huffman benchmark in `tests/test_token_huffman.py` logging to `data/benchmarks.sqlite`.
