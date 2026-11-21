---
name: review-docs
description: >-
  Review user-facing documentation against a scoped code diff at an effort level (low|medium|high|xhigh|max) to find misalignments: stale signatures, renamed flags, changed config fields, broken examples, undocumented features. Defaults to the current branch's own diff (the PR diff) and accepts a narrower scope: a git range, specific paths, a topic, or a drift category. Use this skill whenever you've made code changes and want to check if docs are still accurate, when reviewing a PR or branch, before a release, or when the user asks to audit documentation. Also trigger when the user says "check docs", "docs review", "are the docs up to date", "documentation audit", "did I forget to update the docs", or asks to review the docs for a specific PR, branch, release, directory, or feature. Use the max level only when the user, or instructions such as CLAUDE.md or a skill, explicitly ask for it, never on your own judgment: it is the costliest level and starts many reviewer agents.
argument-hint: "[low|medium|high|xhigh|max] [<ref>|<range>|<path>...] [--focus <topic>] [--categories <a,b>] [--fix] [--max-findings <n>|all]"
---

# Documentation review

Review hand-written user-facing documentation against code changes and report misalignments: stale API signatures, renamed CLI flags, changed config fields, broken examples and undocumented features. It works with mkdocs-style docs (mkdocs-material, mkdocstrings, mkdocs-jupyter, `pymdownx.snippets`) and discovers the project's structure on each run.

The review works like `/code-review`: an effort level sets how much it spends. `low` and `medium` run in this conversation with no subagents. `high` and `xhigh` launch the `project-kit:review-docs` workflow with a bounded number of agents. Only `max` runs the full adversarial panel.

## 1. Arguments

```text
/project-kit:review-docs [low|medium|high|xhigh|max] [<ref>|<range>|<path>...] [--focus <topic>] [--categories <a,b>] [--fix] [--max-findings <n>|all]
```

| Argument | Meaning |
| --- | --- |
| level | Effort level, section 2. Default `medium`. |
| ref or range | The baseline: `main`, `v0.3.0`, `HEAD~3`, `main...HEAD`. A bare ref becomes `<ref>..HEAD`. Without one, the baseline is chosen as in section 3. |
| paths | Restrict to these paths. A path can name either side of the code→docs mapping: `docs/cli/` and `src/foo/cli.py` both work. An argument that exists as a file or directory is a path; otherwise it is a ref. |
| `--focus` | A topic. Code areas unrelated to it are dropped. |
| `--categories` | A subset of `api`, `cli`, `configuration`, `installation`, `behavioral`, `example-notebook`, `missing-docs`. |
| `--fix` | After the report, apply the findings to the docs (section 6). |
| `--max-findings` | Report at most `n` findings, most severe first; `all` removes the limit. The number withheld is stated. |

Where the host has no argument field, read the same values from the wording of the request:

| The user says | Read as |
| --- | --- |
| "review the docs" (on a feature branch) | nothing; the branch diff is the default |
| "a quick docs check" | `low` |
| "a thorough docs review" | `high` |
| "audit the docs before the release" | the latest tag as baseline |
| "what's drifted since v0.3.0" | `v0.3.0` |
| "only the flexshell docs" | `docs/flexshell/` |
| "focus on the per-zone assumptions work" | `--focus "per-zone modeling assumptions"` |
| "are my code examples still valid?" | `--categories example-notebook,api` |
| "did I document the new CLI flags?" | `--categories cli,missing-docs` |

Do not question the user about scope when the request already makes it clear. If it does not (on `main`, with uncommitted work and several tags behind, and only "check the docs"), ask one short question, because the wrong baseline wastes the whole run.

## 2. Effort levels

| Level | Where it runs | Reviewers | Verification | Default cap | Agents (typical) |
| --- | --- | --- | --- | --- | --- |
| `low` | this conversation | you | you re-read each cited line | 5, critical only | 0 |
| `medium` | this conversation | you | you re-read each cited line and apply the three checks | 10 | 0 |
| `high` | workflow | 1 per code area, at most 4 | 1 agent per code area checks all its findings | 15 | ≤ 8 |
| `xhigh` | workflow | 1 per code area, at most 8 | 1 agent per finding | 25 | 15–30 |
| `max` | workflow | 1 per code area, no limit | 3 agents per finding, one per check, majority wins | none | 50+ |

The three checks are the same at every level:

1. **Correctness**: the code change exists at the cited line, inside the range or the uncommitted work.
2. **Doc accuracy**: the doc at the cited line really says the stale thing. For missing docs, the docs really do not cover the feature.
3. **Misleads**: a reader following the doc would be misled, get a wrong result or hit an error. Pedantry fails this check.

Use `max` only when the user, or instructions such as CLAUDE.md, explicitly ask for it. If you start the review on your own initiative, use `low` or `medium`, and ask before any workflow level.

## 3. Map the review (every level)

Do this yourself, in this conversation, at every level. It is cheap, and the result is passed to the workflow so no agent repeats it.

1. **Baseline.** With an explicit ref, resolve it: a bare ref becomes `<ref>..HEAD`; `A...HEAD` becomes `$(git merge-base A HEAD)..HEAD`. Otherwise prefer the narrower range:
   - Default branch: `git symbolic-ref --quiet --short refs/remotes/origin/HEAD`, else the first of `origin/main`, `origin/master`, `main`, `master` that exists.
   - On a branch that has diverged from it (`git rev-list --count <default>..HEAD` > 0): `$(git merge-base <default> HEAD)..HEAD` (scope mode `branch`).
   - Otherwise the latest tag: `git describe --tags --abbrev=0 HEAD`, range `<tag>..HEAD` (scope mode `tag`).

   Uncommitted work (`git status --short`, `git diff`, `git diff --cached`) is always in scope. Write a one-sentence scope note, such as "the 7 commits on `per-zone-modeling-assumptions` since it branched from `main`, plus uncommitted work".
2. **Changed code.** `git diff --stat RANGE` and `git log --oneline RANGE`. If only tests changed, report that nothing doc-relevant changed and stop.
3. **Docs.** Read `mkdocs.yml` (`docs_dir`, `nav`, plugins). Skip auto-generated pages (mostly `:::` mkdocstrings directives), but keep hand-written parts of mixed pages. Snippets and notebooks are hand-written and drift-prone.
4. **Units.** Group the changed code into areas that map to hand-written docs: CLI entry points → CLI reference; `__init__.py` exports → guides and examples; config models → configuration docs; `pyproject.toml` extras and entry points → installation. For each area, find the doc files with `grep -rl` on the changed names; do not read whole pages yet. Drop areas outside `paths`, `--focus` or `--categories`, and note what was dropped.

## 4. Run the review

### `low` and `medium`: inline

For each unit, read the code diff for its files, then grep its doc files for every renamed or changed symbol, flag, field and default, and read only the matching passages. Check the drift categories that apply:

- **api**: signatures, defaults, renames, moved import paths, deprecated API shown as current.
- **cli**: commands, flags and defaults added, removed or renamed.
- **configuration**: fields, types, enum and `Literal` values, defaults.
- **installation**: extras, minimum Python version, required dependencies.
- **behavioral**: outputs, error messages, workflow.
- **example-notebook**: snippets, config examples and notebooks that use old names.
- **missing-docs**: a user-facing feature with no documentation.

Severity: **critical** when the doc is actively wrong and misleads or errors; **warning** when it is incomplete or stale; **info** when the issue is cosmetic. At `low`, report only critical findings you are sure of. At `medium`, check every candidate against the three checks of section 2 by re-opening the cited code and doc lines, and drop any candidate that fails one.

### `high`, `xhigh` and `max`: workflow

When the user asked for the review, that request satisfies the Workflow opt-in. Launch it with the map from section 3:

```js
Workflow({ name: "project-kit:review-docs", args: {
  level: "high",                       // high | xhigh | max
  maxFindings: 15,                     // optional; a number or "all"
  focus: "CLI flags",                  // optional
  categories: ["cli", "missing-docs"], // optional
  map: {
    baseline: "a1b2c3d..HEAD",
    scopeMode: "branch",               // explicit | branch | tag | fallback
    scopeNote: "the 7 commits on ... plus uncommitted work",
    lastTag: "v0.3.0",
    skippedAutogen: ["docs/api/foo.md"],
    reviewUnits: [{ id: "cli-flags", codeArea: "...", changedFilesSummary: "...",
                    docPaths: ["docs/cli.md"], driftCategories: ["cli"] }],
  },
} })
```

If `map` is omitted, the workflow builds it with one extra agent. Units beyond the level's limit are merged, not dropped. The Workflow tool is documented for the Claude Code CLI, desktop app and IDE extensions. Where it is unavailable, say so and run the review at `medium` instead.

The workflow returns `{ level, baseline, scopeNote, findings, withheld, coverageNote, incomplete, note }`. Each finding has `severity`, `category`, `whatChanged`, `codeLocation`, `docLocation`, `whatsWrong`, `readerImpact` and `suggestedFix`, and findings are sorted most severe first. A non-empty `incomplete` list means some checks did not finish, so an empty result does not prove the docs are aligned.

## 5. Report

1. **State the scope first**, in one line, from the scope note, so the user can tell whether the run matched their intent.
2. **Report the findings.** If the `ReportFindings` tool is available, call it once, most severe first, with `file` and `line` taken from `docLocation`, `category` set to the drift category, `summary` set to what is wrong and what changed (with `codeLocation`), `failure_scenario` set to the reader impact, and `severity` set to `important` for critical and warning findings and `nit` for info findings. Do not also print the findings as text. Otherwise render them grouped by severity, each with what changed, where the doc is wrong, what is wrong and the suggested fix.
3. Give the level, the number of findings withheld by the cap, any incomplete checks, and the auto-generated docs that were skipped.
4. If there are no findings, say so in scope terms ("nothing drifted in this branch's diff"). If changes were dropped as out of scope, offer to rerun wider or at a higher level.

## 6. Fix

With `--fix`, or when the user accepts the offer, sort the fixes by what they need:

- **Facts** (a renamed flag, a changed default, a dead import, a broken example) need the code, and the fix is a correct value. Apply them directly.
- **Prose** (a section that now explains the wrong thing, wording that drifted with the behaviour) goes to the `project-kit:editor` agent in revise mode once the facts are right. Give it the corrected facts and the finding. If agents are not available, apply the `project-kit:editorial` skill yourself.

Edit the working tree only; stage and commit nothing. If `ReportFindings` was used, call it again with each finding's `outcome` (`fixed`, `skipped` or `no_change_needed`). Without `--fix`, offer to apply the fixes or to turn the report into a plan.
