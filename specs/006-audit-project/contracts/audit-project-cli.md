# Contract: `audit_project.py`

Invocation: `uv run --no-project "${CLAUDE_PLUGIN_ROOT}/scripts/audit_project.py" [--project DIR] [--template URL_OR_PATH] [--ref BRANCH] [--offline]`

Read-only. Exit 0 when the audit ran (whatever it found), 3 when it could not run at all (the folder doesn't exist), 5 for internal errors.

```json
{"status": "ok", "project_dir": "…", "language": "python", "linked": true,
 "template": {"commit": "<sha>", "latest_commit": "<sha>", "behind": 2},
 "summary": {"error": 0, "warning": 1, "info": 1},
 "findings": [
   {"id": "template-behind", "severity": "warning", "message": "2 template commits behind (abc1234 → def5678).", "fix": "upgrade-project"},
   {"id": "template-drift", "severity": "info", "message": "3 files differ from the template: README.md, …", "fix": "Review; keep intentional changes. upgrade-project shows them during updates.", "files": ["README.md"]}
 ],
 "skipped": [{"check": "template", "reason": "offline"}],
 "passed": ["git-repository", "git-clean", "pre-commit", "linter", "changelog", "speckit"]}
```

| id | severity | when |
|----|----------|------|
| `not-git` | error | not a git repository |
| `git-dirty` | warning | uncommitted changes |
| `language-unknown` | warning | neither `pyproject.toml` nor `package.json` |
| `not-linked` | warning | no `.cruft.json` |
| `template-foreign` | warning | `.cruft.json` names another template |
| `template-behind` | warning | template folder changed since the recorded commit |
| `template-drift` | info | files differ from the template at the recorded commit |
| `pre-commit-missing` | error | no `.pre-commit-config.yaml` |
| `linter-missing` | error | pre-commit config lacks ruff (Python) / biome (Node), or Node project lacks `biome.json` |
| `changelog-missing` | error | no `CHANGELOG.md` |
| `changelog-format` | warning | no Keep a Changelog reference or no `## [Unreleased]` |
| `speckit-missing` | warning | no `.specify/` |
| `speckit-outdated` | warning | `speckit_version` below the plugin's pin |
