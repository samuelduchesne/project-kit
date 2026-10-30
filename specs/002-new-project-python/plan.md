# Implementation Plan: new-project for Python

**Branch**: `002-new-project-python` | **Date**: 2026-10-30 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-new-project-python/spec.md`

## Summary

Replace the `new-project` placeholder with a working workflow. A stdlib-only script, `plugins/project-kit/scripts/new_project.py`, does the predictable steps: check the environment, read the template's questions from its `cookiecutter.json`, validate answers, preview by rendering into a temporary folder (which runs the template's own checks), and create the project with `cruft create`, spec-kit v1.2.5 and an initial git commit. The skill tells Claude how to interview the user, show the preview, get confirmation, run the script and report. Tests use a local fixture template so CI doesn't need the private template. See [research.md](./research.md).

## Technical Context

**Language/Version**: Python ≥ 3.9 (stdlib only) for the script, run via `uv run --no-project`; Markdown for the skill

**Primary Dependencies**: git; uv/uvx; cruft 2.16 (via `uvx cruft`); spec-kit v1.2.5 (via `uvx --from git+https://github.com/github/spec-kit.git@v1.2.5 specify`)

**Storage**: N/A (files written only to the new project folder and temporary folders)

**Testing**: stdlib `unittest` with a fixture template (`tests/test_new_project.py`); existing plugin validation; manual conversation checks in [quickstart.md](./quickstart.md)

**Target Platform**: Claude Code and local Cowork on macOS/Linux with a shell; CI on `ubuntu-latest`

**Project Type**: Claude plugin skill + helper script

**Performance Goals**: preview under 15 s and creation under 30 s on a normal connection (template clone ~1 s, cruft ~3 s, spec-kit ~3 s)

**Constraints**: no copy of template questions or rules in the plugin; no writes outside `PARENT/<project_name>` and temp folders; no deletes; no change to git config; pinned spec-kit; no top-level `bin/`

**Scale/Scope**: 1 script (3 subcommands), 1 skill, 1 test module, CI job, version bump to 0.2.0

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Result |
|-----------|-------|--------|
| I. Templates are the source of truth | Files come only from `cruft create` and spec-kit; questions read from `cookiecutter.json` at run time; template rules enforced by the template's own hooks | Pass |
| II. Scripts for predictable steps | check/options/validate/create scripted with logged commands; Claude only interviews, maps plain language to values, explains; `create --dry-run` provided (the script creates files) | Pass |
| III. Show before changing | Preview + explicit confirmation before creation; refuses non-empty destination; never deletes; new folder only, so the user's existing work is untouched (clean-tree rule applies to modifying existing projects, not to creating a new folder) | Pass |
| IV. Works wherever installed | Skill checks for shell, git, uv and template access and explains what's missing; spec-kit and Claude Code pinned; no `bin/` | Pass |
| Scope | Python creation only; Node deferred; upgrade/audit stay placeholders | Pass |
| Development workflow | Changelog entry; plugin version 0.2.0; validation and new tests in CI | Pass |

Post-design re-check: the only new runtime surface is the script, which follows the contract in [contracts/new-project-cli.md](./contracts/new-project-cli.md). **Pass.**

## Project Structure

### Documentation (this feature)

```text
specs/002-new-project-python/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── new-project-cli.md
│   └── skill-conversation.md
├── checklists/requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
plugins/project-kit/
├── .claude-plugin/plugin.json      # version 0.1.0 → 0.2.0
├── scripts/
│   └── new_project.py              # check | options | create [--dry-run]
└── skills/
    ├── new-project/SKILL.md        # placeholder → working workflow
    ├── upgrade-project/SKILL.md    # unchanged
    └── audit-project/SKILL.md      # unchanged
tests/
└── test_new_project.py             # fixture-template tests (unittest)
.github/workflows/validate.yml      # + script-tests job (uv, unittest)
README.md, CHANGELOG.md             # status and changelog
```

**Structure Decision**: the script ships inside the plugin (`plugins/project-kit/scripts/`) because the installed skill must run it via `${CLAUDE_PLUGIN_ROOT}`; tests stay at the repository root so they are not installed.

## Complexity Tracking

No constitution violations to justify.
