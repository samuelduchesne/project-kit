// Reproduction check for ts-cache-key-year.
// Usage: node --experimental-strip-types ts-cache-key-year.mjs REPO
//
// Queries the QC factor with reference year 2020, switches to 2030 and queries
// again. The table holds 1.7 for 2020 and 1.2 for 2030.

import { fail, loadModule, pass } from "./_load.mjs";

const { emissionFactor, setReferenceYear } = await loadModule("src/sci/analysis/emissions.ts");
setReferenceYear(2020);
const first = emissionFactor("QC");
setReferenceYear(2030);
const second = emissionFactor("QC");
if (first !== 1.7) fail(`2020 factor ${first}; expected 1.7`);
if (second !== 1.2) fail(`2030 factor ${second}; expected 1.2 (the 2020 value was returned from the cache)`);
pass(`factors ${first} (2020) and ${second} (2030)`);
