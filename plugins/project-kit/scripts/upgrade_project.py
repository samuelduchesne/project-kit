#!/usr/bin/env python3
"""Bring an existing project up to the latest cookiecutter-gi template with cruft.

Used by the project-kit ``upgrade-project`` skill. Commands:

    status   report the project's git state, language, template link and how far behind it is
    link     link an unlinked project to the template at a chosen commit (``--dry-run`` to compare first)
    update   apply the template changes since the linked commit (``--dry-run`` to preview the exact diff)

Every command prints one JSON object on stdout; progress goes to stderr.
Exit codes: 0 ok, 2 invalid answers, 3 environment, 5 step failed, 6 project state.
``status`` and every ``--dry-run`` leave the project unchanged; nothing is ever committed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from new_project import (
    CRUFT,
    DEFAULT_TEMPLATE,
    EXIT_ENVIRONMENT,
    EXIT_FAILED,
    EXIT_INVALID,
    EXIT_OK,
    EXIT_PROJECT,
    LANGUAGES,
    Stop,
    check_option_values,
    check_tools,
    commit_matches,
    cookiecutter_config,
    cruft_create,
    default_branch,
    directory_args,
    finish,
    output_of,
    parse_questions,
    rendered_project,
    run,
    template_arg,
    validate_answers,
)

CRUFT_FILE = ".cruft.json"
SHA = re.compile(r"^[0-9a-f]{40}$")


# --- the project ---------------------------------------------------------------


def git_out(*args: str, cwd: Path) -> str:
    proc = run(["git", *args], cwd=cwd)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def project_dir(path: str) -> Path:
    project = Path(path).expanduser().resolve()
    if not project.is_dir():
        raise Stop(EXIT_PROJECT, [f"{project} is not a folder."])
    return project


def git_state(project: Path) -> dict[str, Any]:
    top = git_out("rev-parse", "--show-toplevel", cwd=project)
    if not top or Path(top).resolve() != project:
        return {"repository": False, "clean": False, "first_commit_date": None}
    clean = run(["git", "status", "--porcelain"], cwd=project).stdout.strip() == ""
    roots = git_out("rev-list", "--max-parents=0", "HEAD", cwd=project).split()
    # Compare Unix timestamps: ISO dates with different UTC offsets don't sort chronologically as strings.
    dates = []
    for root in roots:
        stamp, _, iso = git_out("log", "-1", "--format=%ct %cI", root, cwd=project).partition(" ")
        if stamp.isdigit():
            dates.append((int(stamp), iso))
    return {"repository": True, "clean": clean, "first_commit_date": min(dates)[1] if dates else None}


def require_clean_repo(state: dict[str, Any], project: Path) -> None:
    if not state["repository"]:
        raise Stop(
            EXIT_PROJECT,
            [f"{project} is not the root of a git repository. Upgrades need git history to show and revert changes."],
        )
    if not state["clean"]:
        raise Stop(
            EXIT_PROJECT,
            ["The project has uncommitted changes. Commit or stash them first, so every change can be reviewed."],
        )


def read_link(project: Path) -> dict[str, Any] | None:
    path = project / CRUFT_FILE
    if not path.exists():
        return None
    try:
        cruft = json.loads(path.read_text(encoding="utf-8"))
        cruft["template"], cruft["commit"], cruft["context"]["cookiecutter"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise Stop(EXIT_PROJECT, [f"{CRUFT_FILE} is not a usable cruft link record: {exc}"]) from exc
    return cruft


def link_summary(cruft: dict[str, Any]) -> dict[str, Any]:
    return {k: cruft.get(k) for k in ("template", "commit", "checkout", "directory")}


def detect_language(project: Path, cruft: dict[str, Any] | None) -> str | None:
    if cruft is not None:
        return "node" if cruft.get("directory") == LANGUAGES["node"] else "python"
    if (project / "pyproject.toml").is_file():
        return "python"
    if (project / "package.json").is_file():
        return "node"
    return None


def write_checkout(project: Path, ref: str) -> None:
    """Record the branch to follow: cruft stores whatever ``--checkout`` it got, and a SHA pins the project."""
    path = project / CRUFT_FILE
    cruft = json.loads(path.read_text(encoding="utf-8"))
    cruft["checkout"] = ref
    path.write_text(json.dumps(cruft, ensure_ascii=False, indent=2, separators=(",", ": ")) + "\n", encoding="utf-8")


# --- the template --------------------------------------------------------------


def normalize_url(url: str) -> str:
    url = url.strip().lower().rstrip("/")
    url = re.sub(r"^(https?|ssh|git)://", "", url)
    url = re.sub(r"^git@([^:]+):", r"\1/", url)
    url = re.sub(r"^[^@/]+@", "", url)
    return url.removesuffix(".git")


def same_template(a: str, b: str) -> bool:
    paths = [Path(x).expanduser() for x in (a, b)]
    if all(p.exists() for p in paths):
        return paths[0].resolve() == paths[1].resolve()
    return normalize_url(a) == normalize_url(b)


def choose_template(args: argparse.Namespace, cruft: dict[str, Any] | None) -> str:
    """The template to use: the one the project is linked to, which must be cookiecutter-gi or ``--template``."""
    if cruft is None:
        return args.template or DEFAULT_TEMPLATE
    recorded = cruft["template"]
    expected = args.template or DEFAULT_TEMPLATE
    if not same_template(recorded, expected):
        raise Stop(
            EXIT_ENVIRONMENT,
            [
                f"The project is linked to {recorded}, not {expected}. "
                "This workflow only manages projects linked to cookiecutter-gi."
            ],
        )
    return recorded


def choose_ref(args: argparse.Namespace, cruft: dict[str, Any] | None, template: str) -> str:
    if args.ref:
        return args.ref
    checkout = (cruft or {}).get("checkout")
    if checkout and not SHA.match(checkout):
        return checkout
    return default_branch(template_arg(template))


@contextmanager
def template_clone(template: str, ref: str) -> Iterator[tuple[Path, str]]:
    """A full clone of the template at ``ref`` (history needed for commits behind and older definitions)."""
    check_option_values(template, ref)
    with tempfile.TemporaryDirectory(prefix="project-kit-template-") as tmp:
        dest = Path(tmp) / "template"
        proc = run(
            ["git", "clone", "--quiet", "--no-checkout", "--branch", ref, "--", template_arg(template), str(dest)]
        )
        if proc.returncode != 0:
            raise Stop(
                EXIT_ENVIRONMENT,
                [
                    f"Could not download the template {template} at {ref!r}. Check your access to it and that you are "
                    "online.",
                    output_of(proc).strip()[-500:],
                ],
            )
        yield dest, git_out("rev-parse", "HEAD", cwd=dest)


def resolve_commit(clone: Path, commit: str) -> str:
    sha = git_out("rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}", cwd=clone) if commit else ""
    if not sha or commit.startswith("-"):
        raise Stop(EXIT_INVALID, [f"{commit!r} is not a commit of the template."])
    return sha


def definition_path(directory: str) -> str:
    return f"{directory}/cookiecutter.json" if directory else "cookiecutter.json"


def definition_at(clone: Path, commit: str, directory: str) -> dict[str, Any]:
    path = definition_path(directory)
    proc = run(["git", "show", f"{commit}:{path}"], cwd=clone)
    if proc.returncode != 0:
        raise Stop(EXIT_ENVIRONMENT, [f"The template has no {path} at {commit[:12]}."])
    try:
        definition = json.loads(proc.stdout)
    except ValueError as exc:
        raise Stop(EXIT_ENVIRONMENT, [f"The template's {path} at {commit[:12]} is not valid JSON: {exc}"]) from exc
    if not isinstance(definition, dict):
        raise Stop(EXIT_ENVIRONMENT, [f"The template's {path} is not a JSON object."])
    return definition


def template_pathspec(clone: Path, directory: str) -> list[str]:
    """Paths that make up one template, so commits elsewhere (docs, CI, tests, other templates) don't count.

    A sub-folder template is its whole folder. The root template is everything cookiecutter reads: its question
    file, hooks, the ``templates`` folder for Jinja includes, the extension modules named in ``_extensions`` (a
    module file or a package folder) and the folder it renders (the top-level entry whose name holds ``{{``).
    """
    if directory:
        return [directory]
    rendered = [name for name in git_out("ls-tree", "--name-only", "HEAD", cwd=clone).splitlines() if "{{" in name]
    try:
        definition = json.loads(git_out("show", "HEAD:cookiecutter.json", cwd=clone) or "{}")
    except ValueError:
        definition = {}
    extensions = definition.get("_extensions") if isinstance(definition, dict) else None
    modules = [str(ext).split(".")[0] for ext in extensions] if isinstance(extensions, list) else []
    paths = ["cookiecutter.json", "hooks", "templates", "local_extensions.py", *rendered]
    paths += [path for module in modules for path in (f"{module}.py", module) if path not in paths]
    return [":(literal)" + path for path in paths]


def commits_behind(clone: Path, commit: str, directory: str) -> int | None:
    if not git_out("rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}", cwd=clone):
        return None
    count = git_out("rev-list", "--count", f"{commit}..HEAD", "--", *template_pathspec(clone, directory), cwd=clone)
    return int(count) if count.isdigit() else None


def base_commit_for(clone: Path, date: str | None, directory: str) -> dict[str, str] | None:
    """The template's last commit at or before ``date`` (the project's first commit).

    Only the branch's own history counts (``--first-parent``): a commit from a feature branch that was merged later
    was not the template's state at ``date``. ``None`` when the project is older than the template, or than the
    template folder ``directory`` (the Node template was added after the Python one).
    """
    if not date:
        return None
    sha = git_out("rev-list", "-1", "--first-parent", f"--before={date}", "HEAD", cwd=clone)
    if not sha or run(["git", "cat-file", "-e", f"{sha}:{definition_path(directory)}"], cwd=clone).returncode != 0:
        return None
    return {"commit": sha, "date": git_out("log", "-1", "--format=%cI", sha, cwd=clone)}


# --- cruft ---------------------------------------------------------------------


def render(clone: Path, commit: str, directory: str, answers: dict[str, Any], work: Path) -> Path:
    """Render the template at ``commit`` with ``answers``; the template's own hooks check the answers."""
    answers_file = work / "answers.json"
    answers_file.write_text(json.dumps(answers), encoding="utf-8")
    out = work / "render"
    out.mkdir()
    failure = cruft_create(str(clone), commit, out, answers_file, cookiecutter_config(work), directory)
    if failure:
        raise failure
    return rendered_project(out, answers["project_name"])


def files_under(root: Path) -> list[str]:
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        found.extend(str((Path(dirpath) / name).relative_to(root)) for name in filenames)
    return sorted(found)


def compare(rendered: Path, project: Path) -> dict[str, list[str]]:
    match: dict[str, list[str]] = {"same": [], "differs": [], "missing": []}
    for rel in files_under(rendered):
        if rel == CRUFT_FILE:
            continue
        mine = project / rel
        if not mine.is_file():
            match["missing"].append(rel)
        elif mine.read_bytes() == (rendered / rel).read_bytes():
            match["same"].append(rel)
        else:
            match["differs"].append(rel)
    return match


def run_update(target: Path, sha: str, answers: dict[str, Any] | None, work: Path) -> None:
    cmd = [*CRUFT, "update", "--project-dir", str(target), "--skip-apply-ask", "--checkout", sha]
    if answers:
        variables = work / "variables.json"
        variables.write_text(json.dumps({"context": {"cookiecutter": answers}}), encoding="utf-8")
        cmd += ["--variables-to-update-file", str(variables)]
    proc = run(cmd, cwd=target)
    if proc.returncode != 0:
        raise Stop(
            EXIT_FAILED,
            ["cruft update failed.", output_of(proc).strip()[-800:]],
            step="cruft",
            changed=run(["git", "status", "--porcelain"], cwd=target).stdout.strip() != "",
        )


def update_report(target: Path) -> dict[str, Any]:
    """Files changed by the update, files with conflict markers, and rejected hunks (``*.rej``)."""
    # -z everywhere: plain paths (no C-quoting of spaces or non-ASCII names) and renames as separate fields.
    conflicts = [p for p in git_out("diff", "--name-only", "-z", "--diff-filter=U", cwd=target).split("\0") if p]
    # Untracked *.rej files, ignored ones included (a project's .gitignore often lists *.rej).
    rejects = sorted(p for p in git_out("ls-files", "-z", "--others", "--", "*.rej", cwd=target).split("\0") if p)
    changes = {"M": "modified", "A": "added", "D": "deleted", "R": "renamed", "U": "conflict", "?": "added"}
    files = []
    entries = iter(run(["git", "status", "--porcelain", "-z", "--untracked-files=all"], cwd=target).stdout.split("\0"))
    for entry in entries:
        if not entry:
            continue
        code, path = entry[:2], entry[3:]
        if "R" in code or "C" in code:
            next(entries, None)  # the original path of a rename or copy follows as its own field
        if path.endswith(".rej"):
            continue
        kind = "conflict" if "U" in code or code in {"AA", "DD"} else changes.get(code.strip()[:1], "modified")
        files.append({"path": path, "change": kind})
    return {"files": files, "conflicts": conflicts, "rejects": rejects}


def read_answers(path: str | None) -> dict[str, Any] | None:
    if path is None:
        return None
    try:
        answers = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Stop(EXIT_INVALID, [f"Could not read the answers file {path}: {exc}"]) from exc
    if not isinstance(answers, dict):
        raise Stop(EXIT_INVALID, ["The answers file must contain a JSON object."])
    return answers


# --- commands ------------------------------------------------------------------


def cmd_status(args: argparse.Namespace) -> None:
    check_tools()
    project = project_dir(args.project)
    state = git_state(project)
    cruft = read_link(project)
    language = args.language or detect_language(project, cruft)
    template = choose_template(args, cruft)
    ref = choose_ref(args, cruft, template)
    result: dict[str, Any] = {
        "project_dir": str(project),
        "git": state,
        "language": language,
        "linked": cruft is not None,
        "template": template,
        "ref": ref,
    }
    with template_clone(template, ref) as (clone, latest):
        result["latest_commit"] = latest
        if cruft is not None:
            directory = cruft.get("directory") or ""
            behind = commits_behind(clone, cruft["commit"], directory)
            questions, _ = parse_questions(definition_at(clone, latest, directory))
            known = cruft["context"]["cookiecutter"]
            result.update(
                link=link_summary(cruft),
                behind=behind,
                up_to_date=cruft["commit"] == latest or behind == 0,
                new_questions=[q for q in questions if q["name"] not in known],
            )
        else:
            directory = LANGUAGES[language] if language is not None else ""
            suggested = base_commit_for(clone, state["first_commit_date"], directory)
            result["suggested_commit"] = suggested
            if language is not None:
                at = suggested["commit"] if suggested else latest
                questions, derived = parse_questions(definition_at(clone, at, directory))
                result.update(questions_at=at, questions=questions, derived=derived)
    finish(EXIT_OK, **result)


def cmd_link(args: argparse.Namespace) -> None:
    answers = read_answers(args.answers)
    check_tools()
    project = project_dir(args.project)
    require_clean_repo(git_state(project), project)
    if read_link(project) is not None:
        raise Stop(EXIT_PROJECT, [f"The project is already linked ({CRUFT_FILE} exists). Use update instead."])
    language = args.language or detect_language(project, None)
    if language is None:
        raise Stop(EXIT_INVALID, ["Could not tell whether this is a Python or Node project; pass --language."])
    directory = LANGUAGES[language]
    template = choose_template(args, None)
    ref = choose_ref(args, None, template)
    with template_clone(template, ref) as (clone, _), tempfile.TemporaryDirectory(prefix="project-kit-") as tmp:
        sha = resolve_commit(clone, args.commit)
        if run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=clone).returncode != 0:
            raise Stop(EXIT_INVALID, [f"{sha[:12]} is not on the template's {ref} branch."])
        questions, derived = parse_questions(definition_at(clone, sha, directory))
        validate_answers(answers, questions, derived)
        match = compare(render(clone, sha, directory, answers or {}, Path(tmp)), project)
    summary = {k: len(v) for k, v in match.items()}
    result: dict[str, Any] = {
        "project_dir": str(project),
        "language": language,
        "template": template,
        "ref": ref,
        "commit": sha,
        "match": match,
        "summary": summary,
    }
    if args.dry_run:
        finish(EXIT_OK, dry_run=True, **result)

    with tempfile.TemporaryDirectory(prefix="project-kit-") as tmp:
        proc = run(
            [
                *CRUFT,
                "link",
                template_arg(template),
                *directory_args(directory),
                "--project-dir",
                str(project),
                "--checkout",
                sha,
                "--no-input",
                "--extra-context",
                json.dumps(answers),
                "--config-file",
                str(cookiecutter_config(Path(tmp))),
            ]
        )
    if proc.returncode != 0 or not (project / CRUFT_FILE).is_file():
        raise Stop(EXIT_FAILED, ["cruft link failed.", output_of(proc).strip()[-800:]], step="cruft")
    write_checkout(project, ref)
    finish(EXIT_OK, dry_run=False, cruft=link_summary(read_link(project) or {}), **result)


def cmd_update(args: argparse.Namespace) -> None:
    answers = read_answers(args.answers)
    check_tools()
    project = project_dir(args.project)
    require_clean_repo(git_state(project), project)
    cruft = read_link(project)
    if cruft is None:
        raise Stop(EXIT_PROJECT, [f"The project is not linked to the template (no {CRUFT_FILE}). Link it first."])
    directory = cruft.get("directory") or ""
    template = choose_template(args, cruft)
    ref = choose_ref(args, cruft, template)
    with template_clone(template, ref) as (clone, latest):
        questions, derived = parse_questions(definition_at(clone, latest, directory))
        behind = commits_behind(clone, cruft["commit"], directory)
    if answers:
        validate_answers(answers, questions, derived, partial=True)
    if not args.dry_run and not args.expect_commit:
        raise Stop(
            EXIT_INVALID, ["Preview the update with --dry-run first, then pass its to_commit as --expect-commit."]
        )
    if args.expect_commit and not commit_matches(args.expect_commit, latest):
        raise Stop(
            EXIT_FAILED,
            [f"The template changed since the preview: previewed {args.expect_commit}, now {latest}. Preview again."],
            step="commit-check",
            changed=False,
        )
    result: dict[str, Any] = {
        "project_dir": str(project),
        "template": template,
        "ref": ref,
        "from_commit": cruft["commit"],
        "to_commit": latest,
        "behind": behind,
    }
    # Same rule as ``status``: no template commit since the recorded one touched this template.
    if (cruft["commit"] == latest or behind == 0) and not answers:
        finish(EXIT_OK, dry_run=args.dry_run, up_to_date=True, files=[], conflicts=[], rejects=[], **result)

    with tempfile.TemporaryDirectory(prefix="project-kit-") as tmp:
        work = Path(tmp)
        if args.dry_run:
            copy = work / "project"
            proc = run(["git", "clone", "--quiet", "--no-hardlinks", "--", str(project), str(copy)])
            if proc.returncode != 0:
                raise Stop(EXIT_FAILED, ["Could not copy the project to preview the update.", output_of(proc)])
            run_update(copy, latest, answers, work)
            write_checkout(copy, ref)
            report = update_report(copy)
            run(["git", "add", "-A"], cwd=copy)
            patch = run(["git", "diff", "--cached", "--no-color"], cwd=copy).stdout
            finish(EXIT_OK, dry_run=True, up_to_date=not report["files"], patch=patch, **report, **result)

        run_update(project, latest, answers, work)
    if (project / CRUFT_FILE).is_file() and read_link(project)["commit"] == latest:  # type: ignore[index]
        write_checkout(project, ref)
    report = update_report(project)
    finish(EXIT_OK, dry_run=False, up_to_date=not report["files"], **report, **result)


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--project", default=".", help="project folder (default: current folder)")
    common.add_argument("--template", default=None, help="template git URL or local path (default: cookiecutter-gi)")
    common.add_argument("--ref", default=None, help="template branch to follow (default: the recorded or default one)")
    common.add_argument("--language", choices=sorted(LANGUAGES), default=None, help="override language detection")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", parents=[common], help="report link and template state").set_defaults(func=cmd_status)

    link = sub.add_parser("link", parents=[common], help="link an unlinked project to the template")
    link.add_argument("--answers", required=True, help="JSON file with the template answers inferred for the project")
    link.add_argument("--commit", required=True, help="template commit the project was generated from")
    link.add_argument("--dry-run", action="store_true", help="compare the project with the template; change nothing")
    link.set_defaults(func=cmd_link)

    update = sub.add_parser("update", parents=[common], help="apply template changes")
    update.add_argument("--answers", default=None, help="JSON file with answers to new or changed questions")
    update.add_argument("--expect-commit", default=None, help="template commit from the preview; stop if it changed")
    update.add_argument("--dry-run", action="store_true", help="preview the exact diff on a copy; change nothing")
    update.set_defaults(func=cmd_update)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except Stop as stop:
        finish(stop.code, messages=[m for m in stop.messages if m], **stop.extra)
    except Exception as exc:  # the contract promises JSON on stdout, even for bugs
        finish(EXIT_FAILED, messages=[f"Unexpected error: {type(exc).__name__}: {exc}"], step="internal")


if __name__ == "__main__":
    main()
