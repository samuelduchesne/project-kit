# Research: Code-review-style arguments for sci-review

**Feature**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Date**: 2026-11-04

## 0. Method

`/code-review` is a built-in prompt command of Claude Code, not a skill file on disk. Its implementation was read from the strings of the installed binary, Claude Code 2.1.317 (`~/.local/share/claude/versions/2.1.317`), with `strings -n 8`. The command is registered under the name `code-review`; its `getPromptForCommand` function builds the prompt the model receives by concatenating text sections, and its `onUserTypedArgs` hook stores preferences. The quotations below are verbatim from that binary, with the JavaScript template escapes removed; `${PI}` is the findings-reporting tool (`ReportFindings`). Because the text is internal to the host, it can change between Claude Code versions: R10 covers how the plan tracks it.

## R1. How `/code-review` implements `--fix`

**Finding.** `--fix` is implemented entirely as prompt text. When the flag is present, `getPromptForCommand` appends one section, built by a function that takes a single argument: whether the findings-reporting tool is available.

```text
## Applying fixes (--fix)
The `--fix` flag was passed. After producing the findings list, apply the
findings to the working tree instead of stopping at the report: fix each one
directly, correctness bugs and reuse/simplification/efficiency cleanups alike.
Skip any finding whose fix would change intended behavior, require changes well
outside the reviewed diff, or that you judge to be a false positive; note the
skip rather than arguing with it. Then call ReportFindings again with the same
findings, each carrying an `outcome`: `fixed`, `no_change_needed` (the finding
was wrong or already handled), or `skipped` (real but not applied). Do not
repeat the findings as text; after the call, give one line per skipped finding
saying why.
```

Without the findings-reporting tool, the last two sentences are replaced by "Finish with a brief summary of what was fixed and what was skipped."

Three further sections relate to fixing:

1. **Fixed later** (appended whenever the findings-reporting tool is available, with or without `--fix`): "Whenever reported findings get fixed later in this session (the user asks you to fix them, or later work fixes them incidentally) you MUST call ReportFindings again with the same findings, each carrying an `outcome` [...]. Make that call immediately after the fixes land, before any prose summary; the host UI's per-finding status updates only from it, and without it the findings stay marked unresolved."
2. **Outcome lines** (appended when the findings are delivered as a message rather than rendered): "After the call, give one line per finding with its outcome: this session can also be read from a client that does not show the tool call."
3. **After the review** (appended when a `verify` skill is installed): "After the findings are reported (and applied, when --fix was passed): if `/verify` has not run this session and the diff has a runtime surface [...], invoke `/verify` now."

The cloud level (`ultra --fix`) adds, when the cloud findings arrive locally: "apply these findings to the local working tree now. Skip findings that are wrong or not worth fixing, and run the relevant checks after."

What the implementation does **not** contain: no confirmation prompt, no separate fixing agent or subagent, no patch file, no staging or commit, no check of a clean working tree, and no special case for a pull request or branch target that is not checked out.

**Decision.** The scientific review implements `--fix` the same way: as a section of `SKILL.md` that the orchestrating conversation follows after the delivery step, using the host's own editing tools. The section reproduces the text above with three adaptations, each required by the specification:

1. "correctness bugs and reuse/simplification/efficiency cleanups alike" becomes "every delivered finding", because the scientific review reports only scientific-correctness findings (feature 007, FR-007).
2. A sentence states that skipping a finding does not change its agreement label (spec FR-016b, feature 007 rule "Labels come from the script").
3. "run the relevant checks after" is taken from the cloud variant and applied to every `--fix` run (spec FR-016c).

The "fixed later" section and the outcome-lines section are added to the delivery step under the same conditions as in `/code-review` (spec FR-016d). The `/verify` hand-off is not reproduced: it is a host-specific follow-up, not part of `--fix`, and the scientific review has no runtime surface of its own.

**Rationale.** The user asked for the implementation, not only the behaviour, to be the same. Prompt text executed by the orchestrating conversation is also the only mechanism that works on every runner and host of feature 007: a Workflow script cannot edit the project between agent calls, and Codex and claude.ai have no Workflow at all.

**Alternatives considered.**

- *A fixing agent per finding.* Rejected: `/code-review` does not use one, it would multiply cost, and agents are optional under Principle IV.
- *A `panel.py fix` subcommand that writes patches.* Rejected: fixes need judgement (Principle II reserves the model for judgement), and `/code-review` writes no patch file.
- *Showing a diff and asking before writing (Principle III as written).* Rejected by the user's decision that `--fix` behave as `/code-review --fix`; handled as a constitution amendment (plan, Complexity Tracking).

## R2. How `/code-review` implements `--comment`

**Finding.** `--comment` is also prompt text. The section depends on whether the target looks like a GitLab merge request (a `!<n>` reference, a `/-/merge_requests/<n>` URL, or a GitLab remote for a bare number).

GitHub (default):

```text
## Posting to GitHub (--comment)
The `--comment` flag was passed. After producing the findings list, if the
review target is a GitHub PR, post each finding as an inline PR comment via
`mcp__github_inline_comment__create_inline_comment` (one call per finding;
include a suggestion block only when it fully fixes the issue). If that tool
is not available in this session, fall back to `gh api`
(repos/{owner}/{repo}/pulls/{pr}/comments) or print the findings instead. If
the target is not a PR, print the findings to the terminal and note that
`--comment` was ignored.
```

GitLab:

```text
## Posting to GitLab (--comment)
The `--comment` flag was passed. After producing the findings list, if the
review target is a GitLab merge request, post the findings as one general MR
note via `glab mr note <iid> [-R <project>] -m "<body>"` (every finding with
its file:line, the issue, and the suggested fix). glab has no single verb for
line-anchored comments; those require
`glab api projects/:id/merge_requests/:iid/discussions`, so post the general
note unless the user asks for inline threads. If glab is not available in this
session, print the findings instead. If the target is not an MR, print the
findings to the terminal and note that `--comment` was ignored.
```

There is no summary comment on GitHub, no comment when there are no findings, and no confirmation before posting: the flag is the request.

**Decision.** The scientific review reproduces both sections in `SKILL.md`, applied after the delivery step and before `--fix`. Each posted comment carries the finding's agreement label, severity, dimension, issue and scenario; a suggestion block is included only when the finding's correction fully fixes the issue. The GitLab rule is kept, so that a GitLab-hosted project behaves as under `/code-review`.

**Consequence for the specification.** Spec FR-015 and User Story 5 currently require a summary comment for unanchored findings and for an empty review, which `/code-review` does not post. Since the user's direction is to match `/code-review`, the plan follows R2, and FR-015, SC-006 and User Story 5 were amended accordingly during planning (2026-11-04). Findings that do not anchor to a line of the pull request diff are printed in the reply with a note and are not posted, as `/code-review`'s "print the findings instead" fallback does (contracts/fix-and-comment.md section 1; spec US5 scenario 1).

**Alternatives considered.** Keeping the summary comment of the current FR-015. Rejected: it departs from `/code-review`, and the user asked for parity.

## R3. How `/code-review` parses its arguments

**Finding.** Parsing is deterministic code, not prompt text:

1. The flags `--fix`, `--comment`, `--post`, `--no-post` and `--max-findings [value]` are removed from any position in the argument string.
2. The first remaining token is taken as the effort level when it is one of `low`, `medium`, `high`, `xhigh`, `max` (case-insensitive) or `ultra`; a token that begins with the first three letters of a level but is not one (for example `hig`) is reported as an unrecognised level.
3. Everything after the level is the target, with backquotes removed and a leading `#` stripped.
4. `--max-findings` accepts a whole number above zero, `all` or `default`; any other value is ignored with the note "`--max-findings` was ignored: type a whole number above zero, `all`, or `default` after it. Using the usual limit."
5. With the findings-reporting tool, the cap is clamped to 32, the tool's maximum: "This review reports at most 32 findings, so the limit is 32 here."

**Decision.** `panel.py args` implements the same tokenisation (Principle II: a predictable step belongs in the script), producing `arguments.json` in the run directory. Divergences required by the specification: a level may appear anywhere rather than only first (spec edge case on argument order), two levels are a usage error (FR-003), `ultra` is a usage error (FR-003), and an unknown `--flag` is a usage error (FR-003). A near-level token (step 2) is a usage error only when it is not an existing branch or path; otherwise it is the target (FR-003). `args` records the token as a near-level candidate and `scope`, which can inspect the repository, raises the usage error when the token resolves to nothing. The 32-finding clamp is reproduced for delivery through the findings-reporting tool; the Markdown report is not clamped.

## R4. How `/code-review` persists the level and the finding cap

**Finding.** The `onUserTypedArgs` hook runs only when the user types the command (not when the model invokes it). It stores `codeReviewLastEffort` when a level was given and `codeReviewLastMaxFindings` when `--max-findings` was given (`default` clears it), in Claude Code's global user configuration. A review with no level reuses the stored level; a review with no `--max-findings` reuses the stored cap and tells the user so, with "passing `--max-findings default` goes back to the usual limit". The model is told: "Use the max level only when the user, or instructions such as CLAUDE.md or a skill, explicitly ask for it, never on your own judgment."

**Decision.** Plugins cannot write Claude Code's global configuration, and the specification requires separate storage (FR-017). `panel.py prefs` stores the preferences in a JSON file under the user's configuration directory: `$XDG_CONFIG_HOME/sci-review/preferences.json`, defaulting to `~/.config/sci-review/preferences.json`, and `%APPDATA%\sci-review\preferences.json` on Windows. It writes only when called with `--persist`, which `SKILL.md` passes only when the user typed the command or wrote the arguments in the request, mirroring `onUserTypedArgs`. When the directory cannot be read or written (claude.ai chat, a read-only home), `panel.py` reports it and the review adds the notice of FR-018. The `max` instruction is reproduced in the skill description and in `SKILL.md` (FR-008).

**Alternatives considered.** A file in the project (rejected: FR-017 and the read-only rule); host memory (rejected: not available on Codex and not deterministic).

## R5. How `/code-review` resolves targets

**Finding.** The prompt says: "If a PR number, branch name, or file path was passed as an argument, review that target instead." Resolution is left to the model, which uses `git` and `gh` as needed. The line count used to size the review is computed with `git diff --numstat` on the target range.

**Decision.** The scientific review resolves targets deterministically in `panel.py scope`, which gains `--target`. A whole number, `#<n>`, or a pull request or merge request URL resolves to a pull request; its base and head are read with `gh pr view --json baseRefOid,headRefOid` (or `glab mr view`), the head commits are fetched into a temporary ref (`git fetch origin pull/<n>/head`, which writes only under `.git`, not the working tree), and the scope is the diff between the merge base and that head. A local or remote branch name resolves to branch mode with that branch as head. Existing paths resolve to paths mode. A token matching more than one form exits with code 3 and the candidates, so that the skill asks the user (FR-010). Missing `gh` or `glab`, or no authentication, exits with code 3 and the reason (FR-012).

**Note on FR-011.** Fetching a pull request head writes objects and a ref under `.git`. This is not the working tree or the index, and feature 007's project check (`git status --porcelain --ignored`) does not observe it. The temporary ref is deleted at `panel.py clean`.

## R6. Effort-level profiles

**Finding.** `/code-review` maps each level to a prompt "recipe" and a model effort; levels differ in the number of finder subagents (`ceil(lines / 150)`, between 2 and 8) and in recall versus precision ("from few high-confidence findings to many, some uncertain").

**Decision.** For the scientific review, a level maps to the panel parameters of feature 007, `medium` being the current defaults (FR-006). Values are non-decreasing (FR-005).

| Level | Perspectives | Rebuttal rounds | Debate batches | Default finding cap |
|-------|--------------|-----------------|----------------|---------------------|
| `low` | 3: `theorist`, `numerical-analyst`, `methodologist`; extensions only when named | 1 | 1 | none |
| `medium` | 5 defaults plus selected extensions (at most 7) | 2 | 2 | none |
| `high` | 5 defaults plus selected extensions (at most 7) | 2 | 3 | none |
| `xhigh` | 5 defaults plus selected extensions (at most 7) | 3 | 4 | none |
| `max` | 7: all defaults and selected extensions, up to the limit | 3 | 4 | none |

No level caps the Markdown report by default, so that a review with no arguments delivers every finding, as feature 007 does (spec FR-006). Delivery through the findings-reporting tool is clamped to 32, the tool's maximum, as in `/code-review` (R3 step 5), whatever the cap. The `low` set keeps one perspective for derivations, one for numerics and one for statistics, the dimensions where a single missed defect most often changes a result.

**Rationale.** Keeping the profile in the parameters that already exist keeps the protocol unchanged and the agent-invocation bound of feature 007 (research R7 there) valid: `max` equals feature 007's largest permitted panel.

## R7. Removing the review budget: review parts

**Finding.** `panel.py scope` currently adds files until 6,000 lines and records every further file as "over budget" (`DEFAULT_BUDGET = 6000`). `/code-review` has no limit; it scales the number of finder subagents with the diff size.

**Decision.**

1. `scope` drops `--budget`, `DEFAULT_BUDGET` and the "over budget" reason.
2. A new deterministic step, `panel.py parts`, divides the scope into review parts of at most 2,000 lines, the size for which feature 007 established its agent bound. Files are grouped by directory, in path order; a file larger than one part is split at top-level definition boundaries (Python `def`/`class`, TypeScript and JavaScript `function`/`class`/`export`, notebook cells), falling back to fixed line windows. Output: `parts.json`.
3. The independent round runs once per part per perspective. Each reviewer receives its part and may read any file of the project to follow a reference (spec edge case).
4. `panel.py merge` already clusters candidates by location across all candidate files; it runs once on the candidates of all parts, so a defect raised in two parts is merged before the debate (FR-021).
5. Above 6,000 lines (the large-scope threshold, FR-022), the skill states the size, file count and number of parts, and asks before any reviewer runs. The threshold is a constant in `panel.py`, reported by `parts`.

**Cost.** With P perspectives and K parts, the independent round makes P x K invocations instead of P; the debate is unchanged, because it runs on merged findings. For an 18,000-line scope at `medium` (9 parts), that is 45 independent-round invocations instead of 5.

**Alternatives considered.** One reviewer per perspective reading the whole scope (rejected: exceeds a reviewer's context for large scopes, which is why the budget existed); sampling (rejected: FR-020 requires full coverage).

## R8. Runner impact

- **Workflow runner**: the generated script iterates over `parts` in the independent round (`parallel` over perspective x part). `build_workflow.py` is updated; the parity test is extended to the part loop.
- **Codex subagents and Claude agents**: one subagent per perspective x part, in batches no larger than the host's concurrency limit.
- **Sequential runner**: parts in order, each perspective completing all parts before the next starts, preserving the independence order of feature 007 FR-028.

## R9. Hosts without command arguments

Claude Code passes the text after the command as `$ARGUMENTS`; the skill declares `argument-hint` in its frontmatter (FR-002). Codex, claude.ai and Cowork have no argument field; the skill passes the user's request text to `panel.py args --text`, which applies the same grammar, so that the same arguments written in the request are accepted (FR-019).

## R10. Tracking `/code-review` over time

The reproduced text is pinned to Claude Code 2.1.317. A test (`tests/test_sci_review_arguments.py`) checks that the `SKILL.md` sections cite that version; a release checklist item re-reads the sections from the current Claude Code binary with the method of section 0 and updates them when they change. No automated extraction is added, because the binary layout is not a public interface.
