/**
 * Level 3 BPE-Aligned Token Dictionary Builder.
 *
 * Scans input text for high-frequency multi-word n-grams (2–5 tokens),
 * then assigns them compact §N two-char sigil substitutions.
 *
 * Using §-prefixed alphanumeric sigils (§0..§z) guarantees zero collision
 * with normal prose. The § character is outside standard keyboard input
 * and is a verified 1-token BPE character in o200k_base/cl100k_base.
 * Per §9 Emoji Anti-Pattern Rule: NO emojis.
 */

/** Safe §N sigils: § + single alphanumeric char. Never collide with prose. */
export const SIGIL_POOL: readonly string[] = Array.from(
  '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
).map((c) => `§${c}`);

export interface DictionaryEntry {
  sigil: string;
  phrase: string;
  frequency: number;
}

export type TokenDictionary = Map<string, DictionaryEntry>;

/**
 * Build a frequency dictionary from a corpus string.
 * Extracts top N n-grams and assigns compact §N sigils.
 *
 * @param corpus      Input text to analyze.
 * @param maxEntries  Max dictionary size (bounded by SIGIL_POOL length).
 * @param ngramSizes  Token n-gram window sizes to consider (word-level).
 */
export function buildDictionary(
  corpus: string,
  maxEntries = 30,
  ngramSizes: number[] = [2, 3, 4, 5]
): TokenDictionary {
  const words = corpus
    .toLowerCase()
    .replace(/[^a-z0-9\s\-_']/g, ' ')
    .split(/\s+/)
    .filter((w) => w.length > 0);

  const freq = new Map<string, number>();

  for (const n of ngramSizes) {
    for (let i = 0; i <= words.length - n; i++) {
      const gram = words.slice(i, i + n).join(' ');
      if (gram.length < 4) continue;
      freq.set(gram, (freq.get(gram) ?? 0) + 1);
    }
  }

  // Sort: frequency desc, then length desc (prefer longer phrases)
  const sorted = Array.from(freq.entries())
    .filter(([, count]) => count >= 2)
    .sort(([a, ca], [b, cb]) => cb - ca || b.length - a.length);

  const cap = Math.min(maxEntries, SIGIL_POOL.length, sorted.length);
  const dict: TokenDictionary = new Map();

  for (let i = 0; i < cap; i++) {
    const [phrase, frequency] = sorted[i];
    const sigil = SIGIL_POOL[i];
    dict.set(phrase, { sigil, phrase, frequency });
  }

  return dict;
}

/**
 * Serialize dictionary to compact inline header string.
 * Format: §{phrase1|sigil1,phrase2|sigil2,...}
 * Uses '|' as key-value separator (safe: not present in normalized phrases).
 */
export function serializeDict(dict: TokenDictionary): string {
  if (dict.size === 0) return '';
  const entries = Array.from(dict.values())
    .map((e) => `${e.phrase}|${e.sigil}`)
    .join(',');
  return `§{${entries}}`;
}

/**
 * Deserialize dictionary header back to TokenDictionary map.
 */
export function deserializeDict(header: string): TokenDictionary {
  const dict: TokenDictionary = new Map();
  const match = header.match(/^§\{([\s\S]*)\}$/);
  if (!match) return dict;

  const pairs = match[1].split(',');
  for (const pair of pairs) {
    const pipeIdx = pair.lastIndexOf('|');
    if (pipeIdx < 1) continue;
    const phrase = pair.slice(0, pipeIdx).trim();
    const sigil = pair.slice(pipeIdx + 1).trim();
    dict.set(phrase, { sigil, phrase, frequency: 0 });
  }
  return dict;
}
