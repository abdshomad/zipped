import { describe, it, expect } from 'vitest';
import {
  deriveMorphToken,
  parseMorphToken,
} from '../src/morphology.js';
import { MorphRole } from '../src/types.js';
import {
  serializeFrame,
  deserializeFrame,
  serializeAST,
} from '../src/frame.js';
import { ZLangCodec } from '../src/codec.js';
import { ZippedEngine, CompressionLevel } from '@zipped/core';
import pluginZLang from '../src/index.js';

describe('Z-Lang Semitic Morphology', () => {
  it('derives correct morphological tokens with 1-token sigils', () => {
    expect(deriveMorphToken(MorphRole.Agent, 'write')).toBe('+write');
    expect(deriveMorphToken(MorphRole.Patient, 'write')).toBe('*write');
    expect(deriveMorphToken(MorphRole.Locus, 'repo')).toBe('@repo');
    expect(deriveMorphToken(MorphRole.Causative, 'log')).toBe('!log');
    expect(deriveMorphToken(MorphRole.Reciprocal, 'write')).toBe('~write');
  });

  it('parses morphological tokens correctly', () => {
    expect(parseMorphToken('+write')).toEqual({ role: MorphRole.Agent, root: 'write' });
    expect(parseMorphToken('*log')).toEqual({ role: MorphRole.Patient, root: 'log' });
    expect(parseMorphToken('@repo')).toEqual({ role: MorphRole.Locus, root: 'repo' });
    expect(parseMorphToken('eval')).toEqual({ role: MorphRole.Verb, root: 'eval' });
  });
});

describe('Z-Lang Relational Frames', () => {
  it('serializes structured frame into compact bracketed format', () => {
    const frame = {
      agent: 'user',
      action: 'commit',
      patient: 'code',
      locus: 'repo',
      constraints: { timeout: 30 },
    };
    const serialized = serializeFrame(frame);
    expect(serialized).toBe('⟨+user commit *code @repo !{timeout:30}⟩');
  });

  it('deserializes bracketed frame into structured object', () => {
    const serialized = '⟨+user commit *code @repo !{timeout:30}⟩';
    const frame = deserializeFrame(serialized);
    expect(frame.agent).toBe('user');
    expect(frame.action).toBe('commit');
    expect(frame.patient).toBe('code');
    expect(frame.locus).toBe('repo');
    expect(frame.constraints).toEqual({ timeout: 30 });
  });

  it('serializes full AST with anchors', () => {
    const ast = {
      anchors: { '§E1': 'User', '§E2': 'Database' },
      frames: [
        { agent: '§E1', action: 'query', locus: '§E2' },
      ],
    };
    const serialized = serializeAST(ast);
    expect(serialized).toContain('§[§E1:User §E2:Database]');
    expect(serialized).toContain('⟨+§E1 query @§E2⟩');
  });
});

describe('ZLangCodec', () => {
  const codec = new ZLangCodec();

  it('compresses natural language using Semitic morphology patterns', () => {
    const input = 'the person who writes the document in the repository';
    const result = codec.compress(input);
    expect(result.level).toBe(CompressionLevel.Level4_LLMNative);
    expect(result.compressed).toContain('+write');
    expect(result.compressed).toContain('*write');
    expect(result.compressed).toContain('@repo');
    expect(result.compressedLength).toBeLessThan(result.originalLength);
  });

  it('decompresses Z-Lang tokens back to grounded English', () => {
    const compressed = '+write *write @repo';
    const decompressed = codec.decompress(compressed);
    expect(decompressed).toContain('the author who writes');
    expect(decompressed).toContain('the written document');
    expect(decompressed).toContain('in the repository');
  });
});

describe('Cordis Plugin Registration', () => {
  it('registers ZLangCodec in ZippedEngine', () => {
    const engine = new ZippedEngine();
    pluginZLang.apply(engine);

    const codec = engine.registry.get('zlang-tier4');
    expect(codec).toBeDefined();
    expect(codec?.level).toBe(CompressionLevel.Level4_LLMNative);
  });
});
