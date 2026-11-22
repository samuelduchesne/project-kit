# Validation: bounded-cost scientific review

Measured on 2026-11-22 against the seeded fixture of feature 007 (`tests/fixtures/sci-review/seeded-repo`), at `medium`, branch mode: 17 files, 526 lines, 1 review part. Both runs used the `claude-workflow` runner, the same model for every agent, empty preferences, and were scored with `score.py report.json --run RUN`.

## 1. Method

1. The fixture was built twice with `build.py`, once per run, with `feature` checked out.
2. The opening steps of SKILL.md (`init`, `args`, `scope`, `parts`, `select-extensions`, `panel --runner claude-workflow`) ran with the `panel.py` of each version: commit `1be2c00` (before) and this branch (after).
3. The panel Workflow script of each version was copied to the scratchpad and launched with the arguments of `runners/claude-workflow.md`.
4. The result was ingested, adjudicated and reported, then scored. Agent counts and subagent tokens are those the Workflow tool reported.
5. `git status --porcelain --ignored` showed both fixtures unchanged.

## 2. Results

| Measure | Before (debate) | After (verify) |
|---------|-----------------|----------------|
| Panel | 5 perspectives, defender, moderator; 2 rebuttal rounds; 2 batches | theorist, numerical analyst, methodologist (focused); 1 verifier; 2 batches |
| Agents | 34 | 7 (estimate before the run: 3 to 7) |
| Subagent tokens | 3,431,166 | 725,233 (21%) |
| Tool calls | 61 | 19 |
| Wall time | 526 s | 227 s |
| SC-001 recall (feature 007) | 16 of 16 | 16 of 16 |
| SC-002 look-alikes reported | 0 of 4 | 0 of 4 |
| SC-003 complete fields | 17 of 17 | 17 of 17 |
| SC-010 contested construct | Fail (consensus) | Pass (contested, with both arguments and the deciding assumption) |
| Labels | 17 consensus | 16 consensus, 1 contested |

Tokens by phase:

| Phase | Before: agents, tokens | After: agents, tokens |
|-------|------------------------|-----------------------|
| Independent | 5, 540,123 | 3, 325,856 |
| Merge | 2, 240,871 | 2, 208,721 |
| Debate | 25, 2,439,227 | — |
| Notes | 2, 210,945 | — |
| Verify | — | 2, 190,656 |

## 3. Success criteria of this feature

- **SC-001** (recall at least that of the debate, no look-alike): pass, 16 of 16 and 0.
- **SC-002** (at most a quarter of the agents, at most a third of the tokens): pass, 7 of 34 agents (21%) and 21% of the tokens.
- **SC-003** (feature 007 and 008 debate tests pass): pass, 247 tests pass, golden reports changed only by the new `protocol` and `verifiers` fields and the "Protocol: debate." line.

## 4. Observations

1. Every agent costs about 100,000 tokens whatever its task, so the number of agents sets the cost. Shorter prompts (no `protocol.md` in finder prompts) matter far less.
2. The focused finders still found almost everything outside their focus: the theorist and the numerical analyst each found 16 of 16. The three finders raised 50 candidates in 17 clusters, so both batches held overlapping candidates and needed the merge moderator. The merge is now the second-largest phase. A later change could merge clusters whose members agree on location and dimension without a moderator, which would save up to two agents at `medium`.
3. The verifier labelled the contested construct `contested`, with a deciding assumption that matches the fixture's, where the debate had reached consensus. A single verifier asked to name the assumption that settles a finding does this better than a panel that converges.
4. SC-008 of feature 007 (the panel beats its best single perspective) still fails, as in every recorded run: on this fixture one strong reviewer finds every seeded defect. The fixture does not show what extra finders buy, so `high` and `xhigh` are justified by verification depth, not by recall measured here.
5. The higher levels and the `sequential`, `claude-agents` and `codex-subagents` runners were not run live. Their logic is covered by unit tests and the Workflow simulation.
