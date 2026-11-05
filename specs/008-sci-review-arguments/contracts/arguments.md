# Contract: arguments, preferences and level profiles

Supersedes section 2 of [007 contracts/invocation.md](../../007-sci-review-plugin/contracts/invocation.md) for explicit arguments; natural-language arguments of that section remain valid where no explicit argument covers them (FR-004).

## 1. Grammar

```text
/sci-review:scientific-review [low|medium|high|xhigh|max] [<pr#>|<pr-url>|<branch>|<path>...] [--comment] [--fix] [--max-findings <n>|all|default]
```

`SKILL.md` frontmatter:

```yaml
argument-hint: "[low|medium|high|xhigh|max] [<pr#>|<branch>|<path>] [--comment] [--fix] [--max-findings <n>|all|default]"
```

Tokenisation (research R3):

1. Remove `--comment`, `--fix` and `--max-findings[ =]<value>` from any position. The last `--max-findings` wins.
2. Any remaining token starting with `--` is an unknown flag: usage error.
3. A token equal (case-insensitive) to a level is the level; a second one is a usage error; `ultra` is a usage error with the message "`ultra` is not an effort level of the scientific review; use `max`."
4. A token that begins with the first three letters of a level but is not one (for example `hig`) is recorded as `near_level` and kept in the target text. `scope` resolves each target token separately; it treats the near-level token as a target when it is an existing branch or path, and otherwise exits 2, whatever the other target tokens are, with the usage error "`<token>` is not a recognised level: use low, medium, high, xhigh or max." (FR-003).
5. Remaining tokens, with backquotes removed and a leading `#` stripped from the first, are the target text (`target_text` in `arguments.json`; resolved by `scope`).

`--max-findings` values: a whole number above zero, `all`, `default`. Any other value, or a missing value, is ignored with the note: "`--max-findings` was ignored: type a whole number above zero, `all`, or `default` after it." followed by "Using the usual limit." when no cap is persisted.

## 2. `panel.py args`

```text
panel.py args --run RUN (--argv TEXT | --text TEXT | --argv-stdin | --text-stdin) [--persist] [--prefs PATH] [--dry-run]
```

- `--argv`: the command arguments (`$ARGUMENTS` on Claude Code).
- `--text`: the request text on hosts without an argument field (R9); only the grammar's tokens are taken from it, and the rest is left to the natural-language reading of feature 007.
- `--argv-stdin`, `--text-stdin`: the same, read from standard input, with one trailing newline removed. The skill uses these forms, with a quoted here-document, so that no shell parses the user's text.
- `--persist`: store a typed level and `--max-findings` choice. `SKILL.md` passes it only when the user typed the arguments (research R4).
- `--prefs`: preferences path, for tests; default per research R4.

Writes `$RUN/arguments.json` (data-model section 1). Prints its JSON. Exit codes: 0, 2 (usage error, message names the accepted values), 3 never.

## 3. `panel.py prefs`

```text
panel.py prefs [--show | --clear] [--prefs PATH] [--dry-run]
```

Shows or clears the stored preferences. `args --persist` is the only writer during a review.

## 4. Level profiles

`panel.py panel --level LEVEL` applies the profile of research R6 before the existing `--perspectives`, `--rounds`, `--batches` options, which override individual parameters (spec edge case) and are recorded in `panel.json` `overrides`. Clamping is unchanged from feature 007.

| Level | Perspectives | Rounds | Batches | Default cap |
|-------|--------------|--------|---------|-------------|
| `low` | `theorist`, `numerical-analyst`, `methodologist` | 1 | 1 | none |
| `medium` | five defaults plus selected extensions, at most 7 | 2 | 2 | none |
| `high` | as `medium` | 2 | 3 | none |
| `xhigh` | as `medium` | 3 | 4 | none |
| `max` | all defaults and selected extensions, at most 7 | 3 | 4 | none |

"none" means the Markdown report is not capped by default (spec FR-006). Delivery through the findings-reporting tool is clamped to 32 whatever the cap (research R3 step 5).

## 5. Rules in `SKILL.md`

1. The skill description carries the sentence: "Use the max level only when the user, or instructions such as CLAUDE.md or a skill, explicitly ask for it, never on your own judgment: it is the costliest level and starts many reviewer agents." (FR-008, wording from `/code-review`).
2. Notes in `arguments.json` are told to the user in one short line as the review begins.
3. The report states the level and whether it was given, reused or defaulted (FR-009), and the cap and the number of findings withheld (FR-014).
