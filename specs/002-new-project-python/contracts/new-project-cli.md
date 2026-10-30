# Contract: `new_project.py` command line

Invocation (from the skill): `uv run --no-project "${CLAUDE_PLUGIN_ROOT}/scripts/new_project.py" <command> [options]`

All commands print one JSON object on stdout; human-readable progress goes to stderr.

## Common options

| Option | Default | Meaning |
|--------|---------|---------|
| `--template URL_OR_PATH` | `https://github.com/samuelduchesne/cookiecutter-gi` | template location |
| `--ref REF` | template's default branch | branch or tag to use |

## Exit codes

| Code | Meaning | stdout `status` |
|------|---------|-----------------|
| 0 | success | `ok` |
| 2 | invalid answers, or the template rejected them | `invalid` |
| 3 | environment problem (missing tool, template unreachable, no git identity) | `environment` |
| 4 | destination exists and is not empty | `destination` |
| 5 | a step failed after the project folder was created | `failed` |

Every non-zero result includes `"messages": [str, …]`.

## `check`

Checks `git`, `uv`/`uvx` on PATH and that the template is reachable.

```json
{"status": "ok", "template": "…", "ref": "main", "commit": "<sha>", "tools": {"git": "git version …", "uvx": "uv …"}}
```

## `options`

```json
{
  "status": "ok", "template": "…", "ref": "main", "commit": "<sha>",
  "questions": [
    {"name": "layout", "type": "choice", "default": "flat", "choices": ["flat", "src"],
     "prompt": "Project layout", "choice_labels": {"flat": "Flat - …", "src": "src/ - …"}},
    {"name": "mkdocs", "type": "bool", "default": true, "prompt": "Include MkDocs? …"},
    {"name": "project_name", "type": "text", "default": "example-project", "prompt": "project_name"}
  ],
  "derived": ["project_slug"]
}
```

## `create`

| Option | Required | Meaning |
|--------|----------|---------|
| `--answers FILE` | yes | answers JSON (see data-model.md) |
| `--dest PARENT` | no (default `.`) | parent folder; the project goes in `PARENT/<project_name>` |
| `--expect-commit SHA` | no | the full commit from the preview (a prefix of at least 7 characters is accepted); stop before writing anything if the template's commit differs |
| `--dry-run` | no | render into a temporary folder, report, delete it |

Success (`--dry-run`):

```json
{"status": "ok", "dry_run": true, "project_dir": "/abs/PARENT/demo-proj", "commit": "<sha>",
 "answers": {…full context…}, "non_default": {"layout": "src"}, "derived": {"project_slug": "demo_proj"},
 "files": ["AGENTS.md", "Makefile", …], "steps": ["cruft create …", "specify init …", "git init -b main", "git commit …"]}
```

Success (real run): same fields with `"dry_run": false`, plus `"git_commit": "<sha>"`.

`failed` results add `"step"` (`cruft` | `commit-check` | `speckit` | `git` | `internal`) and `"created": true|false`. `cruft` and `commit-check` failures always have `created: false`: the project is rendered in a staging folder and moved into place only when complete.

## Guarantees

- `check`, `options` and `create --dry-run` write only inside a temporary folder they remove.
- `create` writes only inside `PARENT/<project_name>`, plus a hidden staging folder `PARENT/.project-kit-*` that it removes before finishing; it refuses (exit 4) if the target exists and is not an empty folder, or is a symlink.
- `project_name` must be a single folder name (no `/`, `\`, leading `.` or `-`); text answers must not contain `{{`, `{%` or `{#`; `--template` and `--ref` must not start with `-` (exit 2).
- Cookiecutter's clone cache and replay files go to a temporary folder, not the user's home.
- Child processes run without a terminal (`GIT_TERMINAL_PROMPT=0`, no stdin) and with a 10-minute timeout.
- The initial commit uses the `author`/`email` answers for both author and committer, ignores `GIT_AUTHOR_*`/`GIT_COMMITTER_*`, skips the user's git hooks (`--no-verify`) and is not signed (`commit.gpgsign=false`).
- No command deletes anything outside its own temporary folders.
- No command changes the user's git configuration.
- Every outcome, including unexpected errors, prints one JSON object (`step: internal` for bugs).
