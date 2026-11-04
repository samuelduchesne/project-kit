# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.2] - 2026-11-04

### Changed

- The project constitution is amended to version 1.2.0: the repository is a marketplace of plugins, each under `plugins/<name>/`; it defines the scope of `sci-review`, states that Principle I does not apply to it, and introduces per-plugin release tags of the form `sci-review-vX.Y.Z`.
- The validation workflow now also validates `sci-review`, checks that its workflow script is up to date with its skill files, and installs it in a clean environment.

## [sci-review-v0.1.0] - 2026-11-04

First release of the `sci-review` plugin, tagged separately from `project-kit` as the constitution requires.

### Added

- The `sci-review` plugin 0.1.0 in `plugins/sci-review/`, which reviews code for scientific correctness with a panel of independent reviewers. It covers five dimensions (mathematical derivations, numerical stability, physical modelling and units, statistical integrity, algorithmic correctness) and reports only findings with a concrete failure scenario. The review never modifies the reviewed project.
- The `scientific-review` skill, `scientific-auditor` agent and `scientific-review` workflow of `sci-review`. Five default perspectives (theorist, numerical analyst, experimentalist, methodologist, computer scientist), a defender and a moderator review independently, debate each finding, and receive an agreement label of consensus, majority or contested that `scripts/panel.py` computes from the recorded positions. `scripts/build_workflow.py` regenerates the workflow script, which embeds the protocol, role briefs, dimension documents and message schemas.
- Four `sci-review` runners, selected by host: the Claude Workflow, Codex subagents, Claude agents, and a sequential runner for claude.ai chat, Cowork and Codex without agents.
- The `sci-review` domain-extension contract, version 1 (`plugins/sci-review/skills/scientific-review/extensions.md`), through which any plugin can add a domain perspective. The first extension, `building-energy-sci-review-extension`, ships in the idfkit plugin and is released separately.
- A Codex manifest for `sci-review` and a Codex marketplace at `.agents/plugins/marketplace.json`, so that `sci-review` installs in Codex from `samuelduchesne/project-kit`.

## [0.5.1] - 2026-11-02

### Fixed

- `new-project` now tells you to commit `uv.lock` before pushing a Python project, because CI fails without it.

## [0.5.0] - 2026-11-02

### Changed

- `new-project`, `upgrade-project` and `audit-project` now use the public [project-kit-cookiecutter](https://github.com/samuelduchesne/project-kit-cookiecutter) template by default, so they no longer need access to a private repository.
- Projects linked to the retired `cookiecutter-gi` template are told to remove `.cruft.json` and link again, because its commits are not in the public template. Pass `--template` to keep using another template.

## [0.4.0] - 2026-10-30

### Added

- Plugin marketplace definition, so the repository can be added as `samuelduchesne/project-kit` in claude.ai, the Claude desktop app and Claude Code.
- The `project-kit` plugin in `plugins/project-kit/`.
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

[Unreleased]: https://github.com/samuelduchesne/project-kit/compare/v0.5.2...HEAD
[0.5.2]: https://github.com/samuelduchesne/project-kit/compare/v0.5.1...v0.5.2
[sci-review-v0.1.0]: https://github.com/samuelduchesne/project-kit/releases/tag/sci-review-v0.1.0
[0.5.1]: https://github.com/samuelduchesne/project-kit/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/samuelduchesne/project-kit/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/samuelduchesne/project-kit/releases/tag/v0.4.0
