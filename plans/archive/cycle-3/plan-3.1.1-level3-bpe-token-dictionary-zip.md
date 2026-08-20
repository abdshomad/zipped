# Sub-Plan 3.1.1 — Level 3 BPE-Aligned Token Dictionary & Entropy Zip

## Objective & Quantifiable Measure
- **Target:** Implement Level 3 high-entropy frequency substitution and Token-Huffman packing in `packages/plugin-token-zip`.
- **Mechanism:** Frequency analysis across large prompt corpuses, mapping recurring multi-token n-grams directly into verified 1-token ASCII/Latin-1 symbols (`§`, `@`, `~`, `!`, `:`, `&`, `+`, `*`, `#`, `%`, `^`).
- **Quantifiable Benchmark:** $\ge 60\%$ token reduction across `o200k_base` and `cl100k_base` on repetitive/large context prompts with 100% exact roundtrip decompression.

## Implementation Tasks
1. `3.1.1`: Create `packages/plugin-token-zip` with dynamic frequency dictionary builder.
2. `3.1.2`: Implement Token-Huffman variable length bit-packing into single-token byte arrays.
3. `3.1.3`: Cordis engine registration and multi-tokenizer bench test.
