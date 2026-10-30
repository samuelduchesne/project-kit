# Contract: `upgrade_project.py` command line

Invocation: `uv run --no-project "${CLAUDE_PLUGIN_ROOT}/scripts/upgrade_project.py" <command> --project DIR [options]`

Exit codes and `status` values: 0 `ok`, 2 `invalid`, 3 `environment`, 5 `failed` (as in new-project), and 6 `project`. Code 6 has its own value so it never collides with new-project's 4 (`destination`); it means the project is not in a state the command accepts (not a git repository, dirty tree, already linked, not linked), with `messages`.

## Common options

`--project DIR` (default `.`), `--template URL_OR_PATH` (default: the link record's template, else cookiecutter-gi), `--ref BRANCH` (default: the link record's `checkout` if it is a branch, else the template's default branch).

## `status`

```json
{"status": "ok", "project_dir": "…", "git": {"repository": true, "clean": true, "first_commit_date": "2024-03-01T10:00:00+00:00"},
 "language": "node", "linked": true,
 "link": {"template": "…", "commit": "<sha>", "checkout": "main", "directory": "node"},
 "latest_commit": "<sha>", "behind": 3, "up_to_date": false,
 "new_questions": [{"name": "codecov", "type": "bool", "default": true, "prompt": "…"}]}
```

Unlinked: `"linked": false`, `"suggested_commit": {"commit": "<sha>", "date": "…"} | null`, `"latest_commit"`, and, when the language is known, `"questions_at"` (the suggested commit, else the latest), `"questions"` and `"derived"` at that commit.

## `link`

`--answers FILE --commit SHA [--language python|node] [--dry-run]`. Requires a clean git repository without `.cruft.json`.

```json
{"status": "ok", "dry_run": true, "commit": "<sha>", "language": "python",
 "match": {"same": ["Makefile", …], "differs": ["README.md"], "missing": ["CHANGELOG.md"]},
 "summary": {"same": 40, "differs": 3, "missing": 1}}
```

The real run returns the same plus `"cruft": {…written .cruft.json minus context…}`. It writes only `.cruft.json`.

## `update`

`[--answers FILE] [--dry-run] [--expect-commit SHA]`. Requires a clean, linked git repository. Without `--dry-run`, `--expect-commit` is required (exit 2 otherwise).

```json
{"status": "ok", "dry_run": true, "from_commit": "<sha>", "to_commit": "<sha>", "up_to_date": false,
 "files": [{"path": "Makefile", "change": "modified"}, {"path": "biome.json", "change": "added"}],
 "conflicts": ["README.md"], "rejects": ["pyproject.toml.rej"], "patch": "<git diff>"}
```

`--answers` maps question names to new values (validated against the latest questions). The real run requires `--expect-commit` to equal the latest commit (else exit 5, `step: commit-check`, nothing changed) and returns the same fields with `"dry_run": false`. It never commits.

## Guarantees

- `status` and every `--dry-run` leave the project unchanged (they work in temporary folders they remove).
- `link` writes only `.cruft.json`; `update` changes only what `cruft update` applies plus `.cruft.json`'s `checkout`.
- No command commits, pushes or deletes files outside its temporary folders.
