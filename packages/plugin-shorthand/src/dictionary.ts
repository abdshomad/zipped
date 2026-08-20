/**
 * High-frequency English multi-token idioms mapped to minimal-token abbreviations.
 * Sourced to minimize BPE splits under o200k_base and cl100k_base.
 */
export const SHORTHAND_DICTIONARY: Record<string, string> = {
  "by the way": "btw",
  "away from keyboard": "afk",
  "as soon as possible": "asap",
  "with respect to": "wrt",
  "with regard to": "wrt",
  "in my opinion": "imo",
  "in my humble opinion": "imho",
  "too long didn't read": "tldr",
  "too long; didn't read": "tldr",
  "for your information": "fyi",
  "as far as i know": "afaik",
  "i don't know": "idk",
  "at the moment": "atm",
  "let me know": "lmk",
  "be right back": "brb",
  "to be honest": "tbh",
  "laughing out loud": "lol",
  "for what it's worth": "fwiw",
  "in case you missed it": "icymi",
  "end of day": "eod",
  "point of view": "pov",
  "direct message": "dm",
  "rolling on the floor laughing": "rofl",
  "frequently asked questions": "faq",
  "do it yourself": "diy",
  "talk to you later": "ttyl",
  "thanks in advance": "tia",
  "if i recall correctly": "iirc",
  "if i remember correctly": "iirc",
  "no problem": "np",
  "you are welcome": "yw",
  "you're welcome": "yw",
};

/**
 * Reverse mapping for lossless decompression.
 */
export const REVERSE_SHORTHAND_DICTIONARY: Record<string, string> = Object.entries(
  SHORTHAND_DICTIONARY
).reduce((acc, [phrase, abbr]) => {
  if (!acc[abbr]) {
    acc[abbr] = phrase;
  }
  return acc;
}, {} as Record<string, string>);
