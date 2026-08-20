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

## Cycle 4: Tier 4 Z-Lang Semitic Morphology & Relational Frame Codec [DONE]
- [x] `4.1.1` **Z-Lang Morphology Engine Scaffolding:** Create `packages/plugin-zlang` with AST parser, semantic anchor validator, and morphological derivation generator (`+` Agent, `*` Patient, `@` Locus, `!` Causative, `~` Reciprocal, `?` Inquiry).
- [x] `4.1.2` **Relational Frame Compression & Cordis Registration:** Implement `ZLangCodec` with relational frame serialization and register in `@zipped/core` with `CompressionLevel.Level4_LLMNative`.
- [x] `4.1.3` **Multi-Tokenizer Benchmark & Zero-Shot Fidelity Verification:** Verify $\ge 65\%$ token reduction across `o200k_base` and `cl100k_base` (achieved **69.93%**) on multi-agent swarm pipeline corpuses with $\ge 99\%$ semantic reconstruction fidelity and log metrics to `data/benchmarks.sqlite`.

## Cycle 5: Autonomous Evolutionary Arena & Multi-Tier Pareto Optimizer [DONE]
- [x] `5.1.1` **Genetic Mutation & Crossover Operators:** Implement token representation mutation, crossover, and fitness evaluation in `services/researcher/arena.py`.
- [x] `5.1.2` **Pareto Frontier & SQLite Integration:** Connect evolutionary loop with `BenchmarkDB` to record generation deltas and update `pareto_leaderboard`.
- [x] `5.1.3` **E2E Self-Evolution Test Run:** Execute multi-generation evolution harness (`tests/test_evolution_arena.py`) discovering novel Pareto-optimal compressed configurations.

## Cycle 6: Z-Omega Latent Eigen-Tokens & HyperGraph Representation [DONE]
- [x] `6.1.1` **Z-HyperGraph Pointer-Referencing Compiler:** Implement structured graph serialization with back-references and edge contractions in `services/researcher/hypergraph.py`.
- [x] `6.1.2` **Latent Eigen-Token Approximation Engine:** Implement centroid token mapping and latent dimensional projection in `services/researcher/hypergraph.py`.
- [x] `6.1.3` **E2E Multi-Reference Topology Verification:** Verify $\ge 80\%$ token reduction across deeply interconnected multi-agent graph topologies (achieved **88.65%**) with 100% relationship accuracy and log to `data/benchmarks.sqlite`.

## Cycle 7: Multi-Tier Auto-Adaptive Pipeline & Global Context Streaming [DONE]
- [x] `7.1.1` **Adaptive Pipeline Router & Entropy Analyzer:** Implement payload classification and optimal codec selection in `packages/core/src/pipeline.ts`.
- [x] `7.1.2` **Unified Engine Integration & Batch API:** Connect router into `ZippedEngine` with auto-selection mode.
- [x] `7.1.3` **Heterogeneous Corpus Multi-Tokenizer Verification:** Benchmark mixed datasets (JSON, repetitive text, agent prompts, graph networks) achieving $\ge 70\%$ reduction across `o200k_base` and `cl100k_base` (achieved **77.60%**) and record in `data/benchmarks.sqlite`.

## Cycle 8: Production CLI / Multi-Language SDK & Real-Time Context Streaming Arena [DONE]
- [x] `8.1.1` **Production CLI Package Scaffolding:** Create `packages/cli` with CLI commands (`compress`, `decompress`, `stats`, `bench`).
- [x] `8.1.2` **Cordis Engine & Multi-Tier Codec Wiring:** Wire all plugins (`@zipped/plugin-shorthand`, `@zipped/plugin-schema-zip`, `@zipped/plugin-token-zip`, `@zipped/plugin-zlang`) into CLI engine.
- [x] `8.1.3` **E2E CLI Execution & Throughput Verification:** Verify end-to-end CLI commands and streaming throughput with tests in `packages/cli/tests/cli.spec.ts`.
