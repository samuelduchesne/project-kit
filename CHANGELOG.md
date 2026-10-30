# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Plugin marketplace definition, so the repository can be added as `samuelduchesne/project-kit` in claude.ai, the Claude desktop app and Claude Code.
- The `project-kit` plugin in `plugins/project-kit/`.
- `new-project` creates Python projects from the cookiecutter-gi template: it interviews you using the template's own questions, previews the result, generates the project with cruft so it stays linked for upgrades, sets up spec-kit v1.2.5 and makes an initial git commit. Node projects are not supported yet.
- `scripts/new_project.py`, the helper `new-project` runs (`check`, `options`, `create --dry-run`).
- Placeholder skills `upgrade-project` and `audit-project`, which explain the planned workflows and change nothing.
- README with install and update steps for each surface.
- A validation workflow that runs `claude plugin validate --strict` on the marketplace and the plugin, checks manifest consistency, installs the plugin in a clean environment, and tests the `new-project` script against a fixture template.

[Unreleased]: https://github.com/samuelduchesne/project-kit/commits/main
