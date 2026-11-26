"""Build the practical fixture repository used to validate spec 010 of sci-review.

Usage:
    python3 build.py --out DIR     create the git repository at DIR
    python3 build.py --check       verify manifest.json against the embedded sources only

The fixture checks what spec 010 adds, not recall: whether findings say who hits them. It holds three cases,
each beside a correct look-alike, in a small results service whose settings come from the environment:

- ``stale-config-cache``: a results cache keyed on the inputs but not on the search configuration, which
  differs only between deployments (``.env`` against the defaults in ``settings.py``). Expected: severity at
  most ``medium``, trigger class ``operator-change`` or ``release`` (SC-002).
- ``frozen-report``: a report lookup that ignores the stored schema version, with nothing saying whether that
  is deliberate. Expected: reported under "Design questions" (SC-003).
- ``quoted-setting``: a defect whose obvious reproduction quotes the development setting from a docstring
  (``SEARCH_GENERATIONS=5``) that ``.env`` contradicts (``10``). Expected: no report repeats the wrong value
  without a correction (SC-004).

``main`` holds the baseline; ``feature`` adds the modules under review. The repository is left on ``feature``
with no remote, so ``panel.py scope --mode branch`` resolves ``main`` as the base. Names are invented. Each
manifest entry is located by ``anchor``, a substring on exactly one line of its file; every build verifies them.
Only the Python standard library is used.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "manifest.json"
GIT_IDENTITY = ("-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false")
COMMIT_DATES = ("2026-02-02T10:00:00+00:00", "2026-02-09T14:30:00+00:00")

README = """\
# results-service

Computes and serves optimised retrofit results for buildings. Each deployment (development, staging,
production) runs its own service with its own results store; settings come from the environment.

- `src/results/settings.py`: settings and their defaults.
- `src/results/`: the search, the results cache and the report store.
"""

ENV = """\
# Development settings. Production uses the defaults in src/results/settings.py.
SEARCH_POPULATION=200
SEARCH_GENERATIONS=10
"""

SETTINGS = '''\
"""Service settings, read once from the environment at start-up."""

import os

SEARCH_POPULATION = int(os.environ.get("SEARCH_POPULATION", "10000"))
SEARCH_GENERATIONS = int(os.environ.get("SEARCH_GENERATIONS", "100"))
REPORT_SCHEMA_VERSION = 3
'''

INIT = '"""Results service."""\n'

SEARCH = '''\
"""Evolutionary search for the best retrofit plan of a building.

Development runs use SEARCH_GENERATIONS=5 so that a search finishes in seconds on a laptop.
"""

from __future__ import annotations

import random
from collections.abc import Callable, Sequence

from results import settings


def improvement_rate(history: Sequence[float], generations: int) -> float:
    """Mean improvement per generation over the last tenth of the run."""
    window = generations // 10
    recent = history[-window - 1 :]
    return (recent[-1] - recent[0]) / window


def search(score: Callable[[int], float], seed: int = 7) -> tuple[int, float]:
    """The best candidate found and its score, with the configured population and generations."""
    rng = random.Random(seed)
    generations = settings.SEARCH_GENERATIONS
    best, best_score, history = 0, float("-inf"), []
    for _ in range(generations):
        for _ in range(settings.SEARCH_POPULATION // 100):
            candidate = rng.randrange(1_000_000)
            value = score(candidate)
            if value > best_score:
                best, best_score = candidate, value
        history.append(best_score)
    if improvement_rate(history, generations) > 0.01:
        raise RuntimeError("search did not converge")
    return best, best_score
'''

CACHE = '''\
"""Cache of search results, so that an unchanged building is not searched again."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from typing import Any

from results import search as search_module
from results import settings

_results: dict[str, tuple[int, float]] = {}
_rates: dict[tuple[str, int], float] = {}


def inputs_key(inputs: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()


def best_plan(inputs: dict[str, Any], score: Callable[[int], float]) -> tuple[int, float]:
    """The best plan for these building inputs, searched once and then served from the cache."""
    key = inputs_key(inputs)
    if key not in _results:
        _results[key] = search_module.search(score)
    return _results[key]


def tariff_rate(region: str, year: int, table: Callable[[str, int], float]) -> float:
    """The electricity tariff of a region in a year, cached on both."""
    if (region, year) not in _rates:
        _rates[(region, year)] = table(region, year)
    return _rates[(region, year)]


def search_settings() -> dict[str, int]:
    return {"population": settings.SEARCH_POPULATION, "generations": settings.SEARCH_GENERATIONS}
'''

REPORTS = '''\
"""Store of building reports that users download."""

from __future__ import annotations

from typing import Any

from results import settings

_store: dict[str, dict[str, Any]] = {}


def save_report(building_id: str, body: dict[str, Any]) -> None:
    _store[building_id] = {"schema_version": settings.REPORT_SCHEMA_VERSION, "body": body}


def issued_report(building_id: str) -> dict[str, Any]:
    """The report as issued for this building."""
    return _store[building_id]["body"]


def current_summary(building_id: str, rebuild: Any) -> dict[str, Any]:
    """The dashboard summary, rebuilt when it was stored under an older schema."""
    record = _store[building_id]
    if record["schema_version"] != settings.REPORT_SCHEMA_VERSION:
        record = {"schema_version": settings.REPORT_SCHEMA_VERSION, "body": rebuild(building_id)}
        _store[building_id] = record
    return record["body"]
'''

BASE = {
    "README.md": README,
    ".env": ENV,
    "src/results/__init__.py": INIT,
    "src/results/settings.py": SETTINGS,
}
FEATURE = {
    "src/results/search.py": SEARCH,
    "src/results/cache.py": CACHE,
    "src/results/reports.py": REPORTS,
}


def feature_tree() -> dict[str, str]:
    return {**BASE, **FEATURE}


def verify_manifest(manifest_path: Path) -> list[str]:
    problems = []
    tree = feature_tree()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    for group in ("cases", "lookalikes"):
        for entry in data[group]:
            text = tree.get(entry["file"])
            if text is None:
                problems.append(f"{entry['id']}: no file {entry['file']}")
                continue
            lines = [i + 1 for i, line in enumerate(text.splitlines()) if entry["anchor"] in line]
            if len(lines) != 1:
                problems.append(f"{entry['id']}: anchor occurs on {len(lines)} lines of {entry['file']}")
            elif lines[0] != entry["line"]:
                problems.append(f"{entry['id']}: anchor is on line {lines[0]}, manifest says {entry['line']}")
    return problems


def git(repo: Path, *args: str, date: str = COMMIT_DATES[0]) -> None:
    env = {**os.environ, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
    subprocess.run(["git", *GIT_IDENTITY, *args], cwd=repo, check=True, capture_output=True, env=env)


def write(repo: Path, files: dict[str, str]) -> None:
    for relative, text in files.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def build(out: Path) -> None:
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"{out} exists and is not empty")
    out.mkdir(parents=True, exist_ok=True)
    git(out, "init", "-q", "-b", "main")
    write(out, BASE)
    git(out, "add", "-A")
    git(out, "commit", "-qm", "Baseline settings", date=COMMIT_DATES[0])
    git(out, "checkout", "-q", "-b", "feature")
    write(out, FEATURE)
    git(out, "add", "-A")
    git(out, "commit", "-qm", "Search, results cache and report store", date=COMMIT_DATES[1])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--out", type=Path, help="directory in which to create the repository")
    group.add_argument("--check", action="store_true", help="verify manifest.json only; create nothing")
    args = parser.parse_args(argv)
    problems = verify_manifest(MANIFEST)
    if problems:
        for problem in problems:
            print(f"manifest: {problem}", file=sys.stderr)
        return 1
    if args.check:
        print("manifest: every entry verified against the feature sources")
        return 0
    build(args.out.resolve())
    print(f"built {args.out} (branches main and feature; feature checked out)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
