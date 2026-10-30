"""Tests for plugins/project-kit/scripts/new_project.py against a local fixture template.

Run with: uv run --no-project python -m unittest discover -s tests -v

Needs git and uv on PATH, and network access to public GitHub (cruft from PyPI,
spec-kit from github.com/github/spec-kit). No access to the private
cookiecutter-gi template is needed.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plugins"
    / "project-kit"
    / "scripts"
    / "new_project.py"
)

COOKIECUTTER = {
    "project_name": "example-project",
    "project_slug": "{{ cookiecutter.project_name|lower|replace('-', '_') }}",
    "author": "Your Name",
    "email": "you@example.com",
    "use_docs": True,
    "flavor": ["vanilla", "chocolate"],
    "_private": "ignored",
    "__prompts__": {
        "use_docs": "Include docs?",
        "flavor": {
            "__prompt__": "Flavor",
            "vanilla": "Vanilla (default)",
            "chocolate": "Chocolate",
        },
    },
}

PRE_GEN_HOOK = """\
import sys
name = "{{ cookiecutter.project_name }}"
if "_" in name:
    print(f"ERROR: The project name {name} must not contain underscores")
    sys.exit(1)
"""


def git(*args: str, cwd: Path) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout


def make_template(root: Path) -> Path:
    tpl = root / "template"
    project = tpl / "{{cookiecutter.project_name}}"
    (tpl / "hooks").mkdir(parents=True)
    project.mkdir()
    (tpl / "cookiecutter.json").write_text(
        json.dumps(COOKIECUTTER, indent=2), encoding="utf-8"
    )
    (tpl / "hooks" / "pre_gen_project.py").write_text(PRE_GEN_HOOK, encoding="utf-8")
    (project / "README.md").write_text(
        "# {{ cookiecutter.project_name }}\n\nFlavor: {{ cookiecutter.flavor }}\n",
        encoding="utf-8",
    )
    (project / "{{cookiecutter.project_slug}}.py").write_text(
        "VALUE = 1\n", encoding="utf-8"
    )
    git("init", "-q", "-b", "main", cwd=tpl)
    git("add", "-A", cwd=tpl)
    git(
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.com",
        "commit",
        "-q",
        "-m",
        "init",
        cwd=tpl,
    )
    return tpl


class NewProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory(prefix="pk-tests-")
        cls.root = Path(cls._tmp.name)
        cls.template = make_template(cls.root)
        cls.commit = git("rev-parse", "HEAD", cwd=cls.template).strip()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def setUp(self) -> None:
        self.parent = Path(tempfile.mkdtemp(prefix="dest-", dir=self.root))

    def script(self, *args: str) -> tuple[int, dict]:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "GIT_CONFIG_GLOBAL": os.devnull},
        )
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError:
            self.fail(
                f"no JSON on stdout (exit {proc.returncode}):\n{proc.stdout}\n{proc.stderr}"
            )
        return proc.returncode, payload

    def answers(self, **values: object) -> str:
        path = Path(tempfile.mkstemp(suffix=".json", dir=self.root)[1])
        path.write_text(json.dumps(values), encoding="utf-8")
        return str(path)

    def create(self, answers: str, *extra: str) -> tuple[int, dict]:
        return self.script(
            "create",
            "--template",
            str(self.template),
            "--answers",
            answers,
            "--dest",
            str(self.parent),
            *extra,
        )

    # --- options (US1, FR-002) ----------------------------------------------

    def test_options_reads_template_definition(self) -> None:
        code, out = self.script("options", "--template", str(self.template))
        self.assertEqual(code, 0, out)
        self.assertEqual(out["ref"], "main")
        self.assertEqual(out["commit"], self.commit)
        by_name = {q["name"]: q for q in out["questions"]}
        self.assertEqual(
            set(by_name), {"project_name", "author", "email", "use_docs", "flavor"}
        )
        self.assertEqual(by_name["flavor"]["type"], "choice")
        self.assertEqual(by_name["flavor"]["default"], "vanilla")
        self.assertEqual(by_name["flavor"]["prompt"], "Flavor")
        self.assertEqual(by_name["flavor"]["choice_labels"]["chocolate"], "Chocolate")
        self.assertEqual(
            by_name["use_docs"],
            {
                "name": "use_docs",
                "type": "bool",
                "default": True,
                "prompt": "Include docs?",
            },
        )
        self.assertEqual(by_name["project_name"]["type"], "text")
        self.assertEqual(out["derived"], ["project_slug"])

    def test_check_reports_tools_and_template(self) -> None:
        code, out = self.script("check", "--template", str(self.template))
        self.assertEqual(code, 0, out)
        self.assertIn("git", out["tools"])
        self.assertEqual(out["commit"], self.commit)

    def test_unreachable_template_is_environment_error(self) -> None:
        code, out = self.script(
            "options", "--template", str(self.root / "missing-template")
        )
        self.assertEqual(code, 3, out)
        self.assertEqual(out["status"], "environment")

    # --- create (US1) ---------------------------------------------------------

    def test_create_links_template_sets_up_speckit_and_commits(self) -> None:
        answers = self.answers(
            project_name="demo-proj",
            author="Ada Lovelace",
            email="ada@example.com",
            flavor="chocolate",
            use_docs=False,
        )
        code, out = self.create(answers, "--expect-commit", self.commit)
        self.assertEqual(code, 0, out)
        project = Path(out["project_dir"])
        self.assertEqual(project, self.parent / "demo-proj")

        cruft = json.loads((project / ".cruft.json").read_text(encoding="utf-8"))
        self.assertEqual(cruft["checkout"], "main")
        self.assertEqual(cruft["commit"], self.commit)
        context = cruft["context"]["cookiecutter"]
        self.assertEqual(context["flavor"], "chocolate")
        self.assertIs(context["use_docs"], False)
        self.assertEqual(out["derived"], {"project_slug": "demo_proj"})
        self.assertEqual(
            out["non_default"],
            {
                "project_name": "demo-proj",
                "author": "Ada Lovelace",
                "email": "ada@example.com",
                "flavor": "chocolate",
                "use_docs": False,
            },
        )
        self.assertIn(
            "Flavor: chocolate", (project / "README.md").read_text(encoding="utf-8")
        )

        self.assertTrue((project / ".specify").is_dir())
        self.assertTrue(any((project / ".claude" / "skills").glob("speckit-*")))

        log = git("log", "--format=%an <%ae>|%s", cwd=project).strip().splitlines()
        self.assertEqual(len(log), 1)
        self.assertTrue(
            log[0].startswith(
                "Ada Lovelace <ada@example.com>|Initial commit from cookiecutter-gi"
            )
        )
        self.assertEqual(git("status", "--porcelain", cwd=project).strip(), "")
        self.assertEqual(git("branch", "--show-current", cwd=project).strip(), "main")
        self.assertEqual(
            out["git_commit"], git("rev-parse", "HEAD", cwd=project).strip()
        )
        self.assertEqual(sorted(os.listdir(self.parent)), ["demo-proj"])

    def test_create_into_existing_empty_folder(self) -> None:
        (self.parent / "empty-proj").mkdir()
        code, out = self.create(
            self.answers(project_name="empty-proj", author="A", email="a@example.com")
        )
        self.assertEqual(code, 0, out)
        self.assertTrue((self.parent / "empty-proj" / ".cruft.json").is_file())

    def test_commit_mismatch_stops_before_speckit(self) -> None:
        answers = self.answers(
            project_name="drift-proj", author="A", email="a@example.com"
        )
        code, out = self.create(answers, "--expect-commit", "0" * 40)
        self.assertEqual(code, 5, out)
        self.assertEqual(out["step"], "commit-check")
        project = self.parent / "drift-proj"
        self.assertTrue(project.is_dir(), "folder must be kept, not deleted")
        self.assertFalse((project / ".specify").exists())
        self.assertFalse((project / ".git").exists())

    # --- validation (US2) -----------------------------------------------------

    def test_invalid_answers_are_rejected_without_creating(self) -> None:
        cases = {
            "bad choice": (
                {"project_name": "p-one", "flavor": "mint"},
                "vanilla, chocolate",
            ),
            "non-boolean": (
                {"project_name": "p-two", "use_docs": "no"},
                "true or false",
            ),
            "unknown key": (
                {"project_name": "p-three", "colour": "red"},
                "not a question",
            ),
            "derived key": (
                {"project_name": "p-four", "project_slug": "x"},
                "computed by the template",
            ),
            "missing name": ({"author": "A"}, "project_name is required"),
        }
        for label, (values, expected) in cases.items():
            with self.subTest(label):
                code, out = self.create(self.answers(**values), "--dry-run")
                self.assertEqual(code, 2, out)
                self.assertTrue(
                    any(expected in m for m in out["messages"]), out["messages"]
                )
                code, out = self.create(self.answers(**values))
                self.assertEqual(code, 2, out)
                self.assertEqual(os.listdir(self.parent), [])

    # --- preview and safe failure (US3) ---------------------------------------

    def test_dry_run_previews_and_creates_nothing(self) -> None:
        answers = self.answers(
            project_name="preview-proj", author="A", email="a@example.com"
        )
        code, out = self.create(answers, "--dry-run")
        self.assertEqual(code, 0, out)
        self.assertTrue(out["dry_run"])
        self.assertEqual(out["project_dir"], str(self.parent / "preview-proj"))
        self.assertEqual(out["commit"], self.commit)
        self.assertEqual(out["derived"], {"project_slug": "preview_proj"})
        self.assertIn("README.md", out["files"])
        self.assertIn(".cruft.json", out["files"])
        self.assertTrue(any("specify init" in s for s in out["steps"]))
        self.assertEqual(os.listdir(self.parent), [])

    def test_template_hook_error_is_relayed(self) -> None:
        code, out = self.create(
            self.answers(project_name="bad_name", author="A", email="a@example.com"),
            "--dry-run",
        )
        self.assertEqual(code, 2, out)
        self.assertEqual(
            out["messages"],
            ["ERROR: The project name bad_name must not contain underscores"],
        )
        self.assertEqual(os.listdir(self.parent), [])

    def test_non_empty_destination_is_refused(self) -> None:
        existing = self.parent / "taken"
        existing.mkdir()
        (existing / "keep.txt").write_text("mine\n", encoding="utf-8")
        for extra in ((), ("--dry-run",)):
            with self.subTest(extra=extra):
                code, out = self.create(self.answers(project_name="taken"), *extra)
                self.assertEqual(code, 4, out)
                self.assertEqual(os.listdir(existing), ["keep.txt"])

    def test_missing_parent_is_refused(self) -> None:
        code, out = self.script(
            "create",
            "--template",
            str(self.template),
            "--answers",
            self.answers(project_name="x-proj"),
            "--dest",
            str(self.root / "nope"),
        )
        self.assertEqual(code, 4, out)

    def test_no_author_and_no_git_identity_is_environment_error(self) -> None:
        code, out = self.create(self.answers(project_name="anon-proj"), "--dry-run")
        self.assertEqual(code, 3, out)
        self.assertEqual(os.listdir(self.parent), [])


if __name__ == "__main__":
    unittest.main()
