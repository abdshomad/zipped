export * from './engine.js';

import { createEngine } from './engine.js';

export interface CliOptions {
  codec?: string;
  auto?: boolean;
}

/**
 * Execute CLI compression.
 */
export async function executeCompress(input: string, options?: CliOptions): Promise<string> {
  const engine = createEngine();
  const res = await engine.compress(input, options?.codec);
  return res.compressed;
}

/**
 * Execute CLI decompression.
 */
export async function executeDecompress(input: string, codecId: string): Promise<string> {
  const engine = createEngine();
  return await engine.decompress(input, codecId);
}

/**
 * List registered codecs and status.
 */
export function executeStats(): Record<string, unknown> {
  const engine = createEngine();
  const codecs = engine.registry.list();
  return {
    registeredCodecs: codecs.map((c) => ({
      id: c.id,
      name: c.name,
      level: c.level,
    })),
    totalCodecs: codecs.length,
  };
}
