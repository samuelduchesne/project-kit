# Feature Specification: new-project for Node

**Feature Branch**: `004-new-project-node`

**Created**: 2026-10-30

**Status**: Implemented

**Input**: User description: "Node support in new-project: create a Node (TypeScript) project from the cookiecutter-gi Node template with the same interview, preview, cruft link, spec-kit setup and initial commit as Python projects."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a Node project (Priority: P1)

The user asks for a new Node or TypeScript project. Claude runs the same workflow as for Python, but reads the questions from the Node template, previews, and creates a project linked to the Node template, with spec-kit and one commit.

**Why this priority**: It is the feature.

**Independent Test**: Ask for a Node project named `demo-lib` with defaults; the folder contains the Node template's files, a template link that names the Node template folder, spec-kit's files and one commit.

**Acceptance Scenarios**:

1. **Given** the user asks for a Node, TypeScript or JavaScript project, **When** the workflow runs, **Then** the questions shown are the Node template's.
2. **Given** a created Node project, **When** it is inspected, **Then** its template link records the template, the Node template folder, the branch and the commit, so it can be upgraded later.
3. **Given** a created Node project, **When** Claude reports, **Then** the next steps are the Node ones (install with the project's own command, which uses pnpm).

---

### User Story 2 - Language is explicit (Priority: P2)

When the request doesn't say which language, Claude asks Python or Node before anything else.

**Independent Test**: Ask for "a new project"; Claude asks the language and does not read any template until answered.

**Acceptance Scenarios**:

1. **Given** no language in the request, **When** the workflow starts, **Then** Claude asks Python or Node.
2. **Given** another language (e.g. Rust), **When** the workflow starts, **Then** Claude says only Python and Node are supported and stops.

### Edge Cases

- The template version has no Node template (older ref): the workflow says the template has no Node template at that version and stops.
- Python behavior is unchanged: existing invocations without a language default to Python.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The helper script MUST accept a language (`python` default, `node`) for every command, and read questions, validate and generate from the matching template folder.
- **FR-002**: Node projects MUST be generated so that the link record names the template folder, and later upgrades use it.
- **FR-003**: Every Python guarantee of spec 002 (preview, confirmation, same commit, no overwrite, no deletes, spec-kit, one commit, no dependency install or push) MUST hold for Node.
- **FR-004**: The skill MUST pick the language from the request or ask, and give language-specific next steps.
- **FR-005**: The plugin changelog, README and version MUST reflect Node support.

## Success Criteria *(mandatory)*

- **SC-001**: A Node project with defaults is created in the same number of questions as a Python one (at most 5).
- **SC-002**: 100% of the script's Python tests still pass; Node equivalents of the create, preview and link-record tests pass.

## Assumptions

- The Node template lives under `node/` in the same repository and branch as the Python template (spec 003).
- Creating a Node project needs only git and uv, like Python; pnpm and Node are needed afterwards to install and work on it, and the report says so.
