// Reproduction check for ts-surface-gradient-nonuniform.
// Usage: node --experimental-strip-types ts-surface-gradient-nonuniform.mjs REPO
//
// Sensors at 0.5, 1 and 2 m on the profile T(z) = 290 - 0.5 (z - 0.5)^2 K,
// whose gradient at 0.5 m is zero. The documented second-order one-sided
// difference is exact for quadratic profiles.

import { fail, loadModule, pass } from "./_load.mjs";

const { surfaceGradient } = await loadModule("src/limno/web/stratification.ts");
const depths = [0.5, 1, 2, 4];
const temperatures = depths.map((z) => 290 - 0.5 * (z - 0.5) ** 2);
const g = surfaceGradient({ time: 0, depths, temperatures, salinities: [0, 0, 0, 0] });
if (Math.abs(g) > 1e-9) fail(`surface gradient ${g.toFixed(4)} K/m for sensors at 0.5, 1, 2 m on a quadratic profile; expected 0`);
pass(`surface gradient ${g}`);
