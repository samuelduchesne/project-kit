---

description: "Task list for audit-project"
---

# Tasks: audit-project

**Input**: `/specs/006-audit-project/`

## Phase 1: User Story 1 - Audit a linked project (P1) 🎯

- [X] T001 [US1] `plugins/project-kit/scripts/audit_project.py`: finding model, local checks (git, language, pre-commit, linter, changelog, spec-kit) per contracts/audit-project-cli.md
- [X] T002 [US1] Template checks: link record, behind count (via `upgrade_project` helpers), drift with `cruft diff` on a temporary clone; `--offline` and unreachable template → `skipped`
- [X] T003 [US1] `tests/test_audit_project.py`: a freshly created fixture project has 0 errors and 0 warnings; seeded defects (edited file, template commit added, changelog without Unreleased, missing `.specify/`, missing pre-commit config) each give their finding; the project is unchanged (git status and file hashes)

## Phase 2: User Story 2 - Unlinked or foreign projects (P2)

- [X] T004 [US2] Unlinked: `not-linked`, template checks skipped with the reason; unknown language: `language-unknown`, linter check skipped
- [X] T005 [US2] Tests for both

## Phase 3: Skill and polish

- [X] T006 Rewrite `plugins/project-kit/skills/audit-project/SKILL.md`: run, explain by severity, map fixes to workflows, change nothing
- [X] T007 README, CHANGELOG
