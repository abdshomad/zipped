# Current Focus & Steering Direction

**Active Phase:** Cycle 29 — Continuous In-Context Autonomous Learning Engine & Perpetual Codec Registry
**Primary Objective:** Maximize LLM context compression (5x–20x / 75%–98% token reduction) across all major LLM tokenizers (`o200k_base`, `cl100k_base`, Claude, SentencePiece) while strictly preserving 100% bidirectional lossless fidelity and eliminating hallucinations.

---

## 1. Master Compression Hierarchy & Synthesized Capabilities (Tiers 1–28)

The `zipped` engine integrates classical compression mechanics, machine-native synthetic interlinguas, and modern LLM compression science into a unified poly-modal architecture:

1. **Tier 1–3 (Foundational Codecs):**
   - **Level 1 (Natural Shorthands & Idioms):** Ultra-dense colloquial abbreviations (`btw`, `imo`, `asap`, `tldr`, `wrt`).
   - **Level 2 (Deterministic Schema DSL):** Structured grammar schemas and compact AST notations.
   - **Level 3 (BPE-Aligned Token Dictionaries):** Entropy-ranked n-gram token packing.
2. **Tier 4 (Z-Lang Synthetic Interlingua):**
   - Machine-native language for LLM-to-LLM / agent-to-agent passing.
   - Non-concatenative morphology: 1-token base lemmas + 1-token transformation sigils (Agent `+`, Locus `@`, Patient `*`, Causative `!`, Reciprocal `~`).
3. **Classical ZIP Submodule Syntheses (`ref/`):**
   - **Tier 21 (Token-LZ77):** Multi-turn conversation sliding window with relative back-references `§(-turn:len)`.
   - **Tier 22 (Token-Huffman):** Dynamic entropy trees and self-describing codebook headers `§H{...}`.
   - **Tier 23 (Central Directory Manifest):** Random-access multi-file repository indexing `§DIR[...]`.
   - **Tier 24 (Miniz Streaming Buffer):** Sub-millisecond on-the-fly token stream compression.
4. **SOTA LLM Compression Syntheses (`ref/llm-compression/`):**
   - **Tier 25 (Query-Aware Perplexity Budgeting - LLMLingua + Supercompress):** Shannon information entropy scoring + query-salience evidence protection (user query is never compressed).
   - **Tier 26 (Content-Aware Agent Proxy & Reversible Cache - Headroom + PromptIntern):** Intercepts tool outputs/logs, generates `§CCR[...]` handles with lossless on-demand retrieval, and absorbs prompt templates `§TPL[...]`.
5. **Universal Poly-Modal Arbiter & Evolutionary Generators (Tiers 27–28):**
   - **Tier 27 (Adaptive Compression Arbiter):** Auto-classifies context topology and cascades winning tiers.
   - **Tier 28 (Autonomous Codec Generator):** In-memory genetic breeding loop discovering Pareto-optimal mutant codecs.

---

## 2. Active Steering Directives for Cycle 29+
- **Perpetual Autonomous Learning:** Mine incoming agent sessions and query patterns to continuously synthesize and register winning domain-specific compression codecs in `data/benchmarks.sqlite`.
- **Zero-Latency Invariant:** All interceptor, routing, and caching operations must execute in $< 0.05\text{ms}$ per chunk.
- **Strict Anti-Duplication:** Always compose and reuse existing verified modules across `packages/` and `services/`.

---

## 3. Non-Negotiable Invariants (Every Trigger)
- **Submodule Protection:** NEVER edit, modify, or tamper with files inside `ref/*`, `autoresearch/*`, `cordis/*`. Treat them as strictly read-only.
- **Real Tokenizer Metrics Only:** Compute metrics against real tokenizers (`o200k_base`, `cl100k_base`).
- **Lossless Fidelity (≥ 99%):** Compressed representations must support deterministic decompression and evidence verification.
- **Local Commit & No-Push:** Commit upon cycle completion with 0 errors. NEVER push.
