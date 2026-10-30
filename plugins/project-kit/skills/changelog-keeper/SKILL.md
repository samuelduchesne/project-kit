---
name: changelog-keeper
description: Create new CHANGELOG.md files from git history, or audit and fix existing changelogs, following the Keep a Changelog 1.1.0 specification (https://keepachangelog.com). Use this skill whenever the user mentions a changelog, CHANGELOG.md, release notes derived from commits, "what changed since the last release," cutting a release, or wants to turn a git log / commit history into a human-readable changelog. Also trigger when the user asks to clean up, audit, validate, or reformat an existing changelog file, or mentions Keep a Changelog by name. Don't require the user to explicitly say "Keep a Changelog" — any request that involves producing release notes from commits, or improving an existing CHANGELOG, should pull this skill in.
---

# Changelog Keeper

Produce changelogs that humans actually want to read, following the [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) convention.

The format is mechanical. The hard part is judgment: filtering noise out of commits, grouping related changes, and rewriting commit-speak into entries that tell a user *what changed and why they should care*. Lean into that judgment — don't just transcribe.

## When to use this skill

Two workflows are supported:

1. **Create from scratch** — given a git log (or commit list) and optionally a version number, produce a new `CHANGELOG.md`.
2. **Audit / fix existing** — given an existing `CHANGELOG.md`, identify violations of the Keep a Changelog spec and produce a corrected version.

If the user gives input that fits neither workflow cleanly (e.g., free-form notes), still apply the format and principles below — they generalize.

## Guiding principles (non-negotiable)

These come straight from the spec. Internalize them:

- **Changelogs are for humans, not machines.** A reader should learn what changed and roughly why. If an entry doesn't help a human, drop it.
- **Group changes by type.** Use only the six categories below.
- **Latest version first.** Reverse chronological order, always.
- **Every released version gets an entry.** Empty entries are worse than no entry — omit categories that have nothing in them.
- **Dates are ISO 8601** (`YYYY-MM-DD`). Never regional formats.
- **Keep an `Unreleased` section at the top** to stage upcoming changes.
- **Mention SemVer adherence** in the preamble if the project follows it.
- **Don't dump the git log.** This is the single most common failure mode and the explicit thing the spec was created to prevent.

## The six change types

Use only these. If a change doesn't fit one, you're probably describing something that doesn't belong in a changelog (e.g., internal refactors with no user-visible effect).

- **Added** — new features.
- **Changed** — changes in existing functionality.
- **Deprecated** — soon-to-be-removed features. Always list these; never silently deprecate.
- **Removed** — features removed in this release.
- **Fixed** — bug fixes.
- **Security** — vulnerabilities. Be specific about severity and whether users need to act.

If a change is a breaking change, call it out explicitly in the entry text (e.g., "**Breaking:** ..."). The spec doesn't define a separate "Breaking" category — breaking changes are surfaced *within* Changed/Removed entries by being explicit.

## Standard format

Every changelog uses this skeleton. Use it verbatim except where noted.

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Short, human-readable description of the new feature.

## [1.2.0] - 2025-03-14

### Added

- ...

### Fixed

- ...

[unreleased]: https://github.com/OWNER/REPO/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/OWNER/REPO/compare/v1.1.0...v1.2.0
```

Notes on the skeleton:

- The SemVer line is included by default. If the user explicitly says they don't follow SemVer, drop that sentence.
- Version headings use `[X.Y.Z]` (in brackets) so they can be linked to compare URLs at the bottom of the file.
- The compare links at the bottom assume GitHub; adapt to GitLab/Bitbucket/etc. if the repo URL suggests otherwise. If you don't know the repo URL, omit the link definitions and tell the user to add them.
- Yanked releases get a `[YANKED]` tag in the heading: `## [0.0.5] - 2014-12-13 [YANKED]`.

## Workflow 1: Creating from a git log

Given commits, the goal is to produce *a curated narrative*, not a transcription. Process:

### Step 1: Read every commit and classify

For each commit, decide:

- **Drop it?** Merge commits, version bumps, CI/lint/formatting tweaks, dependency-only updates with no user-visible effect, internal refactors, doc-only changes (unless the docs are user-facing like a README), test-only changes — all noise. Drop them.
- **Keep it?** If it changes behavior, API, performance, security posture, or anything a user/consumer would notice on upgrade, keep it.
- **Which type?** Map to one of the six categories. Be honest — if a commit says "fix" but actually adds a feature, it's Added.

When in doubt about whether something is user-visible, err toward dropping it. A short, sharp changelog is better than a long noisy one.

### Step 2: Group and merge related commits

Multiple commits often describe one logical change. Merge them. Three commits ("start work on X", "more X", "finish X") become one entry: "Added X."

Conversely, a single commit can describe multiple changes — split it if needed.

### Step 3: Rewrite each entry for a human reader

Commit messages are written for the author's future self. Changelog entries are written for *users*. Rewrite accordingly:

- Past tense or imperative? **Past tense** for entries describing what shipped (e.g., "Added dark mode"). The leading `### Added` already implies the verb, so entries can also start with the noun ("Dark mode for the dashboard").
- **Drop implementation jargon.** "Refactored `UserService` to use repository pattern" → drop entirely (not user-visible) or, if the refactor *did* change behavior, describe the behavioral change.
- **Lead with the user-facing thing**, not the file or class. "Login form now accepts emails with `+` aliases" beats "Updated `validateEmail()` regex."
- **Mention the why if it isn't obvious.** Especially for Changed and Removed entries — a user reading the changelog wants to know if they need to act.
- **Be specific.** "Fixed a bug" is useless. "Fixed crash when importing CSVs with empty trailing rows" is useful.
- **End entries with a period.** Consistency matters; the spec's own changelog enforces this.

### Step 4: Order within each section

Within a section, order by importance (most impactful first), not by commit date. A breaking API change should appear above a typo fix in the same section.

### Step 5: Pick the version number

If the user supplied one, use it. If not:

- Look at the changes you classified. Any breaking changes (Removed entries, breaking Changed entries) → next major version.
- Any Added entries with no breakage → next minor.
- Only Fixed/Security → next patch.

If you had to infer the version, **say so** in your reply and ask the user to confirm.

### Step 6: Assemble

Produce the file using the standard skeleton. If this is a brand-new changelog covering the project's history, include all known prior versions in reverse chronological order. If it's just adding the latest release, leave space for older versions or note that they should be backfilled.

## Workflow 2: Auditing an existing changelog

Read the existing `CHANGELOG.md` and check it against the spec. Common violations to look for, with how to fix them:

| Violation | Fix |
|---|---|
| Missing preamble / Keep a Changelog reference | Add the standard preamble. |
| Non-ISO dates (`03/14/2025`, `Mar 14 2025`) | Convert to `YYYY-MM-DD`. |
| Categories outside the six standard ones (e.g., "Improvements", "Breaking") | Re-bucket into the six. Surface breaking changes by prefixing the entry text. |
| Empty category sections (`### Removed` with no entries) | Delete the empty section. |
| Commit-log-style entries (hashes, "Merge branch...", author names) | Rewrite as human-readable entries; drop noise. |
| Versions out of order | Reorder, latest first. |
| Missing `[Unreleased]` section | Add at top. |
| Missing or stale link definitions at bottom | Regenerate compare links. |
| Inconsistent voice / tense / punctuation | Normalize across the file. |
| Vague entries ("various fixes", "minor changes") | Flag these — ask the user for detail; don't fabricate it. |

When auditing, **never invent content**. If an entry is too vague to fix without more information, leave it and note it in your reply for the user to clarify. Fabricating changelog content is worse than leaving it imperfect — users rely on the changelog being accurate.

Produce the corrected file plus a short summary of what you changed and why.

## Anti-patterns to avoid

The Keep a Changelog spec calls these out explicitly. Avoid them:

- **Dumping the git log.** Commit logs are full of noise; changelogs are curated. If your output reads like `git log --oneline`, start over.
- **Ignoring deprecations.** A deprecation that isn't in the changelog is a trap for users. List every one.
- **Confusing dates.** Always ISO 8601.
- **Inconsistent changes.** If the changelog only mentions some changes, users will assume it's complete and miss the rest. Either it's the source of truth or it's worse than nothing.

## Examples

**Bad (commit-dump style):**
```
### Changes
- 8a3f1c2 fix login bug
- d2e4f5a Merge pull request #142 from feature/dark-mode
- 9c1b3a7 wip
- e4d2c1b update deps
- 7b8a9c0 fix typo in README
```

**Good (curated):**
```markdown
## [2.1.0] - 2025-03-14

### Added

- Dark mode for the dashboard, toggleable in user settings.

### Fixed

- Login no longer fails for users whose email contains a `+` alias.
```

(The `wip` commit, dependency update, and README typo were dropped as noise. The merge commit was collapsed into the feature it delivered.)

**Bad (vague):**
```markdown
### Fixed
- Various bug fixes and improvements.
```

**Good (specific):**
```markdown
### Fixed
- Fixed crash when uploading files larger than 100 MB on Safari.
- Fixed timezone offset error in scheduled report emails for non-UTC users.
```

## Output expectations

- For **create** workflows: write the changelog to `CHANGELOG.md` (or whatever path the user specifies). After creating it, briefly summarize the choices you made — particularly any commits you dropped, version numbers you inferred, or repo-URL assumptions for the compare links — so the user can sanity-check.
- For **audit** workflows: produce the corrected file and a short diff-style summary of what changed. Flag anything you couldn't fix without more information rather than guessing.
- Keep your reply focused on the changelog itself; the file is the deliverable, not a long prose explanation.

## Reference

For the full Keep a Changelog 1.1.0 spec — including FAQs, edge cases like yanked releases, and the rationale behind specific choices — see `references/keep-a-changelog-1.1.0.md`. Read it when you encounter a situation this SKILL.md doesn't cover.
