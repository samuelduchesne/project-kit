# Feature Specification: upgrade-project

**Feature Branch**: `005-upgrade-project`

**Created**: 2026-10-30

**Status**: Implemented

**Input**: User description: "upgrade-project for Python and Node: bring an existing project up to the latest cookiecutter-gi template with cruft, linking it to the template first if it was never linked. For unlinked projects, link at the template commit closest to the project's first commit, with answers Claude infers from the project, both confirmed by the user, so the update is a real three-way merge. Show every change before applying it; start from a clean working tree; Claude resolves conflicts with the user."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Update a linked project (Priority: P1)

The project was created by new-project (or with cruft). The user asks to upgrade it. Claude reports how far behind it is, shows the exact changes the update would make, gets confirmation, applies them, helps resolve any conflict, and offers to commit.

**Why this priority**: Every project created by project-kit is linked; keeping them current is the main use.

**Independent Test**: Create a project from a fixture template, change the template, run the upgrade: the preview lists the changed files and diff, the real run applies exactly that diff, and the link record moves to the new template commit.

**Acceptance Scenarios**:

1. **Given** a linked project with a clean working tree and a newer template, **When** the user asks to upgrade, **Then** Claude shows the template versions (current and latest), the files that would change and the diff, and changes nothing.
2. **Given** the user confirms, **When** the upgrade runs, **Then** the project receives exactly the previewed changes, its link record points to the new commit, and nothing is committed until the user agrees.
3. **Given** an update conflicts with local changes, **When** it is applied, **Then** Claude lists each conflicted file and rejected hunk, proposes resolutions, and applies them only with the user's agreement.
4. **Given** the project is already up to date, **When** the user asks to upgrade, **Then** Claude says so and changes nothing.
5. **Given** the template added questions since the project was created, **When** the upgrade is previewed, **Then** Claude asks the user for those answers (defaults offered) and the preview uses them.

---

### User Story 2 - Link an unlinked project, then update (Priority: P2)

The project was made by hand or from an old copy of the template. Claude finds the template commit closest to the project's first commit, infers the answers from the project's files, shows how closely the template at that commit with those answers matches the project, refines the answers with the user, links, then continues with the update.

**Why this priority**: Older projects predate cruft; without linking they can never be upgraded safely.

**Independent Test**: Generate a project with plain cookiecutter from an old fixture commit, commit it, then link: the suggested commit is the old one, the match report shows identical files for the right answers, and after linking the update brings the later template changes.

**Acceptance Scenarios**:

1. **Given** an unlinked project, **When** the user asks to upgrade, **Then** Claude identifies the language, proposes the base template commit with its date and the answers it inferred, and shows which files match, differ, or are missing compared with the template rendered at that commit.
2. **Given** the user confirms the base commit and answers, **When** linking runs, **Then** only the link record is written, and it follows the template's branch so later updates work.
3. **Given** the user prefers the latest template commit as the base, **When** linking runs, **Then** it links there and the update finds nothing; Claude shows the remaining drift instead.

---

### User Story 3 - Refuse unsafe starts (Priority: P3)

**Independent Test**: Uncommitted changes, a project that is not a git repository, or an unreachable template each stop the workflow before any change, with the reason.

**Acceptance Scenarios**:

1. **Given** uncommitted changes, **When** the upgrade starts, **Then** Claude asks the user to commit or stash them first and changes nothing.
2. **Given** a project that is not a git repository, **When** the upgrade starts, **Then** Claude says the workflow needs git history to show and revert changes, and stops.
3. **Given** the template changed between preview and apply, **When** apply runs, **Then** it stops before writing and asks to preview again.

### Edge Cases

- The project is linked to a different template: Claude says so and stops; this workflow only manages cookiecutter-gi projects.
- A Node project linked before the Node template moved: the link's template folder is kept as recorded.
- Files the template deletes are deleted only as part of the previewed diff.
- `.rej` files from conflicts are listed; Claude removes them only after the user accepts the resolution.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The workflow MUST report link status, language, current and latest template commit, and whether the working tree is clean, without changing anything.
- **FR-002**: For unlinked projects, it MUST propose a base commit (the template's last commit at or before the project's first commit) and let the user choose another, including the latest.
- **FR-003**: It MUST validate inferred answers against the template's questions at the base commit and show a per-file match report between the project and the template rendered with those answers, writing nothing to the project.
- **FR-004**: Linking MUST write only the link record, recording the branch to follow.
- **FR-005**: An update preview MUST produce the exact diff the update would apply, by running the update on a copy of the project, and MUST NOT change the project.
- **FR-006**: Applying MUST refuse a dirty tree, check that the template commit equals the previewed one, apply the update, and report changed files, conflicted files and rejected hunks.
- **FR-007**: The workflow MUST NOT commit, push or delete files without the user's confirmation.
- **FR-008**: Answers to questions the template added MUST be asked of the user and passed to the update.
- **FR-009**: The workflow MUST work for Python and Node projects.

## Success Criteria *(mandatory)*

- **SC-001**: The applied changes equal the previewed diff in 100% of tested updates without conflicts.
- **SC-002**: Status, link preview and update preview leave the project byte-for-byte unchanged.
- **SC-003**: For a project generated from an old template commit, the suggested base is that commit and the match report shows 0 differing files with the right answers.

## Assumptions

- cruft (pinned, as in new-project) performs link and update; spec-kit files are not managed by this workflow.
- The project's first commit date approximates when it was generated from the template.
