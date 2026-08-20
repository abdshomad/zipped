# Sub-Plan 2.1.1 — Level 2 Symbolic & Schema Zip Codec (`packages/plugin-schema-zip`)

## Objective & Quantifiable Measure
- **Target:** Implement Level 2 Symbolic & Schema Zip Codec for compact structured data (JSON/key-value/AST payloads).
- **Mechanism:** Sourced from `ref/alexmullins-zip` and `ref/kuba-zip` central directory/header packing. Employs a single 1-token header declaring column/field names once (e.g. `§[id,name,role,status]`), followed by compact delimiter-packed tuple arrays.
- **Quantifiable Benchmark:** $\ge 50\%$ token reduction on structured/tabular payloads across `o200k_base` and `cl100k_base` with $100\%$ bidirectional JSON losslessness.

## Implementation Tasks
1. `2.1.1`: Create `packages/plugin-schema-zip` with `SchemaZipCodec` implementing `compress(jsonObj)` and `decompress(compactStr)`.
2. `2.1.2`: Wire `plugin-schema-zip` into `@zipped/core` engine registry.
3. `2.1.3`: Bench-test on complex nested JSON payloads with `o200k_base` and `cl100k_base`.
