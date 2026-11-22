"""Reproduction check for py-solar-time-longitude-sign.

At longitude 90 degrees east the sun culminates near 06:00 UTC, so the solar
zenith angle at 06:00 UTC must be smaller than at 18:00 UTC (at 18:00 UTC the
sun is below the horizon there).
"""

from _common import failed, passed, setup

setup()
from limno.radiation import Site, cos_zenith  # noqa: E402

site = Site(latitude=30.0, longitude=90.0)
morning = cos_zenith(site, 172, 6.0)
evening = cos_zenith(site, 172, 18.0)
if morning <= 0.0 or evening >= morning:
    failed(f"cos(zenith) is {morning:.3f} at 06:00 UTC and {evening:.3f} at 18:00 UTC at 90 E; noon is near 06:00 UTC")
passed(f"cos(zenith) {morning:.3f} at 06:00 UTC, {evening:.3f} at 18:00 UTC")
