---

description: "Task list for new-project (Python)"
---

# Tasks: new-project for Python

**Input**: Design documents from `/specs/002-new-project-python/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: The plan includes automated tests for the script (fixture template), written alongside each story.

## Format: `[ID] [P?] [Story] Description`

---

## Phase 1: Setup

- [X] T001 Create `plugins/project-kit/scripts/` and `tests/` directories

---

## Phase 2: Foundational (Blocking Prerequisites)

- [X] T002 Create `plugins/project-kit/scripts/new_project.py` skeleton: `from __future__ import annotations`, stdlib only, constants `DEFAULT_TEMPLATE = "https://github.com/samuelduchesne/cookiecutter-gi"` and `SPECKIT_REF = "v1.2.5"`, argparse with subcommands `check`, `options`, `create` and common `--template`/`--ref`, a `Result` helper that prints one JSON object to stdout and exits with the contract codes (0 ok, 2 invalid, 3 environment, 4 destination, 5 failed), a `run()` helper that logs each command to stderr and captures output
- [X] T003 Implement template access in `new_project.py`: resolve default branch via `git ls-remote --symref <template> HEAD` (local paths: `git -C <path> symbolic-ref --short HEAD`), shallow clone into a `tempfile.TemporaryDirectory`, return `(ref, commit, cookiecutter.json)`; map failures to exit 3 with a message naming the template and the likely cause (access or network)
- [X] T004 Implement `parse_questions()` per data-model.md: skip keys starting with `_`; list → `choice` (default = first item); bool → `bool`; string containing `{{` → derived; else `text`; prompt and choice labels from `__prompts__`
- [X] T005 Create `tests/test_new_project.py` fixture: build a git repo template in a temp folder with `cookiecutter.json` containing a text question, a bool, a choice with `__prompts__`, a derived `project_slug`, and a `hooks/pre_gen_project.py` that rejects names containing `_`; helper to run the script via `subprocess` and parse JSON

**Checkpoint**: script can read any template's questions

---

## Phase 3: User Story 1 - Create with the recommended setup (P1) 🎯 MVP

**Independent Test**: `create` with minimal answers against the fixture produces a project with `.cruft.json` (checkout = branch), `.specify/`, and a single commit; nothing outside the project changes

- [X] T006 [US1] Implement `check` in `new_project.py`: `shutil.which` for `git` and `uvx`, capture versions, template reachability via T003; exit 3 listing every missing item with an install hint (git: system package manager; uv: https://docs.astral.sh/uv/)
- [X] T007 [US1] Implement `options` in `new_project.py`: output `template`, `ref`, `commit`, `questions`, `derived` per contracts/new-project-cli.md
- [X] T008 [US1] Implement `create` (real run) in `new_project.py`: load answers; destination `PARENT/<project_name>` must not exist or be empty (exit 4); write answers to a temp JSON file; `uvx cruft create <template> --no-input --checkout <ref> --output-dir <PARENT> --extra-context-file <file>`; if `--expect-commit` differs from `.cruft.json` `commit`, exit 5 step `commit-check`; `uvx --from git+https://github.com/github/spec-kit.git@v1.2.5 specify init --here --integration claude --script sh --non-interactive --force` in the project; `git init -b main`, `git add -A`, `git -c user.name=<author> -c user.email=<email> commit -m "Initial commit from cookiecutter-gi <sha12>"` (author/email from answers, else git config, else exit 3 before any change); report `project_dir`, `commit`, `answers` (from `.cruft.json` context), `non_default`, `derived`, `files`, `git_commit`; any step failure → exit 5 with `step` and `created`, never deleting
- [X] T009 [US1] Tests in `tests/test_new_project.py`: `options` lists the fixture's questions with correct types/defaults/labels and `project_slug` as derived; full `create` produces `.cruft.json` with `checkout` = `main` and the answers, `.specify/` present, `git log` has exactly one commit with the given author, `git status` clean
- [X] T010 [US1] Rewrite `plugins/project-kit/skills/new-project/SKILL.md` per contracts/skill-conversation.md: frontmatter `name: new-project` and a description of the working workflow (Python only; Node planned); body with the steps language check → `check` → `options` → interview (required: project name, description, author, email, GitHub handle; others as one defaults list) → write answers to a temp file outside any project → `create --dry-run` → show preview → confirm → `create --expect-commit` → report and next steps; every command written as `uv run --no-project "${CLAUDE_PLUGIN_ROOT}/scripts/new_project.py" …`; rules: never create without confirmation, never delete, relay template errors verbatim, stop and explain when no shell or tools

**Checkpoint**: a Python project can be created end to end

---

## Phase 4: User Story 2 - Choose the options (P2)

**Independent Test**: invalid choice, non-boolean yes/no, unknown key and missing `project_name` each give exit 2 with the allowed values and create nothing; valid non-default answers appear in `.cruft.json`

- [X] T011 [US2] Implement `validate_answers()` in `new_project.py` per data-model.md (unknown or derived keys rejected; choice membership with allowed values in the message; bool must be JSON boolean; text non-empty string; `project_name` required); compute `non_default`; call it at the start of `create` (both modes) → exit 2 with all problems at once
- [X] T012 [US2] Tests: each invalid case above returns exit 2 and leaves the destination parent empty; a non-default choice and bool are recorded in `.cruft.json` context

**Checkpoint**: answers are checked against the template definition

---

## Phase 5: User Story 3 - Preview and fail safely (P3)

**Independent Test**: dry run reports files and derived names and leaves the parent empty; non-empty destination → exit 4; template hook rejection → exit 2 with the hook's `ERROR:` line; unreachable template → exit 3

- [X] T013 [US3] Implement `create --dry-run` in `new_project.py`: same validation and destination check, run `cruft create` into a temporary folder, read `.cruft.json` for `commit`, `answers`, `derived`; list top-level files; return `steps` the real run would execute; remove the temporary folder; on cruft failure, extract lines starting with `ERROR:` (or the last error line) and return exit 2 with them
- [X] T014 [US3] Tests: dry run returns `files` and `derived.project_slug` and leaves the parent empty; fixture hook rejects `bad_name` with exit 2 and its message; existing non-empty destination → exit 4 and its contents unchanged; `--template /nonexistent` → exit 3
- [X] T015 [US3] Run the script against the real template per quickstart step 3 (check, options, dry run, real create, `uvx cruft check`, negative cases) and fix any differences from the contract

**Checkpoint**: previews and failures change nothing

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T016 [P] Add a `script-tests` job to `.github/workflows/validate.yml`: checkout, `astral-sh/setup-uv@v6`, git identity for tests, `uv run --no-project python -m unittest discover -s tests -v`
- [X] T017 [P] Bump `plugins/project-kit/.claude-plugin/plugin.json` `version` to `0.2.0`; update `README.md` workflow table (new-project: Available, Python; Node planned) and requirements (git, uv, access to cookiecutter-gi, Claude Code or local Cowork); add `CHANGELOG.md` entries under `[Unreleased]` → `### Added`/`### Changed`
- [X] T018 Run ruff check/format on the script and tests, the plugin validators, `check_manifests.py`, and the unittest suite; confirm no trailing whitespace and final newlines
- [X] T019 Set spec status to Implemented; commit, push `002-new-project-python`, open a pull request listing verification results and the manual conversation checks (quickstart step 4)

---

## Dependencies & Execution Order

- Setup → Foundational (T002–T005) → US1 (T006–T010) → US2 (T011–T012) → US3 (T013–T015) → Polish
- US2 and US3 build on `create` from US1 (same file), so they run after it
- T016 and T017 touch different files and can run in parallel

## Implementation Strategy

MVP = US1: a project can be created with defaults. US2 adds answer validation, US3 adds preview and safe failures; the skill (T010) already describes the preview flow, which becomes fully functional after T013.
