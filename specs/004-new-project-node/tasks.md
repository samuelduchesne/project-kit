---

description: "Task list for new-project (Node)"
---

# Tasks: new-project for Node

**Input**: `/specs/004-new-project-node/`

## Phase 1: Foundational

- [X] T001 Add `LANGUAGES = {"python": "", "node": "node"}` and a common `--language` option to `plugins/project-kit/scripts/new_project.py`; `fetch_definition` reads `<folder>/cookiecutter.json` and reports a missing folder as exit 3
- [X] T002 Pass `--directory` to `cruft create` and show it in `planned_steps`; add `language` and `directory` to `check`, `options` and `create` results
- [X] T003 Fixture: `make_template` in `tests/test_new_project.py` also writes a `node/` sub-template (own `cookiecutter.json`, hook and files)

## Phase 2: User Story 1 - Create a Node project (P1) 🎯

- [X] T004 [US1] Tests: `options --language node` lists the Node questions; `create --language node` (dry run and real) produces the Node files, `.cruft.json` with `directory: node`, spec-kit and one commit; Python results unchanged
- [X] T005 [US1] Test: a template without `node/` gives exit 3 for `--language node`

## Phase 3: User Story 2 - Language is explicit (P2)

- [X] T006 [US2] Rewrite step 1 of `plugins/project-kit/skills/new-project/SKILL.md`: infer Python or Node from the request or ask; refuse other languages; pass `--language` to every command; Node next steps (`npm install -g pnpm`, `make install`, commit `pnpm-lock.yaml`); update the frontmatter description

## Phase 4: Polish

- [X] T007 README (workflow table, new-project section), CHANGELOG, `plugin.json` version
