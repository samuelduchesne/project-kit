# Contract: Install Interface

What users and Claude rely on from this repository. Breaking any line here is a breaking change for installed users.

## Identifiers

| Identifier | Value | Stability |
|------------|-------|-----------|
| Marketplace source | `samuelduchesne/project-kit` (GitHub) | Stable while the repo stays at this location |
| Marketplace name | `project-kit` | Stable; changing it changes every install id |
| Plugin install id | `project-kit@project-kit` | Stable |
| Synced id (from claude.ai) | `project-kit@synced` | Platform-assigned |
| Skill names | `project-kit:new-project`, `project-kit:upgrade-project`, `project-kit:audit-project` | Stable; later specs replace bodies, never names |

## Install commands

Claude Code (shell):

```bash
claude plugin marketplace add samuelduchesne/project-kit
claude plugin install project-kit@project-kit
```

Claude Code (session): `/plugin marketplace add samuelduchesne/project-kit`, then `/plugin install project-kit@project-kit`.

claude.ai / desktop app: Customize > Plugins > Add > Add marketplace → `samuelduchesne/project-kit` → add **project-kit**.

## Stub behavior contract

When any stub skill is invoked, explicitly or by a matching plain-language request, Claude:

1. States the workflow's purpose in one or two sentences.
2. States that it is not implemented yet in this version of project-kit.
3. Runs no commands and creates, edits or deletes no files.
4. May point to the repository for status, and may offer to help with the task by other means only if the user asks.
