// Reproduction check for ts-rescale-zero-span.
// Usage: node --experimental-strip-types ts-rescale-zero-span.mjs REPO
//
// Rescales a constant batch [5, 5, 5]. A correct implementation either throws
// a documented error or returns finite values; it must not return NaN.

import { fail, loadModule, pass } from "./_load.mjs";

const { rescale } = await loadModule("src/sci/core/normalise.ts");
let result;
try {
  result = rescale([5, 5, 5]);
} catch (error) {
  pass(`constant batch rejected (${error.message})`);
}
if (!result.every(Number.isFinite)) fail(`rescale([5, 5, 5]) returned [${result.join(", ")}]`);
pass(`rescale([5, 5, 5]) returned [${result.join(", ")}]`);
