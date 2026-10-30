# Research: Marketplace and Plugin Skeleton

**Feature**: 001-plugin-skeleton | **Date**: 2026-10-30

Sources: Claude Code docs — [Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces), [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference.md), [Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference), [Plugin commands reference](https://code.claude.com/docs/en/plugins/cli-reference.md), [Plugin loading reference](https://code.claude.com/docs/en/plugins/loading.md), [Skills](https://code.claude.com/docs/en/skills); claude.com docs — [Plugins](https://claude.com/docs/plugins/overview).

## R1. Marketplace file location and required fields

- **Decision**: `.claude-plugin/marketplace.json` at the repository root with `name`, `owner.name`, `description` and one `plugins` entry `{ name, source, description }`. Marketplace name `project-kit`.
- **Rationale**: `name`, `owner` and `plugins` are required; `validate` warns when `description` is missing, which would fail a `--strict` run. `project-kit` is not a reserved name (reserved: official/community names, `claude-*`/`claudeai-*` patterns, `inline`, `skills-dir`, `synced`, `npm`, `github`, …).
- **Alternatives considered**: marketplace named `samuelduchesne` (better if more plugins are added later) — kept the spec's assumption; renaming later is possible but changes every user's install id, so it is flagged to the user at the end.

## R2. Plugin location and what gets installed

- **Decision**: plugin at `plugins/project-kit/` with a relative source `./plugins/project-kit`.
- **Rationale**: for every marketplace plugin except local-path ones, Claude Code copies only the plugin directory into `cache/<marketplace>/<plugin>/<version>/`; "Files outside the plugin directory aren't copied". So `.specify/`, root `.claude/skills/speckit-*`, `specs/` and `.github/` are never installed (FR-008). A root-level plugin (`"source": "."`) would package the whole repository, spec-kit files included.
- **Alternatives considered**: `git-subdir` source pointing at the same repo — unnecessary indirection; `metadata.pluginRoot` with a bare name — requires Claude Code ≥ 2.1.239 for no benefit.

## R3. Plugin manifest and versioning

- **Decision**: `plugins/project-kit/.claude-plugin/plugin.json` with `name: "project-kit"`, `version: "0.1.0"`, `description`, `author { name, url }`, `homepage`, `repository`, `license: "MIT"`, `keywords`. Set `version` only in `plugin.json`, never in the marketplace entry.
- **Rationale**: the manifest `name` namespaces skills (`project-kit:new-project`) and must equal the entry name (FR-003). A pinned `version` keeps users on that version until it changes, which matches the constitution's release rule (tag = `plugin.json` version). The docs say setting `version` in both places triggers a validator warning; validator 2.1.314 does not flag it, so the consistency script enforces it.
- **Alternatives considered**: no `version` (users track every commit SHA) — rejected because the constitution ties releases to tags; `homepage` omitted — but it must parse as a URL, so the GitHub URL is safe.

## R4. Stub skill format

- **Decision**: three skills at `plugins/project-kit/skills/<name>/SKILL.md` (`new-project`, `upgrade-project`, `audit-project`), each with frontmatter `name` and `description`. The description starts with "Placeholder (not yet implemented):" followed by the workflow's purpose. Model invocation stays enabled. The body tells Claude to state the purpose and status, and not to run commands, edit files, or improvise the workflow.
- **Rationale**: skills are namespaced `/plugin-name:skill-name` and work in chat, Cowork and Claude Code; commands are the older form ("Prefer `skills/` for new plugins"). Leaving model invocation on means a plain-language request ("create a new project") routes to the stub, which then says it is planned — satisfying FR-007 / US2 scenario 3. With `disable-model-invocation: true`, Claude would not see the stub and might improvise.
- **Alternatives considered**: `commands/*.md` — legacy; `disable-model-invocation: true` — rejected as above.

## R5. Validation in CI

- **Decision**: GitHub Actions workflow on `pull_request` and `push` to `main`: install `@anthropic-ai/claude-code` pinned to `2.1.314` with npm, then run `claude plugin validate . --strict` and `claude plugin validate ./plugins/project-kit --strict`.
- **Rationale**: validating the marketplace directory does not open the plugins' skill files ("From a marketplace directory, Claude Code doesn't open the plugins' skill, agent, command, or hook files"), so the plugin directory needs its own run. `--strict` turns warnings (missing description, version in two places, unknown fields) into failures. Verified locally that `validate` runs with no sign-in and an empty `HOME` (exit 0), so CI needs no secrets. Exit codes: 0 pass, 1 fail, 2 validator error. Pinning follows constitution principle IV.
- **Gap and fix**: per the docs, `validate` passes a relative `source` whose directory doesn't exist (it fails only at install) and does not compare the entry name with the manifest name. CI therefore also runs (a) a stdlib-only Python script, `.github/scripts/check_manifests.py`, that checks entry name == manifest name, the source directory exists, the entry sets no `version`, and the plugin directory holds no forbidden files (`bin/`, `CLAUDE.md`, hooks, agents, MCP); and (b) an install smoke test into a temporary `HOME` that confirms the plugin installs and exposes exactly the three skills.
- **Alternatives considered**: JSON-schema validation with a generic tool — doesn't check name matching, reserved names or path resolution; unpinned `latest` — breaks reproducibility.

## R6. Surfaces and organization controls

- **Decision**: README documents (a) claude.ai / desktop: Customize > Plugins > Add > Add marketplace, enter `samuelduchesne/project-kit`, then Check for updates or Sync automatically; (b) Claude Code: `claude plugin marketplace add samuelduchesne/project-kit` then `claude plugin install project-kit@project-kit`, update with `claude plugin update project-kit@project-kit` or `/plugin` > Marketplaces > Update marketplace. Note that on Team/Enterprise an Owner controls whether members can add marketplaces.
- **Rationale**: matches the documented flows on both surfaces; plugins added on claude.ai also sync into Claude Code as `project-kit@synced`.
- **Alternatives considered**: none.

## R7. Things to avoid in the plugin directory

- **Decision**: no `bin/`, no `CLAUDE.md`, no hooks/agents/MCP in the plugin.
- **Rationale**: claude.ai and Cowork refuse to install a plugin with a top-level `bin/`; a `CLAUDE.md` at the plugin root is not loaded and triggers a validator warning (fails `--strict`); hooks/agents/connectors are out of scope (FR-013).
