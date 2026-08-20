import { describe, it, expect } from 'vitest';
import { ZippedEngine } from '@zipped/core';
import { ShorthandCodec, apply } from '../src/index.js';

describe('ShorthandCodec (Level 1 Natural)', () => {
  it('should compress common phrases into abbreviations', () => {
    const codec = new ShorthandCodec();
    const text = 'By the way, I will be away from keyboard as soon as possible.';
    const res = codec.compress(text);

    expect(res.compressed).toBe('Btw, I will be afk asap.');
    expect(res.compressedLength).toBeLessThan(res.originalLength);
    expect(res.codecId).toBe('shorthand-level1');
  });

  it('should preserve casing correctly', () => {
    const codec = new ShorthandCodec();
    const res1 = codec.compress('IN MY OPINION this is great.');
    expect(res1.compressed).toBe('IMO this is great.');

    const res2 = codec.compress('In my opinion this is great.');
    expect(res2.compressed).toBe('Imo this is great.');
  });

  it('should decompress abbreviations back into expanded text', () => {
    const codec = new ShorthandCodec();
    const compressed = 'Btw, please let me know asap.';
    const decompressed = codec.decompress(compressed);

    expect(decompressed).toBe('By the way, please let me know as soon as possible.');
  });

  it('should register via Cordis apply hook into ZippedEngine', async () => {
    const engine = new ZippedEngine();
    apply(engine);

    expect(engine.registry.get('shorthand-level1')).toBeDefined();
    const res = await engine.compress('For your information: thanks in advance.', 'shorthand-level1');
    expect(res.compressed).toBe('Fyi: tia.');
  });
});
