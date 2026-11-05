# Implementation Plan: Code-review-style arguments for sci-review

**Branch**: `008-sci-review-arguments` | **Date**: 2026-11-04 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/008-sci-review-arguments/spec.md`, plus the planning directive to research how Claude Code's `/code-review` implements `--fix` and `--comment` and to reproduce that implementation.

## Summary

The `sci-review:scientific-review` skill gains the argument grammar of `/code-review`: an effort level, a target (pull request, branch or paths), `--comment`, `--fix` and `--max-findings`, with the level and the finding cap persisted per user. The fixed 6,000-line review budget is removed; large scopes are divided into review parts that are each reviewed in full.

Research ([research.md](./research.md)) read `/code-review`'s implementation from the Claude Code 2.1.317 binary. Its argument parsing and preference storage are code; its `--fix` and `--comment` are prompt sections that the orchestrating model follows after reporting the findings, with no confirmation, no separate agent and no patch file (R1, R2). The plan reproduces that split:

1. **Deterministic steps in `panel.py`** (Principle II): `args` parses the grammar (R3), `prefs` reads and writes the user's preferences outside the project (R4), `scope --target` resolves pull requests, branches and paths (R5), `panel --level` applies the level profile (R6), and `parts` divides the scope (R7).
2. **Prompt sections in `SKILL.md`**, reproduced from `/code-review` with the adaptations listed in R1 and R2: "Posting to GitHub / GitLab (--comment)", "Applying fixes (--fix)", "If findings are fixed later", and the outcome lines. The orchestrating conversation executes them after the delivery step, on every runner.
3. **Runner changes** limited to the independent round, which runs once per review part (R8).

## Technical Context

**Language/Version**: Markdown skill; Python 3.10+ standard library for `scripts/panel.py`; JavaScript (ES2022) for the generated Workflow script.

**Primary Dependencies**: as feature 007; in addition, `gh` (GitHub) or `glab` (GitLab) for pull request targets and `--comment`, both optional and detected at start; the host's `mcp__github_inline_comment__create_inline_comment` tool when present, as in `/code-review`.

**Storage**: Run directory under the system temporary directory (unchanged). User preferences in `$XDG_CONFIG_HOME/sci-review/preferences.json` (default `~/.config/sci-review/`; `%APPDATA%\sci-review\` on Windows), never in the reviewed project. A temporary git ref for a fetched pull request head, removed by `panel.py clean`.

**Testing**: `unittest`: a new `tests/test_sci_review_arguments.py` (grammar table for SC-001 and SC-004, preference persistence, target resolution on a fixture repository, level profiles for SC-002 and SC-003, part division for SC-008); extensions of `tests/test_sci_review_panel.py` (no "over budget" exclusion; merge across parts) and `tests/test_sci_review_workflow_build.py` (part loop parity). Manual runs per [quickstart.md](./quickstart.md) for `--comment`, `--fix` (SC-005, SC-006, SC-010) and the large-scope prompt, consistent with the constitution's deferral of automated evals.

**Target Platform**: as feature 007: Claude Code, claude.ai chat and Cowork, Codex.

**Project Type**: Agent plugin (skill, helper script, generated workflow).

**Performance Goals**: At `medium` on a scope within one review part (2,000 lines), the agent-invocation bound of feature 007 is unchanged (at most 45). Above that, the independent round grows to P x K invocations for P perspectives and K parts; the debate does not grow with K (R7).

**Constraints**: Read-only on the project except the closing `--fix` step; no reviewer receives another perspective's output; `max` never selected by the model on its own initiative; reproduced `/code-review` text pinned to Claude Code 2.1.317 (R10).

**Scale/Scope**: Five levels, three target forms, three flags; scopes of any size, with confirmation above 6,000 lines.

No item remains marked NEEDS CLARIFICATION; each was resolved in research.md.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitution version 1.2.0.

| Principle | Check | Result |
|-----------|-------|--------|
| I. Templates are the source of truth | `sci-review` generates no project files. | Not applicable (constitution, Scope and Constraints) |
| II. Scripts for predictable steps, the model for judgment | Argument parsing, preference storage, target resolution, level profiles, part division and the large-scope threshold run in `panel.py` with logged arguments. The model reviews, debates, decides which findings to skip under `--fix`, writes the fixes and the comments. New writing subcommands (`args`, `prefs`, `parts`) accept `--dry-run`; `prefs` writes outside the run directory only to the preferences file. | Pass |
| III. Show before changing | `--fix` writes to the working tree without showing a diff or asking for confirmation, as `/code-review --fix` does (spec FR-016, research R1). This violates "MUST show the user a diff or a list of planned changes and get confirmation before writing". | **Violation, justified in Complexity Tracking; requires amendment before implementation** |
| III (scope) | The constitution's Scope and Constraints describe `sci-review` as "read-only on the reviewed project". `--fix` contradicts it. | **Same amendment** |
| IV. Works wherever it is installed | Pull request targets and `--comment` need `gh` or `glab`; they are detected at start and the review offers a branch or paths review, or prints the findings, instead of failing (FR-012, R2). Preferences degrade to defaults with a notice where no configuration directory is writable (FR-018). Arguments are accepted in the request text where the host has no argument field (R9). Version pinning: Principle IV as amended by item 2 below applies the pin rule to tools the plugin installs (spec-kit, cruft, cookiecutter). `git`, `gh` and `glab` are user-installed hosting clients that the plugin detects, not installs; as for `git` in feature 007, they are not pinned, and `panel.py` checks a minimum version only where a subcommand it calls requires one, reporting the installed and required versions when the check fails. | Pass |
| Development workflow | Spec-kit flow; CHANGELOG entry under `[Unreleased]`; `claude plugin validate` on both plugins; `sci-review` minor version bump. | Pass |

**Required amendment (first implementation task, precondition of the gate).** Constitution 1.2.0 to 1.3.0 (MINOR), with a stated reason. The version class is MINOR because the amendment adds a bounded exception and leaves the principle's rules unchanged for every other command; it neither removes nor redefines Principle III. The amendment lands in the same pull request as this feature, which states its reason (Governance), and is its first commit.

1. Principle III gains: "Exception: a review command MAY apply its own findings to the working tree without a further confirmation when the user passed an explicit flag requesting it (`--fix`), provided nothing is staged or committed and every change is reported. Passing the flag is the user's explicit acceptance of the risk of writing to a working tree that has uncommitted changes; the command does not require a clean working tree." 
2. Principle IV, third bullet, gains a clarification (PATCH-level, carried by the same amendment): "The pin rule applies to tools the plugin installs. User-installed clients that the plugin detects and calls (`git`, `gh`, `glab`) are checked for presence and, where a command requires it, a minimum version; they are not pinned."
3. Scope and Constraints, `sci-review`: "read-only on the reviewed project, except when the user passes `--fix`, which applies the delivered findings to the working tree after the report".

Feature 007's FR-006 and SC-004 are narrowed by this spec (FR-016e, SC-005) and need no separate change.

**Post-design re-check (after Phase 1)**: Pass, conditional on the amendment. The design adds no core dependency on an environment-specific component: `gh`, `glab`, the inline-comment tool and the preferences directory are all optional with stated fallbacks. The `--fix` section writes only from the orchestrating conversation, after the report; no panel member, runner or `panel.py` subcommand writes to the project.

## Project Structure

### Documentation (this feature)

```text
specs/008-sci-review-arguments/
├── plan.md              # This file
├── research.md          # Phase 0: /code-review implementation, decisions R1 to R10
├── data-model.md        # Phase 1: entities and file formats
├── quickstart.md        # Phase 1: validation scenarios
├── contracts/
│   ├── arguments.md     # Grammar, panel.py args/prefs, level profiles
│   ├── targets-and-parts.md  # scope --target, parts, large-scope threshold
│   └── fix-and-comment.md    # SKILL.md sections reproduced from /code-review
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 (/speckit-tasks)
```

### Source Code (repository root)

```text
.specify/memory/constitution.md                 # amendment 1.3.0
plugins/sci-review/
├── .claude-plugin/plugin.json                  # version bump
├── .codex-plugin/plugin.json                   # version bump
├── README.md                                   # arguments, --fix, --comment, no budget
├── scripts/
│   ├── panel.py                                # args, prefs, scope --target, panel --level, parts; budget removed
│   └── build_workflow.py                       # part loop in the independent round
├── scripts/scientific-review-panel.js          # regenerated (moved from workflows/scientific-review.js in commit 8c93198; not registered)
└── skills/scientific-review/
    ├── SKILL.md                                # argument-hint; sections 2, 5, 7 rewritten; --comment, --fix, fixed-later sections
    ├── protocol.md                             # independent round per part; section 10 fallback rules for args/parts
    └── runners/*.md                            # independent round per part
specs/007-sci-review-plugin/contracts/invocation.md   # pointer to 008 contracts
tests/
├── test_sci_review_arguments.py                # new
├── test_sci_review_panel.py                    # budget removal, merge across parts
├── test_sci_review_workflow_build.py           # part loop parity
└── fixtures/sci-review/large-scope/            # 18,000-line fixture with a defect in the last file
CHANGELOG.md
```

**Structure Decision**: The feature extends the existing `plugins/sci-review` tree; no new component is introduced. Deterministic logic goes into `panel.py`, reproduced `/code-review` behaviour into `SKILL.md`, matching the split that `/code-review` itself uses between code and prompt.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principle III: `--fix` writes without showing a diff and asking first | The user directed that `--fix` behave and be implemented as `/code-review --fix` (spec FR-016), which applies fixes directly; passing the flag is the confirmation. Changes are left unstaged and uncommitted, so each is reversible with `git restore`, and every finding is re-reported with an outcome. | Showing a diff and asking (Principle III as written) departs from `/code-review`, which the user rejected; printing patches only (option A at specify time) was also rejected by the user. |
| Principle III: `--fix` does not require a clean working tree | `/code-review --fix` performs no clean-tree check (research R1); the user directed parity. The amendment makes the flag the explicit acceptance of the risk that the principle already allows. Nothing is staged, so the user can still separate the fixes from earlier edits with `git diff`. | Checking first and asking departs from `/code-review` in the common case of a feature branch with uncommitted work; refusing on a dirty tree makes `--fix` unusable in that case. |
| `sci-review` scope: no longer strictly read-only | Same as above. The read-only guarantee is kept for every review without `--fix` (FR-016e) and for every panel phase with it (FR-016a). | Rejecting `--fix` (option C) leaves the grammar incomplete, against the user's request to copy `/code-review`'s arguments. |
