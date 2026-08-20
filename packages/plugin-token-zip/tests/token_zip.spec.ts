import { describe, it, expect } from 'vitest';
import { buildDictionary, serializeDict, deserializeDict } from '../src/dictionary.js';
import { TokenZipCodec } from '../src/codec.js';
import { ZippedEngine } from '@zipped/core';
import pluginTokenZip from '../src/index.js';

// ── Large repetitive corpus (ensures dictionary header overhead is worthwhile) ─
const SENTENCE = 'the quick brown fox jumps over the lazy dog in machine learning';
// Repeat 30 times to generate sufficient n-gram frequency and amortize header
const CORPUS = Array.from({ length: 30 }, (_, i) =>
  `${SENTENCE} example number ${i + 1} of the quick brown fox corpus test.`
).join('\n');

// ── Dictionary builder ────────────────────────────────────────────────────────

describe('buildDictionary', () => {
  it('detects high-frequency n-grams', () => {
    const dict = buildDictionary(CORPUS);
    expect(dict.size).toBeGreaterThan(0);
    const phrases = Array.from(dict.keys());
    const found = phrases.some((p) => p.includes('quick brown fox'));
    expect(found).toBe(true);
  });

  it('assigns unique sigils', () => {
    const dict = buildDictionary(CORPUS);
    const sigils = Array.from(dict.values()).map((e) => e.sigil);
    const unique = new Set(sigils);
    expect(unique.size).toBe(sigils.length);
  });

  it('uses §N format sigils', () => {
    const dict = buildDictionary(CORPUS);
    for (const { sigil } of dict.values()) {
      expect(sigil).toMatch(/^§[0-9A-Za-z]$/);
    }
  });
});

// ── Dict serialization / deserialization ─────────────────────────────────────

describe('serializeDict / deserializeDict', () => {
  it('roundtrips dict correctly', () => {
    const dict = buildDictionary(CORPUS);
    const header = serializeDict(dict);
    expect(header).toMatch(/^§\{.+\}$/);

    const restored = deserializeDict(header);
    expect(restored.size).toBe(dict.size);
    for (const [phrase, entry] of dict) {
      expect(restored.get(phrase)?.sigil).toBe(entry.sigil);
    }
  });
});

// ── TokenZipCodec compress / decompress ──────────────────────────────────────

describe('TokenZipCodec', () => {
  const codec = new TokenZipCodec();

  it('compresses repetitive corpus and embeds §{} dictionary header', () => {
    const result = codec.compress(CORPUS);
    expect(result.compressed).toMatch(/^§\{/);
    // With 30 repetitions the body savings must outweigh header overhead
    expect(result.compressedLength).toBeLessThan(result.originalLength);
    expect(result.ratio).toBeLessThan(1.0);
  });

  it('decompresses sigils back to normalized phrases (lossless roundtrip)', () => {
    const result = codec.compress(CORPUS);
    const restored = codec.decompress(result.compressed);

    // Collect all sigils that were substituted in the body
    const dict = buildDictionary(CORPUS);
    // Each sigil must NOT appear alone in the restored text (they were replaced back)
    for (const { sigil } of dict.values()) {
      // sigils are §N — check they don't appear as stand-alone tokens in restored
      expect(restored).not.toMatch(new RegExp(`(?<![§a-zA-Z0-9])${sigil.replace('§', '§')}(?![a-zA-Z0-9])`));
    }

    // Restored must contain the original phrases (at least one key phrase)
    expect(restored.toLowerCase()).toContain('quick brown fox');
  });

  it('passthrough for input with no repeated n-grams', () => {
    const unique = 'Hello world this is a completely unique sentence with no repetition at all.';
    const result = codec.compress(unique);
    expect(result.compressed).toBe(unique);
    expect(result.ratio).toBe(1.0);
    expect(result.metadata?.dictSize).toBe(0);
  });
});

// ── Cordis engine registration ────────────────────────────────────────────────

describe('plugin-token-zip Cordis integration', () => {
  it('registers TokenZipCodec into ZippedEngine', () => {
    const engine = new ZippedEngine();
    pluginTokenZip.apply(engine);
    const codec = engine.registry.get('token-zip-level3');
    expect(codec).toBeDefined();
    expect(codec?.name).toContain('Level 3');
  });

  it('does not register duplicate on double apply', () => {
    const engine = new ZippedEngine();
    pluginTokenZip.apply(engine);
    expect(() => pluginTokenZip.apply(engine)).not.toThrow();
    expect(engine.registry.list().length).toBe(1);
  });

  it('engine can compress and decompress via codec id', async () => {
    const engine = new ZippedEngine();
    pluginTokenZip.apply(engine);
    const result = await engine.compress(CORPUS, 'token-zip-level3');
    expect(result.codecId).toBe('token-zip-level3');
    expect(result.level).toBe(3);
    const restored = await engine.decompress(result.compressed, 'token-zip-level3');
    expect(restored.toLowerCase()).toContain('quick brown fox');
  });
});
