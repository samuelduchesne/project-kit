---
name: review-docs
description: >-
  Review user-facing documentation against a scoped code diff to find misalignments: stale signatures, renamed flags, changed config fields, broken examples, undocumented features. Defaults to the current branch's own diff (the PR diff) and accepts a narrower scope: a git range, specific paths, a topic, or a drift category. Use this skill whenever you've made code changes and want to check if docs are still accurate, when reviewing a PR or branch, before a release, or when the user asks to audit documentation. Also trigger when the user says "check docs", "docs review", "are the docs up to date", "documentation audit", "did I forget to update the docs", or asks to review the docs for a specific PR, branch, release, directory, or feature.
---

# Documentation Review

Review hand-written user-facing documentation against code changes to find misalignments: stale API signatures, renamed CLI flags, changed config fields, broken examples, and undocumented new features.

This runs as a **multi-agent workflow** (`project-kit:review-docs`): one agent resolves the diff baseline, maps the project's docs structure, and builds independent code→docs review units; the units are reviewed in parallel; every finding is confirmed by a 3-lens adversarial verification panel (correctness / doc-accuracy / does-it-actually-mislead) so false positives are dropped; then a synthesis agent produces the severity-ranked report.

Works with any project that ships mkdocs-style docs (mkdocs-material, mkdocstrings, mkdocs-jupyter, `pymdownx.snippets`). It discovers the project structure fresh each run, with no hardcoded paths.

## Prerequisites

This skill requires the `Workflow` tool, which is documented for the Claude Code CLI, desktop app and IDE extensions. The plugin ships the workflow itself in `workflows/review-docs.js`. If the tool is unavailable or workflows are disabled, state what is missing and stop.

## Scoping the review

Scope is the single thing most likely to make this report useful or useless. A review scoped to a whole release when the user is looking at one PR buries the handful of findings they can act on under drift that predates their branch and isn't theirs to fix. So read the user's request for scope before launching, and pass it through.

Four independent axes, all optional, all passed via `args`:

| Axis | Type | What it does |
| --- | --- | --- |
| `baseline` | string | The git ref or range to diff against. A bare ref (`main`, `v0.3.0`, `abc1234`) becomes `<ref>..HEAD`; `main...HEAD` resolves to the merge-base. |
| `paths` | string[] | Restrict to these paths. Matches **either** side of the code→docs mapping, so `["docs/cli/"]` and `["src/foo/cli.py"]` both work. |
| `focus` | string | Freeform topic. Units unrelated to it are dropped. |
| `categories` | string[] | Subset of `api`, `cli`, `configuration`, `installation`, `behavioral`, `example-notebook`, `missing-docs`. |

**With no `args`, the workflow picks the baseline itself**, preferring the narrower one: if HEAD is on a branch that has diverged from the default branch, it uses `merge-base(default, HEAD)..HEAD`, the branch's own diff. Otherwise it falls back to the most recent tag. Uncommitted work is always included either way. So on a PR branch, launching with no args already does the right thing; you only need `baseline` when the user wants something *other* than that.

### Reading scope out of the request

| The user says | Pass |
| --- | --- |
| "review the docs" (on a feature branch) | *(nothing; auto-detects the branch diff)* |
| "check the docs for this PR" / "just my changes" | *(nothing, or `{ baseline: "main" }` to be explicit)* |
| "audit the docs before the release" / "since the last release" | `{ baseline: "<latest tag>" }`, or nothing if already on the default branch |
| "what's drifted since v0.3.0" | `{ baseline: "v0.3.0" }` |
| "the last 3 commits" | `{ baseline: "HEAD~3" }` |
| "only the flexshell docs" | `{ paths: ["docs/flexshell/"] }` |
| "focus on the per-zone assumptions work" | `{ focus: "per-zone modeling assumptions" }` |
| "are my code examples still valid?" | `{ categories: ["example-notebook", "api"] }` |
| "did I document the new CLI flags?" | `{ categories: ["cli", "missing-docs"] }` |

Combine axes freely: `{ baseline: "main", paths: ["docs/quest-phase-2/"] }` is a normal request.

Don't interrogate the user about scope when their intent is already legible. If it genuinely isn't (say they're on `main` with both uncommitted work and three tags behind, and they just say "check the docs"), ask one short question rather than guessing, since the wrong baseline wastes the whole run.

## How to run it

```
Workflow({ name: "project-kit:review-docs" })                                  // auto-scoped
Workflow({ name: "project-kit:review-docs", args: { baseline: "v0.3.0" } })     // explicit
Workflow({ name: "project-kit:review-docs", args: { focus: "CLI flags", categories: ["cli"] } })
```

When the user invoked this skill or asked for this review, launching it satisfies the Workflow opt-in requirement, so do not ask again. If you invoked the skill on your own initiative, ask before launching, because a run spawns many agents. The workflow does all the git/file work inside its agents; you just launch it and handle the result.

## What it returns

A structured report object with `critical`, `warning`, and `info` arrays, plus `baseline`, `scopeNote`, `lastTag`, a `coverageNote`, and an optional `note`. Each finding carries: `whatChanged` + `codeLocation`, `docLocation`, `whatsWrong`, and `suggestedFix`.

Severity meanings:

- **Critical**: docs are actively wrong and will mislead users (renames where docs use the old name, removed features still documented, changed defaults, examples that would raise errors, dead import paths).
- **Warning**: docs are incomplete or stale (new features/CLI commands with no docs, changed behavior not reflected, new extras undocumented).
- **Info**: minor or cosmetic (help-text wording, could-mention-a-feature, minor version discrepancies, style).

## Presenting the result

1. **Lead with the scope.** State `scopeNote` (or `baseline`) in one line before the findings: "Reviewed the 7 commits on `per-zone-modeling-assumptions` since it branched from `main`, plus uncommitted work." The reader can then tell instantly whether the run matched their intent, and correct it in one message if not, instead of reading findings that were never in scope.
2. Render the report grouped by severity, most-actionable first. For each finding show what changed (with `codeLocation`), where the doc is wrong (`docLocation`), what's wrong, and the suggested fix.
3. Include the `coverageNote` so the user knows what was reviewed and which auto-generated docs (mkdocstrings `:::` pages, etc.) were intentionally skipped.
4. If every severity array is empty, say so clearly; that's a good outcome, and say it *in scope terms* ("nothing drifted in this branch's diff"). Surface the `note`.
5. If the report mentions changes dropped as out of scope, offer to rerun wider.

## Hand off

Sort the fixes by what they actually need before offering anything:

- **Facts** (a renamed flag, a changed default, a dead import, a broken example)
  are yours. They need the code, and the fix is a correct value, not a better
  sentence. Apply them directly.
- **Prose** (a section that now explains the wrong thing, an opening that no
  longer matches what the feature does, wording that drifted with the behavior)
  goes to the `project-kit:editor` agent in revise mode, once the facts are right. Give it
  the corrected facts and the finding, and let it own the wording. If agents are
  not available, apply the `project-kit:editorial` skill yourself.

Then offer to turn the rest into a fix plan:

> Here's what I found. Want me to create a plan to fix these? Run `/plan` and I'll use this report as the basis.
