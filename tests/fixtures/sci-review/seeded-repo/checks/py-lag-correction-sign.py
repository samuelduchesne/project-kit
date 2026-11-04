"""Reproduction check for py-lag-correction-sign.

Usage: python3 py-lag-correction-sign.py REPO

The air temperature rises at 1 K/s, T_air = t. A first-order sensor with
tau = 5 s then reads T_s = t - 5 once the transient has decayed. Correcting
those readings (dt = 1 s) must recover T_air = 10 at t = 10.
Exit status: 0 when the corrected value is 10, 1 when the wrong output is
reproduced, 2 on a usage error.
"""

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    sys.path.insert(0, str(Path(sys.argv[1]) / "src"))
    from sci.core.sensor import lag_corrected

    readings = [t - 5.0 for t in range(20)]
    value = lag_corrected(readings, dt=1.0, tau=5.0)[10]
    if abs(value - 10.0) > 1e-9:
        print(f"FAIL: corrected temperature at t = 10 is {value!r}; expected 10.0")
        return 1
    print(f"PASS: corrected temperature at t = 10 is {value!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
