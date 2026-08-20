/**
 * Compression representation tier levels.
 */
export enum CompressionLevel {
  Level1_Natural = 1,   // Colloquial & Natural Shorthand (btw, afk, lol)
  Level2_Symbolic = 2,  // Deterministic AST / Schema DSL
  Level3_TokenZip = 3,  // BPE-Aligned Token Dictionary & Entropy Zip
  Level4_LLMNative = 4, // LLM-Native Synthetic Interlingua (Z-Lang)
}

/**
 * Metadata result from compression operation.
 */
export interface CompressionResult {
  compressed: string;
  originalLength: number;
  compressedLength: number;
  ratio: number;
  level: CompressionLevel;
  codecId: string;
  metadata?: Record<string, unknown>;
}

/**
 * Codec plugin interface for token compression.
 */
export interface TokenCodec {
  id: string;
  name: string;
  level: CompressionLevel;
  compress(input: string, options?: Record<string, unknown>): Promise<CompressionResult> | CompressionResult;
  decompress(input: string, options?: Record<string, unknown>): Promise<string> | string;
}
