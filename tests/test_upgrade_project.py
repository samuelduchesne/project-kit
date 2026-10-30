"""Tests for plugins/project-kit/scripts/upgrade_project.py against a local fixture template.

Run with: uv run --no-project python -m unittest discover -s tests -v

The fixture template has two commits: the second changes README.md, adds a question (``use_ci``) and a file that
uses it. Projects are generated at the first commit, linked (with new_project.py) or unlinked (plain generation,
committed with an older date), then upgraded.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_new_project import SCRIPT as NEW_PROJECT
from test_new_project import git, make_node_template, make_template

SCRIPTS = NEW_PROJECT.parent
SCRIPT = SCRIPTS / "upgrade_project.py"
sys.path.insert(0, str(SCRIPTS))

from new_project import CRUFT  # noqa: E402

OLD_DATE = "2024-01-01T12:00:00+00:00"
PROJECT_DATE = "2024-06-01T12:00:00+00:00"
NEW_DATE = "2025-01-01T12:00:00+00:00"
PERSON = {"author": "Ada Lovelace", "email": "ada@example.com"}


def clean_env(**extra: str) -> dict[str, str]:
    env = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith(("GIT_AUTHOR_", "GIT_COMMITTER_", "GIT_CONFIG_")) and k != "EMAIL"
    }
    env.update({"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}, **extra)
    return env


def commit_all(path: Path, message: str, date: str | None = None) -> str:
    env = clean_env(**({"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date} if date else {}))
    for args in (
        ["add", "-A"],
        ["-c", "user.name=T", "-c", "user.email=t@example.com", "commit", "-q", "--no-verify", "-m", message],
    ):
        subprocess.run(["git", *args], cwd=path, check=True, capture_output=True, env=env)
    return git("rev-parse", "HEAD", cwd=path).strip()


class UpgradeProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory(prefix="pk-upgrade-")
        cls.root = Path(cls._tmp.name)
        cls.template = cls.root / "template"
        saved = {k: os.environ.get(k) for k in ("GIT_AUTHOR_DATE", "GIT_COMMITTER_DATE")}
        os.environ.update(GIT_AUTHOR_DATE=OLD_DATE, GIT_COMMITTER_DATE=OLD_DATE)
        try:
            make_template(cls.template)
        finally:
            for key, value in saved.items():
                os.environ.pop(key) if value is None else os.environ.__setitem__(key, value)
        cls.old = git("rev-parse", "HEAD", cwd=cls.template).strip()
        git("branch", "v1", cwd=cls.template)
        # Second template commit, a year later.
        definition = json.loads((cls.template / "cookiecutter.json").read_text(encoding="utf-8"))
        definition["use_ci"] = True
        (cls.template / "cookiecutter.json").write_text(json.dumps(definition, indent=2), encoding="utf-8")
        project = cls.template / "{{cookiecutter.project_name}}"
        (project / "README.md").write_text(
            "# {{ cookiecutter.project_name }}\n\nFlavour: {{ cookiecutter.flavor }}\n", encoding="utf-8"
        )
        (project / "CI.md").write_text("CI: {{ cookiecutter.use_ci }}\n", encoding="utf-8")
        cls.new = commit_all(cls.template, "template v2", NEW_DATE)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def setUp(self) -> None:
        self.parent = Path(tempfile.mkdtemp(prefix="dest-", dir=self.root))

    # --- helpers ----------------------------------------------------------------

    def run_script(self, script: Path, *args: str) -> tuple[int, dict]:
        proc = subprocess.run(
            [sys.executable, str(script), *args], capture_output=True, text=True, check=False, env=clean_env()
        )
        try:
            return proc.returncode, json.loads(proc.stdout)
        except json.JSONDecodeError:
            self.fail(f"no JSON on stdout (exit {proc.returncode}):\n{proc.stdout}\n{proc.stderr}")

    def upgrade(self, command: str, project: Path, *args: str) -> tuple[int, dict]:
        return self.run_script(SCRIPT, command, "--project", str(project), "--template", str(self.template), *args)

    def answers(self, **values: object) -> str:
        path = Path(tempfile.mkstemp(suffix=".json", dir=self.root)[1])
        path.write_text(json.dumps(values), encoding="utf-8")
        return str(path)

    def linked_project(self, name: str) -> Path:
        """A project created by new-project at the old template commit."""
        code, out = self.run_script(
            NEW_PROJECT,
            "create",
            "--template",
            str(self.template),
            "--ref",
            "v1",
            "--answers",
            self.answers(project_name=name, **PERSON),
            "--dest",
            str(self.parent),
        )
        self.assertEqual(code, 0, out)
        project = Path(out["project_dir"])
        # new-project records the ref it was given; a project created from main records "main".
        cruft = json.loads((project / ".cruft.json").read_text(encoding="utf-8"))
        cruft["checkout"] = "main"
        (project / ".cruft.json").write_text(json.dumps(cruft, indent=2) + "\n", encoding="utf-8")
        commit_all(project, "follow main")
        return project

    def unlinked_project(self, name: str, **answers: object) -> Path:
        """A project generated by hand from the old template commit, before cruft was used."""
        out = self.parent / "render"
        context = self.answers(project_name=name, **PERSON, **answers)
        subprocess.run(
            [
                *CRUFT,
                "create",
                str(self.template),
                "--no-input",
                "--checkout",
                self.old,
                "--output-dir",
                str(out),
                "--extra-context-file",
                context,
            ],
            check=True,
            capture_output=True,
            env=clean_env(),
        )
        project = self.parent / name
        (out / name).rename(project)
        (project / ".cruft.json").unlink()
        (project / "pyproject.toml").write_text(f'[project]\nname = "{name}"\n', encoding="utf-8")  # a local file
        git("init", "-q", "-b", "main", cwd=project)
        commit_all(project, "initial", PROJECT_DATE)
        return project

    def snapshot(self, project: Path) -> tuple[str, str]:
        return git("rev-parse", "HEAD", cwd=project), git("status", "--porcelain", "--untracked-files=all", cwd=project)

    def test_project_state_code_does_not_rename_new_projects_destination_code(self) -> None:
        import new_project
        import upgrade_project

        self.assertEqual(upgrade_project.EXIT_PROJECT, 6)
        self.assertEqual(new_project.STATUS[new_project.EXIT_DESTINATION], "destination")
        self.assertEqual(new_project.STATUS[upgrade_project.EXIT_PROJECT], "project")

    # --- status -------------------------------------------------------------------

    def test_status_of_linked_project(self) -> None:
        project = self.linked_project("st-linked")
        code, out = self.upgrade("status", project)
        self.assertEqual(code, 0, out)
        self.assertTrue(out["linked"])
        self.assertEqual(out["language"], "python")
        self.assertEqual(out["link"]["commit"], self.old)
        self.assertEqual(out["latest_commit"], self.new)
        self.assertEqual(out["behind"], 1)
        self.assertFalse(out["up_to_date"])
        self.assertEqual([q["name"] for q in out["new_questions"]], ["use_ci"])
        self.assertEqual(out["git"]["clean"], True)

    def test_status_of_unlinked_project_suggests_its_base_commit(self) -> None:
        project = self.unlinked_project("st-unlinked")
        code, out = self.upgrade("status", project)
        self.assertEqual(code, 0, out)
        self.assertFalse(out["linked"])
        self.assertEqual(out["suggested_commit"]["commit"], self.old)
        self.assertEqual(out["questions_at"], self.old)
        self.assertNotIn("use_ci", {q["name"] for q in out["questions"]})

    def test_status_of_node_project_older_than_the_node_template(self) -> None:
        """A Node project started before node/ existed has no base commit, instead of failing on that commit."""
        template = self.root / f"late-node-{self.parent.name}"
        saved = {k: os.environ.get(k) for k in ("GIT_AUTHOR_DATE", "GIT_COMMITTER_DATE")}
        os.environ.update(GIT_AUTHOR_DATE=OLD_DATE, GIT_COMMITTER_DATE=OLD_DATE)
        try:
            make_template(template, with_node=False)
        finally:
            for key, value in saved.items():
                os.environ.pop(key) if value is None else os.environ.__setitem__(key, value)
        make_node_template(template / "node")
        latest = commit_all(template, "add the Node template", NEW_DATE)

        project = self.parent / "old-lib"
        project.mkdir()
        (project / "package.json").write_text('{"name": "old-lib"}\n', encoding="utf-8")
        git("init", "-q", "-b", "main", cwd=project)
        commit_all(project, "initial", PROJECT_DATE)

        code, out = self.run_script(SCRIPT, "status", "--project", str(project), "--template", str(template))
        self.assertEqual(code, 0, out)
        self.assertEqual(out["language"], "node")
        self.assertIsNone(out["suggested_commit"])
        self.assertEqual(out["questions_at"], latest)
        self.assertIn("node_version", {q["name"] for q in out["questions"]})

    def test_foreign_template_is_refused(self) -> None:
        project = self.linked_project("st-foreign")
        cruft = json.loads((project / ".cruft.json").read_text(encoding="utf-8"))
        cruft["template"] = "https://github.com/someone/other-template"
        (project / ".cruft.json").write_text(json.dumps(cruft), encoding="utf-8")
        commit_all(project, "foreign")
        code, out = self.upgrade("status", project)
        self.assertEqual(code, 3, out)
        self.assertIn("only manages projects linked to cookiecutter-gi", out["messages"][0])

    # --- update -------------------------------------------------------------------

    def test_update_preview_then_apply_the_same_diff(self) -> None:
        project = self.linked_project("up-apply")
        before = self.snapshot(project)
        code, preview = self.upgrade("update", project, "--dry-run")
        self.assertEqual(code, 0, preview)
        self.assertEqual(self.snapshot(project), before, "the preview changed the project")
        self.assertEqual(preview["to_commit"], self.new)
        changes = {f["path"]: f["change"] for f in preview["files"]}
        self.assertEqual(changes, {"README.md": "modified", "CI.md": "added", ".cruft.json": "modified"})
        self.assertEqual(preview["conflicts"], [])
        self.assertIn("+Flavour: vanilla", preview["patch"])

        code, out = self.upgrade("update", project)
        self.assertEqual(code, 2, out)  # applying needs the previewed commit
        code, out = self.upgrade("update", project, "--expect-commit", "0" * 40)
        self.assertEqual((code, out.get("step")), (5, "commit-check"), out)
        self.assertEqual(self.snapshot(project), before)

        code, out = self.upgrade("update", project, "--expect-commit", preview["to_commit"])
        self.assertEqual(code, 0, out)
        self.assertEqual({f["path"]: f["change"] for f in out["files"]}, changes)
        git("add", "-A", cwd=project)
        self.assertEqual(git("diff", "--cached", "--no-color", cwd=project), preview["patch"])
        cruft = json.loads((project / ".cruft.json").read_text(encoding="utf-8"))
        self.assertEqual((cruft["commit"], cruft["checkout"]), (self.new, "main"))
        self.assertEqual(git("rev-parse", "HEAD", cwd=project), before[0], "the update committed something")

        commit_all(project, "upgrade")
        code, out = self.upgrade("update", project, "--dry-run")
        self.assertEqual(code, 0, out)
        self.assertTrue(out["up_to_date"])
        code, out = self.upgrade("status", project)
        self.assertTrue(out["up_to_date"])

    def test_answers_for_new_questions_are_used(self) -> None:
        project = self.linked_project("up-answers")
        code, out = self.upgrade("update", project, "--dry-run", "--answers", self.answers(use_ci=False))
        self.assertEqual(code, 0, out)
        self.assertIn("+CI: False", out["patch"])
        code, out = self.upgrade("update", project, "--dry-run", "--answers", self.answers(use_ci="nope"))
        self.assertEqual(code, 2, out)

    def test_conflicting_local_change_is_reported(self) -> None:
        project = self.linked_project("up-conflict")
        readme = project / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8").replace("Flavor:", "Taste:"), encoding="utf-8")
        commit_all(project, "local edit")
        code, out = self.upgrade("update", project, "--dry-run")
        self.assertEqual(code, 0, out)
        self.assertTrue(out["conflicts"] or out["rejects"], out)

    def test_dirty_or_missing_repository_is_refused(self) -> None:
        project = self.linked_project("up-dirty")
        (project / "README.md").write_text("changed\n", encoding="utf-8")
        for command in ("update", "link"):
            with self.subTest(command=command):
                extra = ("--dry-run",) if command == "update" else ("--dry-run", "--commit", self.old, "--answers", "x")
                code, out = self.upgrade(command, project, *extra)
                self.assertIn(code, (2, 6), out)
        code, out = self.upgrade("update", project, "--dry-run")
        self.assertEqual(code, 6, out)
        self.assertIn("uncommitted changes", out["messages"][0])

        plain = self.parent / "no-git"
        plain.mkdir()
        code, out = self.upgrade("update", plain, "--dry-run")
        self.assertEqual(code, 6, out)

    # --- link ---------------------------------------------------------------------

    def test_link_preview_link_then_update(self) -> None:
        project = self.unlinked_project("ln-proj", flavor="chocolate")
        before = self.snapshot(project)

        wrong = self.answers(project_name="ln-proj", **PERSON)  # flavor left at the default
        code, out = self.upgrade("link", project, "--dry-run", "--commit", self.old[:10], "--answers", wrong)
        self.assertEqual(code, 0, out)
        self.assertEqual(out["match"]["differs"], ["README.md"])

        right = self.answers(project_name="ln-proj", flavor="chocolate", **PERSON)
        code, out = self.upgrade("link", project, "--dry-run", "--commit", self.old, "--answers", right)
        self.assertEqual(code, 0, out)
        self.assertEqual(out["summary"], {"same": 2, "differs": 0, "missing": 0})
        self.assertEqual(self.snapshot(project), before, "the link preview changed the project")

        code, out = self.upgrade("link", project, "--commit", self.old, "--answers", right)
        self.assertEqual(code, 0, out)
        self.assertEqual(git("status", "--porcelain", cwd=project), "?? .cruft.json\n")
        cruft = json.loads((project / ".cruft.json").read_text(encoding="utf-8"))
        self.assertEqual((cruft["commit"], cruft["checkout"]), (self.old, "main"))
        self.assertEqual(cruft["context"]["cookiecutter"]["flavor"], "chocolate")

        code, out = self.upgrade("link", project, "--commit", self.old, "--answers", right)
        self.assertEqual(code, 6, out)  # dirty (and already linked)
        commit_all(project, "link to template")
        code, out = self.upgrade("link", project, "--commit", self.old, "--answers", right)
        self.assertEqual(code, 6, out)
        self.assertIn("already linked", out["messages"][0])

        code, out = self.upgrade("update", project, "--dry-run")
        self.assertEqual(code, 0, out)
        self.assertIn("+Flavour: chocolate", out["patch"])

    def test_link_rejects_invalid_answers_and_commits(self) -> None:
        project = self.unlinked_project("ln-bad")
        cases = [
            (self.answers(project_name="ln-bad", flavor="mint", **PERSON), self.old, 2),
            (self.answers(project_name="ln_bad", **PERSON), self.old, 2),  # the template's hook rejects it
            (self.answers(project_name="ln-bad", **PERSON), "0" * 40, 2),
        ]
        for answers, commit, expected in cases:
            with self.subTest(commit=commit):
                code, out = self.upgrade("link", project, "--dry-run", "--commit", commit, "--answers", answers)
                self.assertEqual(code, expected, out)
        self.assertFalse((project / ".cruft.json").exists())


if __name__ == "__main__":
    unittest.main()
