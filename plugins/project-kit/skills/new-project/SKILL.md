---
name: new-project
description: "Create a new Python or Node (TypeScript) project from the cookiecutter-gi templates: interview the user for the template's answers, preview, then generate it with cruft (linked for later upgrades), set up spec-kit and make an initial git commit. Use when the user asks project-kit to start, scaffold, bootstrap or create a new repository, Python project, Node, TypeScript or JavaScript project or library."
---

# new-project

Create a new Python or Node project from [cookiecutter-gi](https://github.com/samuelduchesne/cookiecutter-gi): the Python template is at the repository root, the Node (TypeScript library) template in its `node/` folder. The template provides every project file (linting, formatting, changelog, agent instructions); this workflow adds only spec-kit and an initial git commit.

All predictable steps go through one script. Run it exactly like this (call it `NP` below):

```bash
uv run --no-project "${CLAUDE_PLUGIN_ROOT}/scripts/new_project.py" <command> --language <python|node> [options]
```

Pass the same `--language` to every command.

Each command prints one JSON object on stdout (`status` is `ok`, `invalid`, `environment`, `destination` or `failed`, with `messages` on failure). Read the JSON; don't show it raw to the user.

## Rules

- Never create anything before the user confirms the preview.
- Never delete the user's files or folders, including the project folder after a failure. Say what exists and let the user decide.
- Never edit generated files, install dependencies, create a remote repository or push.
- Relay errors from the template word for word, then ask for a corrected answer.
- Don't invent answers the user didn't give, except the template's own defaults that they accepted.

## Steps

### 1. Language

This workflow creates **Python** (`--language python`) and **Node** (`--language node`) projects. A request for Node, TypeScript, JavaScript or an npm package means `node`; Python, a package for PyPI or uv means `python`. If the request doesn't say, ask which one before running anything. For any other language, say project-kit supports only Python and Node templates, and stop.

### 2. Environment

Run `NP check`. If you cannot run shell commands at all (for example in a chat without a local environment), say this workflow needs Claude Code or Cowork on the user's computer, and stop.

If `status` is `environment`, tell the user each message (missing git or uv with the install hint, no access to `samuelduchesne/cookiecutter-gi`, or no Node template at that template version), and stop.

### 3. Questions

Run `NP options`. It returns the template's `questions` (name, type `text`/`bool`/`choice`, default, choices, prompt, choice labels), the derived names, and the template `commit`.

Ask the user, in one message:

- project name (this is also the folder name; Python: letters, digits and `-`; Node: it is also the npm package name, so lowercase letters, digits and `-`, starting with a letter)
- a one-line description
- author name, email and GitHub handle (suggest `git config user.name` / `user.email` if set)

Then show the other questions as one compact list, `prompt: default`, using the choice labels where they help, and ask whether to keep these defaults or change any. Map plain-language changes to the exact allowed values (for example "use mypy" → `type_checker: mypy`, "no Docker" → `dockerfile: false`, "publish to npm" → `publish_to_npm: true`); if a change is ambiguous, ask.

Ask where to create the project; default is the current folder (the project goes in `<parent>/<project_name>`).

### 4. Preview

Write the answers (only the questions the user set or changed, using exact names and JSON types; always include `author` and `email`) to a new temporary file outside any project, for example with `mktemp`. Text answers can't contain `{{`, `{%` or `{#`; if the user's description does, ask them to rephrase it. Run:

```bash
NP create --answers <file> --dest <parent> --dry-run
```

- `invalid`: relay the messages, ask for corrected answers, update the file and preview again.
- `destination`: the folder exists and isn't empty; ask for another name or parent.
- `environment`: relay the messages (a tool or the network failed) and stop; don't ask for new answers.
- `failed` with `step: cruft`: the template couldn't generate the project; relay the message. Nothing was created.
- `ok`: show the user the language, the destination (`project_dir`), the template version (`commit`, first 12 characters), the package name (`derived`, Python only), the answers that differ from the defaults (`non_default`), and the top-level `files`. Ask for confirmation.

### 5. Create

After the user confirms, run with the full `commit` value from the preview (all 40 characters, not the short form you showed):

```bash
NP create --answers <file> --dest <parent> --expect-commit <commit>
```

- `failed`: say which `step` failed and relay the messages. When `created` is `false` (steps `cruft` and `commit-check`), nothing was created; for `commit-check`, the template changed since the preview, so preview again. When `created` is `true` (steps `speckit` and `git`), the project folder at `project_dir` was kept and nothing was deleted.
- `ok`: report:
  - the project folder and the template version it is linked to
  - the main choices (from `non_default`)
  - next steps for Python:
    1. `cd <project_dir>` and `make install` to install dependencies and pre-commit hooks
    2. create a remote repository and push (for example `gh repo create`)
    3. start a first spec: `/speckit-constitution`, then `/speckit-specify`
  - next steps for Node (needs Node.js at the chosen version or newer):
    1. `cd <project_dir>`, `npm install -g pnpm` if pnpm is missing (it switches to the version pinned in `package.json`), then `make install` to install dependencies and pre-commit hooks
    2. commit the new `pnpm-lock.yaml` (CI installs with `--frozen-lockfile`)
    3. create a remote repository and push (for example `gh repo create`)
    4. start a first spec: `/speckit-constitution`, then `/speckit-specify`

Finally, delete the temporary answers file you created in step 4 (it is yours, not the user's).
