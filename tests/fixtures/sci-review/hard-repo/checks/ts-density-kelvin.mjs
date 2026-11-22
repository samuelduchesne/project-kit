// Reproduction check for ts-density-kelvin.
// Usage: node --experimental-strip-types ts-density-kelvin.mjs REPO
//
// A profile at 277.13 K (3.98 C, the density maximum of fresh water) must give
// sensor densities of about 1000.0 kg/m^3.

import { fail, loadModule, pass } from "./_load.mjs";

const { sensorDensities } = await loadModule("src/limno/web/stratification.ts");
const profile = { time: 0, depths: [1, 5, 10], temperatures: [277.13, 277.13, 277.13], salinities: [0, 0, 0] };
const rho = sensorDensities(profile);
if (rho.some((r) => Math.abs(r - 1000) > 0.05)) fail(`densities ${rho.map((r) => r.toFixed(2)).join(", ")} kg/m^3 at 277.13 K; expected 1000.0`);
pass(`densities ${rho.map((r) => r.toFixed(3)).join(", ")}`);
