# Implementation Plan: new-project for Node

**Branch**: `004-new-project-node` | **Date**: 2026-10-30 | **Spec**: [spec.md](./spec.md)

## Summary

Add a `--language python|node` option to every `new_project.py` command. The language selects the template folder inside cookiecutter-gi (`""` for Python, `node` for Node): questions are read from `<folder>/cookiecutter.json`, and `cruft create` gets `--directory node`, so `.cruft.json` records `directory: node` and later `cruft update` uses it. The skill asks or infers the language, passes it to every command, and gives Node next steps. Tests add a `node/` sub-template to the fixture.

## Technical Context

Same as spec 002 (stdlib Python script, cruft 2.16.0, cookiecutter 2.7.1, spec-kit v1.2.5). No new tools: creating a Node project needs only git and uv.

## Constitution Check

| Principle | Check | Result |
|-----------|-------|--------|
| I. Templates are the source of truth | Node files come from `node/` in cookiecutter-gi via cruft; questions read at run time | Pass |
| II. Scripts for predictable steps | Language is one script option; `--dry-run` unchanged | Pass |
| III. Show before changing | Same preview and confirmation | Pass |
| IV. Works wherever installed | Same tool checks; missing Node template at a ref reported as an environment problem | Pass |

## Project Structure

```text
plugins/project-kit/scripts/new_project.py    # --language, TEMPLATE_DIRS, --directory
plugins/project-kit/skills/new-project/SKILL.md
tests/test_new_project.py                     # node/ fixture sub-template, Node tests
README.md, CHANGELOG.md, plugin.json (0.3.0 → 0.4.0, shared with specs 005–006)
```

## Research

- **R1 Directory option**: `cruft create --directory node` and `cruft link --directory node` both record `"directory": "node"`; `cruft update` reads it (verified in cruft 2.16.0 source: `update.py` builds the template path from `cruft_state["directory"]`).
- **R2 Missing folder**: an older ref without `node/cookiecutter.json` → exit 3 (`environment`) "The template has no Node template at <ref>".
- **R3 Language default**: `python`, so existing calls and tests are unchanged.
