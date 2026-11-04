"""Reproduction check for py-onepass-variance.

Usage: python3 py-onepass-variance.py REPO

Computes the moments of [1e9 + 1, 1e9 + 2, 1e9 + 3] with
``sci.core.numerics.moments``. The population variance is 2/3.
Exit status: 0 when the variance and standard deviation are correct, 1 when the
wrong output is reproduced, 2 on a usage error.
"""

import math
import sys
from pathlib import Path

EXPECTED = 2.0 / 3.0


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    sys.path.insert(0, str(Path(sys.argv[1]) / "src"))
    from sci.core.numerics import moments

    result = moments(iter([1e9 + 1.0, 1e9 + 2.0, 1e9 + 3.0]))
    if abs(result.variance - EXPECTED) > 1e-9:
        print(f"FAIL: variance {result.variance!r}; expected {EXPECTED!r}")
        return 1
    try:
        std = result.std
    except ValueError as error:
        print(f"FAIL: std raised {error!r}")
        return 1
    if abs(std - math.sqrt(EXPECTED)) > 1e-9:
        print(f"FAIL: std {std!r}; expected {math.sqrt(EXPECTED)!r}")
        return 1
    print(f"PASS: variance {result.variance!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
