// Reproduction check for ts-barometer-hpa.
// Usage: node --experimental-strip-types ts-barometer-hpa.mjs REPO
//
// A transducer reading 150 359 Pa (absolute) under a barometric pressure of
// 1013.25 hPa sits under 49 034 Pa of water, 5.00 m at 1000 kg/m^3.

import { fail, loadModule, pass } from "./_load.mjs";

const { compensatedDepths } = await loadModule("src/limno/web/level.ts");
const series = compensatedDepths([{ time: 0, pressure: 150359 }], [{ time: 0, pressure: 1013.25, airTemperature: 10, windSpeed: 3 }]);
const depth = series[0].depth;
if (Math.abs(depth - 5.0) > 0.01) fail(`depth ${depth.toFixed(3)} m for 150359 Pa under 1013.25 hPa; expected 5.00 m`);
pass(`depth ${depth.toFixed(3)} m`);
