// Reproduction check for ts-schmidt-centre-of-volume.
// Usage: node --experimental-strip-types ts-schmidt-centre-of-volume.mjs REPO
//
// A lake of uniform temperature is fully mixed; its Schmidt stability is zero
// whatever its shape. The hypsography narrows with depth, as real basins do.
// The sensors reach below the deepest hypsography depth.

import { fail, loadModule, pass } from "./_load.mjs";

const { schmidtStability } = await loadModule("src/limno/web/stratification.ts");
const profile = { time: 0, depths: [0, 10, 25], temperatures: [285.15, 285.15, 285.15], salinities: [0, 0, 0] };
const hypsography = { depths: [0, 5, 10, 15, 20], areas: [1e6, 7.5e5, 5e5, 2.5e5, 1e3] };
const s = schmidtStability(profile, hypsography);
if (!(Math.abs(s) < 1e-3)) fail(`Schmidt stability ${s.toExponential(3)} J/m^2 for a uniform lake; expected 0`);
pass(`Schmidt stability ${s.toExponential(2)} J/m^2`);
