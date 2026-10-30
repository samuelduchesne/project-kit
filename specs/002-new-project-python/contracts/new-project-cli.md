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
| `--expect-commit SHA` | no | stop if the generated project's template commit differs |
| `--dry-run` | no | render into a temporary folder, report, delete it |

Success (`--dry-run`):

```json
{"status": "ok", "dry_run": true, "project_dir": "/abs/PARENT/demo-proj", "commit": "<sha>",
 "answers": {…full context…}, "non_default": {"layout": "src"}, "derived": {"project_slug": "demo_proj"},
 "files": ["AGENTS.md", "Makefile", …], "steps": ["cruft create …", "specify init …", "git init -b main", "git commit …"]}
```

Success (real run): same fields with `"dry_run": false`, plus `"git_commit": "<sha>"`.

`failed` results add `"step"` (`cruft` | `commit-check` | `speckit` | `git`) and `"created": true|false`.

## Guarantees

- `check`, `options` and `create --dry-run` write only inside a temporary folder they remove.
- `create` writes only inside `PARENT/<project_name>`, and refuses (exit 4) if it exists and is not empty.
- No command deletes anything outside its own temporary folders.
- No command changes the user's git configuration.
