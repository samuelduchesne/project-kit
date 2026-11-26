# Data model: Findings that say who hits them

Changes to the records of `plugins/sci-review/scripts/panel.py` and their JSON schemas under `skills/scientific-review/schemas/`. The records not listed here are unchanged. "Optional" means optional in the dataclass (`_optional`, default null) so that earlier runs load (research R10); the schemas for new messages mark the field required unless stated.

## Enumerations

- **TriggerClass**: `user-action`, `data-condition`, `release`, `operator-change`, `unreachable`. Frequency order for ties: `user-action`, `data-condition`, `release`, `operator-change` (research R3).
- **FindingKind**: `defect`, `design-question`.
- **OwnerSource**: `codeowners`, `blame`, `none`.

## CandidateFinding (`candidate-findings.schema.json`)

| Field | Type | Rule |
|-------|------|------|
| `headline` | string, 1 to 90 characters | Plain words; names the situation, not the code. |
| `context` | string, non-empty | One or two sentences: what the code does for its users and when the problem arises. |
| `in_practice` | string, non-empty | Who or what triggers it, how often, whether anyone would notice; for a cache, whether reuse looks intended. |

## MergedFinding (`merge-ruling.schema.json`)

Gains `headline`, `context` and `in_practice`. The moderator chooses or combines them from the members and MUST NOT add a claim that no member made. The automatic merge copies them from the single member.

## VerdictRecord (`verification.schema.json`)

| Field | Type | Rule |
|-------|------|------|
| `reach` | string, non-empty | Files read to establish how the trigger state arises (configuration, environment, deployment, release) and what each showed; "none present" when the project has none. |
| `trigger_class` | TriggerClass | `unreachable` only with verdict `refute`. |
| `possibly_intended` | boolean, default false | Not allowed with `refute`. |
| `possibly_intended_reason` | string or null | Required and non-empty when `possibly_intended` is true; null otherwise. |
| `value_corrections` | array of ValueCorrection, may be empty | One entry per quoted value that the repository contradicts. |
| `reproduction` | string or null | The code or command run and its observed output; required when `evidence` is `reproduced`. |
| `extent` | array of ExtentRow, may be empty | A few runs, input by input, including ordinary inputs. |
| `in_practice_revision` | string or null | A replacement in-practice statement when reach contradicts or omits part of the finding's (research R14). |

### ExtentRow

| Field | Type |
|-------|------|
| `input` | string, non-empty |
| `expected` | string, non-empty |
| `actual` | string, non-empty |

`VerdictRecord.effective` returns `uncertain` for a verdict marked possibly intended, as it already does for a `confirm` with evidence `none`.

### ValueCorrection

| Field | Type |
|-------|------|
| `quoted` | string: the value as the finding quotes it, for example `SEARCH_GENERATIONS=5` |
| `actual` | string: the value in the repository, for example `SEARCH_GENERATIONS=10` |
| `file` | string |
| `line` | integer, at least 1 |

## Position (`debate-positions.schema.json`, debate protocol only)

Gains optional `possibly_intended` and `possibly_intended_reason` with the same rules, for the defender only. `panel.py validate` rejects the mark from other members.

## Finding (`report.schema.json`, `adjudication.json`)

| Field | Type | Source |
|-------|------|--------|
| `headline`, `context`, `in_practice` | string, optional | The merged finding. |
| `kind` | FindingKind, default `defect` | Rule 2a of protocol.md section 5.1 (research R6). |
| `trigger_class` | TriggerClass or null, optional | The combination of research R3; null in the debate protocol. |
| `reach` | string or null, optional | The `reach` of the first non-refuting verdict that recorded the reported class. |
| `possibly_intended_reason` | string or null, optional | The first recorded reason; set when `kind` is `design-question`. |
| `value_corrections` | array of ValueCorrection, optional | The union over verdicts, deduplicated on (`quoted`, `file`, `line`). |
| `reproduction` | string or null, optional | The first non-refuting verdict's, preferring a reproduced one (research R13). |
| `extent` | array of ExtentRow, optional | The same verdict's table, or the first non-refuting one recorded. |
| `in_practice_original` | string or null, optional | The finder's statement, kept when a verifier revised it; `in_practice` then holds the revision. |

The severity is the merged finding's; adjudication never changes it (research R5).

## ReviewReport (`report.schema.json`)

Gains `design_questions`, an array of Finding with `kind: design-question`. `findings` then holds only findings with `kind: defect`. The `max_findings` cap counts both lists together, design questions after defects.

## IssueDraft (no schema; markdown in the run directory)

Written by `panel.py issue` to `<run>/issues/<finding id>.md`. Layout in [contracts/issue.md](./contracts/issue.md). Its owner section records an OwnerSource and up to three owners. For `blame`, each owner has a line count and the date of their most recent commit to the lines.

## Validation rules added to `panel.py validate`

1. A verdict with `trigger_class: unreachable` has `verdict: refute`.
2. A verdict with `possibly_intended: true` has a non-refute verdict and a non-empty reason.
3. A `value_corrections` entry's `line` is at least 1. Its file is not required to exist: the verifier may cite a file outside the scope.
4. `headline` is at most 90 characters.
5. A verdict with `evidence: reproduced` has a non-empty `reproduction`.

## State transitions

Adjudication of a verify-protocol finding follows the rules of protocol.md section 5.1. The new rule 2a and the evidence are applied in this order:

```
verdicts ──► 1 not verified? ──► contested + notice
         ──► 2 refuted?      ──► rejected
         ──► 2a any possibly-intended mark? ──► kind = design-question; marks count as uncertain
         ──► 3..6 label rules (unchanged)
         ──► trigger class combined (R3)
         ──► evidence: reproduction and extent of the first non-refuting verdict, preferring a reproduced one
```
