# Runner: Claude Workflow

This runner performs the panel phases of `protocol.md` (independent round, merge, debate and moderator notes) by launching the panel Workflow script of the plugin, which runs every panel agent with schema-validated output and returns all panel messages in one result. It starts after the opening steps of `SKILL.md` (`panel.py init`, `scope`, extension discovery with `select-extensions`, and `panel --runner claude-workflow`) and ends before its closing steps (`adjudicate`, `report`, delivery and `clean`). On completion, return to the closing steps of `SKILL.md`.

## 1. Notation

| Symbol | Meaning |
|--------|---------|
| `$SKILL` | Absolute path of the skill directory: `${CLAUDE_PLUGIN_ROOT}/skills/scientific-review`. |
| `$PANEL` | `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/panel.py"`, the plugin's `scripts/panel.py` (equivalently `python3 "$SKILL/../../scripts/panel.py"`). Write the command out in full, with the absolute path, in every shell command: never store it in a shell variable such as `PANEL=...`, because zsh does not split a variable into words, and the shell is not kept between commands. |
| `$SOURCE` | Absolute path of the panel Workflow script in the plugin, `scripts/scientific-review-panel.js` (resolve `$SKILL/../../scripts/scientific-review-panel.js`). The script is not registered as a workflow, so that the plugin exposes a single command, `/sci-review:scientific-review`. |
| `$SCRATCH` | The session's scratchpad directory, as the system prompt names it. |
| `$WORKFLOW` | `$SCRATCH/scientific-review-panel.js`, the copy of `$SOURCE` that is launched. The Workflow tool accepts a script path only in the working directory, an added directory or the scratchpad, and an installed plugin is in none of them, so `$SOURCE` cannot be launched where it is. |
| `$RUN` | The run directory printed by `panel.py init`. |
| `$PROJECT` | The reviewed project, the `project` field of `$RUN/run.json`. |

## 2. Preconditions

1. The `Workflow` tool is available, `$SOURCE` exists, and the system prompt names a scratchpad directory. Otherwise apply section 6.
2. Opt-in. When the user asked for the review, that request satisfies the Workflow opt-in requirement; do not ask again. When the review was started on the model's own initiative, ask the user before launching, because the Workflow spawns many agents. When the user declines, apply section 6.
3. Record the state of the project before the launch:
   1. When `$PROJECT` is a git repository, run `git -C "$PROJECT" status --porcelain --ignored` and keep its output as the baseline.
   2. Otherwise, the baseline is the modification time of `$RUN/run.json`.

## 3. Inputs per phase

The Workflow embeds `protocol.md`, the role briefs of `roles/` and the schemas of `schemas/`, and builds each agent's prompt itself. It passes each role only the inputs of contracts/panel-messages.md section 1 (SC-011):

| Phase | Role | Inputs passed by the Workflow |
|-------|------|-------------------------------|
| Independent | each perspective, once per review part | its brief; `protocol.md`; the five dimension documents; for a domain perspective, the files of its `reference_paths`; the scope; its review part (when there are several); the candidate-findings schema |
| Merge | moderator, one call per batch | its brief; all candidate-findings messages; the clusters of the batch; the merge-ruling schema |
| Debate round 0 | each perspective and the defender | its brief; the batch's merge ruling; for a perspective, its own candidate-findings message; the debate-positions schema |
| Debate round k >= 1 | each member that protocol.md section 8 calls | its brief; the batch's merge ruling; all positions of the batch from rounds 0 to k-1; the debate-positions schema |
| Moderator notes | moderator, one call per batch | its brief; the batch's merge ruling; all positions of the batch; the moderator-notes schema |

The arguments of section 4 are the only information the orchestrating conversation passes to the Workflow. Add nothing else, in particular no summary of the code, no expected findings and no prior review.

## 4. Steps

1. **Read the inputs.** Read `$RUN/scope.json`, `$RUN/parts.json` and `$RUN/panel.json`.
2. **Build the arguments** (contracts/invocation.md section 4):

   | Argument | Value |
   |----------|-------|
   | `scope` | the contents of `$RUN/scope.json` |
   | `project` | `$PROJECT`, the absolute path of the reviewed project; scope paths are relative to it, and Workflow agents do not necessarily start there |
   | `skill_dir` | `$SKILL`, the absolute path of the scientific-review skill directory, from which Workflow agents read the dimension documents (`dimensions/`) on demand |
   | `perspectives` | `panel.perspectives` of `$RUN/panel.json`, each entry reduced to `id`, `name`, `brief_path` and `reference_paths` |
   | `extensions` | the entries of `extensions` in `$RUN/panel.json` whose `status` is `selected` |
   | `rebuttal_rounds` | `panel.rebuttal_rounds` |
   | `max_batches` | `panel.max_batches` |
   | `parts` | the `parts` array of `$RUN/parts.json` |
   | `models` | `panel.models` as an object mapping each `role` to its `model`; `{}` when the list is empty |

   The Workflow embeds the default briefs; `brief_path` and `reference_paths` are read by the Workflow only for domain perspectives, whose brief and reference material are not embedded.
3. **Copy** the script into the scratchpad, replacing any earlier copy, so that the launched script is the plugin's current one:

   ```sh
   cp "$SOURCE" "$WORKFLOW"
   ```

   Write both paths out in full. Never edit the copy.
4. **Launch** the Workflow:

   ```text
   Workflow({ scriptPath: "$WORKFLOW", args: { scope, project, skill_dir, perspectives, extensions, rebuttal_rounds, max_batches, parts, models } })
   ```

   The independent round runs one agent per perspective and review part, in parallel. Each agent receives its part, may read any file of the project to follow a reference, and raises findings only on lines of its part; its message carries `part`, and in a review of several parts the script numbers its findings `<perspective>-<part>-<n>`. In debate round 0, a perspective receives its candidates of every part. A failed agent returns nothing and is listed in `dropped`; the Workflow writes no part status, and `panel.py report` derives each part's status from the ingested candidate files.

5. **Write the result.** Write the returned `PanelRun` object (`candidates`, `merge`, `debate` as a list of `{batch, message}`, `notes`, `dropped`), exactly as returned, to `$RUN/workflow-result.json`. When the copy or the launch fails, or the Workflow returns no `PanelRun`, apply section 6.
6. **Ingest** the messages into the run directory layout of contracts/panel-messages.md section 2:

   ```sh
   $PANEL ingest --run $RUN $RUN/workflow-result.json
   ```

   `ingest` validates every message, writes `candidates/` (as `candidates/<perspective>--<part>.json`), `merge/`, `debate/` and `notes/`, records a notice for each message it drops, and records the notice "The output of <role> was dropped after failing validation twice." for each role listed in `dropped`. A non-zero exit means the result is not a `PanelRun`; apply section 6.
7. **Project check** (SC-004).
   1. For a git repository, run `git -C "$PROJECT" status --porcelain --ignored` and compare it with the baseline of section 2.3. Otherwise, run `find "$PROJECT" -type f -newer "$RUN/run.json" -not -path '*/.git/*'`.
   2. When any path differs from the baseline, or `find` lists any file, record it and tell the user which paths changed. Do not revert them.

      ```sh
      $PANEL notice --run $RUN "The reviewed project changed during the review: <paths>."
      ```

8. Return to the closing steps of `SKILL.md`.

## 5. Rules

1. Never edit `$RUN/workflow-result.json` or the ingested files by hand; labels and the report are computed by `panel.py` from the messages as the agents wrote them.
2. Never pass to the Workflow, or add to its result, any content not produced by its agents.

## 6. Fallback

When the Workflow is unavailable, the session has no scratchpad directory, the Workflow is declined or fails, or returns a result that `ingest` rejects:

1. Select the next runner in the order of contracts/invocation.md section 3 that is available: `claude-agents` when the Agent tool lists `sci-review:scientific-auditor`, otherwise `sequential`.
2. Record it, repeating the panel recorded in `$RUN/panel.json`:

   ```sh
   $PANEL panel --run $RUN --runner <runner> --perspectives <ids of panel.perspectives, comma-separated> --rounds <panel.rebuttal_rounds> --batches <panel.max_batches>
   ```

3. Remove any partially ingested message directories (`candidates/`, `merge/`, `debate/`, `notes/`) from `$RUN`, and continue with `runners/claude-agents.md` or `runners/sequential.md` from its first step.
