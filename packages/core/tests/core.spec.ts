import { describe, it, expect } from 'vitest';
import { ZippedEngine, CompressionLevel, TokenCodec, CompressionResult } from '../src/index.js';

describe('ZippedEngine & CodecRegistry', () => {
  it('should initialize engine with empty registry and fallback to passthrough', async () => {
    const engine = new ZippedEngine();
    expect(engine.registry.list()).toHaveLength(0);

    const res = await engine.compress('Hello world');
    expect(res.compressed).toBe('Hello world');
    expect(res.ratio).toBe(1.0);
    expect(res.codecId).toBe('passthrough');
  });

  it('should register and execute a custom token codec', async () => {
    const engine = new ZippedEngine();
    const mockCodec: TokenCodec = {
      id: 'mock-shorthand',
      name: 'Mock Shorthand Codec',
      level: CompressionLevel.Level1_Natural,
      compress: (input: string): CompressionResult => {
        const compressed = input.replace(/by the way/gi, 'btw');
        return {
          compressed,
          originalLength: input.length,
          compressedLength: compressed.length,
          ratio: compressed.length / input.length,
          level: CompressionLevel.Level1_Natural,
          codecId: 'mock-shorthand',
        };
      },
      decompress: (input: string): string => {
        return input.replace(/\bbtw\b/gi, 'by the way');
      },
    };

    engine.registry.register(mockCodec);
    expect(engine.registry.list()).toHaveLength(1);

    const res = await engine.compress('By the way, I will be late.', 'mock-shorthand');
    expect(res.compressed).toBe('btw, I will be late.');
    expect(res.compressedLength).toBeLessThan(res.originalLength);

    const roundtrip = await engine.decompress(res.compressed, 'mock-shorthand');
    expect(roundtrip.toLowerCase()).toContain('by the way');
  });
});
