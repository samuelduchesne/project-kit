# Implementation Plan: upgrade-project

**Branch**: `005-upgrade-project` | **Date**: 2026-10-30 | **Spec**: [spec.md](./spec.md)

## Summary

A stdlib script, `plugins/project-kit/scripts/upgrade_project.py`, reusing `new_project.py`'s template access and validation, with three commands:

- `status`: read-only report (git state, language, link record, current and latest template commit, commits behind for the template's folder, questions added since the project's commit; for unlinked projects, the suggested base commit and the questions at that commit).
- `link [--dry-run]`: validate inferred answers against the template at the base commit; the dry run renders the template there and compares it with the project file by file; the real run checks the same, then runs `cruft link` and records the branch as `checkout`.
- `update [--dry-run]`: the dry run clones the project into a temporary folder, runs `cruft update` there pinned to the latest commit, and returns the files, conflicts, rejected hunks and full patch; the real run checks the commit, runs the same update in the project, and reports the same. Nothing is committed.

The skill drives the conversation: status → (infer answers, link preview, refine, confirm, link) → update preview → confirm → apply → resolve conflicts with the user → offer to commit.

## Technical Context

Python ≥ 3.9 stdlib, cruft 2.16.0 + cookiecutter 2.7.1 via `uvx`, git; tests with a fixture template that gains a second commit.

## Constitution Check

| Principle | Check | Result |
|-----------|-------|--------|
| I. Templates are the source of truth | Every change comes from `cruft update`/`cruft link` against cookiecutter-gi | Pass |
| II. Scripts for predictable steps | Status, link and update are scripted with logged commands and dry runs; Claude infers answers, explains, resolves conflicts | Pass |
| III. Show before changing | Link and update previews; clean tree required; same commit enforced; no commit or deletion without confirmation | Pass |
| IV. Works wherever installed | Same tool checks as new-project; pinned cruft | Pass |

## Research

- **R1 Exact preview**: cruft has no dry run; running it on `git clone <project>` (a clean tree equals `HEAD`) produces the same three-way application the real run will make. The patch is `git diff --cached` after `git add -A` in the clone, with `.rej` files and unmerged paths listed separately.
- **R2 Same commit**: `update` resolves the branch head with `git ls-remote`, runs `cruft update --checkout <sha>`, then writes the branch back into `checkout` in `.cruft.json`, because cruft records whatever `--checkout` it was given and a SHA would pin the project (same reasoning as spec 002 R1). The real run takes `--expect-commit` from the preview.
- **R3 Base commit for unlinked projects**: `git rev-list -1 --before=<first project commit date> <branch>` in a full clone of the template; if the project is older than the template, none is suggested and the skill offers the latest commit.
- **R4 Link match report**: render the template at the base commit with the answers (`cruft create --checkout <sha>` into a temporary folder; this also runs the template's own input checks) and compare each rendered file with the project's: `same`, `differs`, `missing`. `.cruft.json` is ignored.
- **R5 cruft link**: `cruft link <template> --project-dir <p> --checkout <sha> --no-input --extra-context <json> [--directory node]` writes `.cruft.json` with the context built from defaults plus the answers; it runs no hooks, hence the render check first. `checkout` is then rewritten to the branch.
- **R6 New questions**: questions in the latest `cookiecutter.json` missing from the project's context; answers are passed with `--variables-to-update-file` (a `{"context": {"cookiecutter": …}}` file). Without answers cruft uses template defaults.
- **R7 Template mismatch**: a `.cruft.json` whose template is not cookiecutter-gi (URL compared without scheme, `.git` and case) stops with exit 3 unless `--template` names it.

## Project Structure

```text
plugins/project-kit/scripts/upgrade_project.py
plugins/project-kit/scripts/new_project.py      # shared helpers (partial validation)
plugins/project-kit/skills/upgrade-project/SKILL.md
tests/test_upgrade_project.py
```
