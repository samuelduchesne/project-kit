# Data Model: sci-review plugin

Entities are implemented as frozen `dataclasses` in `scripts/panel.py` and serialised as JSON panel messages (contracts/panel-messages.md). Enumerations are `enum.StrEnum` (Python 3.11) or string constants validated on load (Python 3.10).

## 1. Enumerations

| Name | Values |
|------|--------|
| `ScopeMode` | `branch`, `explicit`, `repository`, `paths` (`explicit` is recorded when `branch` is given an explicit `--baseline`) |
| `Dimension` | `mathematical-derivations`, `numerical-stability`, `physical-modelling-and-units`, `statistical-integrity`, `algorithmic-correctness` |
| `Severity` | `high`, `medium`, `low` (definitions in FR-018) |
| `Role` | `perspective`, `defender`, `moderator` |
| `Stance` | `accept`, `challenge`, `withdraw` (withdraw only for the raiser) |
| `AgreementLabel` | `consensus`, `majority`, `contested` |
| `Runner` | `claude-workflow`, `codex-subagents`, `claude-agents`, `sequential` |
| `ExtensionStatus` | `selected`, `not-applicable`, `failed`, `recommended` |

## 2. Entities

### ReviewScope

| Field | Type | Rule |
|-------|------|------|
| `mode` | `ScopeMode` | required |
| `base` | `str or None` | required for `branch` and `explicit`; a resolved commit |
| `head` | `str or None` | `HEAD` plus uncommitted work for diff modes |
| `files` | `list[ScopedFile]` | non-empty unless the review ends with "no reviewable scientific code" |
| `excluded` | `list[Exclusion]` | each with `path` and `reason` (generated, vendored, outside paths, over budget) |
| `note` | `str` | one sentence for the report |

`ScopedFile`: `path`, `language` (`python`, `typescript`, `other`), `line_ranges` (list of `[start, end]`, empty in repository mode meaning whole file).

### Perspective

| Field | Type | Rule |
|-------|------|------|
| `id` | `str` | kebab-case, unique in panel |
| `name` | `str` | display name |
| `brief_path` | `str` | path to the role brief |
| `source` | `str` | `sci-review` or the extension id |

### DomainExtension

| Field | Type | Rule |
|-------|------|------|
| `id` | `str` | the skill name, ending in `sci-review-extension` |
| `plugin` | `str` | contributing plugin |
| `contract_version` | `int` | must equal the supported version (1) |
| `perspective` | `Perspective` | required |
| `reference_paths` | `list[str]` | relative to the skill directory |
| `applies_to` | `Applicability` | at least one criterion |
| `checks` | `str or None` | instructions for domain checks (optional) |
| `status` | `ExtensionStatus` | set by selection |
| `status_reason` | `str` | required for `failed`, `not-applicable`, `recommended` |

`Applicability`: `globs` (list), `file_types` (list of extensions), `import_patterns` (list of regular expressions matched against file contents), `languages` (list). A file matches if any glob or file type matches, or if its language is listed and any import pattern matches. Globs and file types are matched case-insensitively, so `**/*.epJSON` and `.epjson` match `model.epjson` and `model.epJSON` alike.

### Panel

| Field | Type | Rule |
|-------|------|------|
| `perspectives` | `list[Perspective]` | 2 to 7 entries, extensions included (FR-026); chosen from the five defaults plus selected domain perspectives, so a request for more than are available yields all of them |
| `rebuttal_rounds` | `int` | 0 to 3, default 2 |
| `max_batches` | `int` | 1 to 4, default 2 |
| `runner` | `Runner` | recorded in the report |
| `independent` | `bool` | false only for `sequential` |
| `models` | `dict[str, str]` | optional, per role id (Workflow runner only) |

Defender and moderator are implicit and always present.

### CandidateFinding (independent-round output)

| Field | Type | Rule |
|-------|------|------|
| `id` | `str` | `<perspective>-<n>` |
| `raised_by` | `str` | perspective id |
| `file`, `line_start`, `line_end` | `str`, `int`, `int` | inside the scope |
| `dimension` | `Dimension` | required |
| `severity` | `Severity` | required |
| `summary` | `str` | one sentence |
| `trigger` | `str or None` | concrete input or state; null makes the finding non-concrete (FR-016) |
| `wrong_output` | `str or None` | the wrong result or behaviour |
| `fix` | `str` | derivation or code change |
| `evidence` | `str` | what was read or computed |

Each perspective's output also carries `checked_items: list[CheckedItem]` (`file`, `line_start`, `line_end`, `dimension`, `note`).

### MergedFinding

A cluster of `CandidateFinding` confirmed as one defect by the moderator. Fields: `id` (`F<n>`), `members` (candidate ids), `raised_by` (union), `batch` (int), and the representative fields of FR-014 chosen by the moderator. Severity is the highest member severity unless the moderator records a reason to lower it.

### Position

| Field | Type | Rule |
|-------|------|------|
| `finding_id` | `str` | merged finding id |
| `member` | `str` | perspective id or `defender` |
| `round` | `int` | 0 for initial positions, then 1 to `rebuttal_rounds` |
| `stance` | `Stance` | `withdraw` only from a raiser |
| `reason` | `str` | required |
| `answers` | `list[str]` | ids of positions this one responds to |

A member's stance at the end of the debate is its latest position on the finding; a member not called in a later round (because the call rule of protocol.md section 8 left it out, or the batch stopped early) keeps that position. A defender objection is "answered" when a later position by any perspective reviewer lists it in `answers` and the defender does not challenge again in a subsequent round.

### DebateRecord

`finding_id`, `positions: list[Position]`, `rounds_run: int`. Debate on a finding ends when no stance changed in a round or `rebuttal_rounds` is reached.

### ModeratorNote

Written by the moderator for every merged finding of a batch after its debate ends, without knowledge of labels: `finding_id`, `argument_for`, `argument_against`, `deciding_assumption` (nullable), `rejection_reason` (one sentence), `no_trigger_reason` (required when `trigger` or `wrong_output` is null). When no member argued against a finding, `argument_against` is "No member argued against."; when nothing in the debate supports rejection, `rejection_reason` is "Not rejected." `panel.py adjudicate` keeps the arguments only for contested findings and the rejection reason only for rejected ones.

### Finding (reported)

All `MergedFinding` fields plus: `label: AgreementLabel`; for `contested`, `argument_for`, `argument_against`, `deciding_assumption` (nullable). Invariant: every field of FR-014 present (SC-003). `trigger` and `wrong_output` are non-null for `consensus` and `majority`; they may be null only for `contested`, in which case `no_trigger_reason` is present (FR-014, FR-016).

### RejectedFinding

`finding_id`, `summary`, `raised_by`, `reason` (`withdrawn`, `unsupported`, or a moderator sentence).

### PanelRun

The object returned by the Workflow runner: `candidates: list` (one candidate-findings message per perspective), `merge: list` (one merge ruling per batch), `debate: list` (debate-positions messages, each tagged with batch and round), `notes: list` (one moderator-notes message per batch), `dropped: list[str]` (roles whose output failed validation twice). `panel.py ingest` writes it into the run directory layout.

### ReviewReport

`scope`, `panel`, `extensions: list[DomainExtension]`, `findings: list[Finding]` ordered by label then severity (FR-019), `rejected`, `checked_items`, `unreviewed: list[Exclusion]`, `notices: list[str]` (reduced independence, languages without worked examples, missing tools).

## 3. State transitions

```text
CandidateFinding --merge--> MergedFinding --debate (rounds 0..R)--> DebateRecord --moderator notes--> ModeratorNote
DebateRecord + ModeratorNote --adjudicate--> Finding(label) | RejectedFinding
```

Adjudication rules (applied in order, by `panel.py adjudicate`). "Stance" means each member's latest position (Position, above). "Perspectives" means every perspective reviewer in the panel, default and domain, the raiser included, and never the defender.

1. Raiser withdrew: rejected.
2. Only the raiser accepts and a defender objection is unanswered: rejected.
3. `trigger` or `wrong_output` is null: at most `contested`.
4. No perspective's stance is `challenge` or `withdraw`, at least two perspectives accept, and every defender objection is answered: `consensus`.
5. More than half of the perspectives have stance `accept`: `majority`.
6. Otherwise: `contested`.

Semantic checks that a JSON Schema cannot express, run by `panel.py` (exit code 1 on failure): `line_end >= line_start`; `withdraw` only from a member listed in the finding's `raised_by` (checked by `adjudicate`); a lowered merged severity has `severity_reason`; a moderator note has a non-null `no_trigger_reason` when its merged finding's `trigger` or `wrong_output` is null (checked by `adjudicate`).

Extension status: `discovered` then `failed` (declaration invalid or contract version unsupported) or `selected` or `not-applicable`; known but undiscovered extensions whose applicability matches become `recommended`.
