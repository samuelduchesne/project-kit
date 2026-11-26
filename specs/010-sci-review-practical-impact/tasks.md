---

description: "Task list for feature 010: findings that say who hits them"
---

# Tasks: Findings that say who hits them

**Input**: Design documents from `specs/010-sci-review-practical-impact/`

**Prerequisites**: plan.md, spec.md, research.md (R1 to R12), data-model.md, contracts/ (issue.md, report-layout.md), quickstart.md

**Tests**: Requested. The plan (Technical Context, Testing) names a new `tests/test_sci_review_practical.py`, updates to `tests/test_sci_review_panel.py`, `tests/test_sci_review_verify.py` and `tests/test_sci_review_workflow_build.py`, new message fixtures and a live fixture `tests/fixtures/sci-review/practical-repo/`. Test tasks come before the implementation tasks of each story and are expected to fail until that story is implemented.

**Organization**: Tasks are grouped by user story (US1 to US5 of spec.md), so that each story can be implemented and tested on its own.

**Privacy**: This repository is public. No task may add the name, people, paths, code or quotations of the downstream project behind the evaluation (research R12). The evaluation's case file and raw artifacts stay outside the repository.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: The user story the task belongs to (US1 to US5)
- Every description names the exact file path

## Path Conventions

- `PANEL` = `plugins/sci-review/scripts/panel.py`
- `SKILL_DIR` = `plugins/sci-review/skills/scientific-review/`
- `PRACTICAL_TESTS` = `tests/test_sci_review_practical.py`
- `MSG` = `tests/fixtures/sci-review/messages/`
- New fields are added to the existing frozen dataclasses of `PANEL`, never passed around as dictionaries, and are listed in `_optional` with a null or false default so that earlier runs load (research R10).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Test scaffolding and the new enumerations.

- [X] T001 Create `PRACTICAL_TESTS` as a `unittest` module that imports `PANEL` the same way `tests/test_sci_review_verify.py` does. It provides helpers that build a temporary run directory from in-memory messages: a panel, a candidate message, a merge ruling and verification messages, as `tests/test_sci_review_verify.py` builds them.
- [X] T002 [P] Add to `PANEL` the enumeration classes `TriggerClass` (`VALUES = ("user-action", "data-condition", "release", "operator-change", "unreachable")` and `FREQUENCY_ORDER = ("user-action", "data-condition", "release", "operator-change")`), `FindingKind` (`"defect"`, `"design-question"`) and `OwnerSource` (`"codeowners"`, `"blame"`, `"none"`), next to `Verdict` and `AgreementLabel`, following the existing enumeration pattern (data-model.md, Enumerations).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Every new field exists in the schemas and records and is validated. Every story reads these.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T003 [P] Write schema and record tests in `PRACTICAL_TESTS`:
  - a feature-009 candidate message without `headline`, `context` or `in_practice` fails `panel.py validate --schema candidate-findings`;
  - a message with them passes;
  - a `headline` of 91 characters fails;
  - a feature-009 `adjudication.json` and `report.json` still load through `from_json` with the new fields null or false (FR-012).
- [X] T004 [P] Add the validation-rule tests of data-model.md, "Validation rules added to `panel.py validate`", to `PRACTICAL_TESTS`. Use new fixtures:
  - `MSG/invalid/verification-unreachable-confirm.json`: `trigger_class: unreachable` with `verdict: confirm`; must fail.
  - `MSG/invalid/verification-intended-refute.json`: `possibly_intended: true` with `verdict: refute`; must fail.
  - `MSG/invalid/verification-intended-no-reason.json`: `possibly_intended: true` with `possibly_intended_reason: null`; must fail.
  - `MSG/invalid/verification-correction-line-zero.json`: a `value_corrections` entry with `line: 0`; must fail.
  - `MSG/valid/verification-practical.json`: all new fields set correctly; must pass.
  - `MSG/invalid/debate-intended-non-defender.json`: a non-defender position with `possibly_intended: true`; must fail.
- [X] T005 [P] In `SKILL_DIR/schemas/candidate-findings.schema.json`, add to `CandidateFinding` the required properties:
  - `headline`: string, `minLength` 1, `maxLength` 90, description "Plain words; names the situation, not the code.";
  - `context`: string, `minLength` 1, description "One or two sentences: what the code does for its users and when the problem arises.";
  - `in_practice`: string, `minLength` 1, description "Who or what triggers it, how often, whether anyone would notice; for a cache, whether reuse looks intended.".
- [X] T006 [P] In `SKILL_DIR/schemas/merge-ruling.schema.json`, add `headline`, `context` and `in_practice` to `MergedFinding` with the same constraints as T005, as required properties.
- [X] T007 [P] In `SKILL_DIR/schemas/verification.schema.json`, add the following to `Verdict`, and add a `ValueCorrection` definition (`quoted`: string; `actual`: string; `file`: string; `line`: integer, `minimum` 1; all required, `additionalProperties: false`):
  - `reach`: string, `minLength` 1, required, description "Files read to establish how the trigger state arises (configuration, environment, deployment, release) and what each showed; 'none present' when the project has none.";
  - `trigger_class`: enum of `TriggerClass.VALUES`, required, description "`unreachable` only with verdict `refute`.";
  - `possibly_intended`: boolean, default false, description "Not allowed with `refute`.";
  - `possibly_intended_reason`: string or null, description "Required and non-empty when `possibly_intended` is true; null otherwise.";
  - `value_corrections`: array of `ValueCorrection`, required, may be empty.
- [X] T008 [P] In `SKILL_DIR/schemas/debate-positions.schema.json`, add optional `possibly_intended` (boolean) and `possibly_intended_reason` (string or null) to a position, with the description "Defender only; same rules as a verdict".
- [X] T009 [P] In `SKILL_DIR/schemas/report.schema.json`, add to `Finding` the following optional properties, and add a `ValueCorrection` definition identical to T007's:
  - `headline`, `context`, `in_practice`: string;
  - `kind`: enum `defect` | `design-question`, default `defect`;
  - `trigger_class`: enum of `TriggerClass.VALUES` or null;
  - `reach`: string or null;
  - `possibly_intended_reason`: string or null;
  - `value_corrections`: array of `ValueCorrection`;
  - `severity_capped`: boolean, default false.

  Add `design_questions`, an array of `Finding`, to the top-level `required` list and `properties`. Update the description: "findings holds defects only; design_questions holds findings with kind design-question; the finding cap counts both, design questions after defects."
- [X] T010 In `PANEL`, extend the records per data-model.md:
  - **`CandidateFinding`**: gains `headline`, `context` and `in_practice` (optional in the dataclass, default null).
  - **`MergedFinding`**: gains the same three fields.
  - **`VerdictRecord`**: gains `reach` (default `""`), `trigger_class` (default null), `possibly_intended` (default false), `possibly_intended_reason` (default null) and `value_corrections` (tuple of a new frozen `ValueCorrection` record with `quoted`, `actual`, `file`, `line`, default empty). Add `trigger_class` to `_enums`. Extend `effective` to return `uncertain` when `possibly_intended` is true (data-model.md, VerdictRecord).
  - **`Position`**: gains `possibly_intended` and `possibly_intended_reason`.
  - **`Finding`**: gains `headline`, `context`, `in_practice`, `kind` (default `defect`), `trigger_class`, `reach`, `possibly_intended_reason`, `value_corrections` and `severity_capped` (default false).

  Register `ValueCorrection` wherever `_records` maps nested record types.
- [X] T011 In `cmd_validate` of `PANEL` (and the semantic checks it calls), add data-model.md validation rules 1 to 4:
  1. `trigger_class: unreachable` requires `verdict: refute`.
  2. `possibly_intended: true` requires a non-refute verdict and a non-empty `possibly_intended_reason`.
  3. A `value_corrections` entry's `line` is at least 1; its `file` need not exist.
  4. `headline` is at most 90 characters.

  Also reject `possibly_intended` on a debate position whose `member` is not `defender`. Each rule's error message names the field and the rule. Make T003 and T004 pass.
- [X] T012 In the auto-merge of `PANEL` (the `auto-merge` subcommand, research R1), copy `headline`, `context` and `in_practice` from the single candidate to the merged finding. Add a test to `PRACTICAL_TESTS` that an auto-merged batch keeps all three fields.

**Checkpoint**: Every new field round-trips through validate, ingest, merge and adjudicate unchanged. A feature-009 run still loads.

---

## Phase 3: User Story 1 - Every finding orients its reader (Priority: P1) MVP

**Goal**: Finders write a headline, context and in-practice statement for every finding, and the report shows them before the technical details.

**Independent Test**: Render the golden practical run. Every finding block opens with its headline, context and "In practice", before Where, Trigger, Wrong output and Fix. A feature-009 golden run renders "Not recorded by this review." in their place.

### Tests for User Story 1

- [X] T013 [P] [US1] Create the golden run `MSG/golden/practical/`. Follow the file layout of `MSG/golden/full/` (panel, candidates, merge rulings, verifications, expected `report.md` and `report.json`). It has:
  - three findings with every new field set: one `user-action` defect at `high`; one `release` defect raised as `high` without a `severity_reason`; one finding with a `possibly_intended` verdict;
  - one finding whose verdict carries a value correction;
  - only invented file names and code (for example `src/services/results_cache.py`); nothing from a real project.

  The expected outputs follow contracts/report-layout.md.
- [X] T014 [P] [US1] Add report-layout tests to `PRACTICAL_TESTS`, comparing `panel.py report --format markdown` output on `MSG/golden/practical/` with its expected `report.md`. Assert that:
  - each finding is a `#### Fn. <headline>` block;
  - its badge line comes first, then context, then "**In practice.**", then the bullet list;
  - a feature-009 golden run (`MSG/golden/full/`) renders `<summary>` as the heading and "Not recorded by this review." for context and in practice.
- [X] T015 [P] [US1] Add `ReportFindings` mapping tests to `PRACTICAL_TESTS`, per contracts/report-layout.md:
  - `short_summary` is the headline truncated to 60 characters;
  - `summary` is `<headline>. <summary>`;
  - `failure_scenario` is `<context> In practice: <in_practice> Trigger: <trigger> Wrong output: <wrong_output>`.

### Implementation for User Story 1

- [X] T016 [P] [US1] In each finder brief, independent round, step 4, add the instruction verbatim from contracts/report-layout.md, "Brief changes", first bullet: "Write `headline` (at most 90 characters, no code identifiers), `context` (...) and `in_practice` (...)". Also add the three fields to the step-8 output description.
  - `SKILL_DIR/roles/theorist.md`
  - `SKILL_DIR/roles/numerical-analyst.md`
  - `SKILL_DIR/roles/experimentalist.md`
  - `SKILL_DIR/roles/methodologist.md`
  - `SKILL_DIR/roles/computer-scientist.md`
  - `SKILL_DIR/roles/generalist.md`
- [X] T017 [P] [US1] In `SKILL_DIR/roles/moderator.md`, merge step 4, add `headline`, `context` and `in_practice` to the fields the moderator chooses from the members. Keep the existing rule: "You may combine the members' wording, but you MUST NOT add a claim that no member made."
- [X] T018 [US1] In `render_markdown` of `PANEL`, replace the findings table (the `headers = ["Location", ...]` block) with one block per finding, per contracts/report-layout.md:
  - heading `#### Fn. <headline>`, or `<summary>` when the headline is null;
  - a badge line: severity, plus " (lowered from high)" when `severity_capped`; label; dimension; "trigger: <class>" when set;
  - the context paragraph;
  - "**In practice.** <in_practice>";
  - bullets for Where, Trigger, Wrong output, Fix and Raised by;
  - "Not recorded by this review." for null prose.

  Keep the per-label subsections. Make T014 pass for the defect findings.
- [X] T019 [US1] In `report_findings` of `PANEL`, apply the `ReportFindings` mapping of contracts/report-layout.md (`short_summary`, `summary`, `failure_scenario`). Make T015 pass.
- [X] T020 [US1] In `SKILL_DIR/protocol.md`, add a subsection "Finding prose" to section 3 (Role inputs), or after section 4. It defines `headline`, `context` and `in_practice` as in spec.md, Defined terms, and states that finders write them, the moderator merges them, and verifiers check them through reach.

**Checkpoint**: A run on the seeded fixture produces a report whose every finding opens in plain words.

---

## Phase 4: User Story 2 - Severity reflects how the software is used (Priority: P1)

**Goal** (revised in Phase 9): severity is defined on ordinary use, and the trigger class is shown beside it without changing it; findings carry evidence a reader can check.

**Independent Test**: Adjudicate the golden practical run. The `release` finding raised as `high` without a `severity_reason` is reported `medium` with `severity_capped: true`. With a `severity_reason` added, it stays `high`.

### Tests for User Story 2

- [X] T021 [P] [US2] Add trigger-class combination tests to `PRACTICAL_TESTS` (research R3):
  - majority among non-refuting verdicts;
  - a tie resolved by `TriggerClass.FREQUENCY_ORDER`, for example `release` against `user-action` gives `user-action`;
  - refuting verdicts ignored;
  - no non-refuting verdict gives null;
  - the reported `reach` is the first non-refuting verdict's with the reported class.
- [X] T022 **Superseded by Phase 9 (cap removed).** [P] [US2] Add cap tests to `PRACTICAL_TESTS` (research R5):
  - `high` + `release` + no `severity_reason` becomes `medium` with `severity_capped` true;
  - the same with `operator-change`;
  - `high` + `data-condition` stays `high`;
  - `high` + `release` + a `severity_reason` stays `high`;
  - `medium` + `release` is unchanged, with `severity_capped` false;
  - a debate-protocol finding (null class) is unchanged.
- [X] T023 [P] [US2] Add a test to `PRACTICAL_TESTS`: a finding whose verdicts are all `refute` with `trigger_class: unreachable` is rejected by the existing rule 2, with the first refuting verifier's reason.

### Implementation for User Story 2

- [X] T024 **Superseded by Phase 9 (cap removed).** [US2] In `adjudicate` of `PANEL` (verify protocol), after the label rules, combine the verdicts' `trigger_class` into `Finding.trigger_class` and `Finding.reach` per research R3. Then apply the cap: when `severity == "high"`, `trigger_class` is `release` or `operator-change`, and the merged finding has no `severity_reason`, set `severity = "medium"` and `severity_capped = True`. Make T021 to T023 pass.
- [X] T025 **Superseded by Phase 9 (cap removed).** [P] [US2] In `SKILL_DIR/protocol.md` section 4, replace the severity definitions with the definitions of research R5, verbatim:
  - **High**: produces a wrong result in ordinary use of the software.
  - **Medium**: produces a wrong result only in plausible edge cases, or only after a rare operational event (a release, an operator changing configuration), or prevents reproduction of a result.
  - **Low**: a latent risk that does not currently produce a wrong result.

  Add: "Adjudication lowers `high` to `medium` when the reported trigger class is `release` or `operator-change` and no `severity_reason` was recorded; the finding then carries `severity_capped`." In section 5.1, add the trigger-class combination rule of research R3 after the rules list.
- [X] T026 **Superseded by Phase 9 (cap removed).** [P] [US2] In the step-5 severity sentence of each finder brief (the six files of T016), replace the definition with the one of research R5. Add: "A defect whose only trigger is a release or an operator changing configuration is at most `medium`."

**Checkpoint**: No report rates `high` a finding whose only trigger is a release or an operator change, unless a reason is given.

---

## Phase 5: User Story 3 - Verifiers check practical reach and quoted values (Priority: P1)

**Goal**: Verifiers read configuration, environment, deployment and release files, classify the trigger, and correct quoted values that the repository contradicts. The report shows the corrections.

**Independent Test**: On the golden practical run, the finding with a value correction renders its trigger followed by "*(the finding quoted `X`; `file:line` has `Y`)*", and `report.json` carries the deduplicated corrections.

### Tests for User Story 3

- [X] T027 [P] [US3] Add tests to `PRACTICAL_TESTS`:
  - value corrections from two verifiers are unioned and deduplicated on (`quoted`, `file`, `line`) into `Finding.value_corrections`;
  - the markdown report shows each correction after the trigger, in the format of contracts/report-layout.md.
- [X] T028 [P] [US3] Extend `tests/test_sci_review_verify.py` so that every verification message it builds carries `reach`, `trigger_class` and `value_corrections`. The existing label tests must pass unchanged in meaning (SC-007).

### Implementation for User Story 3

- [X] T029 [US3] In `adjudicate` of `PANEL`, collect `value_corrections` from all verdicts of a finding: union them, deduplicate on (`quoted`, `file`, `line`), and keep the first-seen order. Add a notice to the report for each finding with a correction: "F<n>: a value quoted in the finding is contradicted by the repository; see the correction under its trigger." In `render_markdown`, append the corrections to the Trigger bullet. Make T027 pass.
- [X] T030 [US3] In `SKILL_DIR/roles/verifier.md`:
  - Insert step 2b verbatim from research R4 ("**2b. Establish practical reach.** When the trigger depends on configuration, a deployment, a release or data provenance, ...").
  - Add to step 4: "A verdict whose trigger cannot occur in any configuration the project ships is `refute` with `trigger_class: unreachable`."
  - Add rule 6 to "Verdicts": "Every verdict records `reach`, `trigger_class` and `value_corrections` (empty when none)."
  - Extend the JSON example with `"reach"`, `"trigger_class": "user-action"` and `"value_corrections": []`.
- [X] T031 [P] [US3] In `SKILL_DIR/protocol.md` section 3 (Role inputs), state that verifiers may read configuration, environment, deployment and release files outside the scope to establish reach. Add the definition of trigger class from spec.md, Defined terms.

**Checkpoint**: Each verdict records how the trigger arises, and the report never repeats a contradicted value without its correction.

---

## Phase 6: User Story 4 - Possibly deliberate behaviour is raised as a question (Priority: P2)

**Goal**: A finding that a verifier (or, in a debate, the defender) marks as possibly intended is reported under "Design questions", not as a defect.

**Independent Test**: On the golden practical run, the marked finding appears under "## Design questions", with "**Why it may be intended.**" and "**If it is not intended.**". It is absent from `findings` and present in `design_questions` in `report.json`, and its label counts the mark as uncertain.

### Tests for User Story 4

- [X] T032 [P] [US4] Add rule-2a tests to `PRACTICAL_TESTS` (research R6):
  - one confirm and one marked confirm: `kind: design-question`, label `majority` (rule 5: one confirm, no refute; the marked verdict counts as uncertain, so it is not `consensus`);
  - a single marked confirm: `design-question`, `contested`;
  - two confirms, one refute and no mark: `defect`, as before;
  - a marked finding that more verifiers refute than confirm is rejected, because rule 2 applies before 2a;
  - `possibly_intended_reason` is the first recorded.
- [X] T033 [P] [US4] Add debate tests to `PRACTICAL_TESTS`, using the message style of `MSG/debate/`:
  - a defender position with `possibly_intended: true`, not withdrawn, makes the finding a design question;
  - a finding whose marked defender position is followed by a later unmarked defender position is a defect.
- [X] T034 [P] [US4] Add report tests to `PRACTICAL_TESTS`:
  - `design_questions` is rendered after the defects, under "## Design questions", in the layout of contracts/report-layout.md;
  - `--max-findings 2` on a run with two defects and one design question withholds the design question and counts it in `withheld`.

### Implementation for User Story 4

- [X] T035 [US4] In `adjudicate` of `PANEL`, insert rule 2a after rule 2 for the verify protocol: when any non-refuted finding has a verdict with `possibly_intended`, set `kind = "design-question"` and `possibly_intended_reason` to the first recorded reason. The label rules 3 to 6 already see marked verdicts as uncertain through `VerdictRecord.effective` (T010). For the debate protocol, set `kind = "design-question"` when the defender's latest position on the finding carries `possibly_intended`. Make T032 and T033 pass.
- [X] T036 [US4] In `cmd_report` and `render_markdown` of `PANEL`:
  - split findings into `findings` (defects) and `design_questions`;
  - apply the finding cap to defects first, then design questions;
  - render "## Design questions" with "**Why it may be intended.**" and "**If it is not intended.**" per contracts/report-layout.md;
  - map design questions to `category: design-question` in `report_findings`.

  Make T034 pass.
- [X] T037 [P] [US4] In `SKILL_DIR/roles/verifier.md` step 4, add verbatim from contracts/report-layout.md: "Mark `possibly_intended` when the behaviour looks like a deliberate trade-off (stability, caching, tolerance, cost) that the code and its documentation neither state nor rule out; give the reason. When the documentation states the trade-off, refute instead and cite it." Extend the JSON example with `"possibly_intended": false, "possibly_intended_reason": null`.
- [X] T038 [P] [US4] In `SKILL_DIR/roles/defender.md`, allow the defender to mark a position `possibly_intended` with a reason, under the same rule as the verifier.
- [X] T039 [P] [US4] In `SKILL_DIR/roles/computer-scientist.md`, replace guiding question 7 with the text of research R7: "Can a cache or memoised value be returned after something it depends on has changed, including the code or configuration that computed it? If so, is the reuse deliberate (stability, cost), and what in the code or its documentation says so?" In `SKILL_DIR/dimensions/algorithmic-correctness.md`, add to the stale-caching check: "State whether the reuse looks intended; if it might be, say so in `in_practice`, so that a verifier can mark it."
- [X] T040 [P] [US4] In `SKILL_DIR/protocol.md` section 5.1, insert rule 2a verbatim from research R6, between rules 2 and 3: "**2a. Design question**: at least one verdict is marked possibly intended. The finding is not rejected; its label is computed by the remaining rules with the marked verdicts counted as uncertain, and it is reported with `kind: design-question`." In section 5.2, add the defender-mark rule. In the report description, add the Design questions section.

**Checkpoint**: Behaviour that may be deliberate reaches the owners as a question, with the trade-off stated both ways.

---

## Phase 7: User Story 5 - A finding becomes a well-routed issue (Priority: P2)

**Goal**: `panel.py issue` renders one delivered finding as an issue body in reader order, with suggested owners. It posts nothing.

**Independent Test**: On the golden practical run, `panel.py issue --run RUN --finding F1` writes `RUN/issues/F1.md` with the sections of contracts/issue.md in order. In a temporary git repository with a CODEOWNERS file, the owners come from that file; without one, they come from blame; outside git, the command explains that there are no owners. The project's `git status --porcelain` is empty afterwards.

### Tests for User Story 5

- [X] T041 [P] [US5] Add issue-layout tests to `PRACTICAL_TESTS`, on `MSG/golden/practical/` with a new expected `issues/F1.md` and an expected design-question `issues/F3.md`. Assert:
  - the section order of contracts/issue.md (title, Situation, Who hits this and when, Bug or design question, Where, Reproduction, Proposed fix, Suggested owners, provenance line);
  - a design-question title starts "Confirm intended behaviour: ";
  - a capped defect says "lowered from high because its only trigger is a release of new code";
  - value corrections appear as "Note: the finding quoted `X`; `file:line` has `Y`.";
  - a contested finding includes the arguments for and against and the deciding assumption;
  - a feature-009 run prints "Not recorded by this review." for missing prose.
- [X] T042 [P] [US5] Add owner tests to `PRACTICAL_TESTS`. Use a helper that builds a temporary git repository with commits by two authors on a file (`git -c user.name=... commit`).
  - CODEOWNERS at `.github/CODEOWNERS` with rules `* @team-a`, `/src/ @alice` and `src/cache/ @bob`: the finding in `src/cache/x.py` resolves to `@bob`, because the last match wins.
  - CODEOWNERS present but not matching: falls back to blame.
  - No CODEOWNERS: blame lists up to three authors by line count, then by latest date, with "(<n> of <m> lines, last <date>)".
  - A shallow clone (`git clone --depth 1` of the helper repository): output contains "History is truncated (shallow clone); older authors may be missing."
  - A project that is not a git repository: "No owners found: ".
- [X] T043 [P] [US5] Add CLI tests to `PRACTICAL_TESTS`:
  - an unknown id exits 2 with a message listing the delivered ids;
  - a withheld or rejected id exits 2;
  - a run without `report.json` exits 3;
  - `--dry-run` prints the body and the path, and writes no file;
  - after any `issue` call, the project's `git status --porcelain` is unchanged.

### Implementation for User Story 5

- [X] T044 [US5] In `PANEL`, add a frozen `IssueOwners` record (`source`: `OwnerSource`; `owners`: tuple of a frozen `Owner` record with `name`, `lines` (int or null), `last_date` (str or null); `truncated`: bool; `reason`: str or null). Add a function `suggest_owners(project, head, file, line_start, line_end) -> IssueOwners`:
  1. Read the first existing file among `.github/CODEOWNERS`, `CODEOWNERS`, `docs/CODEOWNERS` and `.gitlab/CODEOWNERS` with `git show <head>:<path>`, or from disk when there is no head.
  2. Match with the gitignore subset of research R9: anchored `/`, trailing `/` for directories, `*`, `**`, last match wins, GitLab `[Section]` lines skipped.
  3. Otherwise, run `git blame --line-porcelain -L <start>,<end> <head> -- <file>` and count lines per author. Keep up to three, ordered by count, then by latest author time. Set `truncated` when a `boundary` line appears.
  4. Otherwise, return source `none` with the reason.

  Use only read-only `git`. Make T042 pass.
- [X] T045 [US5] In `PANEL`, add `render_issue(report: ReviewReport, finding: Finding, owners: IssueOwners, head: str, level: str) -> str`, producing the body of contracts/issue.md exactly, including its rules 1 to 3. Write class names in words: `user-action` → "a user action", `data-condition` → "a data condition in ordinary inputs", `release` → "a release of new code", `operator-change` → "an operator changing configuration". Make T041 pass.
- [X] T046 [US5] Add the `issue` subcommand to `PANEL`'s parser (`add("issue", cmd_issue, "render one delivered finding as an issue body in the run directory")`, with `--finding` required) and implement `cmd_issue`:
  - load `report.json`, or exit 3 with "run `panel.py report` first";
  - find the finding in `findings` or `design_questions`, or exit 2 listing the delivered ids;
  - call `suggest_owners` and `render_issue`;
  - write `<run>/issues/<Fn>.md` unless `--dry-run`, and print the body; with `--dry-run`, also print the path it would write;
  - log the arguments as the other subcommands do.

  Make T043 pass.
- [X] T047 [US5] In `SKILL_DIR/SKILL.md` section 7 (Closing steps), before the `panel.py clean` step, add: "When the user wants to file a delivered finding or design question, run `panel.py issue --run $RUN --finding <id>` and show the body. Never post it: the user files it. Run it before `panel.py clean`, which removes the run directory." In the delivery step, mention in one line that each finding can be rendered as an issue.

**Checkpoint**: Any delivered finding can be turned into an issue that a domain reader can act on and route.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Generated runner, live fixtures, the downstream evaluation, documentation and release metadata.

- [X] T048 Regenerate `plugins/sci-review/scripts/scientific-review-panel.js` with `plugins/sci-review/scripts/build_workflow.py`, so that the embedded briefs and schemas carry the new fields. Update `tests/test_sci_review_workflow_build.py` only where it asserts the old schema content, and run it.
- [X] T049 Update the golden expected outputs of `MSG/golden/full/`, `MSG/golden/contested/` and `MSG/golden/empty/`, and any assertions in `tests/test_sci_review_panel.py` and `tests/test_sci_review_verify.py`, that compare the old findings table or the old severity wording. Change only the layout, the new empty `design_questions` and the new fields (SC-007). Run `python3 -m unittest discover -s tests -p 'test_sci_review_*.py'` (quickstart scenario 1) and fix any remaining failure.
- [X] T050 [P] Create the live fixture `tests/fixtures/sci-review/practical-repo/` with `build.py` and `manifest.json`, modelled on `tests/fixtures/sci-review/seeded-repo/build.py` (sources embedded, a `--check` mode, no markers in the sources). Write it in Python, with a small settings module and a `.env` file. It contains three cases and a correct look-alike for each (quickstart scenario 5):
  - (a) a results cache keyed on inputs but not on the algorithm's configuration, whose configuration differs only between deployments (`.env` against defaults);
  - (b) a cache that deliberately ignores a version field to keep results stable across releases, with no comment saying so;
  - (c) a defect whose obvious reproduction quotes a setting value that `.env` sets differently.

  All names are invented.
- [X] T051 Run quickstart scenario 5 live on `practical-repo` (five runs at `medium`) and once on `seeded-repo`. Record SC-002 to SC-005 in `specs/010-sci-review-practical-impact/validation.md`, section "Fixtures", with agents, tokens per verifier against feature 009 (budget +15%, plan Performance Goals) and wall time. If SC-003 fails, revise the verifier's possibly-intended instruction (T037) and run again once.
- [X] T052 Run quickstart scenario 6, the downstream evaluation, from the private case file kept outside the repository, following the steps of quickstart.md exactly: worktree, `medium` run, select the finding, `panel.py issue`, deterministic checks C5 to C7, blind judge for C1 to C4. Record in `specs/010-sci-review-practical-impact/validation.md`, section "Downstream case", the anonymised results only: the C1 to C7 table for the baseline and the treatment, the judge's preference paraphrased, agents, tokens, wall time, and the number of other findings by kind. Before committing, check that `validation.md` names no project, person, path, setting or code from the case (`grep` against the case file's values). If C2, C4 or C7 fails, revise the corresponding brief or rule and run the evaluation once more (plan, Phases after this plan). Then **re-check on current code and draft the issue**:
  1. Fetch the downstream project's current default branch and add a second worktree at its head.
  2. Re-check the treatment finding there: re-run `/sci-review:scientific-review medium <path>` on that worktree, or, if the cited lines are unchanged (`git diff <case commit> <head> -- <path>` shows nothing in the cited range or its callers), re-check the cited lines by reading them.
  3. If the finding still holds, render it with `panel.py issue` from the current-head run, or update the line numbers of the evaluation's body. Save it as `issue-draft.md` beside the case file, outside this repository, with a first line linking the original issue as the one it replaces.
  4. If it no longer holds, write a short note there instead, saying what changed.
  5. Post nothing: the user files the issue.
- [X] T053 [P] Update `plugins/sci-review/README.md`: findings now open in plain words; severity on realistic use and the cap; design questions; `panel.py issue` and its owner sources; nothing is posted.
- [X] T054 [P] Bump the version from 0.3.0 to 0.4.0 in `plugins/sci-review/.claude-plugin/plugin.json` and `plugins/sci-review/.codex-plugin/plugin.json`. Add an entry under `## [Unreleased]` in `CHANGELOG.md`, following its existing sci-review entries:
  - **Added**: finding prose, trigger class and reach, design questions, the `issue` command;
  - **Changed**: severity definition and cap, report layout, required message fields.
- [X] T055 Run `claude plugin validate` on the marketplace and on the `sci-review` plugin (constitution, Development Workflow), and run the full test suite once more.

---

## Phase 9: Revision after a second domain review (cap removed, evidence added)

**Purpose**: A second issue from the review drew comments that pointed at evidence, not prose ("valid, if we trust what the LLM has written"; a request for a compact input-to-output table), and at a severity judged on a guessed rarity. Research R5 (revised) and R13 record the decisions: the automatic severity cap is removed, verdicts carry a runnable reproduction and an extent table, the in-practice statement must cite where inputs come from, and how a fix is chosen stays with the reviewers.

- [X] T056 Remove the severity cap from `PANEL`: delete `capped_severity` and `TriggerClass.RARE`, remove `Finding.severity_capped`, keep the merged finding's severity, and drop "lowered from high" from `badges` and `render_issue`. Remove `severity_capped` from `SKILL_DIR/schemas/report.schema.json`.
- [X] T057 Add to `PANEL` a frozen `ExtentRow` record (`input`, `expected`, `actual`) and the verdict fields `reproduction` (string or null) and `extent` (tuple of `ExtentRow`), and the same two fields on `Finding`. Add `representative_evidence`: the reproduction and extent of the first non-refuting verdict that recorded them, preferring a reproduced one; tables are not merged. Add both fields to `verification.schema.json` (required, nullable or empty) and `report.schema.json`.
- [X] T058 Add validation rule 5 of data-model.md to `semantic_errors` in `PANEL`: a verdict with `evidence: reproduced` has a non-empty `reproduction`. Add the fixture `MSG/invalid/verification-reproduced-without-code.json` and its expected message to `tests/test_sci_review_panel.py`.
- [X] T059 Render the evidence: in the report block, an "**Extent.**" table and a fenced "**Reproduction.**" after the bullets; in the issue, the extent table under "Who hits this and when" and "To check it, run:" with the fenced reproduction under "Reproduction". The fence is longer than any run of backquotes in the code.
- [X] T060 Replace the cap tests in `PRACTICAL_TESTS` with `TestSeverityIsTheReviewers` (no trigger class changes the severity) and `TestEvidence` (reproduced verdict required to carry code, reproduced verdict preferred, refuting verdicts give no evidence, fence length). Give the golden practical run a reproduced verdict with an extent table, add the reproduction and extent to `MSG/valid/verification.json` and the verify-test helper, and regenerate the golden outputs.
- [X] T061 Update the briefs and the protocol: the six finder briefs' severity sentence (no release or operator-change downgrade; judge ordinary use from what was read) and in-practice instruction (users' terms, most common manifestation first, cite where inputs come from or say frequency is unknown); the verifier's reproduction and extent instructions and JSON example; `protocol.md` sections 3.1 and 4; remove the release-only severity row from `dimensions/algorithmic-correctness.md`. Regenerate `plugins/sci-review/scripts/scientific-review-panel.js`.
- [X] T062 Update `plugins/sci-review/README.md` and `CHANGELOG.md` for the removed cap and the added evidence; update spec.md (Story 2, FR-002 to FR-004, SC-002, Assumptions), research.md (R3, R5, R8, R12 C6, R13), data-model.md, contracts, quickstart.md and plan.md.
- [X] T063 Add the second downstream issue to the private case file kept outside the repository, with its baseline body, the reviewer's comments and its expected trigger class (`data-condition`). Nothing about it enters this repository beyond generic wording.

## Phase 10: Gaps found by the first validation (research R14)

**Purpose**: Make the issue agree with the review's own evidence, then re-validate on a fixture that can fail, and render new issues that supersede the criticised ones.

- [X] T064 [US6] Add `in_practice_revision` (string or null, required key) to the verdict in `SKILL_DIR/schemas/verification.schema.json` and `VerdictRecord`; add `in_practice_original` to `Finding` and `report.schema.json`. In `adjudicate_verified`, when a non-refuting verdict carries a revision, set `in_practice` to the first such revision and `in_practice_original` to the finder's statement.
- [X] T065 [US6] Render "(Revised by the verifier.)" after a revised in-practice statement in `finding_block` and `render_issue`.
- [X] T066 [US6] Owners: introduce history owners as "Last changed these lines (git blame)"; detect one commit for every cited line whose subject ends in `(#N)` or `!N` and add the merged-pull-request sentence (contracts/issue.md).
- [X] T067 [US6] `panel.py issue --supersedes REF` (repeatable): open the body with "Supersedes REF, REF." after the title.
- [X] T068 [US6] Tests in `PRACTICAL_TESTS` for T064 to T067; extend the golden practical run with a revised verdict; regenerate golden outputs.
- [X] T069 [US6] Briefs: finders never drop a concrete defect on rarity, cite per-file line numbers, and consider code releases for cached or stored results; the verifier writes `in_practice_revision` when reach contradicts the statement, and treats rarity as no ground for refutation; the algorithmic-correctness stale-caching check names releases. Update `protocol.md` section 3.1. Regenerate the Workflow script.
- [X] T070 Rebuild `tests/fixtures/sci-review/practical-repo/` (build.py, manifest.json) per research R14 item 7: a JSON-file store that persists across processes, a stored-result case triggered by a code release or a configuration change, a deliberate-reuse case, a unit-conversion rounding case, and a correct look-alike for each.
- [X] T071 Update README, CHANGELOG, plan.md and quickstart.md for Phase 10.
- [X] T072 Re-run quickstart scenario 5 (five practical runs and one seeded run) and scenario 6 (both downstream cases); record SC-002, SC-003, SC-005 and SC-008 and the downstream table in validation.md, section 6, anonymised.
- [X] T073 Render the two downstream issues with `--supersedes`, unedited, and save them beside the private case file for the user to file.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: none.
- **Foundational (Phase 2)**: depends on Setup; blocks every story.
- **US1, US2 and US3 (Phases 3 to 5)**: depend on Phase 2 only. They touch different functions of `PANEL`, except that `render_markdown` is edited by T018 (US1), T029 (US3) and T036 (US4). Do those three tasks in that order.
- **US4 (Phase 6)**: depends on Phase 2. T036 builds on the block layout of T018 (US1).
- **US5 (Phase 7)**: depends on US1 (prose fields in `report.json`). It reads `severity_capped` (US2), `value_corrections` (US3) and `kind` (US4) when present, and renders without them otherwise, so it can start after US1.
- **Polish (Phase 8)**: T048 and T049 after all stories; T050 can start any time after Phase 2; T051 after T048 to T050; T052 after T051; T053 to T055 last.

### Within Each User Story

- Tests are written first and fail.
- Then come record or adjudication changes in `PANEL`, then rendering, then briefs and `protocol.md`. Brief tasks marked [P] can run alongside the `PANEL` tasks.

### Parallel Opportunities

- T005 to T009 (one schema each) in parallel.
- In US1: T013 to T017 in parallel (fixtures, tests and briefs are in different files).
- In US2: T021 to T023 together, and T025 with T026.
- In US4: T037 to T040 in parallel with each other once T035 is under way.
- In US5: T041 to T043 together.
- In Polish: T053 and T054 together.

## Parallel Example: User Story 1

```text
T013 golden practical run      (MSG/golden/practical/)
T014 report-layout tests       (PRACTICAL_TESTS)
T016 finder briefs             (SKILL_DIR/roles/*.md)
T017 moderator brief           (SKILL_DIR/roles/moderator.md)
then: T018 render_markdown → T019 report_findings → T020 protocol.md
```

## Implementation Strategy

### MVP (User Story 1)

Phases 1 and 2, then Phase 3. Every finding opens in plain words, which addresses the reviewer's main complaint on its own. Validate with a single live run on `seeded-repo` before going further.

### Incremental Delivery

1. US1: orientation (MVP).
2. US2 and US3 together: severity on use, and reach with value checks. They share the verdict fields from Phase 2.
3. US4: design questions.
4. US5: the issue command.
5. Polish: regenerate, fixtures, the downstream evaluation, release metadata.

Each step leaves the test suite green and the plugin releasable.
