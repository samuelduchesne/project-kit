"""Score a sci-review report against the seeded fixture manifest.

Usage:
    python3 score.py REPORT [--manifest PATH] [--run DIR] [--domain-perspective ID]
                     [--verify-fixes REPO]
    python3 score.py --verify-fixes REPO

A finding matches a seeded defect when its file equals the defect's file and the
defect's line lies within ``match_tolerance`` (three) lines of the finding range,
that is in [line_start - 3, line_end + 3]. The contested construct carries a
range [line, line_end]; a finding matches it when the two ranges, widened by the
tolerance, overlap. A finding reports a look-alike only when its own range
overlaps the look-alike's range with no tolerance, so that a finding about
adjacent code is not counted against the look-alike.

An independent-round candidate is credited with the seeded defect of the merged
finding that absorbed it, as recorded in ``merge/batch-*.json``: the moderator
confirmed that every member of a merged finding describes the same defect, so a
candidate whose own lines lie outside the tolerance is neither a miss nor a
false positive when its merged finding matches the defect.

Criteria printed, each with a final PASS, FAIL or SKIP line:

    SC-001  recall of seeded defects: at least 90% overall, and at least one
            detection per dimension and per language
    SC-002  no finding at a designated look-alike
    SC-003  every finding carries the FR-014 fields
    SC-010  the contested construct is labelled contested with both arguments
            and a deciding assumption
    SC-008  (--run) the panel detects more seeded defects than the best single
            perspective in the independent round, or as many with fewer false
            positives
    SC-009  (--run) at least half of the independent-round false positives are
            rejected in debate or never reported
    SC-012  (--domain-perspective ID) at least 90% of the seeded defects are
            reported by a finding that lists ID among its raisers

Two manifest formats are read: this fixture's (``defects``, ``lookalikes`` and
``contested`` lists) and the entry format of the idfkit building-energy fixture
(one ``entries`` list whose items carry ``kind``: ``defect``, ``lookalike`` or
``contested``). Entries without a ``dimension`` are left out of the
per-dimension recall; their languages are reported as found.

``--verify-fixes REPO`` runs every reproduction check listed in the manifest
against REPO and prints which pass (SC-007). Python checks run with this
interpreter; TypeScript checks run with ``node --experimental-strip-types``
(Node 22.6 or later).

The exit status is 0 whatever the verdicts, and 2 when an input cannot be read.
Only the Python standard library is used.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "manifest.json"
EXIT_OK = 0
EXIT_UNREADABLE = 2
RECALL_THRESHOLD = 0.90
SC009_THRESHOLD = 0.5
SC012_THRESHOLD = 0.90
CHECK_TIMEOUT_S = 120
DIMENSIONS = (
    "mathematical-derivations",
    "numerical-stability",
    "physical-modelling-and-units",
    "statistical-integrity",
    "algorithmic-correctness",
)
LANGUAGES = ("python", "typescript")
CONCRETE_LABELS = ("consensus", "majority")


class UnreadableInput(Exception):
    """An input file is missing or is not valid JSON of the expected shape."""


# ---------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Defect:
    id: str
    file: str
    line: int
    dimension: str | None
    language: str
    severity: str | None
    description: str
    reproduce: str | None


@dataclass(frozen=True)
class RangedEntry:
    """A look-alike or the contested construct: a range of lines in one file."""

    id: str
    file: str
    line: int
    line_end: int
    description: str
    expected_label: str | None = None
    expected_deciding_assumption: str | None = None


@dataclass(frozen=True)
class Manifest:
    tolerance: int
    defects: tuple[Defect, ...]
    lookalikes: tuple[RangedEntry, ...]
    contested: tuple[RangedEntry, ...]


@dataclass(frozen=True)
class Location:
    """A file and an inclusive line range taken from a finding."""

    file: str
    line_start: int
    line_end: int


@dataclass(frozen=True)
class ReportFinding:
    """A reported finding; fields are None when absent from the report."""

    id: str
    location: Location | None
    dimension: str | None
    severity: str | None
    summary: str | None
    trigger: str | None
    wrong_output: str | None
    fix: str | None
    raised_by: tuple[str, ...]
    label: str | None
    argument_for: str | None
    argument_against: str | None
    deciding_assumption: str | None
    no_trigger_reason: str | None
    has_trigger_key: bool
    has_wrong_output_key: bool


@dataclass(frozen=True)
class Report:
    findings: tuple[ReportFinding, ...]
    rejected_ids: frozenset[str]


@dataclass(frozen=True)
class Candidate:
    """An independent-round finding of one perspective."""

    id: str
    perspective: str
    location: Location | None
    merged_into: str | None = None


@dataclass
class PerspectiveScore:
    perspective: str
    detected: set[str] = field(default_factory=set)
    false_positives: int = 0
    findings: int = 0


@dataclass(frozen=True)
class Verdict:
    criterion: str
    status: str
    detail: str


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise UnreadableInput(f"cannot read {path}: {error}") from error


def text_or_none(value: object) -> str | None:
    """Return ``value`` when it is a non-blank string, otherwise None."""
    return value if isinstance(value, str) and value.strip() else None


def normalise_path(path: str) -> str:
    path = path.replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    return path


def defect_entry(raw: dict[str, Any]) -> Defect:
    return Defect(
        id=raw["id"],
        file=normalise_path(raw["file"]),
        line=int(raw["line"]),
        dimension=raw.get("dimension"),
        language=raw["language"],
        severity=raw.get("severity"),
        description=raw["description"],
        reproduce=raw.get("reproduce"),
    )


def load_manifest(path: Path) -> Manifest:
    data = read_json(path)
    try:
        if isinstance(data, dict) and "entries" in data:
            # The idfkit building-energy fixture: one list of entries, each with a kind.
            kinds = ("defect", "lookalike", "contested")
            unknown = sorted({str(raw.get("kind")) for raw in data["entries"] if raw.get("kind") not in kinds})
            if unknown:
                raise ValueError(f"unknown entry kind(s): {', '.join(unknown)}")
            defects = tuple(defect_entry(raw) for raw in data["entries"] if raw["kind"] == "defect")
            lookalikes = tuple(ranged_entry(raw) for raw in data["entries"] if raw["kind"] == "lookalike")
            contested = tuple(ranged_entry(raw) for raw in data["entries"] if raw["kind"] == "contested")
        else:
            defects = tuple(defect_entry(raw) for raw in data["defects"])
            lookalikes = tuple(ranged_entry(raw) for raw in data["lookalikes"])
            contested = tuple(ranged_entry(raw) for raw in data["contested"])
        tolerance = int(data.get("match_tolerance", 3))
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        raise UnreadableInput(f"{path} is not a valid manifest: {error!r}") from error
    return Manifest(tolerance, defects, lookalikes, contested)


def ranged_entry(raw: dict[str, Any]) -> RangedEntry:
    line = int(raw["line"])
    return RangedEntry(
        id=raw["id"],
        file=normalise_path(raw["file"]),
        line=line,
        line_end=int(raw.get("line_end", line)),
        description=raw["description"],
        expected_label=raw.get("expected_label"),
        expected_deciding_assumption=raw.get("expected_deciding_assumption"),
    )


def location_of(raw: dict[str, Any]) -> Location | None:
    file = raw.get("file")
    start = raw.get("line_start")
    if not isinstance(file, str) or not isinstance(start, int):
        return None
    end = raw.get("line_end")
    return Location(normalise_path(file), start, end if isinstance(end, int) and end >= start else start)


def load_report(path: Path) -> Report:
    data = read_json(path)
    if not isinstance(data, dict) or not isinstance(data.get("findings"), list):
        raise UnreadableInput(f"{path} has no findings list")
    findings: list[ReportFinding] = []
    for index, raw in enumerate(data["findings"], start=1):
        if not isinstance(raw, dict):
            raise UnreadableInput(f"{path}: finding {index} is not an object")
        raised = raw.get("raised_by")
        findings.append(
            ReportFinding(
                id=str(raw.get("id", f"#{index}")),
                location=location_of(raw),
                dimension=text_or_none(raw.get("dimension")),
                severity=text_or_none(raw.get("severity")),
                summary=text_or_none(raw.get("summary")),
                trigger=text_or_none(raw.get("trigger")),
                wrong_output=text_or_none(raw.get("wrong_output")),
                fix=text_or_none(raw.get("fix")),
                raised_by=tuple(r for r in raised if isinstance(r, str)) if isinstance(raised, list) else (),
                label=text_or_none(raw.get("label")),
                argument_for=text_or_none(raw.get("argument_for")),
                argument_against=text_or_none(raw.get("argument_against")),
                deciding_assumption=text_or_none(raw.get("deciding_assumption")),
                no_trigger_reason=text_or_none(raw.get("no_trigger_reason")),
                has_trigger_key="trigger" in raw,
                has_wrong_output_key="wrong_output" in raw,
            )
        )
    rejected = data.get("rejected", [])
    rejected_ids = frozenset(str(r["finding_id"]) for r in rejected if isinstance(r, dict) and "finding_id" in r)
    return Report(tuple(findings), rejected_ids)


def load_candidates(run: Path) -> tuple[Candidate, ...]:
    owner = load_merge_members(run)
    candidates: list[Candidate] = []
    for path in sorted((run / "candidates").glob("*.json")):
        data = read_json(path)
        if not isinstance(data, dict) or not isinstance(data.get("findings"), list):
            raise UnreadableInput(f"{path} has no findings list")
        perspective = str(data.get("perspective", path.stem))
        for raw in data["findings"]:
            if isinstance(raw, dict):
                cid = str(raw.get("id", ""))
                candidates.append(Candidate(cid, perspective, location_of(raw), owner.get(cid)))
    return tuple(candidates)


def load_merge_members(run: Path) -> dict[str, str]:
    """Map each candidate id to the merged finding id that absorbed it."""
    owner: dict[str, str] = {}
    for path in sorted((run / "merge").glob("batch-*.json")):
        data = read_json(path)
        for merged in data.get("findings", []) if isinstance(data, dict) else []:
            if not isinstance(merged, dict):
                continue
            for member in merged.get("members", []):
                owner[str(member)] = str(merged.get("id", ""))
    return owner


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------


def matches_line(location: Location | None, file: str, line: int, tolerance: int) -> bool:
    if location is None or location.file != file:
        return False
    return location.line_start - tolerance <= line <= location.line_end + tolerance


def matches_range(location: Location | None, entry: RangedEntry, tolerance: int) -> bool:
    if location is None or location.file != entry.file:
        return False
    return location.line_start - tolerance <= entry.line_end and entry.line <= location.line_end + tolerance


def detected_defects(locations: Iterable[Location | None], manifest: Manifest) -> set[str]:
    found: set[str] = set()
    for location in locations:
        for defect in manifest.defects:
            if matches_line(location, defect.file, defect.line, manifest.tolerance):
                found.add(defect.id)
    return found


def is_false_positive(location: Location | None, manifest: Manifest) -> bool:
    """True when a location matches neither a seeded defect nor the contested construct."""
    if any(matches_line(location, d.file, d.line, manifest.tolerance) for d in manifest.defects):
        return False
    return not any(matches_range(location, c, manifest.tolerance) for c in manifest.contested)


def candidate_locations(candidate: Candidate, report: Report) -> list[Location | None]:
    """The candidate's own location and that of the reported finding that absorbed it, if any."""
    merged = [
        f.location for f in report.findings if candidate.merged_into is not None and f.id == candidate.merged_into
    ]
    return [candidate.location, *merged]


def candidate_is_false_positive(candidate: Candidate, report: Report, manifest: Manifest) -> bool:
    return all(is_false_positive(location, manifest) for location in candidate_locations(candidate, report))


def percent(numerator: int, denominator: int) -> str:
    return f"{100.0 * numerator / denominator:.0f}%" if denominator else "n/a"


# ---------------------------------------------------------------------------
# Criteria
# ---------------------------------------------------------------------------


def score_recall(report: Report, manifest: Manifest) -> Verdict:
    print("SC-001 Recall of seeded defects")
    found = detected_defects((f.location for f in report.findings), manifest)
    for defect in manifest.defects:
        ids = [f.id for f in report.findings if matches_line(f.location, defect.file, defect.line, manifest.tolerance)]
        status = f"detected by {', '.join(ids)}" if ids else "missed"
        print(f"  {defect.id:<28} {defect.file}:{defect.line:<5} {status}")
    total = len(manifest.defects)
    print(f"  overall: {len(found)}/{total} ({percent(len(found), total)})")
    gaps: list[str] = []
    languages = tuple(dict.fromkeys((*LANGUAGES, *(d.language for d in manifest.defects))))
    dimensions = DIMENSIONS if any(d.dimension for d in manifest.defects) else ()
    for title, key, values in (
        ("dimension", lambda d: d.dimension, dimensions),
        ("language", lambda d: d.language, languages),
    ):
        for value in values:
            members = [d for d in manifest.defects if key(d) == value]
            hits = sum(1 for d in members if d.id in found)
            print(f"  {title} {value}: {hits}/{len(members)} ({percent(hits, len(members))})")
            if members and hits == 0:
                gaps.append(value)
    ok = total > 0 and len(found) / total >= RECALL_THRESHOLD and not gaps
    detail = f"{len(found)}/{total} detected" + (f"; none detected for {', '.join(gaps)}" if gaps else "")
    return Verdict("SC-001", "PASS" if ok else "FAIL", detail)


def score_lookalikes(report: Report, manifest: Manifest) -> Verdict:
    print("SC-002 Findings at designated look-alikes")
    count = 0
    for entry in manifest.lookalikes:
        # A look-alike is reported only by a finding whose own lines overlap it; a finding that also matches a
        # seeded defect is a detection, not a report of the look-alike.
        ids = [
            f.id
            for f in report.findings
            if matches_range(f.location, entry, 0) and is_false_positive(f.location, manifest)
        ]
        count += len(ids)
        status = f"reported as {', '.join(ids)}" if ids else "not reported"
        print(f"  {entry.id:<28} {entry.file}:{entry.line}-{entry.line_end} {status}")
    return Verdict("SC-002", "PASS" if count == 0 else "FAIL", f"{count} false positive(s) at look-alikes")


def missing_fields(finding: ReportFinding) -> list[str]:
    missing: list[str] = []
    if finding.location is None:
        missing.append("file/line_start")
    for name in ("dimension", "severity", "summary", "fix", "label"):
        if getattr(finding, name) is None:
            missing.append(name)
    if not finding.raised_by:
        missing.append("raised_by")
    if not finding.has_trigger_key:
        missing.append("trigger")
    if not finding.has_wrong_output_key:
        missing.append("wrong_output")
    concrete = finding.trigger is not None and finding.wrong_output is not None
    if finding.label in CONCRETE_LABELS and not concrete:
        missing.append("trigger and wrong_output (required for consensus and majority)")
    elif not concrete and finding.no_trigger_reason is None:
        missing.append("no_trigger_reason (required when trigger or wrong_output is null)")
    if finding.label == "contested":
        for name in ("argument_for", "argument_against"):
            if getattr(finding, name) is None:
                missing.append(name)
    return missing


def score_fields(report: Report) -> Verdict:
    print("SC-003 FR-014 fields")
    incomplete = 0
    for finding in report.findings:
        missing = missing_fields(finding)
        if missing:
            incomplete += 1
            print(f"  {finding.id}: missing {', '.join(missing)}")
    total = len(report.findings)
    print(f"  complete: {total - incomplete}/{total}")
    return Verdict("SC-003", "PASS" if incomplete == 0 else "FAIL", f"{incomplete} incomplete finding(s) of {total}")


def score_contested(report: Report, manifest: Manifest) -> Verdict:
    print("SC-010 Contested construct")
    if not manifest.contested:
        print("  no contested construct in the manifest")
        return Verdict("SC-010", "SKIP", "no contested construct in the manifest")
    failures: list[str] = []
    for entry in manifest.contested:
        matched = [f for f in report.findings if matches_range(f.location, entry, manifest.tolerance)]
        print(f"  {entry.id} {entry.file}:{entry.line}-{entry.line_end}")
        print(f"    expected label: {entry.expected_label}")
        print(f"    expected deciding assumption: {entry.expected_deciding_assumption}")
        if not matched:
            print("    not reported")
            failures.append(f"{entry.id} not reported")
            continue
        good = False
        for finding in matched:
            present = {
                "argument_for": finding.argument_for is not None,
                "argument_against": finding.argument_against is not None,
                "deciding_assumption": finding.deciding_assumption is not None,
            }
            flags = ", ".join(f"{name} {'present' if ok else 'missing'}" for name, ok in present.items())
            print(f"    {finding.id}: label {finding.label}; {flags}")
            if finding.deciding_assumption is not None:
                print(f"      deciding assumption: {finding.deciding_assumption}")
            if finding.label == entry.expected_label and all(present.values()):
                good = True
        if not good:
            failures.append(f"{entry.id} not labelled {entry.expected_label} with both arguments and the assumption")
    detail = "; ".join(failures) if failures else "labelled contested with both arguments and the assumption"
    return Verdict("SC-010", "FAIL" if failures else "PASS", detail)


def score_perspectives(report: Report, manifest: Manifest, candidates: Sequence[Candidate]) -> Verdict:
    print("SC-008 Panel versus best single perspective (independent round)")
    scores: dict[str, PerspectiveScore] = {}
    for candidate in candidates:
        score = scores.setdefault(candidate.perspective, PerspectiveScore(candidate.perspective))
        score.findings += 1
        score.detected |= detected_defects(candidate_locations(candidate, report), manifest)
        if candidate_is_false_positive(candidate, report, manifest):
            score.false_positives += 1
    if not scores:
        print("  no candidate files found")
        return Verdict("SC-008", "SKIP", "no candidates/*.json in the run directory")
    total = len(manifest.defects)
    for score in sorted(scores.values(), key=lambda s: s.perspective):
        print(
            f"  {score.perspective:<24} {len(score.detected)}/{total} detected, "
            f"{score.false_positives} false positive(s) of {score.findings} finding(s)"
        )
    best = max(scores.values(), key=lambda s: (len(s.detected), -s.false_positives))
    panel_detected = detected_defects((f.location for f in report.findings), manifest)
    panel_fp = sum(1 for f in report.findings if is_false_positive(f.location, manifest))
    print(f"  {'panel':<24} {len(panel_detected)}/{total} detected, {panel_fp} false positive(s)")
    better = len(panel_detected) > len(best.detected)
    tie = len(panel_detected) == len(best.detected) and panel_fp < best.false_positives
    detail = (
        f"panel {len(panel_detected)} detected / {panel_fp} FP; best single ({best.perspective}) "
        f"{len(best.detected)} detected / {best.false_positives} FP"
    )
    return Verdict("SC-008", "PASS" if better or tie else "FAIL", detail)


def score_debate_rejections(report: Report, manifest: Manifest, run: Path, candidates: Sequence[Candidate]) -> Verdict:
    print("SC-009 Independent-round false positives rejected in debate")
    owner = load_merge_members(run)
    reported_ids = {f.id for f in report.findings}
    false_positives = [c for c in candidates if candidate_is_false_positive(c, report, manifest)]
    if not false_positives:
        print("  no independent-round false positives")
        return Verdict("SC-009", "PASS", "no independent-round false positives")
    removed = 0
    for candidate in false_positives:
        merged = owner.get(candidate.id)
        if merged is not None and merged in report.rejected_ids:
            fate, gone = f"rejected in debate as {merged}", True
        elif merged is not None and merged in reported_ids:
            fate, gone = f"reported as {merged}", False
        else:
            fate, gone = "never reported", True
        removed += int(gone)
        where = f"{candidate.location.file}:{candidate.location.line_start}" if candidate.location else "no location"
        print(f"  {candidate.id:<28} {where:<40} {fate}")
    total = len(false_positives)
    print(f"  removed: {removed}/{total} ({percent(removed, total)})")
    ok = removed / total >= SC009_THRESHOLD
    return Verdict("SC-009", "PASS" if ok else "FAIL", f"{removed}/{total} false positives removed")


def score_domain_attribution(report: Report, manifest: Manifest, perspective: str) -> Verdict:
    print(f"SC-012 Seeded defects reported with {perspective} among the raisers")
    attributed = 0
    for defect in manifest.defects:
        matched = [f for f in report.findings if matches_line(f.location, defect.file, defect.line, manifest.tolerance)]
        with_domain = [f.id for f in matched if perspective in f.raised_by]
        attributed += int(bool(with_domain))
        if with_domain:
            status = f"raised by {perspective} in {', '.join(with_domain)}"
        elif matched:
            status = f"reported as {', '.join(f.id for f in matched)} without {perspective}"
        else:
            status = "missed"
        print(f"  {defect.id:<34} {status}")
    total = len(manifest.defects)
    print(f"  attributed: {attributed}/{total} ({percent(attributed, total)})")
    ok = total > 0 and attributed / total >= SC012_THRESHOLD
    return Verdict("SC-012", "PASS" if ok else "FAIL", f"{attributed}/{total} reported with {perspective} as a raiser")


# ---------------------------------------------------------------------------
# Reproduction checks
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CheckResult:
    defect: str
    check: str
    exit_code: int | None
    output: str


def check_command(check: Path, repo: Path) -> list[str]:
    if check.suffix == ".mjs":
        return ["node", "--experimental-strip-types", "--disable-warning=ExperimentalWarning", str(check), str(repo)]
    return [sys.executable, str(check), str(repo)]


def run_check(defect: Defect, repo: Path) -> CheckResult:
    assert defect.reproduce is not None
    check = HERE / defect.reproduce
    if not check.is_file():
        return CheckResult(defect.id, defect.reproduce, None, "check file not found")
    try:
        done = subprocess.run(
            check_command(check, repo),
            capture_output=True,
            text=True,
            timeout=CHECK_TIMEOUT_S,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return CheckResult(defect.id, defect.reproduce, None, str(error))
    lines = (done.stdout.strip() or done.stderr.strip()).splitlines()
    return CheckResult(defect.id, defect.reproduce, done.returncode, lines[-1] if lines else "")


def verify_fixes(manifest: Manifest, repo: Path) -> None:
    print(f"SC-007 Reproduction checks against {repo}")
    results = [run_check(d, repo) for d in manifest.defects if d.reproduce]
    for result in results:
        if result.exit_code == 0:
            status = "pass   (fixed)"
        elif result.exit_code == 1:
            status = "fail   (failure reproduced)"
        else:
            status = f"error  (exit {result.exit_code})"
        print(f"  {result.defect:<28} {status:<28} {result.output}")
    passed = sum(1 for r in results if r.exit_code == 0)
    failed = sum(1 for r in results if r.exit_code == 1)
    errors = len(results) - passed - failed
    print(f"  checks: {passed} pass, {failed} fail, {errors} error, of {len(results)}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score a sci-review report against the seeded fixture manifest.")
    parser.add_argument("report", nargs="?", type=Path, help="report.json written by panel.py report")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST, help="fixture manifest")
    parser.add_argument("--run", type=Path, help="run directory with candidates/ and merge/ (SC-008, SC-009)")
    parser.add_argument(
        "--domain-perspective", metavar="ID", help="check that seeded defects are raised by this perspective (SC-012)"
    )
    parser.add_argument("--verify-fixes", type=Path, metavar="REPO", help="run every reproduction check against REPO")
    args = parser.parse_args(argv)
    if args.report is None and args.verify_fixes is None:
        parser.error("give a report, --verify-fixes REPO, or both")
    try:
        manifest = load_manifest(args.manifest)
        verdicts: list[Verdict] = []
        if args.report is not None:
            report = load_report(args.report)
            verdicts.append(score_recall(report, manifest))
            verdicts.append(score_lookalikes(report, manifest))
            verdicts.append(score_fields(report))
            verdicts.append(score_contested(report, manifest))
            if args.domain_perspective:
                verdicts.append(score_domain_attribution(report, manifest, args.domain_perspective))
            if args.run is not None:
                if not args.run.is_dir():
                    raise UnreadableInput(f"run directory {args.run} does not exist")
                candidates = load_candidates(args.run)
                verdicts.append(score_perspectives(report, manifest, candidates))
                verdicts.append(score_debate_rejections(report, manifest, args.run, candidates))
        if args.verify_fixes is not None:
            if not args.verify_fixes.is_dir():
                raise UnreadableInput(f"repository {args.verify_fixes} does not exist")
            verify_fixes(manifest, args.verify_fixes.resolve())
    except UnreadableInput as error:
        print(f"error: {error}", file=sys.stderr)
        return EXIT_UNREADABLE
    if verdicts:
        print("Verdicts")
        for verdict in verdicts:
            print(f"{verdict.criterion}: {verdict.status} ({verdict.detail})")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
