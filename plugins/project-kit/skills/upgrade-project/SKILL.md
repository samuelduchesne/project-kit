---
name: upgrade-project
description: "Bring an existing Python or Node project up to the latest cookiecutter-gi template with cruft: show how far behind it is, preview the exact diff, apply it after confirmation and help resolve conflicts. Projects that were never linked to the template are linked first, at the template commit they were most likely generated from, with answers inferred from the project. Use when the user asks project-kit to upgrade, update, re-sync or link a repository with its template."
---

# upgrade-project

Update a project generated from [cookiecutter-gi](https://github.com/samuelduchesne/cookiecutter-gi) (Python template at the repository root, Node template in `node/`) to the template's latest version. cruft computes the template's changes since the project's recorded commit and applies them as a three-way merge, so local edits are kept unless they touch the same lines.

All predictable steps go through one script. Run it exactly like this (call it `UP` below), from any folder:

```bash
uv run --no-project "${CLAUDE_PLUGIN_ROOT}/scripts/upgrade_project.py" <command> --project <project folder> [options]
```

Each command prints one JSON object (`status` is `ok`, `invalid`, `environment`, `project` or `failed`, with `messages` on failure). Read the JSON; don't show it raw.

## Rules

- Change nothing before the user confirms a preview. `status` and every `--dry-run` change nothing.
- Never commit, push, stash, reset or delete on the user's behalf without asking. Never discard their changes.
- Relay the template's error messages word for word.
- The project must be a clean git repository: if `status` is `project` because of uncommitted changes, ask the user to commit or stash them themselves, then start again.

## Steps

### 1. Status

If you cannot run shell commands, say this workflow needs Claude Code or Cowork on the user's computer, with git and uv, and stop.

Run `UP status`. On `environment`, relay the messages (missing tool, template unreachable, or linked to a template other than cookiecutter-gi) and stop. Otherwise tell the user: the language, whether the project is linked, and the git state. If `git.repository` is false, say upgrades need a git repository and stop. If `git.clean` is false, ask them to commit or stash first.

- `linked: true` → go to step 3.
- `linked: false` → step 2.

### 2. Link an unlinked project

The project must be linked before it can be updated. Explain this in a sentence, then:

1. **Base commit.** `suggested_commit` is the template's last commit before the project's first commit: the version it was most likely generated from. Show its date. Offer it, or the latest commit (`latest_commit`) if the user knows the project was set up recently or rewritten by hand. With the latest commit there will be nothing to update; the link only records the answers, and the drift stays for the user to adopt by hand. If `suggested_commit` is null, the project is older than the template: use the latest commit.
2. **Answers.** Infer an answer for every question in `questions` (they are the template's questions at `questions_at`) by reading the project: `project_name` from the folder or package name, `project_description`, author and email from `pyproject.toml` or `package.json` (or `git log`), license from `LICENSE`, layout from `src/`, Python or Node versions from `.python-version`/`.nvmrc` and CI, yes/no options from which files exist (`Dockerfile`, `mkdocs.yml`, `.devcontainer/`, `CHANGELOG.md`, publish workflows, agent files). Use the template default only when nothing in the project says otherwise, and say which answers are guesses.
3. **Compare.** Write the answers to a new temporary file outside the project (with `mktemp`) and run `UP link --dry-run --commit <sha> --answers <file>` (add `--language` if `language` was null). `match` lists the template's files that are `same`, `differs` or `missing` in the project. Many `differs` usually mean a wrong answer: look at those files, adjust the answers and compare again. Some differences are the project's own edits; that is expected. On `invalid`, relay the messages and fix the answers.
4. **Confirm and link.** Show the base commit, the answers and the match summary, and ask to link. Then run `UP link --commit <sha> --answers <file>`. It writes only `.cruft.json`. Offer to commit it (`git add .cruft.json && git commit -m "Link to cookiecutter-gi <sha12>"`); the update needs a clean tree, so if the user declines, stop here.

### 3. Preview the update

If `up_to_date` is true, say the project is up to date and stop.

Otherwise report `behind` (template commits that changed this project's template since its commit). If `new_questions` is not empty, these are options the template added since: show each with its prompt and default and ask for the user's answers (keeping the defaults is fine). Write the answers to a temporary file and pass `--answers <file>` to both the preview and the update. The user can also change an existing answer this way (for example a new license).

Run `UP update --dry-run [--answers <file>]`. Show:

- the template versions (`from_commit` → `to_commit`, 12 characters)
- the files and how each changes (`files`)
- files that will conflict with local edits (`conflicts`, `rejects`)
- the diff (`patch`): summarize it per file; show the full hunks for anything non-trivial or when asked

Ask for confirmation.

### 4. Apply

Run `UP update --expect-commit <to_commit> [--answers <file>]` with the full 40-character `to_commit` from the preview.

- `failed` with `step: commit-check`: the template changed since the preview; preview again.
- `failed` with `step: cruft`: relay the messages; `changed` says whether the project was modified. Show `git status` and let the user decide.
- `ok`: report the changed files. For each conflict:
  - files in `conflicts` have `<<<<<<< ours` / `=======` / `>>>>>>> theirs` markers (ours is the project, theirs the template). Propose a resolution per conflict, apply it when the user agrees, and `git add` the file.
  - files in `rejects` (`*.rej`) hold hunks that could not be applied. Propose how to apply each to its file; delete the `.rej` file only after the user accepts.

### 5. Finish

When no conflict is left, suggest the user review with `git diff` and run the project's checks (`make check` and `make test`). Offer to commit everything the update changed (`git add -A`, then `git commit -m "Update to cookiecutter-gi <sha12>"`); commit only if they agree. Never push.

Delete the temporary answers files you created.
