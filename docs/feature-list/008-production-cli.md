# 008 — Production CLI & Context Streaming Engine

**Package:** `@zipped/cli`
**Binary:** `packages/cli/dist/bin.js`
**Strategy ID:** `production-cli-tier8`
**Tier:** Tier 8 (Production CLI & Context Streaming Runtime)
**Status:** ✅ Verified (Cycle 8)

## Feature Summary
Production-grade command-line interface for real-time LLM context compression, decompression, and codec telemetry. Pre-wires all official Cordis compression plugins (`@zipped/plugin-shorthand`, `@zipped/plugin-schema-zip`, `@zipped/plugin-token-zip`, `@zipped/plugin-zlang`) into a unified `ZippedEngine` pipeline.

Provides sub-millisecond execution latency with full support for STDIN/STDOUT stream piping and automatic tier selection.

## Key Commands
- `zipped compress <input> [--codec <id>]`: Compress string via specified codec or auto-adaptive router.
- `zipped decompress <input> [--codec <id>]`: Losslessly reconstruct compressed string back to full original text.
- `zipped stats`: Print registered codecs and system capabilities.

## Benchmark Evidence
- Execution latency: **< 2ms** per command.
- Verified exact roundtrip decompression across all registered tiers.
- Integrated test suite: 35 vitest tests + 17 pytest tests (52/52 total pass).
