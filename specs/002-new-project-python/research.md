# Research: new-project for Python

**Feature**: 002-new-project-python | **Date**: 2026-10-30

All findings below were verified by running the tools in this environment (cruft 2.16.0, cookiecutter 2.7.1, spec-kit v1.2.5, git, uv 0.11) against the real `samuelduchesne/cookiecutter-gi` and a local fixture template.

## R1. Generator: cruft create

- **Decision**: generate with `uvx cruft create <template> --no-input --checkout <default-branch> --output-dir <parent> --extra-context-file <answers.json>`.
- **Rationale**: cruft writes `.cruft.json` with `template`, `commit`, `checkout` and the full answer context, which is what `cruft check`/`cruft update` (and the future `upgrade-project`) need (FR-007, SC-005). Passing `--checkout main` records the branch, so later updates follow `main`; passing a commit SHA would pin the project and make updates find nothing. Answers in a JSON file keep booleans as real booleans (`false` → Python `False`), which avoids the template's known failure with a lowercase `false` passed on the command line.
- **Alternatives considered**: plain `cookiecutter` (no link record); `--checkout <sha>` (pins forever); `key=value` CLI arguments (string booleans break the template's hooks).

## R2. Reading the template definition

- **Decision**: `git clone --depth 1 --branch <default-branch>` the template into a temporary folder, read `cookiecutter.json`, record `git rev-parse HEAD`, then delete the folder. Default branch from `git ls-remote --symref <template> HEAD`.
- **Rationale**: FR-002 forbids a copy of the questions in the plugin. `cookiecutter.json` holds every question: a list value is a choice (first item is the default), a boolean is yes/no, a string is free text, and a string containing `{{` is derived by the template (e.g. `project_slug`) and not asked. Keys starting with `_` are private. `__prompts__` gives the prompt text and, for choices, a label per value. The template's `pre_prompt` hook only rewrites author defaults from the OS user name; the workflow asks for author details anyway (FR-003).
- **Alternatives considered**: GitHub API (needs a token and is GitHub-specific); keeping a schema in the plugin (violates FR-002 and Principle I).

## R3. Validation: who checks what

- **Decision**: the script checks only what the definition itself says — answer keys exist, choice answers are among the listed values, yes/no answers are booleans, free text is a non-empty string. Everything else (project name pattern, package name pattern, development Python ≥ minimum) is left to the template's own `pre_gen_project` hook, which the preview runs.
- **Rationale**: Principle I and FR-004. Verified: an invalid name and an inverted Python-version pair both make `cruft create` exit 1 with a single `ERROR: …` line from the template, and leave the output folder empty. An invalid choice also exits 1 (cookiecutter's own `ValueError`), but the script catches it first with a clearer message.
- **Alternatives considered**: re-implementing the template's regexes and version rule in the plugin — duplicates and drifts.

## R4. Preview (dry run)

- **Decision**: `create --dry-run` runs the same `cruft create` into a new temporary folder, reads the rendered `.cruft.json` (commit, derived values such as `project_slug`), lists the generated files, prints the steps the real run would take, then deletes the temporary folder.
- **Rationale**: rendering is the only way to run the template's own checks and show derived names and files exactly (FR-004, FR-005, FR-006). Nothing is written outside the temporary folder (SC-004). Constitution II requires a dry-run for any script that creates files.
- **Alternatives considered**: a "plan only" preview without rendering — could not show template errors or derived names.

## R5. Same version in preview and creation

- **Decision**: the preview reports the commit; the real run takes `--expect-commit <sha>` and, after `cruft create`, compares it with `.cruft.json`'s `commit`. On mismatch it stops before spec-kit and git, reports both commits, and leaves the folder (FR-013).
- **Rationale**: keeps `checkout: main` for upgrades (R1) while still guaranteeing the user created what they previewed (edge case "template changes between preview and creation"). A mismatch needs a push to the template within seconds, so this is a safety net, not a common path.

## R6. spec-kit setup

- **Decision**: in the new project, `uvx --from git+https://github.com/github/spec-kit.git@v1.2.5 specify init --here --integration claude --script sh --non-interactive --force --ignore-agent-tools`.
- **Rationale**: same pinned version and flags used to set up this repository; `--force` is needed because the folder is not empty; `--non-interactive` never prompts; `--ignore-agent-tools` skips spec-kit's check that the `claude` CLI is on PATH, which fails in Cowork, the desktop app and CI even though the Claude integration files are still installed (found when CI failed without the CLI). Verified: exits 0 in about 3 seconds and adds `.specify/` and `.claude/skills/speckit-*`.
- **Alternatives considered**: unpinned `specify` (Principle IV requires pins); `--script ps` (Windows only; the workflow targets macOS/Linux shells, noted as an assumption).

## R7. Git

- **Decision**: `git init -b main`, `git add -A`, then `git -c user.name=<author> -c user.email=<email> commit -m "Initial commit from cookiecutter-gi <sha12>"`. The author comes from the template answers `author` and `email` when present, otherwise from the user's git config; if neither exists, the pre-check reports it.
- **Rationale**: FR-009 and the edge case where git has no identity configured; `-c` changes nothing in the user's git configuration. A new repository in its own folder never touches an enclosing repository.

## R8. Running the script

- **Decision**: one stdlib-only Python script, `plugins/project-kit/scripts/new_project.py`, run as `uv run --no-project "${CLAUDE_PLUGIN_ROOT}/scripts/new_project.py" <command>`. Subcommands: `check`, `options`, `create [--dry-run]`. Machine-readable JSON on stdout, progress on stderr, distinct exit codes.
- **Rationale**: uv is already required, so `uv run --no-project` guarantees a Python without needing one on PATH; `${CLAUDE_PLUGIN_ROOT}` is substituted in skill content. Principle II: predictable steps are scripted, Claude only interviews and explains. The plugin must not use a top-level `bin/` (claude.ai/Cowork refuse it), so the script lives in `scripts/`.

## R9. Testing without the private template

- **Decision**: unit and integration tests in `tests/test_new_project.py` (stdlib `unittest`) build a small fixture template in a temporary git repository and run the script against it with `--template <path>`, covering options parsing, validation errors, dry run (no files left), refusal of a non-empty destination, and a full create (cruft link record, spec-kit files, one commit). CI runs them with uv installed.
- **Rationale**: CI's token cannot read the private template; a local fixture exercises the same code paths. spec-kit is fetched from public GitHub, so the full create runs in CI.

## R10. Environments without a shell

- **Decision**: the skill tells Claude to stop and explain when it cannot run shell commands, or when `check` reports missing tools: the workflow needs Claude Code or Cowork on the user's computer with git and uv.
- **Rationale**: Principle IV ("check for those tools and say clearly what is missing instead of failing partway").
