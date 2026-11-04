---

description: "Task list for the sci-review plugin"
---

# Tasks: sci-review plugin

**Input**: Design documents from `specs/007-sci-review-plugin/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included. plan.md (Technical Context, Testing) requires `unittest` coverage of `scripts/panel.py` with message fixtures and golden reports, a drift test for the generated Workflow script, manifest checks, and a seeded fixture repository scored by `score.py`. It also requires a Node.js parity test for the Workflow script's pure section and reproduction checks for SC-007. Test tasks are written before the implementation they cover within each phase.

**Organization**: Tasks are grouped by user story so that each story can be implemented and verified independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task).
- **[Story]**: The user story the task belongs to (US1 to US6).
- Every task names the file it creates or changes.

## Path Conventions

- Paths are relative to the repository root unless stated otherwise.
- `SKILL_DIR` denotes `plugins/sci-review/skills/scientific-review/`.
- Paths beginning `idfkit-plugin/` are relative to the separate idfkit plugin checkout at `/Users/samueld/PycharmProjects/idfkit-workspace/idfkit-plugin`. Those tasks are committed and released through that repository's own process (spec.md, Dependencies).
- `scripts/panel.py` uses the Python 3.10 standard library only, frozen `dataclasses` for every entity (no dictionaries passed between functions), and string-constant enumerations validated on load (data-model.md, section 1).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Constitution amendment and the plugin skeleton. The amendment is a precondition of the plan's Constitution Check.

- [X] T001 Amend the constitution (MINOR bump from 1.1.1 to 1.2.0) in `.specify/memory/constitution.md`: widen the repository scope to a marketplace of plugins; replace the sentence stating that the plugin "lives under `plugins/project-kit/`" with one stating that each plugin lives under `plugins/<name>/`; record `sci-review`'s scope (scientific-correctness review, read-only, on Claude and Codex); state that Principle I does not apply to `sci-review` while Principles II to IV do; add the per-plugin release-tag rule `sci-review-vX.Y.Z`; update the Sync Impact Report header
- [X] T002 Create the plugin directory tree of plan.md (Project Structure) with empty placeholder directories `plugins/sci-review/skills/scientific-review/{roles,dimensions,schemas,runners,codex-agents}/`, `plugins/sci-review/agents/`, `plugins/sci-review/workflows/`, `plugins/sci-review/scripts/`, and `tests/fixtures/sci-review/{messages,seeded-repo,test-extension-plugin}/`
- [X] T003 [P] Create the Claude manifest `plugins/sci-review/.claude-plugin/plugin.json` with `name: "sci-review"`, `version: "0.1.0"`, a description limited to scientific-correctness review (mathematics, numerics, physical modelling and units, statistics, algorithms; no style or lint), author and repository fields copied from `plugins/project-kit/.claude-plugin/plugin.json`
- [X] T004 [P] Create the Codex manifest `plugins/sci-review/.codex-plugin/plugin.json` with the same `name` and `version` as T003, `skills: "./skills/"`, and an `interface` block (display name, short description, category), following the pattern of `idfkit-plugin/.codex-plugin/plugin.json` (research R11)
- [X] T005 [P] Confirm that `ruff check` and `ruff format --check` with the existing `ruff.toml` cover `plugins/sci-review/scripts/` and `tests/test_sci_review_*.py`, and leave `target-version = "py39"` unchanged repository-wide (it governs only upgrade suggestions); enforce the Python 3.10 minimum at run time with a version check at the top of `plugins/sci-review/scripts/panel.py` and `plugins/sci-review/scripts/build_workflow.py` that exits with code 3 and a message

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The single protocol source (protocol, schemas, data model) and the `panel.py` core that every runner and every story uses.

**CRITICAL**: No user-story work begins until this phase is complete.

- [X] T006 Write `SKILL_DIR/protocol.md`: the three phases of FR-023 (independent round, debate, adjudication), with adjudication run as moderator notes followed by label computation in `panel.py`; the role inputs table of contracts/panel-messages.md section 1 verbatim; severity definitions of FR-018 verbatim ("High: produces a wrong result under realistic inputs; Medium: produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result; Low: a latent risk that does not currently produce a wrong result"); the definition of a member's stance as its latest position, carried forward when it is not called again; the six adjudication rules of data-model.md section 3 in order, with the majority denominator (every perspective reviewer, default and domain, the raiser included, never the defender); the debate stop rule (a batch stops when no stance changed in a round; settled members are not called again); limits "panel size 2 to 7 perspectives, counting domain perspectives; a request for more than are available yields all of them", "rebuttal rounds 0 to 3, default 2", "max_batches 1 to 4, default 2"; the clustering rule "same file, line ranges within three lines" (research R7); and a "Written fallback rules" section describing how to perform each `panel.py` step by hand when `python3` is absent (contracts/invocation.md section 5)
- [X] T007 [P] Write `SKILL_DIR/schemas/candidate-findings.schema.json` (JSON Schema draft 2020-12, `additionalProperties: false` at every object level): `{perspective: string, findings: [CandidateFinding], checked_items: [CheckedItem], notes: string}`; CandidateFinding fields `id` (pattern `^[a-z0-9-]+-[0-9]+$`), `raised_by`, `file`, `line_start` (integer >= 1), `line_end` (integer >= `line_start`, checked by panel.py), `dimension` (enum of the five Dimension values), `severity` (enum `high`, `medium`, `low`), `summary`, `trigger` (string or null), `wrong_output` (string or null), `fix`, `evidence`; CheckedItem fields `file`, `line_start`, `line_end`, `dimension`, `note`
- [X] T008 [P] Write `SKILL_DIR/schemas/merge-ruling.schema.json` (`additionalProperties: false`): `{batch: integer, findings: [MergedFinding], split: [{cluster: string, reason: string}]}`; MergedFinding fields `id` (pattern `^F[0-9]+$`), `members` (`minItems: 1`, candidate ids), `raised_by` (`minItems: 1`), `batch`, the FR-014 representative fields (`file`, `line_start`, `line_end`, `dimension`, `severity`, `summary`, `trigger`, `wrong_output`, `fix`), and optional `severity_reason` (required by the semantic checks of panel.py when severity is lower than the highest member severity)
- [X] T009 [P] Write `SKILL_DIR/schemas/debate-positions.schema.json` (`additionalProperties: false`): `{member: string, round: integer >= 0, positions: [Position]}`; Position fields `finding_id`, `member`, `round`, `stance` (enum `accept`, `challenge`, `withdraw`), `reason` (string, `minLength: 1`), `answers` (array of position ids)
- [X] T010 [P] Write `SKILL_DIR/schemas/moderator-notes.schema.json` (`additionalProperties: false`): `{batch: integer, notes: [ModeratorNote]}`; ModeratorNote fields `finding_id`, `argument_for`, `argument_against` (strings, `minLength: 1`), `deciding_assumption` (string or null), `rejection_reason` (string, `minLength: 1`), `no_trigger_reason` (string or null) (data-model.md, ModeratorNote)
- [X] T011 [P] Write `SKILL_DIR/schemas/report.schema.json` (`additionalProperties: false`) for ReviewReport of data-model.md section 2: `scope`, `panel` (with `runner` enum `claude-workflow`, `codex-subagents`, `claude-agents`, `sequential` and `independent` boolean), `extensions` (status enum `selected`, `not-applicable`, `failed`, `recommended`, with `status_reason` required through `if`/`then` for all but `selected`), `findings` (each with `label` enum `consensus`, `majority`, `contested`; through `if`/`then`, `argument_for`, `argument_against`, `deciding_assumption` required when `label` is `contested`, `deciding_assumption` nullable; `trigger` and `wrong_output` non-null when `label` is `consensus` or `majority`; `no_trigger_reason` present when either is null), `rejected`, `checked_items`, `unreviewed`, `notices`
- [X] T012 Write unit tests for the data model, validator and file-writing safety in `tests/test_sci_review_panel.py` (class `TestModelAndValidate`): load each schema; valid fixtures pass; each of these fails with exit code 1 and a named error: unknown property, `line_end < line_start`, unknown dimension, empty `members` (`minItems`), empty `reason` (`minLength`), contested finding without `argument_for` (`if`/`then`), consensus finding with null `trigger`; `init --dry-run` and `clean --dry-run` print the path and leave the file system unchanged; `init --project P` refuses a run directory inside P; fixtures in `tests/fixtures/sci-review/messages/valid/` and `tests/fixtures/sci-review/messages/invalid/`
- [X] T013 Implement the data model in `plugins/sci-review/scripts/panel.py`: string-constant enumerations `ScopeMode`, `Dimension`, `Severity`, `Role`, `Stance`, `AgreementLabel`, `Runner`, `ExtensionStatus` with the exact values of data-model.md section 1; frozen dataclasses `ScopedFile`, `Exclusion`, `ReviewScope`, `Perspective`, `Applicability`, `DomainExtension`, `Panel`, `CandidateFinding`, `CheckedItem`, `MergedFinding`, `Position`, `DebateRecord`, `Finding`, `RejectedFinding`, `ReviewReport`, each with `from_json` and `to_json` methods and the field rules of data-model.md section 2
- [X] T014 Implement a minimal JSON Schema validator (types, enums, required, `additionalProperties: false`, patterns, nullable, minimum, `minItems`, `minLength`, and `if`/`then` whose `if` tests a property's `const` or `enum`) plus the single-message semantic checks of data-model.md section 3, and the subcommands `validate --schema NAME FILE`, `init --project PATH` (run directory under `tempfile.gettempdir()`, refusing any path inside the project) and `clean --run DIR` in `plugins/sci-review/scripts/panel.py`; `init` and `clean` accept `--dry-run` (contracts/panel-cli.md); argument logging to standard error and the exit codes of contracts/panel-cli.md ("0 success, 1 validation failure, 2 usage error, 3 precondition not met")
- [X] T015 [P] Write the agent `plugins/sci-review/agents/scientific-auditor.md`: frontmatter with read-only tools (Read, Grep, Glob, Bash), a system prompt stating that it adopts the role brief named in its task, reads only the inputs listed for its phase, writes only its named output file inside the run directory, and never modifies project files (research R4)

**Checkpoint**: Schemas, data model, validator and agent exist; `python -m unittest tests.test_sci_review_panel` passes for `TestModelAndValidate`.

---

## Phase 3: User Story 1 - Review the scientific correctness of a branch (Priority: P1) MVP

**Goal**: A branch review by a parallel panel (five perspectives, defender, moderator) across five dimensions, reporting labelled, evidenced findings and checked items, on the Claude Workflow, Claude Agent and Codex subagent runners, with no file modified.

**Independent Test**: Build the seeded fixture (`tests/fixtures/sci-review/seeded-repo/build.py`), run the review on its feature branch with the Workflow runner, score with `score.py`: at least 90% of seeded defects found, one per dimension and language, no look-alike reported, every finding has the FR-014 fields, tree checksum unchanged (SC-001 to SC-004).

### Tests for User Story 1

- [X] T016 [P] [US1] Write scope tests (class `TestScopeBranch`) in `tests/test_sci_review_panel.py`: a temporary git repository with a default branch and a feature branch; `scope --mode branch` resolves the merge-base, lists changed files with line ranges including uncommitted and untracked files, assigns `language` (`python`, `typescript`, `other`), excludes `node_modules/`, `dist/`, lock files and `linguist-generated` paths with reasons; a repository with no remote and no default branch exits with code 3; a non-git directory exits with code 3 and a message offering repository or path mode
- [X] T017 [P] [US1] Write panel and merge tests (classes `TestPanel`, `TestMerge`) in `tests/test_sci_review_panel.py`: `panel` clamps perspectives to 2 to 7, rounds to 0 to 3, batches to 1 to 4 and records the clamped values; a request for more perspectives than are available yields all available ones and records that; `merge` clusters candidates in the same file whose line ranges are within three lines, never clusters across files, and groups clusters into at most `max_batches` batches by file; `panel --dry-run` writes nothing; store the merge fixtures and expected clusters as JSON in `tests/fixtures/sci-review/messages/merge/` so that the parity test can reuse them
- [X] T018 [P] [US1] Write adjudication tests (class `TestAdjudicate`) in `tests/test_sci_review_panel.py`: one fixture debate record per rule of data-model.md section 3 (raiser withdrew: rejected; only the raiser accepts with an unanswered defender objection: rejected; null `trigger` or `wrong_output`: at most contested; no perspective stance is `challenge` and every defender objection answered: consensus; more than half of the perspectives accept: majority; otherwise contested); the "answered" definition of data-model.md (Position); a member absent from the final round keeps its latest position; the majority denominator includes domain perspectives and the raiser and excludes the defender; `withdraw` from a non-raiser exits 1; a moderator note without `no_trigger_reason` for a finding with null `trigger` exits 1; moderator notes are attached as arguments only to contested findings and as reasons only to rejected ones; store each record and its expected stop round as JSON in `tests/fixtures/sci-review/messages/debate/` so that the parity test can reuse them
- [X] T019 [P] [US1] Write report tests (class `TestReport`) in `tests/test_sci_review_panel.py` against golden files in `tests/fixtures/sci-review/messages/golden/`: findings ordered consensus, majority, contested and within each high, medium, low (FR-019); all eight sections in the order of contracts/report.md section 1, including Rejected findings with id, summary, raised by and reason; the no-reviewable-code case renders sections 1 to 3 and the sentence "No reviewable scientific code changed in this scope."; the ReportFindings mapping of contracts/report.md section 3 for consensus and majority findings (`failure_scenario` = trigger + " produces " + wrong_output, `verdict` CONFIRMED, `short_summary` prefixed with the label)
- [X] T020 [P] [US1] Write `tests/test_sci_review_workflow_build.py`: (1) drift: `build_workflow.py --check` exits 0 on the committed script; editing a role brief in a temporary copy of the plugin makes `--check` exit 1 and print the diff; `--dry-run` prints the diff and leaves the file unchanged; the generated script contains every role brief and schema between the generated-section markers; (2) parity: extract the code between `// BEGIN PURE` and `// END PURE` in `plugins/sci-review/workflows/scientific-review.js`, run it with `node` on the fixtures of `tests/fixtures/sci-review/messages/merge/` and `.../debate/`, and assert the same clusters, batches and stop rounds as `panel.py`; skip the parity class with a stated reason when `node` is absent

### Seeded fixture for User Story 1

- [X] T021 [US1] Write `tests/fixtures/sci-review/seeded-repo/manifest.json`: for each of the five dimensions and each of Python and TypeScript, at least one seeded defect with `id`, `file`, `line`, `dimension`, `language`, `severity`, and, for every High-severity defect, `reproduce` (the path of its reproduction check, T024); designated look-alikes (float equality against a sentinel, equality against an exact integer-valued float, seeding documented as left to the caller); and the cases of US1 acceptance scenarios 1, 2, 6 and 7 (division by a quantity reaching zero, scaler fitted before the split, explicit time step above its stability limit, parallel float sum in completion order)
- [X] T022 [US1] Write `tests/fixtures/sci-review/seeded-repo/build.py` (`--out DIR`): creates a git repository whose `main` holds correct baseline code and whose `feature` branch adds every defect and look-alike of `manifest.json` in `src/sci/*.py` and `src/sci/*.ts`, split across two directories for User Story 3
- [X] T023 [US1] Write `tests/fixtures/sci-review/seeded-repo/score.py` (`report.json [--manifest PATH] [--run DIR]`): matches findings to seeded defects by file and line within three lines, prints recall overall, per dimension and per language (SC-001), look-alike false positives (SC-002), missing FR-014 fields (SC-003), and, when `--run` is given, best single-perspective recall from `candidates/*.json` (SC-008) and the share of independent-round false positives rejected in debate (SC-009)
- [X] T024 [US1] Write one reproduction check per High-severity seeded defect in `tests/fixtures/sci-review/seeded-repo/checks/` (`<id>.py` or `<id>.mjs`, outside the built repository so that it is never reviewed), each taking the built repository path, calling the defective function with the triggering input, and exiting 1 on the wrong output; add `score.py --verify-fixes REPO` that runs every check and reports which pass, so that a check fails on the `feature` branch and passes once the recommended fix is applied (SC-007)

### Implementation for User Story 1

- [X] T025 [P] [US1] Write `SKILL_DIR/dimensions/mathematical-derivations.md` (FR-008): language-neutral checks for correspondence of equations to stated or standard forms, matrix and array shapes, index and summation bounds including off-by-one; worked defect and look-alike examples in Python and TypeScript
- [X] T026 [P] [US1] Write `SKILL_DIR/dimensions/numerical-stability.md` (FR-009): float equality, overflow and underflow, catastrophic cancellation, division near zero, log-sum-exp, silent narrowing of precision, unintended broadcasting shapes, NaN propagation through reductions; the legitimate-use exceptions of FR-015 (sentinel and exact integer-valued float equality); worked examples in Python and TypeScript
- [X] T027 [P] [US1] Write `SKILL_DIR/dimensions/physical-modelling-and-units.md` (FR-010): explicit consistent units, unit handling at I/O, continuous and discrete conservation, probabilities and fractions summing to one, physically impossible values, discretisation, boundary and initial conditions, stability limits (CFL), sign conventions and frames, validity regimes; worked examples in Python and TypeScript; no building-energy content (FR-012a)
- [X] T028 [P] [US1] Write `SKILL_DIR/dimensions/statistical-integrity.md` (FR-011): data leakage including temporal leakage and preprocessing fitted on validation or test data, plotting or reporting code that mutates data, unseeded stochastic processes, with the documented-caller-seeding exception of FR-015; worked examples in Python and TypeScript
- [X] T029 [P] [US1] Write `SKILL_DIR/dimensions/algorithmic-correctness.md` (FR-012): invariants and pre- and postconditions, termination and convergence criteria, integer overflow and index arithmetic, empty, single-element and duplicate-key edge cases, order and concurrency dependence, nondeterminism across runs or platforms, stale caching; worked examples in Python and TypeScript
- [X] T030 [P] [US1] Write the five perspective briefs `SKILL_DIR/roles/theorist.md`, `SKILL_DIR/roles/numerical-analyst.md`, `SKILL_DIR/roles/experimentalist.md`, `SKILL_DIR/roles/methodologist.md`, `SKILL_DIR/roles/computer-scientist.md`, each with the sections stance, guiding questions, checks owned, what not to flag (contracts/extension.md section 3), the stances of FR-022, the instruction to review every dimension, to load dimension documents on demand, to make every failure scenario concrete or set `trigger` to null, to record checked items, and to output only `candidate-findings.schema.json`
- [X] T031 [P] [US1] Write `SKILL_DIR/roles/defender.md`: argues that each finding is not a defect by identifying context, assumption or documented intent (FR-022); answers every finding of a batch in one output conforming to `debate-positions.schema.json`; never uses `withdraw`
- [X] T032 [P] [US1] Write `SKILL_DIR/roles/moderator.md`: merge task (confirm or split each location cluster, choose representative fields, highest member severity unless a `severity_reason` is recorded, output `merge-ruling.schema.json`); notes task, run per batch after its debate and without knowledge of labels (for every finding: the strongest argument for and against drawn from the recorded positions, the assumption or missing information that would settle a disagreement where identifiable (FR-025), a one-sentence rejection reason, and, when `trigger` or `wrong_output` is null, the reason no concrete trigger was established; output `moderator-notes.schema.json`); when no member argued against a finding, `argument_against` is "No member argued against.", and when a finding was not challenged to rejection, `rejection_reason` is "Not rejected."; never introduces findings and never assigns labels
- [X] T033 [US1] Implement `scope` for `--mode branch` (and `--baseline REF` for explicit ranges) in `plugins/sci-review/scripts/panel.py`: base resolution as `review-docs` does (remote default branch, merge-base), uncommitted and untracked files, line ranges from `git diff --unified=0`, generated and vendored exclusions, `--budget N` (default 6,000 lines) with partitioning and the unreviewed remainder recorded in `excluded`, exit 3 when no base can be determined, `--dry-run`; writes `$RUN/scope.json` (research R12)
- [X] T034 [US1] Implement `panel` in `plugins/sci-review/scripts/panel.py`: `--perspectives`, `--rounds`, `--batches`, `--runner`, `--dry-run`; clamps to "2 to 7 entries, extensions included" (a request for more than are available yields all of them), "0 to 3, default 2", "1 to 4, default 2"; sets `independent` to false only for `sequential`; records each perspective's absolute brief and reference paths; writes `$RUN/panel.json`
- [X] T035 [US1] Implement `merge` in `plugins/sci-review/scripts/panel.py`: reads `$RUN/candidates/*.json`, clusters by "same file, line ranges within three lines", groups clusters by file into at most `max_batches` batches, prints the clusters and batches as JSON (research R7)
- [X] T036 [US1] Implement `adjudicate` in `plugins/sci-review/scripts/panel.py`: reads `merge/`, `debate/` and `notes/` messages, builds `DebateRecord`s with each member's latest position, runs the cross-message semantic checks (exit 1 on `withdraw` from a non-raiser), applies the six rules of data-model.md section 3 in order, attaches moderator notes (arguments to contested findings, reasons to rejected ones), supports `--dry-run`, and writes `$RUN/adjudication.json`
- [X] T037 [US1] Implement `report` in `plugins/sci-review/scripts/panel.py`: builds `ReviewReport`, validates it against `report.schema.json`, writes `$RUN/report.json` (with `--dry-run`), renders `--format json` and `--format markdown` with all eight sections of contracts/report.md section 1 (Scope, Panel, Extensions, Findings, Rejected findings, Checked and found correct, Not reviewed, Notices) in that order, and emits the ReportFindings mapping of section 3 for consensus and majority findings in the JSON output under `report_findings`
- [X] T038 [US1] Implement `ingest --run DIR FILE` in `plugins/sci-review/scripts/panel.py`: reads a Workflow `PanelRun` result (contracts/invocation.md section 4), validates each message against its schema, and writes it into the layout of contracts/panel-messages.md section 2 (`candidates/`, `merge/`, `debate/`, `notes/`), with `--dry-run`; add a test (class `TestIngest`) in `tests/test_sci_review_panel.py` that ingests a fixture result and checks the files written
- [X] T039 [US1] Write `plugins/sci-review/scripts/build_workflow.py` (`[--check | --dry-run]`): reads `SKILL_DIR/protocol.md`, `SKILL_DIR/roles/*.md` and `SKILL_DIR/schemas/*.json` and writes them as string constants between `// BEGIN GENERATED` and `// END GENERATED` markers in `plugins/sci-review/workflows/scientific-review.js`, logging its arguments to standard error; `--dry-run` prints the unified diff and writes nothing; `--check` prints the diff and exits 1 when it is not empty
- [X] T040 [US1] Write the hand-maintained part of `plugins/sci-review/workflows/scientific-review.js` (structure of `plugins/project-kit/workflows/review-docs.js`): `meta` with phases `Independent`, `Merge`, `Debate`, `Notes`; arguments of contracts/invocation.md section 4; a pure section between `// BEGIN PURE` and `// END PURE` holding only `clusterCandidates`, `batchClusters` and `debateStopped`, implementing the clustering, batching and stop rules of `protocol.md` with no Workflow globals; independent round via `parallel()` with one `agent()` per perspective given only its brief, protocol, dimension documents, reference material for domain perspectives and scope, with the candidate-findings schema; debate via `pipeline()` over batches with one moderator merge call per batch, then rounds 0 to R for perspectives and defender with the debate-positions schema, calling only unsettled members and stopping when `debateStopped` holds, then one moderator notes call per batch with the moderator-notes schema; optional per-role `models`; returns a `PanelRun` holding every message, with no label computation in JavaScript; then run `python3 plugins/sci-review/scripts/build_workflow.py` to fill the generated section
- [X] T041 [P] [US1] Write `SKILL_DIR/runners/claude-workflow.md`, starting after the opening steps of `SKILL.md`: preconditions, launch `sci-review:scientific-review` with the arguments of contracts/invocation.md section 4 (perspectives with brief and reference paths taken from `panel.json`), write the returned `PanelRun` to `$RUN/workflow-result.json`, run `panel.py ingest`, then return to the closing steps of `SKILL.md`
- [X] T042 [P] [US1] Write `SKILL_DIR/runners/codex-subagents.md` following contracts/codex-orchestration.md sections 1 to 3, starting after the opening steps of `SKILL.md` and ending before its closing steps: wave spawning when `agents.max_concurrent_threads_per_session` is lower than the step size, one subagent per perspective listed in `panel.json` (brief and reference paths from it, so domain perspectives need no runner change) in parallel with only the listed inputs and its output path, validate and return invalid outputs once, merge with one moderator per batch, debate rounds per batch calling only unsettled members, moderator notes per batch; `git status --porcelain` before and after; fallback to sequential when spawning fails
- [X] T043 [P] [US1] Write `SKILL_DIR/runners/claude-agents.md`: the steps of `runners/codex-subagents.md` with "launch a `sci-review:scientific-auditor` agent", all launches of one step in a single message, perspectives and their brief and reference paths taken from `panel.json`, and the schema passed in each prompt (research R3)
- [X] T044 [P] [US1] Write the optional Codex template `SKILL_DIR/codex-agents/sci-review-panelist.toml` with `name`, `description`, `developer_instructions` (adopt the role brief named in the task, write only the named output file), `model_reasoning_effort = "high"`, `features.apps = false`; the skill never copies it (research R4)
- [X] T045 [US1] Write `SKILL_DIR/SKILL.md`: frontmatter `name: scientific-review` with a trigger description from contracts/invocation.md section 1 that excludes style, lint and documentation reviews; argument parsing of section 2; precondition checks of section 5; runner selection in the order of section 3 with the Workflow opt-in rule; the opening steps shared by every runner, run in the orchestrating conversation (`panel.py init`, `scope`, then `panel --runner R`); hand-over to the selected runner file, which covers the independent round to the moderator notes; the closing steps shared by every runner (`panel.py adjudicate`, `report`, delivery via ReportFindings when available per contracts/report.md section 3, otherwise the table, then `clean` unless the user asked to keep the run directory); the read-only rule (FR-006); the empty-scope rule (US1 scenario 4); links to `protocol.md`, `roles/`, `dimensions/`, `runners/`
- [X] T046 [US1] Regenerate `plugins/sci-review/workflows/scientific-review.js` with `python3 plugins/sci-review/scripts/build_workflow.py`, run `uv run --no-project --python 3.12 python -m unittest discover -s tests -v`, and fix failures in `plugins/sci-review/scripts/panel.py`
- [ ] T047 [US1] Run quickstart.md section 4 on the Claude Workflow, Codex and Claude Agent runners, keeping each run directory; record each runner's `score.py --run` output (SC-001 to SC-003, SC-008, SC-009), the tree checksum comparison (SC-004), the SC-011 inspection, and, for one runner, the `score.py --verify-fixes` result after applying each High finding's recommended fix in a copy of the fixture (SC-007) in `specs/007-sci-review-plugin/validation.md`

**Checkpoint**: User Story 1 is functional on all three multi-agent runners and is the MVP.

---

## Phase 4: User Story 2 - See where the panel disagrees and why (Priority: P2)

**Goal**: Contested findings carry the strongest argument on each side and the deciding assumption in every report format; withdrawn and rejected findings appear in their own section with reasons. The moderator's notes task (T032) and the Rejected findings section (T037) are delivered with User Story 1.

**Independent Test**: The seeded contested construct is reported as `contested` with `argument_for`, `argument_against` and `deciding_assumption`; a finding withdrawn in debate appears only under Rejected findings (SC-010, US2 scenarios 1 to 3).

### Tests for User Story 2

- [X] T048 [P] [US2] Add tests (class `TestDisagreement`) in `tests/test_sci_review_panel.py`: a contested finding missing `argument_for` or `argument_against` fails report validation; `deciding_assumption` may be null; a contested finding with null `trigger` renders `failure_scenario` as "No concrete trigger established: " + `no_trigger_reason`; the ReportFindings `summary` of a contested finding carries " Contested. For: … Against: … Decided by: …"; a withdrawn finding renders only in the Rejected findings section; the Markdown and golden output in `tests/fixtures/sci-review/messages/golden/contested.md` match

### Implementation for User Story 2

- [X] T049 [US2] Add the contested construct to `tests/fixtures/sci-review/seeded-repo/manifest.json` and `tests/fixtures/sci-review/seeded-repo/build.py` (an approximation valid only in an undocumented regime, for example a small-angle or linearised relation), with `expected_label: "contested"` and the expected deciding assumption; extend `tests/fixtures/sci-review/seeded-repo/score.py` to check the label and the presence of both arguments (SC-010)
- [X] T050 [US2] Extend `report` in `plugins/sci-review/scripts/panel.py` to render contested findings with their arguments, deciding assumption and, for a null trigger, the no-trigger reason, both in the Markdown table and in the ReportFindings mapping of contracts/report.md section 3
- [X] T051 [US2] Run the seeded review once on the Workflow runner and record the contested result in `specs/007-sci-review-plugin/validation.md`

**Checkpoint**: User Stories 1 and 2 both pass their independent tests.

---

## Phase 5: User Story 3 - Review a whole repository or selected paths (Priority: P2)

**Goal**: Repository and path modes with the same panel and report, and an explicit record of unreviewed parts.

**Independent Test**: On the seeded fixture, repository mode reports defects in both seeded directories; path mode on one directory reports nothing outside it; `--budget 200` lists the unreviewed remainder (quickstart.md section 5).

### Tests for User Story 3

- [X] T052 [P] [US3] Add tests (class `TestScopeModes`) in `tests/test_sci_review_panel.py`: `--mode repository` enumerates tracked files with empty `line_ranges` regardless of history; `--mode paths --path P` restricts to P and records other paths as excluded with reason "outside paths"; `--mode paths` without `--path` exits 2; generated and vendored files are excluded unless named; `--budget` partitions and records the remainder with reason "over budget"; notebooks (`.ipynb`) are included as code

### Implementation for User Story 3

- [X] T053 [US3] Implement `--mode repository` and `--mode paths` in the `scope` subcommand of `plugins/sci-review/scripts/panel.py`, sharing the exclusion and budget logic of T033
- [X] T054 [US3] Add the repository and path modes, the "name the unreviewed parts" rule (US3 scenario 3), and the non-git edge case (offer repository or path mode) to `SKILL_DIR/SKILL.md`
- [X] T055 [US3] Add a filter in `plugins/sci-review/scripts/panel.py` `report` that drops and records as a notice any finding whose file lies outside the scope, so that path mode never reports outside the named paths (US3 scenario 2)
- [X] T056 [US3] Run quickstart.md section 5 and record the results in `specs/007-sci-review-plugin/validation.md`

**Checkpoint**: User Stories 1 to 3 pass independently.

---

## Phase 6: User Story 4 - Review building energy simulation code with the idfkit extension (Priority: P2)

**Goal**: The domain-extension contract (version 1), its discovery and selection in `sci-review`, a contract-only test extension, and the idfkit building-energy extension with the building physicist and idfkit model checks.

**Independent Test**: With the idfkit extension installed, the building-energy fixture's seeded defects are reported with the building physicist among the raisers (at least 90%); uninstalled, none is attributed to a domain perspective and the report recommends the extension; the test extension joins the panel without any change to `sci-review`; an invalid declaration is listed as failed (SC-012, SC-013, quickstart.md section 6).

### Tests for User Story 4

- [X] T057 [P] [US4] Add tests (class `TestExtensions`) in `tests/test_sci_review_panel.py`: a valid declaration whose glob, file type, or language plus import pattern matches a scoped file is `selected`; glob and file-type matching is case-insensitive (`**/*.epJSON` matches `model.epjson`); a valid non-matching one is `not-applicable` with a reason; missing fields or `contract_version` other than 1 give `failed` with the reason; two selected extensions claiming one file both join the panel; the known idfkit entry becomes `recommended` when undiscovered and a scoped file imports `idfkit` or is an `.idf`, `.epjson` or `.epw` file; selected domain perspectives count toward the limit of 7; `select-extensions --dry-run` writes nothing
- [X] T058 [P] [US4] Write the contract-only test extension plugin in `tests/fixtures/sci-review/test-extension-plugin/` (`.claude-plugin/plugin.json`, `skills/acoustics-sci-review-extension/SKILL.md`, `extension.json`, `perspective.md`, `reference/acoustics.md`) using only contracts/extension.md, plus a copy `tests/fixtures/sci-review/test-extension-plugin-invalid/` whose `extension.json` has `contract_version: 2` (SC-013)

### Implementation for User Story 4 (sci-review)

- [X] T059 [US4] Implement `select-extensions --run DIR --declaration FILE ... [--dry-run]` in `plugins/sci-review/scripts/panel.py`: parse each declaration into `DomainExtension`, apply the `Applicability` rule of data-model.md ("A file matches if any glob or file type matches, or if its language is listed and any import pattern matches", globs and file types case-insensitive), set statuses, add the known-extension registry constant with the idfkit row of contracts/extension.md section 5 as `recommended` when applicable, and record statuses in `$RUN/panel.json`; make `panel` include selected domain perspectives with `source` set to the extension id and absolute brief and reference paths
- [X] T060 [US4] Write the extension section of `SKILL_DIR/protocol.md` and a new reference `SKILL_DIR/extensions.md` reproducing contracts/extension.md sections 1 to 5 (skill naming, `extension.json` fields, obligations, discovery and failure, known extensions) as the authoritative contract text for extension authors
- [X] T061 [US4] Add extension discovery to the opening steps of `SKILL_DIR/SKILL.md`, between `panel.py scope` and `panel.py panel`: find skills whose names end in `sci-review-extension` in the host's skill listing, load each for its directory, pass each `extension.json` to `panel.py select-extensions`, and render the Extensions section (selected, not applicable, failed with reason, recommended with what it would add); the runners need no change because they start after the opening steps and take perspectives and their brief and reference paths from `panel.json` (T041 to T043, T073)
- [X] T062 [US4] Extend `plugins/sci-review/workflows/scientific-review.js` to accept `extensions` with absolute brief and reference paths, add one independent-round agent and one debate member per selected domain perspective, and regenerate with `python3 plugins/sci-review/scripts/build_workflow.py`
- [X] T063 [US4] Extend `report` in `plugins/sci-review/scripts/panel.py` to render the Extensions section from `panel.json` statuses, with the reason for `failed` and `not-applicable` and the "adds" text for `recommended`

### Implementation for User Story 4 (idfkit plugin, separate repository)

- [X] T064 [P] [US4] Write `idfkit-plugin/skills/building-energy-sci-review-extension/extension.json` exactly as in contracts/extension.md section 2 (`contract_version: 1`, `id: "building-energy-sci-review-extension"`, `plugin: "idfkit"`, perspective `building-physicist`, the listed globs, file types, languages and import patterns, `checks: "checks.md"`)
- [X] T065 [P] [US4] Write `idfkit-plugin/skills/building-energy-sci-review-extension/SKILL.md`: name ending in `sci-review-extension`, description beginning `sci-review extension: building energy`, body stating that it is consumed by `sci-review` and instructing a model that loads it directly to run `sci-review` instead
- [X] T066 [P] [US4] Write `idfkit-plugin/skills/building-energy-sci-review-extension/perspective.md` (building physicist; stance, guiding questions, checks owned, what not to flag): heat-transfer and psychrometric relations, zone and system energy balances, IP and SI conversions (for example kBtu and kWh), simulation time conventions (hour-ending timestamps, leap years, daylight saving time, aggregation across timesteps and reporting frequencies) (FR-033)
- [X] T067 [P] [US4] Write `idfkit-plugin/skills/building-energy-sci-review-extension/reference/building-energy.md` in the dimension-document form: language-neutral checks, then worked defect and look-alike examples in Python and TypeScript using idfkit
- [X] T068 [P] [US4] Write `idfkit-plugin/skills/building-energy-sci-review-extension/checks.md` (FR-034, research R10): for each in-scope IDF or epJSON file run `validate_model` and `check_model_integrity` through the idfkit MCP server, falling back to the `idfkit` Python package, and otherwise reporting the checks as not run; each failure becomes a candidate finding; never run a simulation without the user's request
- [X] T069 [US4] Write the building-energy fixture in `idfkit-plugin/tests/fixtures/sci-review/` (`build.py`, `manifest.json`): Python and TypeScript code seeded with an hour-ending timestamp read as hour-starting, a kBtu to kWh conversion with the wrong factor, a leap-year series truncated to 8760 hours, and one IDF file with an integrity failure; plus correct look-alikes
- [X] T070 [US4] Register the new skill in the idfkit plugin manifests `idfkit-plugin/.claude-plugin/plugin.json` and `idfkit-plugin/.codex-plugin/plugin.json` if they enumerate skills, and add a changelog entry in `idfkit-plugin/CHANGELOG.md`
- [X] T071 [US4] Run quickstart.md section 6 (steps 1 to 4) and record the results, including SC-012 and SC-013, in `specs/007-sci-review-plugin/validation.md`

**Checkpoint**: Extensions work on the contract alone; User Stories 1 to 4 pass independently.

---

## Phase 7: User Story 5 - Run the review where agents or parallel workflows are unavailable (Priority: P3)

**Goal**: The sequential runner, the written fallback when `python3` is absent, table delivery without ReportFindings, and the reduced-independence notice.

**Independent Test**: With agents and workflows disabled, the seeded review produces the same report sections and labels, detects the seeded defects within one defect of the Workflow run, and carries the reduced-independence notice (SC-005).

### Tests for User Story 5

- [X] T072 [P] [US5] Add tests (class `TestSequential`) in `tests/test_sci_review_panel.py`: with `--runner sequential`, `panel.json` has `independent: false` and the report's Notices section contains the reduced-independence sentence; Markdown output without ReportFindings renders one table per label with every field of contracts/report.md section 2; a message dropped after two failed validations adds a notice naming the role

### Implementation for User Story 5

- [X] T073 [US5] Write `SKILL_DIR/runners/sequential.md`, starting after the opening steps of `SKILL.md` and ending before its closing steps: perform each perspective listed in `panel.json` (domain perspectives included, with their brief and reference paths) in turn, writing its candidates file before reading the next perspective's brief, then merge, debate rounds and moderator notes in the conversation, using the same message files and `panel.py` steps; when `python3` is absent, apply the written fallback rules of `protocol.md` to the opening and closing steps as well
- [X] T074 [US5] Add to `plugins/sci-review/scripts/panel.py` `report` the reduced-independence notice for `sequential` ("The perspectives were not independent agents; agreement among them was reached within a single reviewer and is weaker evidence than in a parallel review."), the notice for languages other than Python and TypeScript, and the missing-tool notices
- [X] T075 [US5] Add to `SKILL_DIR/SKILL.md` the user-forced lower runner ("run it without agents"), the sequential fallback when spawning fails, and table delivery when ReportFindings is unavailable
- [X] T076 [US5] Run quickstart.md section 4 step 3 with the sequential runner and record the SC-005 comparison in `specs/007-sci-review-plugin/validation.md`

**Checkpoint**: The review works on every surface.

---

## Phase 8: User Story 6 - Install the reviewer separately from project-kit (Priority: P3)

**Goal**: `sci-review` listed in the Claude marketplace and alone in a Codex marketplace (FR-001, FR-001a), validated and smoke-installed in CI, with install separation verified.

**Independent Test**: In a fresh `HOME`, installing only `sci-review@project-kit` exposes its skill, agent and workflow and no project-kit skill; installing only `project-kit` exposes no `sci-review` component; Codex lists `sci-review` and not `project-kit` (SC-006, quickstart.md section 3).

### Tests for User Story 6

- [X] T077 [P] [US6] Extend `.github/scripts/check_manifests.py` to iterate over every plugin in `.claude-plugin/marketplace.json`, check that each `source` holds a `.claude-plugin/plugin.json` whose `name` matches, check that `plugins/sci-review/.codex-plugin/plugin.json` has the same `name` and `version` as its Claude manifest, and check that `.agents/plugins/marketplace.json` lists `sci-review` only

### Implementation for User Story 6

- [X] T078 [US6] Add the `sci-review` entry (`source: "./plugins/sci-review"`, a description distinct from project-kit's) to `.claude-plugin/marketplace.json` and update the marketplace description to cover both plugins
- [X] T079 [US6] Create the Codex marketplace `.agents/plugins/marketplace.json` listing only `sci-review` with a `local` source of `./plugins/sci-review` (research R11)
- [X] T080 [US6] Extend `.github/workflows/validate.yml`: `claude plugin validate ./plugins/sci-review --strict`; `python3 plugins/sci-review/scripts/build_workflow.py --check`; make Node.js 22 available to the unit-test job so that the Workflow parity test runs rather than skips; a smoke-install job that installs only `sci-review@project-kit` in a fresh `HOME` and asserts skill `scientific-review`, agent `scientific-auditor` and `workflows/scientific-review.js`, and that no project-kit skill is present; assert in the existing project-kit smoke install that no sci-review component is present; Codex manifests are checked statically by T077, so no Codex CLI is installed
- [X] T081 [US6] Verify research R11's open question (whether Codex prefers `.agents/plugins/marketplace.json` over `.claude-plugin/marketplace.json`) and record the result and, if needed, the explicit Codex install command in `specs/007-sci-review-plugin/validation.md`
- [X] T082 [US6] Run quickstart.md section 3, including the Codex listing of US6 scenario 3 (FR-001a), and record the results in `specs/007-sci-review-plugin/validation.md`

**Checkpoint**: All user stories are independently functional and installable.

---

## Phase 9: Polish and Cross-Cutting Concerns

- [X] T083 [P] Add an Unreleased entry for `sci-review` 0.1.0 and the constitution amendment to `CHANGELOG.md` (Keep a Changelog 1.1.0 format)
- [X] T084 [P] Document both plugins, the `sci-review` install commands for Claude and Codex, and the extension contract link in `README.md`
- [X] T085 [P] Write `plugins/sci-review/README.md`: purpose, dimensions, panel, runners, arguments, report, extension contract pointer to `SKILL_DIR/extensions.md`
- [X] T086 Re-run the plan's Constitution Check against the implemented files and record the result at the end of `specs/007-sci-review-plugin/plan.md`
- [X] T087 Run every command of quickstart.md section 2, fix failures, and confirm `ruff check` and `ruff format --check` pass on `plugins/sci-review/scripts/` and `tests/test_sci_review_*.py`
- [X] T088 Review all new prose under `plugins/sci-review/` for the formal register and the absence of em dashes, and correct it in place

---

## Dependencies and Execution Order

### Phase dependencies

- **Setup (Phase 1)**: no dependencies; T001 (constitution amendment) precedes all other work by plan.md.
- **Foundational (Phase 2)**: depends on Setup; blocks every user story.
- **US1 (Phase 3)**: depends on Foundational. It is the MVP.
- **US2 (Phase 4)**: depends on US1 (panel, adjudication and report exist).
- **US3 (Phase 5)**: depends on US1 (`scope` and report exist); independent of US2.
- **US4 (Phase 6)**: depends on US1; the sci-review tasks T057 to T063 precede the idfkit tasks' validation (T071), and the contract text (T060) must be fixed before T064 to T068 are merged in the idfkit repository.
- **US5 (Phase 7)**: depends on US1; independent of US2 to US4.
- **US6 (Phase 8)**: depends on Setup and on the plugin files of US1 for the smoke install; otherwise independent.
- **Polish (Phase 9)**: depends on the stories being delivered.

### Story completion order

```text
Setup -> Foundational -> US1 (MVP) -> { US2, US3, US4, US5, US6 } -> Polish
```

US2 to US6 may proceed in parallel once US1 is complete, with one constraint: tasks that edit `SKILL_DIR/SKILL.md`, `plugins/sci-review/scripts/panel.py` or `plugins/sci-review/workflows/scientific-review.js` (T050, T053 to T055, T059, T061 to T063, T074, T075) touch shared files and must be serialised. No US4 task edits the runner files, so US4 does not depend on US5.

### Within each story

- Tests before the implementation they cover; they must fail first.
- Schemas and data model before subcommands; role briefs and protocol before `build_workflow.py` is run.
- Every change to `protocol.md`, `roles/` or `schemas/` is followed by regeneration of the Workflow script.
- Every change to the clustering, batching or stop rule in `protocol.md` or `panel.py` is mirrored in the Workflow script's pure section and checked by the parity test (T020).

## Parallel Execution Examples

### Phase 2

```text
T007 candidate-findings.schema.json
T008 merge-ruling.schema.json
T009 debate-positions.schema.json
T010 moderator-notes.schema.json
T011 report.schema.json
T015 agents/scientific-auditor.md
```

### User Story 1

```text
Tests:       T016, T017, T018, T019, T020            (separate test classes; serialise edits to the shared test file or use separate commits)
Dimensions:  T025, T026, T027, T028, T029
Roles:       T030, T031, T032
Fixture:     T024 after T021 and T022
Runners:     T041, T042, T043, T044
```

### User Story 4

```text
idfkit extension files: T064, T065, T066, T067, T068
sci-review side:        T057, T058
```

## Implementation Strategy

### MVP first (User Story 1 only)

1. Complete Phase 1 (with the constitution amendment) and Phase 2.
2. Complete Phase 3.
3. Stop and validate with the seeded fixture on the Workflow runner (SC-001 to SC-004), then on the Codex and Agent runners.

### Incremental delivery

1. US1: parallel panel review on a branch (MVP).
2. US2: disagreement reporting.
3. US3: repository and path modes.
4. US4: extension contract and the idfkit extension (released separately in the idfkit plugin).
5. US5: sequential runner for chat and Cowork surfaces.
6. US6: marketplace listing and CI; release as `sci-review-v0.1.0`.

## Notes

- `scripts/panel.py` never writes inside the reviewed project; every test asserts the fixture tree is byte-for-byte unchanged (SC-004).
- `workflows/scientific-review.js` is a generated artefact in its marked section; never edit that section by hand.
- Record every manual validation run in `specs/007-sci-review-plugin/validation.md`.
