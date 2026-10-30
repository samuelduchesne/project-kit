# Feature Specification: audit-project

**Feature Branch**: `006-audit-project`

**Created**: 2026-10-30

**Status**: Implemented

**Input**: User description: "audit-project for Python and Node: check a project against the cookiecutter-gi standards and report drift without changing anything: template link and version, files that differ from the template, linting and formatting setup (ruff or Biome through pre-commit), the changelog, and spec-kit. Each finding says how to fix it."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Audit a linked project (Priority: P1)

The user asks Claude to audit a project. Claude reports, grouped by severity, whether the project is linked and current, which files have drifted from the template, and whether the lint/format, changelog and spec-kit standards are in place, each with the fix (usually another project-kit workflow).

**Independent Test**: Audit a freshly created fixture project: 0 problems. Edit a template file, delete the changelog's Unreleased section, remove `.specify/`, update the template: the audit reports each one, and the project is unchanged.

**Acceptance Scenarios**:

1. **Given** a project just created by new-project, **When** it is audited, **Then** no errors or warnings are reported.
2. **Given** a project behind the template, **When** audited, **Then** the report shows how many template commits it is behind and suggests upgrade-project.
3. **Given** local edits to template-generated files, **When** audited, **Then** each drifted file is listed, as information (local edits may be intentional).
4. **Given** a missing or malformed changelog, missing lint/format hooks, or missing spec-kit, **When** audited, **Then** each is reported with its fix.

---

### User Story 2 - Audit an unlinked or foreign project (Priority: P2)

**Independent Test**: Audit a project with no link record: the report says it is unlinked, still checks the standards, and suggests upgrade-project to link it.

**Acceptance Scenarios**:

1. **Given** no link record, **When** audited, **Then** the template checks are skipped with that reason and the standards checks still run.
2. **Given** a project that is neither Python nor Node, **When** audited, **Then** Claude says the standards cover Python and Node projects only and reports only the language-neutral checks.

### Edge Cases

- No network: template checks are reported as not run, with the reason; local checks still run.
- Not a git repository: reported as an error, since upgrades need history.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The audit MUST be read-only: it MUST NOT create, change or delete any file in the project.
- **FR-002**: It MUST check: git repository and clean tree; language; template link (template, folder, commit); commits behind the template's branch for that template's folder; files that differ from the template at the recorded commit; pre-commit configuration with the language's linter/formatter (ruff for Python, Biome for Node); a Keep a Changelog 1.1.0 changelog with an Unreleased section; spec-kit set up, and at which version compared with the plugin's pin.
- **FR-003**: Every finding MUST have an id, a severity (error, warning, info), a message and a fix.
- **FR-004**: The output MUST be machine-readable for Claude to explain, with a summary count per severity.
- **FR-005**: Checks that cannot run MUST be reported as skipped with the reason, not as passing.

## Success Criteria *(mandatory)*

- **SC-001**: A freshly created project audits with 0 errors and 0 warnings.
- **SC-002**: Each seeded defect in the test suite produces exactly its finding.
- **SC-003**: The project is byte-for-byte unchanged after an audit.

## Assumptions

- Template comparison uses the same cruft and template access as new-project and upgrade-project.
- Standards beyond those listed (test coverage thresholds, dependency freshness) are out of scope for this version.
