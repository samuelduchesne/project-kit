"""Build the practical fixture repository used to validate spec 010 of sci-review.

Usage:
    python3 build.py --out DIR     create the git repository at DIR
    python3 build.py --check       verify manifest.json against the embedded sources only

The fixture checks what spec 010 adds, not recall: whether findings say who hits them. Results, reports and
tariffs live in a JSON store on disk that persists across processes and upgrades, so every case is reachable:

- ``stored-plan``: plans are stored under a key of the building inputs only. The search settings (which differ
  between deployments) and the search code (which changes in a release) are not in the key, so a plan computed
  before a release or a settings change is served afterwards. Expected: in practice names a release (SC-002).
- ``issued-report``: issued reports are served as stored, whatever schema they were written in, with nothing
  saying whether that is deliberate. Expected: a design question (SC-003).
- ``pound-lots``: offer bounds entered in pounds are converted to tonnes before whole-lot rounding, so about a
  fifth of whole-lot bounds round to the wrong lot. Expected: in practice names pounds or converted units (SC-008).
- ``quoted-setting``: the search's convergence window divides by zero below ten generations; its docstring quotes
  a development setting (5) that ``.env`` contradicts (10) (SC-004).

Each has a correct look-alike. ``main`` holds the baseline; ``feature`` adds the modules under review. Names are
invented. Each manifest entry is located by ``anchor``, a substring on exactly one line of its file.
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

Computes and serves optimised retrofit plans, carbon-credit purchases and reports for buildings. Each deployment
(development, staging, production) runs its own service with its own store file; settings come from the
environment. The store persists across restarts and upgrades.

Users enter carbon-credit offers in pounds, kilograms or tonnes of CO2e; quantities are converted to tonnes on entry.

- `src/results/settings.py`: settings and their defaults.
- `src/results/store.py`: the JSON store on disk.
- `src/results/`: the search, the plan cache, the report store and credit purchasing.
"""

ENV = """\
# Development settings. Production uses the defaults in src/results/settings.py.
SEARCH_POPULATION=20
SEARCH_GENERATIONS=10
STORE_PATH=var/store.json
"""

SETTINGS = '''\
"""Service settings, read once from the environment at start-up."""

import os

SEARCH_POPULATION = int(os.environ.get("SEARCH_POPULATION", "100"))
SEARCH_GENERATIONS = int(os.environ.get("SEARCH_GENERATIONS", "100"))
STORE_PATH = os.environ.get("STORE_PATH", "/var/lib/results/store.json")
REPORT_SCHEMA_VERSION = 3
'''

STORE = '''\
"""A JSON store on disk, shared by every process of a deployment and kept across upgrades."""

from __future__ import annotations

import json
import os
from typing import Any

from results import settings


def load(table: str) -> dict[str, Any]:
    if not os.path.exists(settings.STORE_PATH):
        return {}
    with open(settings.STORE_PATH, encoding="utf-8") as handle:
        return json.load(handle).get(table, {})


def save(table: str, rows: dict[str, Any]) -> None:
    data: dict[str, Any] = {}
    if os.path.exists(settings.STORE_PATH):
        with open(settings.STORE_PATH, encoding="utf-8") as handle:
            data = json.load(handle)
    data[table] = rows
    os.makedirs(os.path.dirname(settings.STORE_PATH) or ".", exist_ok=True)
    with open(settings.STORE_PATH, "w", encoding="utf-8") as handle:
        json.dump(data, handle)
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
        for _ in range(settings.SEARCH_POPULATION):
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
"""Plans already searched, kept in the store so that an unchanged building is not searched again."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from typing import Any

from results import search as search_module
from results import store


def inputs_key(inputs: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()


def best_plan(inputs: dict[str, Any], score: Callable[[int], float]) -> tuple[int, float]:
    """The best plan for these building inputs (which include the scoring objective), searched once."""
    plans = store.load("plans")
    key = inputs_key(inputs)
    if key not in plans:
        plans[key] = list(search_module.search(score))
        store.save("plans", plans)
    best, score_value = plans[key]
    return best, score_value


def tariff(region: str, year: int, table_version: str, table: Callable[[str, int], float]) -> float:
    """The electricity tariff of a region in a year from a published, immutable table version."""
    rates = store.load("tariffs")
    key = f"{region}/{year}/{table_version}"
    if key not in rates:
        rates[key] = table(region, year)
        store.save("tariffs", rates)
    return rates[key]
'''

REPORTS = '''\
"""Reports that users download, and the dashboard summary built from the latest data."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from results import settings, store


def save_report(building_id: str, body: dict[str, Any]) -> None:
    reports = store.load("reports")
    reports[building_id] = {"schema_version": settings.REPORT_SCHEMA_VERSION, "body": body}
    store.save("reports", reports)


def issued_report(building_id: str) -> dict[str, Any]:
    """The report issued for this building."""
    return store.load("reports")[building_id]["body"]


def dashboard_summary(building_id: str, rebuild: Callable[[str], dict[str, Any]]) -> dict[str, Any]:
    """The dashboard summary, rebuilt when it was stored under an older schema."""
    summaries = store.load("summaries")
    record = summaries.get(building_id)
    if record is None or record["schema_version"] != settings.REPORT_SCHEMA_VERSION:
        record = {"schema_version": settings.REPORT_SCHEMA_VERSION, "body": rebuild(building_id)}
        summaries[building_id] = record
        store.save("summaries", summaries)
    return record["body"]
'''

CREDITS = '''\
"""Carbon-credit offers sold in whole lots, with quantities converted to tonnes of CO2e on entry."""

from __future__ import annotations

import math

TONNES_PER_UNIT = {"t": 1.0, "kg": 0.001, "lb": 0.00045359237}


def to_tonnes(quantity: float, unit: str) -> float:
    return quantity * TONNES_PER_UNIT[unit]


def lot_bounds(minimum: float, maximum: float, step: float, unit: str) -> tuple[int, int]:
    """The fewest and the most whole lots a buyer may purchase from an offer."""
    low, high, lot = to_tonnes(minimum, unit), to_tonnes(maximum, unit), to_tonnes(step, unit)
    first = max(math.ceil(low / lot), 1)
    last = math.floor(high / lot)
    return first, last


def purchasable(minimum: float, maximum: float, step: float, unit: str) -> bool:
    first, last = lot_bounds(minimum, maximum, step, unit)
    return last >= first


def whole_tonnes(quantity: float, unit: str) -> int:
    """Tonnes of CO2e rounded to the nearest whole tonne, for display."""
    return round(to_tonnes(quantity, unit))
'''

BASE = {
    "README.md": README,
    ".env": ENV,
    "src/results/__init__.py": INIT,
    "src/results/settings.py": SETTINGS,
    "src/results/store.py": STORE,
}
FEATURE = {
    "src/results/search.py": SEARCH,
    "src/results/cache.py": CACHE,
    "src/results/reports.py": REPORTS,
    "src/results/credits.py": CREDITS,
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
    git(out, "commit", "-qm", "Baseline settings and store", date=COMMIT_DATES[0])
    git(out, "checkout", "-q", "-b", "feature")
    write(out, FEATURE)
    git(out, "add", "-A")
    git(out, "commit", "-qm", "Search, plan cache, report store and credit lots", date=COMMIT_DATES[1])


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
