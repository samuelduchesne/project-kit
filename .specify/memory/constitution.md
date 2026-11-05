<!--
Sync Impact Report
- Version change: 1.2.0 -> 1.3.0 (MINOR)
- Reason: feature 008 (code-review-style arguments for sci-review) adds `--fix`, which must behave as `/code-review --fix`: it applies the review's findings to the working tree without a further confirmation and without requiring a clean working tree.
- Version class: MINOR, because the amendment adds a bounded exception to Principle III and neither removes nor redefines the principle; the clarification of Principle IV (pin rule) is PATCH-level and is carried by the same amendment.
- Modified sections: Principle III (exception for an explicit `--fix` request); Principle IV (pin rule applies to tools the plugin installs); Scope and Constraints (`sci-review` read-only except under `--fix`)
- Added sections: none
- Removed sections: none
- Templates requiring updates: none (plan, spec and tasks templates reference principles by name only)
- Follow-up TODOs: none
-->

# project-kit Constitution

project-kit is a marketplace of plugins, distributed from `samuelduchesne/project-kit`. Its first plugin, `project-kit`, creates, audits, upgrades and maintains software projects against Samuel's standards. Its second plugin, `sci-review`, reviews code for scientific correctness. The `project-kit` plugin's project templates live in `samuelduchesne/project-kit-cookiecutter`: the Python template at the repository root, the Node template under `node/`.

## Core Principles

### I. Templates Are the Source of Truth

- Project files MUST come from the project-kit-cookiecutter templates, generated with cookiecutter and kept current with cruft.
- The plugin MUST NOT write project scaffolding from its own instructions or keep a second copy of any template file.
- When a standard changes, the change is made in the template first; the plugin only learns how to apply it.

Rationale: a template is deterministic, testable and upgradable. A file the model writes from prose is none of these, and it leaves nothing for `cruft update` to compare against later.

### II. Scripts for Predictable Steps, the Model for Judgment

- Generation, linking, checking and auditing MUST run through scripts or the underlying CLIs (cookiecutter, cruft, specify, git), invoked with explicit, logged arguments.
- The model is reserved for steps that need judgment: interviewing the user for template answers, inferring answers for unlinked projects, resolving `cruft update` conflicts and `.rej` files, and explaining audit findings.
- Every script that creates or changes files MUST support a dry-run mode that prints what it would do. Read-only scripts (checks, audits) need none.

Rationale: the same inputs must always produce the same project; the model's value is in the cases a script can't decide.

### III. Show Before Changing

- Commands that modify an existing project (upgrade, link, fix) MUST show the user a diff or a list of planned changes and get confirmation before writing.
- Existing files MUST NOT be overwritten without confirmation. Audits are read-only by default.
- Work MUST start from a clean git working tree, or the user MUST explicitly accept the risk, so every change can be reverted.
- Exception: a review command MAY apply its own findings to the working tree without a further confirmation when the user passed an explicit flag requesting it (`--fix`), provided nothing is staged or committed and every change is reported. Passing the flag is the user's explicit acceptance of the risk of writing to a working tree that has uncommitted changes; the command does not require a clean working tree.

Rationale: these commands run on real projects with uncommitted work and local customizations.

### IV. Works Wherever It Is Installed

- Skills MUST work in claude.ai chat, Cowork and Claude Code, provided the environment has a shell with the required CLIs; a skill MUST check for those tools and say clearly what is missing instead of failing partway.
- Components that only run in some environments (hooks, agents) MUST be optional: no core workflow may depend on them.
- Tool versions the plugin installs or calls (spec-kit, cruft, cookiecutter) MUST be pinned, and the pins updated deliberately. The pin rule applies to tools the plugin installs. User-installed clients that the plugin detects and calls (`git`, `gh`, `glab`) are checked for presence and, where a command requires it, a minimum version; they are not pinned.

Rationale: the plugin is installed per account and syncs to every surface, and colleagues will use it in environments the author doesn't control.

## Scope and Constraints

- In scope: creating projects (Python and Node), setting up spec-kit in them, enforcing lint/format standards (ruff for Python, Biome for Node, the pre-commit framework for both), keeping a Keep a Changelog 1.1.0 `CHANGELOG.md`, auditing projects for drift, upgrading projects via cruft, and maintenance workflows: cutting releases, splitting work into stacked pull requests, and writing and reviewing documentation.
- Out of scope: hosting projects, managing secrets, and changing GitHub settings without an explicit request.
- Publishing is limited to a release the user has explicitly confirmed. Package registry uploads MUST be left to the project's own CI unless the user asks otherwise.
- Deferred to v2: automated evals for each skill.
- The repository keeps spec-kit's development files (`.specify/`, root `.claude/skills/speckit-*`) separate from the plugins. Each plugin lives under `plugins/<name>/`.
- `sci-review` scope: scientific-correctness review of code (mathematical derivations, numerical stability, physical modelling and units, statistical integrity, algorithmic correctness), read-only on the reviewed project, except when the user passes `--fix`, which applies the delivered findings to the working tree after the report, on Claude and on Codex. Style, lint and documentation reviews are out of its scope.
- Principle I does not apply to `sci-review`, which generates no project files. Principles II to IV apply to it in full.
- License: MIT.

## Development Workflow

- Each feature goes through spec-kit: specify, plan, tasks, implement. One spec per feature.
- Every user-facing change gets an entry under `## [Unreleased]` in this repository's `CHANGELOG.md`.
- `claude plugin validate` MUST pass on the marketplace and the plugin before merging.
- Releases are tagged with semantic versions, and the plugin's `version` in `plugin.json` matches the tag. `project-kit` releases use tags `vX.Y.Z`; every other plugin uses a per-plugin tag `<name>-vX.Y.Z` (for example `sci-review-vX.Y.Z`).
- `claude plugin validate` MUST pass on every plugin listed in the marketplace.

## Governance

- This constitution overrides other practices in this repository. Specs and plans MUST include a check against each principle and justify any exception in writing.
- Amendments are made by pull request, state their reason, and bump the version: MAJOR for removing or redefining a principle, MINOR for adding one, PATCH for clarifications.

**Version**: 1.3.0 | **Ratified**: 2026-10-30 | **Last Amended**: 2026-11-04
