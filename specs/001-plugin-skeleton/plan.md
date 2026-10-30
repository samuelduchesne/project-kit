# Implementation Plan: Marketplace and Plugin Skeleton

**Branch**: `001-plugin-skeleton` | **Date**: 2026-10-30 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-plugin-skeleton/spec.md`

## Summary

Make `samuelduchesne/project-kit` a Claude plugin marketplace that lists one plugin, `project-kit`, kept in `plugins/project-kit/` so only that folder is ever installed. The plugin ships three placeholder skills (`new-project`, `upgrade-project`, `audit-project`) that explain their purpose and do nothing else. The repository gets a README with install steps for claude.ai and Claude Code, a Keep a Changelog file, and a GitHub Actions check that runs the official validator in strict mode, a small consistency script, and an install smoke test. See [research.md](./research.md).

## Technical Context

**Language/Version**: JSON manifests and Markdown skills; Python 3 (stdlib only) for the consistency script; YAML for the workflow

**Primary Dependencies**: Claude Code CLI `2.1.314` (`claude plugin validate`, `claude plugin marketplace add`, `claude plugin install`), installed from npm in CI

**Storage**: N/A (files in the repository)

**Testing**: `claude plugin validate --strict` on the marketplace and on the plugin; `.github/scripts/check_manifests.py`; install smoke test into a temporary `HOME`; manual checks in [quickstart.md](./quickstart.md)

**Target Platform**: Claude plugin surfaces — claude.ai chat, Claude desktop app, Cowork, Claude Code; CI on GitHub Actions `ubuntu-latest`

**Project Type**: Plugin marketplace (declarative package)

**Performance Goals**: CI check finishes in under 3 minutes

**Constraints**: Only `plugins/project-kit/` is packaged; no `bin/`, `CLAUDE.md`, hooks, agents or connectors in the plugin; no secrets needed in CI; tool versions pinned

**Scale/Scope**: 1 marketplace, 1 plugin, 3 stub skills, 1 CI workflow

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Result |
|-----------|-------|--------|
| I. Templates are the source of truth | Stubs generate nothing; no template files are copied into the plugin | Pass |
| II. Scripts for predictable steps, model for judgment | Validation, consistency checks and install test are scripted; no model judgment is needed in this feature | Pass |
| III. Show before changing | Stubs MUST NOT run commands or change files (FR-006); nothing here modifies user projects | Pass |
| IV. Works wherever it is installed | Skills only (no hooks/agents); no `bin/` (claude.ai/Cowork refuse it); stubs need no shell; Claude Code pinned to `2.1.314` in CI | Pass |
| Scope and constraints | Spec-kit files stay at root, plugin under `plugins/project-kit/`; MIT | Pass |
| Development workflow | Changelog entry under `[Unreleased]`; `claude plugin validate` gates merges; `plugin.json` version `0.1.0` will equal the first tag | Pass |

Post-design re-check (after Phase 1): no new components, dependencies or exceptions introduced. **Pass.**

## Project Structure

### Documentation (this feature)

```text
specs/001-plugin-skeleton/
├── plan.md              # This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1
├── contracts/
│   ├── install-interface.md
│   └── manifests.md
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 (/speckit-tasks)
```

### Source Code (repository root)

```text
.claude-plugin/
└── marketplace.json            # marketplace definition (repo root)
plugins/
└── project-kit/                # the only packaged folder
    ├── .claude-plugin/
    │   └── plugin.json
    └── skills/
        ├── new-project/SKILL.md
        ├── upgrade-project/SKILL.md
        └── audit-project/SKILL.md
.github/
├── scripts/
│   └── check_manifests.py      # name/source/forbidden-file checks
└── workflows/
    └── validate.yml            # validate x2, consistency script, install smoke test
README.md
CHANGELOG.md
LICENSE                         # existing
.specify/, .claude/skills/speckit-*, specs/   # spec-kit development files, not packaged
```

**Structure Decision**: Single marketplace repository with the plugin in a subfolder (`plugins/project-kit/`), as required by the constitution's scope section. Repository tooling (CI, scripts, specs, spec-kit) lives outside that folder so the install copies only the plugin (research R2).

## Complexity Tracking

No constitution violations to justify.
