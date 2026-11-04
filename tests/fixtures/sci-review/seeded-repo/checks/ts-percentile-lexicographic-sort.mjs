// Reproduction check for ts-percentile-lexicographic-sort.
// Usage: node --experimental-strip-types ts-percentile-lexicographic-sort.mjs REPO
//
// percentile([10, 9, 100, 2], 50): the sorted readings are [2, 9, 10, 100], so
// the median by linear interpolation is 9.5.

import { fail, loadModule, pass } from "./_load.mjs";

const { percentile } = await loadModule("src/sci/analysis/rank.ts");
const value = percentile([10, 9, 100, 2], 50);
if (value !== 9.5) fail(`percentile ${value}; expected 9.5`);
pass(`percentile ${value}`);
