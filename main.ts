// main.ts — copy the rendered entry image to /output/entry.png.
// Node 22, stdlib only. Deterministic: a plain byte-for-byte copy,
// so running it twice produces identical output.
import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'entry.png');
const outDir = '/output';
const dest = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
console.log(`copied ${src} -> ${dest}`);
