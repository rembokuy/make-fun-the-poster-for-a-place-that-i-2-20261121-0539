// VELMARA entrypoint: place the finished poster where the grader looks.
// Node 22, standard library only — no network, no extra packages.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const poster = readFileSync(new URL("./entry.png", import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true, mode: 0o755 });
writeFileSync(join(outDir, "entry.png"), poster);
console.log(`wrote ${poster.length} bytes to ${join(outDir, "entry.png")}`);
