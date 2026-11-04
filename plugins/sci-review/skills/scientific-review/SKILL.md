---
name: scientific-review
description: >-
  Review code for scientific correctness with a panel of independent reviewers (theorist, numerical analyst, experimentalist, methodologist, computer scientist), a defender and a moderator, across mathematical derivations, numerical stability, physical modelling and units, statistical integrity, and algorithmic correctness. Use when the user asks for a scientific review, to check the maths, whether code is numerically stable, whether units or conservation are right, whether a pipeline leaks data, or whether an algorithm terminates or is deterministic, on a branch (the default), a whole repository or named paths. Not for style, lint, formatting or documentation reviews.
---

# Scientific review

This skill reviews code for scientific correctness with a panel. Perspective reviewers review the scope independently, a moderator merges their candidate findings, the perspectives and a defender debate each finding, and a script computes each finding's agreement label from the recorded positions. The review is read-only: it never creates, modifies or deletes a file in the reviewed project (FR-006).

The protocol is defined once, in [protocol.md](protocol.md). The role briefs are in [roles/](roles/), the dimension documents in [dimensions/](dimensions/), the message schemas in [schemas/](schemas/), the runners in [runners/](runners/), and the domain-extension contract in [extensions.md](extensions.md).

## 1. Notation

| Symbol | Meaning |
|--------|---------|
| `$SKILL` | The directory of this skill. On Claude it is `${CLAUDE_PLUGIN_ROOT}/skills/scientific-review`. |
| `$PANEL` | `python3 "$SKILL/../../scripts/panel.py"`, the plugin's deterministic helper (contracts in [protocol.md](protocol.md)). |
| `$RUN` | The run directory printed by `$PANEL init`, under the system temporary directory and never inside the project. |
| `$PROJECT` | The root of the reviewed project (the current working directory unless the user names another). |

Every `panel.py` subcommand logs its arguments to standard error. Exit codes: 0 success, 1 validation failure, 2 usage error, 3 precondition not met.

## 2. Arguments

Read these from the request; all are optional (contracts/invocation.md section 2).

| Argument | Default | Limits and mapping |
|----------|---------|--------------------|
| mode | `branch` | "review the whole repository" gives `repository`; "review src/solver" gives `paths` |
| baseline | resolved by `panel.py scope` | branch mode only; "since v1.2" gives `--baseline v1.2` |
| paths | none | required for `paths` mode |
| perspectives | the five defaults plus selected extensions | 2 to 7 in total; "a quick review with the theorist and the numerical analyst" names two |
| rebuttal_rounds | 2 | 0 to 3; "a quick review" may use 1 |
| max_batches | 2 | 1 to 4 |
| models | none | Workflow runner only, as `role=model` pairs |
| keep the run directory | no | when the user asks to keep it, skip `clean` and give its path |

Out-of-range values are clamped by `panel.py panel`, and the report states the panel actually used.

## 3. Preconditions

Check these before the opening steps, and say clearly what is missing instead of failing partway (Principle IV).

1. **git.** Branch mode needs `git` and a git repository. When the project is not a git repository, or `git` is absent, tell the user and offer repository mode or paths mode, which work without git. Never switch modes silently.
2. **python3.** Run `python3 --version` (3.10 or later). When it is absent or older, perform every `panel.py` step by hand with the written fallback rules of [protocol.md](protocol.md) section 10, and add the notice they specify to the report.
3. **No base.** When `$PANEL scope --mode branch` exits with code 3 because no base can be determined (no default branch, or the current branch has not diverged from it), ask the user for a baseline, or whether to review the repository or named paths instead. Never fall back to repository mode without asking.

## 4. Runner selection

Select the first available runner, in this order (contracts/invocation.md section 3), and pass it to `$PANEL panel --runner`.

| Order | Runner | Condition | File |
|-------|--------|-----------|------|
| 1 | `claude-workflow` | The `Workflow` tool is available and `sci-review:scientific-review` is listed as a workflow | [runners/claude-workflow.md](runners/claude-workflow.md) |
| 2 | `codex-subagents` | Running in Codex with multi-agent tools enabled | [runners/codex-subagents.md](runners/codex-subagents.md) |
| 3 | `claude-agents` | The `Agent` tool is available with the `sci-review:scientific-auditor` agent | [runners/claude-agents.md](runners/claude-agents.md) |
| 4 | `sequential` | Otherwise (claude.ai chat, Cowork, Codex with agents disabled) | [runners/sequential.md](runners/sequential.md) |

Rules:

1. **Workflow opt-in.** A user request for the review satisfies the Workflow opt-in requirement. When the review is started on your own initiative, ask first, because it spawns many agents.
2. **User-forced lower runner.** When the user asks to run the review without agents ("run it without agents", "do it in this conversation"), use `sequential`. When the user asks for agents but not the Workflow, use `claude-agents`.
3. **Fallback.** When a multi-agent runner cannot spawn its agents, the runner file switches to `sequential` and records it with `$PANEL panel --runner sequential` (same perspectives, rounds and batches), so that the report carries the reduced-independence notice (FR-028).

## 5. Opening steps (every runner)

Run these in the orchestrating conversation.

1. **Run directory.** `$PANEL init --project "$PROJECT"`; keep the printed path as `$RUN`.
2. **Scope.** One of:
   - branch (default): `$PANEL scope --run $RUN --mode branch [--baseline REF]`;
   - repository: `$PANEL scope --run $RUN --mode repository`;
   - paths: `$PANEL scope --run $RUN --mode paths --path P [--path Q ...]`.

   Add `--budget N` when the user asks for a smaller or larger review (default 6,000 lines). Files over the budget, generated and vendored files (unless named in paths mode), and, in paths mode, files outside the named paths are recorded as not reviewed, with the reason. Generated and vendored files are lock files, files under `node_modules/`, `dist/`, `vendor/`, `third_party/` or `__pycache__/`, and files marked `linguist-generated` or `linguist-vendored`; a file named in paths mode is reviewed even when it is one of them. Notebooks (`.ipynb`) are in scope and reviewed as Python code.
3. **Empty scope.** When `scope.json` lists no files, skip to the closing steps: run `$PANEL panel --run $RUN --runner <runner>`, then `$PANEL report --run $RUN`, which renders the Scope, Panel and Extensions sections and the sentence "No reviewable scientific code changed in this scope." (US1 scenario 4). Do not launch any reviewer.
4. **Extension discovery** (contracts/extension.md section 4, [extensions.md](extensions.md)):
   1. In the host's skill listing, find every skill whose name ends in `sci-review-extension`.
   2. Load each such skill to obtain its base directory, and locate `extension.json` in that directory. A skill without one is passed anyway, so that it is reported as failed with the reason.
   3. Run `$PANEL select-extensions --run $RUN --declaration <dir>/extension.json [--declaration ...]`, once, with every declaration found (with no `--declaration` when none was found, so that known extensions are still recommended). It records each extension as `selected`, `not-applicable` or `failed` (with the reason), and adds known but uninstalled extensions that would apply as `recommended`.
5. **Panel.** `$PANEL panel --run $RUN --runner <runner> [--perspectives a,b,...] [--rounds N] [--batches N] [--models role=model ...]`. Selected domain perspectives join the panel with their absolute brief and reference paths; the runners take every perspective from `panel.json`, so domain perspectives need no runner change.
6. **Project state.** When the project is a git repository, record `git -C "$PROJECT" status --porcelain --ignored` for the comparison at the end.

## 6. Panel phases (runner file)

Open the selected runner file and follow it. It covers the independent round, the merge, the debate and the moderator notes, and leaves every panel message in `$RUN` in the layout of contracts/panel-messages.md section 2. Then return here for the closing steps.

## 7. Closing steps (every runner)

1. **Adjudicate.** `$PANEL adjudicate --run $RUN`. It applies the rules of [protocol.md](protocol.md) section 5 and exits 1 on a protocol violation (for example a `withdraw` from a member that did not raise the finding); report such a violation to the user rather than editing the messages.
2. **Report.** `$PANEL report --run $RUN --format json` when `ReportFindings` is available, otherwise `$PANEL report --run $RUN --format markdown`. Both write `$RUN/report.json`.
3. **Project check.** Compare (`--ignored` also lists files that `.gitignore` hides, such as a bytecode cache) `git -C "$PROJECT" status --porcelain --ignored` with the state recorded in the opening steps. If anything changed, tell the user which files changed; the review must not modify the project (SC-004).
4. **Delivery** (contracts/report.md section 3):
   - **ReportFindings available** (Claude Code): call it once with the `report_findings` array of the JSON output, in its order (consensus, majority, contested; within each, high, medium, low). Then give the remaining sections (Scope, Panel, Extensions, Rejected findings, Checked and found correct, Not reviewed, Notices) as Markdown, from `$PANEL report --run $RUN --format markdown`, omitting its Findings section.
   - **Otherwise** (Codex, claude.ai, Cowork): give the Markdown report as printed, with one table per label carrying every field.
5. **Name what was not reviewed.** When the Not reviewed section is non-empty (over budget, outside the named paths, generated or vendored), say so in one sentence in your reply, so that the user knows the review is partial (US3 scenario 3).
6. **Clean.** `$PANEL clean --run $RUN`, unless the user asked to keep the run directory; then give its path instead.

## 8. Rules

1. **Read-only.** Never create, modify or delete a file in the reviewed project, and never instruct a panel member to do so. Every panel message lives in `$RUN`.
2. **Scientific correctness only.** Report nothing about style, formatting, naming, lint or documentation that has no effect on the computed result (FR-007).
3. **Labels come from the script.** Never assign, raise or lower an agreement label yourself; `panel.py adjudicate` computes them from the recorded positions.
4. **Independence.** Never pass one perspective's independent-round output, or a summary of it, to another perspective (SC-011). Pass each role only the inputs listed in [protocol.md](protocol.md) section 3.
5. **No simulations or long computations** in the project without the user's request; short checks of a claim (evaluating an expression at a trigger) are allowed when they write nothing in the project. Run Python with `python3 -B`, so that importing a project module writes no `__pycache__` in the project.
