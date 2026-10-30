# Contract: Manifest Shapes

Reference shapes for the two manifests. Values are those in [data-model.md](../data-model.md); the authoritative check is `claude plugin validate --strict`.

## `.claude-plugin/marketplace.json`

```json
{
  "name": "project-kit",
  "description": "<one sentence>",
  "owner": { "name": "Samuel Letellier-Duchesne", "url": "https://github.com/samuelduchesne" },
  "plugins": [
    { "name": "project-kit", "source": "./plugins/project-kit", "description": "<one sentence>" }
  ]
}
```

Must not contain: a `version` on the plugin entry; component fields (`skills`, `commands`, `hooks`, …) on the entry.

## `plugins/project-kit/.claude-plugin/plugin.json`

```json
{
  "name": "project-kit",
  "version": "0.1.0",
  "description": "<one sentence>",
  "author": { "name": "Samuel Letellier-Duchesne", "url": "https://github.com/samuelduchesne" },
  "homepage": "https://github.com/samuelduchesne/project-kit",
  "repository": "https://github.com/samuelduchesne/project-kit",
  "license": "MIT",
  "keywords": ["<tags>"]
}
```

Must not contain: component path keys (the default `skills/` scan is used), `userConfig`, `mcpServers`, `hooks`.

## Validator exit codes (CI contract)

| Code | Meaning | CI result |
|------|---------|-----------|
| 0 | Passed (no warnings under `--strict`) | pass |
| 1 | Failed, or warnings under `--strict` | fail |
| 2 | Validator error (e.g. unreadable path) | fail |
