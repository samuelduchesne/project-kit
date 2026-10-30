# Implementation Plan: Node template in cookiecutter-gi

**Branch**: `003-node-template` | **Date**: 2026-10-30 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-node-template/spec.md`

## Summary

Add a second cookiecutter template to `samuelduchesne/cookiecutter-gi` under `node/`, generated with `--directory node`. It produces a pnpm TypeScript ES-module library: `tsc` build to `dist/` with declarations, Vitest with V8 coverage, Biome for lint and format (run directly and as a local pre-commit hook), the same generic pre-commit hooks, Keep a Changelog, agent files, GitHub Actions (checks, a test matrix, optional npm trusted publishing), a devcontainer and a license. Hooks validate inputs and prune files exactly like the Python template's. See [research.md](./research.md).

## Technical Context

**Language/Version**: Jinja2 templates; Python ≥ 3.9 hooks; generated projects: TypeScript 7.0, Node 22/24/26 (default 24)

**Primary Dependencies**: cookiecutter 2.7 (template), pnpm 12.16.1 (`packageManager`, installed with `npm install -g pnpm`), Biome 2.6.4, TypeScript 7.0.2, Vitest 5.0.5 with `@vitest/coverage-v8`, `@types/node` matching the Node major, pre-commit 4.7.0 via `uvx`, pre-commit-hooks v6.0.0

**Testing**: pytest + pytest-cookies in cookiecutter-gi (`tests/test_node_template.py`); a CI job that bakes the Node template and runs `pnpm install`, `make check`, `pnpm test`, `pnpm build`

**Target Platform**: macOS/Linux developer machines, GitHub Actions `ubuntu-latest`

**Project Type**: cookiecutter template

**Constraints**: the Python template and its tests unchanged; every tool version pinned; generated files end with one newline and pass Biome and pre-commit unchanged

## Constitution Check

| Principle | Check | Result |
|-----------|-------|--------|
| I. Templates are the source of truth | The Node standard lives in the template; project-kit gets no copy | Pass |
| II. Scripts for predictable steps | Input checks and pruning in template hooks, tested | Pass |
| III. Show before changing | N/A to the template itself; generation writes only a new folder | Pass |
| IV. Works wherever installed | Tool versions pinned (pnpm via `packageManager`, Biome/TS/Vitest exact, pre-commit pinned in `uvx`) | Pass |
| Scope | Node projects, Biome, pre-commit, Keep a Changelog are in scope | Pass |

## Project Structure

```text
cookiecutter-gi/
├── node/
│   ├── cookiecutter.json
│   ├── local_extensions.py          # identical copy of the root one (cookiecutter imports it from the template dir)
│   ├── hooks/{pre,post}_gen_project.py
│   └── {{cookiecutter.project_name}}/
│       ├── package.json, tsconfig.json, tsconfig.build.json, biome.json, vitest.config.ts
│       ├── src/index.ts, tests/index.test.ts
│       ├── .pre-commit-config.yaml, .gitignore, .nvmrc, Makefile
│       ├── README.md, CONTRIBUTING.md, CHANGELOG.md, LICENSE_*
│       ├── AGENTS.md, CLAUDE.md, .cursorrules, .github/copilot-instructions.md
│       ├── .github/workflows/{main,release,copilot-setup-steps}.yml
│       ├── .devcontainer/devcontainer.json, .vscode/{settings,extensions}.json
├── tests/test_node_template.py
├── .github/workflows/main.yml        # + node-template job
├── docs/features/node.md, mkdocs.yml, README.md, CLAUDE.md, MANIFEST.in
```

**Structure Decision**: a sibling template folder rather than a language question in the root template: the two file trees share almost nothing, cruft supports `directory`, and the Python template's tests and users are untouched.

## Complexity Tracking

`node/local_extensions.py` duplicates the root file because cookiecutter imports extensions from the template directory only; a test asserts the two stay identical.
