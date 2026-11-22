"""Reproduction check for py-implicit-diagonal-reuse.

With no surface flux and an insulated bed, backward Euler conserves the heat
content of the column exactly (up to rounding), however many steps are run.
"""

from _common import failed, passed, setup

setup()
from limno.column import LakeColumn  # noqa: E402

column = LakeColumn([1.0] * 6, [1e-4] * 5, [20.0, 18.0, 12.0, 8.0, 6.0, 5.0])
before = column.heat_content()
column.run_implicit(3600.0, [0.0] * 5)
after = column.heat_content()
if abs(after - before) > 1e-9 * abs(before):
    failed(f"heat content {before:.6e} J/m2 becomes {after:.6e} J/m2 after five insulated implicit steps")
passed(f"heat content conserved ({after:.6e} J/m2)")
