# Runner: Codex subagents

This runner performs the panel phases with the procedure of `protocol.md` section 12, starting each task as a Codex subagent. It starts after the opening steps of `SKILL.md` (through `panel --runner codex-subagents`) and ends before its closing steps (`adjudicate` onward).

## 1. Starting a task

1. Multi-agent tools are enabled (`agents.enabled`, default true). If a spawn fails at any step, apply section 2.
2. Each task is one spawned subagent whose task message is that of `protocol.md` section 12.3. When the user has installed the optional `sci-review-panelist` custom agent (`~/.codex/agents/sci-review-panelist.toml`), name it in every spawn; otherwise use the built-in `default` agent. The skill never installs or copies this agent; its template is `$SKILL/codex-agents/sci-review-panelist.toml`.
3. Set `fork_turns` to `"none"` in every spawn. When it is omitted, Codex forks the parent's history into the subagent, including the completion messages of subagents already finished, and the subagent must start from its task message alone (SC-011). If the spawn tool has no `fork_turns` parameter, spawn without a history fork by the means it offers; if it offers none, apply section 2.
4. Spawn the tasks of one step together. Read `agents.max_concurrent_threads_per_session` from the Codex configuration (`[agents]` in `~/.codex/config.toml` or the project's `.codex/config.toml`); when it is lower than the number of tasks in a step, spawn in waves of at most that many, starting the next wave when the previous one has finished. When a spawn is refused because the limit is reached, take the number of subagents then running as the limit. Waves never change a task's inputs.
5. Return an invalid output (rule 12.2.3) to the same subagent when it is still open, otherwise to a new subagent given the original task message followed by the return message.

## 2. Fallback to the sequential runner

When spawning fails (multi-agent tools disabled, a spawn refused for a reason other than the concurrency limit, or no way to spawn without a history fork):

1. Record the runner change, repeating the panel recorded in `$RUN/panel.json`:

   ```sh
   $PANEL panel --run $RUN --runner sequential --perspectives <ids of panel.perspectives, comma-separated> --protocol <protocol> --rounds <rebuttal_rounds> --batches <max_batches> --verifiers <verifiers>
   ```

   With `independent` now false, `panel.py report` adds the reduced-independence notice.
2. Keep every valid message file already written in `$RUN`.
3. Continue with `runners/sequential.md` at the step that failed.
