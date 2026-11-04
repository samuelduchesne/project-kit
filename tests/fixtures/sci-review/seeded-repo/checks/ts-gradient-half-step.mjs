// Reproduction check for ts-gradient-half-step.
// Usage: node --experimental-strip-types ts-gradient-half-step.mjs REPO
//
// Differentiates y = x**2 sampled at x = 0, 0.1, ..., 1.0. The central
// difference is exact for quadratics, so the derivative at x = 0.5 is 1.0.

import { fail, loadModule, pass } from "./_load.mjs";

const { gradient } = await loadModule("src/sci/core/differentiate.ts");
const dx = 0.1;
const y = Array.from({ length: 11 }, (_, i) => (i * dx) ** 2);
const g = gradient(y, dx);
if (Math.abs(g[5] - 1.0) > 1e-9) fail(`derivative at x = 0.5 is ${g[5]}; expected 1`);
pass(`derivative at x = 0.5 is ${g[5]}`);
