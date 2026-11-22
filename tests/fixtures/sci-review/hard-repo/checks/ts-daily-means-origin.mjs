// Reproduction check for ts-daily-means-origin.
// Usage: node --experimental-strip-types ts-daily-means-origin.mjs REPO
//
// Hourly samples from 2026-06-01 12:00 to 2026-06-02 11:00 UTC, valued 1 on
// June 1 and 3 on June 2. The UTC calendar days give two means, 1 and 3,
// stamped at 00:00 UTC.

import { fail, loadModule, pass } from "./_load.mjs";

const { dailyMeans } = await loadModule("src/limno/web/series.ts");
const start = Date.UTC(2026, 5, 1, 12);
const samples = Array.from({ length: 24 }, (_, i) => ({ time: start + i * 3600000, value: i < 12 ? 1 : 3 }));
const days = dailyMeans(samples);
const want = [
  { time: Date.UTC(2026, 5, 1), value: 1 },
  { time: Date.UTC(2026, 5, 2), value: 3 },
];
const ok = days.length === 2 && days.every((d, i) => d.time === want[i].time && Math.abs(d.value - want[i].value) < 1e-12);
if (!ok) fail(`daily means ${JSON.stringify(days.map((d) => [new Date(d.time).toISOString(), d.value]))}; expected June 1 = 1, June 2 = 3 at 00:00 UTC`);
pass("two UTC days with means 1 and 3");
