# Implementation Plan: sci-review plugin

**Branch**: `007-sci-review-plugin` | **Date**: 2026-11-04 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/007-sci-review-plugin/spec.md`, plus the planning directive that the solution use multi-agent workflows on both Claude and Codex.

## Summary

`sci-review` is a second plugin in the project-kit marketplace, shipped with a Claude manifest and a Codex manifest from one source tree. A review is a panel protocol (independent round, debate, adjudication) defined once, as role briefs and JSON message schemas in the `scientific-review` skill, and executed by one of four interchangeable runners:

1. **Claude Workflow runner**: a Workflow script, `workflows/scientific-review.js`, runs each panel role as a separate agent, the independent round in parallel, and the debate as a pipeline over debate batches. It returns every panel message; the orchestrating conversation writes them into the run directory with `panel.py ingest`, and adjudication and the report then run through `panel.py` as on the other runners.
2. **Codex subagent runner**: the skill instructs Codex to spawn one subagent per panel role, in parallel, using Codex's native subagent capability; messages are exchanged as JSON files in a temporary run directory outside the project.
3. **Claude Agent runner**: where the Workflow tool is unavailable but the Agent tool is present, the skill spawns `scientific-auditor` agents in parallel, one per role.
4. **Sequential runner**: where no multi-agent capability exists (claude.ai chat, Cowork, Codex with agents disabled), the skill performs each role in turn and the report carries the reduced-independence notice.

All runners share the deterministic steps, which run through a stdlib Python script, `scripts/panel.py`: scope resolution, extension selection, message validation, location-based duplicate clustering, debate batching, agreement-label computation from recorded positions, and report rendering. The model performs only the reviewing, the debating, the semantic merge confirmation and the moderator's notes. Two deterministic steps must also run inside the Workflow script, because a Workflow cannot call `panel.py` between agent calls: location clustering, grouping clusters into debate batches, and the debate stop rule. They are written once in a marked pure section of the script and tested for parity with `panel.py` on the same fixtures. Domain extensions are skills, named `<domain>-sci-review-extension`, that any plugin can ship; the first is delivered in the idfkit plugin.

## Technical Context

**Language/Version**: Markdown skills and agent definitions; JavaScript (ES2022) for the Claude Workflow script; Python 3.10+ standard library for `scripts/panel.py` and its generator; TOML for the Codex role definitions shipped as optional templates.

**Primary Dependencies**: Claude Code Workflow and Agent tools (optional); Codex subagents, `agents.enabled` (optional); `git` for diff scope; `python3` for deterministic steps (optional, with a written fallback); the idfkit MCP server or `idfkit` Python package for the idfkit extension's model checks.

**Storage**: None in the reviewed project (FR-006). Runner messages are JSON files in a run directory under the system temporary directory, removed at the end of the review.

**Testing**: `unittest` for `scripts/panel.py` (fixtures of panel messages, golden reports); a drift check that the generated Workflow script embeds the current role briefs and schemas; a parity test that runs the Workflow script's pure section under Node.js and compares its clustering, batching and stop-rule results with `panel.py` on the same fixtures; `claude plugin validate --strict` on the marketplace and both plugins; a manifest check for the Codex manifest and Codex marketplace; a seeded fixture repository (Python and TypeScript, five dimensions, look-alikes, one contested construct, building-energy defects, and a reproduction check per High-severity defect for SC-007) exercised manually per the quickstart, consistent with the constitution's deferral of automated evals.

**Target Platform**: Claude Code (CLI, desktop, IDE), claude.ai chat and Cowork through the sequential runner; Codex CLI, IDE extension and app through the Codex subagent runner.

**Project Type**: Agent plugin (skill, agent, workflow, helper script) distributed through a marketplace.

**Performance Goals**: The default panel (five perspectives, defender, moderator, two rebuttal rounds, two batches) completes a branch review of up to 2,000 changed lines with at most 45 agent invocations; the largest permitted panel (seven perspectives, three rebuttal rounds, four batches) needs at most 143 (bound derived in research R7). Agent invocations grow with rounds and debate batches, not with findings.

**Constraints**: Read-only on the reviewed project; no role may receive another perspective's independent-round output (SC-011); the skill alone must produce a complete review; panel size between 2 and 7 perspectives, rebuttal rounds between 0 and 3.

**Scale/Scope**: Five dimensions, five default perspectives, a defender, a moderator; up to two extensions per review in practice; at most two debate batches per review by default.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The constitution (1.1.1) scopes the repository to project creation and maintenance and places the plugin under `plugins/project-kit/`. This feature depends on a MINOR amendment (spec, Dependencies) that widens the scope to a marketplace of plugins and records `sci-review`'s scope. The amendment is the first task of the implementation and is a precondition of the gate below.

| Principle | Check | Result |
|-----------|-------|--------|
| I. Templates are the source of truth | `sci-review` generates no project files. | Not applicable (recorded in the amendment) |
| II. Scripts for predictable steps, the model for judgment | Scope resolution, extension selection, message validation, clustering, batching, agreement labels and report rendering run in `scripts/panel.py` with logged arguments. The model reviews, debates, confirms semantic duplicates and writes the moderator's notes. The Workflow script is generated from the skill's role briefs and schemas, so the protocol has one source; its two in-script deterministic steps are tested for parity with `panel.py`. | Pass. Every subcommand that creates, writes or removes files (`init`, `scope`, `select-extensions`, `panel`, `ingest`, `adjudicate`, `report`, `clean`) and `build_workflow.py` accept `--dry-run`, which prints the paths and contents they would write or remove and changes nothing. They write only to the run directory outside the project, except `build_workflow.py`, which writes the plugin's own Workflow script. |
| III. Show before changing | The review modifies nothing in the project (FR-006, SC-004); it requires no clean tree. | Pass |
| IV. Works wherever it is installed | The skill alone completes a review (sequential runner). Workflow, agents and Codex subagents are optional accelerators. Missing `python3` or `git` is detected at start and reported, with the written fallback rules for the script's steps. CI pins the Claude Code version. The Codex manifests are checked statically by `check_manifests.py`, so CI calls no Codex CLI and none needs pinning. | Pass |
| Development workflow | Spec-kit flow followed; CHANGELOG entry; `claude plugin validate` extended to the second plugin; `sci-review` carries its own `version`. | Pass, with the release-tag rule clarified in the amendment (per-plugin tags, `sci-review-vX.Y.Z`). |

**Post-design re-check (after Phase 1)**: Pass. The design adds a Codex manifest and a Codex marketplace file; neither introduces a core dependency on an environment-specific component. The Codex role TOML files are optional templates the user may copy, never written by the plugin (Principle III).

## Project Structure

### Documentation (this feature)

```text
specs/007-sci-review-plugin/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── invocation.md            # skill arguments, runner selection, Workflow args
│   ├── panel-messages.md        # role inputs and outputs, JSON schemas
│   ├── panel-cli.md             # scripts/panel.py subcommands
│   ├── extension.md             # domain-extension contract
│   ├── codex-orchestration.md   # Codex subagent runner protocol
│   └── report.md                # report sections and ReportFindings mapping
└── tasks.md                     # produced by /speckit-tasks
```

### Source Code (repository root)

```text
.claude-plugin/marketplace.json          # adds the sci-review entry
.agents/plugins/marketplace.json         # new: Codex marketplace, lists sci-review only
.github/workflows/validate.yml           # validates and smoke-installs sci-review
.github/scripts/check_manifests.py       # extended to several plugins and the Codex manifest
.specify/memory/constitution.md          # MINOR amendment

plugins/sci-review/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── skills/scientific-review/
│   ├── SKILL.md                         # entry point, runner selection, report rules
│   ├── protocol.md                      # phases, labels, limits (single source)
│   ├── roles/                           # one brief per panel role
│   │   ├── theorist.md
│   │   ├── numerical-analyst.md
│   │   ├── experimentalist.md
│   │   ├── methodologist.md
│   │   ├── computer-scientist.md
│   │   ├── defender.md
│   │   └── moderator.md
│   ├── dimensions/                      # loaded on demand (FR-003)
│   │   ├── mathematical-derivations.md
│   │   ├── numerical-stability.md
│   │   ├── physical-modelling-and-units.md
│   │   ├── statistical-integrity.md
│   │   └── algorithmic-correctness.md
│   ├── schemas/                         # JSON Schema for every panel message
│   │   ├── candidate-findings.schema.json
│   │   ├── debate-positions.schema.json
│   │   ├── merge-ruling.schema.json
│   │   ├── moderator-notes.schema.json
│   │   └── report.schema.json
│   ├── runners/
│   │   ├── claude-workflow.md
│   │   ├── claude-agents.md
│   │   ├── codex-subagents.md
│   │   └── sequential.md
│   └── codex-agents/                    # optional templates for ~/.codex/agents/
│       └── sci-review-panelist.toml
├── agents/scientific-auditor.md         # takes any role given its brief
├── workflows/scientific-review.js       # GENERATED section from roles/, protocol.md, schemas/; PURE section tested for parity
└── scripts/
    ├── panel.py                         # deterministic steps (contracts/panel-cli.md)
    └── build_workflow.py                # regenerates workflows/scientific-review.js

tests/
├── test_sci_review_panel.py
├── test_sci_review_workflow_build.py    # drift test and Node.js parity test
└── fixtures/sci-review/
    ├── messages/                        # panel message fixtures and golden reports
    ├── seeded-repo/                     # build.py, manifest.json, score.py, reproduction checks
    └── test-extension-plugin/           # extension written only against the contract (SC-013)

# Separate repository: idfkit/idfkit-plugin (planned here, released there)
skills/building-energy-sci-review-extension/
├── SKILL.md                             # extension declaration and instructions
├── extension.json                       # machine-readable declaration
├── perspective.md                       # building physicist brief
├── checks.md                            # idfkit model checks (FR-034)
└── reference/building-energy.md
tests/fixtures/sci-review/               # building-energy seeded defects
```

**Structure Decision**: One plugin directory serves both hosts: Claude reads `.claude-plugin/plugin.json` (skills, agents, workflows) and Codex reads `.codex-plugin/plugin.json` (skills). The protocol lives in the skill's Markdown and JSON files; the Workflow script is a generated artefact, checked for drift in CI, because Workflow scripts cannot read plugin files at run time.

## Complexity Tracking

| Item | Why Needed | Simpler Alternative Rejected Because |
|------|------------|-------------------------------------|
| Four runners | FR-027 and FR-028 require parallel agents where available and a sequential path elsewhere; the user requires Claude and Codex multi-agent execution. | A single sequential runner fails FR-027 and SC-011; a Workflow-only runner fails on Codex and on Claude surfaces without Workflow. |
| Generated Workflow script | The protocol must be identical across runners. | Hand-maintaining prompts in JavaScript and Markdown would let the runners drift. |
| Clustering, batching and stop rule duplicated in JavaScript | A Workflow cannot call `panel.py` between agent calls, and the debate pipeline needs clusters, batches and the stop rule mid-run. | Calling a helper agent to run `panel.py` adds agent invocations per batch and round; a Node.js parity test bounds the drift risk instead. Labels and the report stay in `panel.py` only. |
| Second marketplace file for Codex | Codex reads `.agents/plugins/marketplace.json`; listing only `sci-review` there prevents Codex from offering `project-kit`, which has no Codex manifest. | Relying on Codex's legacy read of `.claude-plugin/marketplace.json` would expose `project-kit` to Codex. |

## Constitution Check (post-implementation)

Re-checked on 2026-11-04 against constitution 1.2.0 and the implemented files.

| Principle | Evidence | Result |
|-----------|----------|--------|
| I. Templates are the source of truth | `sci-review` writes no project files; the amendment records that Principle I does not apply to it. | Not applicable |
| II. Scripts for predictable steps | `scripts/panel.py` implements scope, extension selection, panel limits, validation, clustering, batching, adjudication and the report, logs its arguments, and gives `--dry-run` on `init`, `scope`, `select-extensions`, `panel`, `ingest`, `adjudicate`, `report`, `clean` and `notice`; `build_workflow.py` has `--dry-run` and `--check`. The Workflow script's pure section is tested for parity with `panel.py` under Node.js. | Pass |
| III. Show before changing | Every run file is under the system temporary directory; `init` refuses a run directory inside the project; the tests assert that the reviewed tree is unchanged; the skill compares `git status --porcelain` before and after. | Pass |
| IV. Works wherever it is installed | The sequential runner and the written fallback rules (protocol.md section 10) need neither agents nor `python3`; Workflow, agents and Codex subagents are optional; missing `git` or `python3` and an undeterminable base are reported with the alternatives. CI keeps the pinned Claude Code version; Codex manifests are checked statically. | Pass |
| Development workflow | CHANGELOG entries under Unreleased; `claude plugin validate` runs on both plugins in CI; `sci-review` carries its own version and the per-plugin tag rule. | Pass |
