# Contract: panel messages

Every runner exchanges the same messages. In the Workflow runner they are agent outputs validated by the Workflow schema option, returned by the Workflow and written into the run directory by `panel.py ingest`; in the Codex and Agent runners they are JSON files in the run directory, validated by `panel.py validate`. Every runner therefore ends with the same files, from which `panel.py adjudicate`, `panel.py report` and `score.py --run` work. Field definitions are in data-model.md. The JSON Schemas live in `plugins/sci-review/skills/scientific-review/schemas/`.

## 1. Inputs per role and phase

The table lists everything a role receives. Nothing else may be passed (SC-011).

| Phase | Role | Receives | Must not receive |
|-------|------|----------|------------------|
| Independent | perspective | its brief; `protocol.md`; the five dimension documents (loaded on demand); extension reference material if it is a domain perspective; `scope.json`; output path | any other perspective's output |
| Merge | moderator | its brief; all `candidates/*.json`; the clusters from `panel.py merge` | none |
| Debate round 0 | each perspective and defender | its brief; the batch's merged findings; its own independent output | other members' round 0 positions |
| Debate round k > 0 | each perspective and defender | its brief; the batch's merged findings; all positions from rounds 0 to k-1 | positions from round k |
| Moderator notes | moderator | its brief; the batch's merged findings; all positions of the batch | labels (they are computed afterwards) |

## 2. Message files (file-based runners)

```text
$RUN/                                  # under the system temp dir, never in the project
├── run.json                           # project and run paths, written by init
├── scope.json                         # ReviewScope
├── panel.json                         # Panel and selected extensions
├── candidates/<perspective>.json      # candidate-findings.schema.json
├── merge/batch-<b>.json               # merge-ruling.schema.json
├── debate/batch-<b>/round-<k>/<member>.json   # debate-positions.schema.json
├── notes/batch-<b>.json               # moderator-notes.schema.json
├── clusters.json                      # output of panel.py merge (file-based runners)
├── notices.json                       # notices added by panel.py notice and ingest
├── adjudication.json                  # output of panel.py adjudicate
└── report.json                        # report.schema.json
```

## 3. Schemas (summary)

- `candidate-findings.schema.json`: `{ "perspective": str, "findings": [CandidateFinding], "checked_items": [CheckedItem], "notes": str }`.
- `merge-ruling.schema.json`: `{ "batch": int, "findings": [MergedFinding], "split": [{ "cluster": str, "reason": str }] }`.
- `debate-positions.schema.json`: `{ "member": str, "round": int, "positions": [Position] }`; one entry per finding in the batch.
- `moderator-notes.schema.json`: `{ "batch": int, "notes": [ModeratorNote] }`; one entry per finding in the batch.
- `report.schema.json`: `ReviewReport`.

Conditional rules (for example, `argument_for` required when `label` is `contested`) are written with `if`/`then` on a property's `const` or `enum`, which `panel.py validate` supports. Rules that span messages are semantic checks in `panel.py` (data-model.md, section 3).

All schemas set `additionalProperties: false`. A message that fails validation is returned once to its author with the validator's errors; a second failure drops the message and adds a notice naming the role.
