# Contract: review report

## 1. Sections, in order

1. **Scope**: one sentence (`scope.note`), runner, and whether the perspectives were independent agents.
2. **Panel**: perspectives used (with source), rebuttal rounds, batches.
3. **Extensions**: selected, not applicable, failed (with reason), recommended (with what it would add).
4. **Findings**: ordered consensus, majority, contested; within each, high, medium, low (FR-019).
5. **Rejected findings**: id, summary, raised by, reason.
6. **Checked and found correct**: location, dimension, note.
7. **Not reviewed**: path and reason.
8. **Notices**: reduced independence (FR-028), languages without worked examples, tools missing, messages dropped after failed validation.

When no reviewable scientific code changed, the report contains sections 1 to 3 and the sentence "No reviewable scientific code changed in this scope."

## 2. Finding fields

`location` (file:line), `dimension`, `severity`, `summary`, `trigger`, `wrong_output`, `fix`, `raised_by`, `label`, and for contested findings `argument_for`, `argument_against`, `deciding_assumption`, and `no_trigger_reason` when `trigger` or `wrong_output` is null.

## 3. Delivery

- **ReportFindings available** (Claude Code): one call, findings ordered as in section 1.4. Mapping: `file`, `line` from location; `summary`; `failure_scenario` = `trigger` + " produces " + `wrong_output`, or, when either is null (contested only), "No concrete trigger established: " + `no_trigger_reason`; `category` = dimension; `verdict` = `CONFIRMED` for consensus and majority, `PLAUSIBLE` for contested; `short_summary` prefixed with the label; for contested findings, `summary` is followed by " Contested. For: " + `argument_for` + " Against: " + `argument_against` and, when present, " Decided by: " + `deciding_assumption`. The remaining sections follow as Markdown.
- **Otherwise** (Codex, claude.ai, Cowork): Markdown table with all fields of section 2, one table per label, followed by the other sections.
