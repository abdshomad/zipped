import { ZLangAST, ZLangFrame } from './types.js';

/**
 * Format a structured frame into compact Z-Lang representation.
 * Syntax: ⟨+agent action *patient @locus !constraints ~modifiers⟩
 */
export function serializeFrame(frame: ZLangFrame): string {
  const parts: string[] = [];
  if (frame.agent) parts.push(frame.agent.startsWith('+') ? frame.agent : `+${frame.agent}`);
  parts.push(frame.action);
  if (frame.patient) parts.push(frame.patient.startsWith('*') ? frame.patient : `*${frame.patient}`);
  if (frame.locus) parts.push(frame.locus.startsWith('@') ? frame.locus : `@${frame.locus}`);
  if (frame.modifiers && frame.modifiers.length > 0) {
    for (const mod of frame.modifiers) {
      parts.push(mod.startsWith('~') ? mod : `~${mod}`);
    }
  }
  if (frame.constraints && Object.keys(frame.constraints).length > 0) {
    const cStr = Object.entries(frame.constraints)
      .map(([k, v]) => `${k}:${v}`)
      .join(',');
    parts.push(`!{${cStr}}`);
  }
  return `⟨${parts.join(' ')}⟩`;
}

/**
 * Parse a serialized frame string into a ZLangFrame object.
 */
export function deserializeFrame(serialized: string): ZLangFrame {
  const clean = serialized.replace(/^⟨|⟩$/g, '').trim();
  const tokens = clean.split(/\s+/);

  const frame: ZLangFrame = {
    action: '',
  };

  for (const token of tokens) {
    if (token.startsWith('+')) {
      frame.agent = token.slice(1);
    } else if (token.startsWith('*')) {
      frame.patient = token.slice(1);
    } else if (token.startsWith('@')) {
      frame.locus = token.slice(1);
    } else if (token.startsWith('~')) {
      frame.modifiers = frame.modifiers || [];
      frame.modifiers.push(token.slice(1));
    } else if (token.startsWith('!{') && token.endsWith('}')) {
      const inner = token.slice(2, -1);
      frame.constraints = {};
      inner.split(',').forEach((pair) => {
        const [k, v] = pair.split(':');
        if (k && v !== undefined) {
          frame.constraints![k.trim()] = isNaN(Number(v)) ? v.trim() : Number(v);
        }
      });
    } else if (!frame.action) {
      frame.action = token;
    }
  }

  return frame;
}

/**
 * Serialize full AST with entity anchors and frames.
 */
export function serializeAST(ast: ZLangAST): string {
  const anchorEntries = Object.entries(ast.anchors)
    .map(([k, v]) => `${k}:${v}`)
    .join(' ');
  const frameStrings = ast.frames.map((f) => serializeFrame(f)).join(' ');
  if (anchorEntries.length > 0) {
    return `§[${anchorEntries}] ${frameStrings}`;
  }
  return frameStrings;
}
