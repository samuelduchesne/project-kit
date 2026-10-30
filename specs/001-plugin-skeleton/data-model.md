# Data Model: Marketplace and Plugin Skeleton

**Feature**: 001-plugin-skeleton | **Date**: 2026-10-30

The "data" in this feature is a small set of declarative files. Field-level contracts live in [contracts/](./contracts/).

## Entities

### Marketplace

File: `.claude-plugin/marketplace.json` (repository root).

| Field | Value | Rule |
|-------|-------|------|
| `name` | `project-kit` | Required; not a reserved name; users type it after `@` |
| `owner.name` | `Samuel Letellier-Duchesne` | Required |
| `owner.url` | `https://github.com/samuelduchesne` | Optional |
| `description` | one sentence | Required here because `--strict` fails without it |
| `plugins` | array with exactly one Plugin entry | Required (FR-002) |

### Plugin entry

Item of `marketplace.plugins`.

| Field | Value | Rule |
|-------|-------|------|
| `name` | `project-kit` | MUST equal Plugin `name` (FR-003) |
| `source` | `./plugins/project-kit` | Relative to repo root; starts with `./`; no `..` |
| `description` | one sentence | Shown in plugin listings |
| `version` | — | MUST NOT be set (version lives in the Plugin only) |

### Plugin

File: `plugins/project-kit/.claude-plugin/plugin.json`.

| Field | Value | Rule |
|-------|-------|------|
| `name` | `project-kit` | Required; kebab-case; namespaces skills |
| `version` | `0.1.0` | Pinned; equals the first release tag (FR-004) |
| `description` | one sentence | Warned if missing |
| `author` | `{ name, url }` | Warned if missing |
| `homepage`, `repository` | `https://github.com/samuelduchesne/project-kit` | `homepage` must parse as a URL |
| `license` | `MIT` | Matches repo LICENSE |
| `keywords` | e.g. `scaffolding`, `templates`, `cookiecutter`, `spec-kit` | Optional |

Relationships: one Marketplace → one Plugin entry → one Plugin → three Skills.

### Skill (stub)

File: `plugins/project-kit/skills/<name>/SKILL.md`, one per workflow.

| Name | Purpose stated in description |
|------|-------------------------------|
| `new-project` | Create a new Python or Node project from the cookiecutter-gi templates, with spec-kit, linting and a changelog set up |
| `upgrade-project` | Bring an existing project up to the latest cookiecutter-gi template, linking it first if needed |
| `audit-project` | Check a project against the standards and report drift without changing anything |

Fields: `name` (equals directory), `description` (starts with "Placeholder (not yet implemented):"). Body: purpose, status, and a no-action rule.

## State transitions

Skill status: `stub` → `implemented` (later specs). A transition replaces the skill's body in place under the same name; the name never changes (spec assumption). Plugin `version` increases with each release that changes behavior.

## Validation rules (summary)

- Entry `name` == Plugin `name` == `project-kit`.
- `source` directory exists and contains `.claude-plugin/plugin.json`.
- Nothing outside `plugins/project-kit/` is part of the Plugin.
- Plugin directory contains no `bin/`, `CLAUDE.md`, `hooks/`, `agents/`, `.mcp.json`.
- Both validator runs pass with `--strict`.
