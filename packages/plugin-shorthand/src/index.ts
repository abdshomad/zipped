export * from './dictionary.js';
export * from './codec.js';

import { ZippedEngine } from '@zipped/core';
import { ShorthandCodec } from './codec.js';

/**
 * Cordis plugin apply hook to register ShorthandCodec into ZippedEngine.
 */
export function apply(ctx: { engine?: ZippedEngine } | ZippedEngine): void {
  const engine = 'engine' in ctx && ctx.engine ? ctx.engine : (ctx as ZippedEngine);
  if (engine && engine.registry) {
    const codec = new ShorthandCodec();
    if (!engine.registry.get(codec.id)) {
      engine.registry.register(codec);
    }
  }
}

export default {
  name: 'plugin-shorthand',
  apply,
};
