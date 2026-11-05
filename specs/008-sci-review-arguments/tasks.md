---

description: "Task list for feature 008: code-review-style arguments for sci-review"
---

# Tasks: Code-review-style arguments for sci-review

**Input**: Design documents from `specs/008-sci-review-arguments/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ (arguments.md, targets-and-parts.md, fix-and-comment.md), quickstart.md

**Tests**: Requested. The plan (Technical Context, Testing) names `tests/test_sci_review_arguments.py` and extensions of `tests/test_sci_review_panel.py` and `tests/test_sci_review_workflow_build.py`; SC-001, SC-002, SC-003, SC-004 and SC-008 are verified by these tests. Test tasks precede the implementation tasks of each story and are expected to fail until that story is implemented.

**Organization**: Tasks are grouped by user story so that each story can be implemented and tested independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: The user story the task belongs to (US1 to US6)
- Every description names the exact file path

## Path Conventions

- Plugin: `plugins/sci-review/` (scripts, skill, runners, workflow)
- Skill directory, abbreviated `SKILL_DIR` below: `plugins/sci-review/skills/scientific-review/`
- Tests: `tests/` at the repository root; fixtures under `tests/fixtures/sci-review/`
- All new entities are frozen dataclasses in `plugins/sci-review/scripts/panel.py`, serialised to JSON in the run directory, never dictionaries passed between functions (user instruction: prefer typed objects)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Governance precondition and test scaffolding.

- [X] T001 Amend the constitution from 1.2.0 to 1.3.0 (MINOR) in `.specify/memory/constitution.md`: (1) add to Principle III the exception, verbatim from plan.md "Required amendment": "Exception: a review command MAY apply its own findings to the working tree without a further confirmation when the user passed an explicit flag requesting it (`--fix`), provided nothing is staged or committed and every change is reported. Passing the flag is the user's explicit acceptance of the risk of writing to a working tree that has uncommitted changes; the command does not require a clean working tree."; (2) add to the third bullet of Principle IV the clarification, verbatim from plan.md "Required amendment" item 2: "The pin rule applies to tools the plugin installs. User-installed clients that the plugin detects and calls (`git`, `gh`, `glab`) are checked for presence and, where a command requires it, a minimum version; they are not pinned."; (3) change the `sci-review` entry of Scope and Constraints to "read-only on the reviewed project, except when the user passes `--fix`, which applies the delivered findings to the working tree after the report"; (4) update the Sync Impact Report header, the version line and "Last Amended: 2026-11-04", stating the reason (feature 008, parity with `/code-review --fix`) and the version class: MINOR, because the amendment adds a bounded exception and neither removes nor redefines Principle III. Make this the first commit of the feature pull request (plan, "Required amendment"). This task is a precondition of every `--fix` task (Phase 8).
- [X] T002 [P] Create `tests/test_sci_review_arguments.py` with a `unittest` module skeleton: imports `panel.py` the same way `tests/test_sci_review_panel.py` does, a helper that creates a temporary run directory, and a helper that sets a temporary preferences path (passed as `--prefs`) so that no test reads or writes the real `~/.config/sci-review/`.
- [X] T003 Add a fixture-repository helper to `tests/test_sci_review_arguments.py` that builds, in a temporary directory, a git repository with a `main` branch, a checked-out feature branch, a second local branch `feature/other` that is not checked out, and a file and directory whose names collide with a branch name (for the ambiguity case of FR-010).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The typed entities, the argument tokeniser and the preferences store that every user story reads.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T004 Add frozen dataclasses to `plugins/sci-review/scripts/panel.py` per data-model.md sections 1 to 4, each with `to_json`/`from_json` methods consistent with the existing entities: `InvocationArguments` (fields `level`: one of `low` | `medium` | `high` | `xhigh` | `max`; `level_source`: `given` | `reused` | `default`; `target_text`: str or null, "The target tokens as typed, unresolved; null means the current branch"; `near_level`: str or null (a near-level token such as `hig`, resolved by `scope`); `comment`: bool; `fix`: bool; `max_findings`: "int >= 1 | `all` | null", "null means the level's default"; `max_findings_source`: `given` | `reused` | `default`; `notes`: list of str; `raw`: str), `Target` (fields `kind`: `pull-request` | `branch` | `paths`; `host`: `github` | `gitlab` | null; `number`: int or null; `ref`: str or null; `paths`: list of str, "each inside the project root"; `text`: str), `UserPreferences` (`version`: int, value 1; `last_level`: level or absent; `last_max_findings`: "int >= 1 | `all` or absent") and `LevelProfile` (`level`, `perspectives`: list of ids or `defaults+extensions` or `all`, `max_perspectives`: "int (2 to 7)", `rebuttal_rounds`: "int (0 to 3)", `max_batches`: "int (1 to 4)", `default_cap`: "int or null", "null means unbounded; null for every level").
- [X] T005 [P] Write grammar-table tests in `tests/test_sci_review_arguments.py` for `panel.py args --argv` (contracts/arguments.md section 1; SC-001, SC-004): each level alone; level in any position; target before level; `--fix`, `--comment` in any position; `--max-findings 5`, `--max-findings=5`, `--max-findings all`, `--max-findings default`, last `--max-findings` wins; leading `#` and backquotes stripped from the target; usage error (exit 2, message names the accepted values, `arguments.json` not written) for an unknown flag such as `--post`, for two levels, for `ultra` (message exactly "`ultra` is the cloud review of /code-review and is not available for the scientific review; use `max`."), and a near-level token such as `hig` recorded as `near_level` with exit 0 (the usage error is raised by `scope`, tested in T019); malformed `--max-findings` (`0`, `zero`, missing value) runs with exit 0 and a note beginning "`--max-findings` was ignored: type a whole number above zero, `all`, or `default` after it."
- [X] T006 Write preference-store tests in `tests/test_sci_review_arguments.py`: missing file treated as empty with a note; unreadable or unwritable directory yields a note and no failure (FR-018); atomic write (temporary file then rename); `prefs --show` and `prefs --clear`; default path resolution `$XDG_CONFIG_HOME/sci-review/preferences.json`, else `~/.config/sci-review/preferences.json`, and `%APPDATA%\sci-review\preferences.json` on Windows (research R4); the path is never inside the project root.
- [X] T007 Implement the tokeniser in `plugins/sci-review/scripts/panel.py` as a pure function `parse_arguments(text: str) -> ParsedArguments` (a frozen dataclass holding the raw tokens before preferences are applied), following contracts/arguments.md section 1 steps 1 to 4 and the divergences of research R3 (level anywhere, two levels and `ultra` are usage errors, unknown `--flag` is a usage error, a near-level token beginning with the first three letters of a level is recorded as `near_level` and kept in the target text, per contracts/arguments.md section 1 step 4).
- [X] T008 Implement the preferences store in `plugins/sci-review/scripts/panel.py`: `preferences_path()`, `load_preferences(path) -> tuple[UserPreferences, list[str]]` and `save_preferences(path, prefs)` with atomic write, per data-model.md section 3 and research R4; never write when `--dry-run` is set.
- [X] T009 Add the `args` subcommand to `plugins/sci-review/scripts/panel.py` with the interface `panel.py args --run RUN (--argv TEXT | --text TEXT) [--persist] [--prefs PATH] [--dry-run]` (contracts/arguments.md section 2): combine `parse_arguments` with the loaded preferences into `InvocationArguments` (the target is stored unresolved as `target_text`), write `$RUN/arguments.json`, print its JSON, exit 0 or 2 (never 3). With `--text`, take only the grammar's tokens from the request text and leave the rest to the natural-language reading of feature 007 (research R9). Log the arguments as the existing subcommands do. Level and cap persistence are wired in T015 and T029.
- [X] T010 Add the `prefs` subcommand to `plugins/sci-review/scripts/panel.py`: `panel.py prefs [--show | --clear] [--prefs PATH] [--dry-run]` (contracts/arguments.md section 3).
- [X] T011 Rewrite section 2 "Arguments" of `SKILL_DIR/SKILL.md`: add `argument-hint: "[low|medium|high|xhigh|max] [<pr#>|<branch>|<path>] [--comment] [--fix] [--max-findings <n>|all|default]"` to the frontmatter (FR-002); state that the skill runs `panel.py args --argv "$ARGUMENTS"` on Claude Code and `panel.py args --text "<request>"` on hosts without an argument field (FR-019); pass `--persist` only when the user typed the arguments or wrote them in the request (research R4); explicit arguments override arguments inferred from wording, and feature 007's natural-language arguments still apply where no explicit argument covers them (FR-004); on exit 2, show the usage message and run nothing; tell the user each entry of `notes` in one short line as the review begins (contracts/arguments.md section 5 rule 2).

**Checkpoint**: `panel.py args` parses every form of the grammar table; preferences can be read and written outside the project.

---

## Phase 3: User Story 1 - Select the review depth with an effort level (Priority: P1) MVP

**Goal**: `/sci-review:scientific-review <level>` runs the panel configuration of that level, the level persists, and the report states the level and the panel used.

**Independent Test**: Invoke the review at each of the five levels on the same fixture branch and confirm that the panel recorded in `panel.json` and the report matches the level profile; invoke with no arguments and no preferences and confirm the feature 007 defaults.

### Tests for User Story 1

- [X] T012 [P] [US1] Write level-profile tests in `tests/test_sci_review_arguments.py` (SC-002, SC-003): for each level, `panel.py panel --level LEVEL` writes a `panel.json` matching the table of contracts/arguments.md section 4; no parameter of `LevelProfile` decreases from `low` to `max` (FR-005); `medium` equals the feature 007 defaults (five default perspectives plus selected extensions, 2 rebuttal rounds, 2 debate batches) (FR-006); `--rounds 1` with `--level high` yields 1 round and records `rounds` in `overrides` (spec edge case).
- [X] T013 [US1] Write level-persistence tests in `tests/test_sci_review_arguments.py`: `args --argv xhigh --persist` stores `last_level`; a later `args --argv ""` yields `level: xhigh`, `level_source: reused` and a note; no persisted level yields `medium`, `default`; without `--persist` nothing is stored (FR-007).

### Implementation for User Story 1

- [X] T014 [US1] Add the constant `LEVEL_PROFILES: dict[str, LevelProfile]` to `plugins/sci-review/scripts/panel.py` with the values of research R6: `low` = `theorist`, `numerical-analyst`, `methodologist`, 1 round, 1 batch; `medium` = five defaults plus selected extensions (at most 7), 2 rounds, 2 batches; `high` = as `medium`, 2 rounds, 3 batches; `xhigh` = as `medium`, 3 rounds, 4 batches; `max` = all defaults and selected extensions (at most 7), 3 rounds, 4 batches; `default_cap` is null (unbounded) for every level. Keep feature 007's clamping limits (2 to 7 perspectives, 0 to 3 rounds, 1 to 4 batches).
- [X] T015 [US1] Wire level resolution and persistence into `cmd_args` in `plugins/sci-review/scripts/panel.py`: given level becomes `given` and, with `--persist` (passed only when the user typed the arguments or wrote them in the request, never when the model starts a review on its own initiative, FR-007), is stored as `last_level`; otherwise reuse `last_level` (`reused`, with a note) or use `medium` (`default`).
- [X] T016 [US1] Extend `cmd_panel` in `plugins/sci-review/scripts/panel.py` with `--level LEVEL` (default: read `level` from `$RUN/arguments.json` when present, else `medium`): apply the profile first, then the existing `--perspectives`, `--rounds`, `--batches` options as overrides recorded in a new `overrides` list; add the fields `level`, `level_source`, `overrides` and `parts` (integer, 1 until US4 sets it), and no finding-cap field, to the `Panel` dataclass and `panel.json` (data-model.md section 5).
- [X] T017 [US1] Add `level`, `level_source` and `notes` to the report in `plugins/sci-review/scripts/panel.py` (`cmd_report`) and to `SKILL_DIR/schemas/report.schema.json`; the Markdown report states "Effort level: <level> (<given|reused|default>)" and the panel actually used after overrides (FR-009).
- [X] T018 [US1] Update `SKILL_DIR/SKILL.md` section 5 "Opening steps" to pass the resolved level to `panel.py panel`, and add to the skill `description` in the frontmatter, verbatim: "Use the max level only when the user, or instructions such as CLAUDE.md or a skill, explicitly ask for it, never on your own judgment: it is the costliest level and starts many reviewer agents." Repeat the rule in section 8 "Rules" (FR-008).

**Checkpoint**: User Story 1 is fully functional and testable on its own; a review with no arguments behaves exactly as feature 007.

---

## Phase 4: User Story 2 - Name the target: pull request, branch or path (Priority: P1)

**Goal**: A pull request number, `#n`, a pull request URL, a branch name or paths resolve to the correct scope without checking anything out.

**Independent Test**: On the fixture repository of T003, invoke the review with each target form and confirm the scope recorded in `scope.json` and the report; confirm `git status --porcelain --ignored` and the current branch are unchanged.

### Tests for User Story 2

- [X] T019 [P] [US2] Write target-resolution tests in `tests/test_sci_review_arguments.py` using the T003 fixture (contracts/targets-and-parts.md section 1): `feature/other` resolves to `kind: branch` with that branch as head and the working tree, index and current branch unchanged (FR-011); an existing path resolves to `kind: paths`; several paths are accepted; a token that is both a path and a branch exits 3 with `{"ambiguous": [...]}`; a path outside the project root exits 2; a `near_level` token `hig` exits 2 with "`hig` is not a recognised level: use low, medium, high, xhigh or max." when no branch or path has that name, and resolves as a target when a branch `hig` exists (FR-003); `hig src/` with no branch or path `hig` also exits 2 with that message; the resolved `Target` is written to `scope.json`, never to `arguments.json`; a number with `gh` absent from `PATH` exits 3 with `{"missing": "gh"}` (FR-012); `#12`, `12` and `https://github.com/o/r/pull/12` all classify as `pull-request` on GitHub; `!12` and a `/-/merge_requests/12` URL classify as GitLab.
- [X] T020 [US2] Write a test in `tests/test_sci_review_arguments.py` that `panel.py clean` deletes every ref under `refs/sci-review/` in the fixture repository.

### Implementation for User Story 2

- [X] T021 [US2] Implement `classify_target(text: str, project_root: Path) -> Target | Ambiguous` in `plugins/sci-review/scripts/panel.py` per the table of contracts/targets-and-parts.md section 1: whole number, `#n` or GitHub pull URL to GitHub `pull-request`; `!n`, `/-/merge_requests/n` URL, or a number when `origin` is a GitLab remote, to GitLab `pull-request`; an existing local or remote branch to `branch`; existing paths inside the project root to `paths`; more than one match returns an `Ambiguous` dataclass listing the kinds.
- [X] T022 [US2] Implement pull request resolution in `plugins/sci-review/scripts/panel.py`: detect `gh` or `glab` and authentication; read base and head with `gh pr view <n> --json baseRefOid,headRefOid` (or `glab mr view`); fetch the head with `git fetch origin pull/<n>/head:refs/sci-review/pr-<n>` (GitLab: `merge-requests/<n>/head`); scope is the diff from the merge base of base and head to that ref; for a merged pull request use the base commit at the time of merge (spec edge case). On failure exit 3 with `{"missing": "gh" | "glab" | "auth" | "network"}`.
- [X] T023 [US2] Extend `cmd_scope` in `plugins/sci-review/scripts/panel.py` with `--target TEXT` (default: `target_text` of `$RUN/arguments.json`): resolve each target token separately; when a token equals `near_level` and is neither an existing branch nor an existing path, exit 2 with the usage error of contracts/arguments.md section 1 step 4, whatever the other tokens are; dispatch to branch, paths or pull request resolution without checkout; add `target` (`Target` or null) and `pull_request_ref` (temporary ref or null) to the `ReviewScope` dataclass and `scope.json` (data-model.md section 6); a branch that has not diverged from its base keeps feature 007's handling (ask for a baseline or another mode).
- [X] T024 [US2] Extend `cmd_clean` in `plugins/sci-review/scripts/panel.py` to delete every ref under `refs/sci-review/` with `git update-ref -d`.
- [X] T025 [US2] Update `SKILL_DIR/SKILL.md` section 5 to pass `--target`, and to handle exit 3: for `ambiguous`, ask the user which kind was meant; for `missing`, say what is missing and offer a branch or paths review, never switching silently (FR-010, FR-012); exit 2 for a path outside the project is a usage error and nothing runs. The report names the pull request or branch reviewed.
- [X] T026 [US2] Update the scope rules in `SKILL_DIR/protocol.md` section 10 "Written fallback rules" with the target-resolution rules of contracts/targets-and-parts.md section 1, for runners that apply the protocol without `panel.py`.

**Checkpoint**: User Stories 1 and 2 work independently; every target form resolves without changing the working tree.

---

## Phase 5: User Story 3 - Cap the number of reported findings (Priority: P2)

**Goal**: `--max-findings <n>|all|default` limits the delivered findings in report order, persists until `default`, and the report states the cap and the withheld count.

**Independent Test**: Using the adjudicated messages fixture with at least eight findings, run `panel.py report` with caps 5, `all` and `default`, and compare delivered and withheld counts.

### Tests for User Story 3

- [X] T027 [P] [US3] Write cap tests in `tests/test_sci_review_arguments.py`: with eight adjudicated findings and cap 5, `report.json` holds the top five in report order (consensus, majority, contested; within each high, medium, low) and `withheld: 3`; `all` delivers eight and `withheld: 0`; `default` applies the level's default cap, which is unbounded (eight delivered, `withheld: 0`); with no argument and no preference all findings are delivered, as in feature 007 (FR-006); delivery through the findings-reporting tool is clamped to 32 whatever the cap (research R3 step 5); withheld findings remain in the run directory.
- [X] T028 [US3] Write cap-persistence tests in `tests/test_sci_review_arguments.py`: `--max-findings 5 --persist` stores `last_max_findings: 5`; a later run without the flag yields `max_findings: 5`, `max_findings_source: reused` and a note that ends "passing `--max-findings default` goes back to the usual limit"; `--max-findings default --persist` removes `last_max_findings`; a malformed value leaves the stored cap unchanged and applies it (FR-003a); without `--persist` nothing is stored (FR-014).

### Implementation for User Story 3

- [X] T029 [US3] Wire cap resolution and persistence into `cmd_args` in `plugins/sci-review/scripts/panel.py`: `<n>` (n at least 1) or `all` given becomes `given` and, with `--persist`, is stored as `last_max_findings`; `default` clears it and yields `max_findings: null`, `default`; otherwise reuse the stored value (`reused`, with note) or `null`, `default`; a malformed value adds the FR-003a note, followed by "Using the usual limit." when no cap is persisted.
- [X] T030 [US3] Apply the cap in `cmd_report` in `plugins/sci-review/scripts/panel.py`: truncate `report_findings` to the resolved cap (or the level's `default_cap` when `max_findings` is null, which is unbounded; no limit for `all`), add `max_findings` and `withheld` (int) to `report.json` and the Markdown report, keep all adjudicated findings in the run directory (FR-013, FR-014); update `SKILL_DIR/schemas/report.schema.json` accordingly.
- [X] T031 [US3] Update `SKILL_DIR/SKILL.md` section 7 "Closing steps" so that delivery states the cap applied and the number withheld, and clamps delivery through the findings-reporting tool to 32 with the line "This review reports at most 32 findings, so the limit is 32 here." when the resolved cap is larger than 32 or unbounded (research R3).

**Checkpoint**: The cap works with any level and any target.

---

## Phase 6: User Story 4 - Review the whole scope, however large (Priority: P2)

**Goal**: The 6,000-line budget is removed; large scopes are divided into review parts of at most 2,000 lines, each reviewed by every perspective, merged before the debate, with confirmation above 6,000 lines.

**Independent Test**: Run `panel.py scope` and `panel.py parts` on the 18,000-line fixture and confirm that no file is excluded for size, that 9 parts cover every line and that `confirm_required` is true; run the full review and confirm the defect in the last file is reported (quickstart scenario 10).

### Tests for User Story 4

- [X] T032 [P] [US4] Create the fixture `tests/fixtures/sci-review/large-scope/` with about 18,000 reviewable lines of Python split over several directories, one file larger than 2,000 lines with top-level `def`/`class` boundaries, and one seeded scientific defect (for example a unit conversion error with a stated failure scenario) in the last file in path order; add a `README.md` in the fixture stating the defect and its expected finding, so that the score helper of feature 007 can match it.
- [X] T033 [P] [US4] Extend `tests/test_sci_review_panel.py`: no scope contains the exclusion reason "over budget"; `scope --budget` is rejected as an unknown option; the scope note no longer mentions a budget; `merge` clusters candidates from `candidates/<perspective>--p1.json` and `candidates/<perspective>--p2.json` on the same location into one finding (FR-021).
- [X] T034 [P] [US4] Write part-division tests in `tests/test_sci_review_arguments.py` on the T032 fixture (SC-008): every reviewable line belongs to exactly one part; each part has at most 2,000 lines unless it holds a single indivisible definition; files of the same directory share a part where they fit; the oversized file is split at definition boundaries; part ids are `p1`, `p2`, ... in path order; `parts.json` records `threshold: 6000`, `total_lines` and `confirm_required: true`; a scope of 2,000 lines or fewer yields one part and `confirm_required: false`.
- [X] T035 [US4] Write a test in `tests/test_sci_review_arguments.py` that `SKILL_DIR/SKILL.md` states that a review started on the model's own initiative always asks for confirmation when `confirm_required` is true (FR-022), by asserting the presence of that sentence as written by T049.
- [X] T036 [P] [US4] Extend `tests/test_sci_review_workflow_build.py` with a parity check that the generated `plugins/sci-review/workflows/scientific-review.js` runs the independent round over perspective x part, writes `candidates/<perspective>--<part>.json`, and writes no part status (status is derived by `report`).

### Implementation for User Story 4

- [X] T037 [US4] Remove the review budget from `plugins/sci-review/scripts/panel.py`: delete `DEFAULT_BUDGET`, the `--budget` option of `scope`, the "over budget" exclusion and its sentence in the scope note (FR-020; contracts/targets-and-parts.md section 1 "Removed"); add `total_lines` (int) to `ReviewScope` and `scope.json`.
- [X] T038 [US4] Add the `ReviewPart` dataclass to `plugins/sci-review/scripts/panel.py` (data-model.md section 7: `id`: str, "`p1`, `p2`, ... in path order"; `files`: list of `ScopedFile` "with `line_ranges` narrowed when a file is split"; `lines`: int, "At most 2,000 unless a single indivisible definition is larger"; `status`: `pending` | `reviewed` | `incomplete`) and a `ReviewParts` container with `threshold` (6,000), `total_lines` and `confirm_required` (`total_lines > threshold`); define the constants `PART_LINES = 2000` and `LARGE_SCOPE_THRESHOLD = 6000`.
- [X] T039 [US4] Implement `divide_into_parts(scope: ReviewScope) -> ReviewParts` in `plugins/sci-review/scripts/panel.py` (research R7 step 2): group files by directory in path order; fill parts up to 2,000 lines; split a file larger than one part at top-level definition boundaries (Python `def`/`class`, TypeScript and JavaScript `function`/`class`/`export`, notebook cells), falling back to fixed line windows; in branch mode count changed lines.
- [X] T040 [US4] Add the `parts` subcommand to `plugins/sci-review/scripts/panel.py`: `panel.py parts --run RUN [--dry-run]` reads `scope.json`, writes `parts.json` and prints one summary line with total lines, files, parts and whether confirmation is required (contracts/targets-and-parts.md section 2); write the number of parts into `panel.json` `parts`.
- [X] T041 [US4] Update candidate handling in `plugins/sci-review/scripts/panel.py`: candidate files are named `candidates/<perspective>--<part>.json` (the path template near the `"candidates/{}.json"` format string), candidate messages carry `part`, `ingest` and `validate` accept the new names, and `merge` reads the candidates of all parts in one pass; add `part` to `SKILL_DIR/schemas/candidate-findings.schema.json`.
- [X] T042 [US4] In `cmd_report` in `plugins/sci-review/scripts/panel.py`, derive each part's status identically on every runner: `reviewed` when the candidate file `candidates/<perspective>--<part>.json` of every panel perspective exists and validates, `incomplete` otherwise (data-model.md section 7); no runner writes part status. Add `parts` (int) and the list of `incomplete` parts to the report and to `SKILL_DIR/schemas/report.schema.json`; every incomplete part is listed under Not reviewed with its reason (FR-023). Add a test of the derivation to `tests/test_sci_review_panel.py` (one missing candidate file yields one incomplete part).
- [X] T043 [US4] Update `plugins/sci-review/scripts/build_workflow.py` so that the generated independent round runs `parallel` over every perspective x part pair, passes each reviewer its part and permission to read other project files to follow a reference, and writes `candidates/<perspective>--<part>.json` (a failed agent writes nothing, so `report` derives the part as `incomplete`); regenerate `plugins/sci-review/workflows/scientific-review.js` with the script.
- [X] T044 [P] [US4] Update the independent round of `SKILL_DIR/runners/claude-agents.md` and `SKILL_DIR/runners/codex-subagents.md`: one agent per perspective x part, in batches no larger than the host's concurrency limit (research R8).
- [X] T045 [P] [US4] Update the independent round of `SKILL_DIR/runners/sequential.md`: parts in order, each perspective completing all parts before the next perspective starts (feature 007 FR-028 independence order).
- [X] T046 [P] [US4] Update `SKILL_DIR/runners/claude-workflow.md` to describe the part loop of the regenerated workflow.
- [X] T047 [US4] Update `SKILL_DIR/protocol.md`: remove the line-budget sentence from the scope rule in section 10; add the part-division rule and the per-part independent round to sections 2 "Phases" and 6 "Limits", including the bound of P x K independent-round invocations (research R7 "Cost").
- [X] T048 [US4] Update the reviewer inputs for review parts: in `plugins/sci-review/agents/scientific-auditor.md` rule 2 and `SKILL_DIR/codex-agents/sci-review-panelist.toml`, state that a perspective reviewer receives one review part (its files and line ranges from `parts.json`), reviews every line of it, and may read any file of the reviewed project, inside or outside the scope, to follow a reference, while raising findings only on lines of its part; update the Independent round row of `SKILL_DIR/protocol.md` section 3 "Role inputs" with the part as input and the candidate file name `candidates/<perspective>--<part>.json` (spec edge case on evidence spanning two parts).
- [X] T049 [US4] Update `SKILL_DIR/SKILL.md`: remove the `--budget N` paragraph of section 5 and "over budget" from section 7 step 5; add an opening step after `scope` that runs `panel.py parts` and, when `confirm_required` is true, says "This scope has <L> lines in <F> files and will be reviewed in <K> parts. Continue?" before any reviewer runs, running nothing and offering named paths on refusal; add the sentence "A review started on your own initiative always asks before a scope that requires confirmation." (FR-022, tested by T035); the reply names any incomplete part.

**Checkpoint**: A scope of any size is reviewed in full; scopes of 6,000 lines or fewer run without a prompt and with the same findings as feature 007 (SC-009).

---

## Phase 7: User Story 5 - Post findings as pull request comments (Priority: P3)

**Goal**: With `--comment` and a pull request target, each delivered finding is posted as an inline comment (GitHub) or all findings as one note (GitLab), as `/code-review --comment` does.

**Independent Test**: Run quickstart scenario 6 on a throwaway GitHub pull request and scenario 7 on a branch; compare posted comments with delivered findings.

### Tests for User Story 5

- [X] T050 [P] [US5] Write a test in `tests/test_sci_review_arguments.py` that `SKILL_DIR/SKILL.md` contains the line "Reproduced from /code-review, Claude Code 2.1.317" and, verbatim, every non-adapted line of the "Posting to GitHub (--comment)" and "Posting to GitLab (--comment)" blocks of contracts/fix-and-comment.md sections 1 and 2 (research R10).

### Implementation for User Story 5

- [X] T051 [US5] Add to `SKILL_DIR/SKILL.md`, after the delivery step of section 7 and under the citation "Reproduced from /code-review, Claude Code 2.1.317", the section "Posting to GitHub (--comment)", included when `arguments.json` has `comment: true` and the target host is not GitLab, with the text of contracts/fix-and-comment.md section 1, including both **[adapted]** sentences (agreement label, severity and dimension in each comment; an unanchorable finding printed with a note; nothing posted when there are no findings).
- [X] T052 [US5] Add to `SKILL_DIR/SKILL.md` the section "Posting to GitLab (--comment)", included when `comment: true` and the target host is GitLab, with the verbatim text of contracts/fix-and-comment.md section 2.
- [X] T053 [US5] State in `SKILL_DIR/SKILL.md` section 7 the order of the closing steps: deliver, then post (`--comment`), then fix (`--fix`), then clean; a posting failure never suppresses the local report and is reported with its reason (FR-015); `--comment` without a pull request target prints the findings and notes that `--comment` was ignored (FR-003b).

**Checkpoint**: `--comment` works on GitHub and GitLab pull request targets and is ignored with a note elsewhere.

---

## Phase 8: User Story 6 - Apply fixes after the review (Priority: P3)

**Goal**: With `--fix`, the user's session model applies each delivered finding to the working tree after the report, skips those it should not apply, runs the relevant checks and reports each finding again with its outcome, as `/code-review --fix` does.

**Independent Test**: Run quickstart scenario 9 on a fixture branch with one seeded defect; inspect the working-tree diff (nothing staged), the checks run and the outcome of each finding.

**Depends on**: T001 (constitution amendment).

### Tests for User Story 6

- [X] T054 [P] [US6] Write a test in `tests/test_sci_review_arguments.py` that `SKILL_DIR/SKILL.md` contains, verbatim, every non-adapted line of the "Applying fixes (--fix)", "If findings are fixed later" and outcome-lines blocks of contracts/fix-and-comment.md sections 3, 4 and 5, both variants of the `--fix` ending (with and without the findings-reporting tool), and no `/verify` hand-off (section 6).

### Implementation for User Story 6

- [X] T055 [US6] Add to `SKILL_DIR/SKILL.md`, after the posting sections, the section "Applying fixes (--fix)", included when `arguments.json` has `fix: true`, with the text of contracts/fix-and-comment.md section 3: "every delivered finding"; the three skip conditions; "Skipping a finding never changes its agreement label."; "Run the relevant checks after."; the `ReportFindings` variant (outcomes `fixed`, `no_change_needed`, `skipped`, no text repetition, one line per skipped finding) and the variant without the tool ("Finish with a brief summary of what was fixed and what was skipped.").
- [X] T056 [US6] Add the constraints around the fix section to `SKILL_DIR/SKILL.md` (contracts/fix-and-comment.md section 3, constraints 1 to 4): nothing is staged or committed; the project check of section 7 step 3 runs before the fix step; only delivered findings (after `--max-findings`) are considered; the fixes are made by the orchestrating conversation with the host's own editing tools, and no agent, perspective reviewer or other panel member is started for them (FR-016, FR-016a); no clean-working-tree check is made, because passing `--fix` is the user's explicit acceptance of that risk (constitution 1.3.0; contracts/fix-and-comment.md section 3 constraint 5); without `--fix`, the review is read-only (FR-016e).
- [X] T057 [US6] Add to `SKILL_DIR/SKILL.md` the section "If findings are fixed later", included whenever the findings-reporting tool is available, with or without `--fix` (contracts/fix-and-comment.md section 4, FR-016d), and the outcome-lines sentence of section 5, appended when findings are delivered as a message.
- [X] T058 [US6] Add the `FindingOutcome` shape (data-model.md section 8: `finding_id`: str; `outcome`: `fixed` | `no_change_needed` | `skipped`; `reason`: str, "Required for `skipped`"; `files`: list of str) to the delivery instructions of `SKILL_DIR/SKILL.md` section 7, stating that `panel.py` never writes outcomes and that the agreement label never changes.
- [X] T059 [US6] Replace the read-only statement in the introduction of `SKILL_DIR/SKILL.md` ("The review is read-only: it never creates, modifies or deletes a file in the reviewed project (FR-006).") with the narrowed guarantee: read-only except the closing `--fix` step, which edits the working tree after the report and stages or commits nothing (constitution 1.3.0, spec FR-016e).

**Checkpoint**: All six user stories are functional; `--fix` is the only path that writes to the project.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, versioning, cross-references and validation across all stories.

- [X] T060 [P] Update `plugins/sci-review/README.md`: document the grammar and argument hint, the five level profiles (table of contracts/arguments.md section 4), the three target forms, `--max-findings` and its persistence, the preferences file location and `panel.py prefs`, `--comment`, `--fix` and its exception to the read-only rule; replace the "Line budget | 6,000 lines" row with the review-part size (2,000 lines) and the large-scope threshold (6,000 lines, confirmation); remove "over budget" from the Not reviewed list; add a maintenance item to re-read the reproduced `/code-review` sections from the current Claude Code binary before each release (research R10).
- [X] T061 [P] Add a pointer at the top of section 2 of `specs/007-sci-review-plugin/contracts/invocation.md` and of the `scope` section of `specs/007-sci-review-plugin/contracts/panel-cli.md` to the 008 contracts, stating that explicit arguments and the removal of the budget are specified there.
- [X] T062 [P] Bump the `sci-review` version from 0.1.0 to 0.2.0 in `plugins/sci-review/.claude-plugin/plugin.json` and `plugins/sci-review/.codex-plugin/plugin.json` (the marketplace manifest records no plugin version).
- [X] T063 [P] Add `[Unreleased]` entries to `CHANGELOG.md` (Keep a Changelog, formal register, no em-dashes): Added (effort levels, targets, `--max-findings`, `--comment`, `--fix`, review parts and the large-scope confirmation), Changed (constitution 1.3.0, `sci-review` no longer read-only under `--fix`), Removed (the 6,000-line budget and `--budget`).
- [X] T064 Run `python3 -m unittest tests.test_sci_review_arguments tests.test_sci_review_panel tests.test_sci_review_workflow_build tests.test_sci_review_score` and the repository's full test suite; fix any failure in the files named by the failing tests.
- [X] T065 Run `claude plugin validate plugins/sci-review` and validate the `project-kit` plugin the same way; run `python3 plugins/sci-review/scripts/build_workflow.py --check` to confirm `plugins/sci-review/workflows/scientific-review.js` matches the skill files.
- [ ] T066 Verify SC-009: build the feature 007 seeded fixture with `python3 tests/fixtures/sci-review/seeded-repo/build.py --out <dir>`, run the review on its `feature` branch at `medium` with no other argument, score the run with `python3 tests/fixtures/sci-review/seeded-repo/score.py`, and compare the seeded defects found with the baseline of `specs/007-sci-review-plugin/validation.md` (SC-001 recall: 11 of 11 seeded defects); record both counts in `specs/008-sci-review-arguments/validation.md` and treat any decrease as a failure to fix before release.
- [ ] T067 Execute the manual scenarios 1 to 11 of `specs/008-sci-review-arguments/quickstart.md` with the plugin installed from this worktree and `XDG_CONFIG_HOME` set to a temporary directory; after each scenario except 9, compare `git status --porcelain --ignored` with the prior state (SC-005); record the results, with dates and observed outputs, in a new `specs/008-sci-review-arguments/validation.md`.
- [ ] T068 Run the cross-host check of `specs/008-sci-review-arguments/quickstart.md` section 4 (Codex request text with a level and a cap; claude.ai preferences notice) and append the results to `specs/008-sci-review-arguments/validation.md`.

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (Phase 1)**: no dependencies. T001 must be complete before Phase 8.
- **Foundational (Phase 2)**: depends on T002 for the test file; blocks every user story.
- **US1 (Phase 3)** and **US2 (Phase 4)**: depend only on Phase 2; independent of each other.
- **US3 (Phase 5)**: depends on Phase 2; uses `LevelProfile.default_cap` from T014 (US1) for the `default` cap. If US3 is built before US1, treat the default cap as unbounded, which is the value T014 sets.
- **US4 (Phase 6)**: depends on Phase 2 only; touches `scope`, `merge`, the runners and the workflow builder, none of which US1 to US3 change, except `cmd_report` and `report.schema.json` (sequence T042 after T017 and T030 when stories run concurrently).
- **US5 (Phase 7)**: depends on US2 (pull request target) for its independent test.
- **US6 (Phase 8)**: depends on T001 and on the delivery step of US3 (only delivered findings are fixed).
- **Polish (Phase 9)**: depends on all user stories to be included.

### Shared-file sequencing

`plugins/sci-review/scripts/panel.py` and `SKILL_DIR/SKILL.md` are edited by most stories. Tasks on the same file are not marked [P] and run in task-ID order within a story; this includes the test tasks that share `tests/test_sci_review_arguments.py`, of which at most one per phase carries [P]; across concurrently developed stories, merge edits to these two files one story at a time.

### Within each story

Tests first (they fail), then dataclasses and pure functions, then subcommands, then `SKILL.md` and runner text.

## Parallel Examples

### Phase 2

```text
T005 grammar-table tests (tests/test_sci_review_arguments.py)  |  T008 preferences store (panel.py, after T004)   (T006 follows T005 in the same file)
```

### User Story 1

```text
T012 level-profile tests (tests/test_sci_review_arguments.py)  |  T014 level profiles (panel.py) once T012 is written
```

### User Story 4

```text
T032 large-scope fixture  |  T033 panel tests  |  T034 part-division tests  |  T036 workflow parity test   (T035 follows T034 in the same file)
T044 claude-agents and codex-subagents runners  |  T045 sequential runner  |  T046 claude-workflow runner
```

### Polish

```text
T060 README  |  T061 007 contract pointers  |  T062 version bump  |  T063 CHANGELOG
```

## Implementation Strategy

### MVP (User Story 1)

1. Phase 1. T001 is the first commit of the feature pull request.
2. Phase 2.
3. Phase 3. Validate with quickstart scenarios 1 and 2 and the level-profile tests (SC-002, SC-003). A review with no arguments must remain identical to feature 007.

### Incremental delivery

1. MVP: levels (US1).
2. Targets (US2): pull requests and branches without checkout.
3. Finding cap (US3) and full-scope review (US4), independently.
4. `--comment` (US5), then `--fix` (US6) after the constitution amendment.
5. Polish, version 0.2.0 and the `sci-review-v0.2.0` release.

### Notes

- Every new `panel.py` subcommand that writes (`args`, `prefs`, `parts`) accepts `--dry-run` (Principle II).
- No task writes into a reviewed project except the `--fix` prompt section executed by the orchestrating conversation.
- Commit after each task or logical group; stop at each checkpoint to validate the story independently.
