"""Reproduction check for py-simpson-weights.

Usage: python3 py-simpson-weights.py REPO

Integrates the samples of x**2 on [0, 2] with ``sci.core.quadrature.simpson``.
Simpson's rule is exact for quadratics, so the correct result is 8/3.
Exit status: 0 when the result is correct, 1 when the wrong output is
reproduced, 2 on a usage error.
"""

import sys
from pathlib import Path

EXPECTED = 8.0 / 3.0


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    sys.path.insert(0, str(Path(sys.argv[1]) / "src"))
    from sci.core.quadrature import simpson

    result = simpson([0.0, 0.25, 1.0, 2.25, 4.0], 0.5)
    if abs(result - EXPECTED) > 1e-12:
        print(f"FAIL: simpson returned {result!r}; expected {EXPECTED!r}")
        return 1
    print(f"PASS: simpson returned {result!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
