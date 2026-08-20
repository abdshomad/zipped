# zipped — Research & Evolution Pipeline

This document defines how `zipped` systematically sources compression concepts from `ref/` and evolves ultra-compact, lossless token representations using frameworks in `autoresearch/`.

---

## 1. Algorithmic Inspiration Matrix (`ref/` → Token Domain)

Traditional byte-level compression algorithms from `ref/` (`r-lib-zip`, `kuba-zip`, `alexmullins-zip`) are translated into LLM token-space primitives:

| Traditional Zip Concept (`ref/`) | Token-Space Translation in `zipped` | Target Level |
| :--- | :--- | :--- |
| **Sliding Window (LZ77 / LZ78)** | **Token-LZ:** Identifies repeated n-gram token sequences across contexts and encodes back-references or shared macro pointers. | Level 2 / Level 3 |
| **Huffman Coding / Prefix Trees** | **Token-Huffman:** Assigns single BPE tokens (from `o200k_base`, `cl100k_base`) to the highest-frequency semantic expressions. | Level 1 / Level 3 |
| **Static & Dynamic Dictionaries** | **Token-Dictionary:** Maps common English words & phrases to dense natural abbreviations (`btw`, `afk`, `lol`, `imo`, `tldr`, `asap`, `wrt`). | Level 1 |
| **ZIP Central Directory & Metadata** | **Schema & AST Headers:** Compact structural headers that declare types/schemas once, enabling ultra-terse value arrays. | Level 2 |

---

## 2. Autonomous Evolution Engine (`autoresearch/` Integration)

The evolution engine synthesizes two primary paradigms from `autoresearch/`:

```mermaid
flowchart TD
    subgraph REF ["1. Idea Sourcing (ref/)"]
        LZ["Token-LZ (Sliding Window)"]
        HUF["Token-Huffman (Frequency BPE)"]
        DICT["Token-Dictionary (Shorthand/Idioms)"]
    end

    subgraph EVO ["2. Autonomous Evolution (autoresearch/)"]
        HYP["Karpathy-Style Hypothesis Loop<br/>(karpathy-autoresearch / autoloop)"]
        MUT["Genetic Mutation & Crossover<br/>(evo / deep-evolve)"]
        PROMPT["Prompt & Representation Tuning<br/>(autoresearch-prompt-optimization)"]
    end

    subgraph EVAL ["3. Verification & Pareto Selection"]
        TOK["Multi-Tokenizer Counter<br/>(o200k_base, cl100k_base, SP)"]
        SEM["Losslessness & Reconstruction Eval<br/>(≥ 99% accuracy)"]
        PAR["Pareto Frontier Archive"]
    end

    REF --> HYP
    HYP --> MUT
    MUT --> PROMPT
    PROMPT --> TOK
    TOK --> SEM
    SEM -->|Pass & Optimal| PAR
    SEM -->|Iterate / Mutate| HYP
```

### Evolutionary Cycle Stages:
1. **Hypothesis Formulation (`karpathy-autoresearch`, `autoloop`):**
   - Formulate specific token reduction targets (e.g., "Reduce JSON payload tokens by 35% using Token-LZ backrefs").
2. **Genetic Mutation & Exploration (`evo`, `deep-evolve`):**
   - Mutate token substitution dictionaries, test alternative acronyms, and explore BPE-aligned single-token delimiters.
3. **Multi-Tokenizer Evaluation:**
   - Benchmark candidates against OpenAI `o200k_base`, `cl100k_base`, and SentencePiece tokenizers.
4. **Semantic Fidelity Verification:**
   - Execute bidirectional roundtrip decompression and zero-shot reasoning benchmarks ensuring ≥ 99% accuracy.
5. **Pareto Optimization:**
   - Store winning representations on the Pareto frontier (Compression Ratio vs. Readability vs. LLM Task Latency).
