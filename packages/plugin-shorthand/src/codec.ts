import { TokenCodec, CompressionLevel, CompressionResult } from '@zipped/core';
import { SHORTHAND_DICTIONARY, REVERSE_SHORTHAND_DICTIONARY } from './dictionary.js';

export class ShorthandCodec implements TokenCodec {
  public id = 'shorthand-level1';
  public name = 'Level 1 Natural Shorthand Codec';
  public level = CompressionLevel.Level1_Natural;

  /**
   * Compress natural English text by replacing common multi-word idioms with minimal abbreviations.
   */
  public compress(input: string): CompressionResult {
    let result = input;

    for (const [phrase, abbr] of Object.entries(SHORTHAND_DICTIONARY)) {
      // Escape special characters in phrase for regex
      const escaped = phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const regex = new RegExp(`\\b${escaped}\\b`, 'gi');

      result = result.replace(regex, (match) => {
        // Match uppercase casing if whole match is upper
        if (match === match.toUpperCase()) {
          return abbr.toUpperCase();
        }
        // Match capitalized casing
        if (match[0] === match[0].toUpperCase()) {
          return abbr.charAt(0).toUpperCase() + abbr.slice(1);
        }
        return abbr;
      });
    }

    const origLen = input.length;
    const compLen = result.length;
    const ratio = origLen > 0 ? compLen / origLen : 1.0;

    return {
      compressed: result,
      originalLength: origLen,
      compressedLength: compLen,
      ratio: Number(ratio.toFixed(4)),
      level: this.level,
      codecId: this.id,
      metadata: {
        dictionarySize: Object.keys(SHORTHAND_DICTIONARY).length,
      },
    };
  }

  /**
   * Decompress shorthand text back into expanded English phrases.
   */
  public decompress(input: string): string {
    let result = input;

    for (const [abbr, phrase] of Object.entries(REVERSE_SHORTHAND_DICTIONARY)) {
      const escaped = abbr.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const regex = new RegExp(`\\b${escaped}\\b`, 'gi');

      result = result.replace(regex, (match) => {
        if (match === match.toUpperCase()) {
          return phrase.toUpperCase();
        }
        if (match[0] === match[0].toUpperCase()) {
          return phrase.charAt(0).toUpperCase() + phrase.slice(1);
        }
        return phrase;
      });
    }

    return result;
  }
}
