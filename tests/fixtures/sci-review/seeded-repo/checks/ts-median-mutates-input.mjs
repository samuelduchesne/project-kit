// Reproduction check for ts-median-mutates-input.
// Usage: node --experimental-strip-types ts-median-mutates-input.mjs REPO
//
// summarise([0, 1, 2], [3, 1, 2], [1, 1, 1]): the peak value 3 occurs at time
// 0, the median is 2, and the caller's values array must be left unchanged.

import { fail, loadModule, pass } from "./_load.mjs";

const { summarise } = await loadModule("src/sci/analysis/summary.ts");
const values = [3, 1, 2];
const summary = summarise([0, 1, 2], values, [1, 1, 1]);
if (summary.peakTime !== 0) fail(`peakTime ${summary.peakTime}; expected 0`);
if (summary.median !== 2) fail(`median ${summary.median}; expected 2`);
if (values.join(",") !== "3,1,2") fail(`the caller's values became [${values.join(", ")}]`);
pass(`peakTime ${summary.peakTime}, median ${summary.median}, values unchanged`);
