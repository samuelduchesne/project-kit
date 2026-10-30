"""Tests for plugins/project-kit/scripts/new_project.py against local fixture templates.

Run with: uv run --no-project python -m unittest discover -s tests -v

Needs git and uv on PATH, and network access to public GitHub and PyPI (cruft
from PyPI, spec-kit from github.com/github/spec-kit). No access to the private
cookiecutter-gi template is needed.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "plugins" / "project-kit" / "scripts" / "new_project.py"

PRE_GEN_HOOK = """\
import sys
name = "{{ cookiecutter.project_name }}"
if "_" in name:
    print(f"ERROR: The project name {name} must not contain underscores")
    sys.exit(1)
"""

POST_GEN_HOOK = """\
import sys
if "{{ cookiecutter.project_name }}" == "post-fail":
    print("post-generation hook failed on purpose")
    sys.exit(1)
"""


def git(*args: str, cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


def make_template(
    path: Path,
    *,
    root_folder: str = "{{cookiecutter.project_name}}",
    with_author: bool = True,
) -> Path:
    definition: dict = {"project_name": "example-project"}
    definition["project_slug"] = "{{ cookiecutter.project_name|lower|replace('-', '_') }}"
    if with_author:
        definition.update({"author": "Your Name", "email": "you@example.com"})
    definition.update(
        {
            "use_docs": True,
            "flavor": ["vanilla", "chocolate"],
            "description": "A project",
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
    )
    project = path / root_folder
    (path / "hooks").mkdir(parents=True)
    project.mkdir()
    (path / "cookiecutter.json").write_text(json.dumps(definition, indent=2), encoding="utf-8")
    (path / "hooks" / "pre_gen_project.py").write_text(PRE_GEN_HOOK, encoding="utf-8")
    (path / "hooks" / "post_gen_project.py").write_text(POST_GEN_HOOK, encoding="utf-8")
    (project / "README.md").write_text(
        "# {{ cookiecutter.project_name }}\n\nFlavor: {{ cookiecutter.flavor }}\n",
        encoding="utf-8",
    )
    (project / "{{cookiecutter.project_slug}}.py").write_text("VALUE = 1\n", encoding="utf-8")
    git("init", "-q", "-b", "main", cwd=path)
    git("add", "-A", cwd=path)
    git(
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.com",
        "commit",
        "-q",
        "-m",
        "init",
        cwd=path,
    )
    return path


class NewProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory(prefix="pk-tests-")
        cls.root = Path(cls._tmp.name)
        cls.template = make_template(cls.root / "template")
        cls.commit = git("rev-parse", "HEAD", cwd=cls.template).strip()
        # A user git config that would break a naive scaffold commit: signing and a failing hook.
        hooks = cls.root / "git-template" / "hooks"
        hooks.mkdir(parents=True)
        (hooks / "pre-commit").write_text("#!/bin/sh\necho 'user hook ran' >&2\nexit 1\n", encoding="utf-8")
        (hooks / "pre-commit").chmod(0o755)
        cls.hostile_gitconfig = cls.root / "hostile.gitconfig"
        cls.hostile_gitconfig.write_text(
            f"[commit]\n\tgpgsign = true\n[init]\n\ttemplateDir = {cls.root / 'git-template'}\n",
            encoding="utf-8",
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def setUp(self) -> None:
        self.parent = Path(tempfile.mkdtemp(prefix="dest-", dir=self.root))

    def script(self, *args: str, env: dict[str, str] | None = None) -> tuple[int, dict]:
        base = {
            k: v
            for k, v in os.environ.items()
            if not k.startswith(("GIT_AUTHOR_", "GIT_COMMITTER_", "GIT_CONFIG_")) and k != "EMAIL"
        }
        base.update({"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"})
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
            check=False,
            env={**base, **(env or {})},
        )
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError:
            self.fail(f"no JSON on stdout (exit {proc.returncode}):\n{proc.stdout}\n{proc.stderr}")
        return proc.returncode, payload

    def answers(self, **values: object) -> str:
        path = Path(tempfile.mkstemp(suffix=".json", dir=self.root)[1])
        path.write_text(json.dumps(values), encoding="utf-8")
        return str(path)

    def person(self, **values: object) -> str:
        return self.answers(**{"author": "Ada Lovelace", "email": "ada@example.com", **values})

    def create(
        self,
        answers: str,
        *extra: str,
        template: Path | None = None,
        env: dict[str, str] | None = None,
    ) -> tuple[int, dict]:
        return self.script(
            "create",
            "--template",
            str(template or self.template),
            "--answers",
            answers,
            "--dest",
            str(self.parent),
            *extra,
            env=env,
        )

    def assert_root_unchanged(self, before: set[str]) -> None:
        added = set(os.listdir(self.root)) - before
        self.assertFalse(
            {n for n in added if not n.endswith(".json")},
            "files appeared outside the parent folder",
        )

    # --- options (US1, FR-002) ----------------------------------------------

    def test_options_reads_template_definition(self) -> None:
        code, out = self.script("options", "--template", str(self.template))
        self.assertEqual(code, 0, out)
        self.assertEqual(out["ref"], "main")
        self.assertEqual(out["commit"], self.commit)
        by_name = {q["name"]: q for q in out["questions"]}
        self.assertEqual(
            set(by_name),
            {"project_name", "author", "email", "use_docs", "flavor", "description"},
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
        code, out = self.script("options", "--template", str(self.root / "missing-template"))
        self.assertEqual(code, 3, out)
        self.assertEqual(out["status"], "environment")

    def test_option_like_template_or_ref_is_rejected(self) -> None:
        marker = self.root / "pwned"
        for args in (
            ("options", f"--template=--upload-pack=touch {marker};"),
            ("options", "--template", str(self.template), "--ref=--upload-pack=x"),
        ):
            with self.subTest(args=args):
                code, out = self.script(*args)
                self.assertEqual(code, 2, out)
                self.assertFalse(marker.exists())

    def test_missing_uvx_is_environment_error(self) -> None:
        bin_dir = self.root / "only-git"
        bin_dir.mkdir(exist_ok=True)
        if not (bin_dir / "git").exists():
            (bin_dir / "git").symlink_to(shutil.which("git"))
        code, out = self.create(self.person(project_name="no-uv"), "--dry-run", env={"PATH": str(bin_dir)})
        self.assertEqual(code, 3, out)
        self.assertTrue(any("uvx is not installed" in m for m in out["messages"]), out)

    # --- create (US1) ---------------------------------------------------------

    def test_create_links_template_sets_up_speckit_and_commits(self) -> None:
        answers = self.person(project_name="demo-proj", flavor="chocolate", use_docs=False)
        # A hostile user setup must not change the scaffold commit's author or make it fail.
        env = {
            "GIT_CONFIG_GLOBAL": str(self.hostile_gitconfig),
            "GIT_AUTHOR_NAME": "Env Author",
        }
        code, out = self.create(answers, "--expect-commit", self.commit[:12], env=env)
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
        self.assertIn("Flavor: chocolate", (project / "README.md").read_text(encoding="utf-8"))

        self.assertTrue((project / ".specify").is_dir())
        self.assertTrue(any((project / ".claude" / "skills").glob("speckit-*")))

        log = git("log", "--format=%an <%ae>|%cn <%ce>|%s", cwd=project).strip().splitlines()
        self.assertEqual(len(log), 1)
        author, committer, subject = log[0].split("|")
        self.assertEqual(author, "Ada Lovelace <ada@example.com>")
        self.assertEqual(committer, "Ada Lovelace <ada@example.com>")
        self.assertTrue(subject.startswith("Initial commit from cookiecutter-gi"))
        self.assertEqual(git("status", "--porcelain", cwd=project).strip(), "")
        self.assertEqual(git("branch", "--show-current", cwd=project).strip(), "main")
        self.assertEqual(out["git_commit"], git("rev-parse", "HEAD", cwd=project).strip())
        self.assertEqual(
            sorted(os.listdir(self.parent)),
            ["demo-proj"],
            "no staging folder left behind",
        )

    def test_create_into_existing_empty_folder(self) -> None:
        (self.parent / "empty-proj").mkdir()
        code, out = self.create(self.person(project_name="empty-proj"))
        self.assertEqual(code, 0, out)
        self.assertTrue((self.parent / "empty-proj" / ".cruft.json").is_file())
        self.assertEqual(sorted(os.listdir(self.parent)), ["empty-proj"])

    def test_commit_mismatch_stops_before_creating_anything(self) -> None:
        for expected in ("0" * 40, "abc"):  # wrong commit; too short to compare
            with self.subTest(expected=expected):
                code, out = self.create(self.person(project_name="drift-proj"), "--expect-commit", expected)
                self.assertEqual(code, 5, out)
                self.assertEqual(out["step"], "commit-check")
                self.assertIs(out["created"], False)
                self.assertEqual(os.listdir(self.parent), [])

    def test_failed_generation_leaves_existing_empty_folder_empty(self) -> None:
        target = self.parent / "post-fail"
        target.mkdir()
        code, out = self.create(self.person(project_name="post-fail"))
        self.assertEqual(code, 5, out)
        self.assertEqual(out["step"], "cruft")
        self.assertIs(out["created"], False)
        self.assertEqual(os.listdir(target), [])
        self.assertEqual(os.listdir(self.parent), ["post-fail"], "no staging folder left behind")

    def test_template_folder_named_differently_is_refused_without_touching_user_files(
        self,
    ) -> None:
        slug_template = make_template(
            self.root / f"slug-template-{self.parent.name}",
            root_folder="{{cookiecutter.project_slug}}",
        )
        (self.parent / "demo-x").mkdir()
        mine = self.parent / "demo_x"
        mine.mkdir()
        (mine / "README.md").write_text("MY NOTES\n", encoding="utf-8")
        for extra in ((), ("--dry-run",)):
            with self.subTest(extra=extra):
                code, out = self.create(self.person(project_name="demo-x"), *extra, template=slug_template)
                self.assertEqual(code, 5, out)
                self.assertEqual(out["step"], "cruft")
                self.assertEqual((mine / "README.md").read_text(encoding="utf-8"), "MY NOTES\n")
                self.assertEqual(sorted(os.listdir(mine)), ["README.md"])
                self.assertEqual(os.listdir(self.parent / "demo-x"), [])
                self.assertEqual(sorted(os.listdir(self.parent)), ["demo-x", "demo_x"])

    def test_git_config_identity_is_used_when_template_has_no_author(self) -> None:
        plain = make_template(self.root / f"plain-template-{self.parent.name}", with_author=False)
        env = {
            "GIT_CONFIG_COUNT": "2",
            "GIT_CONFIG_KEY_0": "user.name",
            "GIT_CONFIG_VALUE_0": "Grace Hopper",
            "GIT_CONFIG_KEY_1": "user.email",
            "GIT_CONFIG_VALUE_1": "grace@example.com",
        }
        code, out = self.create(self.answers(project_name="plain-proj"), template=plain, env=env)
        self.assertEqual(code, 0, out)
        log = git("log", "--format=%an <%ae>", cwd=self.parent / "plain-proj").strip()
        self.assertEqual(log, "Grace Hopper <grace@example.com>")

        code, out = self.create(self.answers(project_name="anon-proj"), "--dry-run", template=plain)
        self.assertEqual(code, 3, out)

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
            "missing name": ({}, "project_name is required"),
            "non-string name": ({"project_name": 123}, "project_name is required"),
            "jinja": (
                {"project_name": "p-five", "description": "Uses {{ name }}"},
                "template syntax",
            ),
        }
        for label, (values, expected) in cases.items():
            with self.subTest(label):
                for extra in (("--dry-run",), ()):
                    code, out = self.create(self.person(**values), *extra)
                    self.assertEqual(code, 2, out)
                    self.assertTrue(any(expected in m for m in out["messages"]), out["messages"])
                    self.assertEqual(os.listdir(self.parent), [])

    def test_author_and_email_are_both_required(self) -> None:
        code, out = self.create(self.answers(project_name="half", author="Ada"), "--dry-run")
        self.assertEqual(code, 2, out)
        self.assertTrue(any("'author' and 'email'" in m for m in out["messages"]), out)

    def test_project_name_must_be_a_single_folder_name(self) -> None:
        before = set(os.listdir(self.root))
        for name in (
            "../escaped",
            "sub/proj",
            "..",
            ".",
            ".hidden",
            "-flag",
            "a\\b",
            "a\x00b",
            "/abs/path",
        ):
            with self.subTest(name=name):
                for extra in (("--dry-run",), ()):
                    code, out = self.create(self.person(project_name=name), *extra)
                    self.assertEqual(code, 2, out)
                    self.assertEqual(os.listdir(self.parent), [])
        self.assert_root_unchanged(before)

    def test_template_syntax_in_answers_is_not_executed(self) -> None:
        marker = self.root / "ssti"
        payload = f"A {{{{ cycler.__init__.__globals__.os.popen('touch {marker}') }}}}"
        code, out = self.create(
            self.answers(project_name="ssti-proj", author=payload, email="a@b.c"),
            "--dry-run",
        )
        self.assertEqual(code, 2, out)
        self.assertFalse(marker.exists())

    def test_unreadable_answers_file_returns_json(self) -> None:
        path = self.root / "binary.json"
        path.write_bytes(b"\xff\xfe{}")
        code, out = self.create(str(path), "--dry-run")
        self.assertEqual(code, 2, out)

    # --- preview and safe failure (US3) ---------------------------------------

    def test_dry_run_previews_and_creates_nothing(self) -> None:
        before = set(os.listdir(self.root))
        code, out = self.create(self.person(project_name="preview-proj"), "--dry-run")
        self.assertEqual(code, 0, out)
        self.assertTrue(out["dry_run"])
        self.assertEqual(out["project_dir"], str(self.parent / "preview-proj"))
        self.assertEqual(out["commit"], self.commit)
        self.assertEqual(out["derived"], {"project_slug": "preview_proj"})
        self.assertIn("README.md", out["files"])
        self.assertIn(".cruft.json", out["files"])
        self.assertTrue(any("specify init" in s for s in out["steps"]))
        self.assertEqual(os.listdir(self.parent), [])
        self.assert_root_unchanged(before)

    def test_template_hook_error_is_relayed(self) -> None:
        code, out = self.create(self.person(project_name="bad_name"), "--dry-run")
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
        elsewhere = self.root / f"elsewhere-{self.parent.name}"
        elsewhere.mkdir()
        (self.parent / "linked").symlink_to(elsewhere, target_is_directory=True)
        for name in ("taken", "linked"):
            for extra in ((), ("--dry-run",)):
                with self.subTest(name=name, extra=extra):
                    code, out = self.create(self.person(project_name=name), *extra)
                    self.assertEqual(code, 4, out)
        self.assertEqual(os.listdir(existing), ["keep.txt"])
        self.assertEqual(os.listdir(elsewhere), [])

    def test_missing_parent_is_refused(self) -> None:
        code, out = self.script(
            "create",
            "--template",
            str(self.template),
            "--answers",
            self.person(project_name="x-proj"),
            "--dest",
            str(self.root / "nope"),
        )
        self.assertEqual(code, 4, out)


if __name__ == "__main__":
    unittest.main()
