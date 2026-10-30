# Feature Specification: new-project for Python

**Feature Branch**: `002-new-project-python`

**Created**: 2026-10-30

**Status**: Draft

**Input**: User description: "new-project skill, Python only. Replace the new-project placeholder skill in the project-kit plugin with a working workflow that creates a new Python project from the samuelduchesne/cookiecutter-gi template. Claude interviews the user for the template's answers (project name, description, layout, Python versions, type checker, optional features, license, agent instructions…), taking the questions, choices and defaults from the template's own cookiecutter.json rather than a copy kept in the plugin. It shows a summary and a preview of what will be created, gets confirmation, then generates the project with cruft so the project stays linked to the template for later upgrades, initializes spec-kit (pinned version, Claude integration) in the new project, initializes a git repository and makes an initial commit, and reports what was created and the next steps. The project's linting/formatting and CHANGELOG.md come from the template itself; the skill adds nothing the template doesn't provide. A script in the plugin does the predictable steps (fetch template options, validate answers, build and run the commands) and supports a dry-run mode. The skill checks that the required tools (git, uv/uvx) and access to the private template are available and explains clearly what is missing; it refuses to write into an existing non-empty directory. Node projects are out of scope: if the user asks for one, the skill says Node support is planned. Out of scope also: creating a GitHub repository, pushing, installing dependencies, upgrade-project and audit-project (they stay placeholders)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a Python project with the recommended setup (Priority: P1)

Samuel asks Claude to start a new Python project. Claude asks only for what has no sensible default (project name, a one-line description, and who the author is), proposes the template's recommended answers for everything else, shows a summary and confirms, then creates the project. The result is a ready-to-work repository: template files, linked to the template for future upgrades, spec-kit set up, under version control with a first commit.

**Why this priority**: This is the workflow's reason to exist; with it alone, starting a project goes from a manual multi-tool sequence to one conversation.

**Independent Test**: In a scratch folder, ask for a new Python project named `demo-proj` and accept the recommended setup. The new folder contains the template's files, a record linking it to the template, spec-kit's files, and a git history with exactly one commit; nothing outside the new folder changes.

**Acceptance Scenarios**:

1. **Given** the required tools and template access are available, **When** the user asks for a new Python project and accepts the recommended setup, **Then** a new folder is created containing the template's files for the given name, and Claude reports what was created.
2. **Given** a project was just created, **When** the user inspects it, **Then** it records which template and template version it came from (so it can be upgraded later), contains spec-kit's files set up for Claude, and is a git repository whose single commit contains every generated file.
3. **Given** a project was just created, **When** Claude reports back, **Then** the report lists the folder, the template version used, the main options chosen, and the next steps (install dependencies, create a remote repository, start a first spec).

---

### User Story 2 - Choose the options (Priority: P2)

The user wants something other than the defaults: a `src/` layout, a different minimum Python version, mypy instead of pyright, no Docker, a different license. Claude offers every question the template asks, with its choices and defaults, accepts answers in plain language, checks them against the allowed choices, and confirms the full set before creating anything.

**Why this priority**: The recommended setup covers most cases, but the template has many options and a project created with the wrong ones has to be redone.

**Independent Test**: Ask for a project with a `src/` layout, mypy, no Dockerfile and the BSD license. The created project matches each choice, and the record of the template answers shows exactly those values.

**Acceptance Scenarios**:

1. **Given** the template defines a question, **When** Claude interviews the user, **Then** the question, its choices and its default come from the template's current definition, so a new template option appears without changing the plugin.
2. **Given** the user gives an answer outside a question's allowed choices (e.g. a Python version the template doesn't offer), **When** answers are checked, **Then** Claude says which answer is invalid, lists the allowed choices, and asks again; nothing is created.
3. **Given** dependent answers conflict (e.g. a development Python version lower than the minimum), **When** answers are checked, **Then** the conflict is reported before anything is created.
4. **Given** all answers are valid, **When** Claude asks for confirmation, **Then** it shows every answer that differs from the template default and the destination folder, and creates nothing until the user confirms.

---

### User Story 3 - Preview and fail safely (Priority: P3)

Before creating anything, the user can ask what would happen; and when something is missing (a tool, access to the template, a free destination), the workflow stops before making any change and says exactly what to fix.

**Why this priority**: It protects the user's files and saves time on failures, but the main path works without it.

**Independent Test**: Run a preview and confirm no folder is created. Then try to create a project into an existing non-empty folder, and without access to the template; each stops with a specific message and changes nothing.

**Acceptance Scenarios**:

1. **Given** valid answers, **When** the user asks for a preview, **Then** Claude shows the destination, the template version, the answers, and each step that would run, and creates nothing.
2. **Given** the destination folder exists and is not empty, **When** creation is requested, **Then** it is refused before any step runs, and the user is asked for another name or location.
3. **Given** a required tool is missing, **When** the workflow starts, **Then** Claude names the missing tool and how to install it, and stops.
4. **Given** the user's environment cannot reach the private template (no access or no network), **When** the workflow starts, **Then** Claude says the template could not be reached, gives the likely cause (access to `samuelduchesne/cookiecutter-gi` or network), and stops.
5. **Given** a step fails after the project folder was created (e.g. spec-kit setup), **When** the failure is reported, **Then** Claude says which step failed, what was already created, and leaves the folder in place for the user to inspect or delete, without deleting anything itself.

### Edge Cases

- The user asks for a Node project: Claude says Node support is planned and not available yet, and offers a Python project instead only if the user wants one.
- The project name is one the template rejects (e.g. it contains `_` or spaces): the preview reports the template's own error message and asks for another name. For a valid name, the summary shows the folder name and the package name the template derives (e.g. `demo-proj` → `demo_proj`) before confirmation.
- The user is inside an existing git repository: the new project is created in its own folder with its own git repository; the enclosing repository is not modified.
- The template's question list changes between preview and creation: creation uses the same template version shown in the preview.
- The user's git has no name/email configured: the initial commit uses the author name and email from the answers, without changing the user's git configuration.
- The workflow is invoked where no shell is available (e.g. some chat environments): Claude explains that this workflow needs a local environment (Claude Code or Cowork on the user's computer) and stops.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The workflow MUST create new Python projects from the `samuelduchesne/cookiecutter-gi` template only; for any other language it MUST say that support is planned and create nothing.
- **FR-002**: The questions, choices, defaults and prompt texts presented to the user MUST be read from the template's current definition at run time; the plugin MUST NOT keep its own copy of them.
- **FR-003**: The workflow MUST ask the user for the project name, description, and author details (name, email, GitHub handle), and MUST offer the template's defaults for all other questions, letting the user accept them as a whole or change any of them.
- **FR-004**: Every answer MUST be validated before anything is created in the destination: choice questions against the template's allowed values and yes/no questions as booleans by the workflow, and every rule the template enforces itself (e.g. valid project name, development Python version not lower than the minimum) by running the template's own checks during the preview. The plugin MUST NOT re-implement the template's rules.
- **FR-005**: Before creating anything, the workflow MUST show a summary with the destination folder, the template version (commit), the derived folder and package names, and every answer that differs from the template default, and MUST wait for the user's confirmation.
- **FR-006**: A preview mode MUST show everything in FR-005 plus the files the template would generate and each step that would run, and MUST create, change or delete nothing outside a temporary folder that it removes before finishing.
- **FR-007**: The project MUST be generated so that it records its template, template version and answers, allowing it to be upgraded to newer template versions later.
- **FR-008**: The workflow MUST set up spec-kit in the new project, for Claude, using a pinned spec-kit version.
- **FR-009**: The workflow MUST initialize a git repository in the new project on a `main` branch and make one initial commit containing every generated file, authored with the name and email from the answers.
- **FR-010**: The workflow MUST NOT add, remove or modify any project file beyond what the template and spec-kit generate (linting, formatting, changelog and agent files all come from the template).
- **FR-011**: The workflow MUST check, before any change, that the required tools are installed and that the template can be reached, and MUST name what is missing and how to fix it when not.
- **FR-012**: The workflow MUST refuse to create a project in an existing non-empty folder, and MUST NOT modify anything outside the new project folder.
- **FR-013**: When a step fails, the workflow MUST stop, report the failed step and what was already created, and MUST NOT delete anything itself.
- **FR-014**: After success, the workflow MUST report the folder, template version, main options and next steps (install dependencies with the project's own command, create a remote repository, start a first spec).
- **FR-015**: The workflow MUST NOT install dependencies, create a remote repository or push anything.
- **FR-016**: `upgrade-project` and `audit-project` MUST remain placeholders, unchanged in behavior.
- **FR-017**: The plugin's changelog MUST record the new workflow, and the plugin version MUST increase to signal the new behavior to installed users.

### Key Entities

- **Template definition**: The questions the template asks, each with a name, prompt text, type (free text, yes/no, single choice), allowed choices and default. Read from the template at run time.
- **Answers**: The user's value for each question, plus the derived values the template computes (e.g. package name). Validated against the template definition.
- **Template version**: The exact template commit used, shown in the preview and recorded in the project.
- **Project**: The created folder — template files, the template link record, spec-kit files, and a git repository with one commit.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user who accepts the recommended setup goes from request to a ready project in under 3 minutes, answering at most 5 questions.
- **SC-002**: 100% of the template's questions are offered with the template's own choices and defaults; adding a question to the template makes it appear in the interview with 0 plugin changes.
- **SC-003**: For every invalid answer tried during acceptance (out-of-range choice, non-boolean yes/no, development Python below the minimum), 0 files are created and the message names the allowed values.
- **SC-004**: Preview mode and every refused or failed pre-check leave 0 files created, modified or deleted outside the system's temporary folder, and remove what they put there.
- **SC-005**: Every created project can be checked for template updates immediately after creation without any further setup.
- **SC-006**: A newly created project contains 0 files that the template or spec-kit did not generate.

## Assumptions

- The user runs the workflow in an environment with a shell on their own computer (Claude Code, or Cowork running locally), with git and uv installed, and network access to GitHub.
- The user has read access to the private `samuelduchesne/cookiecutter-gi` repository through their existing git credentials; the workflow does not manage credentials.
- The template's default branch is the version used, unless the user names a specific version.
- Spec-kit is pinned to v1.2.5, the version this repository uses; updates are a deliberate change in a later release.
- The default destination is a folder named after the project in the current working directory; the user can name another parent folder.
- Whether a changelog is generated depends on the template version (the changelog option is being added to the template separately); the workflow passes it through like any other question.
- The plugin version moves from 0.1.0 to 0.2.0.
