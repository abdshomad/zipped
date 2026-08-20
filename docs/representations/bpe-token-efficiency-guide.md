# BPE Token Efficiency & Sigil Engineering Guide

This guide documents empirical token costs across major LLM tokenizers (OpenAI `o200k_base` and `cl100k_base`) to guide representation design in `zipped`.

---

## 1. The Emoji Compression Fallacy (Empirical Benchmark)

While human intuition suggests that a single pictorial emoji (e.g. `🗄️` for database, `⚠️` for warning) should be concise, modern Byte-Pair Encoding (BPE) tokenizers split multi-byte UTF-8 sequences into multiple tokens. In almost all cases, **using an emoji increases token count significantly**:

| Concept | Plain English Word | Word Token Cost (`o200k` / `cl100k`) | Emoji Representation | Emoji Token Cost (`o200k` / `cl100k`) | Impact |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **database** | `database` | **1 / 1** | `🗄️` | **4 / 4** | ❌ **+300% Token Blowup** |
| **warning** | `warning` | **1 / 1** | `⚠️` | **3 / 4** | ❌ **+200%–300% Token Blowup** |
| **time / clock** | `time` | **1 / 1** | `⏰` | **3 / 3** | ❌ **+200% Token Blowup** |
| **search** | `search` | **1 / 1** | `🔍` | **2 / 3** | ❌ **+100%–200% Token Blowup** |
| **robot / AI** | `robot` | **1 / 1** | `🤖` | **2 / 3** | ❌ **+100%–200% Token Blowup** |
| **car** | `car` | **1 / 1** | `🚗` | **2 / 3** | ❌ **+100%–200% Token Blowup** |
| **error** | `error` | **1 / 1** | `❌` | **2 / 2** | ❌ **+100% Token Blowup** |
| **money** | `money` | **1 / 1** | `💰` | **2 / 2** | ❌ **+100% Token Blowup** |
| **idea** | `idea` | **1 / 1** | `💡` | **2 / 2** | ❌ **+100% Token Blowup** |

> **Conclusion:** Emojis must **NEVER** be used as a compression mechanism in `zipped`.

---

## 2. Verified 1-Token Sigils (`o200k_base` & `cl100k_base`)

The following single-character ASCII and Latin-1 characters are guaranteed to encode as **exactly 1 token** across modern BPE tokenizers and should be used for relational schemas and Z-Lang operators:

| Character | Name | `o200k_base` | `cl100k_base` | Recommended Z-Lang Role |
| :---: | :--- | :---: | :---: | :--- |
| `§` | Section Sign | **1** | **1** | Frame / Entity Header |
| `@` | At Symbol | **1** | **1** | Target / Destination Anchor |
| `~` | Tilde | **1** | **1** | Property / Modifier Binding |
| `:` | Colon | **1** | **1** | Key-Value Slot Assignment |
| `!` | Exclamation Mark | **1** | **1** | Strict Invariant / Assertion |
| `&` | Ampersand | **1** | **1** | Conjunction / Parallel Merge |
| `+` | Plus | **1** | **1** | Additive Operation |
| `*` | Asterisk | **1** | **1** | Pointer / Macro Expansion |
| `#` | Hash | **1** | **1** | Identifier / Numeric Anchor |
| `%` | Percent | **1** | **1** | Probability / Metric Score |
| `/` | Slash | **1** | **1** | Hierarchy / Namespace Path |
| `?` | Question Mark | **1** | **1** | Query / Conditional Branch |

---

## 3. High-Efficiency Natural Abbreviations (Level 1)

Multi-token English phrases that compress into 1–2 tokens via colloquial abbreviations:

| Original Phrase | Original Tokens | Abbreviation | Compressed Tokens | Token Reduction |
| :--- | :---: | :---: | :---: | :---: |
| `by the way` | **3** | `btw` | **1** (with space: 2) | **~66.7%** |
| `as soon as possible` | **4** | `asap` | **1** (with space: 2) | **~75.0%** |
| `too long didn't read` | **5** | `tldr` | **2** | **~60.0%** |
| `in my opinion` | **3** | `imo` | **1** (with space: 2) | **~66.7%** |
| `away from keyboard` | **3** | `afk` | **1** (with space: 2) | **~66.7%** |
| `for your information` | **3** | `fyi` | **1** (with space: 2) | **~66.7%** |
