# Runner: sequential

This runner performs the panel phases of `protocol.md` (independent round, merge, debate and moderator notes) in the orchestrating conversation, one role at a time, without spawning agents. It starts after the opening steps of `SKILL.md` (`panel.py init`, `scope`, extension discovery with `select-extensions`, and `panel --runner sequential`) and ends before its closing steps (`adjudicate`, `report`, delivery and `clean`). On completion, return to the closing steps of `SKILL.md`. It writes the same message files and runs the same `panel.py` steps as the agent runners. When `python3` is absent, section 6 replaces every `panel.py` step, the opening and closing steps of `SKILL.md` included.

Because one reviewer performs every role, the perspectives are not independent agents. `panel.json` records `independent: false` for this runner, and `panel.py report` adds the reduced-independence notice (FR-028).

## 1. Notation

| Symbol | Meaning |
|--------|---------|
| `$SKILL` | Absolute path of the skill directory, the directory that holds `SKILL.md`. |
| `$PANEL` | `python3 "$SKILL/../../scripts/panel.py"`, the plugin's `scripts/panel.py` resolved from the skill's own directory; on Claude, `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/panel.py"`. |
| `$RUN` | The run directory printed by `panel.py init`. |
| `$PROJECT` | The reviewed project, the `project` field of `$RUN/run.json`. |
| `$SCHEMAS` | `$SKILL/schemas`. The schema of a message named `<name>` is `$SCHEMAS/<name>.schema.json`. |
| Perspectives | The entries of `panel.perspectives` in `$RUN/panel.json`, in their listed order. Each has `id`, `name`, `brief_path` (absolute), `source` and `reference_paths` (absolute). Domain perspectives contributed by extensions appear here like the defaults and need no special handling. |
| Members | The perspectives and the defender (member id `defender`). |
| Defender brief | `$SKILL/roles/defender.md`. |
| Moderator brief | `$SKILL/roles/moderator.md`. |
| R | `panel.rebuttal_rounds` in `$RUN/panel.json`. |

## 2. Rules

1. **One role at a time.** Before each task, state its header (section 3) in the conversation, read the role brief, and work only from the inputs the header lists. Write the output file before starting the next task.
2. **Independent round discipline.** Perform the perspectives in the order of `panel.perspectives`. Write each perspective's candidates file before reading the next perspective's brief. While performing a perspective, do not reread, consult or refer to any candidates file already written; review the scope afresh from that perspective's brief.
3. **Debate discipline.** In round 0, state each member's positions from the merge ruling and, for a perspective, its own candidates file only; do not revise or refer to positions already written in round 0. In round k >= 1, use only positions of rounds 0 to k-1.
4. **Writing files.** Write each message as one JSON object with a file-writing tool or a shell heredoc, at the path given in its header. Write nothing outside `$RUN`, and never create, modify or delete a file of `$PROJECT`. Use git only for read-only commands.
5. **Validation.** Validate each message with `$PANEL validate --schema <name> <file>`. When validation fails, correct the message once from the validator's errors and write it again to the same path. When the second attempt also fails, delete the file and record:

   ```sh
   $PANEL notice --run $RUN "The output of <role> was dropped after failing validation twice."
   ```

   where `<role>` names the role and message, for example `theorist candidates`, `moderator merge (batch 1)`, `defender debate (batch 2, round 1)` or `moderator notes (batch 1)`.
6. **Dropped messages.** A dropped candidates file removes that perspective's candidates from the merge; the perspective still takes part in the debate. A dropped merge ruling removes its batch from the debate and the notes. A dropped position file leaves the member's earlier stances in force. A dropped notes file leaves the batch's findings without notes.

## 3. Task headers

Each task begins with a header of the following form, written in the conversation. Its inputs are exactly those of contracts/panel-messages.md section 1 for the phase (SC-011); nothing else is read for the task, apart from the files of the reviewed project listed in `scope.json`.

```text
sci-review panel task: <role> (<phase>)
Role brief: <absolute path of the role brief>
Task: <phase instruction>
Inputs:
- <absolute path>
- ...
Reviewed project (read only): <$PROJECT>
Output schema: <$SCHEMAS/<name>.schema.json>
Output file: <absolute path inside $RUN>
```

The phase-specific fields are as follows.

### 3.1 Independent round (one task per perspective `<p>`)

- Role: `<p.id>`; phase `independent round`; role brief `<p.brief_path>`.
- Task: `Review the scope under every dimension and write the candidate findings and checked items.`
- Inputs:
  - `$SKILL/protocol.md`
  - `$SKILL/dimensions/mathematical-derivations.md`, `numerical-stability.md`, `physical-modelling-and-units.md`, `statistical-integrity.md`, `algorithmic-correctness.md` (absolute paths; loaded on demand)
  - each path of `<p.reference_paths>` (domain perspectives only)
  - `$RUN/scope.json`
- Output schema: `candidate-findings`. Output file: `$RUN/candidates/<p.id>.json`.

### 3.2 Merge (one task per batch `<b>`)

- Role: `moderator`; phase `merge task, batch <b>`; role brief: the moderator brief.
- Task: `Perform the merge task for batch <b> only, covering every cluster of batch <b> in the clusters file; number split findings from the next_finding_id of batch <b>.`
- Inputs: every file `$RUN/candidates/*.json`, and `$RUN/clusters.json`.
- Output schema: `merge-ruling`. Output file: `$RUN/merge/batch-<b>.json`.

### 3.3 Debate round 0 (one task per member `<m>` of batch `<b>`)

- Role: `<m>`; phase `debate, batch <b>, round 0`; role brief: `<p.brief_path>` for a perspective, the defender brief for `defender`.
- Task: `State the round 0 position of <m> on every merged finding of batch <b>.`
- Inputs:
  - `$RUN/merge/batch-<b>.json`
  - for a perspective only: `$RUN/candidates/<m>.json`, when that file exists
- Output schema: `debate-positions`. Output file: `$RUN/debate/batch-<b>/round-0/<m>.json`.

### 3.4 Debate round k >= 1 (one task per member `<m>` called in round `<k>` of batch `<b>`)

- Role: `<m>`; phase `debate, batch <b>, round <k>`; role brief as in 3.3.
- Task: `State the round <k> position of <m> on every merged finding of batch <b>, answering the earlier positions.`
- Inputs:
  - `$RUN/merge/batch-<b>.json`
  - every file `$RUN/debate/batch-<b>/round-<j>/*.json` for j = 0 to k-1
- Output schema: `debate-positions`. Output file: `$RUN/debate/batch-<b>/round-<k>/<m>.json`.

### 3.5 Moderator notes (one task per batch `<b>`)

- Role: `moderator`; phase `notes task, batch <b>`; role brief: the moderator brief.
- Task: `Perform the notes task for every merged finding of batch <b>.`
- Inputs:
  - `$RUN/merge/batch-<b>.json`
  - every file `$RUN/debate/batch-<b>/round-*/*.json`
- Output schema: `moderator-notes`. Output file: `$RUN/notes/batch-<b>.json`.

## 4. Steps

1. **Project baseline.** When `$PROJECT` is a git repository, run `git -C "$PROJECT" status --porcelain --ignored` and keep its output as the baseline. Otherwise, the baseline is the modification time of `$RUN/run.json`.
2. **Independent round.** For each perspective in turn, perform the task of section 3.1, write `$RUN/candidates/<id>.json`, and validate it with `--schema candidate-findings` (rule 2.5) before reading the next perspective's brief.
3. **Merge.**
   1. Run `$PANEL merge --run $RUN > $RUN/clusters.json`. The file holds `clusters` (each with `id`, `suggested_finding_id`, `file`, `line_start`, `line_end`, `members` and `batch`) and `batches` (each with `batch`, `clusters` and `next_finding_id`). The `next_finding_id` of batch b is the first identifier of the range reserved for findings created by splits in that batch, F(1000*b + 1) onward (`F1001` for batch 1, `F2001` for batch 2), so that moderators working in parallel never assign the same identifier.
   2. When `batches` is empty, no candidate finding was raised: skip steps 4 and 5 and go to step 6.
   3. For each batch in turn, perform the task of section 3.2 and validate `$RUN/merge/batch-<b>.json` with `--schema merge-ruling`.
4. **Debate.** For each batch with a valid merge ruling, in turn:
   1. **Round 0.** For each member in turn (the perspectives in listed order, then the defender), perform the task of section 3.3 and validate the file with `--schema debate-positions`.
   2. When R is 0, the debate of the batch ends after round 0.
   3. **Round 1.** For every member in turn, perform the task of section 3.4 for k = 1, and validate.
   4. **Stop rule** (protocol.md section 8). After each rebuttal round k >= 1, the batch stops when no member's stance changed in round k; otherwise round k + 1 calls the members whose stance changed and, for each finding someone newly challenged, the perspectives that currently accept it. Run `$PANEL debate-status --run $RUN --batch <b> --round <k>`; it prints `{"stopped": ..., "call": [...]}`, where `call` lists the members to call in round k + 1.

   5. **Round k + 1.** When the batch has not stopped and k < R, perform the task of section 3.4 for round k + 1 for each member listed in `call`, in turn, validate, and return to step 4.4 with k + 1.
   6. The debate of the batch ends when it stops or after round R.
5. **Moderator notes.** For each batch whose debate has ended, perform the task of section 3.5 and validate `$RUN/notes/batch-<b>.json` with `--schema moderator-notes`.
6. **Project check** (SC-004).
   1. For a git repository, run `git -C "$PROJECT" status --porcelain --ignored` and compare it with the baseline of step 1. Otherwise, run `find "$PROJECT" -type f -newer "$RUN/run.json" -not -path '*/.git/*'`.
   2. When any path differs from the baseline, or `find` lists any file, record it and tell the user which paths changed. Do not revert them.

      ```sh
      $PANEL notice --run $RUN "The reviewed project changed during the review: <paths>."
      ```

7. Return to the closing steps of `SKILL.md`.

## 5. Arrival from another runner

When an agent runner falls back to this runner after a failed spawn or launch, `$PANEL panel --run $RUN --runner sequential` has already been run with the same perspectives, rounds and batches. Keep every valid message file already in `$RUN`, and start at the step of section 4 that corresponds to the step that failed. Step 1 is still performed when no baseline was recorded.

## 6. Without python3

When `python3` is absent, every `panel.py` step is performed by hand from the written fallback rules of `protocol.md` section 10, including the opening and closing steps of `SKILL.md`. The stop-rule snippet of step 4.4 is replaced by inspection of the position files. Keep the notices in `$RUN/notices.json` as a JSON array of strings, and add to it:

- "python3 was not available; the deterministic steps were performed by hand from the written rules of protocol.md."
- "The perspectives were not independent agents; agreement among them was reached within a single reviewer and is weaker evidence than in a parallel review."

Each `panel.py` step is replaced as follows.

| Step | `panel.py` command | Performed by hand |
|------|--------------------|-------------------|
| Opening | `init` | Create a directory under the system temporary directory (for example with `mktemp -d`), never inside the project, as `$RUN`, and write `$RUN/run.json` as `{"project": <absolute project path>, "run": <absolute run path>}`. |
| Opening | `scope` | protocol.md section 10, rule **scope**: write `$RUN/scope.json` with `mode`, `base`, `head`, `files` (each with `path`, `language` and `line_ranges`), `excluded` (each with `path` and `reason`) and a one-sentence `note`. When no base can be determined, ask the user. |
| Opening | `select-extensions` | protocol.md section 10, rule **select-extensions**, applied to each discovered `extension.json`. |
| Opening | `panel` | protocol.md section 6 limits: write `$RUN/panel.json` with `panel` (`perspectives` with absolute `brief_path` and `reference_paths`, `rebuttal_rounds`, `max_batches`, `runner: "sequential"`, `independent: false`, `models: []`), `extensions` and `notices`. Default perspective briefs are `$SKILL/roles/<id>.md`. |
| Runner | `validate` | Check each message by eye against its schema: every required field present, no unknown field, enumerations respected, `line_end >= line_start`, each candidate's `raised_by` equal to the message `perspective`, each position's `member` and `round` equal to the message's. Rule 2.5 applies, with the notice added to `$RUN/notices.json`. |
| Runner | `merge` | protocol.md section 7: cluster and batch the candidates, and write the result to `$RUN/clusters.json` in the form of step 3.1, with suggested finding ids `F1`, `F2`, ... in cluster order and the `next_finding_id` of batch b set to F(1000*b + 1). |
| Runner | `notice` | Append the sentence to `$RUN/notices.json`. |
| Runner | debate stop rule | protocol.md section 8, by inspection of the position files. |
| Closing | `adjudicate` | protocol.md section 5: for every merged finding, collect the positions of its batch, apply the six rules in order, stop on a `withdraw` from a member outside `raised_by`, and attach the moderator notes. |
| Closing | `report` | protocol.md section 10, rule **report**: write the report in the eight sections of contracts/report.md section 1, with every finding field of section 2, the notices of `$RUN/notices.json` and `panel.json`, and deliver it as a Markdown table per label. |
| Closing | `clean` | Delete `$RUN` unless the user asked to keep it. |
