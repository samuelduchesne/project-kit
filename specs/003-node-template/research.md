# Research: Node template

**Feature**: 003-node-template | **Date**: 2026-10-30

Versions were checked against the npm registry, PyPI and GitHub tags on 2026-10-30, and a generated project was installed, checked, tested and built with each.

## R1. Where the template lives

- **Decision**: `node/` in cookiecutter-gi, generated with `cookiecutter <repo> --directory node` (cruft records `directory: node`).
- **Rationale**: one repository, one branch and one commit history for both languages; cruft's `directory` support makes link and update work unchanged. The root template only renders `{{cookiecutter.project_name}}/`, so `node/` never leaks into Python projects.
- **Alternatives**: a separate repository (two access grants, two histories); a language question in the root template (one huge conditional tree).

## R2. Package manager and versions

- **Decision**: pnpm only, pinned with `"packageManager": "pnpm@12.16.1"`, installed with `npm install -g pnpm` locally (it switches to the pinned version; Node.js 25 and later no longer include corepack) and `pnpm/action-setup@v4` in CI. Exact pins: `@biomejs/biome` 2.6.4, `typescript` 7.0.2, `vitest` and `@vitest/coverage-v8` 5.0.5, `@types/node` latest of the chosen major.
- **Rationale**: user choice (pnpm only); exact versions keep fresh projects reproducible until the lockfile exists. Vitest 5 supports Node `^22.12 || ^24 || >=26`, so the offered versions are 24 (default, LTS), 22 and 26.

## R3. Lint and format through pre-commit

- **Decision**: a `local` pre-commit hook running `pnpm exec biome check --write --no-errors-on-unmatched --files-ignore-unknown=true`, plus the Python template's generic hooks (case conflict, merge conflict, YAML, JSON, end of file, trailing whitespace). pre-commit itself runs as `uvx pre-commit@4.7.0`.
- **Rationale**: one Biome version (the project's own, from the lockfile) for the editor, CI and hooks; the remote `biomejs/pre-commit` hook needs a second pin and a node environment built by pre-commit. Biome formats JSON, so the generic JSON formatter hook is not used.

## R4. TypeScript build and tests

- **Decision**: `tsconfig.json` (strict, `module`/`moduleResolution` `nodenext`, `noEmit`, includes `src` and `tests`) for type checking; `tsconfig.build.json` extends it and emits `dist/` with declarations from `src` only. Vitest with V8 coverage, `lcov` + text reporters, thresholds off by default.
- **Rationale**: tests are type-checked but never published; `exports` points at `dist/index.js` and `dist/index.d.ts`.

## R5. Publishing

- **Decision**: when `publish_to_npm` is true, `.github/workflows/release.yml` runs on a published GitHub release, checks the tag matches `package.json` version, builds and runs `npm publish --provenance --access public` with `id-token: write` (npm trusted publishing). Otherwise the package is `"private": true`.
- **Rationale**: no long-lived token; matches project-kit's `create-release` (`npm version`, then a GitHub release).

## R6. Hooks

- **Decision**: `pre_gen_project.py` checks the name against npm's rules for unscoped names (`^[a-z0-9][a-z0-9._-]*$`, ≤ 214 characters, not starting with `.` or `_`) plus the root template's rule that it starts with a letter, and every boolean like the Python hook. `post_gen_project.py` prunes license, agent, workflow, devcontainer and changelog files with the same helpers.
