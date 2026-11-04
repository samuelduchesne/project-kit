"""Reproduction check for py-richardson-order.

Usage: python3 py-richardson-order.py REPO

Refines the forward-difference derivative of exp at 0 with h = 0.1. The forward
difference is first order, so one Richardson step must reduce the error to
O(h**2), below 2e-3; the true derivative is 1.
Exit status: 0 when the refined derivative is within 2e-3 of 1, 1 when the
wrong output is reproduced, 2 on a usage error.
"""

import math
import sys
from pathlib import Path

TOLERANCE = 2e-3


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    sys.path.insert(0, str(Path(sys.argv[1]) / "src"))
    from sci.core.extrapolate import refined_derivative

    value = refined_derivative(math.exp, 0.0, 0.1)
    if abs(value - 1.0) > TOLERANCE:
        print(f"FAIL: refined derivative {value!r}; expected 1 within {TOLERANCE}")
        return 1
    print(f"PASS: refined derivative {value!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
