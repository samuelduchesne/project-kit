# Runner: Claude agents

This runner performs the panel phases with the procedure of `protocol.md` section 12, starting each task as a `sci-review:scientific-auditor` agent with the Agent tool. It starts after the opening steps of `SKILL.md` (through `panel --runner claude-agents`) and ends before its closing steps (`adjudicate` onward).

## 1. Starting a task

1. Each task is one Agent tool call with `subagent_type: "sci-review:scientific-auditor"`, a short `description` (for example `sci-review theorist p1` or `sci-review v2 batch 1`), and the task message of `protocol.md` section 12.3 as its `prompt`, with every path absolute (the agent does not resolve `${CLAUDE_PLUGIN_ROOT}`). Add nothing else to the prompt.
2. Start all tasks of one step in a single message, one Agent call per task, so that they run concurrently. When they exceed the host's concurrency limit, start them in batches no larger than that limit, each in a single message. Batching never changes a task's inputs. When agents run in the background, wait for the completion notification of every agent of the step before validating.
3. Return an invalid output (rule 12.2.3) to the same agent with SendMessage when that tool is available; otherwise start a new agent with the original prompt followed by the return message.

## 2. Fallback to the sequential runner

When a launch fails (the agent type is unavailable or the Agent tool refuses the call):

1. Record the runner change, repeating the panel recorded in `$RUN/panel.json`:

   ```sh
   $PANEL panel --run $RUN --runner sequential --perspectives <ids of panel.perspectives, comma-separated> --protocol <protocol> --rounds <rebuttal_rounds> --batches <max_batches> --verifiers <verifiers>
   ```

   With `independent` now false, `panel.py report` adds the reduced-independence notice.
2. Keep every valid message file already written in `$RUN`.
3. Continue with `runners/sequential.md` at the step that failed.
