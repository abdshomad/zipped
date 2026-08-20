import { CodecRegistry } from './registry.js';
import { CompressionLevel, CompressionResult, TokenCodec } from './types.js';

export type PayloadCategory = 'json_schema' | 'zlang_agent' | 'repetitive_ngram' | 'colloquial_shorthand' | 'generic';

/**
 * AdaptivePipelineRouter analyzes incoming payload entropy and semantics,
 * automatically dispatching to the optimal compression codec.
 */
export class AdaptivePipelineRouter {
  private registry: CodecRegistry;

  constructor(registry: CodecRegistry) {
    this.registry = registry;
  }

  /**
   * Classify payload type using fast deterministic heuristics.
   */
  public classify(input: string): PayloadCategory {
    const trimmed = input.trim();

    // 1. JSON heuristic
    if ((trimmed.startsWith('{') && trimmed.endsWith('}')) || (trimmed.startsWith('[') && trimmed.endsWith(']'))) {
      try {
        JSON.parse(trimmed);
        return 'json_schema';
      } catch {
        // Not valid JSON
      }
    }

    // 2. Multi-Agent / Semitic Z-Lang heuristic
    const agentPatterns = [
      /\b(?:the\s+)?(?:person\s+who\s+writes|writer|author|logger\s+service|logging\s+agent)\b/i,
      /\b(?:written\s+document|audit\s+log|trace\s+log|in\s+the\s+repository|mandatory\s+write)\b/i,
      /[+*@!~][a-z0-9]+/i,
    ];
    if (agentPatterns.some((p) => p.test(input))) {
      return 'zlang_agent';
    }

    // 3. High repetition n-gram heuristic
    const words = input.toLowerCase().split(/\s+/).filter(Boolean);
    const wordSet = new Set(words);
    if (words.length > 20 && words.length / wordSet.size > 1.8) {
      return 'repetitive_ngram';
    }

    // 4. Colloquial idiom heuristic
    const idiomPatterns = [
      /\b(?:by the way|away from keyboard|as soon as possible|with respect to|in my opinion|for your information)\b/i,
    ];
    if (idiomPatterns.some((p) => p.test(input))) {
      return 'colloquial_shorthand';
    }

    return 'generic';
  }

  /**
   * Route and compress input using the best candidate codec.
   */
  public async routeAndCompress(
    input: string,
    options?: Record<string, unknown>
  ): Promise<CompressionResult> {
    const category = this.classify(input);
    let preferredCodecId: string | undefined;

    switch (category) {
      case 'json_schema':
        preferredCodecId = 'schema-zip-level2';
        break;
      case 'zlang_agent':
        preferredCodecId = 'zlang-tier4';
        break;
      case 'repetitive_ngram':
        preferredCodecId = 'token-zip-level3';
        break;
      case 'colloquial_shorthand':
        preferredCodecId = 'shorthand-level1';
        break;
      default:
        preferredCodecId = undefined;
    }

    if (preferredCodecId) {
      const codec = this.registry.get(preferredCodecId);
      if (codec) {
        return await codec.compress(input, options);
      }
    }

    // Fallback: evaluate all registered codecs and select highest compression ratio
    const codecs = this.registry.list();
    if (codecs.length === 0) {
      return {
        compressed: input,
        originalLength: input.length,
        compressedLength: input.length,
        ratio: 1.0,
        level: CompressionLevel.Level1_Natural,
        codecId: 'passthrough',
      };
    }

    let bestResult: CompressionResult | null = null;
    for (const codec of codecs) {
      try {
        const res = await codec.compress(input, options);
        if (!bestResult || res.compressedLength < bestResult.compressedLength) {
          bestResult = res;
        }
      } catch {
        // Skip failed codec
      }
    }

    return bestResult || (await codecs[0].compress(input, options));
  }

  /**
   * Batch compress multiple inputs.
   */
  public async compressBatch(
    inputs: string[],
    options?: Record<string, unknown>
  ): Promise<CompressionResult[]> {
    return await Promise.all(inputs.map((inp) => this.routeAndCompress(inp, options)));
  }
}
