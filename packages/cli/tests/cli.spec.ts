import { describe, it, expect } from 'vitest';
import { executeCompress, executeDecompress, executeStats } from '../src/index.js';

describe('@zipped/cli commands', () => {
  it('lists all registered codecs in stats', () => {
    const stats = executeStats() as { registeredCodecs: Array<{ id: string }>; totalCodecs: number };
    expect(stats.totalCodecs).toBeGreaterThanOrEqual(4);
    const ids = stats.registeredCodecs.map((c) => c.id);
    expect(ids).toContain('shorthand-level1');
    expect(ids).toContain('schema-zip-level2');
    expect(ids).toContain('token-zip-level3');
    expect(ids).toContain('zlang-tier4');
  });

  it('compresses and decompresses shorthand via CLI API', async () => {
    const input = 'By the way, I will be away from keyboard as soon as possible.';
    const compressed = await executeCompress(input, { codec: 'shorthand-level1' });
    expect(compressed.toLowerCase()).toContain('btw');
    expect(compressed.toLowerCase()).toContain('afk');
    expect(compressed.toLowerCase()).toContain('asap');

    const decompressed = await executeDecompress(compressed, 'shorthand-level1');
    expect(decompressed.toLowerCase()).toContain('by the way');
  });

  it('auto-compresses JSON schema payloads accurately', async () => {
    const jsonInput = '[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]';
    const compressed = await executeCompress(jsonInput);
    expect(compressed).toContain('§[id,name]');
    expect(compressed).toContain('1,Alice');
  });

  it('auto-compresses multi-agent Z-Lang prompts accurately', async () => {
    const agentInput = 'the author who writes the written document in the repository';
    const compressed = await executeCompress(agentInput);
    expect(compressed).toContain('+write');
    expect(compressed).toContain('*write');
    expect(compressed).toContain('@repo');
  });
});
