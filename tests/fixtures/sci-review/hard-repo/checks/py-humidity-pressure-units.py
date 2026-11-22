"""Reproduction check for py-humidity-pressure-units.

Saturated air at 20 degrees Celsius and 101325 Pa holds about 0.0145 kg of
water vapour per kg of air. ``surface_humidities`` must return that value for
the air when the relative humidity is 1.
"""

from _common import failed, passed, setup

setup()
from limno.fluxes import surface_humidities  # noqa: E402
from limno.forcing import Forcing  # noqa: E402

forcing = Forcing(air_temperature=20.0, relative_humidity=1.0, pressure=101325.0, wind_speed=5.0)
q_surface, q_air = surface_humidities(20.0, forcing)
if not 0.013 < q_air < 0.016:
    failed(f"specific humidity of saturated air at 20 C is {q_air:.3e} kg/kg; expected about 1.45e-2")
passed(f"specific humidity {q_air:.4f} kg/kg")
