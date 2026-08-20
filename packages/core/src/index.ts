export * from './types.js';
export * from './registry.js';
export * from './pipeline.js';

import { CodecRegistry } from './registry.js';
import { AdaptivePipelineRouter } from './pipeline.js';
import { CompressionLevel, CompressionResult } from './types.js';

/**
 * ZippedEngine coordinates dynamic codec registration, multi-tier pipeline execution,
 * and intelligent auto-adaptive routing.
 */
export class ZippedEngine {
  public registry: CodecRegistry;
  public router: AdaptivePipelineRouter;

  constructor() {
    this.registry = new CodecRegistry();
    this.router = new AdaptivePipelineRouter(this.registry);
  }

  /**
   * Auto-selects the optimal compression tier based on payload semantics and entropy.
   */
  public async autoCompress(
    input: string,
    options?: Record<string, unknown>
  ): Promise<CompressionResult> {
    return await this.router.routeAndCompress(input, options);
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

    // Use auto-router if no specific codec requested
    return await this.autoCompress(input, options);
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
