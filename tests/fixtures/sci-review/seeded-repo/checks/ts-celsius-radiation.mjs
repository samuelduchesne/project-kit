// Reproduction check for ts-celsius-radiation.
// Usage: node --experimental-strip-types ts-celsius-radiation.mjs REPO
//
// Net long-wave flux from a surface at 20 degC to a sky at 0 degC with
// emissivity 0.9: 0.9 * sigma * (293.15**4 - 273.15**4), about 92.8 W/m^2.

import { fail, loadModule, pass } from "./_load.mjs";

const { netLongwaveFlux } = await loadModule("src/sci/core/surfaceHeat.ts");
const sigma = 5.670374419e-8;
const expected = 0.9 * sigma * (293.15 ** 4 - 273.15 ** 4);
const result = netLongwaveFlux(20, 0, 0.9);
if (Math.abs(result - expected) > 1e-3 * expected) fail(`flux ${result} W/m^2; expected ${expected} W/m^2`);
pass(`flux ${result} W/m^2`);
