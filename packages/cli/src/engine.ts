import { ZippedEngine } from '@zipped/core';
import pluginShorthand from '@zipped/plugin-shorthand';
import pluginSchemaZip from '@zipped/plugin-schema-zip';
import pluginTokenZip from '@zipped/plugin-token-zip';
import pluginZLang from '@zipped/plugin-zlang';

/**
 * Creates and initializes a fully loaded ZippedEngine with all registered multi-tier codecs.
 */
export function createEngine(): ZippedEngine {
  const engine = new ZippedEngine();

  // Register all official plugins
  pluginShorthand.apply(engine);
  pluginSchemaZip.apply(engine);
  pluginTokenZip.apply(engine);
  pluginZLang.apply(engine);

  return engine;
}
