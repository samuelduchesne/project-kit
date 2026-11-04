# Contract: Codex subagent runner

Text of `runners/codex-subagents.md`, in outline. The Claude Agent runner (`runners/claude-agents.md`) follows the same steps, replacing "spawn a subagent" with "launch a `sci-review:scientific-auditor` agent" and running launches of one step in a single message.

## 1. Preconditions

- Multi-agent tools are enabled (`agents.enabled`, default true). If spawning fails, switch to the sequential runner and add the notice.
- If `agents.max_concurrent_threads_per_session` is lower than the number of subagents in a step, spawn in waves; waves do not change any subagent's inputs.
- Every spawn sets `fork_turns` to `"none"`, so that a subagent starts from its task message alone and does not inherit the parent's history, which holds the completion messages of subagents already finished (SC-011).

## 2. Steps

1. **Opening steps** (owned by `SKILL.md`, shared by every runner): `panel.py init`, then `panel.py scope`, then extension discovery (contracts/extension.md) and `panel.py select-extensions`, then `panel.py panel --runner codex-subagents`. The runner file begins at step 2.
2. **Independent round**: spawn one subagent per perspective, all at once. Each task message contains only the inputs listed in contracts/panel-messages.md, the absolute path of its output file, and the instruction to write that file and nothing else. Wait for all; run `panel.py validate` on each output; return invalid outputs once.
3. **Merge**: `panel.py merge`; spawn one moderator subagent per batch, in parallel; validate rulings.
4. **Debate**: for each batch, as soon as its ruling is valid, run round 0 by spawning the perspectives and the defender in parallel; then rounds 1 to R, each spawned only after the previous round of that batch is complete. Stop a batch early when no stance changed; in later rounds, call only the members that `panel.py debate-status` lists: those whose stance changed, plus the perspectives that accept a finding someone newly challenged. Absent members keep their latest position.
5. **Moderator notes**: for each batch, as soon as its debate ends, spawn one moderator subagent to write `notes/batch-<b>.json` for every finding of the batch; validate.
6. **Closing steps** (owned by `SKILL.md`, shared by every runner): `panel.py adjudicate`, which computes labels and attaches the notes; `panel.py report`; delivery per contracts/report.md section 3; `panel.py clean` unless the user asked to keep the run directory. The runner file ends at step 5.

## 3. Rules

- The parent never summarises one subagent's output into another subagent's task, except as the files listed for that phase.
- Subagents inherit the parent's sandbox; each is told not to modify files outside `$RUN`. The parent verifies with `git status --porcelain --ignored` before and after the review and reports any change (SC-004).
- The optional `sci-review-panelist` custom agent may be named in spawns when the user has installed it; otherwise the built-in `default` agent is used.
