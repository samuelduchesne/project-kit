# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Plugin marketplace definition, so the repository can be added as `samuelduchesne/project-kit` in claude.ai, the Claude desktop app and Claude Code.
- The `project-kit` plugin (version 0.4.0) in `plugins/project-kit/`.
- `new-project` creates Python and Node (TypeScript) projects from the cookiecutter-gi templates: it interviews you using the template's own questions, previews the result, generates the project with cruft so it stays linked for upgrades, sets up spec-kit v1.2.5 and makes an initial git commit.
- `scripts/new_project.py`, the helper `new-project` runs (`check`, `options`, `create --dry-run`, with `--language python|node`).
- `upgrade-project` brings a project up to the latest template with cruft: it previews the exact diff on a copy of the project, applies it after confirmation, and reports conflicts for Claude to resolve with you. Unlinked projects are linked first, at the template version they were most likely generated from, with answers inferred from the project and checked against the template file by file.
- `audit-project` checks a project against the standards without changing it (git state, template link and version, drift from the template, ruff or Biome through pre-commit, the changelog, spec-kit) and names the fix for each finding.
- `scripts/upgrade_project.py` (`status`, `link`, `update`, with dry runs) and `scripts/audit_project.py`, the helpers these workflows run.
- `changelog-keeper` skill, which creates a `CHANGELOG.md` from git history or audits and fixes an existing one against Keep a Changelog 1.1.0.
- `create-release` skill, which cuts a Python or Node release: version bump, changelog update, release notes and GitHub release.
- `stacked-prs` skill, which splits uncommitted changes into stacked pull requests and merges them in dependency order.
- `diataxis` skill, which writes, places and reorganizes documentation using the Diátaxis framework.
- `editorial` skill, which holds the house writing style.
- `review-docs` skill and workflow, which review documentation against a scoped code diff. They require the Workflow tool in Claude Code.
- `editor` agent, which writes and revises prose to the `editorial` standard for `diataxis` and `review-docs`.
- README with install and update steps for each surface.
- A validation workflow that runs `claude plugin validate --strict` on the marketplace and the plugin, checks manifest consistency, installs the plugin in a clean environment, and tests the helper scripts against fixture templates.

[Unreleased]: https://github.com/samuelduchesne/project-kit/commits/main
