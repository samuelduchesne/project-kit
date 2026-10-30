# Data Model: new-project for Python

**Feature**: 002-new-project-python | **Date**: 2026-10-30

## Template definition (read from `cookiecutter.json`)

| Field | Source | Rule |
|-------|--------|------|
| `template` | default `https://github.com/samuelduchesne/cookiecutter-gi`, or `--template` | git URL or local path |
| `ref` | template default branch (`git ls-remote --symref`), or `--ref` | recorded as cruft `checkout` |
| `commit` | `git rev-parse HEAD` of the shallow clone | 40-char SHA |
| `questions[]` | each top-level key not starting with `_` and whose value is not a `{{…}}` string | see Question |
| `derived[]` | keys whose string value contains `{{` | not asked; values come from the rendered `.cruft.json` |

### Question

| Field | Rule |
|-------|------|
| `name` | the key, e.g. `layout` |
| `type` | `choice` if the value is a list; `bool` if boolean; `text` otherwise |
| `default` | first list item for `choice`; the value itself otherwise |
| `choices` | list values (`choice` only) |
| `prompt` | `__prompts__[name]` if a string, or `__prompts__[name].__prompt__`; else the name |
| `choice_labels` | `__prompts__[name][value]` per choice, when present |

## Answers (`answers.json`, written by Claude, read by the script)

A JSON object mapping question names to values. Validation (script):

- every key MUST be a question name (unknown keys are rejected, including derived keys);
- `choice` values MUST be one of `choices`;
- `bool` values MUST be JSON `true`/`false`;
- `text` values MUST be non-empty strings;
- `project_name` MUST be present.

Missing questions take the template default. Rules beyond these (name pattern, Python version order) are enforced by the template's hooks during the dry run.

## Project (result)

| Element | Produced by |
|---------|-------------|
| `<parent>/<project_name>/` with template files | cruft create |
| `.cruft.json` (`template`, `commit`, `checkout`, `context`) | cruft create |
| `.specify/`, `.claude/skills/speckit-*` | spec-kit v1.2.5 init |
| `.git/` on `main` with one commit of every file | git |

## Run states

```text
check ──fail──> stop (nothing created)
  │ok
options ──fail──> stop (nothing created)
  │ok
interview → answers.json
  │
create --dry-run ──invalid/template error──> ask again (nothing created)
  │ok → user confirms
create ──destination not empty──> stop (nothing created)
  │
  cruft create ──fail──> stop (report; folder may exist, not deleted)
  │
  commit check ──mismatch──> stop (report both commits; folder kept)
  │
  spec-kit init ──fail──> stop (report; folder kept)
  │
  git init + commit ──fail──> stop (report; folder kept)
  │
  done → report
```
