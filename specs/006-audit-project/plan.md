# Implementation Plan: audit-project

**Branch**: `006-audit-project` | **Date**: 2026-10-30 | **Spec**: [spec.md](./spec.md)

## Summary

A read-only stdlib script, `plugins/project-kit/scripts/audit_project.py`, runs every check and prints findings as JSON; the skill explains them and names the workflow that fixes each one. Template checks reuse `upgrade_project.py` (link record, latest commit, commits behind) and `cruft diff` on a temporary clone of the project for drift.

## Constitution Check

| Principle | Check | Result |
|-----------|-------|--------|
| I. Templates are the source of truth | Drift is measured against the template itself (`cruft diff`), not a copy of its files | Pass |
| II. Scripts for predictable steps | All checks scripted; Claude explains and prioritizes | Pass (read-only, no dry run needed) |
| III. Show before changing | Changes nothing; fixes are separate workflows with their own previews | Pass |
| IV. Works wherever installed | Template checks skipped with a reason when offline; local checks always run | Pass |

## Research

- **R1 Drift**: `cruft diff --exit-code` renders the template at the recorded commit with the recorded answers and diffs it against the project; its output names each file (`diff --git a/<path> b/<path>`). It runs on a `git clone` of the project in a temporary folder so the audit cannot touch the project (cruft diff writes nothing, but the clone also hides untracked files from the comparison).
- **R2 Behind**: `git rev-list --count <commit>..<latest> -- <folder>` in a full template clone, with `:(exclude)node` for Python, so Node-only commits don't count against Python projects and vice versa.
- **R3 Lint/format**: `.pre-commit-config.yaml` must exist and mention `ruff` (Python) or `biome` (Node); Node projects must also have `biome.json`.
- **R4 Changelog**: `CHANGELOG.md` must exist, reference Keep a Changelog 1.1.0 and have a `## [Unreleased]` heading. Deeper checks are `changelog-keeper`'s job.
- **R5 spec-kit**: `.specify/` must exist; `.specify/init-options.json` `speckit_version` older than the plugin's pin is a warning.
- **R6 Severity**: error = upgrades or the standard can't work (not a git repository, no pre-commit/linter, no changelog); warning = out of date or incomplete (behind the template, unlinked, dirty tree, old spec-kit, no Unreleased section); info = drifted files (often intentional).

## Project Structure

```text
plugins/project-kit/scripts/audit_project.py
plugins/project-kit/skills/audit-project/SKILL.md
tests/test_audit_project.py
```
