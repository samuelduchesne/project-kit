// Reproduction check for ts-least-squares-raw-sums.
// Usage: node --experimental-strip-types ts-least-squares-raw-sums.mjs REPO
//
// One minute of 10 Hz samples (a pressure-gauge burst) stamped in ms since the
// epoch (2026), rising by exactly 1e-6 units per ms. The least-squares slope
// must be 1e-6.

import { fail, loadModule, pass } from "./_load.mjs";

const { leastSquares } = await loadModule("src/limno/web/trend.ts");
const start = Date.UTC(2026, 5, 1);
const t = Array.from({ length: 600 }, (_, i) => start + 100 * i);
const y = t.map((ti) => 12 + 1e-6 * (ti - start));
const { slope } = leastSquares(t, y);
if (!(Math.abs(slope - 1e-6) <= 1e-9)) fail(`slope ${slope} per ms for an exact line of slope 1e-6`);
pass(`slope ${slope}`);
