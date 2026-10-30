# project-kit

project-kit is a Claude plugin for setting up and maintaining software projects to a consistent standard. It drives the [cookiecutter-gi](https://github.com/samuelduchesne/cookiecutter-gi) templates (Python today, with a Node template planned) rather than writing project files itself: the templates hold the files, and project-kit handles creating projects from them, keeping projects up to date with cruft, and checking projects for drift. New projects come with [spec-kit](https://github.com/github/spec-kit), the standard linting and formatting rules (ruff for Python, Biome for Node, pre-commit for both) and a [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) `CHANGELOG.md`.

The plugin works in claude.ai chat, the Claude desktop app, Cowork and Claude Code.

## Workflows

| Skill | What it will do | Status |
|-------|-----------------|--------|
| `/project-kit:new-project` | Create a new Python or Node project from the cookiecutter-gi templates, with spec-kit, linting and a changelog set up | Planned |
| `/project-kit:upgrade-project` | Bring an existing project up to the latest template, linking it to the template first if needed | Planned |
| `/project-kit:audit-project` | Check a project against the standards and report drift without changing anything | Planned |
| `/project-kit:changelog-keeper` | Create a `CHANGELOG.md` from git history, or audit and fix an existing one, following Keep a Changelog 1.1.0 | Available |
| `/project-kit:create-release` | Cut a Python or Node release: bump the version, update the changelog, draft release notes and create the GitHub release | Available |
| `/project-kit:stacked-prs` | Split uncommitted changes into stacked pull requests and merge them in dependency order | Available |
| `/project-kit:diataxis` | Write, place and reorganize documentation using the Diátaxis framework | Available |
| `/project-kit:editorial` | Apply the house writing style, after Jean-Luc Doumont's *Trees, maps and theorems* | Available |
| `/project-kit:review-docs` | Review documentation against a scoped code diff and report misalignments (requires a saved `review-docs` workflow in `~/.claude/workflows/`, which the plugin does not ship) | Available |

Skills marked Planned are placeholders: each explains what the workflow will do and that it isn't available yet, and it changes nothing.

The plugin also includes the `editor` agent, which writes and revises prose to the `editorial` standard. `diataxis` and `review-docs` delegate prose work to it. Agents are not available on every surface; where it is unavailable, apply the `editorial` skill directly.

## Install

project-kit is published as a plugin marketplace from this repository. Add the marketplace once, then install the `project-kit` plugin from it.

### claude.ai and the Claude desktop app

1. Go to **Customize > Plugins**.
2. Select **Add > Add marketplace** and enter `samuelduchesne/project-kit`.
3. Find **project-kit** in the list and select **Add**.

The plugin is saved to your account, so it is also available in Cowork and in Claude Code (where it appears as `project-kit@synced`). To get new versions, open the marketplace and select **Check for updates**, or turn on **Sync automatically**.

On Team and Enterprise plans, an organization Owner decides whether members can add their own marketplaces. If **Add marketplace** is missing, ask an Owner to allow it or to add project-kit for the organization.

### Claude Code

From your shell:

```bash
claude plugin marketplace add samuelduchesne/project-kit
claude plugin install project-kit@project-kit
```

Or inside a session:

```text
/plugin marketplace add samuelduchesne/project-kit
/plugin install project-kit@project-kit
```

To update, run `claude plugin update project-kit@project-kit`, or open `/plugin`, go to **Marketplaces**, select project-kit and choose **Update marketplace**.

## Development

```text
.claude-plugin/marketplace.json   marketplace definition
plugins/project-kit/              the plugin (the only folder that gets installed)
  .claude-plugin/plugin.json
  skills/<name>/SKILL.md
  agents/<name>.md
.github/                          CI workflow and the manifest consistency check
specs/                            spec-kit feature specs, plans and tasks
.specify/, .claude/skills/        spec-kit development files (not packaged)
```

Features are built with spec-kit: each one has a spec, plan and task list under `specs/`, checked against the project constitution in `.specify/memory/constitution.md`.

Validate before opening a pull request (CI runs the same checks):

```bash
claude plugin validate . --strict
claude plugin validate ./plugins/project-kit --strict
python3 .github/scripts/check_manifests.py
```

To try the plugin from your working copy, add the folder as a local marketplace: `claude plugin marketplace add ./`, then `claude plugin install project-kit@project-kit`. Edits load at the next session start or after `/reload-plugins`.

Record user-facing changes under `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE) © 2026 Samuel Letellier-Duchesne
