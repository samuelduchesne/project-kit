---

description: "Task list for the Node template"
---

# Tasks: Node template in cookiecutter-gi

**Input**: Design documents from `/specs/003-node-template/`

**Prerequisites**: plan.md, spec.md, research.md

All paths are in `samuelduchesne/cookiecutter-gi`.

## Format: `[ID] [P?] [Story] Description`

---

## Phase 1: Setup

- [X] T001 Create `node/`, `node/hooks/`, `node/{{cookiecutter.project_name}}/` and copy `local_extensions.py` to `node/local_extensions.py`
- [X] T002 Write `node/cookiecutter.json`: author, email, author_github_handle, project_name, project_description, node_version [24, 22, 26], include_github_actions, codecov, publish_to_npm, devcontainer, changelog, agent_instructions, agent_profile, open_source_license, `_extensions`, `__prompts__`

---

## Phase 2: User Story 1 - A working TypeScript library (P1) 🎯 MVP

- [X] T003 [US1] `package.json`, `tsconfig.json`, `tsconfig.build.json`, `biome.json`, `vitest.config.ts`, `src/index.ts`, `tests/index.test.ts`, `.gitignore`, `.nvmrc`
- [X] T004 [US1] `.pre-commit-config.yaml` (generic hooks + local Biome hook) and `Makefile` (install, check, test, build, clean-build, help)
- [X] T005 [US1] `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE_*` (copied from the Python template, unchanged)
- [X] T006 [US1] Agent files `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md` with minimal/full profiles and the changelog rule
- [X] T007 [US1] `.github/workflows/main.yml` (quality job with `make check`; test matrix from the chosen Node version up; optional Codecov upload), `copilot-setup-steps.yml`, `.vscode/`, `.devcontainer/devcontainer.json`
- [X] T008 [US1] Bake with defaults, `pnpm install`, `make check`, `pnpm test`, `pnpm build`, `uvx pre-commit run -a` all pass with no file changes

---

## Phase 3: User Story 2 - Options (P2)

- [X] T009 [US2] `node/hooks/post_gen_project.py`: prune per option, same helpers and agent/license tables as the Python hook
- [X] T010 [US2] `release.yml` for `publish_to_npm`; `"private": true` otherwise; README release section
- [X] T011 [US2] `tests/test_node_template.py`: defaults; each boolean off; every license; every agent choice; every Node version; YAML/JSON files parse; no `{{` left in output

---

## Phase 4: User Story 3 - Input checks (P3)

- [X] T012 [US3] `node/hooks/pre_gen_project.py`: npm name rule and boolean checks with `ERROR:` lines
- [X] T013 [US3] Tests: invalid names and booleans fail with nothing written; `false` strings on the command line are false; `node/local_extensions.py` equals the root copy

---

## Phase 5: Polish

- [X] T014 CI job `node-template` in `.github/workflows/main.yml`: bake with defaults and with publishing on, install, check, test, build
- [X] T015 [P] Docs: `docs/features/node.md`, `mkdocs.yml` nav, `README.md`, `CLAUDE.md`, `MANIFEST.in` (`recursive-include node *`)
- [X] T016 Python template tests unchanged and passing
