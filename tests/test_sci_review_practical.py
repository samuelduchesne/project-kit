"""Tests for spec 010 of sci-review: findings that say who hits them.

Covers the finding prose (headline, context, in practice), the verifiers' practical reach (trigger class and
value corrections), the severity cap, design questions (rule 2a), the report layout and the `issue` command.

Run with: uv run --no-project --python 3.12 python -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from test_sci_review_panel import GOLDEN, GoldenMixin, panel, run_panel

MESSAGES = GOLDEN.parent
PRACTICAL = GOLDEN / "practical"


def verdict(
    kind: str = "confirm",
    *,
    fid: str = "F1",
    verifier: str = "v1",
    trigger_class: str | None = "user-action",
    reach: str = "Read the settings.",
    intended: str | None = None,
    corrections: tuple[panel.ValueCorrection, ...] = (),
) -> panel.VerdictRecord:
    return panel.VerdictRecord(
        finding_id=fid,
        verdict=kind,
        reason=f"{verifier} {kind}",
        argument_for=f"{verifier} for",
        argument_against=f"{verifier} against",
        deciding_assumption="An unsettled assumption." if kind == "uncertain" else None,
        no_trigger_reason=None,
        verifier=verifier,
        reach=reach,
        trigger_class=trigger_class,
        possibly_intended=intended is not None,
        possibly_intended_reason=intended,
        value_corrections=corrections,
    )


def merged(severity: str = "high", severity_reason: str | None = None) -> panel.MergedFinding:
    return panel.MergedFinding(
        id="F1",
        members=("theorist-1",),
        raised_by=("theorist",),
        batch=1,
        file="src/a.py",
        line_start=1,
        line_end=2,
        dimension="algorithmic-correctness",
        severity=severity,
        summary="A defect.",
        trigger="x = 0",
        wrong_output="nan",
        fix="Guard x.",
        severity_reason=severity_reason,
        headline="Results go wrong for an empty building",
        context="This code totals energy for the dashboard.",
        in_practice="Any user with an empty building.",
    )


def adjudicate(finding: panel.MergedFinding, *verdicts: panel.VerdictRecord) -> panel.Adjudication:
    ruling = panel.MergeRuling(batch=1, findings=(finding,))
    return panel.adjudicate_verified([ruling], {1: list(verdicts)}, {m: finding.severity for m in finding.members})


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class TestSchemasAndRecords(unittest.TestCase):
    """T003: the new fields are required in new messages, optional when loading earlier runs."""

    def candidate_message(self) -> dict:
        return read(PRACTICAL / "candidates" / "theorist.json")

    def test_candidate_without_prose_fails(self) -> None:
        for field in ("headline", "context", "in_practice"):
            message = self.candidate_message()
            del message["findings"][0][field]
            errors = panel.validate_message("candidate-findings", message)
            self.assertTrue(any(field in e for e in errors), (field, errors))

    def test_candidate_with_prose_passes(self) -> None:
        self.assertEqual(panel.validate_message("candidate-findings", self.candidate_message()), [])

    def test_headline_of_91_characters_fails(self) -> None:
        message = self.candidate_message()
        message["findings"][0]["headline"] = "x" * 91
        errors = panel.validate_message("candidate-findings", message)
        self.assertTrue(any("at most 90" in e for e in errors), errors)
        message["findings"][0]["headline"] = "x" * 90
        self.assertEqual(panel.validate_message("candidate-findings", message), [])

    def test_earlier_finding_loads_with_defaults(self) -> None:
        earlier = read(GOLDEN / "full" / "expected-report.json")["findings"][0]
        for field in ("headline", "context", "in_practice", "kind", "value_corrections", "severity_capped"):
            earlier.pop(field, None)
        finding = panel.Finding.from_json(earlier)
        self.assertIsNone(finding.headline)
        self.assertEqual(finding.kind, "defect")
        self.assertEqual(finding.value_corrections, ())
        self.assertFalse(finding.severity_capped)
        self.assertIsNone(finding.trigger_class)

    def test_earlier_verdict_loads(self) -> None:
        record = panel.VerdictRecord.from_json(
            {
                "finding_id": "F1",
                "verdict": "confirm",
                "reason": "r",
                "argument_for": "a",
                "argument_against": "b",
                "deciding_assumption": None,
                "no_trigger_reason": None,
            }
        )
        self.assertIsNone(record.trigger_class)
        self.assertEqual(record.effective, "confirm")


class TestValidationRules(unittest.TestCase):
    """T004: data-model.md, Validation rules added to `panel.py validate`.

    The fixtures are also run by test_sci_review_panel.TestModelAndValidate with the expected error messages.
    """

    def test_valid_practical_verification(self) -> None:
        message = read(MESSAGES / "valid" / "verification.json")
        self.assertEqual(panel.validate_message("verification", message), [])
        self.assertTrue(any(v["possibly_intended"] for v in message["verdicts"]))
        self.assertTrue(any(v["value_corrections"] for v in message["verdicts"]))

    def test_invalid_messages(self) -> None:
        cases = {
            "verification-unreachable-confirm.json": "unreachable requires verdict refute",
            "verification-intended-refute.json": "not allowed with verdict refute",
            "verification-intended-no-reason.json": "required when possibly_intended is true",
            "verification-correction-line-zero.json": "less than 1",
            "debate-intended-non-defender.json": "only the defender may mark",
        }
        for name, expected in cases.items():
            with self.subTest(name=name):
                case = read(MESSAGES / "invalid" / name)
                errors = panel.validate_message(case["schema"], case["message"])
                self.assertTrue(any(expected in e for e in errors), errors)


class TestAutoMergeKeepsProse(unittest.TestCase):
    """T012: the automatic merge copies headline, context and in practice."""

    def test_singleton_cluster_keeps_prose(self) -> None:
        message = panel.CandidateMessage.from_json(read(PRACTICAL / "candidates" / "computer-scientist.json"))
        candidates = {f.id: f for f in message.findings}
        plan = panel.merge_plan(list(candidates.values()), 1)
        ruling = panel.auto_ruling(plan.batches[0], plan.clusters, candidates)
        assert ruling is not None
        by_member = {f.members[0]: f for f in ruling.findings}
        for cid, candidate in candidates.items():
            self.assertEqual(by_member[cid].headline, candidate.headline)
            self.assertEqual(by_member[cid].context, candidate.context)
            self.assertEqual(by_member[cid].in_practice, candidate.in_practice)


class TestTriggerClass(unittest.TestCase):
    """T021: research R3."""

    def test_majority_among_non_refuting_verdicts(self) -> None:
        verdicts = [
            verdict(trigger_class="release", verifier="v1"),
            verdict(trigger_class="release", verifier="v2"),
            verdict(trigger_class="user-action", verifier="v3"),
        ]
        self.assertEqual(panel.combined_trigger_class(verdicts)[0], "release")

    def test_tie_goes_to_the_more_frequent_trigger(self) -> None:
        verdicts = [verdict(trigger_class="release", verifier="v1"), verdict(trigger_class="user-action", verifier="v2")]
        self.assertEqual(panel.combined_trigger_class(verdicts)[0], "user-action")

    def test_refuting_verdicts_are_ignored(self) -> None:
        verdicts = [verdict("refute", trigger_class="unreachable"), verdict(trigger_class="release", verifier="v2")]
        self.assertEqual(panel.combined_trigger_class(verdicts)[0], "release")

    def test_no_supporting_verdict_gives_none(self) -> None:
        self.assertEqual(panel.combined_trigger_class([verdict("refute", trigger_class="unreachable")]), (None, None))
        self.assertEqual(panel.combined_trigger_class([]), (None, None))

    def test_reach_of_the_first_verdict_with_the_reported_class(self) -> None:
        verdicts = [
            verdict(trigger_class="user-action", reach="A", verifier="v1"),
            verdict(trigger_class="release", reach="B", verifier="v2"),
            verdict(trigger_class="release", reach="C", verifier="v3"),
        ]
        self.assertEqual(panel.combined_trigger_class(verdicts), ("release", "B"))


class TestSeverityCap(unittest.TestCase):
    """T022: research R5."""

    def finding(self, finding: panel.MergedFinding, trigger_class: str | None) -> panel.Finding:
        return adjudicate(finding, verdict(trigger_class=trigger_class)).findings[0]

    def test_release_and_operator_change_are_capped(self) -> None:
        for trigger_class in ("release", "operator-change"):
            with self.subTest(trigger_class=trigger_class):
                finding = self.finding(merged("high"), trigger_class)
                self.assertEqual((finding.severity, finding.severity_capped), ("medium", True))

    def test_ordinary_use_is_not_capped(self) -> None:
        for trigger_class in ("data-condition", "user-action"):
            finding = self.finding(merged("high"), trigger_class)
            self.assertEqual((finding.severity, finding.severity_capped), ("high", False))

    def test_a_severity_reason_keeps_high(self) -> None:
        finding = self.finding(merged("high", "A release happens every week."), "release")
        self.assertEqual((finding.severity, finding.severity_capped), ("high", False))

    def test_medium_is_unchanged(self) -> None:
        finding = self.finding(merged("medium"), "release")
        self.assertEqual((finding.severity, finding.severity_capped), ("medium", False))

    def test_no_class_is_unchanged(self) -> None:
        finding = self.finding(merged("high"), None)
        self.assertEqual((finding.severity, finding.severity_capped), ("high", False))


class TestUnreachable(unittest.TestCase):
    """T023: an unreachable trigger is a refutation."""

    def test_unreachable_refutations_reject(self) -> None:
        result = adjudicate(merged(), verdict("refute", trigger_class="unreachable"))
        self.assertEqual(result.findings, ())
        self.assertEqual(result.rejected[0].reason, "v1 refute")


class TestValueCorrections(unittest.TestCase):
    """T027: corrections are unioned and deduplicated in first-seen order."""

    def test_union_and_deduplication(self) -> None:
        a = panel.ValueCorrection(quoted="N=5", actual="N=10", file=".env", line=3)
        b = panel.ValueCorrection(quoted="M=1", actual="M=2", file="settings.py", line=8)
        result = adjudicate(merged(), verdict(corrections=(a,)), verdict(verifier="v2", corrections=(a, b)))
        self.assertEqual(result.findings[0].value_corrections, (a, b))


class TestDesignQuestions(unittest.TestCase):
    """T032: rule 2a of protocol.md section 5.1."""

    def test_one_confirm_and_one_marked_confirm(self) -> None:
        finding = adjudicate(merged(), verdict(), verdict(verifier="v2", intended="Looks deliberate.")).findings[0]
        self.assertEqual((finding.kind, finding.label), ("design-question", "majority"))
        self.assertEqual(finding.possibly_intended_reason, "Looks deliberate.")

    def test_a_single_marked_confirm_is_contested(self) -> None:
        finding = adjudicate(merged(), verdict(intended="Looks deliberate.")).findings[0]
        self.assertEqual((finding.kind, finding.label), ("design-question", "contested"))

    def test_unmarked_findings_are_defects(self) -> None:
        finding = adjudicate(merged(), verdict(), verdict(verifier="v2"), verdict("refute", verifier="v3")).findings[0]
        self.assertEqual((finding.kind, finding.label), ("defect", "majority"))

    def test_refutation_comes_before_the_mark(self) -> None:
        result = adjudicate(
            merged(),
            verdict(intended="Deliberate."),
            verdict("refute", verifier="v2"),
            verdict("refute", verifier="v3"),
        )
        self.assertEqual(result.findings, ())

    def test_first_recorded_reason(self) -> None:
        finding = adjudicate(
            merged(), verdict(intended="First."), verdict(verifier="v2", intended="Second.")
        ).findings[0]
        self.assertEqual(finding.possibly_intended_reason, "First.")


class TestDebateDefenderMark(unittest.TestCase):
    """T033: the defender's latest position decides in the debate protocol."""

    def position(self, member: str, round_: int, mark: bool) -> panel.Position:
        return panel.Position(
            finding_id="F1",
            member=member,
            round=round_,
            stance="accept",
            reason="Holds.",
            possibly_intended=mark,
            possibly_intended_reason="Looks deliberate." if mark else None,
        )

    def kind(self, *positions: panel.Position) -> str:
        ruling = panel.MergeRuling(batch=1, findings=(merged(),))
        result = panel.adjudicate([ruling], {1: [list(positions)]}, {}, ["theorist"], {"theorist-1": "high"})
        return result.findings[0].kind

    def test_marked_defender_makes_a_design_question(self) -> None:
        self.assertEqual(
            self.kind(self.position("theorist", 0, False), self.position("defender", 0, True)), "design-question"
        )

    def test_a_later_unmarked_position_wins(self) -> None:
        self.assertEqual(
            self.kind(
                self.position("theorist", 0, False),
                self.position("defender", 0, True),
                self.position("defender", 1, False),
            ),
            "defect",
        )


class PracticalRunMixin(GoldenMixin):
    def practical_run(self) -> Path:
        run_dir = self.run_from_scenario("practical")
        result = run_panel("adjudicate", "--run", str(run_dir))
        self.assertEqual(result.code, 0, result.err)
        return run_dir

    def report(self, run_dir: Path, fmt: str = "markdown") -> str:
        result = run_panel("report", "--run", str(run_dir), "--format", fmt)
        self.assertEqual(result.code, 0, result.err)
        return result.out


class TestPracticalReport(PracticalRunMixin):
    """T013, T014, T015, T034: the report layout of contracts/report-layout.md."""

    def test_markdown_matches_golden(self) -> None:
        markdown = self.report(self.practical_run())
        self.assert_golden("practical/expected-report.md", markdown)

    def test_json_matches_golden(self) -> None:
        run_dir = self.practical_run()
        self.report(run_dir, "json")
        data = read(run_dir / "report.json")
        self.assertEqual(panel.validate_message("report", data), [])
        data["scope"]["note"] = "<scope note>"
        self.assert_golden("practical/expected-report.json", json.dumps(data, indent=2) + "\n")

    def test_blocks_open_with_prose(self) -> None:
        markdown = self.report(self.practical_run())
        block = markdown.split("#### F1. ", 1)[1].split("####", 1)[0]
        order = [
            "Annual energy totals",
            "`high` · consensus",
            "This function converts",
            "**In practice.**",
            "- **Where:**",
            "- **Trigger:**",
            "- **Wrong output:**",
            "- **Fix:**",
        ]
        positions = [block.index(text) for text in order]
        self.assertEqual(positions, sorted(positions))

    def test_capped_release_finding(self) -> None:
        run_dir = self.practical_run()
        markdown = self.report(run_dir)
        self.assertIn("`medium` (lowered from high) · consensus · algorithmic-correctness · trigger: release", markdown)
        self.assertIn(
            "*(the finding quoted `SEARCH_GENERATIONS=5`; `.env:3` has `SEARCH_GENERATIONS=10`)*", markdown
        )
        f2 = next(f for f in read(run_dir / "adjudication.json")["findings"] if f["id"] == "F2")
        self.assertEqual(len(f2["value_corrections"]), 1)

    def test_design_question_section(self) -> None:
        run_dir = self.practical_run()
        markdown = self.report(run_dir)
        defects, questions = markdown.split("## Design questions", 1)
        self.assertNotIn("#### F3.", defects)
        self.assertIn("#### F3. Stored results are reused across schema versions", questions)
        self.assertIn("**Why it may be intended.** Keeping reports byte-identical", questions)
        self.assertIn("**If it is not intended.** A result in the old schema", questions)
        self.report(run_dir, "json")
        data = read(run_dir / "report.json")
        self.assertEqual([f["id"] for f in data["design_questions"]], ["F3"])
        self.assertNotIn("F3", [f["id"] for f in data["findings"]])

    def test_cap_withholds_design_questions_after_defects(self) -> None:
        run_dir = self.practical_run()
        (run_dir / "arguments.json").write_text(
            json.dumps(
                {
                    "level": "medium",
                    "level_source": "given",
                    "target_text": None,
                    "near_level": None,
                    "comment": False,
                    "fix": False,
                    "max_findings": 2,
                    "max_findings_source": "given",
                    "notes": [],
                    "raw": "--max-findings 2",
                }
            ),
            encoding="utf-8",
        )
        self.report(run_dir, "json")
        data = read(run_dir / "report.json")
        self.assertEqual(len(data["findings"]), 2)
        self.assertEqual(data["design_questions"], [])
        self.assertEqual(data["withheld"], 1)

    def test_report_findings_mapping(self) -> None:
        run_dir = self.practical_run()
        data = json.loads(self.report(run_dir, "json"))
        mapping = {r["line"]: r for r in data["report_findings"]}
        f1 = mapping[20]
        self.assertEqual(f1["short_summary"], "Annual energy totals shown in kBtu are about 12 times too small"[:60])
        self.assertTrue(f1["summary"].startswith("Annual energy totals shown in kBtu are about 12 times too small. "))
        self.assertTrue(f1["failure_scenario"].startswith("This function converts each building's"))
        self.assertIn(" In practice: Every user who views", f1["failure_scenario"])
        self.assertIn(" Trigger: annual_total_kbtu(1000)", f1["failure_scenario"])
        self.assertEqual(mapping[170]["category"], "design-question")

    def test_earlier_run_renders_not_recorded(self) -> None:
        run_dir = self.practical_run()
        data = read(run_dir / "adjudication.json")
        for finding in data["findings"]:
            for field in ("headline", "context", "in_practice"):
                finding.pop(field, None)
        (run_dir / "adjudication.json").write_text(json.dumps(data), encoding="utf-8")
        markdown = self.report(run_dir)
        self.assertIn("#### F1. The annual total converts kWh to kBtu", markdown)
        self.assertIn("Not recorded by this review.", markdown)


def git(project: Path, *argv: str) -> str:
    return subprocess.run(["git", *argv], cwd=project, capture_output=True, text=True, check=True).stdout


def commit_as(project: Path, author: str, date: str, message: str) -> None:
    env = {"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date, "PATH": "/usr/bin:/bin:/usr/local/bin"}
    subprocess.run(
        ["git", "-c", f"user.name={author}", "-c", f"user.email={author}@example.com", "commit", "-qam", message],
        cwd=project,
        check=True,
        env=env,
        capture_output=True,
    )


class TestIssue(PracticalRunMixin):
    """T041, T042, T043: the issue command of contracts/issue.md."""

    def issue(self, run_dir: Path, finding: str, *extra: str) -> tuple[int, str, str]:
        result = run_panel("issue", "--run", str(run_dir), "--finding", finding, *extra)
        return result.code, result.out, result.err

    def reported_run(self) -> Path:
        run_dir = self.practical_run()
        self.report(run_dir, "json")
        return run_dir

    def test_defect_issue_matches_golden(self) -> None:
        run_dir = self.reported_run()
        code, out, err = self.issue(run_dir, "F2")
        self.assertEqual(code, 0, err)
        self.assertEqual(out, (run_dir / "issues" / "F2.md").read_text(encoding="utf-8"))
        self.assert_golden("practical/expected-issue-F2.md", out)

    def test_design_question_issue_matches_golden(self) -> None:
        run_dir = self.reported_run()
        code, out, err = self.issue(run_dir, "F3")
        self.assertEqual(code, 0, err)
        self.assert_golden("practical/expected-issue-F3.md", out)

    def test_section_order(self) -> None:
        run_dir = self.reported_run()
        _code, out, _err = self.issue(run_dir, "F2")
        order = [
            "# Cached results are not recomputed after a release",
            "## Situation",
            "## Who hits this and when",
            "Trigger: a release of new code.",
            "## Bug or design question",
            "Defect, medium, lowered from high because its only trigger is a release of new code.",
            "## Where",
            "## Reproduction",
            "Note: the finding quoted `SEARCH_GENERATIONS=5`; `.env:3` has `SEARCH_GENERATIONS=10`.",
            "Result: ",
            "## Proposed fix",
            "## Suggested owners",
            "<sub>Found by a",
        ]
        positions = [out.index(text) for text in order]
        self.assertEqual(positions, sorted(positions))

    def test_design_question_title(self) -> None:
        run_dir = self.reported_run()
        _code, out, _err = self.issue(run_dir, "F3")
        self.assertTrue(out.startswith("# Confirm intended behaviour: Stored results are reused across schema"))
        self.assertIn("Please confirm which behaviour is wanted.", out)

    def test_contested_issue_gives_both_arguments(self) -> None:
        run_dir = self.reported_run()
        data = read(run_dir / "report.json")
        finding = data["findings"][0]
        finding.update(label="contested", argument_for="For it.", argument_against="Against it.",
                       deciding_assumption="Whether meters are in kWh.")  # fmt: skip
        (run_dir / "report.json").write_text(json.dumps(data), encoding="utf-8")
        _code, out, _err = self.issue(run_dir, finding["id"])
        for text in ("For: For it.", "Against: Against it.", "Decided by: Whether meters are in kWh."):
            self.assertIn(text, out)

    def test_earlier_run_prints_not_recorded(self) -> None:
        run_dir = self.reported_run()
        data = read(run_dir / "report.json")
        for field in ("headline", "context", "in_practice"):
            data["findings"][0].pop(field)
        (run_dir / "report.json").write_text(json.dumps(data), encoding="utf-8")
        _code, out, _err = self.issue(run_dir, data["findings"][0]["id"])
        self.assertIn("Not recorded by this review.", out)

    def test_unknown_withheld_or_rejected_id_is_a_usage_error(self) -> None:
        run_dir = self.reported_run()
        code, _out, err = self.issue(run_dir, "F9")
        self.assertEqual(code, 2)
        self.assertIn("delivered: F1, F2, F3", err)

    def test_missing_report_is_a_precondition_error(self) -> None:
        run_dir = self.practical_run()
        code, _out, err = self.issue(run_dir, "F1")
        self.assertEqual(code, 3)
        self.assertIn("run `panel.py report` first", err)

    def test_dry_run_writes_nothing(self) -> None:
        run_dir = self.reported_run()
        code, out, _err = self.issue(run_dir, "F1", "--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("[dry-run] would write", out)
        self.assertFalse((run_dir / "issues").exists())

    def test_not_a_git_repository(self) -> None:
        run_dir = self.reported_run()
        _code, out, _err = self.issue(run_dir, "F1")
        self.assertIn("No owners found: the project is not a git repository", out)


class TestOwners(unittest.TestCase):
    """T042: owners from CODEOWNERS (last match wins), from blame, and none."""

    def setUp(self) -> None:
        self.project = Path(tempfile.mkdtemp(prefix="sci-review-owners-"))
        self.addCleanup(shutil.rmtree, self.project, True)
        git(self.project, "init", "-q")
        target = self.project / "src" / "cache" / "x.py"
        target.parent.mkdir(parents=True)
        target.write_text("a = 1\nb = 2\nc = 3\n", encoding="utf-8")
        git(self.project, "add", ".")
        commit_as(self.project, "alice", "2026-01-01T00:00:00Z", "first")
        target.write_text("a = 1\nb = 20\nc = 30\n", encoding="utf-8")
        commit_as(self.project, "bob", "2026-02-01T00:00:00Z", "second")

    def head(self, project: Path | None = None) -> str:
        return git(project or self.project, "rev-parse", "HEAD").strip()

    def add_codeowners(self, text: str) -> None:
        path = self.project / ".github" / "CODEOWNERS"
        path.parent.mkdir(exist_ok=True)
        path.write_text(text, encoding="utf-8")
        git(self.project, "add", ".")
        commit_as(self.project, "carol", "2026-03-01T00:00:00Z", "owners")

    def test_codeowners_last_match_wins(self) -> None:
        self.add_codeowners("* @team-a\n/src/ @alice\nsrc/cache/ @bob\n")
        owners = panel.suggest_owners(self.project, self.head(), "src/cache/x.py", 1, 3)
        self.assertEqual(owners.source, "codeowners")
        self.assertEqual([o.name for o in owners.owners], ["@bob"])
        self.assertIn("From `.github/CODEOWNERS`: @bob", panel.owners_text(owners))

    def test_codeowners_without_a_match_falls_back_to_blame(self) -> None:
        self.add_codeowners("docs/ @writers\n")
        owners = panel.suggest_owners(self.project, self.head(), "src/cache/x.py", 1, 3)
        self.assertEqual(owners.source, "blame")

    def test_blame_orders_by_lines_then_date(self) -> None:
        owners = panel.suggest_owners(self.project, self.head(), "src/cache/x.py", 1, 3)
        self.assertEqual(owners.source, "blame")
        self.assertEqual([(o.name, o.lines) for o in owners.owners], [("bob", 2), ("alice", 1)])
        self.assertIn("bob (2 of 3 lines, last 2026-02-01)", panel.owners_text(owners))
        self.assertFalse(owners.truncated)

    def test_shallow_clone_is_reported_as_truncated(self) -> None:
        clone = Path(tempfile.mkdtemp(prefix="sci-review-shallow-"))
        self.addCleanup(shutil.rmtree, clone, True)
        subprocess.run(
            ["git", "clone", "-q", "--depth", "1", f"file://{self.project}", str(clone / "c")],
            check=True,
            capture_output=True,
        )
        owners = panel.suggest_owners(clone / "c", self.head(clone / "c"), "src/cache/x.py", 1, 3)
        self.assertTrue(owners.truncated)
        self.assertIn("History is truncated (shallow clone)", panel.owners_text(owners))

    def test_codeowners_patterns(self) -> None:
        cases = [
            ("*.py @py", "a/b.py", ("@py",)),
            ("docs/* @d", "docs/a.md", ("@d",)),
            ("docs/* @d", "docs/a/b.md", None),
            ("/build/ @b", "build/x/y.txt", ("@b",)),
            ("/build/ @b", "src/build/x.txt", None),
            ("apps/** @a", "apps/x/y/z.ts", ("@a",)),
            ("[Section]\nlib/ @l", "lib/x.py", ("@l",)),
        ]
        for text, path, expected in cases:
            with self.subTest(text=text, path=path):
                self.assertEqual(panel.codeowners_owners(text, path), expected)


if __name__ == "__main__":
    unittest.main()
