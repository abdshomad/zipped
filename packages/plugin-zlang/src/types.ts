/**
 * Semitic Root-and-Template morphological derivation roles.
 */
export enum MorphRole {
  Verb = '',             // Base action / verb (fa'ala)
  Agent = '+',          // Active Agent / Doer (fa'il)
  Patient = '*',        // Patient / Product / Object (maf'ul)
  Locus = '@',          // Locus / Location / Environment (maf'al)
  Causative = '!',      // Causative / Enforcement (af'ala)
  Reciprocal = '~',     // Reciprocal / Continuous state (tafa'ala)
  Inquiry = '?',        // Inquiry / Status query (istaf'ala)
}

/**
 * Structured Z-Lang Relational Frame representing an atomic multi-agent action or rule.
 */
export interface ZLangFrame {
  agent?: string;       // +Doer
  action: string;       // Verb / Base root
  patient?: string;     // *Object / Product
  locus?: string;       // @Environment / Target
  modifiers?: string[]; // ~Continuous / !Enforcement
  constraints?: Record<string, string | number | boolean>;
}

/**
 * Parsed AST representing anchored entities and relational frames.
 */
export interface ZLangAST {
  anchors: Record<string, string>; // e.g. "§E1": "User", "§E2": "Database"
  frames: ZLangFrame[];
}
