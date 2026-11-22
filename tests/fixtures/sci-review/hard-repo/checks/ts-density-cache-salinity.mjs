// Reproduction check for ts-density-cache-salinity.
// Usage: node --experimental-strip-types ts-density-cache-salinity.mjs REPO
//
// The memoised density must equal the direct evaluation for fresh and for
// saline water at the same temperature.

import { fail, loadModule, pass } from "./_load.mjs";

const { densityOf, waterDensity, clearDensityCache } = await loadModule("src/limno/web/density.ts");
clearDensityCache();
const fresh = densityOf(10, 0);
const saline = densityOf(10, 8);
const expected = waterDensity(10, 8);
if (Math.abs(saline - expected) > 1e-9) fail(`density at 10 C and 8 g/kg is ${saline.toFixed(3)} after a fresh-water lookup (${fresh.toFixed(3)}); direct value ${expected.toFixed(3)}`);
pass(`cached densities ${fresh.toFixed(3)} and ${saline.toFixed(3)}`);
