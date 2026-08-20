# High-Level Architecture & End-to-End Execution Flow

This document provides a high-level visual and conceptual overview of how `zipped` sits transparently between developers/applications and Large Language Model (LLM) providers to compress prompts, accelerate inference, and losslessly decompress model responses.

---

## 1. End-to-End System Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Developer / User
    participant ZippedIn as ⚡ zipped (Compression Proxy)
    participant LLM as 🧠 LLM Provider (OpenAI / Anthropic / Gemini)
    participant ZippedOut as 🔓 zipped (Decompression Engine)

    Note over User, ZippedIn: Stage 1: Ingestion & Multi-Tier Compression
    User->>ZippedIn: 1. Sends Query + Full Context<br/>(Prompt, RAG Chunks, Code, History: ~10,000 tokens)
    activate ZippedIn
    Note over ZippedIn: • Prunes low-entropy filler (LLMLingua)<br/>• Evaluates Query-Salience (Supercompress)<br/>• Encodes into Z-Lang & Micro-Tokens (Tiers 1-26)<br/>• Caches large tool dumps (CCR Cache)
    ZippedIn->>LLM: 2. Transmits Ultra-Compact Zipped Payload<br/>(Compressed: ~1,200 tokens — 88% Token Reduction!)
    deactivate ZippedIn

    Note over LLM: Stage 2: Machine-Native Inference
    activate LLM
    Note over LLM: LLM processes compact Z-Lang semantics<br/>and generates native Z-Lang response
    LLM->>ZippedOut: 3. Returns Ultra-Dense Compressed Reply<br/>(e.g., §Z[+fix *auth_token @line_42]: ~150 tokens)
    deactivate LLM

    Note over ZippedOut, User: Stage 3: Unzipping & Plain English Expansion
    activate ZippedOut
    Note over ZippedOut: • Resolves Z-Lang Role Badges (+, *, @, !)<br/>• Expands Relative Pointers & CCR Handles<br/>• Restores Natural Human English Grammar
    ZippedOut->>User: 4. Delivers Clean, Full Human-Readable Output<br/>("Fixed authentication token validation at line 42.")
    deactivate ZippedOut
```

---

## 2. The 3-Stage Lifecycle Breakdown

```mermaid
flowchart LR
    subgraph S1 ["Stage 1: Transparent Compression"]
        A["👤 User Input\n(Natural English / JSON / Code)"] --> B["⚡ zipped Ingestion\n• Entropy Filter\n• Query Salience\n• Z-Lang Morph-Packing"]
    end

    subgraph S2 ["Stage 2: Dense LLM Inference"]
        B --> C["🧠 LLM Cloud\n(OpenAI / Claude / Gemini)\n• Low KV-Cache Footprint\n• Fast TTFT & High TPS"]
    end

    subgraph S3 ["Stage 3: Lossless Expansion"]
        C --> D["🔓 zipped Decompressor\n• CCR Cache Lookup\n• Role Badge Expansion\n• Natural Language Generation"] --> E["👤 Developer Output\n(Full Natural Response)"]
    end
```

### Stage 1: Ingestion & Multi-Tier Compression
When a user prompt, multi-document RAG context, or agent tool dump enters `zipped`:
1. **Query-Aware Evidence Protection:** The user's active intent/query is preserved untouched (`Supercompress` principle).
2. **Coarse-to-Fine Entropy Budgeting:** Repetitive boilerplate and low-surprisal filler are pruned dynamically (`LLMLingua` principle).
3. **Z-Lang Semantic Packing:** Complex multi-sentence relationships are compiled into single-token Semitic root lemmas and role badges (`+` Who, `*` What, `@` Where, `!` Why, `~` Sync).
4. **Reversible Tool Caching:** Voluminous JSON outputs and terminal traces are cached as lightweight reference handles (`§CCR[hash:summary]`).

### Stage 2: Machine-Native LLM Inference
The external LLM receives a context payload reduced by **60% to 95%**:
- Time-To-First-Token (TTFT) drops dramatically because prompt prefilling requires far fewer matrix operations.
- LLM KV-cache memory consumption scales down proportionally, unlocking larger batch sizes and concurrency.
- The LLM reasons over compact Z-Lang relational frames and emits its response in native compact tokens.

### Stage 3: Instantaneous Lossless Unzipping
Before the response reaches the user:
- The `zipped` expander unpacks Z-Lang relational frames into natural human sentences.
- Any cached context handles (`§CCR`) are resolved on demand without data loss.
- The user receives an articulate, human-readable answer with zero technical syntax exposed.

---

## 3. Concrete Transformation Example

| Hop | Step | Actual Payload Content | Token Count |
| :--- | :--- | :--- | :---: |
| **1** | **User Input** | `"Investigation Report: The authentication gateway failed during jwt token verification at line 42 because session handles were not properly closed in the validation loop."` | **32 tokens** |
| **2** | **Sent to LLM by `zipped`** | `§Z[+auth_gw !fail *jwt_verify @L42 ~unclosed_sessions]` | **9 tokens** <br/>*(~72% reduction)* |
| **3** | **LLM Response** | `§Z[+patch *close_handles @auth.py:L42 !resolved]` | **8 tokens** |
| **4** | **Unzipped to User** | `"Successfully applied patch to close unhandled session connections in auth.py at line 42, resolving the issue."` | **22 tokens** |
