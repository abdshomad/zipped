export * from './codec.js';

import { ZippedEngine } from '@zipped/core';
import { SchemaZipCodec } from './codec.js';

export function apply(ctx: { engine?: ZippedEngine } | ZippedEngine): void {
  const engine = 'engine' in ctx && ctx.engine ? ctx.engine : (ctx as ZippedEngine);
  if (engine && engine.registry) {
    const codec = new SchemaZipCodec();
    if (!engine.registry.get(codec.id)) {
      engine.registry.register(codec);
    }
  }
}

export default {
  name: 'plugin-schema-zip',
  apply,
};
