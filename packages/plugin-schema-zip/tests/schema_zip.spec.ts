import { describe, it, expect } from 'vitest';
import { ZippedEngine } from '@zipped/core';
import { SchemaZipCodec, apply } from '../src/index.js';

describe('SchemaZipCodec (Level 2 Symbolic)', () => {
  it('should compress tabular JSON array into compact header and tuples', () => {
    const codec = new SchemaZipCodec();
    const data = [
      { id: 1, name: 'Alice', role: 'admin' },
      { id: 2, name: 'Bob', role: 'user' },
      { id: 3, name: 'Charlie', role: 'guest' },
    ];
    const jsonStr = JSON.stringify(data);
    const res = codec.compress(jsonStr);

    expect(res.compressed).toBe('§[id,name,role] 1,Alice,admin;2,Bob,user;3,Charlie,guest');
    expect(res.compressedLength).toBeLessThan(res.originalLength);
    expect(res.codecId).toBe('schema-zip-level2');
  });

  it('should decompress tuples back into exact JSON structure', () => {
    const codec = new SchemaZipCodec();
    const compressed = '§[id,name,role] 1,Alice,admin;2,Bob,user';
    const decompressed = codec.decompress(compressed);
    const parsed = JSON.parse(decompressed);

    expect(parsed).toEqual([
      { id: 1, name: 'Alice', role: 'admin' },
      { id: 2, name: 'Bob', role: 'user' },
    ]);
  });

  it('should integrate with ZippedEngine via apply() hook', async () => {
    const engine = new ZippedEngine();
    apply(engine);

    expect(engine.registry.get('schema-zip-level2')).toBeDefined();
    const data = { status: 'ok', code: 200, message: 'success' };
    const res = await engine.compress(JSON.stringify(data), 'schema-zip-level2');
    expect(res.compressed).toBe('§[status,code,message] ok,200,success');
  });
});
