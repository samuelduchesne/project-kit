# sci-review

sci-review reviews code for scientific correctness. A panel of independent reviewers examines a branch, a pull request, a whole repository or named paths, debates every candidate finding, and reports only findings that carry a concrete failure scenario, each labelled by the panel's measured agreement. Style, formatting, naming, lint and documentation are out of scope: a finding is reported only when it affects a computed result.

The plugin runs on Claude (Claude Code, the Claude desktop app, claude.ai chat and Cowork) and on Codex. It contains:

| Component | Name | Role |
|-----------|------|------|
| Skill | `scientific-review` | Entry point; orchestrates the review on every host |
| Agent | `scientific-auditor` | Panel member used by the `claude-agents` runner |
| Script | `scripts/scientific-review-panel.js` | Panel phases for the `claude-workflow` runner; not registered as a workflow, it is copied to the session's scratchpad and launched by path |
| Script | `scripts/panel.py` | Deterministic steps: arguments and preferences, scope and targets, review parts, panel levels and limits, extension selection, validation, merge, adjudication, report |
| Script | `scripts/build_workflow.py` | Regenerates the workflow script, which embeds the protocol, role briefs, dimension documents and message schemas |

Version: 0.2.0.

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

On Claude the skill is `sci-review:scientific-review`; on Codex it is `scientific-review` from the `sci-review` plugin. On Claude Code it also takes explicit arguments (section 6):

```text
/sci-review:scientific-review high 42 --comment
/sci-review:scientific-review feature/solver --max-findings 5
/sci-review:scientific-review low src/solver --fix
```

## 3. Dimensions

Every perspective reviews every review part of the scope across five dimensions. Each dimension has a document under `skills/scientific-review/dimensions/` with language-neutral checks followed by worked examples in Python and TypeScript.

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

1. **Independent round.** `panel.py parts` divides the scope into review parts of at most 2,000 lines, keeping the files of a directory together where they fit. Each perspective reviews every part without access to any other reviewer's output and writes one candidate-findings message per part. A reviewer may read any project file to follow a reference, but raises findings only on lines of its part.
2. **Debate.** `panel.py merge` clusters the candidates of every part by location (same file, line ranges within three lines) and groups the clusters into debate batches by file. For each batch, the moderator confirms or splits each cluster. The perspectives and the defender then state positions on every merged finding in round 0, followed by at most `rebuttal_rounds` rebuttal rounds. A batch stops early when no stance changes in a round. The moderator then writes notes on every finding of the batch.
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
| 1 | `claude-workflow` | The `Workflow` tool is available and the session has a scratchpad directory, into which the panel script is copied and launched; when the copy is refused, the next runner is used | Independent agents |
| 2 | `codex-subagents` | Running in Codex with multi-agent tools enabled | Independent agents |
| 3 | `claude-agents` | The `Agent` tool is available with the `sci-review:scientific-auditor` agent | Independent agents |
| 4 | `sequential` | Otherwise (claude.ai chat, Cowork, Codex with agents disabled) | Not independent |

The following rules modify the selection:

1. A user request for the review satisfies the Workflow opt-in requirement. A review started on the model's own initiative asks first, because it spawns many agents.
2. The user may force a lower runner. "Run it without agents" selects `sequential`; a request for agents but not the Workflow selects `claude-agents`.
3. When a multi-agent runner cannot spawn its agents, the review falls back to `sequential` with the same perspectives, rounds and batches.

The `sequential` runner plays every role in one conversation, so its perspectives are not independent. The report then carries a reduced-independence notice. The runner documents are under `skills/scientific-review/runners/`.

## 6. Arguments

### 6.1 Explicit arguments

The skill accepts these arguments, in any order. On Claude Code the host shows the argument hint:

```text
[low|medium|high|xhigh|max] [<pr#>|<branch>|<path>] [--comment] [--fix] [--max-findings <n>|all|default]
```

| Argument | Effect |
|----------|--------|
| Level | `low`, `medium`, `high`, `xhigh` or `max`; see section 6.2. Without a level, the level the user last typed is reused, else `medium`. |
| Target | A pull request (`42`, `#42` or its URL; `!42` or a `/-/merge_requests/42` URL on GitLab), a branch, which is reviewed without being checked out, or one or more paths. Without a target, the current branch is reviewed. A target that matches several kinds (for example a branch and a directory of the same name) is not guessed: the skill asks. |
| `--max-findings <n>` | Delivers the first `n` findings in report order. `all` removes the limit; `default` restores the usual limit, which is no limit. The report states the cap and the number of findings it withheld; the withheld findings stay in the run directory. When findings are delivered through `ReportFindings`, at most 32 are delivered, the tool's maximum. |
| `--comment` | Posts each delivered finding as an inline comment on a GitHub pull request, or all findings as one note on a GitLab merge request, after the report. Requires `gh` or `glab`. Without a pull request target, the flag is ignored with a note. |
| `--fix` | Applies the delivered findings to the working tree after the report, runs the relevant checks, and reports each finding again with its outcome (`fixed`, `no_change_needed` or `skipped`, with a reason). Nothing is staged or committed. See section 8. |

An unknown flag, two levels, and `ultra` are usage errors, and nothing runs. A token such as `hig`, which begins like a level but is not one, is a usage error unless it names an existing branch or path. A malformed `--max-findings` value is ignored with a one-line note. On hosts without an argument field (Codex, claude.ai, Cowork), the same arguments are accepted when written in the request.

A level and a `--max-findings` choice that the user typed are stored per user, outside every project, in `$XDG_CONFIG_HOME/sci-review/preferences.json` (default `~/.config/sci-review/preferences.json`; `%APPDATA%\sci-review\preferences.json` on Windows). A level the model chooses itself is never stored. `python3 scripts/panel.py prefs --show` prints the stored preferences and `--clear` removes them. Where the file cannot be read or written, the review uses the defaults and says so.

### 6.2 Effort levels

| Level | Perspectives | Rebuttal rounds | Debate batches | Default finding cap |
|-------|--------------|-----------------|----------------|---------------------|
| `low` | `theorist`, `numerical-analyst`, `methodologist` | 1 | 1 | none |
| `medium` | the five defaults plus selected extensions, at most 7 | 2 | 2 | none |
| `high` | as `medium` | 2 | 3 | none |
| `xhigh` | as `medium` | 3 | 4 | none |
| `max` | all defaults and selected extensions, at most 7 | 3 | 4 | none |

`medium` is the configuration of version 0.1.0, so a review with no arguments behaves as before. The model uses `max` only when the user, or an instruction file, asks for it.

### 6.3 Arguments from the wording of the request

These arguments are read from the request where no explicit argument covers them; explicit arguments take precedence.

| Argument | Default | Limits and examples |
|----------|---------|---------------------|
| `mode` | `branch` | `branch`, `repository` ("review the whole repository") or `paths` ("review src/solver"); ignored when a target is given |
| `baseline` | Resolved from the default branch by `panel.py scope` | Branch mode or a branch target only; "since v1.2" sets the baseline to `v1.2` |
| `paths` | None | Required in `paths` mode |
| `perspectives` | From the level | 2 to 7 in total |
| `rebuttal_rounds` | From the level | 0 to 3 |
| `max_batches` | From the level | 1 to 4 |
| `models` | None | `claude-workflow` runner only, as `role=model` pairs |
| Keep the run directory | No | When requested, the run directory is kept and its path is given |

A parameter named in words overrides that part of the level, and the report records the override. Out-of-range values are clamped, and the report states the panel actually used. Branch mode requires git; when the project is not a git repository, or no base can be determined, the skill asks the user for a baseline or for another mode and never switches modes silently.

### 6.4 Scope size

No file is excluded for the size of the scope. The scope is divided into review parts of at most 2,000 lines, each reviewed in full by every perspective. Above 6,000 lines (the large-scope threshold), the skill states the number of lines, files and parts and asks for confirmation before any reviewer runs; on refusal it runs nothing and offers a narrower target. With P perspectives and K parts, the independent round makes P x K reviewer invocations; the debate does not grow with K.

## 7. Report

The report contains eight sections, in this order:

1. **Scope.** What was reviewed (with the pull request or branch named as the target), the runner, whether the perspectives were independent agents, and the number of review parts.
2. **Panel.** The effort level and whether it was given, reused or defaulted, the perspectives used (with their source), the rebuttal rounds and the batches, and any parameter overridden from the level.
3. **Extensions.** Domain extensions selected, not applicable, failed (with the reason) and recommended (with what each would add).
4. **Findings.** The finding cap and the number of findings it withheld, then the findings, ordered consensus, majority, contested, and within each label high, medium, low. Each finding gives its location, dimension, severity, summary, trigger, wrong output, fix, raisers and label.
5. **Rejected findings.** Identifier, summary, raisers and reason.
6. **Checked and found correct.** Locations the panel examined and confirmed, with the dimension and a note.
7. **Not reviewed.** Paths outside the review, with the reason (outside the named paths, generated or vendored, or a review part that did not complete).
8. **Notices.** Reduced independence, languages without worked examples, missing tools, and messages dropped after failed validation.

When no reviewable scientific code changed, the report contains sections 1 to 3 and the sentence "No reviewable scientific code changed in this scope." In Claude Code the findings are delivered through `ReportFindings` and the other sections as Markdown; on other hosts the whole report is Markdown, with one table per label.

## 8. Read-only guarantee

Without `--fix`, the review never creates, modifies or deletes a file in the reviewed project. With `--fix`, the panel phases remain read-only, and only the closing fix step writes: after the report, the orchestrating conversation applies the delivered findings to the working tree with the host's own editing tools, stages and commits nothing, and reports every finding again with its outcome. No clean working tree is required: passing the flag is the user's acceptance of that risk (constitution 1.3.0, Principle III exception). Resolving a pull request target fetches its head into a temporary ref under `refs/sci-review/`, which is deleted at the end; no target is ever checked out. Every panel message is written to a run directory under the system temporary directory, which is deleted at the end unless the user asks to keep it. In a git repository the skill records `git status --porcelain --ignored` before the review and compares it afterwards, and reports any file that changed, including ignored files such as a bytecode cache. Panel members run Python checks with `python3 -B`, so that they write no `__pycache__` in the project. The review runs no simulation or long computation in the project unless the user requests it.

## 9. Requirements

- `python3` 3.10 or later for `scripts/panel.py`. Without it, the deterministic steps are performed by hand from the written rules of `protocol.md` section 10, and the report records a notice.
- `git` for branch mode and for branch and pull request targets. Repository and paths modes work without a git repository.
- `gh` (GitHub) or `glab` (GitLab), installed and authenticated, for pull request targets and `--comment`. Without them the skill says what is missing and offers a branch or paths review.

## 10. Domain extensions

Any installed plugin, for Claude or for Codex, can add a domain perspective by shipping one skill named `<domain>-sci-review-extension` with an `extension.json` declaration. A selected extension contributes one perspective with its own brief, reference documents and optional domain checks; it reviews and debates on the same terms as the default perspectives and counts toward the panel limit and the majority denominator. No change to sci-review is needed.

The authoritative contract, version 1, is [`skills/scientific-review/extensions.md`](skills/scientific-review/extensions.md). The first extension, `building-energy-sci-review-extension`, ships in the idfkit plugin (`idfkit@idfkit`) and is released separately.

## 11. Releases

sci-review is versioned independently of project-kit. Releases are tagged `sci-review-vX.Y.Z`.

Before each release, re-read the host prompt text reproduced in `SKILL.md` section 8 from the current Claude Code binary, with the method of `specs/008-sci-review-arguments/research.md` section 0, and update them and the cited Claude Code version when they have changed. The text is internal to the host and has no public interface.
