"""Tests of feature 008: code-review-style arguments for sci-review.

Covers the grammar table (SC-001, SC-004), the preferences store, level profiles (SC-002, SC-003), target
resolution on a fixture repository, the finding cap, part division (SC-008) and the presence in SKILL.md of
the sections reproduced from /code-review (research R10).

No test reads or writes the real ~/.config/sci-review/: every `args` call passes `--prefs` with a temporary
path.

Run with: python3 -m unittest tests.test_sci_review_arguments -v
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from dataclasses import dataclass
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
PANEL_PATH = ROOT / "plugins" / "sci-review" / "scripts" / "panel.py"
SKILL_MD = ROOT / "plugins" / "sci-review" / "skills" / "scientific-review" / "SKILL.md"
LARGE_SCOPE = ROOT / "tests" / "fixtures" / "sci-review" / "large-scope"

if "sci_review_panel" in sys.modules:
    panel = sys.modules["sci_review_panel"]
else:
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


def git_version() -> tuple[int, ...]:
    words = subprocess.run(["git", "--version"], check=True, capture_output=True, text=True).stdout.split()
    return tuple(int(n) for n in re.findall(r"\d+", words[2])[:2]) if len(words) > 2 else (0,)


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class RunMixin(unittest.TestCase):
    """A project directory, a run directory outside it, and a temporary preferences path (T002)."""

    def setUp(self) -> None:
        self.project = Path(tempfile.mkdtemp(prefix="sci-review-project-")).resolve()
        self.addCleanup(shutil.rmtree, self.project, True)
        config = Path(tempfile.mkdtemp(prefix="sci-review-config-")).resolve()
        self.addCleanup(shutil.rmtree, config, True)
        self.prefs = config / "sci-review" / "preferences.json"

    def init_run(self) -> Path:
        result = run_panel("init", "--project", str(self.project))
        self.assertEqual(result.code, 0, result.err)
        run_dir = Path(result.out.strip())
        self.addCleanup(shutil.rmtree, run_dir, True)
        return run_dir

    def args(self, run_dir: Path, argv: str, *extra: str) -> Result:
        return run_panel("args", "--run", str(run_dir), f"--argv={argv}", "--prefs", str(self.prefs), *extra)

    def arguments(self, run_dir: Path) -> dict:
        return json.loads((run_dir / "arguments.json").read_text(encoding="utf-8"))

    def build_repository(self) -> None:
        """The fixture repository of T003.

        `main` holds the base; `work` is checked out and changes `src/model.py`; `feature/other` is a second
        local branch, not checked out, that adds `src/other.py`; a branch `docs` collides with the directory
        `docs/` (FR-010).
        """
        git(self.project, "init", "-q")
        (self.project / "src").mkdir()
        (self.project / "src" / "model.py").write_text("def area(r):\n    return 3.14159 * r * r\n")
        (self.project / "docs").mkdir()
        (self.project / "docs" / "notes.md").write_text("# Notes\n")
        git(self.project, "add", "-A")
        git(self.project, "commit", "-q", "-m", "base")
        git(self.project, "branch", "docs")
        git(self.project, "checkout", "-q", "-b", "feature/other")
        (self.project / "src" / "other.py").write_text("def volume(r):\n    return 4 / 3 * 3.14159 * r**2\n")
        git(self.project, "add", "-A")
        git(self.project, "commit", "-q", "-m", "other")
        git(self.project, "checkout", "-q", "main")
        git(self.project, "checkout", "-q", "-b", "work")
        (self.project / "src" / "model.py").write_text("def area(r):\n    return 3.14159 * r**2\n")
        git(self.project, "add", "-A")
        git(self.project, "commit", "-q", "-m", "work")

    def project_state(self) -> tuple[str, str]:
        status = git(self.project, "status", "--porcelain", "--ignored")
        branch = git(self.project, "rev-parse", "--abbrev-ref", "HEAD").strip()
        return status, branch


# ---------------------------------------------------------------------------
# Grammar (T005)
# ---------------------------------------------------------------------------


class TestGrammar(RunMixin):
    def test_each_level_alone(self) -> None:
        for level in panel.Level.VALUES:
            with self.subTest(level=level):
                parsed = panel.parse_arguments(level)
                self.assertEqual(parsed.level, level)
                self.assertIsNone(parsed.target_text)
                self.assertEqual(panel.parse_arguments(level.upper()).level, level)

    def test_level_in_any_position_and_target_before_level(self) -> None:
        for text in ("high 12", "12 high", "--fix 12 high", "12 --comment high --fix"):
            with self.subTest(text=text):
                parsed = panel.parse_arguments(text)
                self.assertEqual(parsed.level, "high")
                self.assertEqual(parsed.target_text, "12")

    def test_flags_in_any_position(self) -> None:
        for text in ("--fix --comment", "--comment low --fix", "src/ --fix --comment"):
            with self.subTest(text=text):
                parsed = panel.parse_arguments(text)
                self.assertTrue(parsed.fix)
                self.assertTrue(parsed.comment)

    def test_max_findings_forms(self) -> None:
        cases = {
            "--max-findings 5": panel.CapChoice(panel.CapKind.NUMBER, 5),
            "--max-findings=5": panel.CapChoice(panel.CapKind.NUMBER, 5),
            "--max-findings all": panel.CapChoice(panel.CapKind.ALL),
            "--max-findings default": panel.CapChoice(panel.CapKind.DEFAULT),
            "--max-findings 5 --max-findings 9": panel.CapChoice(panel.CapKind.NUMBER, 9),
            "--max-findings 0": panel.CapChoice(panel.CapKind.MALFORMED),
            "--max-findings zero": panel.CapChoice(panel.CapKind.MALFORMED),
            "--max-findings": panel.CapChoice(panel.CapKind.MALFORMED),
            "--max-findings --fix": panel.CapChoice(panel.CapKind.MALFORMED),
            "": panel.CapChoice(panel.CapKind.ABSENT),
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(panel.parse_arguments(text).cap, expected)

    def test_max_findings_does_not_swallow_a_level(self) -> None:
        parsed = panel.parse_arguments("--max-findings low")
        self.assertEqual(parsed.level, "low")
        self.assertEqual(parsed.cap.kind, panel.CapKind.MALFORMED)

    def test_hash_and_backquotes_are_stripped_from_the_target(self) -> None:
        self.assertEqual(panel.parse_arguments("#12").target_text, "12")
        self.assertEqual(panel.parse_arguments("`#12` high").target_text, "12")
        self.assertEqual(panel.parse_arguments("`src/solver`").target_text, "src/solver")

    def test_usage_errors_write_nothing(self) -> None:
        run_dir = self.init_run()
        cases = {
            "--post": "--comment, --fix and --max-findings",
            "low high": "low, medium, high, xhigh or max",
            "ultra": panel.ULTRA_MESSAGE,
        }
        for argv, message in cases.items():
            with self.subTest(argv=argv):
                result = self.args(run_dir, argv)
                self.assertEqual(result.code, 2, result.err)
                self.assertIn(message, result.err)
                self.assertFalse((run_dir / "arguments.json").exists())
                self.assertFalse(self.prefs.exists())

    def test_ultra_message_is_exact(self) -> None:
        self.assertEqual(
            panel.ULTRA_MESSAGE,
            "`ultra` is not an effort level of the scientific review; use `max`.",
        )

    def test_near_level_is_recorded_not_rejected(self) -> None:
        run_dir = self.init_run()
        result = self.args(run_dir, "hig")
        self.assertEqual(result.code, 0, result.err)
        data = self.arguments(run_dir)
        self.assertEqual(data["near_level"], "hig")
        self.assertEqual(data["target_text"], "hig")
        self.assertEqual(data["level"], "medium")

    def test_malformed_max_findings_runs_with_a_note(self) -> None:
        for argv in ("--max-findings 0", "--max-findings zero", "--max-findings"):
            with self.subTest(argv=argv):
                run_dir = self.init_run()
                result = self.args(run_dir, argv)
                self.assertEqual(result.code, 0, result.err)
                notes = self.arguments(run_dir)["notes"]
                self.assertTrue(
                    any(n.startswith(panel.MAX_FINDINGS_IGNORED) for n in notes), notes
                )
                self.assertIn(f"{panel.MAX_FINDINGS_IGNORED} {panel.USUAL_LIMIT}", notes)

    def test_request_text_takes_only_grammar_tokens(self) -> None:
        parsed = panel.parse_arguments("scientific review, high, --max-findings 3", request_text=True)
        self.assertEqual(parsed.level, "high")
        self.assertEqual(parsed.cap, panel.CapChoice(panel.CapKind.NUMBER, 3))
        self.assertIsNone(parsed.target_text)
        self.assertIsNone(parsed.near_level)

    def test_request_text_with_several_level_words_takes_no_level(self) -> None:
        parsed = panel.parse_arguments("Review the filter that separates the low and high bands.", request_text=True)
        self.assertIsNone(parsed.level)
        parsed = panel.parse_arguments("high effort please, keep it high", request_text=True)
        self.assertEqual(parsed.level, "high")
        with self.assertRaises(panel.UsageFailure):
            panel.parse_arguments("low high")
        parsed = panel.parse_arguments("give this an ultra careful scientific review", request_text=True)
        self.assertIsNone(parsed.level)

    def test_arguments_read_from_standard_input(self) -> None:
        run_dir = self.init_run()
        with mock.patch("sys.stdin", io.StringIO("high --fix it's\n")):
            result = run_panel("args", "--run", str(run_dir), "--argv-stdin", "--prefs", str(self.prefs))
        self.assertEqual(result.code, 0, result.err)
        arguments = self.arguments(run_dir)
        self.assertEqual((arguments["level"], arguments["fix"], arguments["raw"]), ("high", True, "high --fix it's"))
        run_dir = self.init_run()
        with mock.patch("sys.stdin", io.StringIO("Review the low and high bands, --max-findings 3.\n")):
            result = run_panel("args", "--run", str(run_dir), "--text-stdin", "--prefs", str(self.prefs))
        self.assertEqual(result.code, 0, result.err)
        arguments = self.arguments(run_dir)
        self.assertEqual((arguments["level_source"], arguments["max_findings"]), ("default", 3))

    def test_text_option_writes_arguments(self) -> None:
        run_dir = self.init_run()
        result = run_panel(
            "args", "--run", str(run_dir), "--text", "please review, xhigh, --fix", "--prefs", str(self.prefs)
        )
        self.assertEqual(result.code, 0, result.err)
        data = self.arguments(run_dir)
        self.assertEqual((data["level"], data["fix"], data["target_text"]), ("xhigh", True, None))

    def test_args_dry_run_writes_nothing(self) -> None:
        run_dir = self.init_run()
        result = self.args(run_dir, "high --max-findings 4", "--persist", "--dry-run")
        self.assertEqual(result.code, 0, result.err)
        self.assertIn("[dry-run]", result.out)
        self.assertFalse((run_dir / "arguments.json").exists())
        self.assertFalse(self.prefs.exists())


# ---------------------------------------------------------------------------
# Preferences store (T006)
# ---------------------------------------------------------------------------


class TestPreferences(RunMixin):
    def test_missing_file_is_empty_with_a_note(self) -> None:
        loaded = panel.load_preferences(self.prefs)
        self.assertEqual(loaded.preferences, panel.UserPreferences())
        self.assertTrue(loaded.log)
        self.assertFalse(loaded.notes, "a missing file is not shown to the user")

    def test_invalid_file_is_empty_with_a_note(self) -> None:
        self.prefs.parent.mkdir(parents=True)
        self.prefs.write_text('{"version": 1, "last_level": "ultra"}')
        loaded = panel.load_preferences(self.prefs)
        self.assertEqual(loaded.preferences, panel.UserPreferences())
        self.assertTrue(loaded.notes)

    def test_file_of_another_version_is_empty_with_a_note(self) -> None:
        self.prefs.parent.mkdir(parents=True)
        for content in ('{"version": 2, "last_level": "high"}', '{"version": "1"}', '{"version": true}'):
            with self.subTest(content=content):
                self.prefs.write_text(content)
                loaded = panel.load_preferences(self.prefs)
                self.assertEqual(loaded.preferences, panel.UserPreferences())
                self.assertIn("version", loaded.notes[0])

    def test_file_that_is_not_utf8_is_empty_with_a_note(self) -> None:
        self.prefs.parent.mkdir(parents=True)
        self.prefs.write_bytes(b'{"version": 1, "last_level": "\xff"}')
        loaded = panel.load_preferences(self.prefs)
        self.assertEqual(loaded.preferences, panel.UserPreferences())
        self.assertTrue(loaded.notes)
        run_dir = self.init_run()
        self.assertEqual(self.args(run_dir, "high").code, 0)

    @unittest.skipIf(os.name == "nt" or os.geteuid() == 0, "permissions are not enforced")
    def test_unreadable_and_unwritable_directory_yield_notes(self) -> None:
        self.prefs.parent.mkdir(parents=True)
        self.prefs.write_text('{"version": 1, "last_level": "low"}')
        self.prefs.chmod(0)
        self.addCleanup(self.prefs.chmod, 0o600)
        loaded = panel.load_preferences(self.prefs)
        self.assertTrue(loaded.notes)
        self.assertIn("could not be read", loaded.notes[0])

        locked = self.prefs.parent.parent / "locked"
        locked.mkdir()
        locked.chmod(0o500)
        self.addCleanup(locked.chmod, 0o700)
        run_dir = self.init_run()
        result = run_panel(
            "args", "--run", str(run_dir), "--argv=high", "--persist", "--prefs", str(locked / "p" / "prefs.json")
        )
        self.assertEqual(result.code, 0, result.err)
        data = self.arguments(run_dir)
        self.assertEqual(data["level"], "high")
        self.assertTrue(any("could not be stored" in n for n in data["notes"]), data["notes"])

    def test_atomic_write(self) -> None:
        calls = []
        real_replace = os.replace

        def spy(src, dst):
            calls.append((Path(src), Path(dst)))
            self.assertTrue(Path(src).is_file())
            return real_replace(src, dst)

        with mock.patch.object(panel.os, "replace", spy):
            panel.save_preferences(self.prefs, panel.UserPreferences(last_level="low"), dry_run=False)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1], self.prefs)
        self.assertEqual(calls[0][0].parent, self.prefs.parent)
        self.assertEqual(json.loads(self.prefs.read_text())["last_level"], "low")
        self.assertEqual([p.name for p in self.prefs.parent.iterdir()], ["preferences.json"])

    def test_prefs_show_and_clear(self) -> None:
        panel.save_preferences(self.prefs, panel.UserPreferences(last_level="xhigh", last_max_findings=4), False)
        shown = run_panel("prefs", "--show", "--prefs", str(self.prefs))
        self.assertEqual(shown.code, 0, shown.err)
        self.assertEqual(json.loads(shown.out)["preferences"]["last_level"], "xhigh")
        dry = run_panel("prefs", "--clear", "--prefs", str(self.prefs), "--dry-run")
        self.assertEqual(dry.code, 0)
        self.assertTrue(self.prefs.exists())
        cleared = run_panel("prefs", "--clear", "--prefs", str(self.prefs))
        self.assertEqual(cleared.code, 0, cleared.err)
        self.assertFalse(self.prefs.exists())

    def test_default_path_resolution(self) -> None:
        home = Path.home()
        self.assertEqual(
            panel.preferences_path({"XDG_CONFIG_HOME": "/x/config"}, "linux"),
            Path("/x/config/sci-review/preferences.json"),
        )
        self.assertEqual(panel.preferences_path({}, "darwin"), home / ".config" / "sci-review" / "preferences.json")
        self.assertEqual(
            panel.preferences_path({"APPDATA": "C:/Users/u/AppData/Roaming"}, "win32"),
            Path("C:/Users/u/AppData/Roaming") / "sci-review" / "preferences.json",
        )

    def test_path_inside_the_project_is_refused(self) -> None:
        run_dir = self.init_run()
        inside = self.project / ".config" / "preferences.json"
        result = run_panel("args", "--run", str(run_dir), "--argv=low", "--persist", "--prefs", str(inside))
        self.assertEqual(result.code, 0, result.err)
        self.assertFalse(inside.exists())
        self.assertTrue(any("inside the reviewed project" in n for n in self.arguments(run_dir)["notes"]))


# ---------------------------------------------------------------------------
# Level profiles (T012) and level persistence (T013)
# ---------------------------------------------------------------------------

EXPECTED_PROFILES = {
    "low": (["theorist", "numerical-analyst", "methodologist"], 1, 1),
    "medium": (None, 2, 2),
    "high": (None, 2, 3),
    "xhigh": (None, 3, 4),
    "max": (None, 3, 4),
}
DEFAULT_IDS = ["theorist", "numerical-analyst", "experimentalist", "methodologist", "computer-scientist"]


class TestLevelProfiles(RunMixin):
    def panel_json(self, run_dir: Path) -> dict:
        return json.loads((run_dir / "panel.json").read_text(encoding="utf-8"))["panel"]

    def test_each_level_matches_the_table(self) -> None:
        for level, (ids, rounds, batches) in EXPECTED_PROFILES.items():
            with self.subTest(level=level):
                run_dir = self.init_run()
                result = run_panel("panel", "--run", str(run_dir), "--runner", "claude-agents", "--level", level)
                self.assertEqual(result.code, 0, result.err)
                data = self.panel_json(run_dir)
                self.assertEqual([p["id"] for p in data["perspectives"]], ids or DEFAULT_IDS)
                self.assertEqual((data["rebuttal_rounds"], data["max_batches"]), (rounds, batches))
                self.assertEqual((data["level"], data["overrides"]), (level, []))
                self.assertNotIn("max_findings", data)

    def test_no_parameter_decreases(self) -> None:
        profiles = [panel.LEVEL_PROFILES[level] for level in panel.Level.VALUES]
        for name in ("max_perspectives", "rebuttal_rounds", "max_batches"):
            values = [getattr(p, name) for p in profiles]
            self.assertEqual(values, sorted(values), name)
        self.assertTrue(all(p.default_cap is None for p in profiles))
        sizes = [len(p.requested(DEFAULT_IDS)) for p in profiles]
        self.assertEqual(sizes, sorted(sizes))

    def test_medium_equals_feature_007_defaults(self) -> None:
        available = [panel.default_perspective(pid, name) for pid, name in panel.DEFAULT_PERSPECTIVES]
        legacy, _ = panel.configure_panel(available, None, None, None, "claude-agents")
        run_dir = self.init_run()
        result = run_panel("panel", "--run", str(run_dir), "--runner", "claude-agents")
        self.assertEqual(result.code, 0, result.err)
        data = self.panel_json(run_dir)
        self.assertEqual((data["level"], data["level_source"]), ("medium", "default"))
        self.assertEqual(data, legacy.to_json())

    def test_explicit_option_overrides_the_profile(self) -> None:
        run_dir = self.init_run()
        result = run_panel(
            "panel", "--run", str(run_dir), "--runner", "sequential", "--level", "high", "--rounds", "1"
        )
        self.assertEqual(result.code, 0, result.err)
        data = self.panel_json(run_dir)
        self.assertEqual((data["rebuttal_rounds"], data["max_batches"]), (1, 3))
        self.assertEqual(data["overrides"], ["rounds"])

    def test_repeating_the_profile_records_no_override(self) -> None:
        run_dir = self.init_run()
        result = run_panel(
            "panel", "--run", str(run_dir), "--runner", "sequential", "--level", "low",
            "--perspectives", "theorist,numerical-analyst,methodologist", "--rounds", "1", "--batches", "1",
        )  # fmt: skip
        self.assertEqual(result.code, 0, result.err)
        self.assertEqual(self.panel_json(run_dir)["overrides"], [])

    def test_level_is_read_from_arguments_json(self) -> None:
        run_dir = self.init_run()
        self.assertEqual(self.args(run_dir, "xhigh").code, 0)
        run_panel("panel", "--run", str(run_dir), "--runner", "sequential")
        data = self.panel_json(run_dir)
        self.assertEqual((data["level"], data["level_source"], data["rebuttal_rounds"]), ("xhigh", "given", 3))


class TestLevelPersistence(RunMixin):
    def test_given_level_is_stored_and_reused(self) -> None:
        first = self.init_run()
        self.assertEqual(self.args(first, "xhigh", "--persist").code, 0)
        self.assertEqual(json.loads(self.prefs.read_text())["last_level"], "xhigh")
        second = self.init_run()
        self.assertEqual(self.args(second, "").code, 0)
        data = self.arguments(second)
        self.assertEqual((data["level"], data["level_source"]), ("xhigh", "reused"))
        self.assertTrue(any("xhigh" in n for n in data["notes"]))

    def test_no_persisted_level_yields_medium(self) -> None:
        run_dir = self.init_run()
        self.assertEqual(self.args(run_dir, "").code, 0)
        data = self.arguments(run_dir)
        self.assertEqual((data["level"], data["level_source"], data["notes"]), ("medium", "default", []))

    def test_without_persist_nothing_is_stored(self) -> None:
        run_dir = self.init_run()
        self.assertEqual(self.args(run_dir, "max --max-findings 3").code, 0)
        self.assertFalse(self.prefs.exists())


# ---------------------------------------------------------------------------
# Targets (T019) and clean (T020)
# ---------------------------------------------------------------------------


class TestTargets(RunMixin):
    def setUp(self) -> None:
        super().setUp()
        self.build_repository()

    def scope(self, run_dir: Path, *argv: str) -> Result:
        return run_panel("scope", "--run", str(run_dir), *argv)

    def scope_json(self, run_dir: Path) -> dict:
        return json.loads((run_dir / "scope.json").read_text(encoding="utf-8"))

    def test_branch_not_checked_out(self) -> None:
        before = self.project_state()
        run_dir = self.init_run()
        result = self.scope(run_dir, "--target", "feature/other")
        self.assertEqual(result.code, 0, result.err)
        scope = self.scope_json(run_dir)
        self.assertEqual(scope["target"]["kind"], "branch")
        self.assertEqual(scope["target"]["ref"], "feature/other")
        self.assertEqual([f["path"] for f in scope["files"]], ["src/other.py"])
        self.assertEqual(scope["total_lines"], 2)
        self.assertEqual(self.project_state(), before)

    def test_branch_target_is_read_from_its_ref(self) -> None:
        run_dir = self.init_run()
        self.assertEqual(self.scope(run_dir, "--target", "feature/other").code, 0)
        self.assertEqual(run_panel("parts", "--run", str(run_dir)).code, 0)
        parts = json.loads((run_dir / "parts.json").read_text())
        self.assertEqual(parts["total_lines"], 2)
        self.assertFalse((self.project / "src" / "other.py").exists())

    def test_existing_paths(self) -> None:
        run_dir = self.init_run()
        result = self.scope(run_dir, "--target", "src/model.py")
        self.assertEqual(result.code, 0, result.err)
        scope = self.scope_json(run_dir)
        self.assertEqual(scope["target"]["kind"], "paths")
        self.assertEqual([f["path"] for f in scope["files"]], ["src/model.py"])
        run_dir = self.init_run()
        self.assertEqual(self.scope(run_dir, "--target", "src/model.py docs/notes.md").code, 0)
        self.assertEqual(self.scope_json(run_dir)["target"]["paths"], ["src/model.py", "docs/notes.md"])

    def test_branch_and_path_collision_is_ambiguous(self) -> None:
        run_dir = self.init_run()
        result = self.scope(run_dir, "--target", "docs")
        self.assertEqual(result.code, 3, result.err)
        self.assertEqual(json.loads(result.out)["ambiguous"], ["branch", "paths"])
        self.assertFalse((run_dir / "scope.json").exists())

    def test_path_outside_the_project_is_a_usage_error(self) -> None:
        run_dir = self.init_run()
        result = self.scope(run_dir, "--target", "../elsewhere")
        self.assertEqual(result.code, 2, result.err)

    def test_near_level_without_branch_or_path_is_a_usage_error(self) -> None:
        for argv in ("hig", "hig src/"):
            with self.subTest(argv=argv):
                run_dir = self.init_run()
                self.assertEqual(self.args(run_dir, argv).code, 0)
                result = self.scope(run_dir)
                self.assertEqual(result.code, 2, result.err)
                self.assertIn(
                    "`hig` is not a recognised level: use low, medium, high, xhigh or max.", result.err
                )

    def test_near_level_that_is_a_branch_is_the_target(self) -> None:
        git(self.project, "branch", "hig", "feature/other")
        run_dir = self.init_run()
        self.assertEqual(self.args(run_dir, "hig").code, 0)
        result = self.scope(run_dir)
        self.assertEqual(result.code, 0, result.err)
        self.assertEqual(self.scope_json(run_dir)["target"]["kind"], "branch")

    def test_target_is_written_to_scope_not_arguments(self) -> None:
        run_dir = self.init_run()
        self.assertEqual(self.args(run_dir, "feature/other").code, 0)
        self.assertEqual(self.scope(run_dir).code, 0)
        self.assertNotIn("target", self.arguments(run_dir))
        self.assertEqual(self.arguments(run_dir)["target_text"], "feature/other")
        self.assertEqual(self.scope_json(run_dir)["target"]["text"], "feature/other")

    @unittest.skipUnless(git_version() >= (2, 40), "git check-attr --source needs git 2.40 or later")
    def test_branch_target_uses_its_own_gitattributes(self) -> None:
        worktree = self.project.parent / "generated-worktree"
        git(self.project, "worktree", "add", "-q", "-b", "with-generated", str(worktree), "main")
        (worktree / ".gitattributes").write_text("src/table.py linguist-generated\n")
        (worktree / "src" / "table.py").write_text("TABLE = [1, 2, 3]\n")
        (worktree / "src" / "rate.py").write_text("def rate(x):\n    return x / 2\n")
        git(worktree, "add", "-A")
        git(worktree, "commit", "-q", "-m", "generated table")
        git(self.project, "worktree", "remove", "--force", str(worktree))
        run_dir = self.init_run()
        result = self.scope(run_dir, "--target", "with-generated")
        self.assertEqual(result.code, 0, result.err)
        scope = self.scope_json(run_dir)
        self.assertIn("src/rate.py", [f["path"] for f in scope["files"]])
        self.assertIn({"path": "src/table.py", "reason": "generated (linguist attribute)"}, scope["excluded"])

    def test_merge_request_zero_is_not_a_target(self) -> None:
        self.assertIsNone(panel.pull_request_of("!0", self.project, True))
        self.assertEqual(panel.pull_request_of("!7", self.project, True).number, 7)

    def test_pull_request_without_gh_exits_3(self) -> None:
        bindir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, bindir, True)
        (bindir / "git").symlink_to(shutil.which("git"))
        run_dir = self.init_run()
        with mock.patch.dict(os.environ, {"PATH": str(bindir)}):
            result = self.scope(run_dir, "--target", "12")
        self.assertEqual(result.code, 3, result.err)
        self.assertEqual(json.loads(result.out)["missing"], "gh")

    def test_pull_request_forms(self) -> None:
        github = {"12": 12, "#12": 12, "https://github.com/o/r/pull/12": 12, "https://github.com/o/r/pull/7/files": 7}
        for text, number in github.items():
            with self.subTest(text=text):
                target = panel.classify_target(text, self.project)
                self.assertEqual((target.kind, target.host, target.number), ("pull-request", "github", number))
        gitlab = {"!12": 12, "https://gitlab.com/g/p/-/merge_requests/12": 12}
        for text, number in gitlab.items():
            with self.subTest(text=text):
                target = panel.classify_target(text, self.project)
                self.assertEqual((target.kind, target.host, target.number), ("pull-request", "gitlab", number))
        git(self.project, "remote", "add", "origin", "https://gitlab.example.com/g/p.git")
        self.assertEqual(panel.classify_target("12", self.project).host, "gitlab")

    def test_current_branch_target_reviews_the_working_tree(self) -> None:
        run_dir = self.init_run()
        result = self.scope(run_dir, "--target", "work")
        self.assertEqual(result.code, 0, result.err)
        scope = self.scope_json(run_dir)
        self.assertIsNone(scope["target"])
        self.assertEqual(scope["head"], panel.WORKTREE_HEAD)

    def test_unknown_target_is_a_usage_error(self) -> None:
        run_dir = self.init_run()
        self.assertEqual(self.scope(run_dir, "--target", "no-such-thing").code, 2)

    def test_clean_deletes_temporary_refs(self) -> None:
        head = git(self.project, "rev-parse", "HEAD").strip()
        git(self.project, "update-ref", "refs/sci-review/pr-12", head)
        git(self.project, "update-ref", "refs/sci-review/pr-13", head)
        run_dir = self.init_run()
        dry = run_panel("clean", "--run", str(run_dir), "--dry-run")
        self.assertIn("refs/sci-review/pr-12", dry.out)
        self.assertTrue(git(self.project, "for-each-ref", "refs/sci-review/").strip())
        result = run_panel("clean", "--run", str(run_dir))
        self.assertEqual(result.code, 0, result.err)
        self.assertEqual(git(self.project, "for-each-ref", "refs/sci-review/").strip(), "")
        self.assertTrue(git(self.project, "rev-parse", "--verify", "main").strip())


class TestHosting(unittest.TestCase):
    def test_failure_reasons(self) -> None:
        cases = {
            "GraphQL: Could not resolve to a PullRequest with the number of 9999. (repository.pullRequest)": None,
            "HTTP 404: Not Found": None,
            "failed to look up the author of the commit": None,
            "To get started with GitHub CLI, please run:  gh auth login": "auth",
            "HTTP 401: Bad credentials": "auth",
            "GraphQL: Could not resolve to a PullRequest with the number of 401. (repository.pullRequest)": None,
            "GET https://gitlab.com/api/v4/projects/1/merge_requests/403: 404 Not Found": None,
            "ERROR: 401 Unauthorized": "auth",
            "error: Unauthorized": "auth",
            "oauth token expired": "auth",
            "HTTP 403: Resource not accessible by integration": "auth",
            "fatal: unable to access 'https://github.com/o/r/': Could not resolve host: github.com": "network",
            "dial tcp 140.82.112.3:443: i/o timeout": "network",
        }
        for stderr, expected in cases.items():
            with self.subTest(stderr=stderr):
                self.assertEqual(panel._hosting_failure(stderr), expected)

    def test_remote_repository_forms(self) -> None:
        expected = ("github.com", "owner/repo")
        for url in (
            "https://github.com/owner/repo.git",
            "https://user@github.com/Owner/Repo",
            "git@github.com:owner/repo.git",
            "ssh://git@github.com:22/owner/repo.git",
        ):
            with self.subTest(url=url):
                self.assertEqual(panel.remote_repository(url), expected)

    def test_request_url_of_another_repository_is_fetched_from_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            git(project, "init", "-q")
            git(project, "remote", "add", "origin", "git@github.com:me/repo.git")
            git(project, "remote", "add", "work", "git@github-work:me/private.git")
            self.assertEqual(panel.request_remote(project, "12"), "origin")
            self.assertEqual(panel.request_remote(project, "https://github.com/me/repo/pull/12"), "origin")
            # An ssh host alias names the same repository under another host name.
            self.assertEqual(panel.request_remote(project, "https://github.com/me/private/pull/3"), "work")
            self.assertEqual(
                panel.request_remote(project, "https://github.com/upstream/repo/pull/12"),
                "https://github.com/upstream/repo.git",
            )
            git(project, "remote", "add", "upstream", "https://github.com/Upstream/Repo.git")
            self.assertEqual(panel.request_remote(project, "https://github.com/upstream/repo/pull/12"), "upstream")
            self.assertEqual(
                panel.request_remote(project, "https://gitlab.com/group/sub/proj/-/merge_requests/3"),
                "https://gitlab.com/group/sub/proj.git",
            )

    def fake_hosted_request(self, tmp: Path, head: str | None = None) -> tuple[Path, str, str]:
        """A hosted repository with pull request 5, a project without remotes, and a fake `gh` on PATH.

        The request's URL is rewritten to the hosted repository (url.<path>.insteadOf), so nothing leaves the
        machine. Returns the project, the base commit and the head commit.
        """
        source, hosted, project, bin_dir = tmp / "source", tmp / "hosted.git", tmp / "project", tmp / "bin"
        for directory in (source, project, bin_dir):
            directory.mkdir()
        git(source, "init", "-q")
        (source / "a.py").write_text("x = 1\n")
        git(source, "add", "-A")
        git(source, "commit", "-q", "-m", "base")
        base = git(source, "rev-parse", "HEAD").strip()
        (source / "a.py").write_text("x = 2\n")
        git(source, "commit", "-q", "-am", "head")
        pr_head = git(source, "rev-parse", "HEAD").strip()
        git(tmp, "init", "-q", "--bare", str(hosted))
        git(source, "push", "-q", str(hosted), f"{base}:refs/heads/main", f"{pr_head}:refs/pull/5/head")
        git(project, "init", "-q")
        git(project, "config", f"url.{hosted}.insteadOf", "https://github.com/me/repo.git")
        reported = {
            "baseRefOid": base,
            "headRefOid": head or pr_head,
            "baseRefName": "main",
            "url": "https://github.com/me/repo/pull/5",
        }
        (tmp / "gh.json").write_text(json.dumps(reported))
        gh = bin_dir / "gh"
        gh.write_text(f"#!/bin/sh\ncat '{tmp / 'gh.json'}'\n")
        gh.chmod(0o755)
        return project, base, pr_head

    def fetch(self, project: Path, bin_dir: Path) -> panel.PullRequestRefs:
        path = f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}"
        with mock.patch.dict(os.environ, {"PATH": path}), contextlib.redirect_stderr(io.StringIO()):
            target = panel.pull_request_of("5", project, True)
            assert target is not None
            return panel.fetch_pull_request(project, target)

    def test_request_is_fetched_from_the_repository_the_client_read(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            tmp = Path(name).resolve()
            project, base, pr_head = self.fake_hosted_request(tmp)
            refs = self.fetch(project, tmp / "bin")
            self.assertEqual(refs.base, base)
            self.assertEqual(git(project, "rev-parse", refs.head_ref).strip(), pr_head)

    def test_fetched_head_that_differs_from_the_reported_head_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            tmp = Path(name).resolve()
            project, _base, _head = self.fake_hosted_request(tmp, head="0" * 40)
            with self.assertRaises(panel.PreconditionFailure) as raised:
                self.fetch(project, tmp / "bin")
            self.assertIn("is not the head gh reports", str(raised.exception))


# ---------------------------------------------------------------------------
# Finding cap (T027) and cap persistence (T028)
# ---------------------------------------------------------------------------

LABELS = ("consensus", "majority", "contested")
SEVERITIES = ("high", "medium", "low")


def make_finding(n: int, label: str, severity: str) -> dict:
    finding = {
        "id": f"F{n}",
        "members": [f"theorist-{n}"],
        "raised_by": ["theorist"],
        "batch": 1,
        "file": "a.py",
        "line_start": n,
        "line_end": n,
        "dimension": "numerical-stability",
        "severity": severity,
        "summary": f"finding {n}",
        "trigger": f"x = {n}",
        "wrong_output": "nan",
        "fix": "guard",
        "label": label,
    }
    if label == "contested":
        finding.update(argument_for="for", argument_against="against", deciding_assumption=None)
    return finding


class TestCap(RunMixin):
    def prepare(self, count: int) -> Path:
        (self.project / "a.py").write_text("x = 1\n" * max(count, 1))
        run_dir = self.init_run()
        scope = panel.ReviewScope(
            mode="repository",
            base=None,
            head=None,
            files=(panel.ScopedFile(path="a.py", language="python"),),
            excluded=(),
            note="All files: 1 file.",
        )
        (run_dir / "scope.json").write_text(json.dumps(scope.to_json()))
        self.assertEqual(run_panel("panel", "--run", str(run_dir), "--runner", "claude-agents").code, 0)
        combos = [(label, severity) for label in reversed(LABELS) for severity in reversed(SEVERITIES)]
        findings = [make_finding(n + 1, *combos[n % len(combos)]) for n in range(count)]
        adjudication = {"findings": findings, "rejected": [], "records": [], "notices": []}
        (run_dir / "adjudication.json").write_text(json.dumps(adjudication))
        return run_dir

    def report(self, run_dir: Path) -> dict:
        result = run_panel("report", "--run", str(run_dir), "--format", "json")
        self.assertEqual(result.code, 0, result.err)
        return json.loads(result.out)

    def expected_order(self, run_dir: Path) -> list[str]:
        data = json.loads((run_dir / "adjudication.json").read_text())
        findings = [panel.Finding.from_json(f) for f in data["findings"]]
        return [f.id for f in panel.order_findings(findings)]

    def test_cap_of_five(self) -> None:
        run_dir = self.prepare(8)
        self.assertEqual(self.args(run_dir, "--max-findings 5").code, 0)
        report = self.report(run_dir)
        self.assertEqual([f["id"] for f in report["findings"]], self.expected_order(run_dir)[:5])
        self.assertEqual((report["max_findings"], report["withheld"]), (5, 3))
        stored = json.loads((run_dir / "report.json").read_text())
        self.assertEqual(len(stored["findings"]), 5)
        self.assertEqual(len(json.loads((run_dir / "adjudication.json").read_text())["findings"]), 8)
        markdown = run_panel("report", "--run", str(run_dir)).out
        self.assertIn("Finding cap: 5; 3 findings were withheld by it.", markdown)

    def test_all_default_and_no_argument_deliver_everything(self) -> None:
        for argv in ("--max-findings all", "--max-findings default", None):
            with self.subTest(argv=argv):
                run_dir = self.prepare(8)
                if argv is not None:
                    self.assertEqual(self.args(run_dir, argv).code, 0)
                report = self.report(run_dir)
                self.assertEqual((len(report["findings"]), report["withheld"]), (8, 0))

    def test_reporting_tool_is_clamped_to_32(self) -> None:
        run_dir = self.prepare(40)
        report = self.report(run_dir)
        self.assertEqual(len(report["findings"]), 40)
        self.assertEqual(len(report["report_findings"]), 32)
        self.assertEqual(report["report_tool_withheld"], 8)
        self.assertEqual(report["report_tool_notice"], panel.REPORT_TOOL_NOTICE)
        small = self.report(self.prepare(3))
        self.assertIsNone(small["report_tool_notice"])


class TestCapPersistence(RunMixin):
    def test_number_is_stored_reused_and_cleared(self) -> None:
        self.assertEqual(self.args(self.init_run(), "--max-findings 5", "--persist").code, 0)
        self.assertEqual(json.loads(self.prefs.read_text())["last_max_findings"], 5)
        run_dir = self.init_run()
        self.assertEqual(self.args(run_dir, "").code, 0)
        data = self.arguments(run_dir)
        self.assertEqual((data["max_findings"], data["max_findings_source"]), (5, "reused"))
        self.assertTrue(any(n.endswith(panel.DEFAULT_CAP_HINT) for n in data["notes"]), data["notes"])
        self.assertTrue(panel.DEFAULT_CAP_HINT.startswith("passing `--max-findings default` goes back to the usual limit"))
        self.assertEqual(self.args(self.init_run(), "--max-findings default", "--persist").code, 0)
        self.assertNotIn("last_max_findings", json.loads(self.prefs.read_text()))

    def test_malformed_value_keeps_and_applies_the_stored_cap(self) -> None:
        panel.save_preferences(self.prefs, panel.UserPreferences(last_max_findings=4), False)
        run_dir = self.init_run()
        self.assertEqual(self.args(run_dir, "--max-findings zero", "--persist").code, 0)
        data = self.arguments(run_dir)
        self.assertEqual((data["max_findings"], data["max_findings_source"]), (4, "reused"))
        self.assertIn(panel.MAX_FINDINGS_IGNORED, data["notes"])
        self.assertEqual(json.loads(self.prefs.read_text())["last_max_findings"], 4)

    def test_without_persist_nothing_is_stored(self) -> None:
        self.assertEqual(self.args(self.init_run(), "--max-findings all").code, 0)
        self.assertFalse(self.prefs.exists())


# ---------------------------------------------------------------------------
# Review parts (T034) and the confirmation sentence (T035)
# ---------------------------------------------------------------------------


class TestParts(RunMixin):
    def large_parts(self) -> tuple[dict, dict]:
        shutil.copytree(LARGE_SCOPE, self.project, dirs_exist_ok=True)
        run_dir = self.init_run()
        self.assertEqual(run_panel("scope", "--run", str(run_dir), "--mode", "repository").code, 0)
        result = run_panel("parts", "--run", str(run_dir))
        self.assertEqual(result.code, 0, result.err)
        self.assertIn("confirmation required", result.out)
        scope = json.loads((run_dir / "scope.json").read_text())
        return scope, json.loads((run_dir / "parts.json").read_text())

    def test_large_scope_division(self) -> None:
        scope, parts = self.large_parts()
        self.assertFalse([e for e in scope["excluded"] if "budget" in e["reason"]])
        self.assertEqual((parts["threshold"], parts["confirm_required"]), (6000, True))
        self.assertEqual(parts["total_lines"], scope["total_lines"])
        self.assertGreater(parts["total_lines"], 17000)
        self.assertEqual([p["id"] for p in parts["parts"]], [f"p{i}" for i in range(1, len(parts["parts"]) + 1)])
        self.assertEqual(len(parts["parts"]), 9)

        covered: dict[str, list[int]] = {}
        for part in parts["parts"]:
            for scoped in part["files"]:
                size = panel.count_lines((self.project / scoped["path"]).read_bytes())
                ranges = scoped["line_ranges"] or [[1, size]]
                for start, end in ranges:
                    covered.setdefault(scoped["path"], []).extend(range(start, end + 1))
            single = len(part["files"]) == 1 and len(part["files"][0]["line_ranges"]) <= 1
            self.assertTrue(part["lines"] <= 2000 or single, part["id"])
        for scoped in scope["files"]:
            size = panel.count_lines((self.project / scoped["path"]).read_bytes())
            self.assertEqual(sorted(covered[scoped["path"]]), list(range(1, size + 1)), scoped["path"])

        part_of = {}
        for part in parts["parts"]:
            for scoped in part["files"]:
                part_of.setdefault(scoped["path"], set()).add(part["id"])
        for directory in ("atmosphere", "chemistry", "units"):
            ids = {pid for path, pids in part_of.items() if path.startswith(directory + "/") for pid in pids}
            self.assertEqual(len(ids), 1, directory)

        kernels = (self.project / "solver" / "kernels.py").read_text().splitlines()
        starts = [r[0] for p in parts["parts"] for f in p["files"] if f["path"] == "solver/kernels.py" for r in f["line_ranges"]]
        self.assertGreater(len(starts), 1)
        for start in starts[1:]:
            self.assertRegex(kernels[start - 1], r"^(def|class|async def|@)")

        order = [min(p["files"], key=lambda f: f["path"])["path"] for p in parts["parts"]]
        self.assertEqual(order[-1].split("/")[0], "units")
        self.assertIn("units/conversions.py", part_of)

    def test_small_scope_is_one_part(self) -> None:
        (self.project / "a.py").write_text("x = 1\n" * 50)
        run_dir = self.init_run()
        self.assertEqual(run_panel("scope", "--run", str(run_dir), "--mode", "repository").code, 0)
        self.assertEqual(run_panel("parts", "--run", str(run_dir)).code, 0)
        parts = json.loads((run_dir / "parts.json").read_text())
        self.assertEqual((len(parts["parts"]), parts["confirm_required"], parts["total_lines"]), (1, False, 50))

    def test_parts_records_the_count_in_panel_json(self) -> None:
        (self.project / "a.py").write_text("x = 1\n")
        run_dir = self.init_run()
        run_panel("scope", "--run", str(run_dir), "--mode", "repository")
        run_panel("panel", "--run", str(run_dir), "--runner", "sequential")
        run_panel("parts", "--run", str(run_dir))
        self.assertEqual(json.loads((run_dir / "panel.json").read_text())["panel"]["parts"], 1)

    def test_split_range_at_boundaries_and_windows(self) -> None:
        self.assertEqual(panel.split_range(1, 4500, []), [(1, 2000), (2001, 4000), (4001, 4500)])
        self.assertEqual(panel.split_range(1, 3000, [1500]), [(1, 1499), (1500, 3000)])
        self.assertEqual(panel.split_range(1, 2500, [10]), [(1, 9), (10, 2500)])

    def test_skill_states_confirmation_on_own_initiative(self) -> None:
        text = normalise(SKILL_MD.read_text(encoding="utf-8"))
        for sentence in (
            "A review started on your own initiative always asks before a scope that requires confirmation.",
            "will be reviewed in <K> parts. Continue?",
            # T069 (validation.md section 5.4 observation 2): the confirmation is its own question.
            "Ask this as a separate question, after the scope and its mode are resolved and `parts.json` is written.",
            "Never fold it into another question, such as the mode question of section 3",
            "an answer to another question never counts as confirmation.",
        ):
            self.assertTrue(sentence in text, f"SKILL.md lacks: {sentence}")


# ---------------------------------------------------------------------------
# Sections reproduced from /code-review (T050, T054; research R10)
# ---------------------------------------------------------------------------

COMMENT_GITHUB = [
    "## Posting to GitHub (--comment)",
    "The `--comment` flag was passed. After producing the findings list, if the review target is a GitHub PR, "
    "post each finding as an inline PR comment via `mcp__github_inline_comment__create_inline_comment` (one call "
    "per finding; include a suggestion block only when it fully fixes the issue). If that tool is not available "
    "in this session, fall back to `gh api` (repos/{owner}/{repo}/pulls/{pr}/comments) or print the findings "
    "instead. If the target is not a PR, print the findings to the terminal and note that `--comment` was ignored.",
]
COMMENT_GITLAB = [
    "## Posting to GitLab (--comment)",
    "The `--comment` flag was passed. After producing the findings list, if the review target is a GitLab merge "
    "request, post the findings as one general MR note via `glab mr note <iid> [-R <project>] -m \"<body>\"` "
    "(every finding with its file:line, the issue, and the suggested fix). glab has no single verb for "
    "line-anchored comments; those require `glab api projects/:id/merge_requests/:iid/discussions`, so post the "
    "general note unless the user asks for inline threads. If glab is not available in this session, print the "
    "findings instead. If the target is not an MR, print the findings to the terminal and note that `--comment` "
    "was ignored.",
]
FIX = [
    "## Applying fixes (--fix)",
    "The `--fix` flag was passed. After producing the findings list, apply the findings to the working tree "
    "instead of stopping at the report: fix each one directly",
    "Skip any finding whose fix would change intended behavior, require changes well outside the reviewed diff, "
    "or that you judge to be a false positive; note the skip rather than arguing with it.",
    "Then call ReportFindings again with the same findings, each carrying an `outcome`: `fixed`, "
    "`no_change_needed` (the finding was wrong or already handled), or `skipped` (real but not applied). Do not "
    "repeat the findings as text; after the call, give one line per skipped finding saying why.",
    "Finish with a brief summary of what was fixed and what was skipped.",
]
FIXED_LATER = [
    "## If findings are fixed later",
    "Whenever reported findings get fixed later in this session (the user asks you to fix them, or later work "
    "fixes them incidentally) you MUST call ReportFindings again with the same findings, each carrying an "
    "`outcome`: `fixed`, `no_change_needed` (the finding was wrong or already handled), or `skipped` (real but "
    "not applied). Do not repeat the findings as text.",
    "Make that call immediately after the fixes land, before any prose summary; the host UI's per-finding status "
    "updates only from it, and without it the findings stay marked unresolved.",
]
OUTCOME_LINES = [
    "After the call, give one line per finding with its outcome: this session can also be read from a client "
    "that does not show the tool call.",
]
ADAPTED = [
    "every delivered finding",
    "Skipping a finding never changes its agreement label.",
    "Run the relevant checks after.",
    "Each comment states the finding's agreement label, severity and dimension, then the issue and the scenario.",
    "A finding that does not anchor to a line of the PR diff is printed with a note, not posted.",
    "Post nothing when the review has no findings.",
]


class TestReproducedSections(unittest.TestCase):
    def setUp(self) -> None:
        self.text = normalise(SKILL_MD.read_text(encoding="utf-8"))

    def assert_lines(self, lines: list[str]) -> None:
        for line in lines:
            with self.subTest(line=line[:60]):
                self.assertTrue(normalise(line) in self.text, f"SKILL.md lacks: {line}")

    def test_citation(self) -> None:
        self.assertTrue("Source text: Claude Code 2.1.317" in self.text, "SKILL.md lacks the citation")

    def test_arguments_are_passed_without_shell_expansion(self) -> None:
        raw = SKILL_MD.read_text(encoding="utf-8")
        self.assertNotIn('--argv="$ARGUMENTS"', raw)
        self.assertNotIn("$(cat <<", raw)
        block = re.search(r"```bash\n(\s*\$PANEL args .*?\n)\s*```", raw, re.DOTALL)
        assert block is not None, "SKILL.md lacks the args command block"
        self.assertIn("--argv-stdin <<'SCI_REVIEW_ARGS'", block.group(1))
        # The block, with $ARGUMENTS replaced by hostile text, passes that text to panel.py unchanged in every shell
        # present, bash 3.2 (macOS /bin/bash) included: an unbalanced `)` or quote once ran commands there.
        hostile = 'high `touch pwned` $(touch pwned2) a)$(touch pwned3) it\'s "my dir --fix'
        shells = [shell for shell in ("/bin/bash", "bash", "zsh", "/bin/sh", "dash") if shutil.which(shell)]
        panel_py = ROOT / "plugins" / "sci-review" / "scripts" / "panel.py"
        for shell in shells:
            with self.subTest(shell=shell), tempfile.TemporaryDirectory() as name:
                tmp = Path(name).resolve()
                (tmp / "project").mkdir()
                run_dir = Path(run_panel("init", "--project", str(tmp / "project")).out.strip())
                self.addCleanup(shutil.rmtree, run_dir, True)
                script = (
                    textwrap.dedent(block.group(1))
                    .replace("$PANEL", f"'{sys.executable}' '{panel_py}'")
                    .replace("$RUN", f"'{run_dir}'")
                    .replace("$ARGUMENTS", hostile)
                )
                env = {**os.environ, "XDG_CONFIG_HOME": str(tmp / "config")}
                result = subprocess.run([shell, "-c", script], cwd=tmp, capture_output=True, text=True, env=env)
                self.assertEqual(result.returncode, 0, result.stderr)
                arguments = json.loads((run_dir / "arguments.json").read_text(encoding="utf-8"))
                self.assertEqual(arguments["raw"], hostile)
                self.assertEqual(sorted(p.name for p in tmp.iterdir()), ["project"])

    def test_panel_command_is_never_a_shell_variable(self) -> None:
        # zsh does not split `$PANEL` holding "python3 .../panel.py"; every definition says to write it in full.
        skill_dir = SKILL_MD.parent
        for path in [SKILL_MD, *sorted((skill_dir / "runners").glob("*.md"))]:
            definition = next(
                (line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("| `$PANEL` |")), None
            )
            with self.subTest(file=path.name):
                if definition is None:
                    self.fail(f"{path.name} does not define $PANEL")
                self.assertIn("never store it in a shell variable", definition)

    def test_comment_sections(self) -> None:
        self.assert_lines(COMMENT_GITHUB + COMMENT_GITLAB)

    def test_fix_sections(self) -> None:
        self.assert_lines(FIX + FIXED_LATER + OUTCOME_LINES)

    def test_adaptations(self) -> None:
        self.assert_lines(ADAPTED)

    def test_no_verify_hand_off(self) -> None:
        self.assertNotIn("/verify", self.text)


if __name__ == "__main__":
    unittest.main()
