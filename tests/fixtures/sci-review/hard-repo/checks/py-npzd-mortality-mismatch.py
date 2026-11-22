"""Reproduction check for py-npzd-mortality-mismatch.

The NPZD rates must sum to zero for any state (total nitrogen is conserved).
"""

from _common import failed, passed, setup

setup()
from limno.ecology import PlanktonParameters, npzd_rates  # noqa: E402

rates = npzd_rates([4.0, 3.0, 0.5, 1.0], PlanktonParameters(), 15.0, 120.0, 8.0)
total = sum(rates)
if abs(total) > 1e-12:
    failed(f"derivatives sum to {total:.4g} mmol N m-3 per day for state (4, 3, 0.5, 1); expected 0")
passed(f"derivatives sum to {total:.2g}")
