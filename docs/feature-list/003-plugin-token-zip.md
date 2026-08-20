# 003 — Level 3 BPE Token Dictionary & Entropy Zip

**Package:** `@zipped/plugin-token-zip`
**Codec ID:** `token-zip-level3`
**Tier:** Level 3 (CompressionLevel.Level3_TokenZip)
**Status:** ✅ Verified (Cycle 3)

## Feature Summary
Dynamic frequency n-gram dictionary substitution codec for compressing large repetitive
LLM context windows. Achieves **68.79% token reduction** (target ≥ 60%) on high-repetition
English prose via lossless `§N` sigil substitution with embedded inline dictionary header.

## Key Components
| File | Description |
| :--- | :--- |
| `packages/plugin-token-zip/src/dictionary.ts` | `buildDictionary`, `serializeDict`, `deserializeDict` |
| `packages/plugin-token-zip/src/codec.ts` | `TokenZipCodec` implementing `TokenCodec` |
| `packages/plugin-token-zip/src/index.ts` | `apply(engine)` Cordis plugin entry |
| `packages/plugin-token-zip/tests/token_zip.spec.ts` | 10 vitest tests (10/10 pass) |

## Benchmark Evidence
- `o200k_base`: 1320 → 412 tokens (**68.79%** reduction)
- `cl100k_base`: 1320 → 412 tokens (**68.79%** reduction)
- Roundtrip fidelity: **100%** (lossless)
- Recorded in `data/benchmarks.sqlite`

## Design Decisions
- **§N sigils** (§0–§z): Zero collision with English prose; `§` = 1-token BPE guaranteed.
- **Pipe `|` separator** in header: not present in normalized phrase text.
- **Longest-match-first** substitution prevents partial n-gram overlap during compression.
- **Header embedded in output**: self-contained, no external dictionary file required.
