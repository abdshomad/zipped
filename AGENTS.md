# zipped — Autonomous Agent Guidelines (Token-Optimized Representations & Auto-Evolution)

> Read-first for every trigger (i/e/n/r/m): `plans/CURRENT-FOCUS.md` (steering direction), `plans/README.md`, `plans/cycle_state.json`, and `plans/next-enhancements.md`. Relative paths only.

## §0 — North Star & Core Directive: Maximum Context Window Compression & Lossless Auto-Evolution
**Steering Direction:** Always read and align with `plans/CURRENT-FOCUS.md` first. It serves as the primary user-directed anchor for current compression goals, target representations, and active constraints.
From the user's perspective, the primary objective is creating, testing, and continuously evolving **ultra-compact, token-optimized language representations** that maximize LLM context windows without losing semantic meaning:
1. **Multi-Tier Compression Hierarchy:**
   - **Level 1 (Colloquial & Natural Shorthand):** Ultra-dense English abbreviations, domain idioms (e.g., `btw`, `afk`, `lol`, `imo`, `tldr`, `wrt`, `asap`), and morphological contractions that minimize tokens under modern BPE tokenizers while preserving human readability and prompt naturalness.
   - **Level 2 (Symbolic & Schema Zip):** Deterministic shorthand notation, compact AST representations, structural grammar compression, and dense DSL encodings designed for zero-loss LLM parsing.
   - **Level 3 (BPE-Aligned Token-Dictionary / Byte-Packed Zip):** Frequency-analyzed dictionary substitution, Huffman/entropy-inspired token packing, and BPE-boundary aligned symbols maximizing token entropy per character.
   - **Level 4 (LLM-Native Synthetic Interlingua / Z-Lang):** A completely new, machine-native synthetic language designed exclusively for LLM-to-LLM context passing. Employs Semitic Root-and-Template non-concatenative morphology (1-token base lemmas + 1-token transformation sigils: Agent `+`, Locus `@`, Patient `*`, Causative `!`, Reciprocal `~`), single-token BPE relational sigils, deterministic formal grammars, typed slot mapping, and semantic anchor constraints to maximize token reduction (5x–20x) while strictly eliminating hallucination.
2. **Auto-Everything Engine (Auto-Research, Auto-Improve, Auto-Evolve):**
   - Continuously explore, mutate, benchmark, and evolve token representation representations using autonomous research loops inspired by `autoresearch/` and evolutionary algorithms (`evo`, `deep-evolve`, `autoloop`).
3. **Hybrid Architecture (Cordis Microkernel + Python Evaluator Engine):**
   - **Cordis Microkernel Core (`packages/core`, `packages/plugins-*`):** Dynamic service registry, pipeline coordinator, codec registry, hot module reloading.
   - **Python Sidecars (`services/evaluator`, `services/researcher`):** Multi-tokenizer benchmarking (`tiktoken` `o200k_base`, `cl100k_base`, HuggingFace/SentencePiece), LLM semantic reconstruction evaluations (≥ 99% accuracy).
4. **Autonomous Phased Evolution:** Execute cycle-by-cycle (Phase 1 Baseline & Microkernel → Phase 2 Level 1-3 Codecs → Phase 3 Auto-Research Loop → Phase 4 Multi-Tokenizer Pareto Optimization → Phase 5 E2E Self-Evolving Arena).

## Non-negotiables (every trigger)
- `[👤 User Decision] Absolute Submodule Protection`: **NEVER edit, modify, tamper with, or create files inside git submodules** (`ref/*`, `autoresearch/*`, `cordis/*`). Treat all submodules as read-only references and libraries.
- `[👤 User Decision] Real Tokenizer Benchmarks Only`: Never use synthetic estimations or character approximations. Every token metric must be computed against real LLM tokenizers (OpenAI `o200k_base`, `cl100k_base`, Anthropic/Llama tokenizers).
- `[👤 User Decision] Lossless Semantic Fidelity (≥ 99%) & Zero Hallucination`: Compressed representations (including Tier 4 Z-Lang) must achieve full semantic preservation and zero factual hallucination verified via bidirectional roundtrip decompression and zero-shot LLM reasoning benchmarks.
- `[👤 User Decision] Strict Anti-Duplication & DRY Principle`: **NEVER plan, implement, or replicate duplicate or overlapping algorithms**. Audit existing plugins (`packages/`), reference submodules (`ref/`), and research modules (`autoresearch/`) to extend and compose.
- `[👤 User Decision] Mandatory Issue Recording in issues/`: Document any test failure, tokenizer discrepancy, semantic loss, or bottleneck following the standard 5-Section Postmortem Schema in `issues/###-<slug>.md` and update `issues/README.md`.
- `[👤 User Decision] Mandatory Cycle Commit & No-Push Policy`: Whenever 1 cycle is finished and verified with 0 test errors, the agent **MUST create a local git commit** (`cycle-<N>: <phase_name> verified with <X>% token reduction`). **NEVER run `git push`** without explicit user approval.
- Monorepo & Tooling: `pnpm` for TypeScript/Cordis microkernel packages (`pnpm build`, `pnpm test`), `uv` for Python tokenizer benchmarks and auto-research pipelines (`uv run pytest`).

## §1 — Trigger "i" / "init" / "initialize" → bootstrap monorepo & baseline
- **Bootstrap Monorepo & Structure:**
  - Create monorepo configuration (`pnpm-workspace.yaml`, root `package.json`, `tsconfig.json`, `pyproject.toml`).
  - Scaffold core directories: `packages/core`, `services/evaluator`, `docs/representations`, `docs/feature-list`, `issues/`.
  - Initialize `plans/README.md`, `plans/next-enhancements.md`, `issues/README.md`, and set `plans/cycle_state.json` to Cycle 0.
  - Establish baseline multi-tokenizer test harness (`tests/test_token_compression.py`, `tests/test_semantic_losslessness.py`).
- **Auto-Progression:** Once bootstrap is complete, **automatically trigger "e"** immediately to plan Cycle 1.

## §2 — Trigger "e" / "enhance" / "evolve" → plan next research/compression cycle
Read: `plans/CURRENT-FOCUS.md` → `plans/README.md` → `plans/cycle_state.json` → `plans/next-enhancements.md`.
- **Cycle:** Trigger "e" increments `cycle_state.json` (+1).
- **Hypothesis Formulation:** Formulate a quantifiable compression or auto-evolution hypothesis (e.g., token reduction %, semantic fidelity score, compression speed).
- **Anti-Duplication Audit:** Audit existing codecs and submodules (`ref/`, `autoresearch/`) to ensure originality.
- **Unique Task IDs & Sub-Plans:** Assign identifiers **`<phase>.<package_seq>.<task_seq>`** (e.g. `1.1.1`) and create sub-plan `plans/plan-<id>-<slug>.md`.
- Group planned tasks by Phase/Package (`[TODO]`).

## §3 — Trigger "n" / "next" / "n{x}" → execute token optimization / auto-research task
- **Fallback:** If `plans/next-enhancements.md` has no remaining `[TODO]` tasks → **"n" MUST automatically trigger "e"**.
- Implement compression codecs, token dictionaries, or evolutionary algorithms in `packages/<name>` or `services/`.
- Wire plugins into Cordis root context (`packages/core`) and event bus.
- Run targeted benchmark tests (§8).
- Mark `[DONE]`, dual-document (§5).
- **Auto-Progression:** When all `[TODO]` tasks in cycle are done, **automatically trigger "r"** immediately.

## §4 — Trigger "r" / "review"
- Benchmark token reduction against baseline across `o200k_base`, `cl100k_base`, and SentencePiece.
- Evaluate roundtrip reconstruction accuracy and LLM semantic understanding (>= 99%).
- **SQLite Historical Tracking:** Record run metrics into `data/benchmarks.sqlite` via `services.evaluator.db.BenchmarkDB` and verify non-negative deltas against previous baseline.
- Write `plans/reviews/review-N.md` with complete delta statistics table.
- Automatically run Trigger "m" immediately after writing review.

## §5 — Trigger "m" / "move"
- Dual-document compressed specifications in `docs/representations/` and `docs/feature-list/`.
- Archive sub-plan → `plans/archive/cycle-<N>/`.
- Update `plans/cycle_state.json`.
- **Mandatory Local Commit:** `git add . && git commit -m "cycle-<N>: <phase_name> verified with <X>% token reduction"`.
- **NEVER push.**
- Automatically run Trigger "e" for next evolution cycle.

## §6 — File size & refactoring
New/refactored files ≤ **256 LOC**; split codecs, tokenizer bridges, evaluators, and schemas into modular files.

## §7 — Ad-hoc requests & user decisions
Implement requested features and document in `docs/feature-list/` badged `[👤 User Decision]`.

## §8 — Test & Benchmark Execution
- TypeScript / Cordis Packages: `pnpm --filter <package-name> test` or `pnpm test` (vitest).
- Python Tokenizer Benchmarking & Evaluators:
  - `uv run pytest -q tests/test_token_compression.py -p no:cacheprovider -s`
  - `uv run pytest -q tests/test_semantic_losslessness.py -p no:cacheprovider -s`

## §9 — Token Minimization & Dictionary Engineering Rules
- Prioritize tokens that occupy single BPE tokens across major tokenizers.
- **Emoji Anti-Pattern Rule:** Avoid emoji substitutions for compression. Emojis use 3–4 byte UTF-8 sequences and typically cost **2 to 4 BPE tokens** (e.g., `🗄️` costs 4 tokens vs `database` which costs 1 token).
- **Verified 1-Token Sigils:** Use proven 1-token ASCII and Latin-1 characters (`§`, `@`, `~`, `!`, `:`, `&`, `+`, `*`, `#`, `%`, `^`) for structural relations, operators, and anchors.
- Leverage high-frequency English abbreviations (`btw`, `afk`, `lol`, `imo`, `tldr`, `asap`, `wrt`, `fyi`, `idk`, `e.g.`, `i.e.`).
- Construct frequency-aligned token dictionaries (Lempel-Ziv / Huffman / BPE-aware substitution) to discover minimal-token representations.

## §10 — Reference Submodules & Idea-to-Evolution Pipeline
Refer to `docs/research-pipeline.md` for the full translation matrix and evolutionary loop.
- `ref/` — High-performance compression libraries (Idea Sourcing):
  - `ref/r-lib-zip` — R/C zip algorithm reference (Token-LZ sliding windows, DEFLATE framing).
  - `ref/kuba-zip` — Portable C zip library (Token-Huffman frequency encoding, header minification).
  - `ref/alexmullins-zip` — Go encrypted zip library (Structured schema packing and metadata).
- `autoresearch/` — Autonomous research, self-improvement, and evolution frameworks (Evolution Engine):
  - `autoresearch/karpathy-autoresearch`, `pi-autoresearch`, `autoloop` — Hypothesis & loop drivers.
  - `autoresearch/evo`, `deep-evolve` — Genetic mutation, crossover, and token representation evolution.
  - `autoresearch/autoresearch-prompt-optimization`, `claude-autoresearch-skill` — Prompt tuning and evaluator benchmarks.
- `cordis/` — Cordis microkernel core and dynamic service architecture.
