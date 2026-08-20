import { TokenCodec, CompressionLevel, CompressionResult } from '@zipped/core';

export class SchemaZipCodec implements TokenCodec {
  public id = 'schema-zip-level2';
  public name = 'Level 2 Symbolic & Schema Zip Codec';
  public level = CompressionLevel.Level2_Symbolic;

  /**
   * Compress structured JSON data into single-header schema tuples.
   * e.g., [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
   * becomes: §[id,name] 1,Alice;2,Bob
   */
  public compress(input: string): CompressionResult {
    let parsed: unknown;
    try {
      parsed = JSON.parse(input);
    } catch {
      // If not valid JSON, fallback to passthrough
      return {
        compressed: input,
        originalLength: input.length,
        compressedLength: input.length,
        ratio: 1.0,
        level: this.level,
        codecId: this.id,
      };
    }

    let compressed = input;

    if (Array.isArray(parsed) && parsed.length > 0 && typeof parsed[0] === 'object' && parsed[0] !== null) {
      const keys = Object.keys(parsed[0]);
      const header = `§[${keys.join(',')}]`;
      const rows = parsed.map((item: Record<string, unknown>) => {
        return keys.map((k) => {
          const val = item[k];
          return val === null || val === undefined ? '' : String(val);
        }).join(',');
      });
      compressed = `${header} ${rows.join(';')}`;
    } else if (typeof parsed === 'object' && parsed !== null) {
      // Single object compression
      const entries = Object.entries(parsed as Record<string, unknown>);
      const keys = entries.map(([k]) => k);
      const values = entries.map(([, v]) => String(v));
      compressed = `§[${keys.join(',')}] ${values.join(',')}`;
    }

    const origLen = input.length;
    const compLen = compressed.length;
    const ratio = origLen > 0 ? compLen / origLen : 1.0;

    return {
      compressed,
      originalLength: origLen,
      compressedLength: compLen,
      ratio: Number(ratio.toFixed(4)),
      level: this.level,
      codecId: this.id,
      metadata: {
        type: Array.isArray(parsed) ? 'array' : 'object',
      },
    };
  }

  /**
   * Decompress schema tuples back into exact JSON string.
   */
  public decompress(input: string): string {
    const match = input.match(/^§\[(.*?)\]\s*(.*)$/);
    if (!match) {
      return input;
    }

    const keys = match[1].split(',').map((k) => k.trim());
    const body = match[2].trim();

    if (body.includes(';')) {
      // Array of objects
      const rows = body.split(';');
      const result = rows.map((row) => {
        const values = row.split(',');
        const obj: Record<string, unknown> = {};
        keys.forEach((key, idx) => {
          const val = values[idx];
          obj[key] = !isNaN(Number(val)) && val !== '' ? Number(val) : val;
        });
        return obj;
      });
      return JSON.stringify(result);
    } else {
      // Single object
      const values = body.split(',');
      const obj: Record<string, unknown> = {};
      keys.forEach((key, idx) => {
        const val = values[idx];
        obj[key] = !isNaN(Number(val)) && val !== '' ? Number(val) : val;
      });
      return JSON.stringify(obj);
    }
  }
}
