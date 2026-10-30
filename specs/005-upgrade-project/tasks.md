---

description: "Task list for upgrade-project"
---

# Tasks: upgrade-project

**Input**: `/specs/005-upgrade-project/`

## Phase 1: Foundational

- [X] T001 `new_project.py`: `validate_answers(..., partial=True)` skips the required-answer checks; `fetch_definition` can return a full clone and read a given commit (shared helper)
- [X] T002 `plugins/project-kit/scripts/upgrade_project.py` skeleton: imports helpers from `new_project`, `--project/--template/--ref`, exit code 4 = project state, git helpers (`is_repo`, `clean`, `first_commit_date`), language detection, `.cruft.json` reading, template-URL comparison
- [X] T003 Fixture helpers in `tests/test_upgrade_project.py`: template with two commits (the second changes a file and adds a question), project created with `new_project.py create`, unlinked project from plain cookiecutter at the first commit

## Phase 2: User Story 1 - Update a linked project (P1) 🎯

- [X] T004 [US1] `status` for linked projects: latest commit, `behind` for the template folder, `up_to_date`, `new_questions`
- [X] T005 [US1] `update --dry-run`: clone, `cruft update -y --checkout <sha>` in the clone, collect files/conflicts/rejects/patch, remove the clone
- [X] T006 [US1] `update` real run: `--expect-commit` check, run in place, restore `checkout` to the branch, same report
- [X] T007 [US1] Tests: preview lists the changed file and leaves the project unchanged; apply produces the previewed diff and moves `.cruft.json` to the new commit with `checkout: main`; up-to-date reports nothing to do; new-question answers reach the project; local edits conflicting with the update are reported

## Phase 3: User Story 2 - Link then update (P2)

- [X] T008 [US2] `status` for unlinked projects: suggested base commit and its questions
- [X] T009 [US2] `link --dry-run`: validate, render at the base commit, per-file match report
- [X] T010 [US2] `link`: same checks, `cruft link`, `checkout` set to the branch
- [X] T011 [US2] Tests: suggested commit is the first fixture commit; correct answers give 0 `differs`; link writes only `.cruft.json`; the update after linking brings the second commit's change

## Phase 4: User Story 3 - Refuse unsafe starts (P3)

- [X] T012 [US3] Tests: dirty tree, not a git repository, linking an already linked project, template changed between preview and apply

## Phase 5: Skill and polish

- [X] T013 Rewrite `plugins/project-kit/skills/upgrade-project/SKILL.md` (conversation in plan.md Summary)
- [X] T014 README, CHANGELOG, CI job name
