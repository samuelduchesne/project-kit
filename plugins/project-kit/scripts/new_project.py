#!/usr/bin/env python3
"""Create a new project from the cookiecutter-gi template.

Used by the project-kit ``new-project`` skill. Commands:

    check    verify git, uv and access to the template
    options  print the template's questions, read from its cookiecutter.json
    create   validate answers and create the project (``--dry-run`` to preview)

``--language`` picks the template folder: the repository root for Python, ``node/`` for Node.

Every command prints one JSON object on stdout; progress goes to stderr.
Exit codes: 0 ok, 2 invalid answers, 3 environment, 4 destination, 5 step failed.
The template's own files and checks are the source of truth: this script keeps
no copy of the template's questions or rules.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, NoReturn

DEFAULT_TEMPLATE = "https://github.com/samuelduchesne/cookiecutter-gi"
# Template folder inside the repository for each language ("" is the repository root).
LANGUAGES = {"python": "", "node": "node"}
CRUFT = ["uvx", "--from", "cruft==2.16.0", "--with", "cookiecutter==2.7.1", "cruft"]
SPECKIT_REF = "v1.2.5"
SPECKIT_SOURCE = f"git+https://github.com/github/spec-kit.git@{SPECKIT_REF}"
SPECKIT = [
    "uvx",
    "--from",
    SPECKIT_SOURCE,
    "specify",
    "init",
    "--here",
    "--integration",
    "claude",
    "--script",
    "sh",
    "--non-interactive",
    "--force",
    # The claude CLI may not be on PATH (Cowork, desktop app, CI); spec-kit only needs it for a check.
    "--ignore-agent-tools",
]
COMMAND_TIMEOUT = 600  # seconds
MIN_COMMIT_PREFIX = 7

EXIT_OK = 0
EXIT_INVALID = 2
EXIT_ENVIRONMENT = 3
EXIT_DESTINATION = 4
EXIT_FAILED = 5
EXIT_PROJECT = 6  # upgrade_project.py: the project is not in a state the command accepts

STATUS = {
    EXIT_OK: "ok",
    EXIT_INVALID: "invalid",
    EXIT_ENVIRONMENT: "environment",
    EXIT_DESTINATION: "destination",
    EXIT_FAILED: "failed",
    EXIT_PROJECT: "project",
}

JINJA_MARKERS = ("{{", "{%", "{#")
EXCEPTION_LINE = re.compile(r"\b[A-Za-z_]*(?:Error|Exception): .+")


class Stop(Exception):
    """Ends the command with a contract exit code and messages."""

    def __init__(self, code: int, messages: list[str], **extra: Any) -> None:
        super().__init__("; ".join(messages))
        self.code = code
        self.messages = messages
        self.extra = extra


def log(message: str) -> None:
    print(f"[{Path(sys.argv[0]).stem.replace('_', '-')}] {message}", file=sys.stderr)


def finish(code: int, **payload: Any) -> NoReturn:
    print(json.dumps({"status": STATUS[code], **payload}, indent=2, default=str))
    sys.exit(code)


def child_env() -> dict[str, str]:
    """Environment for child processes: never prompt, and don't let the caller's
    GIT_AUTHOR_*/GIT_COMMITTER_* override the author taken from the answers."""
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_AUTHOR_", "GIT_COMMITTER_"))}
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """Run a command without a terminal, logging it; never raises on failure."""
    log("$ " + shlex.join(cmd))
    try:
        return subprocess.run(
            cmd,
            cwd=cwd,
            env=child_env(),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            check=False,
            timeout=COMMAND_TIMEOUT,
        )
    except FileNotFoundError:
        return subprocess.CompletedProcess(cmd, 127, "", f"{cmd[0]}: command not found")
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(cmd, 124, "", f"{cmd[0]}: timed out after {COMMAND_TIMEOUT}s")


def output_of(proc: subprocess.CompletedProcess[str]) -> str:
    return (proc.stdout or "") + (proc.stderr or "")


def template_arg(template: str) -> str:
    """Local templates are passed as absolute paths; URLs unchanged."""
    path = Path(template).expanduser()
    return str(path.resolve()) if path.exists() else template


def check_option_values(template: str, ref: str | None) -> None:
    """Values that start with '-' would be read as options by git or cruft."""
    for label, value in (("template", template), ("ref", ref)):
        if value is not None and (not value or value.startswith("-")):
            raise Stop(EXIT_INVALID, [f"The {label} {value!r} is not valid."])


def check_tools() -> dict[str, str]:
    missing = []
    tools: dict[str, str] = {}
    for tool, version_cmd, hint in (
        (
            "git",
            ["git", "--version"],
            "Install git with your system package manager (e.g. `brew install git`).",
        ),
        (
            "uvx",
            ["uv", "--version"],
            "Install uv: https://docs.astral.sh/uv/getting-started/installation/",
        ),
    ):
        if shutil.which(tool) is None:
            missing.append(f"{tool} is not installed. {hint}")
        else:
            tools[tool] = run(version_cmd).stdout.strip()
    if missing:
        raise Stop(EXIT_ENVIRONMENT, missing)
    return tools


# --- template access ---------------------------------------------------------


def default_branch(template: str) -> str:
    proc = run(["git", "ls-remote", "--symref", "--", template, "HEAD"])
    if proc.returncode != 0:
        raise Stop(
            EXIT_ENVIRONMENT,
            [
                f"Could not reach the template at {template}.",
                "Check that you have read access to it with your git credentials "
                "(for samuelduchesne/cookiecutter-gi, a GitHub account with access to the private repository) "
                "and that you are online.",
                output_of(proc).strip()[-500:],
            ],
        )
    for line in proc.stdout.splitlines():
        if line.startswith("ref:") and line.endswith("HEAD"):
            return line.split()[1].removeprefix("refs/heads/")
    return "main"


def read_definition(template_dir: Path, directory: str, ref: str) -> dict[str, Any]:
    """Read ``<directory>/cookiecutter.json`` from a template checkout."""
    path = template_dir / directory / "cookiecutter.json"
    if directory and not path.is_file():
        raise Stop(EXIT_ENVIRONMENT, [f"The template has no {directory}/ template at {ref!r}."])
    try:
        definition = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Stop(
            EXIT_ENVIRONMENT,
            [f"The template has no readable {path.relative_to(template_dir)}: {exc}"],
        ) from exc
    if not isinstance(definition, dict):
        raise Stop(EXIT_ENVIRONMENT, ["The template's cookiecutter.json is not a JSON object."])
    return definition


def fetch_definition(template: str, ref: str | None, directory: str = "") -> tuple[str, str, dict[str, Any]]:
    """Return (ref, commit, cookiecutter.json contents) for the template folder ``directory``."""
    check_option_values(template, ref)
    template = template_arg(template)
    ref = ref or default_branch(template)
    with tempfile.TemporaryDirectory(prefix="project-kit-template-") as tmp:
        dest = Path(tmp) / "template"
        proc = run(
            [
                "git",
                "clone",
                "--quiet",
                "--depth",
                "1",
                "--branch",
                ref,
                "--",
                template,
                str(dest),
            ]
        )
        if proc.returncode != 0:
            raise Stop(
                EXIT_ENVIRONMENT,
                [
                    f"Could not download the template {template} at {ref!r}.",
                    output_of(proc).strip()[-500:],
                ],
            )
        commit = run(["git", "rev-parse", "HEAD"], cwd=dest).stdout.strip()
        definition = read_definition(dest, directory, ref)
    return ref, commit, definition


def parse_questions(
    definition: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Turn cookiecutter.json into questions and derived names (see data-model.md)."""
    prompts = definition.get("__prompts__", {}) or {}
    questions: list[dict[str, Any]] = []
    derived: list[str] = []
    for name, value in definition.items():
        if name.startswith("_"):
            continue
        if isinstance(value, str) and "{{" in value:
            derived.append(name)
            continue
        prompt_spec = prompts.get(name)
        prompt = prompt_spec.get("__prompt__", name) if isinstance(prompt_spec, dict) else (prompt_spec or name)
        if isinstance(value, list):
            question: dict[str, Any] = {
                "name": name,
                "type": "choice",
                "default": value[0] if value else None,
                "choices": value,
                "prompt": prompt,
            }
            if isinstance(prompt_spec, dict):
                labels = {str(c): prompt_spec[str(c)] for c in value if str(c) in prompt_spec}
                if labels:
                    question["choice_labels"] = labels
        elif isinstance(value, bool):
            question = {
                "name": name,
                "type": "bool",
                "default": value,
                "prompt": prompt,
            }
        else:
            question = {
                "name": name,
                "type": "text",
                "default": value,
                "prompt": prompt,
            }
        questions.append(question)
    return questions, derived


# --- answers -----------------------------------------------------------------


def project_name_problem(name: Any) -> str | None:
    """The project name becomes a folder name: it must be one plain path component."""
    if not isinstance(name, str) or not name.strip():
        return "project_name is required."
    if (
        name in {".", ".."}
        or name.startswith(("-", "."))
        or "/" in name
        or "\\" in name
        or "\x00" in name
        or Path(name).name != name
    ):
        return f"project_name {name!r} must be a single folder name (no '/', '\\', leading '.' or '-')."
    return None


def validate_answers(
    answers: Any, questions: list[dict[str, Any]], derived: list[str], *, partial: bool = False
) -> dict[str, Any]:
    """Check answers against the template definition; return the non-default ones.

    ``partial`` answers (changes to an existing project) skip the checks for required answers.
    """
    if not isinstance(answers, dict):
        raise Stop(EXIT_INVALID, ["The answers file must contain a JSON object."])
    by_name = {q["name"]: q for q in questions}
    problems: list[str] = []
    name_problem = project_name_problem(answers.get("project_name"))
    if name_problem and not (partial and "project_name" not in answers):
        problems.append(name_problem)
    if not partial and {"author", "email"} <= by_name.keys() and not ({"author", "email"} <= answers.keys()):
        problems.append("Answer both 'author' and 'email' (they are used for the project and its first commit).")
    for key, value in answers.items():
        if key in derived:
            problems.append(f"{key} is computed by the template and cannot be set.")
            continue
        question = by_name.get(key)
        if question is None:
            problems.append(f"{key} is not a question in this template.")
        elif question["type"] == "choice" and value not in question["choices"]:
            allowed = ", ".join(map(str, question["choices"]))
            problems.append(f"{key}={value!r} is not allowed. Choose one of: {allowed}.")
        elif question["type"] == "bool" and not isinstance(value, bool):
            problems.append(f"{key} must be true or false, got {value!r}.")
        elif question["type"] == "text":
            if not isinstance(value, str) or not value.strip():
                problems.append(f"{key} must be a non-empty string.")
            elif any(marker in value for marker in JINJA_MARKERS):
                problems.append(f"{key} must not contain template syntax ({', '.join(JINJA_MARKERS)}).")
    if problems:
        raise Stop(EXIT_INVALID, problems)
    return {k: v for k, v in answers.items() if by_name[k]["default"] != v}


def git_identity(answers: dict[str, Any], questions: list[dict[str, Any]]) -> tuple[str, str]:
    """Commit author: the template's ``author``/``email`` answers, else git config."""
    names = {q["name"] for q in questions}
    if {"author", "email"} <= names:
        return answers["author"], answers["email"]
    name = run(["git", "config", "user.name"]).stdout.strip()
    email = run(["git", "config", "user.email"]).stdout.strip()
    if not name or not email:
        raise Stop(
            EXIT_ENVIRONMENT,
            ["No author for the initial commit: set git config user.name and user.email."],
        )
    return name, email


def commit_matches(expected: str, actual: str) -> bool:
    return len(expected) >= MIN_COMMIT_PREFIX and actual.lower().startswith(expected.lower())


def cruft_failure(proc: subprocess.CompletedProcess[str]) -> Stop:
    """Classify a failed cruft run: the template rejected the answers, or the tools failed."""
    text = output_of(proc)
    lines = [ln.strip() for ln in text.splitlines()]
    hook_errors = [ln for ln in lines if ln.startswith("ERROR:")]
    if hook_errors:
        return Stop(EXIT_INVALID, hook_errors)
    if proc.returncode in (124, 127) or any(ln.startswith("error:") for ln in lines):  # uv's own errors
        return Stop(EXIT_ENVIRONMENT, ["Could not run cruft with uvx.", text.strip()[-500:]])
    exceptions = EXCEPTION_LINE.findall(text)
    message = exceptions[-1] if exceptions else "The template could not be generated."
    return Stop(EXIT_FAILED, [message], step="cruft", created=False)


# --- generation --------------------------------------------------------------


def directory_args(directory: str) -> list[str]:
    return ["--directory", directory] if directory else []


def cookiecutter_config(work: Path) -> Path:
    """Keep cookiecutter's clone cache and replay files out of the user's home folder."""
    config = work / "cookiecutter.yaml"
    config.write_text(
        f"cookiecutters_dir: {json.dumps(str(work / 'cookiecutters'))}\n"
        f"replay_dir: {json.dumps(str(work / 'replay'))}\n",
        encoding="utf-8",
    )
    return config


def cruft_create(
    template: str, ref: str, output_dir: Path, answers_file: Path, config: Path, directory: str = ""
) -> Stop | None:
    proc = run(
        [
            *CRUFT,
            "create",
            template_arg(template),
            *directory_args(directory),
            "--no-input",
            "--checkout",
            ref,
            "--output-dir",
            str(output_dir),
            "--extra-context-file",
            str(answers_file),
            "--config-file",
            str(config),
        ]
    )
    return None if proc.returncode == 0 else cruft_failure(proc)


def rendered_project(output_dir: Path, project_name: str) -> Path:
    entries = sorted(os.listdir(output_dir))
    if entries != [project_name]:
        raise Stop(
            EXIT_FAILED,
            [f"The template produced {entries!r} instead of a single folder named {project_name!r}."],
            step="cruft",
            created=False,
        )
    return output_dir / project_name


def read_cruft(project: Path) -> dict[str, Any]:
    try:
        cruft = json.loads((project / ".cruft.json").read_text(encoding="utf-8"))
        cruft["commit"]
        cruft["context"]["cookiecutter"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise Stop(
            EXIT_FAILED,
            [f"The generated project has no usable .cruft.json: {exc}"],
            step="cruft",
            created=False,
        ) from exc
    return cruft


def planned_steps(template: str, ref: str, author: str, email: str, directory: str = "") -> list[str]:
    cruft = [*CRUFT, "create", template_arg(template), *directory_args(directory), "--no-input", "--checkout", ref]
    commit = ["git", "-c", f"user.name={author}", "-c", f"user.email={email}", "-c", "commit.gpgsign=false"]
    return [
        shlex.join([*cruft, "--output-dir", "<parent>", "--extra-context-file", "<answers>"]),
        shlex.join(SPECKIT),
        "git init -b main",
        "git add -A",
        shlex.join([*commit, "commit", "--no-verify", "-m", "Initial commit from cookiecutter-gi <commit>"]),
    ]


def describe(project: Path, cruft: dict[str, Any], derived: list[str]) -> dict[str, Any]:
    context = {k: v for k, v in cruft["context"]["cookiecutter"].items() if not k.startswith("_")}
    return {
        "commit": cruft["commit"],
        "answers": context,
        "derived": {k: context[k] for k in derived if k in context},
        "files": sorted(os.listdir(project)),
    }


def language_info(args: argparse.Namespace) -> dict[str, str]:
    return {"language": args.language, "directory": LANGUAGES[args.language]}


def cmd_check(args: argparse.Namespace) -> None:
    tools = check_tools()
    ref, commit, _ = fetch_definition(args.template, args.ref, LANGUAGES[args.language])
    finish(EXIT_OK, template=args.template, ref=ref, commit=commit, tools=tools, **language_info(args))


def cmd_options(args: argparse.Namespace) -> None:
    ref, commit, definition = fetch_definition(args.template, args.ref, LANGUAGES[args.language])
    questions, derived = parse_questions(definition)
    finish(
        EXIT_OK,
        template=args.template,
        ref=ref,
        commit=commit,
        questions=questions,
        derived=derived,
        **language_info(args),
    )


def cmd_create(args: argparse.Namespace) -> None:
    try:
        answers = json.loads(Path(args.answers).read_text(encoding="utf-8"))
    except (
        OSError,
        ValueError,
    ) as exc:  # ValueError covers JSON and UTF-8 decoding errors
        raise Stop(EXIT_INVALID, [f"Could not read the answers file {args.answers}: {exc}"]) from exc

    check_tools()
    directory = LANGUAGES[args.language]
    ref, commit, definition = fetch_definition(args.template, args.ref, directory)
    questions, derived = parse_questions(definition)
    non_default = validate_answers(answers, questions, derived)
    if args.expect_commit and not commit_matches(args.expect_commit, commit):
        raise Stop(
            EXIT_FAILED,
            [
                f"The template changed since the preview: previewed {args.expect_commit}, now {commit}. "
                "Nothing was created; preview again."
            ],
            step="commit-check",
            created=False,
        )

    parent = Path(args.dest).expanduser().resolve()
    if not parent.is_dir():
        raise Stop(EXIT_DESTINATION, [f"The parent folder {parent} does not exist."])
    name = answers["project_name"]
    target = parent / name
    if target.is_symlink() or (target.exists() and (not target.is_dir() or any(target.iterdir()))):
        raise Stop(
            EXIT_DESTINATION,
            [f"{target} already exists and is not an empty folder. Choose another project name or parent folder."],
        )

    author, email = git_identity(answers, questions)
    steps = planned_steps(args.template, ref, author, email, directory)

    with tempfile.TemporaryDirectory(prefix="project-kit-") as tmp:
        work = Path(tmp)
        answers_file = work / "answers.json"
        answers_file.write_text(json.dumps(answers), encoding="utf-8")
        config = cookiecutter_config(work)

        if args.dry_run:
            render = work / "render"
            render.mkdir()
            failure = cruft_create(args.template, ref, render, answers_file, config, directory)
            if failure:
                raise failure
            project = rendered_project(render, name)
            info = describe(project, read_cruft(project), derived)
            finish(
                EXIT_OK,
                dry_run=True,
                project_dir=str(target),
                template=args.template,
                ref=ref,
                non_default=non_default,
                steps=steps,
                **language_info(args),
                **info,
            )

        # Render into a staging folder inside the parent, then move the finished folder into
        # place in one rename: nothing appears at the target unless generation succeeded.
        stage = Path(tempfile.mkdtemp(prefix=".project-kit-", dir=parent))
        try:
            failure = cruft_create(args.template, ref, stage, answers_file, config, directory)
            if failure:
                raise failure
            staged = rendered_project(stage, name)
            cruft = read_cruft(staged)
            if not commit_matches(commit, cruft["commit"]):
                raise Stop(
                    EXIT_FAILED,
                    [f"The template changed while creating: expected {commit}, got {cruft['commit']}. Nothing created"],
                    step="commit-check",
                    created=False,
                )
            try:
                os.rename(staged, target)  # fails if the target appeared or is not empty
            except OSError as exc:
                raise Stop(EXIT_DESTINATION, [f"Could not create {target}: {exc}"]) from exc
        finally:
            shutil.rmtree(stage, ignore_errors=True)  # our own staging folder only

    project = target
    speckit = run(SPECKIT, cwd=project)
    if speckit.returncode != 0:
        raise Stop(
            EXIT_FAILED,
            [
                "spec-kit setup failed; the project folder was kept.",
                output_of(speckit).strip()[-800:],
            ],
            step="speckit",
            created=True,
            project_dir=str(project),
        )

    for git_cmd in (
        ["git", "init", "-b", "main"],
        ["git", "add", "-A"],
        # The scaffold commit: author from the answers, no user hooks, no signing.
        [
            "git",
            "-c",
            f"user.name={author}",
            "-c",
            f"user.email={email}",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "--quiet",
            "--no-verify",
            "-m",
            f"Initial commit from cookiecutter-gi {cruft['commit'][:12]}",
        ],
    ):
        proc = run(git_cmd, cwd=project)
        if proc.returncode != 0:
            raise Stop(
                EXIT_FAILED,
                [
                    f"`{' '.join(git_cmd[:2])}` failed; the project folder was kept.",
                    output_of(proc).strip()[-500:],
                ],
                step="git",
                created=True,
                project_dir=str(project),
            )

    git_commit = run(["git", "rev-parse", "HEAD"], cwd=project).stdout.strip()
    finish(
        EXIT_OK,
        dry_run=False,
        project_dir=str(project),
        template=args.template,
        ref=ref,
        non_default=non_default,
        git_commit=git_commit,
        **language_info(args),
        **describe(project, cruft, derived),
    )


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--template", default=DEFAULT_TEMPLATE, help="template git URL or local path")
    common.add_argument(
        "--ref",
        default=None,
        help="branch or tag (default: the template's default branch)",
    )
    common.add_argument(
        "--language",
        choices=sorted(LANGUAGES),
        default="python",
        help="template to use: python (repository root) or node (node/ folder)",
    )

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", parents=[common], help="verify tools and template access").set_defaults(func=cmd_check)
    sub.add_parser("options", parents=[common], help="print the template's questions").set_defaults(func=cmd_options)
    create = sub.add_parser("create", parents=[common], help="create the project")
    create.add_argument("--answers", required=True, help="JSON file mapping question names to answers")
    create.add_argument(
        "--dest",
        default=".",
        help="parent folder for the new project (default: current folder)",
    )
    create.add_argument(
        "--expect-commit",
        default=None,
        help="full template commit from the preview; stop if it changed",
    )
    create.add_argument(
        "--dry-run",
        action="store_true",
        help="preview in a temporary folder; change nothing",
    )
    create.set_defaults(func=cmd_create)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except Stop as stop:
        finish(stop.code, messages=[m for m in stop.messages if m], **stop.extra)
    except Exception as exc:  # the contract promises JSON on stdout, even for bugs
        finish(
            EXIT_FAILED,
            messages=[f"Unexpected error: {type(exc).__name__}: {exc}"],
            step="internal",
        )


if __name__ == "__main__":
    main()
