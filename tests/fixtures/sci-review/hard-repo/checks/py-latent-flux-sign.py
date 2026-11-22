"""Reproduction check for py-latent-flux-sign.

Water at 25 degrees Celsius under dry air at 15 degrees Celsius evaporates and
loses heat. In the module's convention (positive into the water) the latent
heat flux must therefore be negative.
"""

from _common import failed, passed, setup

setup()
from limno.fluxes import evaporation_rate, latent_heat_flux  # noqa: E402
from limno.forcing import Forcing  # noqa: E402

forcing = Forcing(air_temperature=15.0, relative_humidity=0.5, pressure=101325.0, wind_speed=5.0)
evaporation = evaporation_rate(25.0, forcing)
flux = latent_heat_flux(25.0, forcing)
if evaporation <= 0.0:
    print(f"error: expected evaporation, got {evaporation}")
    raise SystemExit(2)
if flux >= 0.0:
    failed(f"evaporating lake gains {flux:.4g} W/m2 of latent heat; the flux must be negative (heat loss)")
passed(f"latent heat flux {flux:.4g} W/m2")
