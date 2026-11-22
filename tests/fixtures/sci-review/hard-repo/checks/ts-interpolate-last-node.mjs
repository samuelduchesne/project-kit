// Reproduction check for ts-interpolate-last-node.
// Usage: node --experimental-strip-types ts-interpolate-last-node.mjs REPO
//
// Interpolating at the deepest sensor (an end point the function documents as
// admissible) must return that sensor's value.

import { fail, loadModule, pass } from "./_load.mjs";

const { interpolate } = await loadModule("src/limno/web/profile.ts");
const value = interpolate([0, 2, 5, 10], [290, 288, 284, 280], 10);
if (value !== 280) fail(`interpolate at the last depth 10 m gives ${value}; expected 280`);
pass(`interpolate at the last depth gives ${value}`);
