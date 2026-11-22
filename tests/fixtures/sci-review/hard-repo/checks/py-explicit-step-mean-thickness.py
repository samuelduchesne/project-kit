"""Reproduction check for py-explicit-step-mean-thickness.

A column refined towards the surface (ten layers of 0.1 m above ten of 1 m)
with a uniform diffusivity of 1e-4 m2/s is run with the explicit scheme at the
step it reports as stable. Diffusion obeys a maximum principle, so the
temperatures must stay within the initial range [4, 20]. A fix may also raise
ValueError for an unstable step.
"""

from _common import failed, passed, setup

setup()
from limno.column import LakeColumn  # noqa: E402

thicknesses = [0.1] * 10 + [1.0] * 10
column = LakeColumn(thicknesses, [1e-4] * 19, [20.0 if i % 2 == 0 else 4.0 for i in range(20)])
dt = column.max_stable_step()
try:
    for _ in range(50):
        column.explicit_step(dt)
except ValueError as error:
    passed(f"unstable step rejected ({error})")
low, high = min(column.temperatures), max(column.temperatures)
if low < 4.0 - 1e-9 or high > 20.0 + 1e-9:
    failed(f"after 50 explicit steps of {dt:.0f} s temperatures span [{low:.4g}, {high:.4g}] C; initial range [4, 20]")
passed(f"temperatures within [{low:.3f}, {high:.3f}] with step {dt:.1f} s")
