# Quickstart: Validate the Marketplace and Plugin Skeleton

Runnable checks that prove the feature works. Contracts: [install-interface.md](./contracts/install-interface.md), [manifests.md](./contracts/manifests.md).

## Prerequisites

- Claude Code `2.1.314` (`npm install -g @anthropic-ai/claude-code@2.1.314`)
- A clone of `samuelduchesne/project-kit`

## 1. Validate locally (US3)

```bash
claude plugin validate . --strict
claude plugin validate ./plugins/project-kit --strict
```

Expected: both print `Validation passed` and exit 0.

## 2. Negative checks (SC-005)

Run each, confirm the matching validator run exits non-zero, then `git checkout .`:

| Break | Command that must fail |
|-------|------------------------|
| Change the entry `name` in marketplace.json to `project-kit-x` | `python3 .github/scripts/check_manifests.py` |
| Change `source` to `./plugins/missing` | `python3 .github/scripts/check_manifests.py`, and the install smoke test (step 3) |
| Add a trailing comma to plugin.json | `claude plugin validate ./plugins/project-kit --strict` |
| Add `"version": "0.1.0"` to the marketplace entry | `claude plugin validate . --strict` (warning → failure) |
| Remove `description` from marketplace.json | `claude plugin validate . --strict` |

Note: `claude plugin validate` passes a missing source directory and doesn't compare the entry name with the manifest name, so CI adds a small consistency script and a local install smoke test (step 3) to cover them.

## 3. Local install smoke test (US1, SC-002, SC-004)

```bash
export HOME=$(mktemp -d)            # isolated Claude Code state
claude plugin marketplace add ./
claude plugin install project-kit@project-kit
claude plugin list                  # project-kit@project-kit, enabled
claude plugin details project-kit   # Skills (3): audit-project new-project upgrade-project
```

Expected: install succeeds; details list exactly the three skills and nothing else (no speckit skills).

## 4. Remote install (US1, SC-001) — manual, after merge to main

- Claude Code: `claude plugin marketplace add samuelduchesne/project-kit && claude plugin install project-kit@project-kit`
- claude.ai: Customize > Plugins > Add > Add marketplace → `samuelduchesne/project-kit` → add project-kit.

## 5. Stub behavior (US2, SC-003) — manual

In a session with the plugin installed, inside a scratch git repo:

1. Run `/project-kit:new-project`, `/project-kit:upgrade-project`, `/project-kit:audit-project`.
2. Ask "create a new Node project for me".

Expected each time: purpose + "not implemented yet"; `git status` shows no changes.
