import { TokenCodec, CompressionLevel } from './types.js';

/**
 * CodecRegistry manages dynamic registration and retrieval of token compression codecs.
 */
export class CodecRegistry {
  private codecs = new Map<string, TokenCodec>();

  /**
   * Register a new compression codec.
   */
  public register(codec: TokenCodec): void {
    if (this.codecs.has(codec.id)) {
      throw new Error(`Codec with id "${codec.id}" is already registered.`);
    }
    this.codecs.set(codec.id, codec);
  }

  /**
   * Unregister an existing codec.
   */
  public unregister(codecId: string): boolean {
    return this.codecs.delete(codecId);
  }

  /**
   * Retrieve a codec by ID.
   */
  public get(codecId: string): TokenCodec | undefined {
    return this.codecs.get(codecId);
  }

  /**
   * Retrieve all registered codecs for a specific compression level.
   */
  public getByLevel(level: CompressionLevel): TokenCodec[] {
    return Array.from(this.codecs.values()).filter((c) => c.level === level);
  }

  /**
   * List all registered codecs.
   */
  public list(): TokenCodec[] {
    return Array.from(this.codecs.values());
  }
}
