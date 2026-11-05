# Runner: Claude agents

This runner performs the panel phases of `protocol.md` (independent round, merge, debate and moderator notes) by launching `sci-review:scientific-auditor` agents with the Agent tool. It starts after the opening steps of `SKILL.md` (`panel.py init`, `scope`, extension discovery with `select-extensions`, and `panel --runner claude-agents`) and ends before its closing steps (`adjudicate`, `report`, delivery and `clean`). On completion, return to the closing steps of `SKILL.md`. Its steps are those of `runners/codex-subagents.md`, with each spawn replaced by the launch of a `sci-review:scientific-auditor` agent.

## 1. Notation

| Symbol | Meaning |
|--------|---------|
| `$SKILL` | Absolute path of the skill directory: `${CLAUDE_PLUGIN_ROOT}/skills/scientific-review`. |
| `$PANEL` | `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/panel.py"`, the plugin's `scripts/panel.py` (equivalently `python3 "$SKILL/../../scripts/panel.py"`). Write the command out in full, with the absolute path, in every shell command: never store it in a shell variable such as `PANEL=...`, because zsh does not split a variable into words, and the shell is not kept between commands. |
| `$RUN` | The run directory printed by `panel.py init`. |
| `$PROJECT` | The reviewed project, the `project` field of `$RUN/run.json`. |
| `$SCHEMAS` | `$SKILL/schemas`. The schema of a message named `<name>` is `$SCHEMAS/<name>.schema.json`. |
| Perspectives | The entries of `panel.perspectives` in `$RUN/panel.json`, in their listed order. Each has `id`, `name`, `brief_path` (absolute), `source` and `reference_paths` (absolute). Domain perspectives contributed by extensions appear here like the defaults and need no special handling. |
| Members | The perspectives and the defender (member id `defender`). |
| Defender brief | `$SKILL/roles/defender.md`. |
| Moderator brief | `$SKILL/roles/moderator.md`. |
| R | `panel.rebuttal_rounds` in `$RUN/panel.json`. |

Every path placed in a prompt is expanded to an absolute path first; the agents do not resolve `${CLAUDE_PLUGIN_ROOT}` or the symbols above.

## 2. Preconditions

1. The Agent tool is available and lists the `sci-review:scientific-auditor` agent type. If a launch fails at any step, apply section 6.
2. All launches of one step are made in a single message, one Agent tool call per task, so that they run concurrently. When agents run in the background, wait for the completion notification of every agent of the step before validating.
3. Record the state of the project before the first launch:
   1. When `$PROJECT` is a git repository, run `git -C "$PROJECT" status --porcelain --ignored` and keep its output as the baseline.
   2. Otherwise, the baseline is the modification time of `$RUN/run.json`.

## 3. Rules

1. Each prompt contains only the inputs listed for its phase in section 4, which are those of contracts/panel-messages.md section 1 (SC-011), the absolute path of the schema, the absolute path of the output file, and the instruction to write that file and nothing else.
2. The orchestrator never summarises, quotes or paraphrases one agent's output in another agent's prompt. Outputs reach other agents only as the files listed for that phase.
3. Every agent is told not to create, modify or delete any file outside `$RUN`, and never any file of `$PROJECT`.
4. After each agent finishes, validate its output with `$PANEL validate --schema <name> <file>`. When validation fails (exit 1) or the file is missing, return the output once to its author with the errors, using the return template of section 4.6: send it to the same agent with SendMessage when that tool is available, otherwise launch a new `sci-review:scientific-auditor` agent with the original prompt followed by the return template. When the second attempt also fails, delete the invalid file and record:

   ```sh
   $PANEL notice --run $RUN "The output of <role> was dropped after failing validation twice."
   ```

   where `<role>` names the role and message, for example `theorist candidates`, `moderator merge (batch 1)`, `defender debate (batch 2, round 1)` or `moderator notes (batch 1)`.
5. A dropped candidates file removes that perspective's candidates from the merge; the perspective still takes part in the debate. A dropped merge ruling removes its batch from the debate and the notes. A dropped position file leaves the member's earlier stances in force. A dropped notes file leaves the batch's findings without notes.

## 4. Prompt templates

Each launch is an Agent tool call with `subagent_type: "sci-review:scientific-auditor"`, a short `description` (for example `sci-review theorist independent p2`), and a `prompt` of the following form. Lines in angle brackets are filled by the orchestrator; no other content is added.

```text
sci-review panel task: <role> (<phase>)

1. Role brief: <absolute path of the role brief>. Read it first and adopt it for the whole task.
   Task: <phase instruction>
2. Inputs (read only these, and the files of the reviewed project listed in scope.json):
   - <absolute path>
   - ...
   Reviewed project (read only): <$PROJECT>
3. Output schema: <$SCHEMAS/<name>.schema.json>
4. Output file: <absolute path inside $RUN>

Write exactly one file, the output file, as one JSON object conforming to the output schema. Do not create, modify or delete any other file, and never modify a file of the reviewed project. Reply with the output path and one sentence summarising its content.
```

The phase-specific fields are as follows.

### 4.1 Independent round (one prompt per perspective `<p>` and review part `<q>` of `$RUN/parts.json`)

- Role: `<p.id>`; phase `independent round`; role brief `<p.brief_path>`.
- Task: `Review review part <q.id> of the scope under every dimension and write your candidate findings and checked items. Review every line of the part; you may read any file of the reviewed project, inside or outside the scope, to follow a reference, but raise findings only on lines of the part. Set `part` to `<q.id>`. When parts.json holds more than one part, number your findings `<p.id>-<q.id>-1`, `<p.id>-<q.id>-2`, ...; otherwise `<p.id>-1`, `<p.id>-2`, ....`
- Inputs:
  - `$SKILL/protocol.md`
  - `$SKILL/dimensions/mathematical-derivations.md`, `numerical-stability.md`, `physical-modelling-and-units.md`, `statistical-integrity.md`, `algorithmic-correctness.md` (absolute paths; loaded on demand)
  - each path of `<p.reference_paths>` (domain perspectives only)
  - `$RUN/scope.json`
  - `$RUN/parts.json` (review part `<q.id>`: its files and line ranges)
- Output schema: `$SCHEMAS/candidate-findings.schema.json`. Output file: `$RUN/candidates/<p.id>--<q.id>.json`.

### 4.2 Merge (one prompt per batch `<b>`)

- Role: `moderator`; phase `merge task, batch <b>`; role brief: the moderator brief.
- Task: `Perform the merge task for batch <b> only, covering every cluster of batch <b> in the clusters file; number split findings from the next_finding_id of batch <b>.`
- Inputs: every file `$RUN/candidates/*.json` (each listed by absolute path), and `$RUN/clusters.json`.
- Output schema: `$SCHEMAS/merge-ruling.schema.json`. Output file: `$RUN/merge/batch-<b>.json`.

### 4.3 Debate round 0 (one prompt per member `<m>` of batch `<b>`)

- Role: `<m>`; phase `debate, batch <b>, round 0`; role brief: `<p.brief_path>` for a perspective, the defender brief for `defender`.
- Task: `State your round 0 position on every merged finding of batch <b>.`
- Inputs:
  - `$RUN/merge/batch-<b>.json`
  - for a perspective only: every file `$RUN/candidates/<m>--*.json` that exists (its candidates of every part)
- Output schema: `$SCHEMAS/debate-positions.schema.json`. Output file: `$RUN/debate/batch-<b>/round-0/<m>.json`.

### 4.4 Debate round k >= 1 (one prompt per member `<m>` called in round `<k>` of batch `<b>`)

- Role: `<m>`; phase `debate, batch <b>, round <k>`; role brief as in 4.3.
- Task: `State your round <k> position on every merged finding of batch <b>, answering the earlier positions.`
- Inputs:
  - `$RUN/merge/batch-<b>.json`
  - every file `$RUN/debate/batch-<b>/round-<j>/*.json` for j = 0 to k-1 (each listed by absolute path)
- Output schema: `$SCHEMAS/debate-positions.schema.json`. Output file: `$RUN/debate/batch-<b>/round-<k>/<m>.json`.

### 4.5 Moderator notes (one prompt per batch `<b>`)

- Role: `moderator`; phase `notes task, batch <b>`; role brief: the moderator brief.
- Task: `Perform the notes task for every merged finding of batch <b>.`
- Inputs:
  - `$RUN/merge/batch-<b>.json`
  - every file `$RUN/debate/batch-<b>/round-*/*.json` (each listed by absolute path)
- Output schema: `$SCHEMAS/moderator-notes.schema.json`. Output file: `$RUN/notes/batch-<b>.json`.

### 4.6 Return of an invalid output

```text
Your output file <absolute path> failed validation against <$SCHEMAS/<name>.schema.json> with these errors:
<validator output, verbatim>
Correct the file and write it again to the same path. Change nothing else.
```

## 5. Steps

1. **Independent round.**
   1. Launch one `sci-review:scientific-auditor` agent per perspective and review part of `$RUN/parts.json`, each with the prompt of section 4.1. Launch them in a single message when they fit within the host's concurrency limit; otherwise launch them in batches no larger than that limit, each batch in a single message, starting the next batch when the previous one has finished. Batches never change an agent's inputs.
   2. Wait for all of them.
   3. Validate each `$RUN/candidates/<id>--<part>.json` with `--schema candidate-findings`, and apply rule 3.4. Write no part status: `panel.py report` derives it, and reports a part whose candidates file is missing or invalid as not reviewed.
2. **Merge.**
   1. Run `$PANEL merge --run $RUN > $RUN/clusters.json`. The file holds `clusters` (each with `id`, `suggested_finding_id`, `file`, `line_start`, `line_end`, `members` and `batch`) and `batches` (each with `batch`, `clusters` and `next_finding_id`). The `next_finding_id` of batch b is the first identifier of the range reserved for findings created by splits in that batch, F(1000*b + 1) onward (`F1001` for batch 1, `F2001` for batch 2), so that moderators working in parallel never assign the same identifier.
   2. When `batches` is empty, no candidate finding was raised: skip steps 3 and 4 and go to step 5.
   3. In a single message, launch one `sci-review:scientific-auditor` agent per batch as moderator, each with the prompt of section 4.2.
   4. Validate each `$RUN/merge/batch-<b>.json` with `--schema merge-ruling`, and apply rule 3.4.
3. **Debate.** The batches advance together: each message launches the next round of every batch still in debate, together with the notes launches of step 4 for batches whose debate has just ended.
   1. **Round 0.** In a single message, launch one agent per member (every perspective and the defender) of every batch with a valid merge ruling, each with the prompt of section 4.3. Wait for all; validate each file with `--schema debate-positions`; apply rule 3.4.
   2. When R is 0, the debate of every batch ends after round 0.
   3. **Round 1.** In a single message, launch every member of every batch, with the prompt of section 4.4 for k = 1. Wait for all; validate; apply rule 3.4.
   4. **Stop rule** (protocol.md section 8). After each rebuttal round k >= 1, the batch stops when no member's stance changed in round k; otherwise round k + 1 calls the members whose stance changed and, for each finding someone newly challenged, the perspectives that currently accept it. Run `$PANEL debate-status --run $RUN --batch <b> --round <k>`; it prints `{"stopped": ..., "call": [...]}`, where `call` lists the members to call in round k + 1.

   5. **Round k + 1.** When k < R, in a single message, launch the members listed in `call` for every batch that has not stopped, with the prompt of section 4.4 for round k + 1. Wait for all; validate; apply rule 3.4; return to step 3.4 with k + 1.
   6. The debate of a batch ends when it stops or after round R.
4. **Moderator notes.** For each batch whose debate has ended, launch one agent as moderator with the prompt of section 4.5, in the same message as the next debate launches of step 3, or in its own message when no debate remains. Validate `$RUN/notes/batch-<b>.json` with `--schema moderator-notes`, and apply rule 3.4.
5. **Project check** (SC-004). When every batch has its notes (or was dropped):
   1. For a git repository, run `git -C "$PROJECT" status --porcelain --ignored` and compare it with the baseline of section 2.3. Otherwise, run `find "$PROJECT" -type f -newer "$RUN/run.json" -not -path '*/.git/*'`.
   2. When any path differs from the baseline, or `find` lists any file, record it and tell the user which paths changed. Do not revert them.

      ```sh
      $PANEL notice --run $RUN "The reviewed project changed during the review: <paths>."
      ```

6. Return to the closing steps of `SKILL.md`.

## 6. Fallback to the sequential runner

When a launch fails (the agent type is unavailable or the Agent tool refuses the call):

1. Record the runner change, repeating the panel recorded in `$RUN/panel.json`:

   ```sh
   $PANEL panel --run $RUN --runner sequential --perspectives <ids of panel.perspectives, comma-separated> --rounds <R> --batches <panel.max_batches>
   ```

   With `independent` now false, `panel.py report` adds the reduced-independence notice.
2. Keep every valid message file already written in `$RUN`.
3. Continue with `runners/sequential.md` at the step corresponding to the one that failed.
