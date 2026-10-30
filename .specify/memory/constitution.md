# project-kit Constitution

project-kit is a Claude plugin (distributed as a marketplace from `samuelduchesne/project-kit`) that creates, audits and upgrades software projects against Samuel's standards. Its project templates live in `samuelduchesne/cookiecutter-gi`: the Python template at the repository root, the Node template under `node/`.

## Core Principles

### I. Templates Are the Source of Truth

- Project files MUST come from the cookiecutter-gi templates, generated with cookiecutter and kept current with cruft.
- The plugin MUST NOT write project scaffolding from its own instructions or keep a second copy of any template file.
- When a standard changes, the change is made in the template first; the plugin only learns how to apply it.

Rationale: a template is deterministic, testable and upgradable. A file the model writes from prose is none of these, and it leaves nothing for `cruft update` to compare against later.

### II. Scripts for Predictable Steps, the Model for Judgment

- Generation, linking, checking and auditing MUST run through scripts or the underlying CLIs (cookiecutter, cruft, specify, git), invoked with explicit, logged arguments.
- The model is reserved for steps that need judgment: interviewing the user for template answers, inferring answers for unlinked projects, resolving `cruft update` conflicts and `.rej` files, and explaining audit findings.
- Every script MUST support a dry-run mode that prints what it would do.

Rationale: the same inputs must always produce the same project; the model's value is in the cases a script can't decide.

### III. Show Before Changing

- Commands that modify an existing project (upgrade, link, fix) MUST show the user a diff or a list of planned changes and get confirmation before writing.
- Existing files MUST NOT be overwritten without confirmation. Audits are read-only by default.
- Work MUST start from a clean git working tree, or the user MUST explicitly accept the risk, so every change can be reverted.

Rationale: these commands run on real projects with uncommitted work and local customizations.

### IV. Works Wherever It Is Installed

- Skills MUST work in claude.ai chat, Cowork and Claude Code, provided the environment has a shell with the required CLIs; a skill MUST check for those tools and say clearly what is missing instead of failing partway.
- Components that only run in some environments (hooks, agents) MUST be optional: no core workflow may depend on them.
- Tool versions the plugin installs or calls (spec-kit, cruft, cookiecutter) MUST be pinned, and the pins updated deliberately.

Rationale: the plugin is installed per account and syncs to every surface, and colleagues will use it in environments the author doesn't control.

## Scope and Constraints

- In scope: creating projects (Python and Node), setting up spec-kit in them, enforcing lint/format standards (ruff for Python, Biome for Node, the pre-commit framework for both), keeping a Keep a Changelog 1.1.0 `CHANGELOG.md`, auditing projects for drift, and upgrading projects via cruft.
- Out of scope: hosting or publishing projects, managing secrets, and changing GitHub settings without an explicit request.
- Deferred to v2: automated evals for each skill.
- The repository keeps spec-kit's development files (`.specify/`, root `.claude/skills/speckit-*`) separate from the plugin itself, which lives under `plugins/project-kit/`.
- License: MIT.

## Development Workflow

- Each feature goes through spec-kit: specify, plan, tasks, implement. One spec per feature.
- Every user-facing change gets an entry under `## [Unreleased]` in this repository's `CHANGELOG.md`.
- `claude plugin validate` MUST pass on the marketplace and the plugin before merging.
- Releases are tagged with semantic versions, and the plugin's `version` in `plugin.json` matches the tag.

## Governance

- This constitution overrides other practices in this repository. Specs and plans MUST include a check against each principle and justify any exception in writing.
- Amendments are made by pull request, state their reason, and bump the version: MAJOR for removing or redefining a principle, MINOR for adding one, PATCH for clarifications.

**Version**: 1.0.0 | **Ratified**: 2026-10-30 | **Last Amended**: 2026-10-30
