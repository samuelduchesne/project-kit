// Reproduction check for ts-correlation-unpaired-gaps.
// Usage: node --experimental-strip-types ts-correlation-unpaired-gaps.mjs REPO
//
// b = 2 a exactly, with one logger gap in each series at different times.
// Over the complete pairs the correlation is 1.

import { fail, loadModule, pass } from "./_load.mjs";

const { correlation } = await loadModule("src/limno/web/series.ts");
const a = [1, 4, 2, NaN, 5, 3, 6, 2, 7];
const b = [2, NaN, 4, 6, 10, 6, 12, 4, 14];
const r = correlation(a, b);
if (!(Math.abs(r - 1) < 1e-12)) fail(`correlation ${r.toFixed(4)} for b = 2a with gaps at different times; expected 1`);
pass(`correlation ${r}`);
