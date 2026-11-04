"""Reproduction check for py-scaler-before-split.

Usage: python3 py-scaler-before-split.py REPO

Calls ``sci.analysis.preprocess.standardise_split([1, 2, 3, 4, 100], 0.2)``.
Without leakage, the mean and standard deviation come from the training part
[1, 2, 3, 4] only, and the test value is transformed with those parameters.
The check accepts the population or the sample standard deviation of the
training part.

Exit status: 0 when correct, 1 when the wrong output is reproduced, 2 on a
usage error.
"""

import statistics
import sys
from pathlib import Path

VALUES = [1.0, 2.0, 3.0, 4.0, 100.0]
TRAIN = VALUES[:4]


def expected(std: float) -> tuple[list[float], list[float]]:
    mean = statistics.fmean(TRAIN)
    return [(v - mean) / std for v in TRAIN], [(VALUES[4] - mean) / std]


def close(a: list[float], b: list[float]) -> bool:
    return len(a) == len(b) and all(abs(x - y) <= 1e-9 for x, y in zip(a, b))


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    sys.path.insert(0, str(Path(sys.argv[1]) / "src"))
    from sci.analysis.preprocess import standardise_split

    train, test = standardise_split(VALUES, 0.2)
    for std in (statistics.pstdev(TRAIN), statistics.stdev(TRAIN)):
        want_train, want_test = expected(std)
        if close(list(train), want_train) and close(list(test), want_test):
            print(f"PASS: first training value {train[0]!r}")
            return 0
    want_train, _ = expected(statistics.pstdev(TRAIN))
    print(f"FAIL: first training value {train[0]!r}; expected {want_train[0]!r} from training statistics only")
    return 1


if __name__ == "__main__":
    sys.exit(main())
