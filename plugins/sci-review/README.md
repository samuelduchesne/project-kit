# sci-review

sci-review reviews code for scientific correctness. A panel of independent reviewers examines a branch, a whole repository or named paths, debates every candidate finding, and reports only findings that carry a concrete failure scenario, each labelled by the panel's measured agreement. Style, formatting, naming, lint and documentation are out of scope: a finding is reported only when it affects a computed result.

The plugin runs on Claude (Claude Code, the Claude desktop app, claude.ai chat and Cowork) and on Codex. It contains:

| Component | Name | Role |
|-----------|------|------|
| Skill | `scientific-review` | Entry point; orchestrates the review on every host |
| Agent | `scientific-auditor` | Panel member used by the `claude-agents` runner |
| Workflow | `scientific-review` | Panel phases for the `claude-workflow` runner |
| Script | `scripts/panel.py` | Deterministic steps: scope, panel limits, extension selection, validation, merge, adjudication, report |
| Script | `scripts/build_workflow.py` | Regenerates the workflow script, which embeds the protocol, role briefs, dimension documents and message schemas |

Version: 0.1.0.

## 1. Install

### 1.1 Claude Code

From a shell:

```bash
claude plugin marketplace add samuelduchesne/project-kit
claude plugin install sci-review@project-kit
```

Inside a session:

```text
/plugin marketplace add samuelduchesne/project-kit
/plugin install sci-review@project-kit
```

In claude.ai and the Claude desktop app, add the marketplace `samuelduchesne/project-kit` under **Customize > Plugins** and add **sci-review** from it.

### 1.2 Codex

The repository ships a Codex marketplace at `.agents/plugins/marketplace.json`, which lists `sci-review` only. Add it with:

```bash
codex plugin marketplace add samuelduchesne/project-kit
```

and then install `sci-review` from that marketplace:

```bash
codex plugin add sci-review@project-kit
```

## 2. Usage

Ask for a scientific review in plain language, for example:

- "Review this branch for scientific correctness."
- "Check the numerical stability of src/solver."
- "Review the whole repository, a quick review with the theorist and the numerical analyst."
- "Check this pipeline for data leakage."

On Claude the skill is `sci-review:scientific-review`; on Codex it is `scientific-review` from the `sci-review` plugin.

## 3. Dimensions

Every perspective reviews the full scope across five dimensions. Each dimension has a document under `skills/scientific-review/dimensions/` with language-neutral checks followed by worked examples in Python and TypeScript.

| Dimension | Document | Examples of defects |
|-----------|----------|---------------------|
| Mathematical derivations | `mathematical-derivations.md` | An implemented formula that differs from its derivation or cited source |
| Numerical stability | `numerical-stability.md` | Catastrophic cancellation, overflow, division near zero, floating-point equality |
| Physical modelling and units | `physical-modelling-and-units.md` | Unit mismatches, violated stability limits, Celsius used as an absolute temperature |
| Statistical integrity | `statistical-integrity.md` | Data leakage, preprocessing fitted before the split, mutated caller data |
| Algorithmic correctness | `algorithmic-correctness.md` | Non-termination, off-by-one indices, order dependence, stale caches |

## 4. Panel

The full protocol is defined once, in `skills/scientific-review/protocol.md`; every runner follows it.

### 4.1 Roles

| Role | Number | Responsibility |
|------|--------|----------------|
| Perspective reviewer | 2 to 7 | Reviews the scope independently from one perspective and raises candidate findings. The defaults are `theorist`, `numerical-analyst`, `experimentalist`, `methodologist` and `computer-scientist`; selected domain extensions add further perspectives. |
| Defender | 1, always present | Argues that each finding is not a defect. Never raises findings and never withdraws. |
| Moderator | 1, always present | Merges duplicate candidates and writes notes on each finding after its debate. Never introduces findings and never assigns labels. |

The role briefs are under `skills/scientific-review/roles/`.

### 4.2 Phases

1. **Independent round.** Each perspective reviews the scope without access to any other reviewer's output and writes one candidate-findings message.
2. **Debate.** `panel.py merge` clusters candidates by location (same file, line ranges within three lines) and groups the clusters into debate batches by file. For each batch, the moderator confirms or splits each cluster. The perspectives and the defender then state positions on every merged finding in round 0, followed by at most `rebuttal_rounds` rebuttal rounds. A batch stops early when no stance changes in a round. The moderator then writes notes on every finding of the batch.
3. **Adjudication.** `panel.py adjudicate` computes each finding's label, or rejects it, from the recorded positions. No model takes part in this step.

Every panel message conforms to a JSON Schema under `skills/scientific-review/schemas/`. A message that fails validation is returned once to its author; a second failure drops it, and the report records a notice.

### 4.3 Severity

| Severity | Definition |
|----------|------------|
| High | Produces a wrong result under realistic inputs. |
| Medium | Produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result. |
| Low | A latent risk that does not currently produce a wrong result. |

### 4.4 Agreement labels

A member's stance on a finding is its latest position (`accept`, `challenge` or `withdraw`). "Perspectives" means every perspective reviewer in the panel, default and domain, including the raiser, and never the defender; the majority denominator is the number of perspectives in the panel. A defender objection is a defender `challenge`; it is answered when a later perspective position responds to it and the defender does not challenge again afterwards.

The rules apply in order, and the first that matches decides:

1. Every raiser withdrew: the finding is rejected (`withdrawn`).
2. No perspective other than the raisers accepts, and a defender objection is unanswered: the finding is rejected (`unsupported`).
3. The finding has no concrete trigger or no wrong output: label `contested`.
4. No perspective challenges or withdraws, at least two perspectives accept, and no defender objection is unanswered: label `consensus`.
5. More than half of the perspectives accept: label `majority`.
6. Otherwise: label `contested`.

Labels are computed by `panel.py adjudicate` only; the orchestrating model never assigns, raises or lowers a label. Contested findings carry the moderator's argument for, argument against and deciding assumption.

## 5. Runners

A runner executes the panel phases on a given host. The skill selects the first available runner in this order:

| Order | Runner | Condition | Independence |
|-------|--------|-----------|--------------|
| 1 | `claude-workflow` | The `Workflow` tool is available and `sci-review:scientific-review` is listed as a workflow | Independent agents |
| 2 | `codex-subagents` | Running in Codex with multi-agent tools enabled | Independent agents |
| 3 | `claude-agents` | The `Agent` tool is available with the `sci-review:scientific-auditor` agent | Independent agents |
| 4 | `sequential` | Otherwise (claude.ai chat, Cowork, Codex with agents disabled) | Not independent |

The following rules modify the selection:

1. A user request for the review satisfies the Workflow opt-in requirement. A review started on the model's own initiative asks first, because it spawns many agents.
2. The user may force a lower runner. "Run it without agents" selects `sequential`; a request for agents but not the Workflow selects `claude-agents`.
3. When a multi-agent runner cannot spawn its agents, the review falls back to `sequential` with the same perspectives, rounds and batches.

The `sequential` runner plays every role in one conversation, so its perspectives are not independent. The report then carries a reduced-independence notice. The runner documents are under `skills/scientific-review/runners/`.

## 6. Arguments

All arguments are optional and are read from the request.

| Argument | Default | Limits and examples |
|----------|---------|---------------------|
| `mode` | `branch` | `branch`, `repository` ("review the whole repository") or `paths` ("review src/solver") |
| `baseline` | Resolved from the default branch by `panel.py scope` | Branch mode only; "since v1.2" sets the baseline to `v1.2` |
| `paths` | None | Required in `paths` mode |
| `perspectives` | The five defaults plus selected extensions | 2 to 7 in total |
| `rebuttal_rounds` | 2 | 0 to 3 |
| `max_batches` | 2 | 1 to 4 |
| `models` | None | `claude-workflow` runner only, as `role=model` pairs |
| Line budget | 6,000 lines | Files beyond the budget are recorded as not reviewed |
| Keep the run directory | No | When requested, the run directory is kept and its path is given |

Out-of-range values are clamped, and the report states the panel actually used. Branch mode requires git; when the project is not a git repository, or no base can be determined, the skill asks the user for a baseline or for another mode and never switches modes silently.

## 7. Report

The report contains eight sections, in this order:

1. **Scope.** What was reviewed, the runner, and whether the perspectives were independent agents.
2. **Panel.** The perspectives used (with their source), the rebuttal rounds and the batches.
3. **Extensions.** Domain extensions selected, not applicable, failed (with the reason) and recommended (with what each would add).
4. **Findings.** Ordered consensus, majority, contested, and within each label high, medium, low. Each finding gives its location, dimension, severity, summary, trigger, wrong output, fix, raisers and label.
5. **Rejected findings.** Identifier, summary, raisers and reason.
6. **Checked and found correct.** Locations the panel examined and confirmed, with the dimension and a note.
7. **Not reviewed.** Paths outside the review, with the reason (over budget, outside the named paths, generated or vendored).
8. **Notices.** Reduced independence, languages without worked examples, missing tools, and messages dropped after failed validation.

When no reviewable scientific code changed, the report contains sections 1 to 3 and the sentence "No reviewable scientific code changed in this scope." In Claude Code the findings are delivered through `ReportFindings` and the other sections as Markdown; on other hosts the whole report is Markdown, with one table per label.

## 8. Read-only guarantee

The review never creates, modifies or deletes a file in the reviewed project. Every panel message is written to a run directory under the system temporary directory, which is deleted at the end unless the user asks to keep it. In a git repository the skill records `git status --porcelain --ignored` before the review and compares it afterwards, and reports any file that changed, including ignored files such as a bytecode cache. Panel members run Python checks with `python3 -B`, so that they write no `__pycache__` in the project. The review runs no simulation or long computation in the project unless the user requests it.

## 9. Requirements

- `python3` 3.10 or later for `scripts/panel.py`. Without it, the deterministic steps are performed by hand from the written rules of `protocol.md` section 10, and the report records a notice.
- `git` for branch mode. Repository and paths modes work without a git repository.

## 10. Domain extensions

Any installed plugin, for Claude or for Codex, can add a domain perspective by shipping one skill named `<domain>-sci-review-extension` with an `extension.json` declaration. A selected extension contributes one perspective with its own brief, reference documents and optional domain checks; it reviews and debates on the same terms as the default perspectives and counts toward the panel limit and the majority denominator. No change to sci-review is needed.

The authoritative contract, version 1, is [`skills/scientific-review/extensions.md`](skills/scientific-review/extensions.md). The first extension, `building-energy-sci-review-extension`, ships in the idfkit plugin (`idfkit@idfkit`) and is released separately.

## 11. Releases

sci-review is versioned independently of project-kit. Releases are tagged `sci-review-vX.Y.Z`.
