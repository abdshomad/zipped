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

## Cycle 9: Autonomous Continuous Compression & Evolution Daemon [DONE]
- [x] `9.1.1` **Sliding Context Buffer & Daemon Scaffolding:** Implement `ContextCompressionDaemon` and `SlidingContextBuffer` in `services/researcher/daemon.py`.
- [x] `9.1.2` **Background Auto-Compaction & State Pinning:** Connect multi-tier codecs for automatic historical message compression and state preservation.
- [x] `9.1.3` **50-Turn Agent Simulation & Benchmark Verification:** Verify $\ge 80\%$ token reduction in 50-turn agent session keeping active tokens $\le 1,000$ and record in `data/benchmarks.sqlite`.

## Cycle 10: Autonomous Self-Evolving Super-Arena & Global Frontier Dashboard [DONE]
- [x] `10.1.1` **Super-Arena Coordinator Scaffolding:** Create `services/researcher/super_arena.py` with multi-tier tournament dispatcher and ASCII/JSON telemetry reporting.
- [x] `10.1.2` **SQLite Metrics Rollup & Leaderboard Export:** Connect global benchmark rollup and Pareto frontier analytics in `services/evaluator/db.py`.
- [x] `10.1.3` **E2E Full-System Super-Arena Benchmark Verification:** Execute tournament simulation across all 9 compression tiers in `tests/test_super_arena.py`.

## Cycle 11: Multi-Model Zero-Shot Reasoning Harness & Hyper-Frontier Evaluator [DONE]
- [x] `11.1.1` **Zero-Shot Reasoning Harness Scaffolding:** Implement `ZeroShotReasoningEvaluator` in `services/evaluator/reasoning_evaluator.py`.
- [x] `11.1.2` **Direct Compressed Context Query Answering:** Implement query evaluation over Level 2 Schema Zip, Tier 4 Z-Lang, and Tier 6 HyperGraph formats.
- [x] `11.1.3` **E2E Reasoning Verification & SQLite Logging:** Run benchmark evaluation in `tests/test_reasoning_evaluator.py` verifying $\ge 99\%$ zero-shot accuracy and record in `data/benchmarks.sqlite`.

## Cycle 12: Autonomous Multi-Agent Battle Royale & Lossless Self-Compression Convergence [DONE]
- [x] `12.1.1` **Battle Royale Matchmaker & Shannon Entropy Estimator:** Implement `BattleRoyaleMatchmaker` and Shannon theoretical entropy calculator in `services/researcher/battle_royale.py`.
- [x] `12.1.2` **ELO Ranking & Elimination Tournament Mechanics:** Implement dynamic ELO rating and survival-of-the-fittest selection.
- [x] `12.1.3` **E2E 16-Strategy Battle Royale Verification:** Run tournament in `tests/test_battle_royale.py` verifying Pareto convergence and record in `data/benchmarks.sqlite`.

## Cycle 13: Continuous Background Evolution & Real-Time Context Streaming Optimization [DONE]
- [x] `13.1.1` **Stream Interceptor & Chunk Window Scaffolding:** Implement `StreamContextInterceptor` and `ChunkWindowBuffer` in `services/researcher/interceptor.py`.
- [x] `13.1.2` **Cross-Chunk Boundary Compression Engine:** Implement sliding window pattern matching across token stream boundaries.
- [x] `13.1.3` **E2E 10,000-Token Stream Verification & SQLite Logging:** Run benchmark simulation in `tests/test_stream_interceptor.py` verifying $\ge 75\%$ token reduction and record in `data/benchmarks.sqlite`.

## Cycle 14: Autonomous Self-Refining Polyglot Interlingua & Dynamic Codec Synthesis [DONE]
- [x] `14.1.1` **Polyglot Root Lemma Dictionary & Translingual Engine:** Implement `PolyglotInterlinguaEngine` in `services/researcher/polyglot.py`.
- [x] `14.1.2` **Universal Cross-Lingual Relational Frame Serializer:** Implement frame parsing and canonical Latin-1 sigil mapping.
- [x] `14.1.3` **E2E Multilingual Multi-Tokenizer Verification:** Verify $\ge 80\%$ token reduction on multilingual corpora in `tests/test_polyglot_interlingua.py` and record in `data/benchmarks.sqlite`.

## Cycle 15: Autonomous Self-Synthesizing Byte-Level Neural Prefix & Extreme Entropy Compression [DONE]
- [x] `15.1.1` **Byte-Level Neural Prefix Engine Scaffolding:** Implement `BytePackedNeuralPrefixEngine` in `services/researcher/neural_prefix.py`.
- [x] `15.1.2` **Context Prefix Cache & Dynamic Macro Synthesizer:** Implement dynamic prefix macro registry and bidirectional expander.
- [x] `15.1.3` **E2E 50k-Token Long-Context Prefix Verification:** Run long-context prompt benchmark in `tests/test_neural_prefix.py` verifying $\ge 85\%$ token reduction and record in `data/benchmarks.sqlite`.

## Cycle 16: Autonomous Cross-Model Entropy Minimization & Multi-Tokenizer Auto-Evolving Arena [DONE]
- [x] `16.1.1` **Cross-Model Frontier Evaluator Scaffolding:** Implement `CrossModelFrontierEvaluator` in `services/researcher/cross_evaluator.py`.
- [x] `16.1.2` **Joint Multi-Model Fitness & Pareto Frontier Optimization:** Implement cross-tokenizer loss objective function and Pareto dominance ranking.
- [x] `16.1.3` **E2E Cross-Model Benchmark Verification:** Run multi-model optimization in `tests/test_cross_evaluator.py` verifying multi-tokenizer Pareto dominance and record in `data/benchmarks.sqlite`.

## Cycle 17: Autonomous Continuous Evolution & Distributed Token Hive-Mind Arena [DONE]
- [x] `17.1.1` **Distributed Token Hive-Mind Scaffolding:** Implement `TokenHiveMind` and `SwarmAgentWorker` in `services/researcher/hivemind.py`.
- [x] `17.1.2` **Consensus-Driven Macro Promotion & Eviction:** Implement voting / consensus mechanics for global dictionary updates.
- [x] `17.1.3` **E2E Swarm Hive-Mind Simulation & SQLite Logging:** Run 10-agent swarm evolution in `tests/test_token_hivemind.py` verifying consensus macro discovery and record to `data/benchmarks.sqlite`.

## Cycle 18: Autonomous Universal Context Shrink-Ray & Master Compression Apex [DONE]
- [x] `18.1.1` **Universal Context Shrink-Ray Scaffolding:** Implement `UniversalContextShrinkRay` in `services/researcher/shrink_ray.py`.
- [x] `18.1.2` **Hierarchical Multi-Stage Cascader & Lossless Expander:** Implement sequential non-interfering transformations across Neural Prefix, Schema Zip, Z-Lang, and HyperGraph tiers.
- [x] `18.1.3` **E2E 100,000-Token Master Corpus Verification:** Run full-system master benchmark in `tests/test_shrink_ray.py` verifying $\ge 85\%$ token reduction and record in `data/benchmarks.sqlite`.

## Cycle 19: Master Autonomous Compression Kernel & Autonomous Self-Maintaining Loop [DONE]
- [x] `19.1.1` **Self-Sustaining Evolutionary Kernel Scaffolding:** Implement `SelfSustainingEvolutionKernel` in `services/researcher/kernel.py`.
- [x] `19.1.2` **Autonomous Self-Monitoring & Invariant Assertions:** Implement health checks, lossless invariant assertions, and telemetry reporter.
- [x] `19.1.3` **E2E 100-Step Perpetual Evolution Verification:** Run continuous simulation in `tests/test_kernel.py` verifying non-negative generation deltas and record in `data/benchmarks.sqlite`.

## Cycle 20: Autonomous Token-Optimized Knowledge Distillation & Latent Vector Codebook [DONE]
- [x] `20.1.1` **Latent Vector Codebook Scaffolding:** Implement `LatentVectorCodebook` in `services/researcher/codebook.py`.
- [x] `20.1.2` **Associative Codebook Indexing & Bidirectional Expansion:** Implement attribute packing and lossless concept recovery.
- [x] `20.1.3` **E2E Knowledge Distillation Benchmark Verification:** Run domain ontology compression benchmark in `tests/test_codebook.py` verifying $\ge 90\%$ token reduction and record in `data/benchmarks.sqlite`.

## Cycle 21: Token-LZ77 Sliding Window & Relative Pointer Codec [DONE]
- [x] `21.1.1` **Token-LZ77 Engine Scaffolding:** Implement `TokenLZ77Codec` in `services/researcher/token_lz77.py` scanning multi-turn agent histories for repeating token sequences.
- [x] `21.1.2` **Relative Turn/Token Pointer Generator:** Implement pointer notation `§(-turn:len)` replacing repeated multi-token phrases with 1-token relative pointers.
- [x] `21.1.3` **E2E 50-Turn Context Sliding Window Benchmark & SQLite Logging:** Run benchmark in `tests/test_token_lz77.py` verifying $\ge 80\%$ token reduction across conversation histories and record in `data/benchmarks.sqlite`.

## Cycle 22: Token-Huffman Dynamic Entropy Tree Codec [DONE]
- [x] `22.1.1` **Token-Huffman Tree Scaffolding:** Implement `TokenHuffmanTreeCodec` in `services/researcher/token_huffman.py`.
- [x] `22.1.2` **Dynamic Canonical Codebook Header Generator:** Implement self-describing header serialization `§H{§0:phrase1;§1:phrase2}` and lossless roundtrip expander.
- [x] `22.1.3` **E2E Multi-Tokenizer Huffman Entropy Benchmark & SQLite Logging:** Run benchmark in `tests/test_token_huffman.py` verifying $\ge 70\%$ token reduction across heterogeneous corpuses and record in `data/benchmarks.sqlite`.

## Cycle 23: Central Directory Manifest & Random-Access Multi-File Index [DONE]
- [x] `23.1.1` **Central Directory Scaffolding:** Implement `CentralDirectoryManifestCodec` and `DirectoryEntry` in `services/researcher/central_directory.py`.
- [x] `23.1.2` **Random-Access File Extraction:** Implement selective file retrieval and range extraction from manifest index.
- [x] `23.1.3` **E2E Multi-File Repository Benchmark & SQLite Logging:** Run repository index benchmark in `tests/test_central_directory.py` verifying $\ge 85\%$ token reduction on targeted file extraction and record in `data/benchmarks.sqlite`.

## Cycle 24: Miniz-Style Streaming On-The-Fly Chunk Pipeline [DONE]
- [x] `24.1.1` **Miniz Streaming Buffer Scaffolding:** Implement `MinizStreamingBuffer` in `services/researcher/miniz_stream.py`.
- [x] `24.1.2` **Sub-Millisecond Incremental Chunk Compressor:** Implement on-the-fly streaming pattern matching with $\le 0.05\text{ms}$ latency.
- [x] `24.1.3` **E2E 10,000-Token Continuous Stream Benchmark & SQLite Logging:** Run streaming benchmark in `tests/test_miniz_stream.py` verifying $\ge 80\%$ token reduction and record in `data/benchmarks.sqlite`.

## Cycle 25: Query-Aware Perplexity & Document Budgeting (LLMLingua + Supercompress) [TODO]
- [ ] `25.1.1` **Perplexity & Information Entropy Scaffolding:** Implement `QueryAwareBudgetAllocator` in `services/researcher/perplexity_budget.py` calculating token-level surprisal and block entropy.
- [ ] `25.1.2` **Query-Salience Scorer & Dynamic Budget Allocator:** Implement query overlap scoring that preserves query-relevant evidence, compresses high-salience blocks via Z-Lang, and prunes boilerplate filler.
- [ ] `25.1.3` **E2E Multi-Document RAG & Chat Benchmark & SQLite Logging:** Run benchmark in `tests/test_perplexity_budget.py` verifying $\ge 80\%$ token reduction with 100% preservation of query-critical facts and record in `data/benchmarks.sqlite`.

## Future Cycles
- **Cycle 26 (Phase 2):** Content-Aware Agent Proxy & Reversible Tool-Dump Cache (Synthesizing Headroom & PromptIntern).
