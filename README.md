# project-kit

project-kit is a Claude plugin for setting up and maintaining software projects to a consistent standard. It drives the [cookiecutter-gi](https://github.com/samuelduchesne/cookiecutter-gi) templates (Python, and Node for TypeScript libraries) rather than writing project files itself: the templates hold the files, and project-kit handles creating projects from them, keeping projects up to date with cruft, and checking projects for drift. New projects come with [spec-kit](https://github.com/github/spec-kit), the standard linting and formatting rules (ruff for Python, Biome for Node, pre-commit for both) and a [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) `CHANGELOG.md`.

The plugin installs in claude.ai chat, the Claude desktop app, Cowork and Claude Code, and each skill needs the tools its workflow calls. `create-release` and `stacked-prs` need a shell with `git` and `gh`. `review-docs` needs the Workflow tool, which is documented for the Claude Code CLI, desktop app and IDE extensions.

## Workflows

| Skill | What it will do | Status |
|-------|-----------------|--------|
| `/project-kit:new-project` | Create a new Python or Node project from the cookiecutter-gi templates, linked to them with cruft, with spec-kit and an initial git commit | Available |
| `/project-kit:upgrade-project` | Bring an existing project up to the latest template, linking it to the template first if needed | Available |
| `/project-kit:audit-project` | Check a project against the standards and report drift without changing anything | Available |
| `/project-kit:changelog-keeper` | Create a `CHANGELOG.md` from git history, or audit and fix an existing one, following Keep a Changelog 1.1.0 | Available |
| `/project-kit:create-release` | Cut a Python or Node release: bump the version, update the changelog, draft release notes and create the GitHub release | Available |
| `/project-kit:stacked-prs` | Split uncommitted changes into stacked pull requests and merge them in dependency order | Available |
| `/project-kit:diataxis` | Write, place and reorganize documentation using the Diátaxis framework | Available |
| `/project-kit:editorial` | Apply the house writing style, after Jean-Luc Doumont's *Trees, maps and theorems* | Available |
| `/project-kit:review-docs` | Review documentation against a scoped code diff and report misalignments | Available |

The plugin also includes the `editor` agent, which writes and revises prose to the `editorial` standard. `diataxis` and `review-docs` delegate prose work to it. Agents are not available on every surface; where it is unavailable, apply the `editorial` skill directly.

### new-project

Ask Claude to create a new Python or Node project, for example "start a new Python project called flow-tools" or "create a TypeScript library called flow-kit". Python projects come from the template at the root of cookiecutter-gi, Node projects (pnpm, TypeScript, Vitest, Biome) from its `node/` folder. Claude asks for the name, description and author, shows the template's other options with their defaults, previews what will be created, and creates nothing until you confirm. The result is a folder with the template's files, a `.cruft.json` link for later upgrades, spec-kit set up for Claude, and one git commit. It does not install dependencies, create a remote repository or push. To work on a Node project afterwards you also need Node.js and pnpm (`npm install -g pnpm`).

### upgrade-project

Ask Claude to upgrade a project, for example "upgrade this project to the latest template". Claude reports how many template changes the project is missing, previews the exact diff (computed by running the update on a copy of the project), applies it only after you confirm, and helps you resolve any conflict with your own edits. It never commits without asking. The project must be a git repository with no uncommitted changes.

A project that was never linked to the template is linked first: Claude proposes the template version that was current when the project's first commit was made, infers the template answers from the project's files, shows how closely the template with those answers matches the project, and links it once you agree. The update then brings in every later template change.

### audit-project

Ask Claude to audit a project, for example "audit this repository against our standards". It reports, without changing anything: whether the project is a clean git repository and linked to the template, how many template changes it is missing, which files differ from the template, whether ruff (Python) or Biome (Node) runs through pre-commit, whether `CHANGELOG.md` follows Keep a Changelog with an `[Unreleased]` section, and whether spec-kit is set up. Each finding names the workflow that fixes it.

### Requirements

new-project, upgrade-project and audit-project need a shell on your own computer (Claude Code, or Cowork running locally) with:

- git and [uv](https://docs.astral.sh/uv/)
- read access to the private [`samuelduchesne/cookiecutter-gi`](https://github.com/samuelduchesne/cookiecutter-gi) repository through your git credentials
- network access to GitHub and PyPI (cruft and spec-kit are run with `uvx`)

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
  scripts/new_project.py          new-project helper (check, options, create)
  scripts/upgrade_project.py      upgrade-project helper (status, link, update)
  scripts/audit_project.py        audit-project helper (read-only)
  skills/<name>/SKILL.md
  agents/<name>.md
  workflows/<name>.js
tests/                            tests for the helper scripts
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
uv run --no-project python -m unittest discover -s tests -v
```

The tests run the helper scripts against small fixture templates, so they don't need access to the private template.

To try the plugin from your working copy, add the folder as a local marketplace: `claude plugin marketplace add ./`, then `claude plugin install project-kit@project-kit`. Edits load at the next session start or after `/reload-plugins`.

Record user-facing changes under `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE) © 2026 Samuel Letellier-Duchesne
