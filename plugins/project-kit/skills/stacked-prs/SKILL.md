---
name: stacked-prs
description: >
  Split uncommitted changes into separate stacked PRs, merge them sequentially,
  and optionally create a release. Use this skill whenever the user wants to
  organize uncommitted work into multiple PRs, says "split into PRs",
  "stacked PRs", "organize into separate PRs", "create PRs for each group",
  or invokes /project-kit:stacked-prs. Also trigger when the user has a large uncommitted
  diff and asks to commit/push it as separate logical changesets.
---

# Stacked PRs

Split uncommitted changes into logically grouped, sequentially-merged pull requests.

## When to use

The user has uncommitted changes spanning multiple concerns (e.g., a new module + exception refactor + API rename + default change) and wants each concern in its own PR, merged in dependency order.

## Prerequisites

Before Phase 1, check that `git` and `gh` are available and that `gh auth status` succeeds. If anything is missing, state what is missing and stop; do not begin splitting changes that cannot be pushed from this environment.

## Workflow

### Phase 1: Analyze and plan

1. Run `git diff --stat` and `git status` to understand the full changeset
2. Read the diffs to identify **logical groups** — look for:
   - New modules/files that are self-contained
   - Changes to shared interfaces (exceptions, base classes)
   - Parameter renames or API changes
   - Default value changes
   - Test/doc updates that go with each group
3. Determine the **dependency order** — which groups build on which
4. Present the breakdown to the user as a numbered list with:
   - Group name and one-line description
   - Which files belong to each group
   - The merge order and why
5. **Wait for user confirmation** before proceeding

### Phase 2: Create branches and PRs

Use task tracking to show progress throughout.

1. **Save the current state**: `git diff > /tmp/full-changes.patch` then `git stash -u`
2. For each group, in dependency order:
   a. Create a branch from the previous group's branch (or `main` for the first):
      ```
      git checkout -b feat/<group-name> <previous-branch-or-main>
      ```
   b. Apply only this group's changes. Since changes are interleaved across files,
      you typically need to edit files manually rather than cherry-picking whole files.
      For untracked files, restore them from the stash's untracked tree: `git show stash^3:<path>`
   c. Run the project's quality checks and tests. Fix any issues.
   d. Stage, commit (let pre-commit hooks run — re-stage and retry if they modify files), push
   e. Create the PR:
      - First group: `gh pr create --base main`
      - Subsequent groups: `gh pr create --base <previous-branch>`

### Phase 3: Monitor CI and merge

1. Check CI status: `gh pr checks <number> --watch`
   - If a PR fails CI, investigate and fix on the branch, push, re-check
2. Merge PRs **one at a time in order**. For each PR:
   a. **Retarget the next PR** to `main` before merging the current one — this
      prevents GitHub from auto-closing it when the current branch is deleted:
      `gh pr edit <next-number> --base main`
   b. Squash-merge the current PR: `gh pr merge <number> --squash --delete-branch`
   c. Fetch updated main: `git fetch origin main`
   d. Rebase the next branch onto main. The already-merged commits will conflict —
      use `git rebase --skip` to skip them (they're already on main via squash merge)
   e. Force-push: `git push --force-with-lease origin <branch>`
   f. Wait for CI on the rebased PR, then continue with the next one

### Phase 4: Release (optional)

After all PRs are merged, ask the user if they want a release. If yes:

1. Determine the version number (ask the user or infer from the changes — breaking changes = minor bump in 0.x, patch otherwise)
2. Create a GitHub release with `gh release create` including:
   - Breaking changes section with before/after code examples
   - Migration instructions (what users need to change)
   - New features section
   - New public API table if applicable

## Key lessons from experience

- **Interleaved changes are the hard part.** When the same function has changes belonging to different groups (e.g., a parameter rename AND a default value change), you need intermediate states that may not exist in the original diff. Plan for this — e.g., rename the parameter but keep the old default, then flip the default in the next PR.
- **Pre-commit hooks modify files.** If the commit fails because hooks reformatted code, re-stage the modified files and commit again (new commit, not amend).
- **Retarget before merging.** Before squash-merging PR N, retarget PR N+1 to `main` with `gh pr edit`. This is critical — `--delete-branch` removes the base branch, and GitHub auto-closes any PR whose base branch is deleted. A closed PR cannot be reopened if its base no longer exists, forcing you to create a replacement PR. Retargeting to `main` first prevents this entirely.
- **`git rebase --skip` is your friend.** After squash-merging PR N, the commits from PRs 1..N are already on main. When rebasing PR N+1, these commits will conflict — skip them.
- **Always verify before merging.** Run `make check && make test` (or equivalent) locally before pushing each branch, not just at the end.
- **Compact generated files.** If the changeset includes generated files (JSON, stubs), consider excluding them from pretty-formatting pre-commit hooks to keep diffs minimal.
