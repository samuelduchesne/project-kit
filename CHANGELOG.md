# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Plugin marketplace definition, so the repository can be added as `samuelduchesne/project-kit` in claude.ai, the Claude desktop app and Claude Code.
- The `project-kit` plugin (version 0.2.0) in `plugins/project-kit/`.
- Placeholder skills `new-project`, `upgrade-project` and `audit-project`, which explain the planned workflows and change nothing.
- `changelog-keeper` skill, which creates a `CHANGELOG.md` from git history or audits and fixes an existing one against Keep a Changelog 1.1.0.
- `create-release` skill, which cuts a Python or Node release: version bump, changelog update, release notes and GitHub release.
- `stacked-prs` skill, which splits uncommitted changes into stacked pull requests and merges them in dependency order.
- `diataxis` skill, which writes, places and reorganizes documentation using the Diátaxis framework.
- `editorial` skill, which holds the house writing style.
- `review-docs` skill and workflow, which review documentation against a scoped code diff. They require the Workflow tool in Claude Code.
- `editor` agent, which writes and revises prose to the `editorial` standard for `diataxis` and `review-docs`.
- README with install and update steps for each surface.
- A validation workflow that runs `claude plugin validate --strict` on the marketplace and the plugin, checks manifest consistency, and installs the plugin in a clean environment.

[Unreleased]: https://github.com/samuelduchesne/project-kit/commits/main
