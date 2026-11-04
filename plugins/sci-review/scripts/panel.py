#!/usr/bin/env python3
"""Deterministic steps of the sci-review panel protocol.

Implements the subcommands of contracts/panel-cli.md: scope resolution,
extension selection, panel configuration, message validation, location
clustering and batching, adjudication of agreement labels, report rendering,
and run-directory management. Standard library only, Python 3.10 or later.

The script never writes inside the reviewed project. Every subcommand that
creates, writes or removes files accepts --dry-run. Exit codes: 0 success,
1 validation failure, 2 usage error, 3 precondition not met.
"""

from __future__ import annotations

import argparse
import dataclasses
import fnmatch
import json
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

if sys.version_info < (3, 10):
    print("panel.py requires Python 3.10 or later.", file=sys.stderr)
    sys.exit(3)

PLUGIN_DIR = Path(__file__).resolve().parents[1]
SKILL_DIR = PLUGIN_DIR / "skills" / "scientific-review"
SCHEMA_DIR = SKILL_DIR / "schemas"
ROLES_DIR = SKILL_DIR / "roles"

EXIT_OK = 0
EXIT_INVALID = 1
EXIT_USAGE = 2
EXIT_PRECONDITION = 3

CONTRACT_VERSION = 1
CLUSTER_DISTANCE = 3
SPLIT_ID_BLOCK = 1000
DEFAULT_BUDGET = 6000
MIN_PERSPECTIVES, MAX_PERSPECTIVES = 2, 7
MIN_ROUNDS, MAX_ROUNDS, DEFAULT_ROUNDS = 0, 3, 2
MIN_BATCHES, MAX_BATCHES, DEFAULT_BATCHES = 1, 4, 2
RUN_PREFIX = "sci-review-"
MEMBER_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")

REDUCED_INDEPENDENCE_NOTICE = (
    "The perspectives were not independent agents; agreement among them was reached within a single "
    "reviewer and is weaker evidence than in a parallel review."
)
NO_REVIEWABLE_CODE = "No reviewable scientific code changed in this scope."
NOT_REJECTED = "Not rejected."


class PanelError(Exception):
    """An error that maps to an exit code."""

    exit_code = EXIT_INVALID

    def __init__(self, message: str, details: Sequence[str] = ()) -> None:
        super().__init__(message)
        self.details = list(details)


class ValidationFailure(PanelError):
    exit_code = EXIT_INVALID


class UsageFailure(PanelError):
    exit_code = EXIT_USAGE


class PreconditionFailure(PanelError):
    exit_code = EXIT_PRECONDITION


# ---------------------------------------------------------------------------
# Enumerations (string constants validated on load)
# ---------------------------------------------------------------------------


class ScopeMode:
    BRANCH = "branch"
    EXPLICIT = "explicit"
    REPOSITORY = "repository"
    PATHS = "paths"
    VALUES = (BRANCH, EXPLICIT, REPOSITORY, PATHS)


class Dimension:
    MATHEMATICAL_DERIVATIONS = "mathematical-derivations"
    NUMERICAL_STABILITY = "numerical-stability"
    PHYSICAL_MODELLING_AND_UNITS = "physical-modelling-and-units"
    STATISTICAL_INTEGRITY = "statistical-integrity"
    ALGORITHMIC_CORRECTNESS = "algorithmic-correctness"
    VALUES = (
        MATHEMATICAL_DERIVATIONS,
        NUMERICAL_STABILITY,
        PHYSICAL_MODELLING_AND_UNITS,
        STATISTICAL_INTEGRITY,
        ALGORITHMIC_CORRECTNESS,
    )


class Severity:
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VALUES = (HIGH, MEDIUM, LOW)
    RANK: ClassVar[dict[str, int]] = {HIGH: 0, MEDIUM: 1, LOW: 2}


class Role:
    PERSPECTIVE = "perspective"
    DEFENDER = "defender"
    MODERATOR = "moderator"
    VALUES = (PERSPECTIVE, DEFENDER, MODERATOR)


class Stance:
    ACCEPT = "accept"
    CHALLENGE = "challenge"
    WITHDRAW = "withdraw"
    VALUES = (ACCEPT, CHALLENGE, WITHDRAW)


class AgreementLabel:
    CONSENSUS = "consensus"
    MAJORITY = "majority"
    CONTESTED = "contested"
    VALUES = (CONSENSUS, MAJORITY, CONTESTED)
    RANK: ClassVar[dict[str, int]] = {CONSENSUS: 0, MAJORITY: 1, CONTESTED: 2}


class Runner:
    CLAUDE_WORKFLOW = "claude-workflow"
    CODEX_SUBAGENTS = "codex-subagents"
    CLAUDE_AGENTS = "claude-agents"
    SEQUENTIAL = "sequential"
    VALUES = (CLAUDE_WORKFLOW, CODEX_SUBAGENTS, CLAUDE_AGENTS, SEQUENTIAL)


class ExtensionStatus:
    SELECTED = "selected"
    NOT_APPLICABLE = "not-applicable"
    FAILED = "failed"
    RECOMMENDED = "recommended"
    VALUES = (SELECTED, NOT_APPLICABLE, FAILED, RECOMMENDED)


class Language:
    PYTHON = "python"
    TYPESCRIPT = "typescript"
    OTHER = "other"
    VALUES = (PYTHON, TYPESCRIPT, OTHER)


DEFENDER_ID = "defender"
MODERATOR_ID = "moderator"
DEFAULT_PERSPECTIVES: tuple[tuple[str, str], ...] = (
    ("theorist", "Theorist"),
    ("numerical-analyst", "Numerical analyst"),
    ("experimentalist", "Experimentalist"),
    ("methodologist", "Methodologist"),
    ("computer-scientist", "Computer scientist"),
)


@dataclass(frozen=True)
class KnownExtension:
    """A known extension that the report recommends when it would apply (FR-032)."""

    id: str
    plugin: str
    install: str
    adds: str
    file_types: tuple[str, ...]
    import_patterns: tuple[str, ...]
    languages: tuple[str, ...]


KNOWN_EXTENSIONS: tuple[KnownExtension, ...] = (
    KnownExtension(
        id="building-energy-sci-review-extension",
        plugin="idfkit",
        install="idfkit@idfkit",
        adds=(
            "building physicist; heat transfer, psychrometrics, energy balances, IP and SI conversions, "
            "simulation time conventions; idfkit model checks"
        ),
        file_types=(".idf", ".epjson", ".epw"),
        import_patterns=(r"^\s*(from|import)\s+idfkit\b", r"from\s+['\"]@?idfkit"),
        languages=(Language.PYTHON, Language.TYPESCRIPT),
    ),
)


# ---------------------------------------------------------------------------
# Typed records
# ---------------------------------------------------------------------------


def _check_enum(owner: str, name: str, value: Any, allowed: Sequence[str]) -> None:
    if value not in allowed:
        raise ValidationFailure(f"{owner}.{name}: {value!r} is not one of {', '.join(allowed)}")


class Record:
    """Mixin giving frozen dataclasses JSON conversion and enumeration checks.

    Subclasses declare `_records` (field name to record class name, for nested
    records or tuples of records), `_enums` (field name to allowed values) and
    `_optional` (fields omitted from JSON when None).
    """

    _records: ClassVar[dict[str, str]] = {}
    _enums: ClassVar[dict[str, Sequence[str]]] = {}
    _optional: ClassVar[tuple[str, ...]] = ()

    def __post_init__(self) -> None:
        for name, allowed in self._enums.items():
            _check_enum(type(self).__name__, name, getattr(self, name), allowed)
        start, end = getattr(self, "line_start", None), getattr(self, "line_end", None)
        if isinstance(start, int) and isinstance(end, int) and end < start:
            ident = getattr(self, "id", getattr(self, "file", ""))
            raise ValidationFailure(f"{type(self).__name__} {ident}: line_end {end} is less than line_start {start}")

    @classmethod
    def from_json(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            raise ValidationFailure(f"{cls.__name__}: expected an object, got {type(data).__name__}")
        values: dict[str, Any] = {}
        for item in dataclasses.fields(cls):  # type: ignore[arg-type]
            if item.name not in data:
                if item.default is not dataclasses.MISSING or item.default_factory is not dataclasses.MISSING:
                    continue
                raise ValidationFailure(f"{cls.__name__}: missing field {item.name!r}")
            values[item.name] = _decode(cls._records.get(item.name), data[item.name])
        return cls(**values)

    def to_json(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for item in dataclasses.fields(self):  # type: ignore[arg-type]
            value = getattr(self, item.name)
            if value is None and item.name in self._optional:
                continue
            out[item.name] = _encode(value)
        return out


def _decode(record_name: str | None, value: Any) -> Any:
    if record_name is not None and value is not None:
        record_cls = globals()[record_name]
        if isinstance(value, list):
            return tuple(record_cls.from_json(v) for v in value)
        return record_cls.from_json(value)
    if isinstance(value, list):
        return tuple(_decode(None, v) for v in value)
    return value


def _encode(value: Any) -> Any:
    if isinstance(value, Record):
        return value.to_json()
    if isinstance(value, (tuple, list)):
        return [_encode(v) for v in value]
    return value


@dataclass(frozen=True)
class ScopedFile(Record):
    path: str
    language: str
    line_ranges: tuple[tuple[int, int], ...] = ()
    _enums: ClassVar[dict[str, Sequence[str]]] = {"language": Language.VALUES}


@dataclass(frozen=True)
class Exclusion(Record):
    path: str
    reason: str


@dataclass(frozen=True)
class ReviewScope(Record):
    mode: str
    base: str | None
    head: str | None
    files: tuple[ScopedFile, ...]
    excluded: tuple[Exclusion, ...]
    note: str
    _records: ClassVar[dict[str, str]] = {"files": "ScopedFile", "excluded": "Exclusion"}
    _enums: ClassVar[dict[str, Sequence[str]]] = {"mode": ScopeMode.VALUES}


@dataclass(frozen=True)
class Perspective(Record):
    id: str
    name: str
    brief_path: str
    source: str
    reference_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class Applicability(Record):
    globs: tuple[str, ...] = ()
    file_types: tuple[str, ...] = ()
    import_patterns: tuple[str, ...] = ()
    languages: tuple[str, ...] = ()


@dataclass(frozen=True)
class DomainExtension(Record):
    id: str
    plugin: str
    contract_version: int
    perspective: Perspective | None
    reference_paths: tuple[str, ...]
    applies_to: Applicability | None
    checks: str | None
    status: str
    status_reason: str | None = None
    adds: str | None = None
    declaration: str | None = None
    _records: ClassVar[dict[str, str]] = {"perspective": "Perspective", "applies_to": "Applicability"}
    _enums: ClassVar[dict[str, Sequence[str]]] = {"status": ExtensionStatus.VALUES}

    def to_report_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "plugin": self.plugin,
            "contract_version": self.contract_version,
            "perspective_id": self.perspective.id if self.perspective else None,
            "status": self.status,
            "status_reason": self.status_reason,
            "adds": self.adds,
        }


@dataclass(frozen=True)
class ModelAssignment(Record):
    role: str
    model: str


@dataclass(frozen=True)
class Panel(Record):
    perspectives: tuple[Perspective, ...]
    rebuttal_rounds: int
    max_batches: int
    runner: str
    independent: bool
    models: tuple[ModelAssignment, ...] = ()
    _records: ClassVar[dict[str, str]] = {"perspectives": "Perspective", "models": "ModelAssignment"}
    _enums: ClassVar[dict[str, Sequence[str]]] = {"runner": Runner.VALUES}


@dataclass(frozen=True)
class PanelState(Record):
    """Content of `$RUN/panel.json`: the panel (once configured), extensions and notices."""

    panel: Panel | None = None
    extensions: tuple[DomainExtension, ...] = ()
    notices: tuple[str, ...] = ()
    _records: ClassVar[dict[str, str]] = {"panel": "Panel", "extensions": "DomainExtension"}


@dataclass(frozen=True)
class CandidateFinding(Record):
    id: str
    raised_by: str
    file: str
    line_start: int
    line_end: int
    dimension: str
    severity: str
    summary: str
    trigger: str | None
    wrong_output: str | None
    fix: str
    evidence: str
    _enums: ClassVar[dict[str, Sequence[str]]] = {"dimension": Dimension.VALUES, "severity": Severity.VALUES}


@dataclass(frozen=True)
class CheckedItem(Record):
    file: str
    line_start: int
    line_end: int
    dimension: str
    note: str
    _enums: ClassVar[dict[str, Sequence[str]]] = {"dimension": Dimension.VALUES}


@dataclass(frozen=True)
class CandidateMessage(Record):
    perspective: str
    findings: tuple[CandidateFinding, ...]
    checked_items: tuple[CheckedItem, ...]
    notes: str
    _records: ClassVar[dict[str, str]] = {"findings": "CandidateFinding", "checked_items": "CheckedItem"}


@dataclass(frozen=True)
class MergedFinding(Record):
    id: str
    members: tuple[str, ...]
    raised_by: tuple[str, ...]
    batch: int
    file: str
    line_start: int
    line_end: int
    dimension: str
    severity: str
    summary: str
    trigger: str | None
    wrong_output: str | None
    fix: str
    severity_reason: str | None = None
    _enums: ClassVar[dict[str, Sequence[str]]] = {"dimension": Dimension.VALUES, "severity": Severity.VALUES}
    _optional: ClassVar[tuple[str, ...]] = ("severity_reason",)


@dataclass(frozen=True)
class SplitRecord(Record):
    cluster: str
    reason: str


@dataclass(frozen=True)
class MergeRuling(Record):
    batch: int
    findings: tuple[MergedFinding, ...]
    split: tuple[SplitRecord, ...] = ()
    _records: ClassVar[dict[str, str]] = {"findings": "MergedFinding", "split": "SplitRecord"}


@dataclass(frozen=True)
class Position(Record):
    finding_id: str
    member: str
    round: int
    stance: str
    reason: str
    answers: tuple[str, ...] = ()
    _enums: ClassVar[dict[str, Sequence[str]]] = {"stance": Stance.VALUES}

    @property
    def position_id(self) -> str:
        return f"{self.member}:{self.finding_id}:{self.round}"


@dataclass(frozen=True)
class DebateMessage(Record):
    member: str
    round: int
    positions: tuple[Position, ...]
    _records: ClassVar[dict[str, str]] = {"positions": "Position"}


@dataclass(frozen=True)
class ModeratorNote(Record):
    finding_id: str
    argument_for: str
    argument_against: str
    deciding_assumption: str | None
    rejection_reason: str
    no_trigger_reason: str | None


@dataclass(frozen=True)
class NotesMessage(Record):
    batch: int
    notes: tuple[ModeratorNote, ...]
    _records: ClassVar[dict[str, str]] = {"notes": "ModeratorNote"}


@dataclass(frozen=True)
class DebateRecord(Record):
    finding_id: str
    positions: tuple[Position, ...]
    rounds_run: int
    _records: ClassVar[dict[str, str]] = {"positions": "Position"}


@dataclass(frozen=True)
class Finding(Record):
    id: str
    members: tuple[str, ...]
    raised_by: tuple[str, ...]
    batch: int
    file: str
    line_start: int
    line_end: int
    dimension: str
    severity: str
    summary: str
    trigger: str | None
    wrong_output: str | None
    fix: str
    label: str
    severity_reason: str | None = None
    argument_for: str | None = None
    argument_against: str | None = None
    deciding_assumption: str | None = None
    no_trigger_reason: str | None = None
    _enums: ClassVar[dict[str, Sequence[str]]] = {
        "dimension": Dimension.VALUES,
        "severity": Severity.VALUES,
        "label": AgreementLabel.VALUES,
    }
    _optional: ClassVar[tuple[str, ...]] = (
        "severity_reason",
        "argument_for",
        "argument_against",
        "no_trigger_reason",
    )

    def to_json(self) -> dict[str, Any]:
        out = super().to_json()
        if self.label != AgreementLabel.CONTESTED:
            out.pop("deciding_assumption", None)
        return out

    @property
    def concrete(self) -> bool:
        return self.trigger is not None and self.wrong_output is not None


@dataclass(frozen=True)
class RejectedFinding(Record):
    finding_id: str
    summary: str
    raised_by: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class Adjudication(Record):
    """Content of `$RUN/adjudication.json`."""

    findings: tuple[Finding, ...]
    rejected: tuple[RejectedFinding, ...]
    records: tuple[DebateRecord, ...]
    notices: tuple[str, ...] = ()
    _records: ClassVar[dict[str, str]] = {
        "findings": "Finding",
        "rejected": "RejectedFinding",
        "records": "DebateRecord",
    }


@dataclass(frozen=True)
class RunInfo(Record):
    """Content of `$RUN/run.json`."""

    project: str
    run: str


@dataclass(frozen=True)
class Cluster:
    id: str
    suggested_finding_id: str
    file: str
    line_start: int
    line_end: int
    members: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "suggested_finding_id": self.suggested_finding_id,
            "file": self.file,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "members": list(self.members),
        }


@dataclass(frozen=True)
class Batch:
    batch: int
    clusters: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {"batch": self.batch, "clusters": list(self.clusters)}


@dataclass(frozen=True)
class DebateStatus:
    """Output of `panel.py debate-status`: whether a batch's debate stops after a round, and whom to call next."""

    batch: int
    round: int
    stopped: bool
    call: tuple[str, ...]


@dataclass(frozen=True)
class MergePlan:
    """Output of `panel.py merge`: location clusters and the debate batches that hold them."""

    clusters: tuple[Cluster, ...]
    batches: tuple[Batch, ...]

    def to_json(self) -> dict[str, Any]:
        batch_of = {cluster_id: b.batch for b in self.batches for cluster_id in b.clusters}
        return {
            "clusters": [{**c.to_json(), "batch": batch_of[c.id]} for c in self.clusters],
            "batches": [{**b.to_json(), "next_finding_id": split_finding_id(b.batch, 1)} for b in self.batches],
        }


@dataclass(frozen=True)
class ReviewReport:
    scope: ReviewScope
    panel: Panel
    extensions: tuple[DomainExtension, ...]
    findings: tuple[Finding, ...]
    rejected: tuple[RejectedFinding, ...]
    checked_items: tuple[CheckedItem, ...]
    unreviewed: tuple[Exclusion, ...]
    notices: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "scope": self.scope.to_json(),
            "panel": self.panel.to_json(),
            "extensions": [e.to_report_json() for e in self.extensions],
            "findings": [f.to_json() for f in self.findings],
            "rejected": [r.to_json() for r in self.rejected],
            "checked_items": [c.to_json() for c in self.checked_items],
            "unreviewed": [u.to_json() for u in self.unreviewed],
            "notices": list(self.notices),
        }


@dataclass(frozen=True)
class ReportFinding:
    """One entry of the ReportFindings mapping (contracts/report.md section 3)."""

    file: str
    line: int
    summary: str
    failure_scenario: str
    category: str
    verdict: str
    short_summary: str

    def to_json(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


# ---------------------------------------------------------------------------
# JSON Schema validation (subset) and single-message semantic checks
# ---------------------------------------------------------------------------

SCHEMA_NAMES = ("candidate-findings", "merge-ruling", "debate-positions", "moderator-notes", "report")


def load_schema(name: str) -> dict[str, Any]:
    if name not in SCHEMA_NAMES:
        raise UsageFailure(f"unknown schema {name!r}; expected one of {', '.join(SCHEMA_NAMES)}")
    return json.loads((SCHEMA_DIR / f"{name}.schema.json").read_text(encoding="utf-8"))


_TYPE_CHECKS = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "null": lambda v: v is None,
}


def _resolve(schema: dict[str, Any], root: dict[str, Any]) -> dict[str, Any]:
    while "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            raise UsageFailure(f"unsupported $ref {ref!r}")
        target: Any = root
        for part in ref[2:].split("/"):
            target = target[part]
        schema = target
    return schema


def schema_errors(schema: dict[str, Any], value: Any, root: dict[str, Any] | None = None, path: str = "$") -> list[str]:
    """Validate `value` against the supported JSON Schema subset; return error messages."""
    root = root if root is not None else schema
    schema = _resolve(schema, root)
    errors: list[str] = []
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_TYPE_CHECKS[t](value) for t in types):
            return [f"{path}: expected {' or '.join(types)}, got {type(value).__name__}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} is not one of {schema['enum']}")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: shorter than {schema['minLength']} characters")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: {value!r} does not match {schema['pattern']}")
    is_number = isinstance(value, (int, float)) and not isinstance(value, bool)
    if is_number and "minimum" in schema and value < schema["minimum"]:
        errors.append(f"{path}: {value} is less than {schema['minimum']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: fewer than {schema['minItems']} items")
        if "items" in schema:
            for index, item in enumerate(value):
                errors.extend(schema_errors(schema["items"], item, root, f"{path}[{index}]"))
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in value:
                errors.append(f"{path}: missing required property {name!r}")
        for name, item in value.items():
            if name in properties:
                errors.extend(schema_errors(properties[name], item, root, f"{path}.{name}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unknown property {name!r}")
    for clause in schema.get("allOf", []):
        if "if" in clause:
            if not schema_errors(clause["if"], value, root, path):
                errors.extend(schema_errors(clause.get("then", {}), value, root, path))
        else:
            errors.extend(schema_errors(clause, value, root, path))
    return errors


def semantic_errors(name: str, value: Any) -> list[str]:
    """Single-message semantic checks that the schema subset cannot express (data-model.md section 3)."""
    errors: list[str] = []

    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            start, end = node.get("line_start"), node.get("line_end")
            if isinstance(start, int) and isinstance(end, int) and end < start:
                errors.append(f"{path}: line_end {end} is less than line_start {start}")
            for key, item in node.items():
                walk(item, f"{path}.{key}")
        elif isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{path}[{index}]")

    walk(value, "$")
    if name == "debate-positions" and isinstance(value, dict):
        for index, position in enumerate(value.get("positions", [])):
            if position.get("member") != value.get("member"):
                errors.append(f"$.positions[{index}]: member differs from the message member")
            if position.get("round") != value.get("round"):
                errors.append(f"$.positions[{index}]: round differs from the message round")
    if name == "candidate-findings" and isinstance(value, dict):
        for index, finding in enumerate(value.get("findings", [])):
            if finding.get("raised_by") != value.get("perspective"):
                errors.append(f"$.findings[{index}]: raised_by differs from the message perspective")
    if name == "report" and isinstance(value, dict):
        for index, finding in enumerate(value.get("findings", [])):
            if (finding.get("trigger") is None or finding.get("wrong_output") is None) and not finding.get(
                "no_trigger_reason"
            ):
                errors.append(
                    f"$.findings[{index}]: no_trigger_reason is required when trigger or wrong_output is null"
                )
    return errors


def validate_message(name: str, value: Any) -> list[str]:
    errors = schema_errors(load_schema(name), value)
    return errors or semantic_errors(name, value)


def require_valid(name: str, value: Any, label: str) -> None:
    errors = validate_message(name, value)
    if errors:
        raise ValidationFailure(f"{label} does not conform to {name}.schema.json", errors)


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PreconditionFailure(f"{path} does not exist") from exc
    except json.JSONDecodeError as exc:
        raise ValidationFailure(f"{path} is not valid JSON: {exc}") from exc


def dumps(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def write_json(path: Path, data: Any, dry_run: bool) -> None:
    write_text(path, dumps(data), dry_run)


def write_text(path: Path, text: str, dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] would write {path}:")
        print(text, end="" if text.endswith("\n") else "\n")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def is_inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def load_run(run: str) -> tuple[Path, RunInfo]:
    run_dir = Path(run).resolve()
    info_path = run_dir / "run.json"
    if not info_path.is_file():
        raise PreconditionFailure(f"{run_dir} is not a sci-review run directory (no run.json); run `panel.py init`")
    info = RunInfo.from_json(read_json(info_path))
    if is_inside(run_dir, Path(info.project)):
        raise PreconditionFailure(f"run directory {run_dir} lies inside the reviewed project")
    return run_dir, info


def load_panel_state(run_dir: Path) -> PanelState:
    path = run_dir / "panel.json"
    if not path.is_file():
        return PanelState()
    return PanelState.from_json(read_json(path))


def load_notices(run_dir: Path) -> list[str]:
    path = run_dir / "notices.json"
    return list(read_json(path)) if path.is_file() else []


# ---------------------------------------------------------------------------
# init, clean, notice
# ---------------------------------------------------------------------------


def cmd_init(args: argparse.Namespace) -> int:
    project = Path(args.project).resolve()
    if not project.is_dir():
        raise PreconditionFailure(f"project {project} is not a directory")
    base = Path(tempfile.gettempdir()).resolve()
    run_dir = base / f"{RUN_PREFIX}{secrets.token_hex(4)}"
    if is_inside(run_dir, project):
        raise PreconditionFailure(
            f"the system temporary directory {base} lies inside the project {project}; "
            "set TMPDIR to a directory outside the project"
        )
    info = RunInfo(project=str(project), run=str(run_dir))
    if args.dry_run:
        print(f"[dry-run] would create {run_dir}")
        write_json(run_dir / "run.json", info.to_json(), True)
        return EXIT_OK
    run_dir.mkdir(parents=True)
    write_json(run_dir / "run.json", info.to_json(), False)
    print(run_dir)
    return EXIT_OK


def cmd_clean(args: argparse.Namespace) -> int:
    run_dir, _info = load_run(args.run)
    if not run_dir.name.startswith(RUN_PREFIX) or not is_inside(run_dir, Path(tempfile.gettempdir())):
        raise PreconditionFailure(f"refusing to remove {run_dir}: not a sci-review run directory under the temp dir")
    if args.dry_run:
        print(f"[dry-run] would remove {run_dir}")
        return EXIT_OK
    shutil.rmtree(run_dir)
    print(f"removed {run_dir}")
    return EXIT_OK


def cmd_notice(args: argparse.Namespace) -> int:
    run_dir, _info = load_run(args.run)
    notices = load_notices(run_dir)
    if args.text not in notices:
        notices.append(args.text)
    write_json(run_dir / "notices.json", notices, args.dry_run)
    return EXIT_OK


# ---------------------------------------------------------------------------
# scope
# ---------------------------------------------------------------------------

LOCK_FILES = frozenset(
    {
        "uv.lock",
        "poetry.lock",
        "pdm.lock",
        "Pipfile.lock",
        "package-lock.json",
        "npm-shrinkwrap.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "bun.lockb",
        "Cargo.lock",
        "Gemfile.lock",
        "composer.lock",
    }
)
VENDORED_DIRS = ("node_modules", "dist", "vendor", "third_party", "__pycache__")
SKIP_WALK_DIRS = frozenset({".git", ".venv", "venv", ".tox", ".mypy_cache", ".ruff_cache", *VENDORED_DIRS})
PYTHON_SUFFIXES = frozenset({".py", ".pyi", ".ipynb"})
TYPESCRIPT_SUFFIXES = frozenset({".ts", ".tsx", ".mts", ".cts"})


def language_of(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix in PYTHON_SUFFIXES:
        return Language.PYTHON
    if suffix in TYPESCRIPT_SUFFIXES:
        return Language.TYPESCRIPT
    return Language.OTHER


def git(project: Path, *argv: str, check: bool = True, stdin: str | None = None) -> str:
    """Run git with unquoted UTF-8 paths in its output (core.quotePath=false)."""
    result = subprocess.run(
        ["git", "-c", "core.quotePath=false", *argv],
        cwd=project,
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="surrogateescape",
        check=False,
    )
    if check and result.returncode != 0:
        raise PreconditionFailure(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout if result.returncode == 0 else ""


def git_paths(project: Path, *argv: str) -> list[str]:
    """Paths printed by a git command run with -z (NUL-separated, never quoted)."""
    return [path for path in git(project, *argv, "-z").split("\0") if path]


_C_ESCAPES = {"a": 7, "b": 8, "t": 9, "n": 10, "v": 11, "f": 12, "r": 13, '"': 34, "\\": 92}


def unquote_git_path(text: str) -> str:
    """Undo git's C-style quoting of a path in a diff header (used for quotes, backslashes, control bytes)."""
    if not (len(text) >= 2 and text.startswith('"') and text.endswith('"')):
        return text
    body, out, i = text[1:-1], bytearray(), 0
    while i < len(body):
        char = body[i]
        if char == "\\" and i + 1 < len(body):
            nxt = body[i + 1]
            if nxt in "01234567" and i + 3 < len(body) + 1 and all(c in "01234567" for c in body[i + 1 : i + 4]):
                out.append(int(body[i + 1 : i + 4], 8))
                i += 4
                continue
            out.append(_C_ESCAPES.get(nxt, ord(nxt)))
            i += 2
            continue
        out.extend(char.encode("utf-8", "surrogateescape"))
        i += 1
    return out.decode("utf-8", "surrogateescape")


def is_git_repo(project: Path) -> bool:
    if shutil.which("git") is None:
        return False
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"], cwd=project, capture_output=True, text=True, check=False
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def ref_exists(project: Path, ref: str) -> bool:
    return bool(git(project, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}", check=False).strip())


def default_branch(project: Path) -> str | None:
    remote_head = git(project, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD", check=False).strip()
    if remote_head:
        return remote_head
    for candidate in ("origin/main", "origin/master", "main", "master"):
        if ref_exists(project, candidate):
            return candidate
    return None


@dataclass(frozen=True)
class ResolvedBase:
    mode: str
    base: str
    description: str


def resolve_base(project: Path, baseline: str | None) -> ResolvedBase:
    if baseline:
        separator = "..." if "..." in baseline else ".." if ".." in baseline else None
        if separator is not None:
            left, right = baseline.split(separator, 1)
            left = left or "HEAD"
            if right and right != "HEAD":
                head = git(project, "rev-parse", "HEAD", check=False).strip()
                if not ref_exists(project, right) or git(project, "rev-parse", f"{right}^{{commit}}").strip() != head:
                    raise UsageFailure(
                        f"baseline {baseline!r} ends at {right!r}, but the review always covers HEAD and the working "
                        "tree; check out that revision first, or give a baseline that ends at HEAD"
                    )
        if separator == "...":
            base = git(project, "merge-base", left, "HEAD").strip()
            return ResolvedBase(ScopeMode.EXPLICIT, base, f"merge-base of {left} and HEAD")
        left = baseline.split("..", 1)[0] or "HEAD" if ".." in baseline else baseline
        if not ref_exists(project, left):
            raise PreconditionFailure(f"baseline {baseline!r} does not resolve to a commit")
        base = git(project, "rev-parse", f"{left}^{{commit}}").strip()
        return ResolvedBase(ScopeMode.EXPLICIT, base, f"baseline {left}")
    default = default_branch(project)
    if default is None:
        raise PreconditionFailure(
            "no base branch could be determined (no remote default branch and no main or master branch); "
            "name a baseline with --baseline REF, or review with --mode repository or --mode paths"
        )
    head_branch = git(project, "rev-parse", "--abbrev-ref", "HEAD", check=False).strip()
    ahead = git(project, "rev-list", "--count", f"{default}..HEAD", check=False).strip()
    if head_branch in (default, default.split("/", 1)[-1]) or ahead in ("", "0"):
        raise PreconditionFailure(
            f"the current branch has not diverged from the default branch {default}, so no branch base can be "
            "determined; name a baseline with --baseline REF, or review with --mode repository or --mode paths"
        )
    base = git(project, "merge-base", default, "HEAD").strip()
    return ResolvedBase(ScopeMode.BRANCH, base, f"merge-base with {default} on branch {head_branch}")


HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def parse_diff(diff: str) -> dict[str, list[tuple[int, int]]]:
    """Map each changed file in a `git diff --unified=0 --no-prefix` to its changed line ranges in the new version."""
    ranges: dict[str, list[tuple[int, int]]] = {}
    current: str | None = None
    for line in diff.splitlines():
        if line.startswith("+++ "):
            # git appends a tab to names containing a space and C-quotes names with special bytes.
            target = unquote_git_path(line[4:].removesuffix("\t"))
            current = None if target == "/dev/null" else target
            if current is not None:
                ranges.setdefault(current, [])
        elif line.startswith("@@") and current is not None:
            match = HUNK.match(line)
            if match is None:
                continue
            start = int(match.group(1))
            count = int(match.group(2)) if match.group(2) is not None else 1
            if count == 0:
                ranges[current].append((max(start, 1), max(start, 1)))
            else:
                ranges[current].append((start, start + count - 1))
    return ranges


def line_count(path: Path) -> int:
    try:
        data = path.read_bytes()
    except OSError:
        return 0
    if not data:
        return 0
    return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def is_binary(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            return b"\0" in handle.read(8192)
    except OSError:
        return False


def generated_paths(project: Path, paths: Sequence[str], in_git: bool) -> dict[str, str]:
    """Return paths marked linguist-generated or linguist-vendored, with the reason."""
    if not in_git or not paths:
        return {}
    marked: dict[str, str] = {}
    output = git(
        project,
        "check-attr",
        "-z",
        "--stdin",
        "linguist-generated",
        "linguist-vendored",
        check=False,
        stdin="\0".join(paths) + "\0",
    )
    fields = output.split("\0")
    for index in range(0, len(fields) - 2, 3):
        path, attribute, value = fields[index : index + 3]
        if value in ("set", "true"):
            marked[path] = "generated" if attribute == "linguist-generated" else "vendored"
    return marked


def exclusion_reason(path: str, marked: dict[str, str]) -> str | None:
    parts = Path(path).parts
    if Path(path).name in LOCK_FILES:
        return "generated (lock file)"
    for directory in VENDORED_DIRS:
        if directory in parts[:-1]:
            return f"vendored or generated ({directory}/)"
    if path in marked:
        return f"{marked[path]} (linguist attribute)"
    return None


def walk_files(project: Path, roots: Sequence[Path]) -> list[str]:
    files: list[str] = []
    for root in roots:
        if root.is_file():
            files.append(root.relative_to(project).as_posix())
            continue
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(project)
            if any(part in SKIP_WALK_DIRS for part in relative.parts[:-1]) or not path.is_file():
                continue
            files.append(relative.as_posix())
    return sorted(set(files))


def cmd_scope(args: argparse.Namespace) -> int:
    run_dir, info = load_run(args.run)
    project = Path(info.project)
    in_git = is_git_repo(project)
    named: set[str] = set()
    base: str | None = None
    head: str | None = None
    mode = args.mode
    candidates: dict[str, list[tuple[int, int]]] = {}
    outside: list[str] = []

    if args.mode == ScopeMode.BRANCH:
        if not in_git:
            raise PreconditionFailure(
                f"{project} is not a git repository, so a branch review is not possible; "
                "review with --mode repository or --mode paths instead"
            )
        resolved = resolve_base(project, args.baseline)
        mode, base = resolved.mode, resolved.base
        head = "HEAD with uncommitted and untracked changes"
        diff = git(project, "diff", "--unified=0", "--no-color", "--no-ext-diff", "--no-prefix", "--find-renames", base)
        candidates = parse_diff(diff)
        for path in git_paths(project, "ls-files", "--others", "--exclude-standard"):
            count = line_count(project / path)
            candidates[path] = [(1, count)] if count else []
        description = f"Changes since {resolved.description} ({base[:12]}), including uncommitted and untracked files"
    elif args.mode in (ScopeMode.REPOSITORY, ScopeMode.PATHS):
        if args.baseline:
            raise UsageFailure("--baseline is accepted only with --mode branch")
        roots: list[Path] = []
        if args.mode == ScopeMode.PATHS:
            if not args.path:
                raise UsageFailure("--mode paths requires at least one --path")
            for raw in args.path:
                resolved_path = (project / raw).resolve()
                if not is_inside(resolved_path, project) or not resolved_path.exists():
                    raise UsageFailure(f"path {raw!r} does not exist inside the project")
                roots.append(resolved_path)
                if resolved_path.is_file():
                    named.add(resolved_path.relative_to(project).as_posix())
        if in_git:
            tracked = git_paths(project, "ls-files")
            untracked = git_paths(project, "ls-files", "--others", "--exclude-standard")
            every = sorted(set(tracked) | set(untracked))
            head = git(project, "rev-parse", "HEAD", check=False).strip() or None
        else:
            every = walk_files(project, [project])
        if args.mode == ScopeMode.PATHS:
            prefixes = [root.relative_to(project).as_posix() for root in roots]
            selected = [
                p for p in every if any(p == x or p.startswith(x.rstrip("/") + "/") or x == "." for x in prefixes)
            ]
            chosen = set(selected)
            outside = [p for p in every if p not in chosen]
            every = selected
            description = f"Files under {', '.join(prefixes)}"
        else:
            description = "All files of the repository"
        candidates = {path: [] for path in every if (project / path).is_file()}
    else:
        raise UsageFailure(f"unknown mode {args.mode!r}")

    marked = generated_paths(project, sorted(candidates), in_git)
    excluded: list[Exclusion] = [Exclusion(path=p, reason="outside paths") for p in outside]
    kept: list[ScopedFile] = []
    for path in sorted(candidates):
        reason = None if path in named else exclusion_reason(path, marked)
        if reason is None and is_binary(project / path):
            reason = "binary file"
        if reason is None and args.mode == ScopeMode.BRANCH and not (project / path).is_file():
            reason = "deleted"
        if reason is not None:
            excluded.append(Exclusion(path=path, reason=reason))
            continue
        kept.append(ScopedFile(path=path, language=language_of(path), line_ranges=tuple(candidates[path])))

    budget = args.budget if args.budget is not None else DEFAULT_BUDGET
    if budget < 1:
        raise UsageFailure("--budget must be a positive number of lines")
    files: list[ScopedFile] = []
    total = 0
    for scoped in kept:
        size = (
            sum(end - start + 1 for start, end in scoped.line_ranges)
            if scoped.line_ranges
            else line_count(project / scoped.path)
        )
        if files and total + size > budget:
            excluded.append(Exclusion(path=scoped.path, reason="over budget"))
            continue
        files.append(scoped)
        total += size
    over = sum(1 for e in excluded if e.reason == "over budget")
    note = f"{description}: {len(files)} files, {total} lines."
    if over:
        note = (
            f"{description}: {len(files)} files, {total} lines; "
            f"{over} files over the {budget}-line budget were not reviewed."
        )
    scope = ReviewScope(mode=mode, base=base, head=head, files=tuple(files), excluded=tuple(excluded), note=note)
    write_json(run_dir / "scope.json", scope.to_json(), args.dry_run)
    if not args.dry_run:
        print(note)
    return EXIT_OK


def load_scope(run_dir: Path) -> ReviewScope:
    return ReviewScope.from_json(read_json(run_dir / "scope.json"))


# ---------------------------------------------------------------------------
# select-extensions
# ---------------------------------------------------------------------------


def _matches_glob(path: str, pattern: str) -> bool:
    path_l, pattern_l = path.lower(), pattern.lower()
    if fnmatch.fnmatchcase(path_l, pattern_l):
        return True
    if pattern_l.startswith("**/"):
        rest = pattern_l[3:]
        return fnmatch.fnmatchcase(path_l, rest) or fnmatch.fnmatchcase(Path(path_l).name, rest)
    return False


def file_matches(project: Path, scoped: ScopedFile, applies: Applicability) -> bool:
    """A file matches if any glob or file type matches, or its language is listed and an import pattern matches."""
    if any(_matches_glob(scoped.path, g) for g in applies.globs):
        return True
    suffix = Path(scoped.path).suffix.lower()
    if any(suffix == t.lower() if t.startswith(".") else suffix == "." + t.lower() for t in applies.file_types):
        return True
    if scoped.language in applies.languages and applies.import_patterns:
        try:
            text = (project / scoped.path).read_text(encoding="utf-8", errors="replace")
        except OSError:
            return False
        return any(re.search(p, text, re.MULTILINE) for p in applies.import_patterns)
    return False


def parse_declaration(path: Path) -> DomainExtension:
    """Parse one extension.json; return a failed extension with the reason if it is invalid."""
    skill_dir = path.parent
    fallback_id = skill_dir.name

    def failed(reason: str, data: dict[str, Any] | None = None) -> DomainExtension:
        data = data or {}
        version = data.get("contract_version")
        return DomainExtension(
            id=str(data.get("id") or fallback_id),
            plugin=str(data.get("plugin") or "unknown"),
            contract_version=version if isinstance(version, int) and not isinstance(version, bool) else 0,
            perspective=None,
            reference_paths=(),
            applies_to=None,
            checks=None,
            status=ExtensionStatus.FAILED,
            status_reason=reason,
            declaration=str(path),
        )

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return failed(f"declaration {path} not found")
    except json.JSONDecodeError as exc:
        return failed(f"declaration is not valid JSON ({exc})")
    if not isinstance(data, dict):
        return failed("declaration is not a JSON object")
    missing = [k for k in ("contract_version", "id", "plugin", "perspective", "applies_to") if k not in data]
    if missing:
        return failed(f"declaration is missing required fields: {', '.join(missing)}", data)
    if data["contract_version"] != CONTRACT_VERSION:
        return failed(
            f"contract_version {data['contract_version']!r} is not supported (supported: {CONTRACT_VERSION})", data
        )
    if not str(data["id"]).endswith("sci-review-extension"):
        return failed("id must end in 'sci-review-extension'", data)
    perspective = data["perspective"]
    if not isinstance(perspective, dict) or not all(
        isinstance(perspective.get(k), str) for k in ("id", "name", "brief")
    ):
        return failed("perspective must have string fields id, name and brief", data)
    if not MEMBER_ID.match(perspective["id"]) or perspective["id"] in (DEFENDER_ID, MODERATOR_ID):
        return failed(
            f"perspective id {perspective['id']!r} must be kebab-case and must not be 'defender' or 'moderator'", data
        )
    applies = data["applies_to"]
    if not isinstance(applies, dict) or not any(applies.get(k) for k in ("globs", "file_types", "import_patterns")):
        return failed("applies_to must declare at least one glob, file type or import pattern", data)
    unknown = set(applies) - {"globs", "file_types", "import_patterns", "languages"}
    if unknown:
        return failed(f"applies_to has unknown fields: {', '.join(sorted(unknown))}", data)
    brief = (skill_dir / perspective["brief"]).resolve()
    if not brief.is_file():
        return failed(f"perspective brief {perspective['brief']!r} not found", data)
    references = []
    for ref in data.get("reference", []):
        ref_path = (skill_dir / ref).resolve()
        if not ref_path.is_file():
            return failed(f"reference document {ref!r} not found", data)
        references.append(str(ref_path))
    checks = data.get("checks")
    checks_path = None
    if checks is not None:
        checks_path = (skill_dir / checks).resolve()
        if not checks_path.is_file():
            return failed(f"checks document {checks!r} not found", data)
    for pattern in applies.get("import_patterns", []):
        try:
            re.compile(pattern)
        except re.error as exc:
            return failed(f"import pattern {pattern!r} is not a valid regular expression ({exc})", data)
    return DomainExtension(
        id=data["id"],
        plugin=data["plugin"],
        contract_version=CONTRACT_VERSION,
        perspective=Perspective(
            id=perspective["id"],
            name=perspective["name"],
            brief_path=str(brief),
            source=data["id"],
            reference_paths=tuple(references) + ((str(checks_path),) if checks_path else ()),
        ),
        reference_paths=tuple(references),
        applies_to=Applicability(
            globs=tuple(applies.get("globs", [])),
            file_types=tuple(applies.get("file_types", [])),
            import_patterns=tuple(applies.get("import_patterns", [])),
            languages=tuple(applies.get("languages", [])),
        ),
        checks=str(checks_path) if checks_path else None,
        status=ExtensionStatus.NOT_APPLICABLE,
        declaration=str(path),
    )


def select_extensions(project: Path, scope: ReviewScope, declarations: Sequence[Path]) -> list[DomainExtension]:
    extensions: list[DomainExtension] = []
    seen_perspectives = {DEFENDER_ID, MODERATOR_ID, *(pid for pid, _ in DEFAULT_PERSPECTIVES)}
    for declaration in declarations:
        extension = parse_declaration(declaration)
        if extension.status != ExtensionStatus.FAILED and extension.applies_to is not None:
            matched = [f.path for f in scope.files if file_matches(project, f, extension.applies_to)]
            assert extension.perspective is not None
            if matched and extension.perspective.id in seen_perspectives:
                extension = dataclasses.replace(
                    extension,
                    status=ExtensionStatus.FAILED,
                    status_reason=f"perspective id {extension.perspective.id!r} is already used in the panel",
                )
            elif matched:
                seen_perspectives.add(extension.perspective.id)
                shown = ", ".join(matched[:3]) + (f" and {len(matched) - 3} more" if len(matched) > 3 else "")
                extension = dataclasses.replace(
                    extension, status=ExtensionStatus.SELECTED, status_reason=f"applies to {shown}"
                )
            else:
                extension = dataclasses.replace(
                    extension,
                    status=ExtensionStatus.NOT_APPLICABLE,
                    status_reason="no file in the scope matches its applicability declaration",
                )
        extensions.append(extension)
    # A known extension that was discovered, even if its declaration failed, is installed: never recommend it.
    discovered = {e.id for e in extensions}
    for known in KNOWN_EXTENSIONS:
        if known.id in discovered:
            continue
        applies = Applicability(
            file_types=known.file_types, import_patterns=known.import_patterns, languages=known.languages
        )
        matched = [f.path for f in scope.files if file_matches(project, f, applies)]
        if matched:
            extensions.append(
                DomainExtension(
                    id=known.id,
                    plugin=known.plugin,
                    contract_version=CONTRACT_VERSION,
                    perspective=None,
                    reference_paths=(),
                    applies_to=None,
                    checks=None,
                    status=ExtensionStatus.RECOMMENDED,
                    status_reason=f"not installed; it would apply to {matched[0]}. Install it with {known.install}.",
                    adds=known.adds,
                )
            )
    return extensions


def cmd_select_extensions(args: argparse.Namespace) -> int:
    run_dir, info = load_run(args.run)
    scope = load_scope(run_dir)
    extensions = select_extensions(Path(info.project), scope, [Path(d) for d in args.declaration or []])
    state = dataclasses.replace(load_panel_state(run_dir), extensions=tuple(extensions))
    write_json(run_dir / "panel.json", state.to_json(), args.dry_run)
    if not args.dry_run:
        for extension in extensions:
            print(f"{extension.status:15} {extension.id}: {extension.status_reason or ''}")
    return EXIT_OK


# ---------------------------------------------------------------------------
# panel
# ---------------------------------------------------------------------------


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def default_perspective(pid: str, name: str) -> Perspective:
    return Perspective(id=pid, name=name, brief_path=str(ROLES_DIR / f"{pid}.md"), source="sci-review")


def configure_panel(
    available: Sequence[Perspective],
    requested: Sequence[str] | None,
    rounds: int | None,
    batches: int | None,
    runner: str,
    models: Sequence[ModelAssignment] = (),
) -> tuple[Panel, list[str]]:
    _check_enum("panel", "runner", runner, Runner.VALUES)
    notices: list[str] = []
    by_id = {p.id: p for p in available}
    if requested:
        unknown = [r for r in requested if r not in by_id]
        if unknown:
            notices.append(f"Unknown perspectives were ignored: {', '.join(unknown)}.")
        chosen = list(dict.fromkeys(r for r in requested if r in by_id))
    else:
        chosen = [p.id for p in available]
    if len(chosen) > MAX_PERSPECTIVES:
        notices.append(
            f"The panel was limited to {MAX_PERSPECTIVES} perspectives; "
            f"{', '.join(chosen[MAX_PERSPECTIVES:])} did not take part."
        )
        chosen = chosen[:MAX_PERSPECTIVES]
    if len(chosen) < MIN_PERSPECTIVES:
        for pid in by_id:
            if len(chosen) >= MIN_PERSPECTIVES:
                break
            if pid not in chosen:
                chosen.append(pid)
        notices.append(f"The panel was raised to the minimum of {MIN_PERSPECTIVES} perspectives.")
    requested_rounds = DEFAULT_ROUNDS if rounds is None else rounds
    requested_batches = DEFAULT_BATCHES if batches is None else batches
    rebuttal_rounds = clamp(requested_rounds, MIN_ROUNDS, MAX_ROUNDS)
    max_batches = clamp(requested_batches, MIN_BATCHES, MAX_BATCHES)
    if rebuttal_rounds != requested_rounds:
        notices.append(f"Rebuttal rounds were clamped from {requested_rounds} to {rebuttal_rounds}.")
    if max_batches != requested_batches:
        notices.append(f"Debate batches were clamped from {requested_batches} to {max_batches}.")
    panel = Panel(
        perspectives=tuple(by_id[pid] for pid in chosen),
        rebuttal_rounds=rebuttal_rounds,
        max_batches=max_batches,
        runner=runner,
        independent=runner != Runner.SEQUENTIAL,
        models=tuple(models),
    )
    return panel, notices


def cmd_panel(args: argparse.Namespace) -> int:
    run_dir, _info = load_run(args.run)
    state = load_panel_state(run_dir)
    available = [default_perspective(pid, name) for pid, name in DEFAULT_PERSPECTIVES]
    available += [e.perspective for e in state.extensions if e.status == ExtensionStatus.SELECTED and e.perspective]
    requested = [p for item in (args.perspectives or []) for p in item.split(",") if p]
    models = []
    for item in args.models or []:
        role, _, model = item.partition("=")
        if not role or not model:
            raise UsageFailure(f"--models expects ROLE=MODEL, got {item!r}")
        models.append(ModelAssignment(role=role, model=model))
    panel, notices = configure_panel(available, requested or None, args.rounds, args.batches, args.runner, models)
    state = dataclasses.replace(state, panel=panel, notices=tuple(notices))
    write_json(run_dir / "panel.json", state.to_json(), args.dry_run)
    if not args.dry_run:
        print(dumps(panel.to_json()), end="")
        for notice in notices:
            print(f"notice: {notice}", file=sys.stderr)
    return EXIT_OK


def load_panel(run_dir: Path) -> tuple[Panel, PanelState]:
    state = load_panel_state(run_dir)
    if state.panel is None:
        raise PreconditionFailure("panel.json has no panel; run `panel.py panel` first")
    return state.panel, state


# ---------------------------------------------------------------------------
# merge: clustering and batching (mirrored in the Workflow script's PURE section)
# ---------------------------------------------------------------------------


def cluster_candidates(candidates: Iterable[CandidateFinding]) -> list[Cluster]:
    """Cluster candidates in the same file whose line ranges are within three lines (protocol.md section 7)."""
    by_file: dict[str, list[CandidateFinding]] = {}
    for candidate in candidates:
        by_file.setdefault(candidate.file, []).append(candidate)
    clusters: list[Cluster] = []
    for file in sorted(by_file):
        ordered = sorted(by_file[file], key=lambda c: (c.line_start, c.line_end, c.id))
        groups: list[list[CandidateFinding]] = []
        max_end = 0
        for candidate in ordered:
            if groups and candidate.line_start <= max_end + CLUSTER_DISTANCE:
                groups[-1].append(candidate)
                max_end = max(max_end, candidate.line_end)
            else:
                groups.append([candidate])
                max_end = candidate.line_end
        for group in groups:
            n = len(clusters) + 1
            clusters.append(
                Cluster(
                    id=f"C{n}",
                    suggested_finding_id=f"F{n}",
                    file=file,
                    line_start=min(c.line_start for c in group),
                    line_end=max(c.line_end for c in group),
                    members=tuple(c.id for c in group),
                )
            )
    return clusters


def batch_clusters(clusters: Sequence[Cluster], max_batches: int) -> list[Batch]:
    """Group clusters by file into at most `max_batches` batches (protocol.md section 7)."""
    by_file: dict[str, list[str]] = {}
    for cluster in clusters:
        by_file.setdefault(cluster.file, []).append(cluster.id)
    slots: list[list[str]] = [[] for _ in range(max(1, max_batches))]
    for file in sorted(by_file, key=lambda f: (-len(by_file[f]), f)):
        target = min(range(len(slots)), key=lambda i: (len(slots[i]), i))
        slots[target].extend(by_file[file])
    order = {cluster.id: index for index, cluster in enumerate(clusters)}
    batches = [sorted(slot, key=order.__getitem__) for slot in slots if slot]
    return [Batch(batch=index + 1, clusters=tuple(ids)) for index, ids in enumerate(batches)]


def carried_stances(rounds: Sequence[Sequence[Position]], upto: int) -> dict[tuple[str, str], str]:
    """Each member's latest stance per finding over rounds 0..upto."""
    stances: dict[tuple[str, str], str] = {}
    for positions in rounds[: upto + 1]:
        for position in positions:
            stances[(position.member, position.finding_id)] = position.stance
    return stances


def changed_members(rounds: Sequence[Sequence[Position]], k: int) -> list[str]:
    """Members whose carried stance on any finding changed in round k (k >= 1)."""
    before, after = carried_stances(rounds, k - 1), carried_stances(rounds, k)
    return sorted({member for (member, finding), stance in after.items() if before.get((member, finding)) != stance})


def members_to_call(rounds: Sequence[Sequence[Position]], k: int) -> list[str]:
    """Members called in round k + 1 (protocol.md section 8).

    These are the members whose stance changed in round k, plus every perspective that currently accepts a
    finding on which some member newly challenged in round k, so that a new objection can be answered.
    """
    before, after = carried_stances(rounds, k - 1), carried_stances(rounds, k)
    changed = {key for key, stance in after.items() if before.get(key) != stance}
    challenged = {finding for (member, finding) in changed if after[(member, finding)] == Stance.CHALLENGE}
    responders = {
        member
        for (member, finding), stance in after.items()
        if finding in challenged and stance == Stance.ACCEPT and member != DEFENDER_ID
    }
    return sorted({member for member, _ in changed} | responders)


def debate_stopped(rounds: Sequence[Sequence[Position]], k: int) -> bool:
    """True when no stance changed in round k (protocol.md section 8)."""
    return k >= 1 and not changed_members(rounds, k)


def stop_round(rounds: Sequence[Sequence[Position]], rebuttal_rounds: int) -> int:
    """The last round a batch runs, given its recorded rounds."""
    for k in range(1, min(rebuttal_rounds, len(rounds) - 1) + 1):
        if debate_stopped(rounds, k):
            return k
    return min(rebuttal_rounds, max(len(rounds) - 1, 0))


def load_candidates(run_dir: Path) -> list[CandidateMessage]:
    messages = []
    for path in sorted((run_dir / "candidates").glob("*.json")):
        data = read_json(path)
        require_valid("candidate-findings", data, str(path))
        messages.append(CandidateMessage.from_json(data))
    return messages


def merge_plan(candidates: Sequence[CandidateFinding], max_batches: int) -> MergePlan:
    clusters = cluster_candidates(candidates)
    return MergePlan(clusters=tuple(clusters), batches=tuple(batch_clusters(clusters, max_batches)))


def split_finding_id(batch: int, n: int) -> str:
    """Identifier of the n-th finding created by a split in a batch: batch b reserves F(1000 b + 1) onward."""
    return f"F{SPLIT_ID_BLOCK * batch + n}"


def cmd_merge(args: argparse.Namespace) -> int:
    run_dir, _info = load_run(args.run)
    panel, _state = load_panel(run_dir)
    candidates = [f for m in load_candidates(run_dir) for f in m.findings]
    print(dumps(merge_plan(candidates, panel.max_batches).to_json()), end="")
    return EXIT_OK


def cmd_debate_status(args: argparse.Namespace) -> int:
    run_dir, _info = load_run(args.run)
    if args.round < 1:
        raise UsageFailure("--round must be a rebuttal round, 1 or later")
    rounds = load_debate(run_dir).get(args.batch, [])
    if len(rounds) <= args.round:
        raise PreconditionFailure(f"batch {args.batch} has no recorded positions for round {args.round}")
    stopped = debate_stopped(rounds, args.round)
    status = DebateStatus(
        batch=args.batch,
        round=args.round,
        stopped=stopped,
        call=() if stopped else tuple(members_to_call(rounds, args.round)),
    )
    print(dumps(dataclasses.asdict(status)), end="")
    return EXIT_OK


# ---------------------------------------------------------------------------
# ingest
# ---------------------------------------------------------------------------


def cmd_ingest(args: argparse.Namespace) -> int:
    run_dir, _info = load_run(args.run)
    result = read_json(Path(args.file))
    if not isinstance(result, dict):
        raise ValidationFailure("the Workflow result is not a JSON object")
    notices = load_notices(run_dir)
    written: list[tuple[Path, Any]] = []

    def accept(schema: str, message: Any, target: Path, role: str) -> None:
        errors = validate_message(schema, message)
        if errors:
            notices.append(f"The {role} message was dropped because it failed validation: {errors[0]}")
            for error in errors:
                print(f"invalid {role}: {error}", file=sys.stderr)
            return
        written.append((target, message))

    for message in result.get("candidates", []):
        perspective = message.get("perspective", "unknown") if isinstance(message, dict) else "unknown"
        accept(
            "candidate-findings", message, run_dir / "candidates" / f"{perspective}.json", f"{perspective} candidates"
        )
    for message in result.get("merge", []):
        batch = message.get("batch", 0) if isinstance(message, dict) else 0
        accept("merge-ruling", message, run_dir / "merge" / f"batch-{batch}.json", f"moderator merge (batch {batch})")
    for entry in result.get("debate", []):
        if not isinstance(entry, dict) or "message" not in entry or "batch" not in entry:
            notices.append("A debate entry without batch and message was dropped.")
            continue
        message, batch = entry["message"], entry["batch"]
        member = message.get("member", "unknown") if isinstance(message, dict) else "unknown"
        round_ = message.get("round", 0) if isinstance(message, dict) else 0
        target = run_dir / "debate" / f"batch-{batch}" / f"round-{round_}" / f"{member}.json"
        accept("debate-positions", message, target, f"{member} debate (batch {batch}, round {round_})")
    for message in result.get("notes", []):
        batch = message.get("batch", 0) if isinstance(message, dict) else 0
        accept(
            "moderator-notes", message, run_dir / "notes" / f"batch-{batch}.json", f"moderator notes (batch {batch})"
        )
    for role in result.get("dropped", []):
        notices.append(f"The output of {role} was dropped after failing validation twice.")

    for target, message in written:
        write_json(target, message, args.dry_run)
    write_json(run_dir / "notices.json", notices, args.dry_run)
    if not args.dry_run:
        print(f"ingested {len(written)} messages into {run_dir}")
    return EXIT_OK


# ---------------------------------------------------------------------------
# adjudicate
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Outcome:
    label: str | None
    rejection: str | None


def unanswered_objection(positions: Sequence[Position], perspective_ids: set[str]) -> bool:
    """True when a defender objection on the finding is unanswered (data-model.md, Position).

    An objection is answered when a perspective position in a later round lists a defender position on the
    finding in `answers` and the defender does not challenge again in a round after that answer. So the
    objection is unanswered when the defender's latest stance is `challenge` and either no perspective has
    answered any defender position, or the defender challenged again in a round after the latest answer.
    """
    defender = [p for p in positions if p.member == DEFENDER_ID]
    if not defender or max(defender, key=lambda p: p.round).stance != Stance.CHALLENGE:
        return False
    defender_ids = {p.position_id for p in defender}
    answer_rounds = [
        p.round
        for p in positions
        if p.member in perspective_ids
        and any(a in defender_ids and int(a.rsplit(":", 1)[1]) < p.round for a in p.answers)
    ]
    if not answer_rounds:
        return True
    latest_answer = max(answer_rounds)
    return any(p.stance == Stance.CHALLENGE and p.round > latest_answer for p in defender)


def latest_stances(positions: Sequence[Position]) -> dict[str, str]:
    stances: dict[str, str] = {}
    for position in sorted(positions, key=lambda p: p.round):
        stances[position.member] = position.stance
    return stances


def adjudicate_finding(
    finding: MergedFinding, positions: Sequence[Position], perspective_ids: Sequence[str]
) -> Outcome:
    """Apply the six rules of data-model.md section 3, in order."""
    for position in positions:
        if position.stance == Stance.WITHDRAW and position.member not in finding.raised_by:
            raise ValidationFailure(
                f"{position.position_id}: withdraw is valid only from a raiser of {finding.id} "
                f"({', '.join(finding.raised_by)})"
            )
    ids = set(perspective_ids)
    stances = latest_stances(positions)
    for raiser in finding.raised_by:
        stances.setdefault(raiser, Stance.ACCEPT)
    perspective_stances = {pid: stances.get(pid) for pid in perspective_ids}
    if finding.raised_by and all(stances.get(r) == Stance.WITHDRAW for r in finding.raised_by):
        return Outcome(None, "withdrawn")
    objection = unanswered_objection(positions, ids)
    others_accept = any(s == Stance.ACCEPT for pid, s in perspective_stances.items() if pid not in finding.raised_by)
    if not others_accept and objection:
        return Outcome(None, "unsupported")
    if finding.trigger is None or finding.wrong_output is None:
        return Outcome(AgreementLabel.CONTESTED, None)
    accepts = sum(1 for s in perspective_stances.values() if s == Stance.ACCEPT)
    # A withdrawing co-raiser dissents as a challenger does; consensus also needs a second accepting perspective,
    # so that no finding is reported as consensus on its raiser's word alone (FR-013).
    dissent = any(s in (Stance.CHALLENGE, Stance.WITHDRAW) for s in perspective_stances.values())
    if not dissent and not objection and accepts >= 2:
        return Outcome(AgreementLabel.CONSENSUS, None)
    if accepts * 2 > len(perspective_ids):
        return Outcome(AgreementLabel.MAJORITY, None)
    return Outcome(AgreementLabel.CONTESTED, None)


def load_merge_rulings(run_dir: Path) -> list[MergeRuling]:
    rulings = []
    for path in sorted((run_dir / "merge").glob("batch-*.json")):
        data = read_json(path)
        require_valid("merge-ruling", data, str(path))
        rulings.append(MergeRuling.from_json(data))
    return rulings


def load_debate(run_dir: Path) -> dict[int, list[list[Position]]]:
    """Positions per batch, as a list of rounds."""
    debate: dict[int, list[list[Position]]] = {}
    for batch_dir in sorted((run_dir / "debate").glob("batch-*")):
        batch = int(batch_dir.name.split("-", 1)[1])
        rounds: dict[int, list[Position]] = {}
        for path in sorted(batch_dir.glob("round-*/*.json")):
            data = read_json(path)
            require_valid("debate-positions", data, str(path))
            message = DebateMessage.from_json(data)
            rounds.setdefault(message.round, []).extend(message.positions)
        debate[batch] = [rounds.get(k, []) for k in range(max(rounds) + 1)] if rounds else []
    return debate


def load_notes(run_dir: Path) -> dict[str, ModeratorNote]:
    notes: dict[str, ModeratorNote] = {}
    for path in sorted((run_dir / "notes").glob("batch-*.json")):
        data = read_json(path)
        require_valid("moderator-notes", data, str(path))
        for note in NotesMessage.from_json(data).notes:
            notes[note.finding_id] = note
    return notes


def adjudicate(
    rulings: Sequence[MergeRuling],
    debate: dict[int, list[list[Position]]],
    notes: dict[str, ModeratorNote],
    perspective_ids: Sequence[str],
    candidate_severity: dict[str, str],
) -> Adjudication:
    findings: list[Finding] = []
    rejected: list[RejectedFinding] = []
    records: list[DebateRecord] = []
    notices: list[str] = []
    errors: list[str] = []
    seen: set[str] = set()
    for ruling in rulings:
        rounds = debate.get(ruling.batch, [])
        for merged in ruling.findings:
            if merged.id in seen:
                errors.append(f"merged finding {merged.id} appears in more than one merge ruling")
                continue
            seen.add(merged.id)
            member_ranks = [Severity.RANK[candidate_severity[m]] for m in merged.members if m in candidate_severity]
            if member_ranks and Severity.RANK[merged.severity] > min(member_ranks) and not merged.severity_reason:
                errors.append(
                    f"{merged.id}: severity lowered below the highest member severity without severity_reason"
                )
            positions = tuple(p for r in rounds for p in r if p.finding_id == merged.id)
            records.append(
                DebateRecord(
                    finding_id=merged.id,
                    positions=positions,
                    rounds_run=(max(p.round for p in positions) + 1) if positions else 0,
                )
            )
            note = notes.get(merged.id)
            concrete = merged.trigger is not None and merged.wrong_output is not None
            if note is not None and not concrete and not note.no_trigger_reason:
                errors.append(
                    f"{merged.id}: moderator note lacks no_trigger_reason although trigger or wrong_output is null"
                )
            if note is None:
                notices.append(f"No moderator note was recorded for {merged.id}.")
            if not positions:
                notices.append(f"{merged.id} was not debated: no panel member recorded a position on it.")
            try:
                outcome = adjudicate_finding(merged, positions, perspective_ids)
            except ValidationFailure as exc:
                errors.append(str(exc))
                continue
            if outcome.label is None:
                reason = outcome.rejection or "unsupported"
                if note is not None and note.rejection_reason.strip() and note.rejection_reason.strip() != NOT_REJECTED:
                    reason = note.rejection_reason
                rejected.append(
                    RejectedFinding(
                        finding_id=merged.id, summary=merged.summary, raised_by=merged.raised_by, reason=reason
                    )
                )
                continue
            extra: dict[str, Any] = {}
            if outcome.label == AgreementLabel.CONTESTED:
                extra["argument_for"] = note.argument_for if note else "No moderator note was recorded."
                extra["argument_against"] = note.argument_against if note else "No moderator note was recorded."
                extra["deciding_assumption"] = note.deciding_assumption if note else None
            if not concrete:
                extra["no_trigger_reason"] = (
                    note.no_trigger_reason
                    if note and note.no_trigger_reason
                    else "No member supplied a concrete trigger."
                )
            findings.append(
                Finding(
                    id=merged.id,
                    members=merged.members,
                    raised_by=merged.raised_by,
                    batch=merged.batch,
                    file=merged.file,
                    line_start=merged.line_start,
                    line_end=merged.line_end,
                    dimension=merged.dimension,
                    severity=merged.severity,
                    summary=merged.summary,
                    trigger=merged.trigger,
                    wrong_output=merged.wrong_output,
                    fix=merged.fix,
                    label=outcome.label,
                    severity_reason=merged.severity_reason,
                    **extra,
                )
            )
    if errors:
        raise ValidationFailure("adjudication found protocol violations", errors)
    merged_members = {member for ruling in rulings for merged in ruling.findings for member in merged.members}
    unmerged = sorted(set(candidate_severity) - merged_members)
    if unmerged:
        notices.append(
            "These candidate findings were not merged into any debated finding and are not reported: "
            + ", ".join(unmerged)
            + "."
        )
    return Adjudication(
        findings=tuple(order_findings(findings)),
        rejected=tuple(rejected),
        records=tuple(records),
        notices=tuple(notices),
    )


def order_findings(findings: Iterable[Finding]) -> list[Finding]:
    return sorted(
        findings,
        key=lambda f: (AgreementLabel.RANK[f.label], Severity.RANK[f.severity], f.file, f.line_start, f.id),
    )


def cmd_adjudicate(args: argparse.Namespace) -> int:
    run_dir, _info = load_run(args.run)
    panel, _state = load_panel(run_dir)
    candidate_severity = {f.id: f.severity for m in load_candidates(run_dir) for f in m.findings}
    result = adjudicate(
        load_merge_rulings(run_dir),
        load_debate(run_dir),
        load_notes(run_dir),
        [p.id for p in panel.perspectives],
        candidate_severity,
    )
    write_json(run_dir / "adjudication.json", result.to_json(), args.dry_run)
    if not args.dry_run:
        counts = {label: sum(1 for f in result.findings if f.label == label) for label in AgreementLabel.VALUES}
        print(
            f"{counts['consensus']} consensus, {counts['majority']} majority, {counts['contested']} contested, "
            f"{len(result.rejected)} rejected"
        )
    return EXIT_OK


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------


def build_report(
    scope: ReviewScope,
    state: PanelState,
    adjudication: Adjudication | None,
    candidates: Sequence[CandidateMessage],
    run_notices: Sequence[str],
) -> ReviewReport:
    panel = state.panel
    assert panel is not None
    notices: list[str] = []
    if not panel.independent:
        notices.append(REDUCED_INDEPENDENCE_NOTICE)
    other = sorted({Path(f.path).suffix or Path(f.path).name for f in scope.files if f.language == Language.OTHER})
    if other:
        notices.append(
            "Files in languages other than Python and TypeScript were reviewed without worked examples: "
            + ", ".join(other)
            + "."
        )
    notices.extend(state.notices)
    notices.extend(run_notices)
    findings: list[Finding] = []
    rejected: list[RejectedFinding] = []
    if adjudication is not None:
        notices.extend(adjudication.notices)
        in_scope = {f.path for f in scope.files}
        for finding in adjudication.findings:
            if finding.file in in_scope:
                findings.append(finding)
            else:
                notices.append(f"Finding {finding.id} on {finding.file} lies outside the scope and was not reported.")
        rejected = list(adjudication.rejected)
    checked = [item for message in candidates for item in message.checked_items]
    checked.sort(key=lambda c: (c.file, c.line_start, c.line_end, c.dimension))
    return ReviewReport(
        scope=scope,
        panel=panel,
        extensions=state.extensions,
        findings=tuple(order_findings(findings)),
        rejected=tuple(rejected),
        checked_items=tuple(checked),
        unreviewed=scope.excluded,
        notices=tuple(dict.fromkeys(notices)),
    )


def failure_scenario(finding: Finding) -> str:
    if finding.trigger is not None and finding.wrong_output is not None:
        return f"{finding.trigger} produces {finding.wrong_output}"
    return f"No concrete trigger established: {finding.no_trigger_reason or 'no reason was recorded.'}"


def report_findings(findings: Sequence[Finding]) -> list[ReportFinding]:
    """The ReportFindings mapping of contracts/report.md section 3."""
    out = []
    for finding in findings:
        summary = finding.summary
        if finding.label == AgreementLabel.CONTESTED:
            summary += f" Contested. For: {finding.argument_for} Against: {finding.argument_against}"
            if finding.deciding_assumption:
                summary += f" Decided by: {finding.deciding_assumption}"
        short = f"{finding.label.capitalize()}: {finding.summary}"
        out.append(
            ReportFinding(
                file=finding.file,
                line=finding.line_start,
                summary=summary,
                failure_scenario=failure_scenario(finding),
                category=finding.dimension,
                verdict="PLAUSIBLE" if finding.label == AgreementLabel.CONTESTED else "CONFIRMED",
                short_summary=short[:60],
            )
        )
    return out


def _cell(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, (list, tuple)):
        value = ", ".join(str(v) for v in value)
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ").strip() or "n/a"


def _table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines += ["| " + " | ".join(_cell(v) for v in row) + " |" for row in rows]
    return lines


def render_markdown(report: ReviewReport) -> str:
    panel = report.panel
    lines = ["# Scientific review", "", "## Scope", "", report.scope.note, ""]
    lines.append(
        f"Runner: `{panel.runner}`. The perspectives were "
        + ("independent agents." if panel.independent else "not independent agents.")
    )
    lines += ["", "## Panel", ""]
    for perspective in panel.perspectives:
        lines.append(f"- {perspective.name} (`{perspective.id}`, source `{perspective.source}`)")
    lines.append("- Defender and moderator")
    lines += ["", f"Rebuttal rounds: {panel.rebuttal_rounds}. Debate batches: at most {panel.max_batches}."]
    if panel.models:
        lines.append("Models: " + ", ".join(f"{m.role}: {m.model}" for m in panel.models) + ".")
    lines += ["", "## Extensions", ""]
    if report.extensions:
        for extension in report.extensions:
            entry = f"- `{extension.id}` ({extension.plugin}): {extension.status}"
            if extension.status_reason:
                entry += f"; {extension.status_reason}"
            if extension.adds:
                entry += f" It would add: {extension.adds}."
            lines.append(entry)
    else:
        lines.append("No extensions were discovered or recommended.")
    if not report.scope.files:
        lines += ["", NO_REVIEWABLE_CODE, ""]
        return "\n".join(lines)

    lines += ["", "## Findings", ""]
    headers = ["Location", "Dimension", "Severity", "Summary", "Trigger", "Wrong output", "Fix", "Raised by", "Label"]
    for label in AgreementLabel.VALUES:
        lines += [f"### {label.capitalize()}", ""]
        subset = [f for f in report.findings if f.label == label]
        if not subset:
            lines += ["None.", ""]
            continue
        table_headers = list(headers)
        if label == AgreementLabel.CONTESTED:
            table_headers += ["Argument for", "Argument against", "Deciding assumption", "No-trigger reason"]
        rows = []
        for f in subset:
            row: list[Any] = [
                f"{f.file}:{f.line_start}" + (f"-{f.line_end}" if f.line_end != f.line_start else ""),
                f.dimension,
                f.severity,
                f"{f.id}: {f.summary}",
                f.trigger,
                f.wrong_output,
                f.fix,
                f.raised_by,
                f.label,
            ]
            if label == AgreementLabel.CONTESTED:
                row += [f.argument_for, f.argument_against, f.deciding_assumption, f.no_trigger_reason]
            rows.append(row)
        lines += [*_table(table_headers, rows), ""]

    lines += ["## Rejected findings", ""]
    if report.rejected:
        lines += _table(
            ["Id", "Summary", "Raised by", "Reason"],
            [[r.finding_id, r.summary, r.raised_by, r.reason] for r in report.rejected],
        )
    else:
        lines.append("None.")
    lines += ["", "## Checked and found correct", ""]
    if report.checked_items:
        lines += _table(
            ["Location", "Dimension", "Note"],
            [[f"{c.file}:{c.line_start}-{c.line_end}", c.dimension, c.note] for c in report.checked_items],
        )
    else:
        lines.append("None recorded.")
    lines += ["", "## Not reviewed", ""]
    if report.unreviewed:
        lines += _table(["Path", "Reason"], [[u.path, u.reason] for u in report.unreviewed])
    else:
        lines.append("Every file in the requested scope was reviewed.")
    lines += ["", "## Notices", ""]
    lines += [f"- {n}" for n in report.notices] if report.notices else ["None."]
    lines.append("")
    return "\n".join(lines)


def cmd_report(args: argparse.Namespace) -> int:
    run_dir, _info = load_run(args.run)
    scope = load_scope(run_dir)
    _panel, state = load_panel(run_dir)
    adjudication_path = run_dir / "adjudication.json"
    adjudication = Adjudication.from_json(read_json(adjudication_path)) if adjudication_path.is_file() else None
    if adjudication is None and scope.files:
        raise PreconditionFailure("adjudication.json does not exist; run `panel.py adjudicate` first")
    candidates = load_candidates(run_dir) if (run_dir / "candidates").is_dir() else []
    report = build_report(scope, state, adjudication, candidates, load_notices(run_dir))
    data = report.to_json()
    require_valid("report", data, "the report")
    write_json(run_dir / "report.json", data, args.dry_run)
    if args.format == "markdown":
        print(render_markdown(report), end="")
    else:
        print(dumps({**data, "report_findings": [r.to_json() for r in report_findings(report.findings)]}), end="")
    return EXIT_OK


# ---------------------------------------------------------------------------
# validate and the command line
# ---------------------------------------------------------------------------


def cmd_validate(args: argparse.Namespace) -> int:
    data = read_json(Path(args.file))
    errors = validate_message(args.schema, data)
    if errors:
        for error in errors:
            print(f"error: {error}")
        return EXIT_INVALID
    print(f"{args.file}: valid {args.schema} message")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="panel.py", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name: str, handler: Any, help_text: str, dry_run: bool = True, run: bool = True) -> argparse.ArgumentParser:
        command = sub.add_parser(name, help=help_text)
        command.set_defaults(handler=handler)
        if run:
            command.add_argument("--run", required=True, help="run directory created by init")
        if dry_run:
            command.add_argument("--dry-run", action="store_true", help="print what would be written; change nothing")
        return command

    init = add("init", cmd_init, "create a run directory under the system temp dir", run=False)
    init.add_argument("--project", required=True, help="the reviewed project")

    scope = add("scope", cmd_scope, "resolve the review scope into scope.json")
    scope.add_argument("--mode", required=True, choices=(ScopeMode.BRANCH, ScopeMode.REPOSITORY, ScopeMode.PATHS))
    scope.add_argument("--baseline", help="git ref or range (branch mode only; recorded as explicit)")
    scope.add_argument("--path", action="append", help="path to review (paths mode; repeatable)")
    scope.add_argument("--budget", type=int, help=f"maximum lines to review (default {DEFAULT_BUDGET})")

    select = add("select-extensions", cmd_select_extensions, "select domain extensions for the scope")
    select.add_argument("--declaration", action="append", help="path of an extension.json (repeatable)")

    panel = add("panel", cmd_panel, "configure the panel into panel.json")
    panel.add_argument("--perspectives", action="append", help="perspective ids, comma-separated or repeated")
    panel.add_argument("--rounds", type=int, help=f"rebuttal rounds ({MIN_ROUNDS} to {MAX_ROUNDS})")
    panel.add_argument("--batches", type=int, help=f"maximum debate batches ({MIN_BATCHES} to {MAX_BATCHES})")
    panel.add_argument("--runner", required=True, choices=Runner.VALUES)
    panel.add_argument("--models", action="append", help="ROLE=MODEL (Workflow runner only; repeatable)")

    validate = add("validate", cmd_validate, "validate one panel message", dry_run=False, run=False)
    validate.add_argument("--schema", required=True, choices=SCHEMA_NAMES)
    validate.add_argument("file")

    ingest = add("ingest", cmd_ingest, "write a Workflow PanelRun result into the run directory")
    ingest.add_argument("file")

    add("merge", cmd_merge, "print location clusters grouped into debate batches", dry_run=False)
    status = add(
        "debate-status", cmd_debate_status, "print whether a batch's debate stops and whom to call next", dry_run=False
    )
    status.add_argument("--batch", type=int, required=True)
    status.add_argument("--round", type=int, required=True, help="the rebuttal round just completed")
    add("adjudicate", cmd_adjudicate, "compute agreement labels into adjudication.json")
    report = add("report", cmd_report, "write report.json and print the report")
    report.add_argument("--format", choices=("json", "markdown"), default="markdown")
    add("clean", cmd_clean, "remove the run directory")
    notice = add("notice", cmd_notice, "add a notice for the report (for example, a missing tool)")
    notice.add_argument("text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    print("panel.py " + " ".join(argv), file=sys.stderr)
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return EXIT_USAGE if exc.code not in (0, None) else EXIT_OK
    try:
        return int(args.handler(args))
    except PanelError as exc:
        print(f"error: {exc}", file=sys.stderr)
        for detail in exc.details:
            print(f"  {detail}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    sys.exit(main())
