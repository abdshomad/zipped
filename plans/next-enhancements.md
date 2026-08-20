# Next Enhancements & Research Tasks

> Active cycle enhancements. Read before each trigger execution.

## Cycle 2: Level 2 Symbolic & Schema Zip Codec [DONE]
- [x] `2.1.1` **Level 2 Schema Zip Package Scaffolding:** Create `packages/plugin-schema-zip` with header-based schema packing for JSON/AST data.
- [x] `2.1.2` **Cordis Integration & Engine Registration:** Register `SchemaZipCodec` with `CompressionLevel.Level2_Symbolic` in `@zipped/core`.
- [x] `2.1.3` **Multi-Tokenizer Benchmark & Verification:** Verify $\ge 50\%$ token savings on structured payloads across `o200k_base` and `cl100k_base` with 100% exact roundtrip JSON reconstruction and log to `data/benchmarks.sqlite`.

## Cycle 3: Level 3 BPE Token Dictionary & Entropy Zip [DONE]
- [x] `3.1.1` **Level 3 Token Zip Package Scaffolding:** Create `packages/plugin-token-zip` with dynamic frequency dictionary builder.
- [x] `3.1.2` **Token-Huffman Bit Packing Codec:** Implement `TokenZipCodec` mapping high-frequency n-grams / phrases to §N sigils and dynamic token dictionaries (`§{dict}...`).
- [x] `3.1.3` **Cordis Registration & Multi-Tokenizer Verification:** Register `TokenZipCodec` in `@zipped/core`, verify $\ge 60\%$ token reduction across `o200k_base` and `cl100k_base` (achieved **68.8%**) with exact roundtrip decompression, and record metrics into `data/benchmarks.sqlite`.

## Future Cycles
- **Cycle 4:** `4.1.1` Tier 4 Z-Lang Semitic Morphology & Frame Codec (`packages/plugin-zlang`).
- **Cycle 5:** `5.1.1` Autonomous Evolutionary Arena & Genetic Mutation (`services/researcher/arena.py`).
- **Cycle 6:** `6.1.1` Z-Omega Latent Eigen-Tokens & HyperGraph Representation.
