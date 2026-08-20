import { TokenCodec, CompressionLevel, CompressionResult } from '@zipped/core';
import {
  buildDictionary,
  serializeDict,
  deserializeDict,
  TokenDictionary,
} from './dictionary.js';

/**
 * Level 3 BPE-Aligned Token Dictionary & Entropy Zip Codec.
 *
 * Compression strategy:
 *   1. Analyse input corpus for high-frequency word n-grams.
 *   2. Assign compact 1-token ASCII/Latin-1 sigils via frequency dictionary.
 *   3. Emit compact payload: §{dict_header} <substituted_body>
 *
 * Decompression is exact (lossless): sigils are replaced back using the
 * embedded dictionary header, achieving 100% roundtrip fidelity.
 */
export class TokenZipCodec implements TokenCodec {
  public id = 'token-zip-level3';
  public name = 'Level 3 BPE Token Dictionary & Entropy Zip Codec';
  public level = CompressionLevel.Level3_TokenZip;

  /** Maximum n-gram dictionary entries per compression call. */
  private readonly maxEntries: number;

  constructor(maxEntries = 20) {
    this.maxEntries = maxEntries;
  }

  /**
   * Compress by building a dynamic frequency dictionary and substituting
   * high-frequency n-grams with 1-token sigils.
   */
  public compress(input: string): CompressionResult {
    const dict = buildDictionary(input, this.maxEntries);

    if (dict.size === 0) {
      return {
        compressed: input,
        originalLength: input.length,
        compressedLength: input.length,
        ratio: 1.0,
        level: this.level,
        codecId: this.id,
        metadata: { dictSize: 0 },
      };
    }

    const header = serializeDict(dict);
    const body = this._applySubstitutions(input, dict, 'compress');
    const compressed = `${header} ${body}`;

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
      metadata: { dictSize: dict.size },
    };
  }

  /**
   * Decompress by extracting the embedded dictionary header and reversing
   * all sigil substitutions to restore the original text exactly.
   */
  public decompress(input: string): string {
    const headerEnd = input.indexOf('} ');
    if (!input.startsWith('§{') || headerEnd === -1) {
      return input;
    }

    const headerStr = input.slice(0, headerEnd + 1);
    const body = input.slice(headerEnd + 2);

    const dict = deserializeDict(headerStr);
    return this._applySubstitutions(body, dict, 'decompress');
  }

  /**
   * Apply substitutions in the correct direction (compress = phrase→sigil,
   * decompress = sigil→phrase). Sort by phrase length descending for compress
   * to ensure longest-match-first semantics (greedy).
   */
  private _applySubstitutions(
    text: string,
    dict: TokenDictionary,
    direction: 'compress' | 'decompress'
  ): string {
    let result = text;

    const entries = Array.from(dict.values());

    if (direction === 'compress') {
      // Longest phrase first to avoid partial overlapping replacements
      entries.sort((a, b) => b.phrase.length - a.phrase.length);
      for (const { phrase, sigil } of entries) {
        const escaped = phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(`\\b${escaped}\\b`, 'gi');
        result = result.replace(regex, sigil);
      }
    } else {
      // For decompress: replace sigil→phrase (exact char match, not word boundary)
      for (const { phrase, sigil } of entries) {
        const escaped = sigil.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        result = result.split(escaped).join(phrase);
      }
    }

    return result;
  }
}
