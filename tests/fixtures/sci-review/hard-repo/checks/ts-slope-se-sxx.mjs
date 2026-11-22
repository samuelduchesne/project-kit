// Reproduction check for ts-slope-se-sxx.
// Usage: node --experimental-strip-types ts-slope-se-sxx.mjs REPO
//
// For t = 0..4 and y = (0, 2, 1, 3, 4): slope 0.9, SSE 1.9, Sxx 10, so the
// standard error is sqrt(1.9 / 3 / 10) = 0.2517. Scaling t by 10 must divide
// the standard error by 10.

import { fail, loadModule, pass } from "./_load.mjs";

const { slopeStandardError } = await loadModule("src/limno/web/trend.ts");
const y = [0, 2, 1, 3, 4];
const se = slopeStandardError([0, 1, 2, 3, 4], y);
const scaled = slopeStandardError([0, 10, 20, 30, 40], y);
if (Math.abs(se - 0.25166) > 1e-4 || Math.abs(scaled - se / 10) > 1e-6)
  fail(`standard error ${se.toFixed(5)} (expected 0.25166); with t scaled by 10 it is ${scaled.toFixed(6)} (expected ${(0.025166).toFixed(6)})`);
pass(`standard error ${se.toFixed(5)}`);
