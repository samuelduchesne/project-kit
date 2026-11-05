# Data Model: Code-review-style arguments for sci-review

Entities are frozen dataclasses in `panel.py`, serialised as JSON in the run directory, consistent with feature 007 ([data-model.md](../007-sci-review-plugin/data-model.md)). New and changed entities only.

## 1. InvocationArguments (`$RUN/arguments.json`)

Produced by `panel.py args`.

| Field | Type | Rule |
|-------|------|------|
| `level` | `low` \| `medium` \| `high` \| `xhigh` \| `max` | Resolved level |
| `level_source` | `given` \| `reused` \| `default` | `given` when typed; `reused` from preferences; `default` is `medium` (FR-007) |
| `target_text` | str or null | The target tokens as typed, unresolved; null means the current branch (feature 007 default). Resolved into a `Target` by `panel.py scope`, which writes it to `scope.json` (section 6) |
| `near_level` | str or null | A token that begins with the first three letters of a level but is not one (for example `hig`); `scope` treats it as the target when it is an existing branch or path, and otherwise exits 2 with a usage error (FR-003) |
| `comment` | bool | `--comment` present |
| `fix` | bool | `--fix` present |
| `max_findings` | int >= 1 \| `all` \| null | Resolved cap; null means the level's default |
| `max_findings_source` | `given` \| `reused` \| `default` | As for the level |
| `notes` | list of str | One-line notes to show the user: ignored `--max-findings` value (FR-003a), reused preference, unavailable preferences (FR-018) |
| `raw` | str | The argument text as received, for the log |

Validation (exit code 2, usage error, nothing written): unknown `--flag`; more than one level token; `ultra`. Not errors: malformed `--max-findings` (ignored, note added), `--comment` without a pull request target (resolved later, note added at delivery).

## 2. Target

| Field | Type | Rule |
|-------|------|------|
| `kind` | `pull-request` \| `branch` \| `paths` | |
| `host` | `github` \| `gitlab` \| null | For `pull-request` |
| `number` | int or null | Pull or merge request number |
| `ref` | str or null | Branch name for `branch` |
| `paths` | list of str | For `paths`; each inside the project root |
| `text` | str | The token(s) as typed |

A token matching several kinds is not resolved: `scope` exits 3 with the candidates (FR-010).

## 3. UserPreferences (`preferences.json`, outside the project)

| Field | Type | Rule |
|-------|------|------|
| `version` | int | 1 |
| `last_level` | level or absent | Written when a level is typed with `--persist` |
| `last_max_findings` | int >= 1 \| `all` or absent | Written for `<n>` or `all`; removed by `default` |

Written atomically (temporary file then rename). A missing or unreadable file is treated as empty, with a note.

## 4. LevelProfile (constant table in `panel.py`)

| Field | Type |
|-------|------|
| `level` | level |
| `perspectives` | list of perspective ids, or `defaults+extensions`, or `all` |
| `max_perspectives` | int (2 to 7) |
| `rebuttal_rounds` | int (0 to 3) |
| `max_batches` | int (1 to 4) |
| `default_cap` | int or null | null means unbounded; null for every level (research R6) |

Values: research R6. Invariant tested: no field decreases from `low` to `max`; `medium` equals feature 007's defaults.

## 5. Panel (`$RUN/panel.json`, extended)

New fields: `level`, `level_source`, `overrides` (list of parameters overridden by explicit words in the request, FR-009), `parts` (int). The finding cap is not recorded here: `arguments.json` holds the resolved cap and `report.json` the cap applied.

## 6. ReviewScope (`$RUN/scope.json`, changed)

Removed: the `over budget` exclusion reason and the budget sentence of `note`. Added: `target` (`Target` or null), `total_lines` (int), `pull_request_ref` (temporary git ref or null, deleted by `clean`).

## 7. ReviewPart (`$RUN/parts.json`)

| Field | Type | Rule |
|-------|------|------|
| `id` | str | `p1`, `p2`, ... in path order |
| `files` | list of `ScopedFile` | With `line_ranges` narrowed when a file is split |
| `lines` | int | At most 2,000 unless a single indivisible definition is larger |
| `status` | `pending` \| `reviewed` \| `incomplete` | `pending` when written by `parts`. Derived by `panel.py report`, identically on every runner: `reviewed` when the candidate file of every panel perspective for this part exists and validates, `incomplete` otherwise. `incomplete` parts are listed as not reviewed (FR-023) |

`parts.json` also records `threshold` (6,000), `total_lines` and `confirm_required` (bool, `total_lines > threshold`).

Candidate-findings messages gain `part` (part id); file names become `candidates/<perspective>--<part>.json`.

## 8. FindingOutcome (report, `--fix` only)

| Field | Type | Rule |
|-------|------|------|
| `finding_id` | str | As in the report |
| `outcome` | `fixed` \| `no_change_needed` \| `skipped` | Values of `/code-review` (research R1) |
| `reason` | str | Required for `skipped` |
| `files` | list of str | Files changed for `fixed` |

Outcomes are not written by `panel.py`; the orchestrating conversation passes them to the findings-reporting tool, or states them in the reply. The agreement label of a finding never changes.

## 9. Report (`$RUN/report.json`, extended)

New fields: `level`, `level_source`, `max_findings`, `withheld` (int, findings beyond the cap), `parts` (int), `notes` (from `arguments.json`). The `report_findings` array is truncated to the cap, and to 32 when delivered through the findings-reporting tool (research R3).
