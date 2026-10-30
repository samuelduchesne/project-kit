---

description: "Task list for the project-kit marketplace and plugin skeleton"
---

# Tasks: Marketplace and Plugin Skeleton

**Input**: Design documents from `/specs/001-plugin-skeleton/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: The spec does not request TDD, so there are no separate test-first tasks. Automated checks are part of the deliverable (US3), and each story ends with a verification task drawn from [quickstart.md](./quickstart.md).

**Organization**: Tasks are grouped by user story so each story can be implemented and verified on its own.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

## Path Conventions

Paths are relative to the repository root, per the structure in [plan.md](./plan.md). The packaged plugin is `plugins/project-kit/`; everything else is repository-only.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the folder layout

- [X] T001 Create directories `.claude-plugin/`, `plugins/project-kit/.claude-plugin/`, `plugins/project-kit/skills/`, `.github/workflows/` and `.github/scripts/` at the repository root

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The two manifests every story depends on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 Create `plugins/project-kit/.claude-plugin/plugin.json` per contracts/manifests.md: `name` "project-kit" ("Required; kebab-case; namespaces skills"), `version` "0.1.0" ("Pinned; equals the first release tag"), one-sentence `description`, `author` {name "Samuel Letellier-Duchesne", url "https://github.com/samuelduchesne"}, `homepage` and `repository` "https://github.com/samuelduchesne/project-kit" (`homepage` "must parse as a URL"), `license` "MIT", `keywords` ["scaffolding", "templates", "cookiecutter", "cruft", "spec-kit", "changelog"]; no component path keys, `userConfig`, `mcpServers` or `hooks`
- [X] T003 Create `.claude-plugin/marketplace.json` per contracts/manifests.md: `name` "project-kit" ("Required; not a reserved name"), one-sentence `description` ("Required here because `--strict` fails without it"), `owner` {name "Samuel Letellier-Duchesne", url "https://github.com/samuelduchesne"}, and exactly one plugin entry {`name` "project-kit" ("MUST equal Plugin `name`"), `source` "./plugins/project-kit" ("starts with `./`; no `..`"), one-sentence `description`}; the entry "MUST NOT" set `version` or any component field
- [X] T004 Run `claude plugin validate . --strict` and `claude plugin validate ./plugins/project-kit --strict` from the repository root; both must print `Validation passed` and exit 0

**Checkpoint**: Manifests valid — user stories can begin

---

## Phase 3: User Story 1 - Install project-kit from the repository (Priority: P1) 🎯 MVP

**Goal**: Anyone can add the marketplace and install the plugin on claude.ai / desktop and in Claude Code

**Independent Test**: In a temporary `HOME`, `claude plugin marketplace add ./` then `claude plugin install project-kit@project-kit` succeeds and `claude plugin list` shows `project-kit@project-kit` enabled (quickstart step 3); remote install after merge (quickstart step 4)

### Implementation for User Story 1

- [X] T005 [US1] Create `README.md` with an "Install" section: claude.ai / desktop (Customize > Plugins > Add > Add marketplace → `samuelduchesne/project-kit` → add project-kit; updates via Check for updates or Sync automatically), Claude Code shell (`claude plugin marketplace add samuelduchesne/project-kit`, `claude plugin install project-kit@project-kit`) and session (`/plugin marketplace add …`, `/plugin install …`), updating (`claude plugin update project-kit@project-kit` or `/plugin` > Marketplaces > Update marketplace), and a note that on Team and Enterprise plans an Owner controls whether members can add marketplaces (FR-009, FR-010)
- [X] T006 [US1] Verify the local install per quickstart step 3 in a temporary `HOME`: marketplace add, install, `claude plugin list` shows `project-kit@project-kit` enabled

**Checkpoint**: The plugin installs from the repository; MVP reached

---

## Phase 4: User Story 2 - Discover the planned workflows (Priority: P2)

**Goal**: Three stub skills appear under project-kit and explain themselves without acting

**Independent Test**: `claude plugin details project-kit` lists exactly `audit-project`, `new-project`, `upgrade-project`; invoking each (or asking in plain language) yields purpose + "not implemented yet" and `git status` stays clean (quickstart steps 3 and 5)

### Implementation for User Story 2

- [X] T007 [P] [US2] Create `plugins/project-kit/skills/new-project/SKILL.md`: frontmatter `name: new-project` ("equals directory") and `description` starting "Placeholder (not yet implemented):" then the purpose "create a new Python or Node project from the cookiecutter-gi templates, with spec-kit, linting and a changelog set up"; body per contracts/install-interface.md "Stub behavior contract" (state purpose, state not implemented, run no commands, change no files, point to the repository)
- [X] T008 [P] [US2] Create `plugins/project-kit/skills/upgrade-project/SKILL.md` the same way, purpose "bring an existing project up to the latest cookiecutter-gi template, linking it first if needed"
- [X] T009 [P] [US2] Create `plugins/project-kit/skills/audit-project/SKILL.md` the same way, purpose "check a project against the standards and report drift without changing anything"
- [X] T010 [US2] Add a "Workflows" section to `README.md` listing the three skills (`/project-kit:new-project`, `/project-kit:upgrade-project`, `/project-kit:audit-project`), their purpose, and status "planned" (FR-009)
- [X] T011 [US2] Re-run `claude plugin validate ./plugins/project-kit --strict` and the quickstart step 3 install; confirm `claude plugin details project-kit` lists exactly the three skills and no speckit skills (SC-002, SC-004)

**Checkpoint**: Workflows are discoverable and inert

---

## Phase 5: User Story 3 - Keep the repository releasable (Priority: P3)

**Goal**: An automated check guards the install path; the repository explains itself and records changes

**Independent Test**: CI passes on the unmodified branch; each break in quickstart step 2 makes the matching check fail

### Implementation for User Story 3

- [X] T012 [P] [US3] Create `.github/scripts/check_manifests.py` (Python 3 stdlib only, `from __future__ import annotations`): load both manifests; fail with a clear message when the entry `name` differs from the plugin `name`, the entry `source` doesn't start with `./` or contains `..` or its directory lacks `.claude-plugin/plugin.json`, the entry sets `version`, the marketplace lists other than exactly one plugin, or the plugin directory contains `bin/`, `CLAUDE.md`, `hooks/`, `agents/` or `.mcp.json`; exit 0 on success, 1 on any failure
- [X] T013 [US3] Create `.github/workflows/validate.yml`: triggers `pull_request` and `push` to `main`; job on `ubuntu-latest` with `actions/checkout@v4` and `actions/setup-node@v4` (Node 22); `npm install -g @anthropic-ai/claude-code@2.1.314`; steps `claude plugin validate . --strict`, `claude plugin validate ./plugins/project-kit --strict`, `python3 .github/scripts/check_manifests.py`, and an install smoke test in a temporary `HOME` (marketplace add `./`, install `project-kit@project-kit`, assert `claude plugin details project-kit` output names all three skills); `permissions: contents: read`
- [X] T014 [P] [US3] Create `CHANGELOG.md` in Keep a Changelog 1.1.0 format (header linking keepachangelog.com/en/1.1.0 and semver.org/spec/v2.0.0) with `## [Unreleased]` → `### Added` entries for the marketplace and plugin skeleton, the three placeholder skills, the README, and the validation workflow; `[Unreleased]` link reference to `https://github.com/samuelduchesne/project-kit/commits/main` (FR-011)
- [X] T015 [US3] Complete `README.md`: opening description of what project-kit is and how it relates to cookiecutter-gi; a "Development" section with the repository layout (plugin in `plugins/project-kit/`, spec-kit files at the root and not packaged), how to validate locally, and where specs live; license line (MIT)
- [X] T016 [US3] Run the negative checks in quickstart step 2 locally (each break must make its command fail, then restore with `git checkout .`), and confirm the unmodified tree passes every check (SC-005)

**Checkpoint**: Releasable repository with a guarded install path

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T017 Run quickstart steps 1–3 end to end on the final tree; confirm no trailing whitespace and a final newline in every new file
- [X] T018 Set `**Status**` in `specs/001-plugin-skeleton/spec.md` to "Implemented", then commit, push the `001-plugin-skeleton` branch and open a pull request whose description links the spec and lists the verification results; quickstart steps 4–5 (remote install, stub behavior in a live session) are listed as manual checks after merge

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: none
- **Foundational (Phase 2)**: after Setup; blocks all stories
- **US1 (Phase 3)**: after Foundational
- **US2 (Phase 4)**: after Foundational; independent of US1 except that T010 and T005 both edit `README.md` (do T005 first)
- **US3 (Phase 5)**: after Foundational; T013's smoke test asserts the three skills, so run it after T007–T009; T015 edits `README.md` after T005 and T010
- **Polish (Phase 6)**: after all stories

### Within Each User Story

- Manifests before verification; skills before the README workflow list; script before the workflow that calls it

### Parallel Opportunities

- T007, T008, T009 (three different skill files)
- T012 and T014 (script and changelog) alongside US2 work

---

## Parallel Example: User Story 2

```bash
Task: "Create plugins/project-kit/skills/new-project/SKILL.md"
Task: "Create plugins/project-kit/skills/upgrade-project/SKILL.md"
Task: "Create plugins/project-kit/skills/audit-project/SKILL.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phases 1–2: layout and manifests
2. Phase 3: README install steps and local install check
3. **Stop and validate**: the plugin installs; this alone proves the distribution path

### Incremental Delivery

1. MVP (US1) → installable plugin
2. US2 → visible, inert workflows
3. US3 → CI guard, changelog, full README
4. Polish → PR

---

## Notes

- [P] tasks touch different files with no unfinished dependencies
- Commit after each phase
- Nothing outside `plugins/project-kit/` may end up in the installed plugin
