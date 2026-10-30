# Feature Specification: Node template in cookiecutter-gi

**Feature Branch**: `003-node-template`

**Created**: 2026-10-30

**Status**: Implemented

**Input**: User description: "The Node template: a cookiecutter template for TypeScript libraries, kept in `samuelduchesne/cookiecutter-gi` under `node/`, holding the same standards as the Python template: Biome for linting and formatting run through the pre-commit framework, a Keep a Changelog `CHANGELOG.md`, AI agent instruction files, GitHub Actions, a license choice and a devcontainer. pnpm is the only package manager; TypeScript with Vitest; a library whose npm publishing is optional."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate a working TypeScript library (Priority: P1)

A developer generates a Node project from the template with the defaults. After installing dependencies, every standard command works on the untouched project: lint and format check, type check, tests with coverage and build.

**Why this priority**: A template whose fresh output fails its own checks is unusable, and every later feature (creation, upgrade, audit) builds on it.

**Independent Test**: Generate with defaults, install dependencies, then run the check, test and build commands; each exits successfully and the build produces the package's entry point and type declarations.

**Acceptance Scenarios**:

1. **Given** the template with default answers, **When** a project is generated, **Then** it contains a package manifest named after the project, a source entry point, a test, the linter/formatter configuration, the pre-commit configuration, a changelog, a license, a README and contribution guide, CI workflows and agent instructions.
2. **Given** a generated project, **When** dependencies are installed and the check, test and build commands are run, **Then** all succeed with no changes needed to the generated files.
3. **Given** a generated project, **When** the pre-commit hooks run on all files, **Then** they pass without modifying anything.

---

### User Story 2 - Choose the options (Priority: P2)

The developer picks the Node version, whether to include GitHub Actions, coverage reporting, npm publishing, a devcontainer and a changelog, the agent instruction files and their detail level, and the license. Each choice changes only the files it concerns.

**Why this priority**: The options mirror the Python template so both languages offer the same standard; the defaults alone already give a valid project.

**Independent Test**: Generate with each optional feature turned off and with every license and agent choice; the corresponding files are present or absent, and no generated file refers to a removed one.

**Acceptance Scenarios**:

1. **Given** npm publishing is chosen, **When** the project is generated, **Then** it contains a release workflow that builds and publishes the package to npm when a GitHub release is published, and the README explains how to release.
2. **Given** GitHub Actions are not chosen, **When** the project is generated, **Then** it contains no `.github/workflows` folder.
3. **Given** a license is chosen, **When** the project is generated, **Then** exactly that license is in `LICENSE` and the package manifest names it; "Not open source" leaves no license file and marks the package as unlicensed.
4. **Given** an agent instruction choice, **When** the project is generated, **Then** exactly the files of that choice exist, as in the Python template.
5. **Given** a Node version, **When** the project is generated, **Then** the minimum supported version, the local version file, CI and the devcontainer all use it.

---

### User Story 3 - Reject invalid input early (Priority: P3)

A project name that cannot be an npm package name, or a yes/no answer that is not a boolean, stops generation with a one-line `ERROR:` message before any file is written.

**Why this priority**: project-kit relays the template's own errors; the template must produce them.

**Independent Test**: Generate with the name `My_Package` and with `changelog=maybe`; both fail with an `ERROR:` line and leave no output.

**Acceptance Scenarios**:

1. **Given** a project name with uppercase letters, underscores, spaces or a leading digit, **When** generation runs, **Then** it fails with an `ERROR:` line naming the rule, and nothing is written.
2. **Given** a boolean option given as `false`, `no` or `0` on the command line, **When** generation runs, **Then** it is treated as false, as in the Python template.

### Edge Cases

- Generating the Python template from the repository root is unaffected: the Node template lives in its own folder and is never rendered by the root template.
- A project generated without GitHub Actions still has a README whose badges do not point to missing workflows.
- Turning off the changelog also removes the changelog rule from the agent files and the contribution guide.
- Coverage reporting off: no coverage upload in CI and no coverage badge.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The Node template MUST live in `samuelduchesne/cookiecutter-gi` under `node/`, with its own question file, hooks and files, generated with cookiecutter's directory option.
- **FR-002**: Generated projects MUST be TypeScript ES-module libraries using pnpm only, with strict type checking, Vitest tests with coverage, and a build that emits JavaScript and type declarations.
- **FR-003**: Linting and formatting MUST use Biome, run both directly and through the pre-commit framework, together with the same generic file checks the Python template uses.
- **FR-004**: The template MUST ask for author, email, GitHub handle, project name and description, and offer: Node version, GitHub Actions, coverage reporting, npm publishing, devcontainer, changelog, agent instructions, agent profile and license, with defaults that produce a working project.
- **FR-005**: The agent instruction, agent profile, changelog and license options MUST behave as the Python template's options of the same name.
- **FR-006**: The template MUST validate the project name as an npm package name and every boolean answer before generating, failing with an `ERROR:` line.
- **FR-007**: Every tool version the generated project uses (Biome, TypeScript, Vitest, pnpm, pre-commit hooks) MUST be pinned.
- **FR-008**: The template's test suite MUST cover generation with defaults, each option and the input checks, and CI MUST install, check, test and build a generated project.
- **FR-009**: The template repository's documentation (README, docs site, CLAUDE.md) MUST describe the Node template and how to generate from it.

### Key Entities

- **Node template**: `node/cookiecutter.json`, `node/hooks/`, `node/{{cookiecutter.project_name}}/`.
- **Generated project**: a pnpm TypeScript library with the standard files.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A project generated with defaults passes its check, test and build commands with 0 edits.
- **SC-002**: 100% of option combinations tested in the template's suite generate without error, and every generated YAML and JSON file parses.
- **SC-003**: Invalid names and booleans fail with 0 files written.
- **SC-004**: The existing Python template tests pass unchanged.

## Assumptions

- Node 24 is the default (active LTS); 22 and 26 are offered. The tools pinned support all three.
- pnpm is pinned in the `packageManager` field. Contributors install it with `npm install -g pnpm`, which switches to the pinned version (Node.js 25 and later no longer include corepack); CI installs it with the pnpm GitHub action.
- The pre-commit framework is run through `uvx`, so a Node project's contributor needs uv, as the plugin already requires.
- npm publishing uses npm trusted publishing (OIDC) from GitHub Actions, with provenance.
- Docker, documentation sites and data pipelines are Python-template features with no Node equivalent in this version.
