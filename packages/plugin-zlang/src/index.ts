export * from './types.js';
export * from './morphology.js';
export * from './frame.js';
export * from './codec.js';

import { ZippedEngine } from '@zipped/core';
import { ZLangCodec } from './codec.js';

export function apply(ctx: { engine?: ZippedEngine } | ZippedEngine): void {
  const engine = 'engine' in ctx && ctx.engine ? ctx.engine : (ctx as ZippedEngine);
  if (engine && engine.registry) {
    const codec = new ZLangCodec();
    if (!engine.registry.get(codec.id)) {
      engine.registry.register(codec);
    }
  }
}

export default {
  name: 'plugin-zlang',
  apply,
};
