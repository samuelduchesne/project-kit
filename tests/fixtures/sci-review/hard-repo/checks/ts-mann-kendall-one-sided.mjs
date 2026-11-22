// Reproduction check for ts-mann-kendall-one-sided.
// Usage: node --experimental-strip-types ts-mann-kendall-one-sided.mjs REPO
//
// For y = (1, 3, 2, 5, 4, 6, 8, 7, 10, 9): S = 37, Var(S) = 125, Z = 36 /
// sqrt(125) = 3.220; the two-sided p-value is 2 (1 - Phi(3.220)) = 0.00128.

import { fail, loadModule, pass } from "./_load.mjs";

const { mannKendall } = await loadModule("src/limno/web/trend.ts");
const r = mannKendall([1, 3, 2, 5, 4, 6, 8, 7, 10, 9]);
if (r.s !== 37) fail(`S = ${r.s}; expected 37`);
if (Math.abs(r.p - 0.00128) > 2e-5) fail(`two-sided p-value ${r.p.toFixed(5)}; expected 0.00128`);
pass(`p = ${r.p.toFixed(5)}`);
