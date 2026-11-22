"""Build the hard fixture repository used to measure sci-review.

Usage:
    python3 build.py --out DIR     create the git repository at DIR
    python3 build.py --check       verify manifest.json against the embedded sources only

The repository has two branches. ``main`` holds the package skeleton: unit
conventions, forcing records, the tridiagonal solver and the dashboard record
types. ``feature`` adds the modelling, statistics and dashboard modules, in
Python under ``src/limno/`` and in TypeScript under ``src/limno/web/``, with
the seeded defects, the correct look-alike constructs and the contested
constructs listed in ``manifest.json``. The repository is left checked out on
``feature`` and has no remote, so ``panel.py scope --mode branch`` resolves
``main`` as the base.

The sources carry no marker of any kind. ``manifest.json`` locates each entry
by ``anchor``, a substring that occurs exactly once in the feature version of
the file, and records the 1-based line of that occurrence in ``line``. Every
build first verifies that each anchor is unique, that each recorded line
matches, and that look-alikes and contested constructs lie far enough from
every seeded defect that a single finding cannot match both. The manifest and
the reproduction checks under ``checks/`` stay beside this script and are
never written into the generated repository.

Only the Python standard library is used, here and in the generated Python
code; the generated TypeScript has no dependencies.
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
# defect line in the same file, and between two seeded defects: twice the
# tolerance plus one, so that no finding range can match both.
MIN_SEPARATION = 2 * MATCH_TOLERANCE + 1

GIT_IDENTITY = ("-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false")
COMMIT_DATES = (
    "2026-02-02T09:00:00+00:00",
    "2026-02-09T15:20:00+00:00",
    "2026-02-11T10:05:00+00:00",
    "2026-02-16T13:40:00+00:00",
    "2026-02-18T08:30:00+00:00",
)


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
# Sources
# ---------------------------------------------------------------------------

README_MD_MAIN = """\
# limno

A small one-dimensional lake model and the analysis routines around it:
surface energy balance, vertical heat transport, a plankton model, and the
statistics used to calibrate the model against buoy observations. The
TypeScript modules under `src/limno/web/` feed the monitoring dashboard.

## Conventions

The conventions of `src/limno/units.py` hold for the Python code and those of
`src/limno/web/types.ts` for the TypeScript code. Read them before adding a
module; the two sides do not use the same units everywhere.
"""


PYPROJECT_TOML = """\
[project]
name = "limno"
version = "0.4.0"
description = "One-dimensional lake model and calibration tools"
requires-python = ">=3.10"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/limno"]
"""


PACKAGE_JSON = """\
{
  "name": "limno-dashboard",
  "version": "0.4.0",
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


TSCONFIG_JSON = """\
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


INIT_PY = '''\
"""One-dimensional lake model and calibration tools."""
'''


UNITS_PY = '''\
"""Physical constants and unit conventions of the lake model.

Conventions that hold throughout the Python code of ``limno``:

* Temperatures are in degrees Celsius unless a name ends in ``_k``.
* Pressures are in pascals. Vapour pressures are the one exception: they are
  in hectopascals, the unit in which :func:`saturation_vapour_pressure` and the
  humidity tables of the station network report them.
* Heat fluxes are in W m-2. Time is in seconds unless a name ends in ``_days``.
* Depth ``z`` is positive downwards from the water surface, in metres.
* Angles passed between modules are in radians; latitude and longitude given by
  a user are in degrees, north and east positive.
"""

from __future__ import annotations

import math

KELVIN_OFFSET = 273.15
STEFAN_BOLTZMANN = 5.670374419e-8  # W m-2 K-4
GRAVITY = 9.80665  # m s-2
SECONDS_PER_DAY = 86_400.0
DRY_AIR_GAS_CONSTANT = 287.05  # J kg-1 K-1
AIR_HEAT_CAPACITY = 1005.0  # J kg-1 K-1
WATER_HEAT_CAPACITY = 4186.0  # J kg-1 K-1
REFERENCE_WATER_DENSITY = 1000.0  # kg m-3
MOLAR_MASS_RATIO = 0.622  # water vapour to dry air


def celsius_to_kelvin(t: float) -> float:
    """Convert a temperature from degrees Celsius to kelvin."""
    return t + KELVIN_OFFSET


def kelvin_to_celsius(t_k: float) -> float:
    """Convert a temperature from kelvin to degrees Celsius."""
    return t_k - KELVIN_OFFSET


def saturation_vapour_pressure(t: float) -> float:
    """Saturation vapour pressure over liquid water, in hPa.

    Magnus form with the coefficients of Alduchov and Eskridge (1996), accurate
    to 0.4 % between -40 and 50 degrees Celsius.

    Args:
        t: Temperature in degrees Celsius.
    """
    return 6.1094 * math.exp(17.625 * t / (t + 243.04))


def days_to_seconds(days: float) -> float:
    """Convert a duration from days to seconds."""
    return days * SECONDS_PER_DAY
'''


FORCING_PY = '''\
"""Meteorological forcing of the lake model.

One :class:`Forcing` record holds the weather above the lake for one model
step, in the units of :mod:`limno.units`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Forcing:
    """Weather above the lake surface for one model step.

    Attributes:
        air_temperature: Air temperature at screen height, degrees Celsius.
        relative_humidity: Relative humidity as a fraction in [0, 1].
        pressure: Air pressure at the surface, Pa.
        wind_speed: Wind speed, m s-1, measured at ``wind_height``.
        wind_height: Height of the anemometer above the water, m. Shore
            stations measure at 10 m; the buoys of the network at 2 m.
        shortwave: Incoming shortwave radiation, W m-2.
        longwave: Incoming longwave radiation, W m-2.
    """

    air_temperature: float
    relative_humidity: float
    pressure: float
    wind_speed: float
    wind_height: float = 10.0
    shortwave: float = 0.0
    longwave: float = 300.0
'''


TRIDIAG_PY = '''\
"""Solution of tridiagonal linear systems."""

from __future__ import annotations

from collections.abc import MutableSequence, Sequence


def solve_tridiagonal(
    lower: Sequence[float],
    diag: MutableSequence[float],
    upper: Sequence[float],
    rhs: MutableSequence[float],
) -> list[float]:
    """Solve a tridiagonal system with the Thomas algorithm.

    Row ``i`` reads ``lower[i] * x[i - 1] + diag[i] * x[i] + upper[i] * x[i + 1]
    = rhs[i]``; ``lower[0]`` and ``upper[-1]`` are ignored. The algorithm does
    not pivot, so the matrix must be diagonally dominant.

    To avoid allocating in the inner loop of the model, the forward sweep
    works in place: ``diag`` and ``rhs`` are overwritten with the eliminated
    diagonal and right-hand side. Pass copies if the caller still needs them.

    Returns:
        The solution vector.
    """
    n = len(diag)
    if not (len(lower) == len(upper) == len(rhs) == n):
        raise ValueError("all four sequences must have the same length")
    for i in range(1, n):
        w = lower[i] / diag[i - 1]
        diag[i] -= w * upper[i - 1]
        rhs[i] -= w * rhs[i - 1]
    x = [0.0] * n
    x[n - 1] = rhs[n - 1] / diag[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = (rhs[i] - upper[i] * x[i + 1]) / diag[i]
    return x
'''


WEB_TYPES_TS = """\
/**
 * Shared record types of the dashboard.
 *
 * Unit conventions on the dashboard side differ from the Python model in two
 * places, because the records arrive straight from the logger export:
 *
 * - Water temperatures in a {@link Profile} are absolute temperatures in
 *   kelvin, as the logger stores them. Convert with `toCelsius` from
 *   `convert.ts` before using any empirical formula written for Celsius.
 * - Barometric pressure in a {@link MetSample} is in hPa, as reported by the
 *   weather station; transducer pressures in a {@link DepthSample} are
 *   absolute pressures in Pa.
 *
 * Times are milliseconds since the Unix epoch, UTC. Depths are in metres,
 * positive downwards, and listed in increasing order.
 */

export interface Profile {
  /** Sampling time, ms since the epoch (UTC). */
  time: number;
  /** Sensor depths, m, strictly increasing. */
  depths: number[];
  /** Water temperature at each depth, K. */
  temperatures: number[];
  /** Salinity at each depth, g/kg; zero for fresh water. */
  salinities: number[];
}

export interface MetSample {
  time: number;
  /** Barometric pressure, hPa. */
  pressure: number;
  airTemperature: number;
  windSpeed: number;
}

export interface DepthSample {
  time: number;
  /** Absolute pressure at the transducer, Pa. */
  pressure: number;
}

export interface Hypsography {
  /** Depths, m, strictly increasing from 0 at the surface. */
  depths: number[];
  /** Horizontal lake area at each depth, m^2. */
  areas: number[];
}

export interface Sample {
  time: number;
  value: number;
}
"""


RADIATION_PY = '''\
"""Solar geometry and clear-sky shortwave radiation at the lake surface.

Times are UTC. Sites are given by latitude and longitude in degrees, north and
east positive (see :mod:`limno.units`). The formulae are those of the
network's radiation notes and are accurate to about one minute of time and
0.1 degree of angle, well inside the uncertainty of the pyranometers.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

SOLAR_CONSTANT = 1361.0  # W m-2
CLEAR_SKY_TRANSMISSIVITY = 0.75
MAXIMUM_DECLINATION = math.radians(23.45)


@dataclass(frozen=True)
class Site:
    """A lake site.

    Attributes:
        latitude: Degrees north, from -75 to 75.
        longitude: Degrees east, from -180 to 180.
        elevation: Height of the lake surface above sea level, m.
    """

    latitude: float
    longitude: float
    elevation: float = 0.0


def solar_declination(day_of_year: int) -> float:
    """Solar declination, radians, after Cooper (1969).

    Cooper's formula reads delta = 23.45 deg * sin(2 pi (284 + n) / 365) for
    day number n, January 1 being day 1.
    """
    return MAXIMUM_DECLINATION * math.sin(2.0 * math.pi * (day_of_year - 81) / 365.0)


def equation_of_time(day_of_year: int) -> float:
    """Equation of time, minutes, after Spencer (1971).

    Positive when the apparent sun is ahead of the mean sun.
    """
    b = 2.0 * math.pi * (day_of_year - 1) / 365.0
    return 229.18 * (
        0.000075
        + 0.001868 * math.cos(b)
        - 0.032077 * math.sin(b)
        - 0.014615 * math.cos(2.0 * b)
        - 0.040849 * math.sin(2.0 * b)
    )


def solar_time(utc_hours: float, longitude: float, day_of_year: int) -> float:
    """Apparent solar time, hours, at a site of the given longitude.

    Args:
        utc_hours: Time of day, hours UTC.
        longitude: Degrees east.
        day_of_year: Day number, January 1 being day 1.
    """
    return utc_hours - longitude / 15.0 + equation_of_time(day_of_year) / 60.0


def hour_angle(utc_hours: float, longitude: float, day_of_year: int) -> float:
    """Hour angle of the sun, radians, zero at solar noon and negative before it."""
    return math.radians(15.0 * (solar_time(utc_hours, longitude, day_of_year) - 12.0))


def cos_zenith(site: Site, day_of_year: int, utc_hours: float) -> float:
    """Cosine of the solar zenith angle; negative when the sun is below the horizon."""
    lat = math.radians(site.latitude)
    decl = solar_declination(day_of_year)
    h = hour_angle(utc_hours, site.longitude, day_of_year)
    return math.sin(lat) * math.sin(decl) + math.cos(lat) * math.cos(decl) * math.cos(h)


def day_length(site: Site, day_of_year: int) -> float:
    """Time between sunrise and sunset, hours.

    The sunset hour angle w0 solves cos w0 = -tan(lat) tan(decl); the sun moves
    by 15 degrees of hour angle per hour. Beyond the polar circles the cosine
    is clamped, giving 24 hours of polar day or 0 hours of polar night.
    """
    lat = math.radians(site.latitude)
    x = -math.tan(lat) * math.tan(solar_declination(day_of_year))
    w0 = math.acos(min(1.0, max(-1.0, x)))
    return math.degrees(w0) / 15.0


def extraterrestrial_irradiance(day_of_year: int) -> float:
    """Irradiance at the top of the atmosphere on a surface normal to the sun, W m-2."""
    return SOLAR_CONSTANT * (1.0 + 0.033 * math.cos(2.0 * math.pi * day_of_year / 365.0))


def clear_sky_shortwave(site: Site, day_of_year: int, utc_hours: float) -> float:
    """Clear-sky shortwave irradiance on the horizontal lake surface, W m-2.

    A single broadband transmissivity, raised to the relative air mass and
    corrected for the site elevation, attenuates the direct beam.
    """
    mu = cos_zenith(site, day_of_year, utc_hours)
    if mu <= 0.0:
        return 0.0
    pressure_ratio = math.exp(-site.elevation / 8434.5)
    air_mass = pressure_ratio / mu
    return extraterrestrial_irradiance(day_of_year) * mu * CLEAR_SKY_TRANSMISSIVITY**air_mass


def daily_mean_shortwave(site: Site, day_of_year: int, steps: int = 96) -> float:
    """Clear-sky shortwave irradiance averaged over the UTC day, W m-2."""
    total = 0.0
    for k in range(steps):
        total += clear_sky_shortwave(site, day_of_year, 24.0 * (k + 0.5) / steps)
    return total / steps
'''


FLUXES_PY = '''\
"""Surface energy balance of the lake.

Every flux returned by this module is in W m-2 and is positive when it carries
heat into the water, so that the net flux is the plain sum of the components:

    net = shortwave + longwave + sensible + latent

Bulk aerodynamic formulae give the turbulent fluxes. Their transfer
coefficients are the open-water values recommended for lakes of a few square
kilometres by the network's modelling guidelines.
"""

from __future__ import annotations

from dataclasses import dataclass

from limno.forcing import Forcing
from limno.units import (
    AIR_HEAT_CAPACITY,
    DRY_AIR_GAS_CONSTANT,
    MOLAR_MASS_RATIO,
    STEFAN_BOLTZMANN,
    celsius_to_kelvin,
    saturation_vapour_pressure,
)

WATER_ALBEDO = 0.07
WATER_EMISSIVITY = 0.97
TRANSFER_COEFFICIENT_HEAT = 1.3e-3
TRANSFER_COEFFICIENT_VAPOUR = 1.3e-3
MINIMUM_WIND = 0.5  # m s-1; free convection keeps some exchange in calm air


@dataclass(frozen=True)
class SurfaceFluxes:
    """Components of the surface heat budget, W m-2, positive into the water."""

    shortwave: float
    longwave: float
    sensible: float
    latent: float

    @property
    def net(self) -> float:
        """Net heat flux into the water."""
        return self.shortwave + self.longwave + self.sensible + self.latent


def latent_heat_of_vaporisation(t: float) -> float:
    """Latent heat of vaporisation of water, J kg-1, at ``t`` degrees Celsius.

    Linear fit to the tabulated values between 0 and 40 degrees Celsius.
    """
    return 2.501e6 - 2361.0 * t


def specific_humidity(vapour_pressure: float, pressure: float) -> float:
    """Specific humidity, kg kg-1.

    Args:
        vapour_pressure: Partial pressure of water vapour.
        pressure: Total air pressure, in the same unit as ``vapour_pressure``.
    """
    return MOLAR_MASS_RATIO * vapour_pressure / (pressure - (1.0 - MOLAR_MASS_RATIO) * vapour_pressure)


def air_density(forcing: Forcing) -> float:
    """Density of the air above the lake, kg m-3, from the ideal gas law."""
    return forcing.pressure / (DRY_AIR_GAS_CONSTANT * celsius_to_kelvin(forcing.air_temperature))


def effective_wind(forcing: Forcing) -> float:
    """Wind speed used in the bulk formulae, m s-1, never below ``MINIMUM_WIND``."""
    return max(forcing.wind_speed, MINIMUM_WIND)


def surface_humidities(t_surface: float, forcing: Forcing) -> tuple[float, float]:
    """Specific humidity at the water surface and in the air, kg kg-1.

    The air in contact with the water is saturated at the surface temperature.
    """
    p_air = forcing.pressure
    q_surface = specific_humidity(saturation_vapour_pressure(t_surface), p_air)
    e_air = forcing.relative_humidity * saturation_vapour_pressure(forcing.air_temperature)
    q_air = specific_humidity(e_air, p_air)
    return q_surface, q_air


def shortwave_flux(forcing: Forcing) -> float:
    """Absorbed shortwave radiation, W m-2."""
    return (1.0 - WATER_ALBEDO) * forcing.shortwave


def longwave_flux(t_surface: float, forcing: Forcing) -> float:
    """Net longwave radiation, W m-2: absorbed incoming minus emitted."""
    emitted = WATER_EMISSIVITY * STEFAN_BOLTZMANN * celsius_to_kelvin(t_surface) ** 4
    return WATER_EMISSIVITY * forcing.longwave - emitted


def sensible_heat_flux(t_surface: float, forcing: Forcing) -> float:
    """Sensible heat flux, W m-2, positive when the air is warmer than the water."""
    rho = air_density(forcing)
    wind = effective_wind(forcing)
    return rho * AIR_HEAT_CAPACITY * TRANSFER_COEFFICIENT_HEAT * wind * (forcing.air_temperature - t_surface)


def evaporation_rate(t_surface: float, forcing: Forcing) -> float:
    """Evaporation, kg m-2 s-1; negative values are condensation onto the lake."""
    q_surface, q_air = surface_humidities(t_surface, forcing)
    rho = air_density(forcing)
    return rho * TRANSFER_COEFFICIENT_VAPOUR * effective_wind(forcing) * (q_surface - q_air)


def latent_heat_flux(t_surface: float, forcing: Forcing) -> float:
    """Latent heat flux, W m-2, in the sign convention of the module."""
    evaporation = evaporation_rate(t_surface, forcing)
    return latent_heat_of_vaporisation(t_surface) * evaporation


def surface_fluxes(t_surface: float, forcing: Forcing) -> SurfaceFluxes:
    """All components of the surface heat budget for one model step.

    Args:
        t_surface: Temperature of the uppermost model layer, degrees Celsius.
        forcing: Weather above the lake.
    """
    return SurfaceFluxes(
        shortwave=shortwave_flux(forcing),
        longwave=longwave_flux(t_surface, forcing),
        sensible=sensible_heat_flux(t_surface, forcing),
        latent=latent_heat_flux(t_surface, forcing),
    )
'''


COLUMN_PY = '''\
"""Vertical heat transport in a one-dimensional lake column.

The column is a stack of horizontal layers, numbered from the surface down.
Layer thicknesses may vary; the standard grids refine towards the surface,
where the gradients are largest, for example ten layers of 0.1 m above layers
of 1 m. Each layer holds one temperature (degrees Celsius), and turbulent
diffusion with an eddy diffusivity defined on the interfaces between layers
carries heat between neighbours. The surface heat flux of
:mod:`limno.fluxes` enters the top layer; no heat crosses the lake bed.

Two time-stepping schemes are offered. The explicit scheme is cheap per step
but conditionally stable; :meth:`LakeColumn.max_stable_step` gives its
largest admissible step. The implicit (backward Euler) scheme is
unconditionally stable and is the default for seasonal runs.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

from limno.tridiag import solve_tridiagonal
from limno.units import REFERENCE_WATER_DENSITY, WATER_HEAT_CAPACITY

VOLUMETRIC_HEAT_CAPACITY = REFERENCE_WATER_DENSITY * WATER_HEAT_CAPACITY  # J m-3 K-1


@dataclass
class LakeColumn:
    """State and geometry of the lake column.

    Attributes:
        thicknesses: Layer thicknesses, m, from the surface down.
        diffusivities: Eddy diffusivity at each of the ``len(thicknesses) - 1``
            interfaces, m2 s-1. Wind mixing raises the values near the surface
            to 1e-4 m2 s-1 and above; the hypolimnion is close to the molecular
            value of 1.4e-7 m2 s-1.
        temperatures: Layer temperatures, degrees Celsius.
    """

    thicknesses: list[float]
    diffusivities: list[float]
    temperatures: list[float]
    time: float = field(default=0.0)

    def __post_init__(self) -> None:
        n = len(self.thicknesses)
        if n < 2:
            raise ValueError("the column needs at least two layers")
        if len(self.temperatures) != n or len(self.diffusivities) != n - 1:
            raise ValueError("temperatures need one value per layer and diffusivities one per interface")
        if min(self.thicknesses) <= 0.0:
            raise ValueError("layer thicknesses must be positive")

    @property
    def depth(self) -> float:
        """Total depth of the column, m."""
        return sum(self.thicknesses)

    def layer_centres(self) -> list[float]:
        """Depth of the centre of every layer, m."""
        centres = []
        top = 0.0
        for h in self.thicknesses:
            centres.append(top + 0.5 * h)
            top += h
        return centres

    def heat_content(self) -> float:
        """Heat content per unit area relative to 0 degrees Celsius, J m-2."""
        return VOLUMETRIC_HEAT_CAPACITY * sum(t * h for t, h in zip(self.temperatures, self.thicknesses))

    def exchange_coefficients(self, dt: float) -> tuple[list[float], list[float]]:
        """Dimensionless exchange coefficients of every layer with its neighbours.

        For layer i, ``above[i]`` multiplies T[i - 1] - T[i] and ``below[i]``
        multiplies T[i + 1] - T[i] in the update of T[i] over a step of ``dt``
        seconds. The distance between the centres of layers i and i + 1 is
        (h[i] + h[i + 1]) / 2. The surface layer has no neighbour above and the
        bottom layer none below, so their missing coefficient is zero.
        """
        h = self.thicknesses
        n = len(h)
        above = [0.0] * n
        below = [0.0] * n
        for i, kappa in enumerate(self.diffusivities):
            conductance = kappa / (0.5 * (h[i] + h[i + 1]))
            below[i] = dt * conductance / h[i]
            above[i + 1] = dt * conductance / h[i + 1]
        return above, below

    def max_stable_step(self) -> float:
        """Largest time step, s, for which the explicit scheme is stable.

        The explicit update keeps every new temperature a convex combination
        of old ones, which bounds it by the old extremes, when the exchange
        coefficients of each layer sum to at most one. For a layer of
        thickness h between interfaces of diffusivity kappa this gives
        dt <= h^2 / (2 kappa).
        """
        h = sum(self.thicknesses) / len(self.thicknesses)
        return 0.5 * h * h / max(self.diffusivities)

    def explicit_step(self, dt: float, surface_flux: float = 0.0) -> None:
        """Advance the column by ``dt`` seconds with the explicit scheme.

        Args:
            dt: Time step, s, at most :meth:`max_stable_step`.
            surface_flux: Net heat flux into the lake surface, W m-2.
        """
        if dt > self.max_stable_step():
            raise ValueError(f"time step {dt} s exceeds the explicit stability limit")
        above, below = self.exchange_coefficients(dt)
        t = self.temperatures
        n = len(t)
        new = list(t)
        for i in range(n):
            if i > 0:
                new[i] += above[i] * (t[i - 1] - t[i])
            if i < n - 1:
                new[i] += below[i] * (t[i + 1] - t[i])
        new[0] += dt * surface_flux / (VOLUMETRIC_HEAT_CAPACITY * self.thicknesses[0])
        self.temperatures = new
        self.time += dt

    def implicit_matrix(self, dt: float) -> tuple[list[float], list[float], list[float]]:
        """Lower, main and upper diagonals of the backward Euler system.

        Row i reads -above[i] T'[i - 1] + (1 + above[i] + below[i]) T'[i]
        - below[i] T'[i + 1] = T[i] + sources. In the surface and bottom rows
        one coefficient is zero, so their diagonal holds a single exchange
        term; this is the no-flux condition, not a truncated stencil. The
        matrix is strictly diagonally dominant, so the Thomas algorithm needs
        no pivoting.
        """
        above, below = self.exchange_coefficients(dt)
        n = len(above)
        lower = [-a for a in above]
        upper = [-b for b in below]
        diag = [1.0 + above[i] + below[i] for i in range(n)]
        diag[0] = 1.0 + below[0]
        diag[n - 1] = 1.0 + above[n - 1]
        return lower, diag, upper

    def run_implicit(self, dt: float, surface_fluxes: Iterable[float]) -> list[list[float]]:
        """Advance the column with backward Euler steps of ``dt`` seconds.

        Args:
            dt: Time step, s; any positive value is stable.
            surface_fluxes: Net heat flux into the surface for each step, W m-2.

        Returns:
            The temperature profile after each step.
        """
        lower, diag, upper = self.implicit_matrix(dt)
        top_capacity = VOLUMETRIC_HEAT_CAPACITY * self.thicknesses[0]
        profiles = []
        for flux in surface_fluxes:
            rhs = list(self.temperatures)
            rhs[0] += dt * flux / top_capacity
            self.temperatures = solve_tridiagonal(lower, diag, upper, rhs)
            self.time += dt
            profiles.append(list(self.temperatures))
        return profiles

    def run_explicit(self, duration: float, surface_flux: float = 0.0) -> None:
        """Advance the column by ``duration`` seconds with the largest stable explicit steps."""
        dt = self.max_stable_step()
        remaining = duration
        while remaining > 0.0:
            step = min(dt, remaining)
            self.explicit_step(step, surface_flux)
            remaining -= step


def uniform_column(depth: float, layers: int, diffusivity: float, temperature: float) -> LakeColumn:
    """A column of equal layers with uniform diffusivity and temperature."""
    h = depth / layers
    return LakeColumn([h] * layers, [diffusivity] * (layers - 1), [temperature] * layers)


def mixed_layer_depth(column: LakeColumn, threshold: float = 0.2) -> float:
    """Depth, m, of the first layer centre colder than the surface by more than ``threshold`` K."""
    surface = column.temperatures[0]
    for centre, t in zip(column.layer_centres(), column.temperatures):
        if surface - t > threshold:
            return centre
    return column.depth


def profile_at(column: LakeColumn, depths: Sequence[float]) -> list[float]:
    """Temperature of the layer containing each requested depth, degrees Celsius."""
    result = []
    for z in depths:
        top = 0.0
        value = column.temperatures[-1]
        for h, t in zip(column.thicknesses, column.temperatures):
            if z < top + h:
                value = t
                break
            top += h
        result.append(value)
    return result
'''


ECOLOGY_PY = '''\
"""Nutrient-phytoplankton-zooplankton-detritus (NPZD) model of the mixed layer.

All four pools are in mmol N m-3, so that the model conserves total nitrogen:
the four derivatives returned by :func:`npzd_rates` sum to zero for any state.
Rates are per day and time is in days, the usual units of plankton models.

The phytoplankton growth rate is limited by nutrient (Monod), by light
averaged over the mixed layer, and by temperature through a Q10 factor.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class PlanktonParameters:
    """Parameters of the NPZD model; rates per day, concentrations mmol N m-3.

    Attributes:
        max_growth: Maximum phytoplankton growth rate at 20 degrees Celsius.
        nutrient_half_saturation: Monod constant of nutrient uptake.
        light_half_saturation: Irradiance at which light limitation is 0.5, W m-2.
        attenuation: Light attenuation coefficient of the water, m-1.
        q10: Increase of the growth rate per 10 degrees Celsius.
        max_grazing: Maximum zooplankton grazing rate.
        grazing_half_saturation: Phytoplankton concentration of half-maximal grazing.
        assimilation: Fraction of grazed nitrogen assimilated by zooplankton.
        phyto_mortality: Phytoplankton mortality, per day per (mmol N m-3);
            quadratic mortality closes the model without an explicit predator.
        zoo_mortality: Zooplankton mortality, per day.
        excretion: Zooplankton excretion of ammonium, per day.
        remineralisation: Detritus remineralisation, per day.
    """

    max_growth: float = 1.4
    nutrient_half_saturation: float = 0.5
    light_half_saturation: float = 40.0
    attenuation: float = 0.3
    q10: float = 1.88
    max_grazing: float = 1.0
    grazing_half_saturation: float = 1.0
    assimilation: float = 0.7
    phyto_mortality: float = 0.05
    zoo_mortality: float = 0.08
    excretion: float = 0.03
    remineralisation: float = 0.1


def temperature_factor(t: float, q10: float) -> float:
    """Q10 temperature factor relative to 20 degrees Celsius."""
    return q10 ** ((t - 20.0) / 10.0)


def mean_light_limitation(surface_light: float, half_saturation: float, attenuation: float, depth: float) -> float:
    """Monod light limitation I / (I + K) averaged over a mixed layer of depth ``depth``.

    The irradiance decays as I(z) = I0 exp(-k z). Substituting u = I(z) turns
    the depth average into a closed form, so no quadrature is needed.

    Args:
        surface_light: Irradiance just below the surface I0, W m-2.
        half_saturation: Light half-saturation constant K, W m-2.
        attenuation: Attenuation coefficient k, m-1.
        depth: Mixed-layer depth H, m, positive.
    """
    if surface_light <= 0.0:
        return 0.0
    kh = attenuation * depth
    return math.log((surface_light + half_saturation) / (surface_light + half_saturation * math.exp(-kh))) / kh


def npzd_rates(
    state: Sequence[float],
    params: PlanktonParameters,
    temperature: float,
    surface_light: float,
    mixed_layer_depth: float,
) -> list[float]:
    """Time derivatives of (N, P, Z, D), mmol N m-3 per day."""
    n, p, z, d = state
    light = mean_light_limitation(surface_light, params.light_half_saturation, params.attenuation, mixed_layer_depth)
    nutrient = n / (n + params.nutrient_half_saturation)
    uptake = params.max_growth * temperature_factor(temperature, params.q10) * nutrient * light * p
    grazing = params.max_grazing * p * p / (p * p + params.grazing_half_saturation**2) * z
    zoo_loss = params.zoo_mortality * z
    excreted = params.excretion * z
    remineralised = params.remineralisation * d
    phyto_loss = params.phyto_mortality * p
    dn = -uptake + excreted + remineralised
    dp = uptake - grazing - phyto_loss
    dz = params.assimilation * grazing - zoo_loss - excreted
    dd = (1.0 - params.assimilation) * grazing + params.phyto_mortality * p * p + zoo_loss - remineralised
    return [dn, dp, dz, dd]


def euler_run(
    rates: Callable[[float, list[float]], list[float]],
    state: Sequence[float],
    duration_days: float,
    step_days: float = 1.0 / 24.0,
) -> list[tuple[float, list[float]]]:
    """Integrate with forward Euler steps and return the trajectory.

    The step is short compared with the fastest plankton time scale (about a
    day), which keeps forward Euler stable and accurate enough for the
    seasonal runs the model is used for.

    Returns:
        The pairs (time in days, state), starting with the initial state and
        ending at ``duration_days``.
    """
    y = list(state)
    t = 0.0
    trajectory = [(t, list(y))]
    while t < duration_days:
        dy = rates(t, y)
        y = [yi + step_days * dyi for yi, dyi in zip(y, dy)]
        t += step_days
        trajectory.append((t, list(y)))
    return trajectory


def logistic(t: float, initial: float, capacity: float, rate: float) -> float:
    """Closed-form solution of dP/dt = r P (1 - P / K), used to test the integrators."""
    return capacity / (1.0 + (capacity / initial - 1.0) * math.exp(-rate * t))


def time_to_half_capacity(initial: float, capacity: float, rate: float) -> float:
    """Time at which the logistic solution reaches K / 2, days.

    Requires 0 < initial < capacity / 2.
    """
    return math.log(capacity / initial - 1.0) / rate
'''


ODE_PY = '''\
"""Adaptive integration of ordinary differential equations.

The plankton model of :mod:`limno.ecology` becomes stiff during blooms, when
grazing and uptake rates change by orders of magnitude within days. The
embedded Bogacki-Shampine 3(2) pair adapts the step to the local error, which
keeps seasonal runs both cheap and accurate.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass

Rates = Callable[[float, list[float]], list[float]]

SAFETY = 0.9
MIN_FACTOR = 0.2
MAX_FACTOR = 5.0


@dataclass(frozen=True)
class Solution:
    """Accepted steps of an adaptive integration."""

    times: list[float]
    states: list[list[float]]
    rejected: int


def _combine(y: Sequence[float], h: float, terms: Sequence[tuple[float, Sequence[float]]]) -> list[float]:
    """Return y + h * sum(c * k for c, k in terms)."""
    out = list(y)
    for coefficient, k in terms:
        for i, ki in enumerate(k):
            out[i] += h * coefficient * ki
    return out


def bogacki_shampine_step(f: Rates, t: float, y: list[float], h: float) -> tuple[list[float], list[float]]:
    """One step of the Bogacki-Shampine pair.

    Returns:
        The third-order solution at t + h and the difference between the
        third- and second-order solutions, an estimate of the local error.
    """
    k1 = f(t, y)
    k2 = f(t + 0.5 * h, _combine(y, h, [(0.5, k1)]))
    k3 = f(t + 0.75 * h, _combine(y, h, [(0.75, k2)]))
    y3 = _combine(y, h, [(2.0 / 9.0, k1), (1.0 / 3.0, k2), (4.0 / 9.0, k3)])
    k4 = f(t + h, y3)
    y2 = _combine(y, h, [(7.0 / 24.0, k1), (0.25, k2), (1.0 / 3.0, k3), (0.125, k4)])
    return y3, [a - b for a, b in zip(y3, y2)]


def error_norm(
    error: Sequence[float], y_old: Sequence[float], y_new: Sequence[float], rtol: float, atol: float
) -> float:
    """Root-mean-square of the error scaled by the mixed tolerance of each component."""
    total = 0.0
    for e, a, b in zip(error, y_old, y_new):
        scale = atol + rtol * max(abs(a), abs(b))
        total += (e / scale) ** 2
    return math.sqrt(total / len(error))


def integrate(
    f: Rates,
    y0: Sequence[float],
    t0: float,
    t1: float,
    first_step: float = 0.1,
    rtol: float = 1e-6,
    atol: float = 1e-9,
    max_steps: int = 100_000,
) -> Solution:
    """Integrate y' = f(t, y) from ``t0`` to ``t1`` with adaptive steps.

    A step is accepted when the scaled error norm is at most one; otherwise it
    is repeated from the same point with a smaller step. The step factor
    follows the usual (1 / err) ** (1 / 3) rule of a third-order method,
    limited to [MIN_FACTOR, MAX_FACTOR].

    Returns:
        The accepted times and states, starting at ``t0`` and ending at ``t1``.
    """
    t = t0
    y = list(y0)
    h = min(first_step, t1 - t0)
    times = [t]
    states = [list(y)]
    rejected = 0
    for _ in range(max_steps):
        if t >= t1:
            return Solution(times, states, rejected)
        h = min(h, t1 - t)
        y_old = y
        y, error = bogacki_shampine_step(f, t, y_old, h)
        err = error_norm(error, y_old, y, rtol, atol)
        factor = MAX_FACTOR if err == 0.0 else min(MAX_FACTOR, max(MIN_FACTOR, SAFETY * err ** (-1.0 / 3.0)))
        if err <= 1.0:
            t += h
            times.append(t)
            states.append(list(y))
        else:
            rejected += 1
        h *= factor
    raise RuntimeError(f"no convergence within {max_steps} steps")
'''


MODEL_PY = '''\
"""Coupled lake model: surface energy balance, vertical heat transport and plankton.

One call of :meth:`LakeModel.step` advances the physics and the biology by one
time step of ``ModelConfig.step`` seconds, with the weather of one
:class:`~limno.forcing.Forcing` record.
"""

from __future__ import annotations

import statistics
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

from limno.column import LakeColumn, mixed_layer_depth
from limno.ecology import PlanktonParameters, npzd_rates
from limno.fluxes import SurfaceFluxes, surface_fluxes
from limno.forcing import Forcing
from limno.units import SECONDS_PER_DAY

PAR_FRACTION = 0.45  # share of shortwave energy in the photosynthetically active band


@dataclass(frozen=True)
class ModelConfig:
    """Numerical settings of the coupled model.

    Attributes:
        step: Time step, s. The implicit heat transport is stable for any
            step; the plankton model needs steps well below one day.
        mixing_threshold: Temperature drop, K, that ends the mixed layer.
    """

    step: float = 3600.0
    mixing_threshold: float = 0.2


@dataclass(frozen=True)
class StepOutput:
    """Diagnostics of one model step."""

    time: float
    surface_temperature: float
    mixed_layer_depth: float
    fluxes: SurfaceFluxes
    plankton: tuple[float, float, float, float]


@dataclass
class LakeModel:
    """The coupled model and its state."""

    column: LakeColumn
    plankton: list[float]
    parameters: PlanktonParameters = field(default_factory=PlanktonParameters)
    config: ModelConfig = field(default_factory=ModelConfig)

    def step(self, forcing: Forcing) -> StepOutput:
        """Advance physics and biology by one step."""
        t_surface = self.column.temperatures[0]
        fluxes = surface_fluxes(t_surface, forcing)
        self.column.run_implicit(self.config.step, [fluxes.net])
        depth = mixed_layer_depth(self.column, self.config.mixing_threshold)
        light = PAR_FRACTION * fluxes.shortwave
        mixed = self._mixed_layer_temperature(depth)
        rates = npzd_rates(self.plankton, self.parameters, mixed, light, depth)
        step_days = self.config.step / SECONDS_PER_DAY
        self.plankton = [x + step_days * r for x, r in zip(self.plankton, rates)]
        n, p, z, d = self.plankton
        return StepOutput(self.column.time, self.column.temperatures[0], depth, fluxes, (n, p, z, d))

    def run(self, forcings: Iterable[Forcing]) -> list[StepOutput]:
        """Advance the model through a sequence of forcing records."""
        return [self.step(forcing) for forcing in forcings]

    def total_nitrogen(self) -> float:
        """Sum of the four plankton pools, mmol N m-3."""
        return sum(self.plankton)

    def _mixed_layer_temperature(self, depth: float) -> float:
        """Thickness-weighted mean temperature of the layers above ``depth``."""
        weighted = 0.0
        total = 0.0
        top = 0.0
        for h, t in zip(self.column.thicknesses, self.column.temperatures):
            if top >= depth:
                break
            part = min(h, depth - top)
            weighted += part * t
            total += part
            top += h
        return weighted / total if total > 0.0 else self.column.temperatures[0]


def spin_up(column: LakeColumn, surface_flux: float, days: float, step: float = 3600.0) -> list[list[float]]:
    """Relax a column under a constant surface flux before a run.

    Returns:
        The temperature profile after each step.
    """
    steps = round(days * SECONDS_PER_DAY / step)
    return column.run_implicit(step, [surface_flux] * steps)


def daily_summary(outputs: Sequence[StepOutput]) -> list[dict[str, float]]:
    """Daily means of the surface temperature, mixed-layer depth and net flux.

    Days are counted from the start of the run; the last day may be partial.
    """
    days: dict[int, list[StepOutput]] = {}
    for output in outputs:
        day = int((output.time - 1e-9) // SECONDS_PER_DAY)
        days.setdefault(day, []).append(output)
    summary = []
    for day in sorted(days):
        group = days[day]
        summary.append(
            {
                "day": float(day),
                "surface_temperature": statistics.fmean(o.surface_temperature for o in group),
                "mixed_layer_depth": statistics.fmean(o.mixed_layer_depth for o in group),
                "net_flux": statistics.fmean(o.fluxes.net for o in group),
            }
        )
    return summary
'''


OBSERVATIONS_PY = '''\
"""Reading and quality control of buoy observation files.

Observation files are CSV with a header row and the columns ``time`` (ISO
8601, UTC), ``depth`` (m), ``temperature`` (degrees Celsius) and ``flag``
(0 for a good reading). Readings flagged by the logger are discarded on load.
"""

from __future__ import annotations

import csv
import math
import statistics
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

MAD_TO_SIGMA = 1.4826  # median absolute deviation of a normal sample, in standard deviations


@dataclass(frozen=True)
class Observation:
    """One reading of one thermistor."""

    time: datetime
    depth: float
    temperature: float


def parse_time(text: str) -> datetime:
    """Parse an ISO 8601 time; times without an offset are taken as UTC."""
    value = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def read_observations(path: Path) -> list[Observation]:
    """Read the good readings of an observation file, sorted by time and depth."""
    observations = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if int(row["flag"]) != 0:
                continue
            observations.append(
                Observation(parse_time(row["time"]), float(row["depth"]), float(row["temperature"]))
            )
    observations.sort(key=lambda o: (o.time, o.depth))
    return observations


def hourly_series(
    observations: Iterable[Observation], depth: float, start: datetime, hours: int
) -> list[float | None]:
    """Hourly mean temperature of the thermistor at ``depth``.

    Entry k averages the readings in [start + k h, start + (k + 1) h); hours
    without a reading are ``None``.
    """
    sums = [0.0] * hours
    counts = [0] * hours
    for observation in observations:
        if observation.depth != depth:
            continue
        k = math.floor((observation.time - start) / timedelta(hours=1))
        if 0 <= k < hours:
            sums[k] += observation.temperature
            counts[k] += 1
    return [s / c if c else None for s, c in zip(sums, counts)]


def depths_of(observations: Iterable[Observation]) -> list[float]:
    """Distinct thermistor depths, sorted."""
    return sorted({o.depth for o in observations})


def despike(values: Sequence[float | None], half_window: int = 3, threshold: float = 4.0) -> list[float | None]:
    """Remove isolated spikes with a running median filter.

    A value is replaced by ``None`` when it differs from the median of the
    surrounding window by more than ``threshold`` robust standard deviations,
    estimated from the median absolute deviation of the window.
    """
    out: list[float | None] = list(values)
    for i, v in enumerate(values):
        if v is None:
            continue
        window = [w for w in values[max(0, i - half_window) : i + half_window + 1] if w is not None]
        if len(window) < 3:
            continue
        centre = statistics.median(window)
        mad = statistics.median(abs(w - centre) for w in window)
        if mad == 0.0:
            continue
        if abs(v - centre) > threshold * MAD_TO_SIGMA * mad:
            out[i] = None
    return out
'''


TIMESERIES_PY = '''\
"""Preparation of evenly spaced observation series.

Missing values are ``None``. The functions return new lists and never modify
their arguments.
"""

from __future__ import annotations

import math
import statistics
from collections.abc import Sequence


def valid_indices(values: Sequence[float | None]) -> list[int]:
    """Indices of the values that are present."""
    return [i for i, v in enumerate(values) if v is not None]


def fill_gaps(values: Sequence[float | None], max_gap: int | None = None) -> list[float | None]:
    """Fill missing values by linear interpolation between the nearest present ones.

    Gaps at the start or end of the series take the nearest present value.
    Gaps longer than ``max_gap`` values, when given, are left missing.

    Args:
        values: Evenly spaced series with ``None`` for missing values.
        max_gap: Longest run of missing values to fill.
    """
    present = valid_indices(values)
    if not present:
        raise ValueError("the series has no values")
    filled: list[float | None] = list(values)
    first, last = present[0], present[-1]
    for i in range(first):
        filled[i] = values[first]
    for i in range(last + 1, len(values)):
        filled[i] = values[last]
    for left, right in zip(present, present[1:]):
        gap = right - left - 1
        if gap == 0 or (max_gap is not None and gap > max_gap):
            continue
        a, b = values[left], values[right]
        assert a is not None and b is not None
        for i in range(left + 1, right):
            fraction = (i - left) / (right - left)
            filled[i] = a + fraction * (b - a)
    return filled


def moving_average(values: Sequence[float], window: int) -> list[float]:
    """Trailing moving average; the first ``window - 1`` entries average fewer values."""
    if window < 1:
        raise ValueError("the window must hold at least one value")
    out = []
    total = 0.0
    for i, v in enumerate(values):
        total += v
        if i >= window:
            total -= values[i - window]
        out.append(total / min(i + 1, window))
    return out


def anomalies(values: Sequence[float], period: int) -> list[float]:
    """Deviations from the mean seasonal cycle of length ``period`` samples."""
    if len(values) < period:
        raise ValueError("the series is shorter than one period")
    cycle = [statistics.fmean(values[phase::period]) for phase in range(period)]
    return [v - cycle[i % period] for i, v in enumerate(values)]


def standardise(train: Sequence[float], test: Sequence[float]) -> tuple[list[float], list[float]]:
    """Scale both parts with the mean and standard deviation of the training part only."""
    mean = statistics.fmean(train)
    spread = statistics.stdev(train)
    if spread == 0.0 or math.isnan(spread):
        raise ValueError("the training part has no spread")
    return [(x - mean) / spread for x in train], [(x - mean) / spread for x in test]


def lagged(values: Sequence[float], lag: int) -> list[float | None]:
    """The series shifted by ``lag`` steps; the first ``lag`` entries are missing."""
    if lag < 0:
        raise ValueError("the lag must be non-negative")
    return [None] * lag + list(values[: len(values) - lag])
'''


STATS_PY = '''\
"""Summary statistics for buoy observations and model residuals.

Observation series of the network are short (a few days to a few months of
daily values) and often autocorrelated, so the functions here use small-sample
quantiles and offer effective-sample-size corrections.
"""

from __future__ import annotations

import math
import statistics
from collections.abc import Sequence

# Two-sided 95 % quantiles of Student's t distribution, t(0.975, df).
T_975 = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306,
    9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131, 16: 2.120,
    17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086, 21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064,
    25: 2.060, 26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042, 40: 2.021, 60: 2.000,
    120: 1.980,
}
Z_975 = 1.959964


def t_quantile_975(df: float) -> float:
    """t(0.975, df) from the table, rounding ``df`` down to a tabulated value.

    Rounding down gives the larger quantile, so intervals err on the wide side.
    Above 120 degrees of freedom the normal quantile is used; it is at most
    1 % below the exact value there, no more than rounding down already
    overstates it between 60 and 120 degrees of freedom.
    """
    if df < 1:
        raise ValueError("at least one degree of freedom is needed")
    if df > 120:
        return Z_975
    return T_975[max(k for k in T_975 if k <= df)]


def weighted_mean(values: Sequence[float], weights: Sequence[float]) -> float:
    """Weighted mean of ``values``."""
    if len(values) != len(weights) or not values:
        raise ValueError("values and weights must be non-empty and of equal length")
    return math.fsum(w * x for x, w in zip(values, weights)) / math.fsum(weights)


def weighted_variance(values: Sequence[float], weights: Sequence[float]) -> float:
    """Unbiased weighted variance of sensor readings.

    The weights are reliability weights, the inverse error variances that the
    calibration certificates give for each sensor, not repetition counts, so
    only their ratios carry information. The estimate is unbiased for
    independent readings of a common distribution.
    """
    mean = weighted_mean(values, weights)
    v1 = math.fsum(weights)
    v2 = math.fsum(w * w for w in weights)
    if v2 >= v1 * v1:
        raise ValueError("at least two readings with positive weight are needed")
    spread = math.fsum(w * (x - mean) ** 2 for x, w in zip(values, weights))
    return spread / (v1 - 1.0)


def mean_confidence_interval(values: Sequence[float]) -> tuple[float, float]:
    """Two-sided 95 % confidence interval of the mean of independent readings.

    Uses Student's t with n - 1 degrees of freedom, so it remains valid for the
    short replicate series (three to ten readings) of the laboratory checks.
    """
    n = len(values)
    if n < 2:
        raise ValueError("at least two readings are needed")
    mean = statistics.fmean(values)
    spread = statistics.pstdev(values, mean)
    half_width = t_quantile_975(n - 1) * spread / math.sqrt(n)
    return mean - half_width, mean + half_width


def lag1_autocorrelation(values: Sequence[float]) -> float:
    """Lag-one sample autocorrelation of an evenly spaced series."""
    n = len(values)
    if n < 3:
        raise ValueError("at least three values are needed")
    mean = statistics.fmean(values)
    deviations = [x - mean for x in values]
    numerator = math.fsum(deviations[i] * deviations[i + 1] for i in range(n - 1))
    denominator = math.fsum(d * d for d in deviations)
    return numerator / denominator


def effective_sample_size(n: int, rho: float) -> float:
    """Number of independent values that carry the same information about the mean.

    For a first-order autoregressive series with lag-one autocorrelation rho,
    the variance of the mean is that of n * (1 - rho) / (1 + rho) independent
    values (Bayley and Hammersley 1946, large-n form).
    """
    if not -1.0 < rho < 1.0:
        raise ValueError("rho must lie strictly between -1 and 1")
    return n * (1.0 - rho) / (1.0 + rho)


def autocorrelated_mean_interval(values: Sequence[float]) -> tuple[float, float]:
    """Two-sided 95 % interval of the mean of an AR(1)-like series.

    Negative lag-one autocorrelation is set to zero, which keeps the interval
    from shrinking below the independent case.
    """
    n = len(values)
    rho = max(0.0, lag1_autocorrelation(values))
    n_eff = effective_sample_size(n, rho)
    mean = statistics.fmean(values)
    half_width = t_quantile_975(max(1.0, n_eff - 1.0)) * statistics.stdev(values) / math.sqrt(n_eff)
    return mean - half_width, mean + half_width


def bias(observed: Sequence[float], simulated: Sequence[float]) -> float:
    """Mean of simulated minus observed values."""
    return statistics.fmean(s - o for o, s in zip(observed, simulated, strict=True))


def rmse(observed: Sequence[float], simulated: Sequence[float]) -> float:
    """Root-mean-square difference between simulated and observed values."""
    return math.sqrt(statistics.fmean((s - o) ** 2 for o, s in zip(observed, simulated, strict=True)))


def nash_sutcliffe(observed: Sequence[float], simulated: Sequence[float]) -> float:
    """Nash-Sutcliffe efficiency: 1 for a perfect model, 0 for the mean of the observations."""
    mean = statistics.fmean(observed)
    residual = math.fsum((s - o) ** 2 for o, s in zip(observed, simulated, strict=True))
    variance = math.fsum((o - mean) ** 2 for o in observed)
    return 1.0 - residual / variance
'''


CALIBRATE_PY = '''\
"""Calibration of the lake model against buoy observations.

Calibration uses a chronological split: the first part of the record trains
the model and the remainder, which the fit never sees, measures its skill.
Splitting by time rather than at random keeps the autocorrelation of the
series from leaking information across the split.

Observation series are hourly water temperatures, often several years long;
residuals are model minus observation.
"""

from __future__ import annotations

import math
import random
import statistics
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from limno.stats import rmse
from limno.timeseries import fill_gaps, standardise


@dataclass(frozen=True)
class Split:
    """Training and test parts of an observation series."""

    train: list[float]
    test: list[float]
    cut: int


def chronological_split(observations: Sequence[float | None], train_fraction: float = 0.7) -> Split:
    """Fill the gaps of a series and split it in time.

    Args:
        observations: Hourly observations, ``None`` where the logger failed.
        train_fraction: Share of the record used for training, in (0, 1).
    """
    if not 0.0 < train_fraction < 1.0:
        raise ValueError("train_fraction must lie strictly between 0 and 1")
    filled = fill_gaps(observations)
    cut = int(len(filled) * train_fraction)
    train = [float(v) for v in filled[:cut] if v is not None]
    test = [float(v) for v in filled[cut:] if v is not None]
    return Split(train, test, cut)


def standardised_split(
    observations: Sequence[float | None], train_fraction: float = 0.7
) -> tuple[list[float], list[float]]:
    """Chronological split with both parts scaled by the training statistics."""
    split = chronological_split(observations, train_fraction)
    return standardise(split.train, split.test)


def gaussian_log_likelihood(residuals: Sequence[float], sigma: float) -> float:
    """Log-likelihood of independent Gaussian residuals with standard deviation ``sigma``."""
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    norm = 1.0 / (sigma * math.sqrt(2.0 * math.pi))
    likelihood = math.prod(norm * math.exp(-0.5 * (r / sigma) ** 2) for r in residuals)
    return math.log(likelihood)


def maximum_likelihood_sigma(residuals: Sequence[float]) -> float:
    """Maximum-likelihood estimate of the residual standard deviation."""
    return math.sqrt(statistics.fmean(r * r for r in residuals))


def grid_search(objective: Callable[[float], float], grid: Sequence[float]) -> tuple[float, float]:
    """Return the grid value that minimises ``objective`` and the minimum."""
    best = min(grid, key=objective)
    return best, objective(best)


def calibrate_gain(simulated: Sequence[float], observed: Sequence[float], grid: Sequence[float]) -> float:
    """Gain g minimising the RMSE between g * simulated and observed on the training data."""
    best, _ = grid_search(lambda g: rmse(observed, [g * s for s in simulated]), grid)
    return best


def bootstrap_interval(
    residuals: Sequence[float],
    statistic: Callable[[Sequence[float]], float],
    resamples: int = 2000,
    seed: int = 12345,
) -> tuple[float, float]:
    """Percentile bootstrap 95 % interval of ``statistic`` over the residuals.

    The residuals are the daily means of the hourly model-minus-observation
    differences over the test period. Each resample draws as many residuals
    as there are, with replacement and independently of one another.
    """
    rng = random.Random(seed)
    n = len(residuals)
    estimates = sorted(statistic([residuals[rng.randrange(n)] for _ in range(n)]) for _ in range(resamples))
    lower = estimates[int(0.025 * (resamples - 1))]
    upper = estimates[int(math.ceil(0.975 * (resamples - 1)))]
    return lower, upper


def skill_report(observed: Sequence[float], simulated: Sequence[float]) -> dict[str, float]:
    """RMSE, bias and log-likelihood of the simulated series against the observations."""
    residuals = [s - o for o, s in zip(observed, simulated, strict=True)]
    sigma = maximum_likelihood_sigma(residuals)
    return {
        "rmse": rmse(observed, simulated),
        "bias": statistics.fmean(residuals),
        "log_likelihood": gaussian_log_likelihood(residuals, sigma),
    }
'''


WEB_CONVERT_TS = """\
/**
 * Unit conversions used by the dashboard.
 */

export const KELVIN_OFFSET = 273.15;
export const GRAVITY = 9.80665; // m s^-2
export const DAY_MS = 86_400_000;

/** Kelvin to degrees Celsius. */
export function toCelsius(kelvin: number): number {
  return kelvin - KELVIN_OFFSET;
}

/** Degrees Celsius to kelvin. */
export function toKelvin(celsius: number): number {
  return celsius + KELVIN_OFFSET;
}

/** Hectopascals to pascals. */
export function hPaToPa(hPa: number): number {
  return hPa * 100;
}

/**
 * Mean irradiance in W m^-2 to the daily energy total in MJ m^-2 day^-1,
 * the unit of the radiation panels.
 */
export function wattsToDailyMegajoules(watts: number): number {
  return watts * 0.0864;
}

/** Daily energy total in MJ m^-2 day^-1 back to mean irradiance in W m^-2. */
export function dailyMegajoulesToWatts(megajoules: number): number {
  return megajoules / 0.0864;
}

/** Start of the UTC calendar day that contains `time`, ms since the epoch. */
export function utcDayStart(time: number): number {
  return Math.floor(time / DAY_MS) * DAY_MS;
}
"""


WEB_DENSITY_TS = """\
/**
 * Density of lake water.
 *
 * The heat-map panels evaluate the density for every cell of a depth-time
 * grid, about a million calls per redraw, so the results are memoised.
 */

/**
 * Density of fresh water, kg m^-3, at `celsius` degrees Celsius.
 *
 * Formula of Chen and Millero (1986) as simplified by Martin and McCutcheon
 * (1999); accurate to 0.01 kg m^-3 between 0 and 40 degrees Celsius. The
 * maximum of about 1000 kg m^-3 lies near 4 degrees Celsius.
 */
export function freshWaterDensity(celsius: number): number {
  const t = celsius;
  return 1000 * (1 - ((t + 288.9414) / (508929.2 * (t + 68.12963))) * (t - 3.9863) ** 2);
}

/**
 * Density of lake water with dissolved salts, kg m^-3.
 *
 * Adds the leading salinity terms of the UNESCO equation of state to the
 * fresh-water density; adequate below 10 g/kg, the range of the network's
 * saline lakes.
 *
 * @param celsius - water temperature, degrees Celsius
 * @param salinity - salinity, g/kg
 */
export function waterDensity(celsius: number, salinity: number): number {
  const t = celsius;
  return freshWaterDensity(t) + salinity * (0.824493 - 0.0040899 * t + 7.6438e-5 * t * t);
}

const cache = new Map<string, number>();
const CACHE_LIMIT = 100_000;

/**
 * Memoised {@link waterDensity}. Temperatures are keyed to 0.001 degrees
 * Celsius, far below the resolution of the loggers, so the cached value is
 * indistinguishable from a direct evaluation.
 */
export function densityOf(celsius: number, salinity: number): number {
  const key = celsius.toFixed(3);
  const hit = cache.get(key);
  if (hit !== undefined) return hit;
  const value = waterDensity(celsius, salinity);
  if (cache.size >= CACHE_LIMIT) cache.clear();
  cache.set(key, value);
  return value;
}

/** Empty the density cache. */
export function clearDensityCache(): void {
  cache.clear();
}
"""


WEB_PROFILE_TS = """\
/**
 * Lookup and interpolation of temperature profiles.
 */

import type { Profile } from "./types.ts";

/**
 * Linear interpolation of tabulated values.
 *
 * @param xs - abscissae, strictly increasing
 * @param ys - values at the abscissae
 * @param x - point inside [xs[0], xs[xs.length - 1]], ends included
 */
export function interpolate(xs: readonly number[], ys: readonly number[], x: number): number {
  const n = xs.length;
  if (n < 2 || ys.length !== n) throw new RangeError("need at least two points of equal length");
  if (x < xs[0] || x > xs[n - 1]) throw new RangeError(`${x} lies outside [${xs[0]}, ${xs[n - 1]}]`);
  // Binary search for the first abscissa greater than x.
  let lo = 0;
  let hi = n;
  while (lo < hi) {
    const mid = (lo + hi) >>> 1;
    if (xs[mid] <= x) lo = mid + 1;
    else hi = mid;
  }
  const right = lo;
  const left = right - 1;
  const weight = (x - xs[left]) / (xs[right] - xs[left]);
  return ys[left] + weight * (ys[right] - ys[left]);
}

/**
 * Temperature recorded by the sensor at a nominal depth, K, or undefined when
 * the profile has no sensor there.
 *
 * Sensor depths are the nominal values of the station configuration, copied
 * unchanged into every profile and never computed, so an exact comparison
 * selects the sensor reliably.
 */
export function sensorValue(profile: Profile, depth: number): number | undefined {
  const index = profile.depths.findIndex((d) => d === depth);
  return index < 0 ? undefined : profile.temperatures[index];
}

/** Temperatures of a profile resampled onto `grid`, K. */
export function resample(profile: Profile, grid: readonly number[]): number[] {
  return grid.map((z) => interpolate(profile.depths, profile.temperatures, z));
}

/** Salinities of a profile resampled onto `grid`, g/kg. */
export function resampleSalinity(profile: Profile, grid: readonly number[]): number[] {
  return grid.map((z) => interpolate(profile.depths, profile.salinities, z));
}

/** The deepest sensor depth of a profile, m. */
export function deepestSensor(profile: Profile): number {
  return profile.depths[profile.depths.length - 1];
}
"""


WEB_STRATIFICATION_TS = """\
/**
 * Indicators of thermal stratification shown on the profile panel.
 *
 * Thermistor chains of the network carry sensors at uneven depths, closer
 * together near the surface (for example 0.5, 1, 2, 4, 6 and 9 m), and
 * profiles arrive in the logger units described in `types.ts`.
 */

import { GRAVITY, toCelsius } from "./convert.ts";
import { densityOf } from "./density.ts";
import { resample, resampleSalinity } from "./profile.ts";
import type { Hypsography, Profile } from "./types.ts";

/** Density at each sensor of a profile, kg m^-3. */
export function sensorDensities(profile: Profile): number[] {
  return profile.temperatures.map((t, i) => densityOf(t, profile.salinities[i]));
}

/**
 * Vertical temperature gradient just below the surface, K m^-1, positive
 * when the water warms with depth.
 *
 * Uses the second-order one-sided difference through the three uppermost
 * sensors, which is exact for a profile that is quadratic in depth.
 */
export function surfaceGradient(profile: Profile): number {
  const [z0, z1] = profile.depths;
  const [t0, t1, t2] = profile.temperatures;
  if (profile.depths.length < 3) throw new RangeError("need at least three sensors");
  const h = z1 - z0;
  return (-3 * t0 + 4 * t1 - t2) / (2 * h);
}

/**
 * Depth of the thermocline, m: the midpoint between the two adjacent sensors
 * with the steepest temperature drop, or undefined when the column is
 * mixed (no drop steeper than `minimumGradient`, K m^-1).
 */
export function thermoclineDepth(profile: Profile, minimumGradient = 0.5): number | undefined {
  const { depths, temperatures } = profile;
  let best: number | undefined;
  let steepest = minimumGradient;
  for (let i = 0; i + 1 < depths.length; i++) {
    const gradient = (temperatures[i] - temperatures[i + 1]) / (depths[i + 1] - depths[i]);
    if (gradient > steepest) {
      steepest = gradient;
      best = 0.5 * (depths[i] + depths[i + 1]);
    }
  }
  return best;
}

/** Trapezoidal integral of samples `f` over the abscissae `z`. */
function trapezoid(z: readonly number[], f: readonly number[]): number {
  let total = 0;
  for (let i = 0; i + 1 < z.length; i++) total += 0.5 * (f[i] + f[i + 1]) * (z[i + 1] - z[i]);
  return total;
}

/**
 * Schmidt stability, J m^-2: the work per unit surface area needed to mix
 * the lake to uniform density without adding heat.
 *
 * S = (g / A0) * integral from 0 to zmax of (z - zv) * rho(z) * A(z) dz,
 * where A0 is the surface area and zv the depth of the centre of volume of
 * the lake. The profile is interpolated onto the depths of the hypsography,
 * which must lie within the sensor range.
 */
export function schmidtStability(profile: Profile, hypsography: Hypsography): number {
  const z = hypsography.depths;
  const area = hypsography.areas;
  const temperatures = resample(profile, z);
  const salinities = resampleSalinity(profile, z);
  const rho = temperatures.map((t, i) => densityOf(toCelsius(t), salinities[i]));
  const centre = 0.5 * (z[0] + z[z.length - 1]);
  const moment = z.map((zi, i) => (zi - centre) * rho[i] * area[i]);
  return (GRAVITY / area[0]) * trapezoid(z, moment);
}

/** Volume of the lake, m^3, from its hypsography. */
export function lakeVolume(hypsography: Hypsography): number {
  return trapezoid(hypsography.depths, hypsography.areas);
}
"""


WEB_HEATMAP_TS = """\
/**
 * Depth-time grids for the temperature and density heat maps.
 */

import { toCelsius } from "./convert.ts";
import { densityOf } from "./density.ts";
import { deepestSensor, resample, resampleSalinity } from "./profile.ts";
import type { Profile } from "./types.ts";

export interface Grid {
  /** Column times, ms since the epoch. */
  times: number[];
  /** Row depths, m. */
  depths: number[];
  /** values[row][column]. */
  values: number[][];
}

/**
 * Evenly spaced depths from 0 to `bottom` inclusive, `step` apart; the last
 * row is `bottom` itself even when `step` does not divide it.
 */
export function depthAxis(bottom: number, step: number): number[] {
  if (step <= 0) throw new RangeError("step must be positive");
  const count = Math.floor(bottom / step + 1e-9);
  const axis: number[] = [];
  for (let k = 0; k <= count; k++) axis.push(k * step);
  if (bottom - axis[axis.length - 1] > 1e-9) axis.push(bottom);
  return axis;
}

/** The deepest depth that every profile covers, m. */
export function commonBottom(profiles: readonly Profile[]): number {
  return Math.min(...profiles.map(deepestSensor));
}

/** Shallowest sensor depth over all profiles, m. */
export function commonTop(profiles: readonly Profile[]): number {
  return Math.max(...profiles.map((p) => p.depths[0]));
}

/**
 * Temperature heat map in degrees Celsius. Rows run from the shallowest
 * depth every profile covers down to the deepest such depth.
 */
export function temperatureGrid(profiles: readonly Profile[], step: number): Grid {
  const top = commonTop(profiles);
  const depths = depthAxis(commonBottom(profiles) - top, step).map((z) => z + top);
  const values = depths.map(() => new Array<number>(profiles.length).fill(NaN));
  profiles.forEach((profile, column) => {
    resample(profile, depths).forEach((kelvin, row) => {
      values[row][column] = toCelsius(kelvin);
    });
  });
  return { times: profiles.map((p) => p.time), depths, values };
}

/** Density heat map, kg m^-3, on the same rows as {@link temperatureGrid}. */
export function densityGrid(profiles: readonly Profile[], step: number): Grid {
  const temperatures = temperatureGrid(profiles, step);
  const values = temperatures.values.map((row) => row.slice());
  profiles.forEach((profile, column) => {
    const salinity = resampleSalinity(profile, temperatures.depths);
    temperatures.depths.forEach((_, row) => {
      values[row][column] = densityOf(temperatures.values[row][column], salinity[row]);
    });
  });
  return { times: temperatures.times, depths: temperatures.depths, values };
}

/** Smallest and largest finite value of a grid, for the colour scale. */
export function valueRange(grid: Grid): [number, number] {
  let low = Infinity;
  let high = -Infinity;
  for (const row of grid.values) {
    for (const v of row) {
      if (!Number.isFinite(v)) continue;
      if (v < low) low = v;
      if (v > high) high = v;
    }
  }
  return [low, high];
}
"""


WEB_LEVEL_TS = """\
/**
 * Water level from submerged pressure transducers.
 *
 * Each transducer records the absolute pressure above it; subtracting the
 * barometric pressure of the nearest weather station leaves the hydrostatic
 * pressure of the water column, which gives the depth of water above the
 * sensor.
 */

import { GRAVITY } from "./convert.ts";
import type { DepthSample, MetSample } from "./types.ts";

/** Density used to convert hydrostatic pressure to depth, kg m^-3. */
export const WATER_DENSITY = 1000;

/** Largest time difference, ms, at which a barometric reading is used. */
export const MAX_BAROMETER_LAG = 30 * 60 * 1000;

/**
 * Depth of water above a transducer, m.
 *
 * @param absolutePressure - transducer reading, Pa
 * @param atmosphericPressure - barometric pressure at the same time, Pa
 */
export function depthFromPressure(absolutePressure: number, atmosphericPressure: number): number {
  const hydrostatic = absolutePressure - atmosphericPressure;
  return hydrostatic / (WATER_DENSITY * GRAVITY);
}

/**
 * Index of the barometric sample nearest in time to `time`, or -1 when the
 * nearest one is more than {@link MAX_BAROMETER_LAG} away. `met` is sorted
 * by time.
 */
export function nearestMet(met: readonly MetSample[], time: number): number {
  let best = -1;
  let bestLag = Infinity;
  for (let i = 0; i < met.length; i++) {
    const lag = Math.abs(met[i].time - time);
    if (lag < bestLag) {
      bestLag = lag;
      best = i;
    }
  }
  return bestLag <= MAX_BAROMETER_LAG ? best : -1;
}

/**
 * Depth series of one transducer, compensated with the barometric record.
 * Readings without a barometric sample close enough in time are dropped.
 */
export function compensatedDepths(
  samples: readonly DepthSample[],
  met: readonly MetSample[],
): { time: number; depth: number }[] {
  const out: { time: number; depth: number }[] = [];
  for (const sample of samples) {
    const index = nearestMet(met, sample.time);
    if (index < 0) continue;
    out.push({ time: sample.time, depth: depthFromPressure(sample.pressure, met[index].pressure) });
  }
  return out;
}

/** Water-level change between the first and last compensated readings, m. */
export function levelChange(series: readonly { time: number; depth: number }[]): number {
  if (series.length < 2) throw new RangeError("need at least two readings");
  return series[series.length - 1].depth - series[0].depth;
}
"""


WEB_SERIES_TS = """\
/**
 * Aggregation and summary of logger time series.
 */

import { DAY_MS, utcDayStart } from "./convert.ts";
import type { Sample } from "./types.ts";

/**
 * Mean of the samples of every UTC calendar day that has at least one sample.
 *
 * @param samples - samples sorted by time
 * @returns one sample per day, stamped with the start of the day (00:00 UTC)
 */
export function dailyMeans(samples: readonly Sample[]): Sample[] {
  if (samples.length === 0) return [];
  const origin = samples[0].time;
  const sums = new Map<number, { total: number; count: number }>();
  for (const sample of samples) {
    const day = Math.floor((sample.time - origin) / DAY_MS);
    const entry = sums.get(day) ?? { total: 0, count: 0 };
    entry.total += sample.value;
    entry.count += 1;
    sums.set(day, entry);
  }
  return [...sums.entries()]
    .sort((a, b) => a[0] - b[0])
    .map(([day, { total, count }]) => ({ time: origin + day * DAY_MS, value: total / count }));
}

/**
 * Share of the expected samples present on each UTC day, for the coverage bar.
 *
 * @param samples - samples sorted by time
 * @param intervalMs - logging interval, ms
 */
export function dailyCoverage(samples: readonly Sample[], intervalMs: number): Map<number, number> {
  const expected = DAY_MS / intervalMs;
  const counts = new Map<number, number>();
  for (const sample of samples) {
    const day = utcDayStart(sample.time);
    counts.set(day, (counts.get(day) ?? 0) + 1);
  }
  const coverage = new Map<number, number>();
  for (const [day, count] of counts) coverage.set(day, Math.min(1, count / expected));
  return coverage;
}

/**
 * Sample standard deviation over a trailing window of `window` values, for
 * the noise panel of the pressure transducers (absolute pressures around
 * 1.5e5 Pa, logged every minute for months). Running sums make each window
 * O(1), so the whole series costs O(n).
 *
 * @returns one value per index from `window - 1` on; NaN before
 */
export function rollingStd(values: readonly number[], window: number): number[] {
  if (window < 2) throw new RangeError("window must hold at least two values");
  const prefix = [0];
  const prefixSquares = [0];
  for (const v of values) {
    prefix.push(prefix[prefix.length - 1] + v);
    prefixSquares.push(prefixSquares[prefixSquares.length - 1] + v * v);
  }
  return values.map((_, i) => {
    if (i < window - 1) return NaN;
    const sum = prefix[i + 1] - prefix[i + 1 - window];
    const sumSquares = prefixSquares[i + 1] - prefixSquares[i + 1 - window];
    const variance = (sumSquares - (sum * sum) / window) / (window - 1);
    return Math.sqrt(Math.max(0, variance));
  });
}

/**
 * Pearson correlation of two series sampled at the same times. Logger gaps
 * appear as NaN in either series and are left out.
 */
export function correlation(a: readonly number[], b: readonly number[]): number {
  if (a.length !== b.length) throw new RangeError("series must have equal length");
  const x = a.filter((v) => !Number.isNaN(v));
  const y = b.filter((v) => !Number.isNaN(v));
  const n = Math.min(x.length, y.length);
  if (n < 3) throw new RangeError("need at least three complete pairs");
  let mx = 0;
  let my = 0;
  for (let i = 0; i < n; i++) {
    mx += x[i] / n;
    my += y[i] / n;
  }
  let sxy = 0;
  let sxx = 0;
  let syy = 0;
  for (let i = 0; i < n; i++) {
    sxy += (x[i] - mx) * (y[i] - my);
    sxx += (x[i] - mx) ** 2;
    syy += (y[i] - my) ** 2;
  }
  return sxy / Math.sqrt(sxx * syy);
}
"""


WEB_TREND_TS = """\
/**
 * Trend statistics for the long-term panels: least-squares and Sen slopes
 * and the Mann-Kendall test. Times are ms since the epoch, as in `types.ts`.
 */

/** Standard normal cumulative distribution (Abramowitz and Stegun 7.1.26, error below 1.5e-7). */
export function normalCdf(x: number): number {
  const z = Math.abs(x) / Math.SQRT2;
  const t = 1 / (1 + 0.3275911 * z);
  const poly = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429))));
  const erf = 1 - poly * Math.exp(-z * z);
  return x >= 0 ? 0.5 * (1 + erf) : 0.5 * (1 - erf);
}

/**
 * Least-squares line through (t, y).
 *
 * @returns slope per ms and intercept at t = 0
 */
export function leastSquares(t: readonly number[], y: readonly number[]): { slope: number; intercept: number } {
  const n = t.length;
  if (n < 2 || y.length !== n) throw new RangeError("need at least two points of equal length");
  let st = 0;
  let sy = 0;
  let stt = 0;
  let sty = 0;
  for (let i = 0; i < n; i++) {
    st += t[i];
    sy += y[i];
    stt += t[i] * t[i];
    sty += t[i] * y[i];
  }
  const slope = (n * sty - st * sy) / (n * stt - st * st);
  return { slope, intercept: (sy - slope * st) / n };
}

/**
 * Standard error of the least-squares slope, in the units of the slope,
 * for independent errors of constant variance.
 */
export function slopeStandardError(t: readonly number[], y: readonly number[]): number {
  const n = t.length;
  if (n < 3 || y.length !== n) throw new RangeError("need at least three points of equal length");
  const tm = t.reduce((s, v) => s + v, 0) / n;
  const ym = y.reduce((s, v) => s + v, 0) / n;
  let sxx = 0;
  let sxy = 0;
  for (let i = 0; i < n; i++) {
    sxx += (t[i] - tm) ** 2;
    sxy += (t[i] - tm) * (y[i] - ym);
  }
  const slope = sxy / sxx;
  let sse = 0;
  for (let i = 0; i < n; i++) sse += (y[i] - ym - slope * (t[i] - tm)) ** 2;
  return Math.sqrt(sse / (n - 2)) / sxx;
}

/** Median of a non-empty list; the input is not modified. */
export function median(values: readonly number[]): number {
  const sorted = [...values].sort((a, b) => a - b);
  const mid = sorted.length >> 1;
  return sorted.length % 2 === 1 ? sorted[mid] : 0.5 * (sorted[mid - 1] + sorted[mid]);
}

/** Sen's slope: the median of the slopes between all pairs of points with distinct times. */
export function senSlope(t: readonly number[], y: readonly number[]): number {
  const slopes: number[] = [];
  for (let i = 0; i < t.length; i++) {
    for (let j = i + 1; j < t.length; j++) {
      if (t[j] !== t[i]) slopes.push((y[j] - y[i]) / (t[j] - t[i]));
    }
  }
  if (slopes.length === 0) throw new RangeError("need two points with distinct times");
  return median(slopes);
}

export interface MannKendallResult {
  s: number;
  z: number;
  /** Two-sided p-value of the hypothesis of no monotonic trend. */
  p: number;
  direction: "increasing" | "decreasing" | "none";
}

/**
 * Mann-Kendall test for a monotonic trend in an evenly spaced series, with
 * the variance corrected for tied values and a continuity correction of one.
 * Uses the normal approximation, adequate from about ten values on.
 *
 * @param alpha - significance level of the reported direction
 */
export function mannKendall(y: readonly number[], alpha = 0.05): MannKendallResult {
  const n = y.length;
  if (n < 3) throw new RangeError("need at least three values");
  let s = 0;
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) s += Math.sign(y[j] - y[i]);
  }
  const ties = new Map<number, number>();
  for (const v of y) ties.set(v, (ties.get(v) ?? 0) + 1);
  let tieTerm = 0;
  for (const t of ties.values()) tieTerm += t * (t - 1) * (2 * t + 5);
  const variance = (n * (n - 1) * (2 * n + 5) - tieTerm) / 18;
  const sd = Math.sqrt(variance);
  let z = 0;
  if (sd > 0) {
    if (s > 0) z = (s - 1) / sd;
    else if (s < 0) z = (s + 1) / sd;
  }
  const p = 1 - normalCdf(Math.abs(z));
  let direction: MannKendallResult["direction"] = "none";
  if (p < alpha) direction = z > 0 ? "increasing" : "decreasing";
  return { s, z, p, direction };
}
"""


WEB_PANELS_TS = """\
/**
 * Data for the dashboard panels, assembled from the analysis modules.
 */

import { DAY_MS, toCelsius, wattsToDailyMegajoules } from "./convert.ts";
import { compensatedDepths, levelChange } from "./level.ts";
import { dailyMeans, rollingStd } from "./series.ts";
import { schmidtStability, sensorDensities, surfaceGradient, thermoclineDepth } from "./stratification.ts";
import { leastSquares, mannKendall, senSlope, slopeStandardError } from "./trend.ts";
import type { DepthSample, Hypsography, MetSample, Profile, Sample } from "./types.ts";

const MS_PER_DECADE = 3652.5 * DAY_MS;

export interface ProfilePanel {
  time: number;
  surfaceTemperature: number;
  surfaceGradient: number;
  thermocline: number | undefined;
  schmidt: number;
  densities: number[];
}

/** Stratification summary of one profile; temperatures in degrees Celsius. */
export function profilePanel(profile: Profile, hypsography: Hypsography): ProfilePanel {
  return {
    time: profile.time,
    surfaceTemperature: toCelsius(profile.temperatures[0]),
    surfaceGradient: surfaceGradient(profile),
    thermocline: thermoclineDepth(profile),
    schmidt: schmidtStability(profile, hypsography),
    densities: sensorDensities(profile),
  };
}

export interface TrendPanel {
  /** Least-squares trend, units per decade, with its standard error. */
  slope: number;
  slopeError: number;
  /** Sen's slope, units per decade. */
  sen: number;
  mannKendallP: number;
  direction: "increasing" | "decreasing" | "none";
}

/** Long-term trend of a daily series. */
export function trendPanel(samples: readonly Sample[]): TrendPanel {
  const daily = dailyMeans(samples);
  const t = daily.map((s) => s.time);
  const y = daily.map((s) => s.value);
  const fit = leastSquares(t, y);
  const mk = mannKendall(y);
  return {
    slope: fit.slope * MS_PER_DECADE,
    slopeError: slopeStandardError(t, y) * MS_PER_DECADE,
    sen: senSlope(t, y) * MS_PER_DECADE,
    mannKendallP: mk.p,
    direction: mk.direction,
  };
}

/** Daily radiation totals, MJ m^-2 day^-1, from irradiance samples in W m^-2. */
export function radiationPanel(samples: readonly Sample[]): Sample[] {
  return dailyMeans(samples).map((s) => ({ time: s.time, value: wattsToDailyMegajoules(s.value) }));
}

export interface LevelPanel {
  depths: { time: number; depth: number }[];
  change: number;
  noise: number[];
}

/** Water level and transducer noise of one station. */
export function levelPanel(samples: readonly DepthSample[], met: readonly MetSample[], noiseWindow = 60): LevelPanel {
  const depths = compensatedDepths(samples, met);
  return {
    depths,
    change: levelChange(depths),
    noise: rollingStd(
      samples.map((s) => s.pressure),
      noiseWindow,
    ),
  };
}
"""


README_MD_FEATURE = """\
# limno

A small one-dimensional lake model and the analysis routines around it:
surface energy balance, vertical heat transport, a plankton model, and the
statistics used to calibrate the model against buoy observations. The
TypeScript modules under `src/limno/web/` feed the monitoring dashboard.

## Conventions

The conventions of `src/limno/units.py` hold for the Python code and those of
`src/limno/web/types.ts` for the TypeScript code. Read them before adding a
module; the two sides do not use the same units everywhere.

## Modules

Python (`src/limno/`):

- `radiation.py`: solar geometry and clear-sky shortwave radiation.
- `fluxes.py`: surface energy balance with bulk aerodynamic formulae.
- `column.py`: vertical heat transport, explicit and implicit schemes.
- `ecology.py`, `ode.py`: the NPZD plankton model and its integrators.
- `model.py`: the coupled model.
- `observations.py`, `timeseries.py`, `stats.py`, `calibrate.py`: reading,
  preparing and comparing buoy observations.

TypeScript (`src/limno/web/`):

- `convert.ts`, `density.ts`, `profile.ts`: units, water density and profile
  interpolation.
- `stratification.ts`, `heatmap.ts`: stratification indicators and heat maps.
- `level.ts`, `series.ts`, `trend.ts`: water level, series aggregation and
  trend statistics.
- `panels.ts`: data for the dashboard panels.
"""


MAIN_COMMITS: tuple[Commit, ...] = (
    Commit(
        "Add lake-model package with units, forcing records and the tridiagonal solver",
        (
            SourceFile("README.md", README_MD_MAIN),
            SourceFile("pyproject.toml", PYPROJECT_TOML),
            SourceFile("package.json", PACKAGE_JSON),
            SourceFile("tsconfig.json", TSCONFIG_JSON),
            SourceFile(".gitignore", GITIGNORE),
            SourceFile("src/limno/__init__.py", INIT_PY),
            SourceFile("src/limno/units.py", UNITS_PY),
            SourceFile("src/limno/forcing.py", FORCING_PY),
            SourceFile("src/limno/tridiag.py", TRIDIAG_PY),
            SourceFile("src/limno/web/types.ts", WEB_TYPES_TS),
        ),
    ),
)


FEATURE_COMMITS: tuple[Commit, ...] = (
    Commit(
        "Add solar radiation, surface energy balance and vertical heat transport",
        (
            SourceFile("src/limno/radiation.py", RADIATION_PY),
            SourceFile("src/limno/fluxes.py", FLUXES_PY),
            SourceFile("src/limno/column.py", COLUMN_PY),
        ),
    ),
    Commit(
        "Add the NPZD plankton model, adaptive integrator and coupled model",
        (
            SourceFile("src/limno/ecology.py", ECOLOGY_PY),
            SourceFile("src/limno/ode.py", ODE_PY),
            SourceFile("src/limno/model.py", MODEL_PY),
        ),
    ),
    Commit(
        "Add observation handling, statistics and calibration",
        (
            SourceFile("src/limno/observations.py", OBSERVATIONS_PY),
            SourceFile("src/limno/timeseries.py", TIMESERIES_PY),
            SourceFile("src/limno/stats.py", STATS_PY),
            SourceFile("src/limno/calibrate.py", CALIBRATE_PY),
        ),
    ),
    Commit(
        "Add dashboard modules for stratification, water level and trends",
        (
            SourceFile("src/limno/web/convert.ts", WEB_CONVERT_TS),
            SourceFile("src/limno/web/density.ts", WEB_DENSITY_TS),
            SourceFile("src/limno/web/profile.ts", WEB_PROFILE_TS),
            SourceFile("src/limno/web/stratification.ts", WEB_STRATIFICATION_TS),
            SourceFile("src/limno/web/heatmap.ts", WEB_HEATMAP_TS),
            SourceFile("src/limno/web/level.ts", WEB_LEVEL_TS),
            SourceFile("src/limno/web/series.ts", WEB_SERIES_TS),
            SourceFile("src/limno/web/trend.ts", WEB_TREND_TS),
            SourceFile("src/limno/web/panels.ts", WEB_PANELS_TS),
            SourceFile("README.md", README_MD_FEATURE),
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
    ids = [entry.id for entry in entries]
    for duplicate in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append(f"id {duplicate} is used more than once")
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
    for i, first in enumerate(others):
        for second in others[i + 1 :]:
            if first.file == second.file and first.line <= second.line_end and second.line <= first.line_end:
                problems.append(f"{first.id} and {second.id} overlap")
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
