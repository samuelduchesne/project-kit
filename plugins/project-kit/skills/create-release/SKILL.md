---
name: create-release
description: Cut a new release of a software package, Python or Node.js. Detects the project type, bumps the version with the right tool (`uv version --bump` for Python, `npm version` for Node), makes sure the changelog is updated, drafts real release notes, and creates the GitHub release with `gh release create`. Use this skill whenever the user mentions "cut a release", "release a new version", "ship a release", "tag a release", "publish to PyPI", "publish to npm", or asks to bump a version number ahead of a release. Also use it any time the user is preparing to tag and publish, even if they only mention one piece of the workflow ("bump the version", "draft release notes"), because forgetting the version bump or skipping the changelog update is the recurring failure mode this skill exists to prevent. Use this skill before reaching for project-kit:changelog-keeper directly; this skill orchestrates the full release workflow and calls into project-kit:changelog-keeper as one of its steps.
---

# Create Release

Cuts a clean release of a package: version bump, changelog, release notes, GitHub release. The point is to do all four in the right order with nothing forgotten. The recurring failure mode is shipping a release where one of these steps got skipped, usually the version bump in the manifest file, or stale `[Unreleased]` entries in `CHANGELOG.md`.

This skill works for both Python and Node.js packages. The version-bump tooling differs by ecosystem; everything else (changelog, release notes, tagging, GitHub release) is identical.

## Prerequisites

Before Step 1, check that `git` and `gh` are available and that `gh auth status` succeeds. As soon as Step 2 identifies the ecosystem, and before bumping, check for its version-bump tool as well. If anything is missing, state what is missing and stop; do not begin a release that cannot be completed in this environment.

Also check that `git status --porcelain` is empty. If the working tree has uncommitted changes, show them and proceed only if the user explicitly accepts the risk.

## Workflow

Walk these steps in order. Don't skip ahead, each step's output feeds the next.

### Step 1: Confirm the bump type

Before touching anything, decide on the version bump (major / minor / patch). Look at the commits since the last tag:

```bash
LAST_TAG=$(gh release list --limit 1 --json tagName -q '.[0].tagName')   # most recent release
if [ -n "$LAST_TAG" ]; then git log "$LAST_TAG..HEAD" --oneline; else git log --oneline; fi   # full history for a first release
```

Classify the changes:

- **Breaking changes** (removed APIs, renamed kwargs/params, behavior changes downstream code must handle) → **major** bump (or **minor** if the project is pre-1.0 and uses 0.x.0 for breaking changes, check the manifest file and recent release history to see which convention the project follows).
- **New features, no breakage** → **minor**.
- **Bug fixes, docs, internal cleanup only** → **patch**.

State the proposed bump and a one-sentence justification, then ask the user to confirm before proceeding. Don't guess silently.

### Step 2: Detect the project type, then bump the version

First, figure out which ecosystem this project is: check for `pyproject.toml` (Python) versus `package.json` (Node.js). Most projects have exactly one; if both are present (e.g. a repo with Python tooling around a JS frontend), ask the user which package is being released.

```bash
ls pyproject.toml package.json 2>/dev/null
```

This is the step most likely to be forgotten. **Always use the ecosystem's official version-bump command**, don't hand-edit the manifest file, don't ask the user to do it, don't skip and assume CI handles it.

#### Python (uv)

```bash
uv version --bump <major|minor|patch> --dry-run    # preview
uv version --bump <major|minor|patch>              # apply
```

`uv` updates `pyproject.toml` and `uv.lock` together. Verify the new version:

```bash
uv version              # prints the new version
git diff pyproject.toml # confirm the bump landed
```

`uv version` also supports `stable`, `alpha`, `beta`, `rc`, `post`, and `dev` components for pre-release flows. For the common case of cutting a stable release, stick to `major`/`minor`/`patch`.

If the project doesn't use `uv` (no `uv.lock`, no `[tool.uv]` section, `pyproject.toml` uses Poetry/Hatch/etc. exclusively), fall back to whatever the project's tooling expects, but flag this to the user, since this skill is built around `uv`.

#### Node.js (npm)

```bash
npm pkg get version                                    # current version
npm version <major|minor|patch> --no-git-tag-version   # apply
```

`npm version` has no preview mode: passing `--dry-run` still applies the bump, so a preview followed by the real command bumps twice. Work out the target version from the current one and the bump type, show it to the user for confirmation, and run the command once.

Pass `--no-git-tag-version` so `npm` only edits the manifest and lockfile; this skill handles the commit and tag itself in Step 5, matching how the Python path works. Without that flag, `npm version` commits and tags on its own, which would create a duplicate, out-of-order commit.

`npm version` updates `package.json` and, since npm 7, `package-lock.json` together. Verify the new version:

```bash
npm pkg get version         # prints the new version
git diff package.json       # confirm the bump landed
```

If the project uses Yarn or pnpm instead of npm (look for `yarn.lock` or `pnpm-lock.yaml` next to `package.json`), use that tool's equivalent instead: `yarn version --new-version <x.y.z> --no-git-tag-version`, or `pnpm version <major|minor|patch> --no-git-tag-version`. The manifest field being bumped is the same `package.json` `"version"` key either way; only the command and lockfile differ.

### Step 3: Update the changelog

Check whether the changelog has already been updated for this release:

```bash
head -40 CHANGELOG.md
```

Look for an `[Unreleased]` section with real entries in it (not just empty category headers). Two cases:

- **Changelog is already up to date** for this release: entries cover everything since the last tag, version-numbered and dated. Skip to Step 4.
- **Changelog is stale or has a non-empty `[Unreleased]` section**: invoke the **project-kit:changelog-keeper** skill to handle it. That skill knows the Keep a Changelog 1.1.0 spec, the six change categories, and how to turn commits into curated entries. Don't reimplement that logic here. After project-kit:changelog-keeper finishes, the `[Unreleased]` section should have been promoted to `[X.Y.Z] - YYYY-MM-DD` matching the version from Step 2.

If the project doesn't have a `CHANGELOG.md` at all, ask the user whether they want one. If yes, hand off to project-kit:changelog-keeper to create it from the git log. If they decline, continue without, but the GitHub release notes drafted in Step 4 will be the only record of what changed, so make them good.

### Step 4: Draft the release notes

The GitHub release notes are user-facing and live forever. They are not the same as the changelog: they are usually richer, with code examples for breaking changes, more narrative, and explicit upgrade guidance. The changelog is the curated index; release notes are the prose version. This step is identical regardless of ecosystem.

Pull the changelog entries for this version as the starting point, then expand them. Structure release notes like this when the release has substance:

```markdown
[1-2 sentence framing of what this release is. State the headline:
"first release that intentionally breaks the public API", "weekly maintenance
release with three small fixes", "introduces feature X", etc.]

## ⚠️ Breaking changes

[Only include this section if there are breaking changes. Number each one,
explain the collision/motivation, and show before/after code. Be explicit
about who is affected and what they have to do.]

### 1. <name of breaking change> (#PR)

<one-paragraph explanation of why this changed and what broke>

```python
# Before
old_api()

# After
new_api()
```

<who is affected; who is unaffected; migration path>

## Features

- **<bold lead>** (#PR): one-paragraph description focused on what users get,
  not how it's implemented. If the feature has multiple facets, use a sub-list.

## Fixes

- One-sentence description of the fix and who it affects.

## Documentation

- Brief notes on user-facing doc changes worth surfacing.

## Upgrade notes

- Practical guidance: who can upgrade transparently (`pip install -U` /
  `npm install <pkg>@latest`), who needs to pin, what to migrate first.
```

Section selection is judgment-based, drop sections that don't apply. A patch release with three bug fixes doesn't need "Breaking changes" or "Upgrade notes". A release that's pure refactor with no user-visible effects probably shouldn't be cut at all.

**Tone and style guidance** (drawn from idfkit's release notes, which set the bar):

- **Lead with a one- or two-sentence framing** that tells the reader what kind of release this is. Don't dive straight into bullets.
- **For breaking changes, show before/after code blocks.** Not just prose. The reader is upgrading and wants to grep for the syntax they need to change. Use the project's actual language (Python or JS/TS) in the code fences.
- **Explain the why for breaking changes** in one paragraph. "The named-bag parameter on `doc.add()` collided with `Schedule:Day:Interval`, whose canonical wrapper key is literally `data`" is the kind of motivation that makes the change feel justified rather than capricious.
- **Bold the feature lead** in the Features section: `**\`idfkit tmy --nearby\`** (#134): auto-detect coordinates...`. PR number in parentheses right after.
- **Be specific about who is affected and who isn't.** "Callers passing `data=` positionally are unaffected, only the keyword name changed." This saves users from defensive rewrites.
- **Upgrade notes are not boilerplate.** Tell people which path is transparent and which paths require code edits, with version-pin guidance for those who need time.

Reference PRs by number (`#134`), `gh` will hyperlink them automatically in the release page. Pull PR numbers from the merge commits in `git log`.

Save the draft to a temp file (e.g. `/tmp/release-notes-vX.Y.Z.md`) and show it to the user for review before Step 5. The user almost always wants to tweak the framing sentence or the section ordering.

### Step 5: Confirm the tag and create the release

Before running `gh release create`, **confirm the exact tag string with the user**. Most projects use `vX.Y.Z` (with the `v` prefix). Some use bare `X.Y.Z`. Look at existing tags to match the convention:

```bash
git tag --sort=-creatordate | head -5
```

Show the user the proposed tag and the first ~10 lines of the release notes, then ask for explicit confirmation. Wait for an affirmative response before proceeding.

Commit and push the version bump and changelog updates first. Stage the files that Step 2 actually touched:

- **Python:** `pyproject.toml uv.lock CHANGELOG.md` (or the equivalent lock file for Poetry/Hatch/etc.)
- **Node.js:** `package.json package-lock.json CHANGELOG.md` (or `yarn.lock` / `pnpm-lock.yaml`, whichever this project uses)

```bash
git add <manifest and lockfile from Step 2> CHANGELOG.md   # omit CHANGELOG.md if the project has none
git commit -m "Release vX.Y.Z"
git push
```

Then create the release. `gh release create` tags, pushes the tag, and publishes the release in one go. Pass `--target` so a new tag points at the release commit; without it, `gh` tags the tip of the default branch:

```bash
gh release create vX.Y.Z --target "$(git rev-parse HEAD)" --title "vX.Y.Z" --notes-file /tmp/release-notes-vX.Y.Z.md
```

If the project uses GitHub Actions to publish the package on tag push or on release, look for a workflow with a `release: types: [published]` trigger, and a `twine upload`, `uv publish`, or `npm publish` step, mention this to the user so they know the package will appear on the registry (PyPI or npm) shortly. Don't try to publish manually unless asked; trusted/OIDC publishing via GitHub Actions is the modern default for both PyPI and npm, and bypassing it is a footgun.

### Step 6: Verify

After `gh release create` returns, verify:

```bash
gh release view vX.Y.Z         # release page renders correctly
git fetch --tags && git tag | grep vX.Y.Z   # tag exists locally and remotely
```

If the project publishes to a registry on tag, watch the workflow:

```bash
gh run list --workflow=publish.yml --limit 1   # adjust the workflow filename to match the repo
gh run watch
```

Report back to the user with the release URL and (if applicable) the registry publish status (PyPI or npm).

## Common pitfalls

- **Forgetting the version bump.** This is the #1 reason this skill exists. `uv version --bump` (Python) or `npm version` (Node) is non-negotiable. If the manifest file still has the old version when you create the release, the tag will point at a commit that claims to be the previous version, which breaks version resolution (`pip install <pkg>==X.Y.Z` or `npm install <pkg>@X.Y.Z`) and confuses downstream tooling.
- **Letting `npm version` create its own commit/tag.** Without `--no-git-tag-version`, `npm version` commits and tags immediately, before the changelog is updated, which produces a messy history and can conflict with Step 5's commit. Always pass the flag.
- **Stale `[Unreleased]` entries.** If the `[Unreleased]` section has entries that should have been part of an earlier release, don't silently roll them into the current one without flagging it, ask the user.
- **Hand-writing release notes from scratch.** The changelog already did the curation work. Start from there, then expand with code examples and framing. Don't re-derive the change list from `git log`.
- **Using the wrong tag prefix.** A project that uses `v1.2.3` and suddenly gets a `1.2.4` tag will break tooling that assumes the prefix.
- **Skipping the user confirmation before `gh release create`.** This step publishes a public, hard-to-undo artifact. Always confirm.

## What to skip

If the user is doing a quick patch release and explicitly says "just bump and tag, don't bother with full notes", respect that. Run Steps 1, 2, 5, 6 and use the changelog entry as the release notes verbatim. The skill's defaults are tuned for substantive releases; trivial ones don't need the full ceremony.
