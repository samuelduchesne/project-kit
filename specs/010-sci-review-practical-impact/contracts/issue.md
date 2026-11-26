# Contract: `panel.py issue`

## Synopsis

```
panel.py issue --run RUN --finding Fn [--dry-run]
```

- `--finding` names a delivered finding or design question in `report.json`. An id that was withheld by the finding cap, rejected or unknown is a usage error (exit 2). The error message lists the delivered ids.
- Requires `report.json` in the run directory (run `panel.py report` first). The command fails with a precondition error (exit 3) if it is missing.
- Writes `<run>/issues/<Fn>.md` and prints the same text to standard output. With `--dry-run`, it prints the text and the path it would write, and writes nothing.
- Never writes to the reviewed project, and never calls a host API or posts anything.
- Runs `git` read-only (`blame`, `show`, `rev-parse`) against the project and the scope's head.

## Body layout

Sections appear in this order. A missing field (a run from an earlier version) prints "Not recorded by this review."

```markdown
# <headline>                       ← design question: "Confirm intended behaviour: <headline>"

## Situation

<context>

## Who hits this and when

<in_practice>

Trigger: <trigger class in words, e.g. "a release of new code">. <reach, first two sentences>

## Bug or design question

Defect, <severity>[, lowered from high because its only trigger is <class in words>].
— or —
Possibly intended: <possibly_intended_reason>. If it is not intended: <wrong_output>.
Please confirm which behaviour is wanted.

## Where

`<file>:<line_start>-<line_end>` at `<head short sha>`

## Reproduction

<trigger>
<for each value correction: "Note: the finding quoted `<quoted>`; `<file>:<line>` has `<actual>`.">

Result: <wrong_output>

## Proposed fix

<fix>

## Suggested owners

<owners with source; see below>

---

<sub>Found by a <level> sci-review (<label>; raised by <raised_by>; <n> verifiers) on `<head short sha>`.</sub>
```

Rules:

1. A value correction is shown next to the trigger. The trigger text itself is not rewritten, because the review's own words are kept.
2. For a contested finding, the "Bug or design question" section also gives `argument_for`, `argument_against` and the deciding assumption, each in one sentence.
3. Class in words: `user-action` → "a user action", `data-condition` → "a data condition in ordinary inputs", `release` → "a release of new code", `operator-change` → "an operator changing configuration".

## Suggested owners

| Source | Output |
|--------|--------|
| `codeowners` | `From <ownership file>: <owner>, <owner>` (as written, teams included) |
| `blame` | `From the history of these lines: <author> (<n> of <m> lines, last <date>), ...`, up to three; plus `History is truncated (shallow clone); older authors may be missing.` when boundary commits were seen |
| `none` | `No owners found: <reason>` (no ownership file and git unavailable, or the file has no history at the head) |

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Written (or printed with `--dry-run`). |
| 2 | Usage: unknown, withheld or rejected finding id. |
| 3 | Precondition: no `report.json`. |
