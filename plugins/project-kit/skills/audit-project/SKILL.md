---
name: audit-project
description: "Check a Python or Node project against the cookiecutter-gi standards and report drift without changing anything: template link and version, files that differ from the template, ruff or Biome through pre-commit, the Keep a Changelog CHANGELOG.md and spec-kit. Each finding names its fix. Use when the user asks project-kit to audit, check or review a repository against the standards, or asks whether a project is up to date with its template."
---

# audit-project

Report how a project measures up to the [cookiecutter-gi](https://github.com/samuelduchesne/cookiecutter-gi) standards. The audit is read-only: it never changes the project, and fixing a finding is a separate request.

Run the audit script exactly like this, from any folder:

```bash
uv run --no-project "${CLAUDE_PLUGIN_ROOT}/scripts/audit_project.py" --project <project folder>
```

Add `--offline` only if the user asks for a quick audit without the template checks. If you cannot run shell commands, say this workflow needs Claude Code or Cowork on the user's computer, with git and uv, and stop.

## Reading the result

The script prints one JSON object. `status: environment` means the folder doesn't exist; say so and stop. Otherwise:

- `summary` counts findings by severity; `findings` are sorted errors first. Each has an `id`, `message` and `fix`.
- `skipped` lists checks that could not run, with the reason (for example `not linked`, `offline`, or the template could not be reached). A skipped check has not passed: say so.
- `passed` lists the checks that passed.
- `template` gives the recorded and latest template commits and `behind`.

## Report

Lead with a one-line verdict (for example "2 warnings, no errors"), then group the findings by severity. For each, say what it means for this project in plain words and the fix. Map fixes to the workflows that do them:

| Finding | Fix |
|---------|-----|
| `not-linked`, `template-behind`, `pre-commit-missing`, `linter-missing` | `/project-kit:upgrade-project` (links the project if needed, then previews and applies the template's changes) |
| `changelog-missing`, `changelog-format` | `/project-kit:changelog-keeper` |
| `speckit-missing`, `speckit-outdated` | the `specify` command in the finding |
| `git-dirty` | commit or stash before upgrading |
| `template-drift` | information only: list the files; local edits are often intended, and upgrade-project merges template changes around them |
| `template-foreign`, `language-unknown` | nothing to fix if intended; explain that the template checks or the linter check don't apply |

Then list what passed in one line, and the skipped checks with their reasons.

Don't fix anything as part of the audit. Offer the relevant workflow and let the user choose.
