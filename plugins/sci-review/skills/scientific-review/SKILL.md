---
name: scientific-review
description: >-
  Review code for scientific correctness with a panel of independent reviewers (theorist, numerical analyst, experimentalist, methodologist, computer scientist), a defender and a moderator, across mathematical derivations, numerical stability, physical modelling and units, statistical integrity, and algorithmic correctness. Use when the user asks for a scientific review, to check the maths, numerical stability, units or conservation, data leakage, or algorithm termination, on a branch (the default), a pull request, a whole repository or named paths. Not for style, lint, formatting or documentation reviews. Use the max level only when the user, or instructions such as CLAUDE.md or a skill, explicitly ask for it, never on your own judgment: it is the costliest level and starts many reviewer agents.
argument-hint: "[low|medium|high|xhigh|max] [<pr#>|<branch>|<path>] [--comment] [--fix] [--max-findings <n>|all|default]"
---

# Scientific review

This skill reviews code for scientific correctness with a panel. Perspective reviewers review the scope independently, a moderator merges their candidate findings, the perspectives and a defender debate each finding, and a script computes each finding's agreement label from the recorded positions. The review is read-only: no panel phase creates, modifies or deletes a file in the reviewed project. The only exception is the closing `--fix` step of section 8, which the user requests explicitly: it edits the working tree after the report, and stages or commits nothing (constitution 1.3.0, Principle III exception; spec 008 FR-016e).

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

### 2.1 Explicit arguments

The skill accepts the arguments of `/code-review`, in any order:

```text
/sci-review:scientific-review [low|medium|high|xhigh|max] [<pr#>|<pr-url>|<branch>|<path>...] [--comment] [--fix] [--max-findings <n>|all|default]
```

| Argument | Meaning |
|----------|---------|
| level | `low`, `medium`, `high`, `xhigh` or `max`: the panel configuration of section 2.3. Without a level, the level the user last typed is reused, else `medium`. |
| target | A pull request (`12`, `#12`, a pull request URL; `!12` or a `/-/merge_requests/` URL on GitLab), a branch that need not be checked out, or one or more paths. Without a target, the current branch is reviewed. |
| `--comment` | Post the delivered findings on the pull request (section 8). |
| `--fix` | Apply the delivered findings to the working tree after the report (section 8). |
| `--max-findings` | Deliver at most `<n>` findings in report order; `all` removes the limit; `default` restores the usual limit (no limit). The choice is reused until `default` is passed. |

`$PANEL args` parses them deterministically into `$RUN/arguments.json`:

- When the command came with arguments (`$ARGUMENTS` is not empty on Claude Code), run `$PANEL args --run $RUN --argv="$ARGUMENTS"`.
- Otherwise, and on hosts without an argument field (Codex, claude.ai, Cowork), run `$PANEL args --run $RUN --text "<the user's request>"`. Only the grammar's tokens (a level word, the flags and the `--max-findings` value) are taken from the request; the rest is read as in section 2.2.
- Add `--persist` only when the user typed the arguments or wrote them in the request, so that a typed level and `--max-findings` choice are stored for later reviews. Never pass it when you start the review on your own initiative.

On exit 2 (an unknown flag, two levels, `ultra`), show the message to the user, which names the accepted values, run nothing else, and clean the run directory. A malformed `--max-findings` value is not an error: it is ignored with a note. As the review begins, tell the user each entry of `notes` in `arguments.json` in one short line.

Preferences are stored outside every project, in `$XDG_CONFIG_HOME/sci-review/preferences.json` (default `~/.config/sci-review/`; `%APPDATA%\sci-review\` on Windows). `$PANEL prefs --show` prints them and `$PANEL prefs --clear` removes them. Where they cannot be read or written, the review uses the defaults and the notes say so; it never fails for this reason.

### 2.2 Arguments from the wording of the request

The arguments of feature 007 are still read from the request where no explicit argument covers them. Explicit arguments take precedence over arguments inferred from wording; a parameter named in words (for example "only one rebuttal round") overrides that part of the level's configuration, and the report records the override.

| Argument | Default | Limits and mapping |
|----------|---------|--------------------|
| mode | `branch` | "review the whole repository" gives `repository`; "review src/solver" gives `paths`; ignored when a target is given |
| baseline | resolved by `panel.py scope` | branch mode or a branch target only; "since v1.2" gives `--baseline v1.2` |
| paths | none | required for `paths` mode |
| perspectives | from the level | 2 to 7 in total; "a quick review with the theorist and the numerical analyst" names two |
| rebuttal_rounds | from the level | 0 to 3; "a quick review" may use 1 |
| max_batches | from the level | 1 to 4 |
| models | none | Workflow runner only, as `role=model` pairs |
| keep the run directory | no | when the user asks to keep it, skip `clean` and give its path |

Out-of-range values are clamped by `panel.py panel`, and the report states the panel actually used.

### 2.3 Effort levels

| Level | Perspectives | Rebuttal rounds | Debate batches |
|-------|--------------|-----------------|----------------|
| `low` | `theorist`, `numerical-analyst`, `methodologist` | 1 | 1 |
| `medium` | the five defaults plus selected extensions, at most 7 | 2 | 2 |
| `high` | as `medium` | 2 | 3 |
| `xhigh` | as `medium` | 3 | 4 |
| `max` | all defaults and selected extensions, at most 7 | 3 | 4 |

`medium` is the configuration of feature 007, so a review with no arguments behaves as before. No level caps the number of findings by default. Use the max level only when the user, or instructions such as CLAUDE.md or a skill, explicitly ask for it, never on your own judgment: it is the costliest level and starts many reviewer agents.

## 3. Preconditions

Check these before the opening steps, and say clearly what is missing instead of failing partway (Principle IV).

1. **git.** Branch mode, branch targets and pull request targets need `git` and a git repository. When the project is not a git repository, or `git` is absent, tell the user and offer repository mode or paths mode, which work without git. Never switch modes silently.
2. **python3.** Run `python3 --version` (3.10 or later). When it is absent or older, perform every `panel.py` step by hand with the written fallback rules of [protocol.md](protocol.md) section 10, and add the notice they specify to the report.
3. **No base.** When `$PANEL scope` exits with code 3 because no base can be determined (no default branch, or the branch has not diverged from it), ask the user for a baseline, or whether to review the repository or named paths instead. Never fall back to repository mode without asking.
4. **Hosting client.** A pull request target and `--comment` need `gh` (GitHub) or `glab` (GitLab), installed and authenticated. `panel.py scope` detects them; see section 5 step 3 for what to do when one is missing.

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
2. **Arguments.** `$PANEL args --run $RUN (--argv="$ARGUMENTS" | --text "<request>") [--persist]`, as in section 2.1. Tell the user the notes in one short line each.
3. **Scope.** `$PANEL scope --run $RUN`. It resolves the `target_text` of `arguments.json` (or `--target TEXT`) and writes the resolved target to `scope.json`. With no target, add the mode read from the wording:
   - branch (default): `$PANEL scope --run $RUN [--mode branch] [--baseline REF]`;
   - repository: `$PANEL scope --run $RUN --mode repository`;
   - paths: `$PANEL scope --run $RUN --mode paths --path P [--path Q ...]`.

   Resolving a target never checks out a branch or changes the working tree or the index; a pull request head is fetched into a temporary ref under `refs/sci-review/`, which `clean` deletes. Handle the exit codes as follows:
   - exit 3 with `{"ambiguous": [...]}`: the target matches several kinds (for example a branch and a directory of the same name); ask the user which was meant, then run `scope` again with `--target` set to a form that is not ambiguous (for example `docs/` for the directory).
   - exit 3 with `{"missing": "gh" | "glab" | "auth" | "network"}`: say what is missing (the client, its authentication, or network access) and offer a review of a branch or of named paths instead. Never switch silently.
   - exit 2: a path outside the project, a target that names nothing, or a token such as `hig` that is not a level and names no branch or path. Show the message and run nothing.

   No file is excluded for the size of the scope. Generated and vendored files (unless named in paths mode) and, in paths mode, files outside the named paths are recorded as not reviewed, with the reason. Generated and vendored files are lock files, files under `node_modules/`, `dist/`, `vendor/`, `third_party/` or `__pycache__/`, and files marked `linguist-generated` or `linguist-vendored`; a file named in paths mode is reviewed even when it is one of them. Notebooks (`.ipynb`) are in scope and reviewed as Python code. When `scope.json` has a `target` of kind `branch` or `pull-request`, its files are not in the working tree: every panel member reads them at `head` with `git -C "$PROJECT" show <head>:<path>`.
4. **Review parts.** `$PANEL parts --run $RUN`. It divides the scope into review parts of at most 2,000 lines, keeping the files of a directory together where they fit, and writes `parts.json`. When `confirm_required` is true (more than 6,000 lines), say, before any reviewer runs: "This scope has <L> lines in <F> files and will be reviewed in <K> parts. Continue?" When the user declines, run nothing, clean the run directory, and offer a narrower target such as named paths. A review started on your own initiative always asks before a scope that requires confirmation.
5. **Empty scope.** When `scope.json` lists no files, skip to the closing steps: run `$PANEL panel --run $RUN --runner <runner>`, then `$PANEL report --run $RUN`, which renders the Scope, Panel and Extensions sections and the sentence "No reviewable scientific code changed in this scope." (US1 scenario 4). Do not launch any reviewer.
6. **Extension discovery** (contracts/extension.md section 4, [extensions.md](extensions.md)):
   1. In the host's skill listing, find every skill whose name ends in `sci-review-extension`.
   2. Load each such skill to obtain its base directory, and locate `extension.json` in that directory. A skill without one is passed anyway, so that it is reported as failed with the reason.
   3. Run `$PANEL select-extensions --run $RUN --declaration <dir>/extension.json [--declaration ...]`, once, with every declaration found (with no `--declaration` when none was found, so that known extensions are still recommended). It records each extension as `selected`, `not-applicable` or `failed` (with the reason), and adds known but uninstalled extensions that would apply as `recommended`.
7. **Panel.** `$PANEL panel --run $RUN --runner <runner> [--level LEVEL] [--perspectives a,b,...] [--rounds N] [--batches N] [--models role=model ...]`. The level defaults to the `level` of `arguments.json`; pass `--level` only to repeat it. `--perspectives`, `--rounds` and `--batches` come from the wording of the request (section 2.2) and override the level's values; they are recorded as overrides. Selected domain perspectives join the panel with their absolute brief and reference paths; the runners take every perspective from `panel.json`, so domain perspectives need no runner change.
8. **Project state.** When the project is a git repository, record `git -C "$PROJECT" status --porcelain --ignored` for the comparison at the end.

## 6. Panel phases (runner file)

Open the selected runner file and follow it. It covers the independent round, which runs once per perspective and review part, the merge, the debate and the moderator notes, and leaves every panel message in `$RUN` in the layout of contracts/panel-messages.md section 2. Then return here for the closing steps.

## 7. Closing steps (every runner)

The closing steps run in this order: adjudicate, report, project check, deliver, then post (`--comment`), then fix (`--fix`), then clean.

1. **Adjudicate.** `$PANEL adjudicate --run $RUN`. It applies the rules of [protocol.md](protocol.md) section 5 and exits 1 on a protocol violation (for example a `withdraw` from a member that did not raise the finding); report such a violation to the user rather than editing the messages.
2. **Report.** `$PANEL report --run $RUN --format json` when `ReportFindings` is available, otherwise `$PANEL report --run $RUN --format markdown`. Both write `$RUN/report.json`. The report states the effort level and whether it was given, reused or defaulted, the panel actually used, the target, the number of review parts, the finding cap and the number of findings withheld by it. The withheld findings remain in `$RUN/adjudication.json`.
3. **Project check.** Compare (`--ignored` also lists files that `.gitignore` hides, such as a bytecode cache) `git -C "$PROJECT" status --porcelain --ignored` with the state recorded in the opening steps. If anything changed, tell the user which files changed; the panel must not modify the project (SC-004). This check runs before the fix step, so that any change it reports was made by the panel.
4. **Delivery** (contracts/report.md section 3):
   - **ReportFindings available** (Claude Code): call it once with the `report_findings` array of the JSON output, in its order (consensus, majority, contested; within each, high, medium, low). The array holds at most 32 findings, the tool's maximum; when `report_tool_notice` is set, say "This review reports at most 32 findings, so the limit is 32 here." Then give the remaining sections (Scope, Panel, Extensions, Rejected findings, Checked and found correct, Not reviewed, Notices) as Markdown, from `$PANEL report --run $RUN --format markdown`, omitting its Findings section, and state the cap applied and the number of findings withheld (`max_findings`, `withheld`).
   - **Otherwise** (Codex, claude.ai, Cowork): give the Markdown report as printed, with one table per label carrying every field; it states the cap and the number withheld at the top of its Findings section. Then append the outcome lines of section 8 (If findings are fixed later) when `--fix` or a later fix applies.
5. **Name what was not reviewed.** When the Not reviewed section is non-empty (outside the named paths, generated or vendored, or a review part that did not complete), say so in one sentence in your reply, naming any incomplete part, so that the user knows the review is partial (US3 scenario 3).
6. **Post** (`--comment`): section 8, Posting to GitHub or Posting to GitLab. A posting failure never suppresses the local report; report it with its reason. When `comment` is true but the target is not a pull request, the findings are already printed: say that `--comment` was ignored because the target is not a pull request, and post nothing (FR-003b).
7. **Fix** (`--fix`): section 8, Applying fixes.
8. **Clean.** `$PANEL clean --run $RUN`, which also deletes the temporary refs under `refs/sci-review/`, unless the user asked to keep the run directory; then give its path instead.

**Finding outcomes.** When findings are reported again with an outcome (section 8, Applying fixes and If findings are fixed later), each carries the shape below. `panel.py` never writes outcomes; the orchestrating conversation passes them to `ReportFindings` or states them in the reply. The agreement label of a finding never changes.

| Field | Value |
|-------|-------|
| `finding_id` | the finding's id in the report |
| `outcome` | `fixed`, `no_change_needed` or `skipped` |
| `reason` | required for `skipped` |
| `files` | the files changed, for `fixed` |

## 8. Closing sections reproduced from /code-review

Reproduced from /code-review, Claude Code 2.1.317. The sections below reproduce the prompt text of `/code-review` (spec 008 research R1, R2) with the adaptations marked in contracts/fix-and-comment.md. You, the orchestrating conversation, execute them after the delivery step, with the host's own tools; no `panel.py` subcommand, runner or panel member performs them. In them, "ReportFindings" is the host's findings-reporting tool.

### Posting to GitHub (--comment)

Follow this section only when `arguments.json` has `comment: true` and the target host is not GitLab.

The `--comment` flag was passed. After producing the findings list, if the review target is a GitHub PR, post each finding as an inline PR comment via `mcp__github_inline_comment__create_inline_comment` (one call per finding; include a suggestion block only when it fully fixes the issue). If that tool is not available in this session, fall back to `gh api` (repos/{owner}/{repo}/pulls/{pr}/comments) or print the findings instead. If the target is not a PR, print the findings to the terminal and note that `--comment` was ignored.
Each comment states the finding's agreement label, severity and dimension, then the issue and the scenario. A finding that does not anchor to a line of the PR diff is printed with a note, not posted.
Post nothing when the review has no findings.

### Posting to GitLab (--comment)

Follow this section only when `arguments.json` has `comment: true` and the target host is GitLab.

The `--comment` flag was passed. After producing the findings list, if the review target is a GitLab merge request, post the findings as one general MR note via `glab mr note <iid> [-R <project>] -m "<body>"` (every finding with its file:line, the issue, and the suggested fix). glab has no single verb for line-anchored comments; those require `glab api projects/:id/merge_requests/:iid/discussions`, so post the general note unless the user asks for inline threads. If glab is not available in this session, print the findings instead. If the target is not an MR, print the findings to the terminal and note that `--comment` was ignored.

### Applying fixes (--fix)

Follow this section only when `arguments.json` has `fix: true`. Without `--fix` this section does not apply, and the review is read-only.

The `--fix` flag was passed. After producing the findings list, apply the findings to the working tree instead of stopping at the report: fix each one directly, every delivered finding.
Skip any finding whose fix would change intended behavior, require changes well outside the reviewed diff, or that you judge to be a false positive; note the skip rather than arguing with it.
Skipping a finding never changes its agreement label.
Run the relevant checks after.

- **With ReportFindings:** Then call ReportFindings again with the same findings, each carrying an `outcome`: `fixed`, `no_change_needed` (the finding was wrong or already handled), or `skipped` (real but not applied). Do not repeat the findings as text; after the call, give one line per skipped finding saying why.
- **Without ReportFindings:** Finish with a brief summary of what was fixed and what was skipped.

Constraints on this section (spec 008 FR-016, FR-016a, FR-016e):

1. Nothing is staged or committed.
2. It runs only after the findings are reported; the project check of section 7 step 3 runs before it.
3. Only delivered findings are considered: those left after `--max-findings`, and after the clamp to 32 when they were delivered through ReportFindings.
4. You make the fixes yourself, in this conversation, with the host's own editing tools. Start no agent, perspective reviewer or other panel member for them.
5. No clean-working-tree check is made, as in `/code-review`: passing `--fix` is the user's explicit acceptance of the risk of writing to a working tree with uncommitted changes (constitution 1.3.0, Principle III exception).
6. A pull request target, or a branch that is not checked out, is not in the working tree: its findings fall under the skip rule above, as requiring changes outside the reviewed code.

### If findings are fixed later

Follow this section whenever ReportFindings is available, with or without `--fix`.

Whenever reported findings get fixed later in this session (the user asks you to fix them, or later work fixes them incidentally) you MUST call ReportFindings again with the same findings, each carrying an `outcome`: `fixed`, `no_change_needed` (the finding was wrong or already handled), or `skipped` (real but not applied). Do not repeat the findings as text.
Make that call immediately after the fixes land, before any prose summary; the host UI's per-finding status updates only from it, and without it the findings stay marked unresolved.

When the findings were delivered as a message rather than rendered by the host, append: After the call, give one line per finding with its outcome: this session can also be read from a client that does not show the tool call.

## 9. Rules

1. **Read-only panel.** Never create, modify or delete a file in the reviewed project during the panel phases, and never instruct a panel member to do so. Every panel message lives in `$RUN`. Only the closing fix step of section 8 (Applying fixes), requested with `--fix`, writes to the project.
2. **Scientific correctness only.** Report nothing about style, formatting, naming, lint or documentation that has no effect on the computed result (FR-007).
3. **Labels come from the script.** Never assign, raise or lower an agreement label yourself; `panel.py adjudicate` computes them from the recorded positions.
4. **Independence.** Never pass one perspective's independent-round output, or a summary of it, to another perspective (SC-011). Pass each role only the inputs listed in [protocol.md](protocol.md) section 3.
5. **No simulations or long computations** in the project without the user's request; short checks of a claim (evaluating an expression at a trigger) are allowed when they write nothing in the project. Run Python with `python3 -B`, so that importing a project module writes no `__pycache__` in the project.
6. **The max level.** Use the max level only when the user, or instructions such as CLAUDE.md or a skill, explicitly ask for it, never on your own judgment: it is the costliest level and starts many reviewer agents (FR-008).
7. **Preferences.** Pass `--persist` to `panel.py args` only for arguments the user typed or wrote; a level or cap you choose yourself is never stored (FR-007).
