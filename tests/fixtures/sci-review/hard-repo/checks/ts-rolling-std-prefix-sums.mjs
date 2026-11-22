// Reproduction check for ts-rolling-std-prefix-sums.
// Usage: node --experimental-strip-types ts-rolling-std-prefix-sums.mjs REPO
//
// 100 000 one-minute transducer readings around 150 000 Pa with a 0.05 Pa
// ripple; the standard deviation of any 60-sample window is about 0.0357 Pa
// (computed here by two passes). Compares the last window.

import { fail, loadModule, pass } from "./_load.mjs";

const { rollingStd } = await loadModule("src/limno/web/series.ts");
const n = 100000;
const values = Array.from({ length: n }, (_, i) => 150000 + 0.05 * Math.sin((2 * Math.PI * i) / 30));
const window = 60;
const out = rollingStd(values, window);
const last = values.slice(n - window);
const mean = last.reduce((s, v) => s + v, 0) / window;
const exact = Math.sqrt(last.reduce((s, v) => s + (v - mean) ** 2, 0) / (window - 1));
const got = out[n - 1];
if (!(Math.abs(got - exact) <= 0.01 * exact)) fail(`last-window std ${got} Pa; two-pass value ${exact.toFixed(5)} Pa`);
pass(`last-window std ${got.toFixed(5)} Pa (two-pass ${exact.toFixed(5)})`);
