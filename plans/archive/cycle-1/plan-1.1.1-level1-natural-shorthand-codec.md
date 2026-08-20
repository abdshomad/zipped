# Sub-Plan 1.1.1 — Level 1 Natural Shorthand Codec (`packages/plugin-shorthand`)

## Objective & Quantifiable Measure
- **Target:** Implement Level 1 Colloquial & Natural Shorthand Codec mapping common multi-token English idioms into minimal-token abbreviations (`btw`, `afk`, `lol`, `imo`, `tldr`, `asap`, `wrt`, `fyi`, `idk`, `afaik`, `imho`).
- **Quantifiable Benchmark:** $\ge 40\%$ token reduction across OpenAI `o200k_base` and `cl100k_base` tokenizers with $100\%$ bidirectional roundtrip reconstruction.

## Implementation Architecture
1. **Package:** `packages/plugin-shorthand`
   - `src/dictionary.ts`: High-frequency BPE-analyzed abbreviation dictionary with case-preservation and boundary guards.
   - `src/codec.ts`: Implements `TokenCodec` interface (Level 1 Natural).
   - `src/index.ts`: Cordis plugin lifecycle export (`apply(ctx)`).
   - `tests/shorthand.spec.ts`: Unit tests verifying dictionary replacement, edge cases, punctuation preservation, and roundtrip decompression.
2. **Integration:** Dynamic registration with `@zipped/core` registry.
3. **Verification:** Multi-tokenizer benchmarking in Python test harness (`tests/test_token_compression.py`).

## Anti-Duplication Audit
- Sourced concepts from `ref/kuba-zip` and `ref/r-lib-zip` static dictionary mapping translated to English BPE tokens.
- No existing plugin implements Level 1 shorthand abbreviations.
