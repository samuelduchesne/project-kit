"""Build the seeded fixture repository used to measure sci-review.

Usage:
    python3 build.py --out DIR     create the git repository at DIR
    python3 build.py --check       verify manifest.json against the embedded sources only

The repository has two branches. ``main`` holds correct baseline code. ``feature``
adds the seeded defects, the correct look-alike constructs and the contested
construct listed in ``manifest.json``, in Python and TypeScript files under
``src/sci/core/`` and ``src/sci/analysis/``. The repository is left checked out on
``feature`` and has no remote, so ``panel.py scope --mode branch`` resolves
``main`` as the base.

The sources carry no marker of any kind. ``manifest.json`` locates each entry by
``anchor``, a substring that occurs exactly once in the feature version of the
file, and records the 1-based line of that occurrence in ``line``. Every build
first verifies that each anchor is unique, that each recorded line matches, and
that look-alikes and the contested construct lie far enough from every seeded
defect that a single finding cannot match both.

Only the Python standard library is used, here and in the generated Python code.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "manifest.json"

# Tolerance used by score.py when it matches a finding to a manifest line.
MATCH_TOLERANCE = 3
# Minimum distance, in lines, between a look-alike or contested range and a seeded
# defect line in the same file: twice the tolerance plus one, so that no finding
# range can match both.
MIN_SEPARATION = 2 * MATCH_TOLERANCE + 1

GIT_IDENTITY = ("-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false")
COMMIT_DATES = ("2026-01-05T10:00:00+00:00", "2026-01-12T14:30:00+00:00", "2026-01-13T09:15:00+00:00")


@dataclass(frozen=True)
class SourceFile:
    """One file of the generated repository."""

    path: str
    text: str


@dataclass(frozen=True)
class Commit:
    """A commit that writes a set of files."""

    message: str
    files: tuple[SourceFile, ...]


@dataclass(frozen=True)
class Located:
    """A manifest entry located by an anchor substring."""

    kind: str
    id: str
    file: str
    line: int
    anchor: str
    line_end: int
    anchor_end: str | None


# ---------------------------------------------------------------------------
# Repository scaffolding (main)
# ---------------------------------------------------------------------------

README = """\
# sci-sensors

Analysis routines for building-sensor data: quadrature, heat transfer,
preprocessing, resampling and emissions accounting. Python modules live under
`src/sci/`, and the TypeScript modules used by the dashboard sit beside them.

## Layout

- `src/sci/core/`: numerical and physical building blocks.
- `src/sci/analysis/`: statistical preparation and aggregation of sensor series.
"""

PYPROJECT = """\
[project]
name = "sci-sensors"
version = "0.3.0"
description = "Analysis routines for building-sensor data"
requires-python = ">=3.10"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/sci"]
"""

PACKAGE_JSON = """\
{
  "name": "sci-sensors-dashboard",
  "version": "0.3.0",
  "private": true,
  "type": "module",
  "scripts": {
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {
    "typescript": "^5.6.0"
  }
}
"""

TSCONFIG = """\
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noEmit": true,
    "allowImportingTsExtensions": true
  },
  "include": ["src/**/*.ts"]
}
"""

GITIGNORE = """\
__pycache__/
*.pyc
node_modules/
dist/
"""

PKG_INIT = '''\
"""Analysis routines for building-sensor data."""
'''

CORE_INIT = '''\
"""Numerical and physical building blocks."""
'''

ANALYSIS_INIT = '''\
"""Statistical preparation and aggregation of sensor series."""
'''

# ---------------------------------------------------------------------------
# src/sci/core/quadrature.py
# ---------------------------------------------------------------------------

QUADRATURE_MAIN = '''\
"""Quadrature rules for uniformly sampled data."""

from __future__ import annotations

import math
from collections.abc import Sequence


def trapezoid(y: Sequence[float], h: float) -> float:
    """Integrate uniformly spaced samples with the composite trapezoidal rule.

    Args:
        y: Sample values at spacing ``h``; at least two samples.
        h: Sample spacing, positive.

    Returns:
        The approximation h * (y[0] / 2 + y[1] + ... + y[n - 2] + y[n - 1] / 2).
    """
    if len(y) < 2:
        raise ValueError("the trapezoidal rule needs at least two samples")
    if h <= 0.0:
        raise ValueError("the sample spacing must be positive")
    interior = math.fsum(y[1:-1])
    return h * (0.5 * (y[0] + y[-1]) + interior)
'''

QUADRATURE_FEATURE = (
    QUADRATURE_MAIN
    + '''

def simpson(y: Sequence[float], h: float) -> float:
    """Integrate uniformly spaced samples with the composite Simpson rule.

    The rule applies Simpson's 1/3 formula to consecutive pairs of intervals,
    which gives the weights h / 3 * (1, 4, 2, 4, ..., 2, 4, 1). It is exact for
    polynomials of degree three or less.

    Args:
        y: Sample values at spacing ``h``; an odd number, at least three.
        h: Sample spacing, positive.

    Returns:
        The approximation of the integral over [0, (n - 1) * h].
    """
    n = len(y)
    if n < 3 or n % 2 == 0:
        raise ValueError("Simpson's rule needs an odd number of samples, at least three")
    if h <= 0.0:
        raise ValueError("the sample spacing must be positive")
    odd = math.fsum(y[2 : n - 1 : 2])
    even = math.fsum(y[1 : n - 1 : 2])
    return h / 3.0 * (y[0] + 4.0 * odd + 2.0 * even + y[-1])
'''
)

# ---------------------------------------------------------------------------
# src/sci/core/numerics.py
# ---------------------------------------------------------------------------

NUMERICS = '''\
"""Streaming summary statistics for sensor series."""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Moments:
    """Count, mean and population variance of a series."""

    count: int
    mean: float
    variance: float

    @property
    def std(self) -> float:
        """Population standard deviation."""
        return math.sqrt(self.variance)


def moments(samples: Iterable[float]) -> Moments:
    """Compute the count, mean and population variance in a single pass.

    The samples are consumed once, so the function accepts generators that
    stream readings from disk without holding the series in memory.

    Args:
        samples: The readings, at least one.

    Returns:
        The count, the mean and the population variance of the readings.
    """
    count = 0
    total = 0.0
    total_sq = 0.0
    for x in samples:
        count += 1
        total += x
        total_sq += x * x
    if count == 0:
        raise ValueError("moments of an empty series")
    mean = total / count
    return Moments(count, mean, total_sq / count - mean * mean)
'''

# ---------------------------------------------------------------------------
# src/sci/core/heat.py
# ---------------------------------------------------------------------------

HEAT = '''\
"""One-dimensional transient heat conduction."""

from __future__ import annotations

from collections.abc import Sequence


def diffuse(u0: Sequence[float], alpha: float, dx: float, dt: float, steps: int) -> list[float]:
    """Advance the heat equation u_t = alpha * u_xx with the explicit FTCS scheme.

    The end nodes are Dirichlet boundaries and keep their initial values.

    Args:
        u0: Initial temperature at each grid node, in kelvin.
        alpha: Thermal diffusivity, in m^2/s.
        dx: Grid spacing, in m.
        dt: Time step, in s.
        steps: Number of time steps to take.

    Returns:
        The temperature at each node after ``steps * dt`` seconds.
    """
    if alpha <= 0.0 or dx <= 0.0 or dt <= 0.0:
        raise ValueError("alpha, dx and dt must be positive")
    if len(u0) < 3:
        raise ValueError("the grid needs at least three nodes")
    r = alpha * dt / (dx * dx)
    u = list(u0)
    for _ in range(steps):
        interior = [u[i] + r * (u[i - 1] - 2.0 * u[i] + u[i + 1]) for i in range(1, len(u) - 1)]
        u = [u[0], *interior, u[-1]]
    return u
'''

# ---------------------------------------------------------------------------
# src/sci/core/geometry.py
# ---------------------------------------------------------------------------

GEOMETRY = '''\
"""Geometry of surveyed paths.

The paths are surveyed along graded roads and along unsurfaced hill paths
between them. Segment inclines are read from a hand-held clinometer with a
stated accuracy of 0.5 degrees (0.0087 rad), and the elevation model works to
first order in the incline.
"""

from __future__ import annotations

import math
from collections.abc import Sequence


def elevation_gain(lengths: Sequence[float], inclines: Sequence[float]) -> float:
    """Return the net elevation change along a path of straight segments.

    The rise of each segment is taken as length * incline, the first-order
    form of length * sin(incline).

    Args:
        lengths: Length of each segment measured along the slope, in m.
        inclines: Incline of each segment above the horizontal, in radians;
            negative for a descent.

    Returns:
        The net change in elevation from the first to the last point, in m.
    """
    if len(lengths) != len(inclines):
        raise ValueError("lengths and inclines must have the same length")
    return math.fsum(length * incline for length, incline in zip(lengths, inclines))
'''

# ---------------------------------------------------------------------------
# src/sci/core/differentiate.ts
# ---------------------------------------------------------------------------

DIFFERENTIATE_TS = """\
/**
 * Finite-difference derivatives of uniformly sampled series.
 */

/**
 * Estimate dy/dx at every sample of a uniformly spaced series.
 *
 * Interior points use the second-order central difference
 * (y[i + 1] - y[i - 1]) / (2 dx); the end points use first-order one-sided
 * differences.
 *
 * @param y - sample values, at least two
 * @param dx - sample spacing, positive
 * @returns the derivative estimate at each sample
 */
export function gradient(y: readonly number[], dx: number): number[] {
  const n = y.length;
  if (n < 2) throw new RangeError("gradient needs at least two samples");
  if (!(dx > 0)) throw new RangeError("dx must be positive");
  const g = new Array<number>(n);
  g[0] = (y[1] - y[0]) / dx;
  g[n - 1] = (y[n - 1] - y[n - 2]) / dx;
  for (let i = 1; i < n - 1; i++) {
    g[i] = (y[i + 1] - y[i - 1]) / dx;
  }
  return g;
}
"""

# ---------------------------------------------------------------------------
# src/sci/core/normalise.ts
# ---------------------------------------------------------------------------

NORMALISE_TS_MAIN = """\
/**
 * Scaling of sensor readings onto a common range.
 */

/**
 * Map readings onto [0, 1] using the rated range of the sensor.
 *
 * @param readings - raw readings in sensor units
 * @param ratedMin - lower end of the rated range
 * @param ratedMax - upper end of the rated range, greater than ratedMin
 * @returns the readings scaled so that ratedMin maps to 0 and ratedMax to 1
 */
export function rescale(readings: readonly number[], ratedMin: number, ratedMax: number): number[] {
  if (!(ratedMax > ratedMin)) throw new RangeError("ratedMax must exceed ratedMin");
  const span = ratedMax - ratedMin;
  return readings.map((r) => (r - ratedMin) / span);
}
"""

NORMALISE_TS_FEATURE = """\
/**
 * Scaling of sensor readings onto a common range.
 */

/**
 * Map readings onto [0, 1] using the observed range of the batch.
 *
 * The rated range of many installed sensors is not recorded, so the batch
 * minimum maps to 0 and the batch maximum maps to 1.
 *
 * @param readings - raw readings in sensor units, at least one
 * @returns the readings scaled onto [0, 1]
 */
export function rescale(readings: readonly number[]): number[] {
  if (readings.length === 0) throw new RangeError("cannot rescale an empty batch");
  const lo = Math.min(...readings);
  const hi = Math.max(...readings);
  const span = hi - lo;
  return readings.map((r) => (r - lo) / span);
}
"""

# ---------------------------------------------------------------------------
# src/sci/core/surfaceHeat.ts
# ---------------------------------------------------------------------------

SURFACE_HEAT_TS = """\
/**
 * Surface heat-transfer relations for building envelopes.
 */

/** Stefan-Boltzmann constant, in W m^-2 K^-4. */
export const SIGMA = 5.670374419e-8;

/**
 * Steady conductive heat flux through a homogeneous layer, in W/m^2.
 *
 * @param conductivity - thermal conductivity of the layer, in W/(m K)
 * @param thickness - layer thickness, in m
 * @param insideC - inside surface temperature, in degrees Celsius
 * @param outsideC - outside surface temperature, in degrees Celsius
 * @returns the flux from inside to outside; negative when heat flows inwards
 */
export function conductiveFlux(conductivity: number, thickness: number, insideC: number, outsideC: number): number {
  if (!(thickness > 0)) throw new RangeError("thickness must be positive");
  return (conductivity * (insideC - outsideC)) / thickness;
}

/**
 * Net long-wave radiative flux from a grey surface to the sky, in W/m^2.
 *
 * @param surfaceC - surface temperature, in degrees Celsius
 * @param skyC - effective sky temperature, in degrees Celsius
 * @param emissivity - long-wave emissivity of the surface, in [0, 1]
 * @returns the net flux leaving the surface
 */
export function netLongwaveFlux(surfaceC: number, skyC: number, emissivity: number): number {
  if (emissivity < 0 || emissivity > 1) throw new RangeError("emissivity must lie in [0, 1]");
  return emissivity * SIGMA * (surfaceC ** 4 - skyC ** 4);
}
"""

# ---------------------------------------------------------------------------
# src/sci/analysis/preprocess.py
# ---------------------------------------------------------------------------

PREPROCESS = '''\
"""Preparation of sensor features for model training."""

from __future__ import annotations

import math
import statistics
from collections.abc import Sequence

MISSING = -9999.0
"""Value written by the logger in place of a reading that was not recorded."""


def drop_missing(readings: Sequence[float]) -> list[float]:
    """Remove the readings that the logger marked as not recorded."""
    return [v for v in readings if v != MISSING]


def standardise_split(values: Sequence[float], test_fraction: float) -> tuple[list[float], list[float]]:
    """Standardise a feature and split it into training and test parts.

    The last ``ceil(test_fraction * n)`` values form the test part, so the split
    preserves time order. Each value is mapped to (v - mean) / std, with the
    population standard deviation.

    Args:
        values: The feature, in time order.
        test_fraction: Share of the values held out for testing, in (0, 1).

    Returns:
        The standardised training values and the standardised test values.
    """
    n = len(values)
    n_test = math.ceil(test_fraction * n)
    if not 0 < n_test < n:
        raise ValueError("test_fraction must leave at least one value in each part")
    mean = statistics.fmean(values)
    std = statistics.pstdev(values)
    if not std > 0.0:
        raise ValueError("cannot standardise a constant feature")
    scaled = [(v - mean) / std for v in values]
    return scaled[: n - n_test], scaled[n - n_test :]
'''

# ---------------------------------------------------------------------------
# src/sci/analysis/aggregate.py
# ---------------------------------------------------------------------------

AGGREGATE = '''\
"""Parallel aggregation of metered energy."""

from __future__ import annotations

import math
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed


def chunk_energy(readings: Sequence[float], interval_s: float) -> float:
    """Energy in J of power readings in W, each held for ``interval_s`` seconds."""
    return math.fsum(readings) * interval_s


def total_energy(chunks: Sequence[Sequence[float]], interval_s: float, workers: int = 4) -> float:
    """Total metered energy in J over chunks of power readings, computed in parallel.

    Args:
        chunks: Power readings in W, split into chunks of any size.
        interval_s: Duration represented by each reading, in s.
        workers: Number of worker threads.

    Returns:
        The energy of all readings, in J.
    """
    total = 0.0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(chunk_energy, chunk, interval_s) for chunk in chunks]
        for future in as_completed(futures):
            total += future.result()
    return total
'''

# ---------------------------------------------------------------------------
# src/sci/analysis/resample.py
# ---------------------------------------------------------------------------

RESAMPLE = '''\
"""Resampling methods for uncertainty estimates and hypothesis tests."""

from __future__ import annotations

import random
import statistics
from collections.abc import Sequence


def bootstrap_means(values: Sequence[float], n_resamples: int, rng: random.Random) -> list[float]:
    """Return the means of ``n_resamples`` bootstrap resamples of ``values``.

    Seeding is the caller's responsibility: pass ``random.Random(seed)`` for a
    reproducible result. The function draws only from ``rng``.
    """
    if not values:
        raise ValueError("cannot resample an empty series")
    k = len(values)
    return [statistics.fmean(rng.choices(values, k=k)) for _ in range(n_resamples)]


def permutation_pvalue(a: Sequence[float], b: Sequence[float], n_permutations: int = 10_000) -> float:
    """Two-sided permutation p-value for a difference in means between two samples.

    Returns:
        (count + 1) / (n_permutations + 1), where count is the number of label
        permutations whose absolute difference in means is at least the observed one.
    """
    if not a or not b:
        raise ValueError("both samples must be non-empty")
    observed = abs(statistics.fmean(a) - statistics.fmean(b))
    pooled = [*a, *b]
    count = 0
    for _ in range(n_permutations):
        random.shuffle(pooled)
        diff = abs(statistics.fmean(pooled[: len(a)]) - statistics.fmean(pooled[len(a) :]))
        if diff >= observed:
            count += 1
    return (count + 1) / (n_permutations + 1)
'''

# ---------------------------------------------------------------------------
# src/sci/analysis/summary.ts
# ---------------------------------------------------------------------------

SUMMARY_TS = """\
/**
 * Descriptive summaries of sensor time series.
 */

/** Summary of one series. */
export interface SeriesSummary {
  median: number;
  peakTime: number;
  peakValue: number;
  validFraction: number;
}

/**
 * Fraction of readings that passed quality control.
 *
 * @param flags - quality-control flags, 1 for a valid reading and 0 otherwise; at least one
 */
export function validFraction(flags: readonly number[]): number {
  if (flags.length === 0) throw new RangeError("no flags given");
  return flags.filter((f) => f === 1).length / flags.length;
}

/**
 * Median of a series.
 *
 * @param values - the series, at least one value
 */
export function median(values: number[]): number {
  if (values.length === 0) throw new RangeError("median of an empty series");
  const sorted = values.sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 === 1 ? sorted[mid] : 0.5 * (sorted[mid - 1] + sorted[mid]);
}

/**
 * Summarise a series sampled at the given times.
 *
 * @param times - sample times, in s
 * @param values - sample values, one per time
 * @param flags - quality-control flags, one per sample
 */
export function summarise(times: readonly number[], values: number[], flags: readonly number[]): SeriesSummary {
  if (times.length !== values.length || flags.length !== values.length) {
    throw new RangeError("times, values and flags must have the same length");
  }
  const med = median(values);
  let peak = 0;
  for (let i = 1; i < values.length; i++) {
    if (values[i] > values[peak]) peak = i;
  }
  return { median: med, peakTime: times[peak], peakValue: values[peak], validFraction: validFraction(flags) };
}
"""

# ---------------------------------------------------------------------------
# src/sci/analysis/emissions.ts
# ---------------------------------------------------------------------------

EMISSIONS_TS = """\
/**
 * Grid emission factors for operational carbon accounting.
 */

/** Average grid emission factors, in g CO2e/kWh, by reference year and region. */
const FACTORS: Record<number, Record<string, number>> = {
  2020: { QC: 1.7, ON: 30.0, AB: 590.0 },
  2030: { QC: 1.2, ON: 18.0, AB: 310.0 },
};

let referenceYear = 2020;
const cache = new Map<string, number>();

/**
 * Select the reference year whose grid factors subsequent calls use.
 *
 * @param year - a year present in the factor table
 */
export function setReferenceYear(year: number): void {
  if (!(year in FACTORS)) throw new RangeError(`no grid factors for ${year}`);
  referenceYear = year;
}

/**
 * Grid emission factor of a region in the reference year, in g CO2e/kWh.
 *
 * @param region - province code, for example "QC"
 */
export function emissionFactor(region: string): number {
  const hit = cache.get(region);
  if (hit !== undefined) return hit;
  const factor = FACTORS[referenceYear][region];
  if (factor === undefined) throw new RangeError(`unknown region ${region}`);
  cache.set(region, factor);
  return factor;
}

/**
 * Operational emissions of an electricity use, in kg CO2e.
 *
 * @param region - province code
 * @param energyKWh - electricity used, in kWh
 */
export function operationalEmissions(region: string, energyKWh: number): number {
  return (emissionFactor(region) * energyKWh) / 1000;
}
"""

# ---------------------------------------------------------------------------
# src/sci/core/extrapolate.py (defect exposed by the theorist: error order)
# ---------------------------------------------------------------------------

EXTRAPOLATE = """\
\"\"\"Richardson extrapolation of finite-difference derivatives.\"\"\"

from __future__ import annotations

from collections.abc import Callable


def forward_difference(f: Callable[[float], float], x: float, h: float) -> float:
    \"\"\"One-sided difference quotient (f(x + h) - f(x)) / h.\"\"\"
    return (f(x + h) - f(x)) / h


def refined_derivative(f: Callable[[float], float], x: float, h: float) -> float:
    \"\"\"Return the derivative of f at x, refined by one Richardson step.

    The forward difference is evaluated at steps h and h / 2, and the two
    estimates are combined to cancel the leading term of the truncation error.
    \"\"\"
    coarse = forward_difference(f, x, h)
    fine = forward_difference(f, x, h / 2)
    return (4.0 * fine - coarse) / 3.0
"""

# ---------------------------------------------------------------------------
# src/sci/core/sensor.py (defect exposed by the experimentalist: lag correction)
# ---------------------------------------------------------------------------

SENSOR = """\
\"\"\"Dynamic correction of first-order temperature sensors.\"\"\"

from __future__ import annotations

from collections.abc import Sequence


def lag_corrected(readings: Sequence[float], dt: float, tau: float) -> list[float]:
    \"\"\"Recover the air temperature from a first-order sensor's readings.

    A sensor with time constant tau obeys tau * dT_s/dt = T_air - T_s. The
    rate of change is estimated by central differences, and by one-sided
    differences at the two ends.

    Args:
        readings: Sensor temperatures at a fixed interval, in degC.
        dt: Sampling interval, in s.
        tau: Time constant of the sensor, in s.
    \"\"\"
    n = len(readings)
    if n < 2:
        raise ValueError("at least two readings are needed")
    corrected = []
    for i in range(n):
        if i == 0:
            rate = (readings[1] - readings[0]) / dt
        elif i == n - 1:
            rate = (readings[-1] - readings[-2]) / dt
        else:
            rate = (readings[i + 1] - readings[i - 1]) / (2 * dt)
        corrected.append(readings[i] - tau * rate)
    return corrected
"""

# ---------------------------------------------------------------------------
# src/sci/core/rates.ts (defect exposed by the numerical analyst: log(1 + x))
# ---------------------------------------------------------------------------

RATES_TS = """\
/**
 * Continuous growth rates of slowly drifting quantities, such as clock offsets
 * and oscillator frequencies.
 */

/**
 * Continuous rate r such that exp(r * dt) = 1 + fractionalChange.
 *
 * @param fractionalChange - (next - previous) / previous, dimensionless
 * @param dt - interval, in s
 * @returns the rate, in 1/s
 */
export function continuousRate(fractionalChange: number, dt: number): number {
  if (dt <= 0) throw new RangeError("dt must be positive");
  return Math.log(1 + fractionalChange) / dt;
}
"""

# ---------------------------------------------------------------------------
# src/sci/analysis/intervals.py (defect exposed by the methodologist: z for small n)
# ---------------------------------------------------------------------------

INTERVALS = """\
\"\"\"Confidence intervals for replicate measurements.\"\"\"

from __future__ import annotations

import math
import statistics
from collections.abc import Sequence

Z_95 = 1.959963984540054


def mean_interval(replicates: Sequence[float]) -> tuple[float, float]:
    \"\"\"Return the two-sided 95% confidence interval of the mean.

    Replicates are independent measurements of one quantity with normally
    distributed error of unknown variance; a run has three to ten replicates.
    \"\"\"
    n = len(replicates)
    if n < 2:
        raise ValueError("at least two replicates are needed")
    mean = statistics.fmean(replicates)
    half = Z_95 * statistics.stdev(replicates) / math.sqrt(n)
    return mean - half, mean + half
"""

# ---------------------------------------------------------------------------
# src/sci/analysis/rank.ts (defect exposed by the computer scientist: default sort)
# ---------------------------------------------------------------------------

RANK_TS = """\
/**
 * Empirical percentiles of sensor readings.
 */

/**
 * The p-th percentile by linear interpolation between closest ranks.
 *
 * @param readings - readings, in any order; left unchanged
 * @param p - percentile, from 0 to 100
 */
export function percentile(readings: readonly number[], p: number): number {
  if (readings.length === 0) throw new RangeError("no readings");
  if (p < 0 || p > 100) throw new RangeError("p must lie in [0, 100]");
  const sorted = [...readings].sort();
  const position = (p / 100) * (sorted.length - 1);
  const lower = Math.floor(position);
  const upper = Math.ceil(position);
  const weight = position - lower;
  return sorted[lower] * (1 - weight) + sorted[upper] * weight;
}
"""

# ---------------------------------------------------------------------------
# Branch contents
# ---------------------------------------------------------------------------

MAIN_COMMITS: tuple[Commit, ...] = (
    Commit(
        "Add sensor-analysis package with trapezoidal quadrature and rated-range rescaling",
        (
            SourceFile("README.md", README),
            SourceFile("pyproject.toml", PYPROJECT),
            SourceFile("package.json", PACKAGE_JSON),
            SourceFile("tsconfig.json", TSCONFIG),
            SourceFile(".gitignore", GITIGNORE),
            SourceFile("src/sci/__init__.py", PKG_INIT),
            SourceFile("src/sci/core/__init__.py", CORE_INIT),
            SourceFile("src/sci/analysis/__init__.py", ANALYSIS_INIT),
            SourceFile("src/sci/core/quadrature.py", QUADRATURE_MAIN),
            SourceFile("src/sci/core/normalise.ts", NORMALISE_TS_MAIN),
        ),
    ),
)

FEATURE_COMMITS: tuple[Commit, ...] = (
    Commit(
        "Add Simpson quadrature, heat diffusion, streaming moments and surface heat transfer",
        (
            SourceFile("src/sci/core/quadrature.py", QUADRATURE_FEATURE),
            SourceFile("src/sci/core/numerics.py", NUMERICS),
            SourceFile("src/sci/core/heat.py", HEAT),
            SourceFile("src/sci/core/geometry.py", GEOMETRY),
            SourceFile("src/sci/core/differentiate.ts", DIFFERENTIATE_TS),
            SourceFile("src/sci/core/normalise.ts", NORMALISE_TS_FEATURE),
            SourceFile("src/sci/core/surfaceHeat.ts", SURFACE_HEAT_TS),
            SourceFile("src/sci/core/extrapolate.py", EXTRAPOLATE),
            SourceFile("src/sci/core/sensor.py", SENSOR),
            SourceFile("src/sci/core/rates.ts", RATES_TS),
        ),
    ),
    Commit(
        "Add preprocessing, parallel aggregation, resampling, series summaries and emission factors",
        (
            SourceFile("src/sci/analysis/preprocess.py", PREPROCESS),
            SourceFile("src/sci/analysis/aggregate.py", AGGREGATE),
            SourceFile("src/sci/analysis/resample.py", RESAMPLE),
            SourceFile("src/sci/analysis/summary.ts", SUMMARY_TS),
            SourceFile("src/sci/analysis/emissions.ts", EMISSIONS_TS),
            SourceFile("src/sci/analysis/intervals.py", INTERVALS),
            SourceFile("src/sci/analysis/rank.ts", RANK_TS),
        ),
    ),
)


def feature_tree() -> dict[str, str]:
    """Return the text of every file on the feature branch, by path."""
    tree: dict[str, str] = {}
    for commit in (*MAIN_COMMITS, *FEATURE_COMMITS):
        for source in commit.files:
            tree[source.path] = source.text
    return tree


# ---------------------------------------------------------------------------
# Manifest verification
# ---------------------------------------------------------------------------


def load_located(manifest_path: Path) -> list[Located]:
    """Read every anchored entry of the manifest."""
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries: list[Located] = []
    for kind in ("defects", "lookalikes", "contested"):
        for raw in data[kind]:
            line = int(raw["line"])
            entries.append(
                Located(
                    kind=kind,
                    id=raw["id"],
                    file=raw["file"],
                    line=line,
                    anchor=raw["anchor"],
                    line_end=int(raw.get("line_end", line)),
                    anchor_end=raw.get("anchor_end"),
                )
            )
    return entries


def find_unique(text: str, anchor: str) -> list[int]:
    """Return the 1-based numbers of the lines that contain ``anchor``."""
    return [number for number, line in enumerate(text.splitlines(), start=1) if anchor in line]


def verify_manifest(manifest_path: Path) -> list[str]:
    """Check anchors, recorded lines and separation; return the list of problems."""
    tree = feature_tree()
    problems: list[str] = []
    entries = load_located(manifest_path)
    for entry in entries:
        text = tree.get(entry.file)
        if text is None:
            problems.append(f"{entry.id}: file {entry.file} is not written by build.py")
            continue
        hits = find_unique(text, entry.anchor)
        if len(hits) != 1:
            problems.append(f"{entry.id}: anchor {entry.anchor!r} occurs on {len(hits)} lines of {entry.file}")
        elif hits[0] != entry.line:
            problems.append(f"{entry.id}: anchor is on line {hits[0]}, manifest records {entry.line}")
        if entry.anchor_end is not None:
            end_hits = find_unique(text, entry.anchor_end)
            if len(end_hits) != 1:
                problems.append(f"{entry.id}: anchor_end {entry.anchor_end!r} occurs on {len(end_hits)} lines")
            elif end_hits[0] != entry.line_end:
                problems.append(f"{entry.id}: anchor_end is on line {end_hits[0]}, manifest records {entry.line_end}")
        if entry.line_end < entry.line:
            problems.append(f"{entry.id}: line_end precedes line")
    defects = [e for e in entries if e.kind == "defects"]
    others = [e for e in entries if e.kind != "defects"]
    for other in others:
        for defect in defects:
            if defect.file != other.file:
                continue
            if other.line - MIN_SEPARATION < defect.line < other.line_end + MIN_SEPARATION:
                problems.append(f"{other.id} lies within {MIN_SEPARATION} lines of defect {defect.id}")
    for i, first in enumerate(defects):
        for second in defects[i + 1 :]:
            if first.file == second.file and abs(first.line - second.line) < MIN_SEPARATION:
                problems.append(f"defects {first.id} and {second.id} lie within {MIN_SEPARATION} lines")
    return problems


# ---------------------------------------------------------------------------
# Repository creation
# ---------------------------------------------------------------------------


def git(repo: Path, *args: str, date: str = COMMIT_DATES[0]) -> None:
    """Run a git command in ``repo`` with a fixed identity and fixed dates."""
    env = {**os.environ, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
    subprocess.run(["git", *GIT_IDENTITY, *args], cwd=repo, check=True, env=env, stdout=subprocess.DEVNULL)


def write_commit(repo: Path, commit: Commit, date: str) -> None:
    """Write the files of ``commit`` and commit them."""
    for source in commit.files:
        target = repo / source.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source.text, encoding="utf-8")
        git(repo, "add", "--", source.path)
    git(repo, "commit", "--quiet", "--no-verify", "-m", commit.message, date=date)


def build(out: Path) -> None:
    """Create the fixture repository at ``out``."""
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise SystemExit(f"error: {out} exists and is not an empty directory")
    out.mkdir(parents=True, exist_ok=True)
    git(out, "init", "--quiet", "--template=", "--initial-branch=main")
    commits = (*MAIN_COMMITS, *FEATURE_COMMITS)
    if len(commits) > len(COMMIT_DATES):
        raise SystemExit("error: add a date to COMMIT_DATES for every commit")
    for index, commit in enumerate(commits):
        if index == len(MAIN_COMMITS):
            git(out, "checkout", "--quiet", "-b", "feature")
        write_commit(out, commit, COMMIT_DATES[index])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--out", type=Path, help="directory in which to create the repository")
    group.add_argument("--check", action="store_true", help="verify manifest.json only; create nothing")
    parser.add_argument("--manifest", type=Path, default=MANIFEST, help="manifest to verify (default: beside build.py)")
    args = parser.parse_args(argv)
    problems = verify_manifest(args.manifest)
    if problems:
        for problem in problems:
            print(f"manifest: {problem}", file=sys.stderr)
        return 1
    if args.check:
        print(f"manifest: {len(load_located(args.manifest))} entries verified against the feature sources")
        return 0
    build(args.out.resolve())
    print(f"built {args.out} (branches main and feature; feature checked out)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
