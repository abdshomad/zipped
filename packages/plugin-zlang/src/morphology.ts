import { MorphRole } from './types.js';

/**
 * Common English morphological template patterns to root lemmas.
 */
export const MORPH_PATTERNS: Array<{
  regex: RegExp;
  role: MorphRole;
  root: string;
  reconstruction: (root: string) => string;
}> = [
  // Agent: "the person who writes / the writer / author"
  {
    regex: /\b(?:the\s+)?(?:person\s+who\s+writes|writer|author)\b/gi,
    role: MorphRole.Agent,
    root: 'write',
    reconstruction: () => 'the author who writes',
  },
  // Patient: "the document / book / written text"
  {
    regex: /\b(?:the\s+)?(?:document|written\s+text|manuscript|article)\b/gi,
    role: MorphRole.Patient,
    root: 'write',
    reconstruction: () => 'the written document',
  },
  // Locus: "in the editor / workspace / repository"
  {
    regex: /\b(?:in|at|within)\s+the\s+(?:editor|workspace|repository|repo)\b/gi,
    role: MorphRole.Locus,
    root: 'repo',
    reconstruction: () => 'in the repository',
  },
  // Causative: "force commit / force write / mandatory write"
  {
    regex: /\b(?:force\s+commit|mandatory\s+write|compel\s+write)\b/gi,
    role: MorphRole.Causative,
    root: 'write',
    reconstruction: () => 'mandatorily enforce write',
  },
  // Reciprocal / Continuous: "collaborative editing / streaming logs / continuous logging"
  {
    regex: /\b(?:collaborative\s+editing|collaboratively\s+editing)\b/gi,
    role: MorphRole.Reciprocal,
    root: 'write',
    reconstruction: () => 'collaborative editing',
  },
  // Agent Logger: "logger service / logging agent"
  {
    regex: /\b(?:logger\s+service|logging\s+agent|logger)\b/gi,
    role: MorphRole.Agent,
    root: 'log',
    reconstruction: () => 'logger service',
  },
  // Patient Log: "log entry / trace log / trace entry"
  {
    regex: /\b(?:log\s+entry|trace\s+log|trace\s+entry|audit\s+log)\b/gi,
    role: MorphRole.Patient,
    root: 'log',
    reconstruction: () => 'audit log trace',
  },
  // Causative Log: "mandatory audit log / mandatory logging"
  {
    regex: /\b(?:mandatory\s+audit\s+log|mandatory\s+logging|enforce\s+log)\b/gi,
    role: MorphRole.Causative,
    root: 'log',
    reconstruction: () => 'mandatory audit log',
  },
  // Reciprocal Log: "streaming logs / stream logs"
  {
    regex: /\b(?:streaming\s+logs|stream\s+logs|stream\s+trace\s+logs)\b/gi,
    role: MorphRole.Reciprocal,
    root: 'log',
    reconstruction: () => 'streaming logs',
  },
  // Locus Log: "in the log storage / on disk / in database"
  {
    regex: /\b(?:in\s+the\s+database|in\s+database|on\s+disk|in\s+storage)\b/gi,
    role: MorphRole.Locus,
    root: 'db',
    reconstruction: () => 'in the database storage',
  },
];

/**
 * Derive Semitic Root-and-Template token representation.
 */
export function deriveMorphToken(role: MorphRole, root: string): string {
  return `${role}${root}`;
}

/**
 * Parse a derived token into role and root lemma.
 */
export function parseMorphToken(token: string): { role: MorphRole; root: string } {
  const firstChar = token[0];
  const roles = Object.values(MorphRole) as string[];
  if (roles.includes(firstChar) && firstChar !== '') {
    return {
      role: firstChar as MorphRole,
      root: token.slice(1),
    };
  }
  return {
    role: MorphRole.Verb,
    root: token,
  };
}
