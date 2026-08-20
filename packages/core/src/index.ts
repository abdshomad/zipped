export * from './types.js';
export * from './registry.js';

import { CodecRegistry } from './registry.js';
import { CompressionLevel, CompressionResult } from './types.js';

/**
 * ZippedEngine coordinate dynamic codec registration and multi-tier pipeline execution.
 */
export class ZippedEngine {
  public registry: CodecRegistry;

  constructor() {
    this.registry = new CodecRegistry();
  }

  /**
   * Compress input using the designated codec ID or highest priority level.
   */
  public async compress(
    input: string,
    codecId?: string,
    options?: Record<string, unknown>
  ): Promise<CompressionResult> {
    if (codecId) {
      const codec = this.registry.get(codecId);
      if (!codec) {
        throw new Error(`Codec "${codecId}" not found in registry.`);
      }
      return await codec.compress(input, options);
    }

    // Default to first available codec or pass-through
    const codecs = this.registry.list();
    if (codecs.length === 0) {
      return {
        compressed: input,
        originalLength: input.length,
        compressedLength: input.length,
        ratio: 1.0,
        level: CompressionLevel.Level1_Natural,
        codecId: 'passthrough',
      };
    }

    return await codecs[0].compress(input, options);
  }

  /**
   * Decompress input using specified codec.
   */
  public async decompress(
    input: string,
    codecId: string,
    options?: Record<string, unknown>
  ): Promise<string> {
    const codec = this.registry.get(codecId);
    if (!codec) {
      throw new Error(`Codec "${codecId}" not found in registry.`);
    }
    return await codec.decompress(input, options);
  }
}
