"""Tests for plugins/project-kit/scripts/audit_project.py against a local fixture template.

Run with: uv run --no-project python -m unittest discover -s tests -v
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_new_project import SCRIPT as NEW_PROJECT
from test_new_project import git, make_template
from test_upgrade_project import clean_env, commit_all

SCRIPT = NEW_PROJECT.parent / "audit_project.py"

PRE_COMMIT = """\
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: "v0.14.9"
    hooks:
      - id: ruff-check
      - id: ruff-format
"""

CHANGELOG = """\
# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]
"""


def tree_hash(path: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(str(file.relative_to(path)).encode() + b"\0" + file.read_bytes())
    return digest.hexdigest()


class AuditProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory(prefix="pk-audit-")
        cls.root = Path(cls._tmp.name)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def setUp(self) -> None:
        self.work = Path(tempfile.mkdtemp(prefix="case-", dir=self.root))
        # A template that meets the standards, so a fresh project audits clean.
        self.template = make_template(self.work / "template")
        folder = self.template / "{{cookiecutter.project_name}}"
        (folder / ".pre-commit-config.yaml").write_text(PRE_COMMIT, encoding="utf-8")
        (folder / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
        (folder / "pyproject.toml").write_text('[project]\nname = "{{ cookiecutter.project_name }}"\n', "utf-8")
        commit_all(self.template, "standards")
        self.project = self.create("audit-proj")

    def create(self, name: str) -> Path:
        answers = self.work / "answers.json"
        answers.write_text(json.dumps({"project_name": name, "author": "Ada", "email": "ada@example.com"}), "utf-8")
        args = ["create", "--template", str(self.template), "--answers", str(answers), "--dest", str(self.work)]
        proc = subprocess.run(
            [sys.executable, str(NEW_PROJECT), *args], capture_output=True, text=True, check=False, env=clean_env()
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return self.work / name

    def audit(self, *extra: str, project: Path | None = None) -> dict:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--project", str(project or self.project), "--template", str(self.template)]
            + list(extra),
            capture_output=True,
            text=True,
            check=False,
            env=clean_env(),
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return json.loads(proc.stdout)

    def ids(self, out: dict) -> dict[str, str]:
        return {f["id"]: f["severity"] for f in out["findings"]}

    def change(self, message: str, edit) -> None:  # noqa: ANN001
        edit(self.project)
        commit_all(self.project, message)

    # --- US1 --------------------------------------------------------------------

    def test_fresh_project_is_clean_and_unchanged(self) -> None:
        before = (tree_hash(self.project), git("status", "--porcelain", cwd=self.project))
        out = self.audit()
        self.assertEqual(out["summary"], {"error": 0, "warning": 0, "info": 0}, out["findings"])
        self.assertTrue(out["linked"])
        self.assertEqual(out["template"]["behind"], 0)
        self.assertEqual(out["skipped"], [])
        self.assertEqual(
            set(out["passed"]),
            {"git-repository", "git-clean", "template-current", "template-drift", "pre-commit", "linter"}
            | {"changelog", "speckit"},
        )
        self.assertEqual((tree_hash(self.project), git("status", "--porcelain", cwd=self.project)), before)

    def test_seeded_defects_are_each_reported(self) -> None:
        def edit_readme(p: Path) -> None:
            (p / "README.md").write_text("# My own readme\n", encoding="utf-8")

        def break_changelog(p: Path) -> None:
            (p / "CHANGELOG.md").write_text("# Changelog\n\n## 1.0.0\n", encoding="utf-8")

        self.change("readme", edit_readme)
        self.change("changelog", break_changelog)
        self.change("no spec-kit", lambda p: shutil.rmtree(p / ".specify"))
        (self.template / "NEWS.md").write_text("template news\n", encoding="utf-8")
        (self.template / "{{cookiecutter.project_name}}" / "NOTES.md").write_text("notes\n", encoding="utf-8")
        commit_all(self.template, "template moves on")

        out = self.audit()
        self.assertEqual(
            self.ids(out),
            {
                "template-behind": "warning",
                "template-drift": "info",
                "changelog-format": "warning",
                "speckit-missing": "warning",
            },
        )
        by_id = {f["id"]: f for f in out["findings"]}
        self.assertEqual(by_id["template-behind"]["behind"], 1, "NEWS.md is outside the template folder")
        self.assertIn("README.md", by_id["template-drift"]["files"])
        self.assertIn("CHANGELOG.md", by_id["template-drift"]["files"])
        self.assertEqual([f["severity"] for f in out["findings"]][-1], "info", "sorted by severity")

    def test_lint_setup_and_changelog_errors(self) -> None:
        def no_ruff(p: Path) -> None:
            (p / ".pre-commit-config.yaml").write_text("repos: []\n", encoding="utf-8")

        self.change("no ruff", no_ruff)
        self.assertEqual(self.ids(self.audit("--offline"))["linter-missing"], "error")
        self.change("no pre-commit", lambda p: (p / ".pre-commit-config.yaml").unlink())
        self.change("no changelog", lambda p: (p / "CHANGELOG.md").unlink())
        ids = self.ids(self.audit("--offline"))
        self.assertEqual((ids["pre-commit-missing"], ids["changelog-missing"]), ("error", "error"))
        self.assertNotIn("linter-missing", ids)

    def test_dirty_tree_and_offline(self) -> None:
        (self.project / "scratch.txt").write_text("wip\n", encoding="utf-8")
        out = self.audit("--offline")
        self.assertEqual(self.ids(out), {"git-dirty": "warning"})
        self.assertEqual(out["skipped"], [{"check": "template", "reason": "offline"}])

    # --- US2 --------------------------------------------------------------------

    def test_unlinked_project(self) -> None:
        self.change("unlink", lambda p: (p / ".cruft.json").unlink())
        out = self.audit()
        self.assertFalse(out["linked"])
        self.assertEqual(self.ids(out), {"not-linked": "warning"})
        self.assertEqual(out["skipped"], [{"check": "template", "reason": "not linked"}])

    def test_foreign_folder(self) -> None:
        folder = self.work / "plain"
        folder.mkdir()
        out = self.audit(project=folder)
        self.assertEqual(
            self.ids(out),
            {
                "not-git": "error",
                "pre-commit-missing": "error",
                "changelog-missing": "error",
                "language-unknown": "warning",
                "not-linked": "warning",
                "speckit-missing": "warning",
            },
        )
        self.assertEqual(sorted(p.name for p in folder.iterdir()), [])

    def test_missing_folder(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--project", str(self.work / "nope")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 3)
        self.assertEqual(json.loads(proc.stdout)["status"], "environment")


if __name__ == "__main__":
    unittest.main()
