"""Shared helpers for the Python reproduction checks of the hard fixture.

Every check is run as ``python3 CHECK REPO``. Exit status: 0 when the code
behaves correctly, 1 when the wrong output is reproduced, 2 on a usage error.
"""

import sys
from pathlib import Path


def setup() -> None:
    """Put REPO/src on the import path, or exit with status 2."""
    if len(sys.argv) != 2:
        print("usage: python3 CHECK REPO", file=sys.stderr)
        sys.exit(2)
    sys.path.insert(0, str(Path(sys.argv[1]).resolve() / "src"))


def passed(message: str) -> None:
    print(f"PASS: {message}")
    sys.exit(0)


def failed(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)
