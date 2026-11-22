# Runner: sequential

This runner performs the panel phases with the procedure of `protocol.md` section 12 in the orchestrating conversation, one task at a time, without spawning agents. It starts after the opening steps of `SKILL.md` (through `panel --runner sequential`) and ends before its closing steps (`adjudicate` onward).

Because one reviewer performs every role, the perspectives and verifiers are not independent agents. `panel.json` records `independent: false` for this runner, and `panel.py report` adds the reduced-independence notice (FR-028).

## 1. Performing a task

1. **One task at a time.** Before each task, state its task message (`protocol.md` section 12.3) in the conversation as a header, read the role brief, and work only from the inputs it lists. Write the output file, with a file-writing tool or a shell heredoc, and validate it before starting the next task. When validation fails, correct the message once from the validator's errors; after a second failure apply rule 12.2.3.
2. **Independent round.** Perform the perspectives in the order of `panel.perspectives`; each completes every part, in the order `p1`, `p2`, ..., before the next starts (feature 007 FR-028). While performing a perspective, do not reread, consult or refer to any candidates file of another perspective, or to your reasoning for it.
3. **Verify.** Perform the verifiers of a batch in turn. Judge each finding afresh from the code and the merged finding; do not refer to the verdicts already written for the batch, and do not refer to the reasoning that raised the finding.
4. **Debate.** In round 0, state each member's positions from the merge ruling and, for a perspective, its own candidates file only; do not revise or refer to positions already written in round 0. In round k >= 1, use only positions of rounds 0 to k-1.
5. When the host stops the review partway, the parts whose candidates files are missing are reported as not reviewed by `panel.py report`.
