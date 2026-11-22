"""Reproduction check for py-day-length-half.

At the equinox (declination zero) every latitude has 12 hours between sunrise
and sunset; at 45 N on the June solstice the day lasts about 15.4 hours.
"""

from _common import failed, passed, setup

setup()
from limno.radiation import Site, day_length  # noqa: E402

equinox = day_length(Site(45.0, 0.0), 81)
solstice = day_length(Site(45.0, 0.0), 172)
if abs(equinox - 12.0) > 0.05 or not 15.0 < solstice < 15.8:
    failed(
        f"day length at 45 N: {equinox:.2f} h at the equinox, {solstice:.2f} h at the solstice; expected 12 and 15.4"
    )
passed(f"day lengths {equinox:.2f} h and {solstice:.2f} h")
