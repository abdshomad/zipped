export * from './codec.js';
export * from './dictionary.js';

import { ZippedEngine } from '@zipped/core';
import { TokenZipCodec } from './codec.js';

export function apply(ctx: { engine?: ZippedEngine } | ZippedEngine): void {
  const engine = 'engine' in ctx && ctx.engine ? ctx.engine : (ctx as ZippedEngine);
  if (engine && engine.registry) {
    const codec = new TokenZipCodec();
    if (!engine.registry.get(codec.id)) {
      engine.registry.register(codec);
    }
  }
}

export default {
  name: 'plugin-token-zip',
  apply,
};
