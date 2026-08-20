#!/usr/bin/env node

import { executeCompress, executeDecompress, executeStats } from './index.js';

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';

  switch (command) {
    case 'compress': {
      const input = args[1] || '';
      const codecFlagIdx = args.indexOf('--codec');
      const codec = codecFlagIdx !== -1 ? args[codecFlagIdx + 1] : undefined;
      const result = await executeCompress(input, { codec });
      process.stdout.write(result);
      break;
    }
    case 'decompress': {
      const input = args[1] || '';
      const codecFlagIdx = args.indexOf('--codec');
      const codec = codecFlagIdx !== -1 ? args[codecFlagIdx + 1] : 'shorthand-level1';
      const result = await executeDecompress(input, codec);
      process.stdout.write(result);
      break;
    }
    case 'stats': {
      const stats = executeStats();
      process.stdout.write(JSON.stringify(stats, null, 2) + '\n');
      break;
    }
    default:
      process.stdout.write('Usage: zipped [compress|decompress|stats] <input> [--codec <id>]\n');
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
