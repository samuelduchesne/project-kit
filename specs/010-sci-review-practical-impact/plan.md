# Implementation Plan: Findings that say who hits them

**Branch**: `claude/awesome-einstein-7157bt` (spec directory `010-sci-review-practical-impact`) | **Date**: 2026-11-26 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/010-sci-review-practical-impact/spec.md`, plus the planning directive to "include a quick evaluation where we'll reproduce the sci-review on the same module as the one in the initial feedback and compare the proposed issue".

## Summary

Every sci-review finding gains three statements, written by the finder who already read the code:

- `headline`: the situation in plain words, used as the title;
- `context`: what the code does for its users and when the problem arises;
- `in_practice`: who or what triggers it, how often, and whether anyone would notice.

Verifiers gain a reach step. They read configuration, environment, deployment and release files. They classify the trigger (`user-action`, `data-condition`, `release`, `operator-change` or `unreachable`). They correct any quoted value that the repository contradicts. They may mark a finding as possibly intended.

`panel.py` turns these into deterministic outcomes:

- evidence a reader can check: the verifier's runnable reproduction and a short table of inputs with expected and actual results;
- a verifier revision of the in-practice statement when its reach contradicts it, and owner text that says what blame shows (research R14);
- a "Design questions" section for marked findings;
- a report that leads with prose;
- a new `issue` command that renders a finding as an issue body, in the order a domain reader needs, with owners from CODEOWNERS or `git blame`. Nothing is posted.

No agent is added, and the protocols, labels and levels of features 007 to 009 are unchanged apart from rule 2a ([research.md](./research.md) R6).

A quick evaluation closes the feature (research R12, [quickstart.md](./quickstart.md) scenario 6). It re-runs a `medium` review on the module and commit behind the criticised issue, renders the matching finding as an issue, and compares that issue with the one originally filed. The downstream project is private to the evaluator: its identity and inputs live in a case file outside this repository (research R12), and `validation.md` records only anonymised results. The comparison uses a seven-criterion rubric drawn from the domain reviewer's comment, scored partly by script and partly by a blind judge agent.

## Technical Context

**Language/Version**: Markdown briefs and skill; Python 3.10+ standard library for `scripts/panel.py` and `scripts/build_workflow.py`; JavaScript (ES2022) for the generated Workflow script.

**Primary Dependencies**: As in feature 009. `git` is used read-only by `panel.py issue` for `blame`, and is optional (research R9).

**Storage**: Run directory under the system temporary directory (unchanged). Issue drafts are written to `<run>/issues/`.

**Testing**: `unittest`.
- A new file, `tests/test_sci_review_practical.py`.
- Updates to `test_sci_review_panel.py`, `test_sci_review_verify.py` and `test_sci_review_workflow_build.py`. Their golden reports change by layout only.
- New message fixtures under `tests/fixtures/sci-review/messages/{valid,invalid,golden/practical}/`.
- A new live fixture, `tests/fixtures/sci-review/practical-repo/`, built like `seeded-repo` (`build.py`, `manifest.json`), with three cases (quickstart scenario 5). It is separate so that the 16-defect baseline of `seeded-repo` stays comparable.
- Live runs and the downstream-case evaluation are manual, recorded in `validation.md`, consistent with features 008 and 009.

**Target Platform**: As in feature 007: Claude Code, claude.ai chat and Cowork, Codex.

**Project Type**: Agent plugin (skills, helper script, generated workflow).

**Performance Goals**: Panel agent count and the agent estimate are unchanged (FR-013). Subagent tokens may rise by the reach step's reading: the budget is no more than 15% more subagent tokens for the whole panel on the seeded fixture than feature 009 (725,233), measured in scenario 5. More than that is reported in `validation.md`, but it does not fail the feature.

**Constraints**: Read-only on the reviewed project, except under `--fix` (unchanged). `issue` never posts. Earlier runs keep rendering (FR-012).

**Scale/Scope**: About 25 files. Six finder briefs, the moderator, verifier and defender briefs, one dimension document, `protocol.md`, `SKILL.md`, five schemas, `panel.py` (records, validation, adjudication, report, a new subcommand), the regenerated Workflow script, tests and fixtures.

No item remains marked NEEDS CLARIFICATION; research.md resolves each design choice.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitution version 1.3.0.

| Principle | Check | Result |
|-----------|-------|--------|
| I. Templates are the source of truth | `sci-review` generates no project files. | Not applicable (Scope and Constraints) |
| II. Scripts for predictable steps, the model for judgment | Agents make the judgments: they write the prose, check reach, classify the trigger and mark intent. `panel.py` does everything deterministic, with logged arguments: combining trigger classes, choosing the reported evidence, routing design questions, rendering, matching CODEOWNERS and counting blame. `issue` writes a file, so it accepts `--dry-run`. | Pass |
| III. Show before changing | `issue` writes only to the run directory and posts nothing. The user files the issue. No new write to the project. | Pass |
| IV. Works wherever it is installed | Owners need only files and `git`. Without `git`, `issue` says so and lists no owners. No new tool is installed or pinned. Extension briefs keep working, because schema validation returns missing fields to the agent (research R11). | Pass |
| Development workflow | Spec-kit flow; CHANGELOG entry under `[Unreleased]`; `claude plugin validate` on both plugins; `sci-review` minor version bump (0.3.0 to 0.4.0): new required fields in messages, a new subcommand and a changed report layout. | Pass |

**Post-design re-check (after Phase 1)**: Pass. The design adds no agent, no network access and no write outside the run directory. The one protocol change, rule 2a, is deterministic and lives in `panel.py`.

## Project Structure

### Documentation (this feature)

```text
specs/010-sci-review-practical-impact/
├── plan.md               # This file
├── research.md           # Phase 0: decisions R1 to R12, including the evaluation design
├── data-model.md         # Phase 1: record and schema changes
├── quickstart.md         # Phase 1: validation scenarios 1 to 6 (6 = downstream case)
├── contracts/
│   ├── issue.md          # panel.py issue: synopsis, body layout, owners, exit codes
│   └── report-layout.md  # report.md layout, ReportFindings mapping, brief text
├── checklists/
│   └── requirements.md
├── validation.md         # written after implementation (scenarios 5 and 6)
└── tasks.md              # Phase 2 (/speckit-tasks)
```

### Source Code (repository root)

```text
plugins/sci-review/
├── .claude-plugin/plugin.json                 # 0.4.0
├── .codex-plugin/plugin.json                  # 0.4.0
├── README.md                                  # findings in plain words; design questions; issue command
├── scripts/
│   ├── panel.py                               # records, validate rules, rule 2a, trigger class, evidence, report layout, `issue`
│   ├── build_workflow.py                      # unchanged logic; regenerate
│   └── scientific-review-panel.js             # regenerated (schemas and briefs embedded)
└── skills/scientific-review/
    ├── SKILL.md                               # delivery step offers `issue`
    ├── protocol.md                            # §4 severity; §5.1 rule 2a, trigger class and evidence; report section
    ├── dimensions/algorithmic-correctness.md  # stale-cache intent check
    ├── roles/{theorist,numerical-analyst,experimentalist,methodologist,computer-scientist,generalist}.md
    ├── roles/{moderator,verifier,defender}.md
    └── schemas/{candidate-findings,merge-ruling,verification,debate-positions,report}.schema.json
tests/
├── test_sci_review_practical.py               # new
├── test_sci_review_{panel,verify,workflow_build}.py
└── fixtures/sci-review/
    ├── messages/{valid,invalid,golden/practical}/
    └── practical-repo/                        # new live fixture (build.py, manifest.json)
CHANGELOG.md
```

**Structure Decision**: The feature extends the existing `plugins/sci-review` tree. Judgment goes into the briefs, and deterministic outcomes go into `panel.py`, as in features 008 and 009.

## Phases after this plan

1. **Tasks** (`/speckit-tasks`), ordered as follows:
   - schemas and records;
   - `validate`;
   - adjudication (rule 2a, trigger class, evidence);
   - report layout;
   - `issue`;
   - briefs, `protocol.md` and `SKILL.md`;
   - regenerate the Workflow script;
   - fixtures and tests;
   - live fixture runs (scenario 5);
   - the downstream-case evaluation (scenario 6);
   - CHANGELOG and version.
2. **Evaluation** (scenario 6) runs last, on the finished plugin. Its result decides whether the feature is ready for review. If C2, C4 or C7 fails, the corresponding brief or rule is revised and the evaluation is run once more before the pull request.

## Complexity Tracking

No constitution violations.
