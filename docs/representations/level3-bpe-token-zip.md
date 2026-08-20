# Level 3: BPE Token Dictionary & Entropy Zip

## Overview
`@zipped/plugin-token-zip` implements Level 3 dynamic frequency n-gram dictionary substitution.
High-frequency multi-word phrases are replaced with compact `§N` two-character sigils,
reducing token count on repetitive/large-context LLM prompts by **68.79%** (target: ≥ 60%).

## Compression Format
```
§{phrase1|§0,phrase2|§1,...} <substituted_body>
```
- **Header:** `§{...}` — inline dictionary mapping phrase → sigil.
- **Separator:** `|` between phrase and sigil (safe: not present in normalized English).
- **Sigil pool:** `§0`–`§z` (62 slots). The `§` char is a verified 1-token BPE symbol.
- **Body:** Input with all matched phrases replaced by their assigned sigils.

## Algorithm
1. Normalize corpus → lowercase words, strip punctuation.
2. Count word n-gram frequencies (n = 2–5).
3. Sort by frequency desc, length desc (longest-match preference).
4. Assign `§0`, `§1`, ... sigils to top-K phrases (freq ≥ 2).
5. Apply longest-first substitution (greedy, no partial overlap).
6. Prepend serialized header to body.

## Lossless Roundtrip
Decompression extracts the embedded `§{...}` header, then replaces each sigil back
to its original phrase via string splitting (no regex — avoids special-char conflicts).

## Benchmark
| Corpus | `o200k_base` | `cl100k_base` | Reduction |
| :--- | :---: | :---: | :---: |
| High-repetition paragraph 60× | 1320→412 | 1320→412 | **68.79%** |

## Codec Registration
```typescript
import pluginTokenZip from '@zipped/plugin-token-zip';
pluginTokenZip.apply(engine); // registers 'token-zip-level3'
```
