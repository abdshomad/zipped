import { describe, it, expect } from 'vitest';
import { ZippedEngine, AdaptivePipelineRouter } from '../src/index.js';

describe('AdaptivePipelineRouter', () => {
  it('classifies JSON payloads accurately', () => {
    const engine = new ZippedEngine();
    const router = new AdaptivePipelineRouter(engine.registry);

    expect(router.classify('{"key": "value", "id": 123}')).toBe('json_schema');
    expect(router.classify('[{"id": 1}, {"id": 2}]')).toBe('json_schema');
  });

  it('classifies Z-Lang multi-agent prompts accurately', () => {
    const engine = new ZippedEngine();
    const router = new AdaptivePipelineRouter(engine.registry);

    expect(router.classify('The author who writes the written document in the repository')).toBe('zlang_agent');
    expect(router.classify('+user create *session @db')).toBe('zlang_agent');
  });

  it('classifies colloquial shorthand accurately', () => {
    const engine = new ZippedEngine();
    const router = new AdaptivePipelineRouter(engine.registry);

    expect(router.classify('Please submit this as soon as possible, by the way.')).toBe('colloquial_shorthand');
  });

  it('autoCompress falls back to passthrough when registry is empty', async () => {
    const engine = new ZippedEngine();
    const result = await engine.autoCompress('Hello world');
    expect(result.codecId).toBe('passthrough');
    expect(result.compressed).toBe('Hello world');
  });
});
