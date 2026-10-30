#!/usr/bin/env python3
"""Check a project against the cookiecutter-gi standards and report drift. Read-only.

Used by the project-kit ``audit-project`` skill. Checks git state, the template link and how far behind it is,
files that differ from the template, the lint and format setup (ruff or Biome through pre-commit), the changelog
and spec-kit. Prints one JSON object with every finding; progress goes to stderr.

Exit codes: 0 the audit ran (whatever it found), 3 the project folder does not exist, 5 internal error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from new_project import CRUFT, EXIT_ENVIRONMENT, EXIT_FAILED, EXIT_OK, SPECKIT_REF, Stop, finish, output_of, run
from upgrade_project import (
    choose_ref,
    choose_template,
    commits_behind,
    detect_language,
    git_state,
    read_link,
    template_clone,
)

LINTERS = {"python": "ruff", "node": "biome"}
DIFF_HEADER = re.compile(r"^diff --git upstream-template-old/(.+?) upstream-template-new/")
SEVERITIES = ("error", "warning", "info")


class Audit:
    def __init__(self, project: Path) -> None:
        self.project = project
        self.findings: list[dict[str, Any]] = []
        self.skipped: list[dict[str, str]] = []
        self.passed: list[str] = []

    def find(self, check: str, severity: str, message: str, fix: str, **extra: Any) -> None:
        self.findings.append({"id": check, "severity": severity, "message": message, "fix": fix, **extra})

    def ok(self, check: str) -> None:
        self.passed.append(check)

    def skip(self, check: str, reason: str) -> None:
        self.skipped.append({"check": check, "reason": reason})

    def file(self, name: str) -> str | None:
        path = self.project / name
        return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else None


def version_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", version)[:3])


# --- local checks ----------------------------------------------------------------


def check_git(audit: Audit, state: dict[str, Any]) -> None:
    if not state["repository"]:
        audit.find(
            "not-git",
            "error",
            "The project is not the root of a git repository.",
            "Run `git init -b main` and commit; upgrades need git history to show and revert changes.",
        )
        return
    audit.ok("git-repository")
    if state["clean"]:
        audit.ok("git-clean")
    else:
        audit.find(
            "git-dirty",
            "warning",
            "The project has uncommitted changes; the template checks only see committed files.",
            "Commit or stash the changes before upgrading.",
        )


def check_lint(audit: Audit, language: str | None) -> None:
    config = audit.file(".pre-commit-config.yaml")
    if config is None:
        audit.find(
            "pre-commit-missing",
            "error",
            "No .pre-commit-config.yaml: linting and formatting don't run before commits.",
            "upgrade-project restores the template's pre-commit configuration.",
        )
        return
    audit.ok("pre-commit")
    if language is None:
        audit.skip("linter", "unknown language")
        return
    linter = LINTERS[language]
    problems = []
    if linter not in config.lower():
        problems.append(f".pre-commit-config.yaml has no {linter} hook")
    if language == "node" and audit.file("biome.json") is None and audit.file("biome.jsonc") is None:
        problems.append("there is no biome.json")
    if problems:
        audit.find(
            "linter-missing",
            "error",
            f"The {language.capitalize()} standard is {linter} through pre-commit, but " + " and ".join(problems) + ".",
            "upgrade-project restores the template's lint and format setup.",
        )
    else:
        audit.ok("linter")


def check_changelog(audit: Audit) -> None:
    text = audit.file("CHANGELOG.md")
    if text is None:
        audit.find(
            "changelog-missing",
            "error",
            "No CHANGELOG.md.",
            "changelog-keeper creates one from the git history.",
        )
        return
    problems = []
    if "keepachangelog.com/en/1.1.0" not in text:
        problems.append("does not reference Keep a Changelog 1.1.0")
    if not re.search(r"^## \[Unreleased\]", text, re.MULTILINE):
        problems.append("has no `## [Unreleased]` section")
    if problems:
        audit.find(
            "changelog-format",
            "warning",
            "CHANGELOG.md " + " and ".join(problems) + ".",
            "changelog-keeper audits and fixes it.",
        )
    else:
        audit.ok("changelog")


def check_speckit(audit: Audit) -> None:
    if not (audit.project / ".specify").is_dir():
        audit.find(
            "speckit-missing",
            "warning",
            "spec-kit is not set up (no .specify/).",
            f"Run `uvx --from git+https://github.com/github/spec-kit.git@{SPECKIT_REF} specify init --here "
            "--integration claude --script sh` in the project.",
        )
        return
    try:
        options = json.loads(audit.file(".specify/init-options.json") or "{}")
    except ValueError:
        options = {}
    version = str(options.get("speckit_version") or "")
    if version and version_tuple(version) < version_tuple(SPECKIT_REF):
        audit.find(
            "speckit-outdated",
            "warning",
            f"spec-kit {version} is older than {SPECKIT_REF.lstrip('v')}, the version project-kit sets up.",
            "Upgrade spec-kit in the project (see the spec-kit upgrade guide).",
            version=version,
        )
    else:
        audit.ok("speckit")


# --- template checks -------------------------------------------------------------


def drifted_files(project: Path, work: Path) -> list[str]:
    """Committed files that differ from the template at the recorded commit, from ``cruft diff`` on a clone."""
    copy = work / "project"
    proc = run(["git", "clone", "--quiet", "--no-hardlinks", "--", str(project), str(copy)])
    if proc.returncode != 0:
        raise Stop(EXIT_ENVIRONMENT, ["Could not copy the project to compare it with the template."])
    proc = run([*CRUFT, "diff", "--project-dir", str(copy), "--exit-code"], cwd=copy)
    if proc.returncode not in (0, 1):
        raise Stop(EXIT_ENVIRONMENT, ["cruft diff failed.", output_of(proc).strip()[-300:]])
    return sorted({m.group(1) for line in proc.stdout.splitlines() if (m := DIFF_HEADER.match(line))})


def check_template(audit: Audit, args: argparse.Namespace, state: dict[str, Any], result: dict[str, Any]) -> None:
    try:
        cruft = read_link(audit.project)
    except Stop as stop:
        audit.find("not-linked", "warning", stop.messages[0], "upgrade-project can link the project again.")
        audit.skip("template", "unreadable link record")
        return
    result["linked"] = cruft is not None
    if cruft is None:
        audit.find(
            "not-linked",
            "warning",
            "The project is not linked to the cookiecutter-gi template (no .cruft.json), so it can't be upgraded.",
            "upgrade-project links it at the template version it was generated from.",
        )
        audit.skip("template", "not linked")
        return
    if args.offline:
        audit.skip("template", "offline")
        return
    try:
        template = choose_template(args, cruft)
    except Stop as stop:
        audit.find(
            "template-foreign",
            "warning",
            stop.messages[0],
            "Nothing to do if this is intended; the standards checks still apply.",
        )
        audit.skip("template", "linked to another template")
        return
    try:
        ref = choose_ref(args, cruft, template)
        with template_clone(template, ref) as (clone, latest):
            behind = commits_behind(clone, cruft["commit"], cruft.get("directory") or "")
    except Stop as stop:
        audit.skip("template", " ".join(stop.messages[:1]))
        return
    result["template"] = {"commit": cruft["commit"], "latest_commit": latest, "behind": behind, "ref": ref}
    if behind is None:
        audit.find(
            "template-behind",
            "warning",
            f"The recorded template commit {cruft['commit'][:12]} is not on the template's {ref} branch.",
            "upgrade-project updates the project to the latest template.",
        )
    elif behind:
        audit.find(
            "template-behind",
            "warning",
            f"{behind} template commit(s) behind ({cruft['commit'][:7]} → {latest[:7]}).",
            "upgrade-project previews and applies the template changes.",
            behind=behind,
        )
    else:
        audit.ok("template-current")

    if not state["repository"]:
        audit.skip("template-drift", "not a git repository")
        return
    try:
        with tempfile.TemporaryDirectory(prefix="project-kit-audit-") as tmp:
            files = drifted_files(audit.project, Path(tmp))
    except Stop as stop:
        audit.skip("template-drift", " ".join(stop.messages))
        return
    if files:
        shown = ", ".join(files[:10]) + (f" and {len(files) - 10} more" if len(files) > 10 else "")
        audit.find(
            "template-drift",
            "info",
            f"{len(files)} file(s) differ from the template at the recorded commit: {shown}.",
            "Review them: local changes are often intended. upgrade-project keeps them and merges template changes.",
            files=files,
        )
    else:
        audit.ok("template-drift")


def audit_project(args: argparse.Namespace) -> None:
    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        raise Stop(EXIT_ENVIRONMENT, [f"{project} is not a folder."])
    audit = Audit(project)
    state = git_state(project)
    try:
        language = detect_language(project, read_link(project))
    except Stop:
        language = detect_language(project, None)
    result: dict[str, Any] = {"project_dir": str(project), "language": language, "linked": False}

    check_git(audit, state)
    if language is None:
        audit.find(
            "language-unknown",
            "warning",
            "Neither pyproject.toml nor package.json found; the standards cover Python and Node projects.",
            "Nothing to fix if this is not a Python or Node project.",
        )
    check_template(audit, args, state, result)
    check_lint(audit, language)
    check_changelog(audit)
    check_speckit(audit)

    order = {severity: i for i, severity in enumerate(SEVERITIES)}
    findings = sorted(audit.findings, key=lambda f: order[f["severity"]])
    summary = {severity: sum(f["severity"] == severity for f in findings) for severity in SEVERITIES}
    finish(EXIT_OK, **result, summary=summary, findings=findings, skipped=audit.skipped, passed=audit.passed)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", default=".", help="project folder (default: current folder)")
    parser.add_argument("--template", default=None, help="template git URL or local path (default: cookiecutter-gi)")
    parser.add_argument("--ref", default=None, help="template branch (default: the recorded or default one)")
    parser.add_argument("--offline", action="store_true", help="skip the checks that need the template")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    try:
        audit_project(args)
    except Stop as stop:
        finish(stop.code, messages=[m for m in stop.messages if m], **stop.extra)
    except Exception as exc:  # the contract promises JSON on stdout, even for bugs
        finish(EXIT_FAILED, messages=[f"Unexpected error: {type(exc).__name__}: {exc}"], step="internal")


if __name__ == "__main__":
    main()
