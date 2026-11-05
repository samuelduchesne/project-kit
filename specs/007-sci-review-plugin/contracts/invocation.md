# Contract: invocation and runner selection

## 1. Skill

- Claude: `sci-review:scientific-review`; Codex: `scientific-review` from the `sci-review` plugin.
- Triggers: requests to review code for mathematical, numerical, physical, statistical or algorithmic correctness ("scientific review", "check the maths", "is this numerically stable", "check for data leakage").
- Not triggered by style, lint or documentation reviews.

## 2. Arguments (read from the request, all optional)

> Feature 008 adds explicit arguments (an effort level, a pull request, branch or paths target, `--comment`, `--fix` and `--max-findings`), specified in [008 contracts/arguments.md](../../008-sci-review-arguments/contracts/arguments.md) and [008 contracts/targets-and-parts.md](../../008-sci-review-arguments/contracts/targets-and-parts.md). The natural-language arguments below remain valid where no explicit argument covers them; the defaults of `rebuttal_rounds`, `max_batches` and `perspectives` are those of the `medium` level.

| Argument | Type | Default | Limits |
|----------|------|---------|--------|
| `mode` | `branch` \| `repository` \| `paths` | `branch` | |
| `baseline` | git ref or range | resolved per research R12 | with `mode` `branch` only; the scope is then recorded as `explicit` |
| `paths` | list of paths | none | required when `mode` is `paths` |
| `perspectives` | list of perspective ids | the five defaults plus selected extensions | 2 to 7 in total; ids are chosen from the defaults and selected extensions, so more than are available yields all of them |
| `rebuttal_rounds` | int | 2 | 0 to 3 |
| `max_batches` | int | 2 | 1 to 4 |
| `models` | map of role id to model | none | Workflow runner only |

Out-of-range values are clamped and the report states the panel actually used.

## 3. Runner selection

The skill selects the first available runner, in this order, and records it in the report:

| Order | Runner | Condition | Independence |
|-------|--------|-----------|--------------|
| 1 | `claude-workflow` | The `Workflow` tool is available and `sci-review:scientific-review` is listed as a workflow | independent agents |
| 2 | `codex-subagents` | Running in Codex with multi-agent tools enabled | independent agents |
| 3 | `claude-agents` | The `Agent` tool is available with the `sci-review:scientific-auditor` agent | independent agents |
| 4 | `sequential` | Otherwise | not independent; notice required (FR-028) |

The user may force a lower runner ("run it without agents"). A user request for the review satisfies the Workflow opt-in requirement; a review the model starts on its own initiative asks first, because it spawns many agents.

## 4. Workflow arguments (`claude-workflow`)

```json
{
  "scope": { "...": "ReviewScope as produced by panel.py scope" },
  "extensions": [ { "...": "selected DomainExtension declarations with absolute brief and reference paths" } ],
  "project": "/absolute/path/of/the/reviewed/project",
  "skill_dir": "/absolute/path/of/skills/scientific-review",
  "perspectives": [ { "id": "theorist", "name": "Theorist", "brief_path": "...", "reference_paths": [] } ],
  "rebuttal_rounds": 2,
  "max_batches": 2,
  "models": {}
}
```

`perspectives` is the `panel.perspectives` array of `panel.json` (bare ids are also accepted); default perspectives use the briefs embedded in the script, and domain perspectives read their brief and reference files from the given absolute paths. `project` is the root against which the scope's relative paths resolve; the script states it in every prompt, because agents do not necessarily start in the reviewed project. `skill_dir` lets agents read the dimension documents on demand; without it, the script embeds them in each independent-round prompt. Scope resolution and extension selection run in the orchestrating conversation before launch, because extension discovery needs the host's skill listing (research R9). The workflow returns a `PanelRun` object holding every panel message (candidates, merge rulings, positions per batch and round, moderator notes). The conversation writes it to `$RUN/workflow-result.json`, runs `panel.py ingest`, `adjudicate` and `report`, so labels and the report are computed by `panel.py` on every runner.

## 5. Preconditions checked at start

- `git` present when `mode` is `branch`; otherwise offer `repository` or `paths`.
- `python3` present; if absent, the skill applies the written rules in `protocol.md` for each `panel.py` step and adds a notice.
- No base determinable: ask the user; never fall back to `repository` silently.
