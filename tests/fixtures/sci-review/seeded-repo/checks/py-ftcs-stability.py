"""Reproduction check for py-ftcs-stability.

Usage: python3 py-ftcs-stability.py REPO

Runs ``sci.core.heat.diffuse`` with alpha = 1e-4 m^2/s, dx = 0.01 m and
dt = 1.0 s (r = alpha * dt / dx**2 = 1.0, above the FTCS limit of 0.5) on a
unit spike at the centre of 101 nodes for 20 steps. The heat equation obeys a
maximum principle, so every value must stay within [0, 1].

The check accepts either correct behaviour of a fix: the call raises
ValueError because the step exceeds the stability limit, or it returns values
that respect the maximum principle (for example by sub-stepping or by an
implicit scheme).

Exit status: 0 when correct, 1 when the wrong output is reproduced, 2 on a
usage error.
"""

import sys
from pathlib import Path

TOLERANCE = 1e-9


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    sys.path.insert(0, str(Path(sys.argv[1]) / "src"))
    from sci.core.heat import diffuse

    u0 = [0.0] * 101
    u0[50] = 1.0
    try:
        u = diffuse(u0, 1e-4, 0.01, 1.0, 20)
    except ValueError as error:
        print(f"PASS: unstable step rejected ({error})")
        return 0
    high, low = max(u), min(u)
    if high > 1.0 + TOLERANCE or low < -TOLERANCE:
        print(f"FAIL: values range over [{low:.6g}, {high:.6g}]; the exact solution stays within [0, 1]")
        return 1
    print(f"PASS: values range over [{low:.6g}, {high:.6g}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
