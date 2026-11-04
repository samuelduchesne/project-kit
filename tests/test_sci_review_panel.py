"""Unit tests for plugins/sci-review/scripts/panel.py.

Run with: uv run --no-project --python 3.12 python -m unittest discover -s tests -v
Set UPDATE_GOLDEN=1 to rewrite the golden reports after an intended change.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL_PATH = ROOT / "plugins" / "sci-review" / "scripts" / "panel.py"
FIXTURES = ROOT / "tests" / "fixtures" / "sci-review"
MESSAGES = FIXTURES / "messages"
GOLDEN = MESSAGES / "golden"
UPDATE_GOLDEN = os.environ.get("UPDATE_GOLDEN") == "1"

spec = importlib.util.spec_from_file_location("sci_review_panel", PANEL_PATH)
panel = importlib.util.module_from_spec(spec)
sys.modules["sci_review_panel"] = panel
spec.loader.exec_module(panel)

GIT = ["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid", "-c", "init.defaultBranch=main"]


@dataclass(frozen=True)
class Result:
    code: int
    out: str
    err: str


def run_panel(*argv: str) -> Result:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = panel.main(list(argv))
    return Result(code, out.getvalue(), err.getvalue())


def git(cwd: Path, *argv: str) -> str:
    return subprocess.run([*GIT, *argv], cwd=cwd, check=True, capture_output=True, text=True).stdout


def tree_snapshot(root: Path) -> dict[str, bytes]:
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file() and ".git" not in p.relative_to(root).parts
    }


class RunDirMixin(unittest.TestCase):
    """Creates a project directory and a run directory outside it."""

    def setUp(self) -> None:
        self.project = Path(tempfile.mkdtemp(prefix="sci-review-project-"))
        self.addCleanup(shutil.rmtree, self.project, True)
        self.run_dir: Path | None = None

    def init_run(self) -> Path:
        result = run_panel("init", "--project", str(self.project))
        self.assertEqual(result.code, 0, result.err)
        self.run_dir = Path(result.out.strip())
        self.addCleanup(shutil.rmtree, self.run_dir, True)
        return self.run_dir

    def run_from_scenario(self, scenario: str) -> Path:
        """Copy a golden scenario (a run-directory layout) into a fresh run directory."""
        run_dir = self.init_run()
        for item in (GOLDEN / scenario).iterdir():
            if item.name.startswith("expected"):
                continue
            target = run_dir / item.name
            if item.is_dir():
                shutil.copytree(item, target)
            else:
                shutil.copy(item, target)
        return run_dir

    def write(self, relative: str, text: str) -> Path:
        path = self.project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path


def init_repo(project: Path) -> None:
    git(project, "init", "-q")
    (project / "src").mkdir(exist_ok=True)
    (project / "src" / "base.py").write_text("def area(r):\n    return 3.14159 * r * r\n", encoding="utf-8")
    git(project, "add", ".")
    git(project, "commit", "-qm", "base")


# ---------------------------------------------------------------------------
# Foundational: data model, validator, file-writing safety (T012)
# ---------------------------------------------------------------------------


class TestModelAndValidate(RunDirMixin):
    def test_schemas_load(self) -> None:
        for name in panel.SCHEMA_NAMES:
            with self.subTest(name=name):
                schema = panel.load_schema(name)
                self.assertEqual(schema["type"], "object")

    def test_valid_fixtures_pass(self) -> None:
        for path in sorted((MESSAGES / "valid").glob("*.json")):
            with self.subTest(path=path.name):
                result = run_panel("validate", "--schema", path.stem, str(path))
                self.assertEqual(result.code, 0, result.out)

    def test_invalid_fixtures_fail_with_named_error(self) -> None:
        expected = {
            "unknown-property": "unknown property 'confidence'",
            "line-order": "line_end 10 is less than line_start 12",
            "unknown-dimension": "'style' is not one of",
            "empty-members": "fewer than 1 items",
            "empty-reason": "shorter than 1 characters",
        }
        for path in sorted((MESSAGES / "invalid").glob("*.json")):
            with self.subTest(path=path.name):
                case = json.loads(path.read_text(encoding="utf-8"))
                message = Path(tempfile.mkdtemp()) / "message.json"
                self.addCleanup(shutil.rmtree, message.parent, True)
                message.write_text(json.dumps(case["message"]), encoding="utf-8")
                result = run_panel("validate", "--schema", case["schema"], str(message))
                self.assertEqual(result.code, 1)
                self.assertIn(expected[path.stem], result.out)

    def _report(self) -> dict:
        report_path = GOLDEN / "full" / "expected-report.json"
        return json.loads(report_path.read_text(encoding="utf-8"))

    def test_contested_without_argument_fails(self) -> None:
        report = self._report()
        contested = next(f for f in report["findings"] if f["label"] == "contested")
        del contested["argument_for"]
        errors = panel.validate_message("report", report)
        self.assertTrue(any("argument_for" in e for e in errors), errors)

    def test_consensus_with_null_trigger_fails(self) -> None:
        report = self._report()
        consensus = next(f for f in report["findings"] if f["label"] == "consensus")
        consensus["trigger"] = None
        errors = panel.validate_message("report", report)
        self.assertTrue(any("trigger" in e for e in errors), errors)

    def test_records_round_trip_and_reject_bad_values(self) -> None:
        data = json.loads((MESSAGES / "valid" / "candidate-findings.json").read_text(encoding="utf-8"))
        message = panel.CandidateMessage.from_json(data)
        self.assertEqual(message.to_json(), data)
        bad = dict(data["findings"][0], dimension="style")
        with self.assertRaises(panel.ValidationFailure):
            panel.CandidateFinding.from_json(bad)
        bad = dict(data["findings"][0], line_start=9, line_end=3)
        with self.assertRaises(panel.ValidationFailure):
            panel.CandidateFinding.from_json(bad)

    def test_init_dry_run_writes_nothing(self) -> None:
        before = set(Path(tempfile.gettempdir()).glob("sci-review-*"))
        result = run_panel("init", "--project", str(self.project), "--dry-run")
        self.assertEqual(result.code, 0)
        self.assertIn("[dry-run] would create", result.out)
        self.assertEqual(before, set(Path(tempfile.gettempdir()).glob("sci-review-*")))

    def test_clean_dry_run_keeps_directory(self) -> None:
        run_dir = self.init_run()
        result = run_panel("clean", "--run", str(run_dir), "--dry-run")
        self.assertEqual(result.code, 0)
        self.assertIn(str(run_dir), result.out)
        self.assertTrue(run_dir.is_dir())
        self.assertEqual(run_panel("clean", "--run", str(run_dir)).code, 0)
        self.assertFalse(run_dir.exists())

    def test_init_refuses_run_directory_inside_project(self) -> None:
        result = run_panel("init", "--project", tempfile.gettempdir())
        self.assertEqual(result.code, 3)
        self.assertIn("inside the project", result.err)

    def test_usage_error_exit_code(self) -> None:
        self.assertEqual(run_panel("validate", "--schema", "nope", "x.json").code, 2)
        self.assertEqual(run_panel("frobnicate").code, 2)


# ---------------------------------------------------------------------------
# User Story 1: scope, panel, merge, adjudication, report, ingest
# ---------------------------------------------------------------------------


class TestScopeBranch(RunDirMixin):
    def setUp(self) -> None:
        super().setUp()
        init_repo(self.project)
        git(self.project, "checkout", "-qb", "feature")
        self.write("src/model.py", "import math\n\n\ndef f(x):\n    return math.log(x)\n")
        self.write("src/heat.ts", "export const k = 1;\n")
        self.write("node_modules/pkg/index.js", "module.exports = 1;\n")
        self.write("uv.lock", "version = 1\n")
        self.write("src/gen.py", "X = 1\n")
        self.write(".gitattributes", "src/gen.py linguist-generated\n")
        git(self.project, "add", ".")
        git(self.project, "commit", "-qm", "feature work")
        self.write("src/base.py", "def area(r):\n    return 3.14159 * r * r\n\n\ndef perimeter(r):\n    return 2 * r\n")
        self.write("src/new_untracked.py", "Y = 2\nZ = 3\n")

    def scope(self, *extra: str) -> dict:
        run_dir = self.init_run()
        result = run_panel("scope", "--run", str(run_dir), "--mode", "branch", *extra)
        self.assertEqual(result.code, 0, result.err)
        return json.loads((run_dir / "scope.json").read_text(encoding="utf-8"))

    def test_branch_scope(self) -> None:
        before = tree_snapshot(self.project)
        scope = self.scope()
        self.assertEqual(scope["mode"], "branch")
        self.assertEqual(scope["base"], git(self.project, "rev-parse", "main").strip())
        files = {f["path"]: f for f in scope["files"]}
        self.assertEqual(files["src/model.py"]["language"], "python")
        self.assertEqual(files["src/model.py"]["line_ranges"], [[1, 5]])
        self.assertEqual(files["src/heat.ts"]["language"], "typescript")
        self.assertEqual(files["src/base.py"]["line_ranges"], [[3, 6]])
        self.assertEqual(files["src/new_untracked.py"]["line_ranges"], [[1, 2]])
        self.assertEqual(files[".gitattributes"]["language"], "other")
        excluded = {e["path"]: e["reason"] for e in scope["excluded"]}
        self.assertIn("vendored", excluded["node_modules/pkg/index.js"])
        self.assertIn("lock file", excluded["uv.lock"])
        self.assertIn("generated", excluded["src/gen.py"])
        self.assertEqual(before, tree_snapshot(self.project))

    def test_explicit_baseline(self) -> None:
        scope = self.scope("--baseline", "main")
        self.assertEqual(scope["mode"], "explicit")

    def test_budget_records_remainder(self) -> None:
        scope = self.scope("--budget", "4")
        excluded = {e["path"]: e["reason"] for e in scope["excluded"]}
        self.assertIn("over budget", excluded.values())
        self.assertIn("budget", scope["note"])

    def test_scope_dry_run(self) -> None:
        run_dir = self.init_run()
        result = run_panel("scope", "--run", str(run_dir), "--mode", "branch", "--dry-run")
        self.assertEqual(result.code, 0, result.err)
        self.assertFalse((run_dir / "scope.json").exists())

    def test_no_base_exits_3(self) -> None:
        git(self.project, "branch", "-qm", "main", "trunk")
        result = run_panel("scope", "--run", str(self.init_run()), "--mode", "branch")
        self.assertEqual(result.code, 3)
        self.assertIn("--baseline", result.err)

    def test_on_default_branch_exits_3(self) -> None:
        git(self.project, "checkout", "-q", "main")
        result = run_panel("scope", "--run", str(self.init_run()), "--mode", "branch")
        self.assertEqual(result.code, 3)

    def test_paths_with_spaces_and_non_ascii_characters(self) -> None:
        self.write("src/my model.py", "a = 1\n")
        self.write("src/caf\u00e9.py", "b = 2\n")
        git(self.project, "add", ".")
        git(self.project, "commit", "-qm", "names")
        self.write("src/\u00fcnt racked.py", "c = 3\n")
        scope = self.scope()
        files = {f["path"]: f["line_ranges"] for f in scope["files"]}
        for name in ("src/my model.py", "src/caf\u00e9.py", "src/\u00fcnt racked.py"):
            self.assertEqual(files.get(name), [[1, 1]], name)
        self.assertFalse([e for e in scope["excluded"] if e["reason"] == "deleted"])

    def test_unquote_git_path(self) -> None:
        self.assertEqual(panel.unquote_git_path('"caf\\303\\251.py"'), "caf\u00e9.py")
        self.assertEqual(panel.unquote_git_path('"a\\"q\\\\b.py"'), 'a"q\\b.py')
        self.assertEqual(panel.unquote_git_path("plain name.py"), "plain name.py")

    def test_range_baseline_must_end_at_head(self) -> None:
        self.assertEqual(self.scope("--baseline", "main..HEAD")["mode"], "explicit")
        self.assertEqual(self.scope("--baseline", "main...feature")["mode"], "explicit")
        git(self.project, "branch", "-q", "other", "main")
        result = run_panel("scope", "--run", str(self.init_run()), "--mode", "branch", "--baseline", "main..other")
        self.assertEqual(result.code, 2)
        self.assertIn("always covers HEAD", result.err)


class TestScopeNonGit(RunDirMixin):
    def test_non_git_branch_mode_exits_3_and_offers_modes(self) -> None:
        self.write("a.py", "x = 1\n")
        result = run_panel("scope", "--run", str(self.init_run()), "--mode", "branch")
        self.assertEqual(result.code, 3)
        self.assertIn("--mode repository", result.err)
        self.assertIn("--mode paths", result.err)


def perspectives(ids: list[str]) -> list:
    names = dict(panel.DEFAULT_PERSPECTIVES)
    return [panel.default_perspective(pid, names.get(pid, pid)) for pid in ids]


ALL_DEFAULTS = [pid for pid, _ in panel.DEFAULT_PERSPECTIVES]


class TestPanel(RunDirMixin):
    def test_defaults(self) -> None:
        configured, notices = panel.configure_panel(perspectives(ALL_DEFAULTS), None, None, None, "claude-workflow")
        self.assertEqual([p.id for p in configured.perspectives], ALL_DEFAULTS)
        self.assertEqual((configured.rebuttal_rounds, configured.max_batches), (2, 2))
        self.assertTrue(configured.independent)
        self.assertEqual(notices, [])

    def test_clamping(self) -> None:
        configured, notices = panel.configure_panel(perspectives(ALL_DEFAULTS), ["theorist"], 9, 0, "sequential")
        self.assertEqual(len(configured.perspectives), 2)
        self.assertEqual((configured.rebuttal_rounds, configured.max_batches), (3, 1))
        self.assertFalse(configured.independent)
        self.assertEqual(len(notices), 3)
        configured, _ = panel.configure_panel(perspectives(ALL_DEFAULTS), None, -1, 7, "claude-agents")
        self.assertEqual((configured.rebuttal_rounds, configured.max_batches), (0, 4))

    def test_more_than_available_yields_all(self) -> None:
        requested = [*ALL_DEFAULTS, "astronomer"]
        configured, notices = panel.configure_panel(perspectives(ALL_DEFAULTS), requested, 2, 2, "claude-workflow")
        self.assertEqual(len(configured.perspectives), 5)
        self.assertTrue(any("astronomer" in n for n in notices))

    def test_limit_of_seven(self) -> None:
        ids = [*ALL_DEFAULTS, "d1", "d2", "d3"]
        configured, notices = panel.configure_panel(perspectives(ids), None, 2, 2, "claude-workflow")
        self.assertEqual(len(configured.perspectives), 7)
        self.assertTrue(any("limited to 7" in n for n in notices))

    def test_panel_subcommand_and_dry_run(self) -> None:
        run_dir = self.init_run()
        result = run_panel("panel", "--run", str(run_dir), "--runner", "codex-subagents", "--dry-run")
        self.assertEqual(result.code, 0, result.err)
        self.assertFalse((run_dir / "panel.json").exists())
        result = run_panel("panel", "--run", str(run_dir), "--runner", "codex-subagents", "--rounds", "1")
        self.assertEqual(result.code, 0, result.err)
        state = json.loads((run_dir / "panel.json").read_text(encoding="utf-8"))
        self.assertEqual(state["panel"]["rebuttal_rounds"], 1)
        self.assertTrue(Path(state["panel"]["perspectives"][0]["brief_path"]).is_file())


def candidate_from(data: dict):
    return panel.CandidateFinding.from_json(data)


class TestMerge(unittest.TestCase):
    def test_merge_fixtures(self) -> None:
        for path in sorted((MESSAGES / "merge").glob("*.json")):
            with self.subTest(path=path.name):
                case = json.loads(path.read_text(encoding="utf-8"))
                candidates = [candidate_from(c) for c in case["candidates"]]
                clusters = panel.cluster_candidates(candidates)
                self.assertEqual([c.to_json() for c in clusters], case["expected"]["clusters"])
                batches = panel.batch_clusters(clusters, case["max_batches"])
                self.assertEqual([b.to_json() for b in batches], case["expected"]["batches"])
                self.assertLessEqual(len(batches), case["max_batches"])

    def test_never_clusters_across_files(self) -> None:
        case = json.loads((MESSAGES / "merge" / "basic.json").read_text(encoding="utf-8"))
        for cluster in panel.cluster_candidates([candidate_from(c) for c in case["candidates"]]):
            files = {c["file"] for c in case["candidates"] if c["id"] in cluster.members}
            self.assertEqual(len(files), 1)


def debate_case(path: Path) -> tuple[dict, list[list]]:
    case = json.loads(path.read_text(encoding="utf-8"))
    rounds = [[panel.Position.from_json(p) for p in r] for r in case["rounds"]]
    return case, rounds


class TestAdjudicate(RunDirMixin):
    def test_debate_fixtures(self) -> None:
        for path in sorted((MESSAGES / "debate").glob("*.json")):
            with self.subTest(case=path.stem):
                case, rounds = debate_case(path)
                finding = panel.MergedFinding.from_json(case["finding"])
                positions = [p for r in rounds for p in r]
                outcome = panel.adjudicate_finding(finding, positions, case["perspectives"])
                self.assertEqual(outcome.label, case["expected_label"])
                self.assertEqual(outcome.rejection, case["expected_rejection"])
                self.assertEqual(panel.stop_round(rounds, case["rebuttal_rounds"]), case["expected_stop_round"])
                for k, expected in enumerate(case.get("expected_calls", []), start=1):
                    self.assertEqual(panel.members_to_call(rounds, k), expected, f"round {k + 1} calls")

    def test_withdraw_from_non_raiser_exits_1(self) -> None:
        run_dir = self.run_from_scenario("full")
        path = run_dir / "debate" / "batch-2" / "round-0" / "methodologist.json"
        message = json.loads(path.read_text(encoding="utf-8"))
        message["positions"][0]["stance"] = "withdraw"
        path.write_text(json.dumps(message), encoding="utf-8")
        result = run_panel("adjudicate", "--run", str(run_dir))
        self.assertEqual(result.code, 1)
        self.assertIn("withdraw is valid only from a raiser", result.err)

    def test_missing_no_trigger_reason_exits_1(self) -> None:
        run_dir = self.run_from_scenario("full")
        path = run_dir / "notes" / "batch-1.json"
        notes = json.loads(path.read_text(encoding="utf-8"))
        next(n for n in notes["notes"] if n["finding_id"] == "F2")["no_trigger_reason"] = None
        path.write_text(json.dumps(notes), encoding="utf-8")
        result = run_panel("adjudicate", "--run", str(run_dir))
        self.assertEqual(result.code, 1)
        self.assertIn("no_trigger_reason", result.err)

    def test_unmerged_candidates_and_undebated_findings_are_noticed(self) -> None:
        run_dir = self.run_from_scenario("full")
        path = run_dir / "merge" / "batch-1.json"
        ruling = json.loads(path.read_text(encoding="utf-8"))
        ruling["findings"] = [f for f in ruling["findings"] if f["id"] != "F6"]
        path.write_text(json.dumps(ruling), encoding="utf-8")
        shutil.rmtree(run_dir / "debate" / "batch-2")
        self.assertEqual(run_panel("adjudicate", "--run", str(run_dir)).code, 0)
        result = json.loads((run_dir / "adjudication.json").read_text(encoding="utf-8"))
        self.assertTrue(any("numerical-analyst-2" in n and "not merged" in n for n in result["notices"]))
        self.assertTrue(any(n.startswith("F3 was not debated") for n in result["notices"]))
        labels = {f["id"]: f["label"] for f in result["findings"]}
        self.assertNotEqual(labels["F4"], "consensus")

    def test_debate_status(self) -> None:
        run_dir = self.run_from_scenario("full")
        result = run_panel("debate-status", "--run", str(run_dir), "--batch", "1", "--round", "1")
        self.assertEqual(result.code, 0, result.err)
        self.assertEqual(
            json.loads(result.out), {"batch": 1, "round": 1, "stopped": False, "call": ["numerical-analyst"]}
        )
        self.assertEqual(run_panel("debate-status", "--run", str(run_dir), "--batch", "2", "--round", "1").code, 3)
        self.assertEqual(run_panel("debate-status", "--run", str(run_dir), "--batch", "1", "--round", "0").code, 2)

    def test_lowered_severity_needs_reason(self) -> None:
        run_dir = self.run_from_scenario("full")
        path = run_dir / "merge" / "batch-2.json"
        ruling = json.loads(path.read_text(encoding="utf-8"))
        ruling["findings"][0]["severity"] = "low"
        path.write_text(json.dumps(ruling), encoding="utf-8")
        result = run_panel("adjudicate", "--run", str(run_dir))
        self.assertEqual(result.code, 1)
        self.assertIn("severity_reason", result.err)

    def test_notes_attached_by_label(self) -> None:
        run_dir = self.run_from_scenario("full")
        self.assertEqual(run_panel("adjudicate", "--run", str(run_dir)).code, 0)
        result = json.loads((run_dir / "adjudication.json").read_text(encoding="utf-8"))
        for finding in result["findings"]:
            if finding["label"] == "contested":
                self.assertIn("argument_for", finding)
                self.assertIn("deciding_assumption", finding)
            else:
                self.assertNotIn("argument_for", finding)
                self.assertNotIn("deciding_assumption", finding)
        rejected = {r["finding_id"]: r["reason"] for r in result["rejected"]}
        self.assertEqual(set(rejected), {"F6"})
        self.assertIn("documented sentinel", rejected["F6"])

    def test_adjudicate_dry_run(self) -> None:
        run_dir = self.run_from_scenario("full")
        result = run_panel("adjudicate", "--run", str(run_dir), "--dry-run")
        self.assertEqual(result.code, 0, result.err)
        self.assertFalse((run_dir / "adjudication.json").exists())


SECTION_ORDER = [
    "## Scope",
    "## Panel",
    "## Extensions",
    "## Findings",
    "## Rejected findings",
    "## Checked and found correct",
    "## Not reviewed",
    "## Notices",
]


class GoldenMixin(RunDirMixin):
    def render(self, scenario: str, fmt: str = "markdown") -> tuple[Path, str]:
        run_dir = self.run_from_scenario(scenario)
        if (run_dir / "merge").is_dir():
            result = run_panel("adjudicate", "--run", str(run_dir))
            self.assertEqual(result.code, 0, result.err)
        result = run_panel("report", "--run", str(run_dir), "--format", fmt)
        self.assertEqual(result.code, 0, result.err)
        return run_dir, result.out

    def assert_golden(self, name: str, text: str) -> None:
        path = GOLDEN / name
        if UPDATE_GOLDEN:
            path.write_text(text, encoding="utf-8")
        self.assertTrue(path.is_file(), f"golden file {path} is missing; run the tests with UPDATE_GOLDEN=1")
        self.assertEqual(text, path.read_text(encoding="utf-8"))


class TestReport(GoldenMixin):
    def test_full_report_matches_golden(self) -> None:
        run_dir, markdown = self.render("full")
        self.assert_golden("full/expected-report.md", markdown)
        expected = json.loads((run_dir / "report.json").read_text(encoding="utf-8"))
        expected["panel"]["perspectives"] = [
            dict(p, brief_path=f"roles/{p['id']}.md") for p in expected["panel"]["perspectives"]
        ]
        self.assert_golden("full/expected-report.json", json.dumps(expected, indent=2) + "\n")

    def test_section_order(self) -> None:
        _run_dir, markdown = self.render("full")
        positions = [markdown.index(section + "\n") for section in SECTION_ORDER]
        self.assertEqual(positions, sorted(positions))

    def test_findings_ordered_by_label_then_severity(self) -> None:
        run_dir, _markdown = self.render("full")
        report = json.loads((run_dir / "report.json").read_text(encoding="utf-8"))
        keys = [(panel.AgreementLabel.RANK[f["label"]], panel.Severity.RANK[f["severity"]]) for f in report["findings"]]
        self.assertEqual(keys, sorted(keys))
        labels = [f["id"] + ":" + f["label"] for f in report["findings"]]
        self.assertEqual(labels, ["F5:consensus", "F1:consensus", "F3:majority", "F2:contested", "F4:contested"])

    def test_rejected_section(self) -> None:
        _run_dir, markdown = self.render("full")
        rejected = markdown.split("## Rejected findings", 1)[1].split("## Checked", 1)[0]
        self.assertIn("| F6 |", rejected)
        self.assertIn("numerical-analyst", rejected)
        self.assertIn("documented sentinel", rejected)

    def test_no_reviewable_code(self) -> None:
        _run_dir, markdown = self.render("empty")
        self.assertIn(panel.NO_REVIEWABLE_CODE, markdown)
        for section in SECTION_ORDER[:3]:
            self.assertIn(section, markdown)
        for section in SECTION_ORDER[3:]:
            self.assertNotIn(section + "\n", markdown)
        self.assert_golden("empty/expected-report.md", markdown)

    def test_report_findings_mapping(self) -> None:
        _run_dir, output = self.render("full", "json")
        data = json.loads(output)
        mapping = {(r["file"], r["line"]): r for r in data["report_findings"]}
        consensus = mapping[("src/sci/train.py", 40)]
        self.assertEqual(consensus["verdict"], "CONFIRMED")
        self.assertEqual(
            consensus["failure_scenario"],
            "x = [1, 2, 3, 4, 100] produces the first training row scales to -0.538 instead of -1.342",
        )
        self.assertTrue(consensus["short_summary"].startswith("Consensus: "))
        self.assertLessEqual(len(consensus["short_summary"]), 60)
        self.assertEqual(consensus["category"], "statistical-integrity")
        majority = mapping[("src/sci/model.py", 10)]
        self.assertTrue(majority["short_summary"].startswith("Majority: "))
        self.assertEqual([r["verdict"] for r in data["report_findings"]][:3], ["CONFIRMED"] * 3)

    def test_report_dry_run(self) -> None:
        run_dir = self.run_from_scenario("full")
        self.assertEqual(run_panel("adjudicate", "--run", str(run_dir)).code, 0)
        result = run_panel("report", "--run", str(run_dir), "--dry-run")
        self.assertEqual(result.code, 0, result.err)
        self.assertFalse((run_dir / "report.json").exists())


class TestIngest(RunDirMixin):
    def panel_run(self) -> dict:
        full = GOLDEN / "full"

        def load(path: Path) -> dict:
            return json.loads(path.read_text(encoding="utf-8"))

        debate = []
        for path in sorted(full.glob("debate/batch-*/round-*/*.json")):
            debate.append({"batch": int(path.parts[-3].split("-")[1]), "message": load(path)})
        return {
            "candidates": [load(p) for p in sorted(full.glob("candidates/*.json"))],
            "merge": [load(p) for p in sorted(full.glob("merge/*.json"))],
            "debate": debate,
            "notes": [load(p) for p in sorted(full.glob("notes/*.json"))],
            "dropped": ["moderator notes (batch 3)"],
        }

    def test_ingest_writes_layout(self) -> None:
        run_dir = self.init_run()
        source = run_dir / "workflow-result.json"
        data = self.panel_run()
        data["candidates"].append({"perspective": "rogue", "findings": [], "notes": ""})
        source.write_text(json.dumps(data), encoding="utf-8")
        result = run_panel("ingest", "--run", str(run_dir), str(source))
        self.assertEqual(result.code, 0, result.err)
        for relative in (
            "candidates/theorist.json",
            "merge/batch-1.json",
            "merge/batch-2.json",
            "debate/batch-1/round-0/defender.json",
            "debate/batch-1/round-1/numerical-analyst.json",
            "notes/batch-2.json",
        ):
            self.assertTrue((run_dir / relative).is_file(), relative)
        self.assertFalse((run_dir / "candidates/rogue.json").exists())
        notices = json.loads((run_dir / "notices.json").read_text(encoding="utf-8"))
        self.assertTrue(any("rogue" in n for n in notices))
        self.assertTrue(any("dropped after failing validation twice" in n for n in notices))
        for path in (GOLDEN / "full").glob("debate/**/*.json"):
            relative = path.relative_to(GOLDEN / "full")
            self.assertEqual(path.read_text(encoding="utf-8"), (run_dir / relative).read_text(encoding="utf-8"))

    def test_ingest_rejects_ids_that_are_not_kebab_case(self) -> None:
        run_dir = self.init_run()
        source = run_dir / "workflow-result.json"
        data = self.panel_run()
        evil = json.loads(json.dumps(data["candidates"][0]))
        evil["perspective"] = "../escape"
        for finding in evil["findings"]:
            finding["raised_by"] = "../escape"
        data["candidates"] = [evil]
        data["debate"][0]["message"]["member"] = "../../escape"
        source.write_text(json.dumps(data), encoding="utf-8")
        result = run_panel("ingest", "--run", str(run_dir), str(source))
        self.assertEqual(result.code, 0, result.err)
        self.assertFalse((run_dir.parent / "escape.json").exists())
        self.assertFalse(list(run_dir.rglob("escape.json")))
        self.assertFalse((run_dir / "candidates").exists())

    def test_ingest_dry_run(self) -> None:
        run_dir = self.init_run()
        source = run_dir / "workflow-result.json"
        source.write_text(json.dumps(self.panel_run()), encoding="utf-8")
        result = run_panel("ingest", "--run", str(run_dir), str(source), "--dry-run")
        self.assertEqual(result.code, 0, result.err)
        self.assertFalse((run_dir / "candidates").exists())


# ---------------------------------------------------------------------------
# User Story 2: disagreement
# ---------------------------------------------------------------------------


class TestDisagreement(GoldenMixin):
    def test_contested_golden(self) -> None:
        run_dir, markdown = self.render("contested")
        self.assert_golden("contested/expected-report.md", markdown)
        report = json.loads((run_dir / "report.json").read_text(encoding="utf-8"))
        labels = {f["id"]: f["label"] for f in report["findings"]}
        self.assertEqual(labels, {"F1": "contested", "F2": "contested"})

    def test_deciding_assumption_may_be_null(self) -> None:
        run_dir = self.run_from_scenario("contested")
        path = run_dir / "notes" / "batch-1.json"
        notes = json.loads(path.read_text(encoding="utf-8"))
        notes["notes"][1]["deciding_assumption"] = None
        path.write_text(json.dumps(notes), encoding="utf-8")
        self.assertEqual(run_panel("adjudicate", "--run", str(run_dir)).code, 0)
        result = run_panel("report", "--run", str(run_dir), "--format", "json")
        self.assertEqual(result.code, 0, result.err)
        data = json.loads(result.out)
        mapping = {r["line"]: r for r in data["report_findings"]}
        self.assertNotIn("Decided by", mapping[30]["summary"])

    def test_contested_null_trigger_mapping(self) -> None:
        _run_dir, output = self.render("contested", "json")
        data = json.loads(output)
        mapping = {r["line"]: r for r in data["report_findings"]}
        null_trigger = mapping[14]
        self.assertEqual(
            null_trigger["failure_scenario"],
            "No concrete trigger established: No member could establish an amplitude that callers actually use.",
        )
        self.assertEqual(null_trigger["verdict"], "PLAUSIBLE")
        self.assertIn(" Contested. For: ", null_trigger["summary"])
        self.assertIn(" Against: ", null_trigger["summary"])
        self.assertIn(" Decided by: The maximum amplitude callers pass.", null_trigger["summary"])

    def test_contested_without_arguments_fails_validation(self) -> None:
        _run_dir, output = self.render("contested", "json")
        data = json.loads(output)
        del data["report_findings"]
        del data["findings"][0]["argument_against"]
        self.assertTrue(panel.validate_message("report", data))

    def test_withdrawn_only_in_rejected_section(self) -> None:
        _run_dir, markdown = self.render("full")
        findings, rest = markdown.split("## Rejected findings", 1)
        self.assertNotIn("F6:", findings)
        self.assertIn("F6", rest)


# ---------------------------------------------------------------------------
# User Story 3: repository and path modes
# ---------------------------------------------------------------------------


class TestScopeModes(RunDirMixin):
    def setUp(self) -> None:
        super().setUp()
        init_repo(self.project)
        self.write("src/core/a.py", "A = 1\n")
        self.write("src/analysis/b.ts", "export const b = 2;\n")
        self.write("notebooks/explore.ipynb", '{"cells": []}\n')
        self.write("dist/bundle.js", "var x;\n")
        git(self.project, "add", ".")
        git(self.project, "commit", "-qm", "more")

    def scope(self, *argv: str) -> tuple[Result, dict | None]:
        run_dir = self.init_run()
        result = run_panel("scope", "--run", str(run_dir), *argv)
        path = run_dir / "scope.json"
        return result, json.loads(path.read_text(encoding="utf-8")) if path.exists() else None

    def test_repository_mode(self) -> None:
        result, scope = self.scope("--mode", "repository")
        self.assertEqual(result.code, 0, result.err)
        files = {f["path"]: f for f in scope["files"]}
        self.assertEqual(set(files), {"src/base.py", "src/core/a.py", "src/analysis/b.ts", "notebooks/explore.ipynb"})
        self.assertTrue(all(f["line_ranges"] == [] for f in files.values()))
        self.assertEqual(files["notebooks/explore.ipynb"]["language"], "python")
        self.assertIn({"path": "dist/bundle.js", "reason": "vendored or generated (dist/)"}, scope["excluded"])

    def test_paths_mode(self) -> None:
        result, scope = self.scope("--mode", "paths", "--path", "src/core")
        self.assertEqual(result.code, 0, result.err)
        self.assertEqual([f["path"] for f in scope["files"]], ["src/core/a.py"])
        excluded = {e["path"]: e["reason"] for e in scope["excluded"]}
        self.assertEqual(excluded["src/analysis/b.ts"], "outside paths")

    def test_named_generated_file_is_included(self) -> None:
        result, scope = self.scope("--mode", "paths", "--path", "dist/bundle.js")
        self.assertEqual(result.code, 0, result.err)
        self.assertEqual([f["path"] for f in scope["files"]], ["dist/bundle.js"])

    def test_paths_mode_requires_path(self) -> None:
        result, _scope = self.scope("--mode", "paths")
        self.assertEqual(result.code, 2)

    def test_budget(self) -> None:
        result, scope = self.scope("--mode", "repository", "--budget", "2")
        self.assertEqual(result.code, 0, result.err)
        self.assertTrue(any(e["reason"] == "over budget" for e in scope["excluded"]))

    def test_non_git_repository_mode(self) -> None:
        shutil.rmtree(self.project / ".git")
        result, scope = self.scope("--mode", "repository")
        self.assertEqual(result.code, 0, result.err)
        self.assertIn("src/core/a.py", [f["path"] for f in scope["files"]])

    def test_report_drops_findings_outside_scope(self) -> None:
        state = json.loads((GOLDEN / "full" / "panel.json").read_text(encoding="utf-8"))
        scope = panel.ReviewScope.from_json(json.loads((GOLDEN / "full" / "scope.json").read_text(encoding="utf-8")))
        narrowed = panel.ReviewScope(
            mode="paths", base=None, head=None, files=scope.files[:1], excluded=(), note="Files under src/sci/heat.ts."
        )
        run_dir = self.run_from_scenario("full")
        self.assertEqual(run_panel("adjudicate", "--run", str(run_dir)).code, 0)
        adjudication = panel.Adjudication.from_json(
            json.loads((run_dir / "adjudication.json").read_text(encoding="utf-8"))
        )
        report = panel.build_report(narrowed, panel.PanelState.from_json(state), adjudication, [], [])
        self.assertEqual({f.file for f in report.findings}, {"src/sci/heat.ts"})
        self.assertTrue(any("outside the scope" in n for n in report.notices))


# ---------------------------------------------------------------------------
# User Story 4: extensions
# ---------------------------------------------------------------------------

TEST_EXTENSION = FIXTURES / "test-extension-plugin" / "skills" / "acoustics-sci-review-extension" / "extension.json"
INVALID_EXTENSION = (
    FIXTURES / "test-extension-plugin-invalid" / "skills" / "acoustics-sci-review-extension" / "extension.json"
)


class TestExtensions(RunDirMixin):
    def make_extension(self, name: str, applies: dict, perspective_id: str = "domain-expert", **extra) -> Path:
        skill = Path(tempfile.mkdtemp()) / f"{name}-sci-review-extension"
        self.addCleanup(shutil.rmtree, skill.parent, True)
        (skill / "reference").mkdir(parents=True)
        (skill / "perspective.md").write_text("# Expert\n", encoding="utf-8")
        (skill / "reference" / "ref.md").write_text("# Ref\n", encoding="utf-8")
        declaration = {
            "contract_version": 1,
            "id": f"{name}-sci-review-extension",
            "plugin": name,
            "perspective": {"id": perspective_id, "name": "Expert", "brief": "perspective.md"},
            "reference": ["reference/ref.md"],
            "applies_to": applies,
            **extra,
        }
        (skill / "extension.json").write_text(json.dumps(declaration), encoding="utf-8")
        return skill / "extension.json"

    def scope_with(self, files: dict[str, str]) -> panel.ReviewScope:
        for path, text in files.items():
            self.write(path, text)
        return panel.ReviewScope(
            mode="repository",
            base=None,
            head=None,
            files=tuple(panel.ScopedFile(path=p, language=panel.language_of(p)) for p in files),
            excluded=(),
            note="test",
        )

    def statuses(self, scope: panel.ReviewScope, declarations: list[Path]) -> dict[str, panel.DomainExtension]:
        extensions = panel.select_extensions(self.project, scope, declarations)
        return {e.id: e for e in extensions}

    def test_glob_file_type_and_import_matching(self) -> None:
        scope = self.scope_with({"model.epjson": "{}", "run.py": "import idfkit\n", "other.py": "x = 1\n"})
        by_glob = self.make_extension("globber", {"globs": ["**/*.epJSON"]}, "p1")
        by_type = self.make_extension("typer", {"file_types": [".EPJSON"]}, "p2")
        by_import = self.make_extension(
            "importer", {"languages": ["python"], "import_patterns": [r"^\s*import\s+idfkit\b"]}, "p3"
        )
        missing = self.make_extension("nomatch", {"globs": ["**/*.wav"]}, "p4")
        result = self.statuses(scope, [by_glob, by_type, by_import, missing])
        self.assertEqual(result["globber-sci-review-extension"].status, "selected")
        self.assertEqual(result["typer-sci-review-extension"].status, "selected")
        self.assertEqual(result["importer-sci-review-extension"].status, "selected")
        self.assertEqual(result["nomatch-sci-review-extension"].status, "not-applicable")
        self.assertTrue(result["nomatch-sci-review-extension"].status_reason)

    def test_import_pattern_requires_listed_language(self) -> None:
        scope = self.scope_with({"run.ts": "import idfkit\n"})
        declaration = self.make_extension(
            "pyonly", {"languages": ["python"], "import_patterns": [r"^\s*import\s+idfkit\b"]}
        )
        self.assertEqual(self.statuses(scope, [declaration])["pyonly-sci-review-extension"].status, "not-applicable")

    def test_failed_declarations(self) -> None:
        scope = self.scope_with({"a.py": "x = 1\n"})
        bad_version = self.make_extension("v2", {"globs": ["*.py"]}, contract_version=2)
        data = json.loads(bad_version.read_text(encoding="utf-8"))
        data["contract_version"] = 2
        bad_version.write_text(json.dumps(data), encoding="utf-8")
        missing_field = self.make_extension("missing", {"globs": ["*.py"]})
        data = json.loads(missing_field.read_text(encoding="utf-8"))
        del data["perspective"]
        missing_field.write_text(json.dumps(data), encoding="utf-8")
        result = self.statuses(scope, [bad_version, missing_field, self.project / "absent" / "extension.json"])
        self.assertEqual(result["v2-sci-review-extension"].status, "failed")
        self.assertIn("contract_version", result["v2-sci-review-extension"].status_reason)
        self.assertEqual(result["missing-sci-review-extension"].status, "failed")
        self.assertIn("perspective", result["missing-sci-review-extension"].status_reason)
        self.assertEqual(result["absent"].status, "failed")

    def test_two_extensions_claim_one_file(self) -> None:
        scope = self.scope_with({"model.idf": "Version,24.1;\n"})
        first = self.make_extension("first", {"file_types": [".idf"]}, "p1")
        second = self.make_extension("second", {"globs": ["**/*.idf"]}, "p2")
        result = self.statuses(scope, [first, second])
        self.assertEqual({e.status for e in result.values() if e.plugin in ("first", "second")}, {"selected"})

    def test_known_extension_recommended(self) -> None:
        scope = self.scope_with({"sim.py": "from idfkit import load\n"})
        result = self.statuses(scope, [])
        recommended = result["building-energy-sci-review-extension"]
        self.assertEqual(recommended.status, "recommended")
        self.assertIn("idfkit@idfkit", recommended.status_reason)
        self.assertTrue(recommended.adds)
        scope = self.scope_with({"weather.EPW": "LOCATION\n"})
        self.assertIn("building-energy-sci-review-extension", self.statuses(scope, []))
        scope = self.scope_with({"plain.py": "x = 1\n"})
        self.assertNotIn("building-energy-sci-review-extension", self.statuses(scope, []))

    def test_failed_known_extension_is_not_recommended(self) -> None:
        scope = self.scope_with({"sim.py": "from idfkit import load\n"})
        broken = self.make_extension("building-energy", {"globs": ["*.py"]})
        data = json.loads(broken.read_text(encoding="utf-8"))
        data["contract_version"] = 2
        broken.write_text(json.dumps(data), encoding="utf-8")
        extensions = panel.select_extensions(self.project, scope, [broken])
        self.assertEqual([e.status for e in extensions], ["failed"])

    def test_reserved_or_unsafe_perspective_ids_fail(self) -> None:
        scope = self.scope_with({"a.py": "x = 1\n"})
        for pid in ("defender", "moderator", "../escape", "Upper"):
            with self.subTest(pid=pid):
                declaration = self.make_extension("odd", {"globs": ["*.py"]}, pid)
                extension = panel.select_extensions(self.project, scope, [declaration])[0]
                self.assertEqual(extension.status, "failed")
                self.assertIn("kebab-case", extension.status_reason)

    def test_contract_only_test_extension(self) -> None:
        scope = self.scope_with({"audio/mix.py": "import soundfile\n"})
        extensions = panel.select_extensions(self.project, scope, [TEST_EXTENSION, INVALID_EXTENSION])
        selected = [e for e in extensions if e.status == "selected"]
        failed = [e for e in extensions if e.status == "failed"]
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].perspective.id, "acoustician")
        self.assertEqual(len(failed), 1)
        self.assertIn("contract_version", failed[0].status_reason)

    def test_select_extensions_subcommand_and_panel(self) -> None:
        self.write("model.idf", "Version,24.1;\n")
        git_free_scope = ("scope", "--mode", "repository")
        run_dir = self.init_run()
        self.assertEqual(run_panel(*git_free_scope[:1], "--run", str(run_dir), *git_free_scope[1:]).code, 0)
        declarations = [self.make_extension(f"d{i}", {"file_types": [".idf"]}, f"domain-{i}") for i in range(3)]
        argv = ["select-extensions", "--run", str(run_dir)]
        for declaration in declarations:
            argv += ["--declaration", str(declaration)]
        result = run_panel(*argv, "--dry-run")
        self.assertEqual(result.code, 0, result.err)
        self.assertFalse((run_dir / "panel.json").exists())
        self.assertEqual(run_panel(*argv).code, 0)
        result = run_panel("panel", "--run", str(run_dir), "--runner", "claude-agents")
        self.assertEqual(result.code, 0, result.err)
        state = json.loads((run_dir / "panel.json").read_text(encoding="utf-8"))
        ids = [p["id"] for p in state["panel"]["perspectives"]]
        self.assertEqual(len(ids), 7)
        self.assertEqual(ids[5:], ["domain-0", "domain-1"])
        domain = state["panel"]["perspectives"][5]
        self.assertEqual(domain["source"], "d0-sci-review-extension")
        self.assertTrue(Path(domain["brief_path"]).is_absolute())
        self.assertTrue(all(Path(p).is_absolute() for p in domain["reference_paths"]))
        self.assertTrue(any("limited to 7" in n for n in state["notices"]))

    def test_extensions_section_rendered(self) -> None:
        run_dir = self.run_from_scenario("full")
        state = json.loads((run_dir / "panel.json").read_text(encoding="utf-8"))
        state["extensions"] = [
            {
                "id": "building-energy-sci-review-extension",
                "plugin": "idfkit",
                "contract_version": 1,
                "perspective": None,
                "reference_paths": [],
                "applies_to": None,
                "checks": None,
                "status": "recommended",
                "status_reason": "not installed; it would apply to sim.py. Install it with idfkit@idfkit.",
                "adds": "building physicist",
            },
            {
                "id": "broken-sci-review-extension",
                "plugin": "broken",
                "contract_version": 2,
                "perspective": None,
                "reference_paths": [],
                "applies_to": None,
                "checks": None,
                "status": "failed",
                "status_reason": "contract_version 2 is not supported (supported: 1)",
            },
        ]
        (run_dir / "panel.json").write_text(json.dumps(state), encoding="utf-8")
        self.assertEqual(run_panel("adjudicate", "--run", str(run_dir)).code, 0)
        result = run_panel("report", "--run", str(run_dir))
        self.assertEqual(result.code, 0, result.err)
        section = result.out.split("## Extensions", 1)[1].split("## Findings", 1)[0]
        self.assertIn("recommended; not installed", section)
        self.assertIn("It would add: building physicist.", section)
        self.assertIn("failed; contract_version 2 is not supported", section)


# ---------------------------------------------------------------------------
# User Story 5: sequential runner
# ---------------------------------------------------------------------------


class TestSequential(GoldenMixin):
    def sequential_run(self) -> Path:
        run_dir = self.run_from_scenario("full")
        state = json.loads((run_dir / "panel.json").read_text(encoding="utf-8"))
        state["panel"]["runner"] = "sequential"
        state["panel"]["independent"] = False
        (run_dir / "panel.json").write_text(json.dumps(state), encoding="utf-8")
        self.assertEqual(run_panel("adjudicate", "--run", str(run_dir)).code, 0)
        return run_dir

    def test_panel_independent_false(self) -> None:
        run_dir = self.init_run()
        self.assertEqual(run_panel("panel", "--run", str(run_dir), "--runner", "sequential").code, 0)
        state = json.loads((run_dir / "panel.json").read_text(encoding="utf-8"))
        self.assertFalse(state["panel"]["independent"])

    def test_reduced_independence_notice(self) -> None:
        run_dir = self.sequential_run()
        result = run_panel("report", "--run", str(run_dir))
        notices = result.out.split("## Notices", 1)[1]
        self.assertIn(panel.REDUCED_INDEPENDENCE_NOTICE, notices)
        self.assertIn("not independent agents", result.out.split("## Panel", 1)[0])

    def test_tables_per_label_with_every_field(self) -> None:
        _run_dir, markdown = self.render("full")
        for label in ("### Consensus", "### Majority", "### Contested"):
            self.assertIn(label, markdown)
        header = "| Location | Dimension | Severity | Summary | Trigger | Wrong output | Fix | Raised by | Label |"
        self.assertEqual(markdown.splitlines().count(header), 2)
        self.assertIn(header + " Argument for | Argument against | Deciding assumption | No-trigger reason |", markdown)

    def test_dropped_message_notice(self) -> None:
        run_dir = self.sequential_run()
        text = "The output of methodologist was dropped after failing validation twice."
        self.assertEqual(run_panel("notice", "--run", str(run_dir), text).code, 0)
        result = run_panel("report", "--run", str(run_dir))
        self.assertIn(text, result.out.split("## Notices", 1)[1])

    def test_other_language_notice(self) -> None:
        run_dir = self.sequential_run()
        scope = json.loads((run_dir / "scope.json").read_text(encoding="utf-8"))
        scope["files"].append({"path": "src/sci/kernel.f90", "language": "other", "line_ranges": [[1, 3]]})
        (run_dir / "scope.json").write_text(json.dumps(scope), encoding="utf-8")
        result = run_panel("report", "--run", str(run_dir))
        self.assertIn("languages other than Python and TypeScript", result.out)
        self.assertIn(".f90", result.out)


class TestCodexRunnerIndependence(unittest.TestCase):
    """The Codex runner spawns subagents without a history fork (SC-011)."""

    RUNNER = ROOT / "plugins" / "sci-review" / "skills" / "scientific-review" / "runners" / "codex-subagents.md"

    def test_every_spawn_sets_fork_turns_none(self) -> None:
        text = self.RUNNER.read_text(encoding="utf-8")
        preconditions = text.split("## 2. Preconditions", 1)[1].split("## 3. Rules", 1)[0]
        self.assertIn('Set `fork_turns` to `"none"` in every spawn.', preconditions)

    def test_fallback_covers_spawns_that_cannot_avoid_a_fork(self) -> None:
        text = self.RUNNER.read_text(encoding="utf-8")
        fallback = text.split("## 6. Fallback to the sequential runner", 1)[1]
        self.assertIn("no way to spawn without a history fork", fallback)


class TestPanelMemberRules(unittest.TestCase):
    """Rules added after the live runs of validation.md sections 4.6 to 4.8."""

    SKILL = ROOT / "plugins" / "sci-review" / "skills" / "scientific-review"
    PERSPECTIVES = ("theorist", "numerical-analyst", "experimentalist", "methodologist", "computer-scientist")

    def independent_round(self, perspective: str) -> str:
        text = (self.SKILL / "roles" / f"{perspective}.md").read_text(encoding="utf-8")
        return text.split("## Independent round", 1)[1].split("## Debate", 1)[0]

    def test_one_defect_per_finding(self) -> None:
        for perspective in self.PERSPECTIVES:
            with self.subTest(perspective=perspective):
                self.assertIn("Each finding states one defect", self.independent_round(perspective))

    def test_trigger_survives_the_obvious_defence(self) -> None:
        for perspective in self.PERSPECTIVES:
            with self.subTest(perspective=perspective):
                section = self.independent_round(perspective)
                self.assertIn("the obvious defence does not answer", section)
                self.assertIn("not a change of seed", section)

    def test_members_do_not_install_a_validator(self) -> None:
        auditor = ROOT / "plugins" / "sci-review" / "agents" / "scientific-auditor.md"
        panelist = self.SKILL / "codex-agents" / "sci-review-panelist.toml"
        for path in (auditor, panelist):
            with self.subTest(path=path.name):
                self.assertIn("Do not install a package to validate it", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
