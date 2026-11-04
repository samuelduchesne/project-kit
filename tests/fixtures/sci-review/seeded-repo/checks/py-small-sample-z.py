"""Reproduction check for py-small-sample-z.

Usage: python3 py-small-sample-z.py REPO

The 95% interval of the mean of [9.8, 10.4, 10.1, 9.7] (n = 4, variance
unknown) uses Student's t with 3 degrees of freedom, t = 3.1824, so its
half-width is 0.5032.
Exit status: 0 when the half-width is 0.5032 within 1e-3, 1 when the wrong
output is reproduced, 2 on a usage error.
"""

import sys
from pathlib import Path

EXPECTED_HALF = 0.5031889427942914


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    sys.path.insert(0, str(Path(sys.argv[1]) / "src"))
    from sci.analysis.intervals import mean_interval

    low, high = mean_interval([9.8, 10.4, 10.1, 9.7])
    half = (high - low) / 2
    if abs(half - EXPECTED_HALF) > 1e-3:
        print(f"FAIL: half-width {half!r}; expected {EXPECTED_HALF!r}")
        return 1
    print(f"PASS: half-width {half!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
