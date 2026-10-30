# Feature Specification: Marketplace and Plugin Skeleton

**Feature Branch**: `001-plugin-skeleton`

**Created**: 2026-10-30

**Status**: Implemented

**Input**: User description: "Marketplace and plugin skeleton for project-kit. The repository samuelduchesne/project-kit must be installable as a Claude plugin marketplace (via claude.ai / Claude Desktop "Customize > Plugins > Add > Add marketplace" with the owner/repo shorthand, and via `claude plugin marketplace add samuelduchesne/project-kit` in Claude Code). It contains one plugin, project-kit, under plugins/project-kit/, listed in a root .claude-plugin/marketplace.json; the plugin has its own .claude-plugin/plugin.json whose name matches the marketplace entry. The skeleton ships placeholder (stub) skills for the planned workflows — new-project, upgrade-project, audit-project — each stating its purpose and that it is not yet implemented, so the install and discovery path can be verified end to end before real behavior lands in later specs. The repo also gets a README explaining what project-kit is and how to install it, a CHANGELOG.md in Keep a Changelog 1.1.0 format, and a CI check that runs `claude plugin validate` on the marketplace and plugin. Spec-kit's own files (.specify/, .claude/skills/speckit-*) stay at the repo root and must not be packaged into the plugin. Out of scope: actual skill behavior (scaffolding, upgrades, audits), the Node template, hooks, agents, and evals."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Install project-kit from the repository (Priority: P1)

Samuel (and later an Introba colleague) adds the project-kit repository as a plugin marketplace, in claude.ai / the Claude desktop app or in Claude Code, and installs the project-kit plugin from it without editing any files or knowing the repository layout.

**Why this priority**: Every later feature depends on this install path. If people cannot add the marketplace and install the plugin, no skill can reach them.

**Independent Test**: From an account or machine that has never seen project-kit, add the marketplace by its `owner/repo` shorthand, install the plugin, and confirm it is listed as installed and enabled.

**Acceptance Scenarios**:

1. **Given** a claude.ai account without project-kit, **When** the user adds `samuelduchesne/project-kit` through the Add marketplace dialog, **Then** the project-kit plugin appears among the available plugins and can be added to the account.
2. **Given** Claude Code without project-kit, **When** the user adds the marketplace `samuelduchesne/project-kit` and installs `project-kit` from it, **Then** the install succeeds and the plugin is listed as enabled.
3. **Given** the plugin is installed, **When** a new version is published to the repository, **Then** the user can pull it through the platform's normal update path (check for updates / update marketplace) without reinstalling.

---

### User Story 2 - Discover the planned workflows (Priority: P2)

After installing, the user sees the three planned workflows — new project, upgrade project, audit project — in the skill/command list under the project-kit name. Invoking any of them explains what the workflow will do and states clearly that it is not implemented yet.

**Why this priority**: It proves skills from this plugin are discovered and invocable on every surface, and it sets expectations so nobody mistakes a stub for a working tool.

**Independent Test**: After install, open the skill list, find the three project-kit workflows, invoke each one, and confirm the response describes the purpose and says it is not yet available.

**Acceptance Scenarios**:

1. **Given** the plugin is installed, **When** the user types `/` and filters by project-kit, **Then** new-project, upgrade-project and audit-project are listed with a one-line description each.
2. **Given** the plugin is installed, **When** the user invokes any of the three workflows, **Then** the reply states the workflow's purpose, says it is not implemented yet, and makes no change to any file or project.
3. **Given** the user asks in plain language to create, upgrade or audit a project, **When** the request matches a stub, **Then** the user is told the workflow is planned but not yet available, rather than Claude improvising the work.

---

### User Story 3 - Keep the repository releasable (Priority: P3)

When Samuel changes the marketplace or plugin definition, an automated check tells him before merging whether the marketplace and plugin are still valid. The repository explains itself to a newcomer and records changes in a changelog.

**Why this priority**: It protects the install path from regressions as later specs add real skills, but nothing breaks for users on day one without it.

**Independent Test**: Open a change that breaks the plugin definition and confirm the check fails; revert it and confirm the check passes. Read the README cold and install from its instructions alone.

**Acceptance Scenarios**:

1. **Given** a pull request that leaves the marketplace and plugin definitions valid, **When** the automated check runs, **Then** it passes.
2. **Given** a pull request that makes either definition invalid (e.g. mismatched plugin names or a broken source path), **When** the automated check runs, **Then** it fails and names the problem.
3. **Given** a visitor to the repository, **When** they read the README, **Then** they learn what project-kit is, which workflows are planned, and how to install it on each surface.
4. **Given** this feature is complete, **When** the changelog is opened, **Then** it follows Keep a Changelog 1.1.0 and lists the skeleton under its unreleased or first release section.

### Edge Cases

- The marketplace is added on an account that cannot add custom marketplaces (e.g. a Team/Enterprise organization whose Owner disabled it): the README says this is controlled by the organization and points to the alternative of org-level distribution.
- Spec-kit development files exist at the repository root: they MUST NOT appear in the installed plugin, and installing the plugin MUST NOT add speckit skills to the user's account.
- A stub is invoked inside a real project: it MUST NOT create, modify or delete any file.
- The plugin and marketplace entry names drift apart in a later change: the automated check catches it before merge.
- The repository is renamed or transferred later: out of scope; the README documents only the current location.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The repository MUST be accepted as a plugin marketplace when added by its `samuelduchesne/project-kit` shorthand, in claude.ai / the desktop app and in Claude Code.
- **FR-002**: The marketplace MUST list exactly one plugin, named `project-kit`, whose files live in their own subfolder of the repository, separate from the repository root.
- **FR-003**: The plugin's own name MUST match its marketplace entry name, so it installs as `project-kit@<marketplace name>` and its skills are prefixed `project-kit:`.
- **FR-004**: The plugin MUST carry a version number, starting at `0.1.0`, and the same version MUST be used for the first tagged release.
- **FR-005**: The plugin MUST provide three skills: `new-project`, `upgrade-project` and `audit-project`. Each MUST have a one-line description of the workflow it will provide.
- **FR-006**: When invoked, each skill MUST state its intended purpose, state that it is not implemented yet, and MUST NOT run commands or change files.
- **FR-007**: The skills' descriptions MUST make clear they are placeholders, so Claude does not treat them as able to do the work when a user asks in plain language.
- **FR-008**: The installed plugin MUST NOT include the spec-kit development files (`.specify/`, root `.claude/skills/speckit-*`), the specs, CI configuration or other repository-only files.
- **FR-009**: The repository MUST include a README that explains what project-kit is, lists the planned workflows and their status, and gives install steps for claude.ai / the desktop app and for Claude Code, including how to update.
- **FR-010**: The README MUST note that on Team and Enterprise plans an organization Owner controls whether members can add their own marketplaces.
- **FR-011**: The repository MUST include a `CHANGELOG.md` following Keep a Changelog 1.1.0, with this skeleton recorded as the first entry.
- **FR-012**: An automated check MUST run on every pull request and on pushes to the main branch, validating both the marketplace definition and the plugin definition, and MUST fail when either is invalid.
- **FR-013**: The plugin MUST contain no hooks, agents or connectors in this feature.

### Key Entities

- **Marketplace**: The catalog that the repository presents to Claude. Attributes: name, owner, list of plugin entries. Contains one entry for this feature.
- **Plugin entry**: The marketplace's record of one plugin. Attributes: name, source location within the repository, description.
- **Plugin**: The installable unit. Attributes: name, version, description, author, license, and the skills it contains.
- **Skill (stub)**: A named workflow inside the plugin. Attributes: name, description, status (not yet implemented).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A first-time user can add the marketplace and install the plugin in under 2 minutes on each of the two surfaces (claude.ai / desktop app, Claude Code), following only the README.
- **SC-002**: All 3 planned workflows appear under the project-kit name in the skill list after install, on both surfaces.
- **SC-003**: Invoking each of the 3 stubs changes 0 files and produces a reply that names the workflow's purpose and its not-yet-implemented status.
- **SC-004**: The installed plugin contains 0 spec-kit or repository-only files.
- **SC-005**: The automated check fails on 100% of deliberately broken definitions tried during acceptance (mismatched names, missing source folder, invalid file syntax) and passes on the unmodified repository.

## Assumptions

- The repository stays public on GitHub under `samuelduchesne`, so no access setup is needed to add the marketplace.
- The marketplace is named `project-kit`, the same as the plugin, so the install id reads `project-kit@project-kit`.
- Plugin metadata uses author Samuel Letellier-Duchesne and the MIT license, matching the repository LICENSE.
- The automated check runs on GitHub Actions, the CI the rest of Samuel's repositories use.
- Surfaces that cannot run a shell are acceptable for stubs, because stubs run nothing; shell requirements arrive with the real skills in later specs.
- Later specs replace the stub skills in place under the same names, so users who install now keep the same skill names.
