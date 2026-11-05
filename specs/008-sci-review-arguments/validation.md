# Validation: code-review-style arguments

Validation record for tasks T066 to T068 of [tasks.md](./tasks.md), against the scenarios of [quickstart.md](./quickstart.md).

## 1. Status

| Task | Status | Remaining |
|------|--------|-----------|
| T066 (SC-009, seeded recall) | Done (section 3) | None. Recall 16 of 16, equal to the baseline. |
| T067 (manual scenarios 1 to 11) | Done | Steps before the panel verified (section 2); scenarios 1 and 2 run live interactively (sections 4.1 to 4.4); scenarios 3 to 11 run live in headless sessions (section 5). Open observations are listed in section 5.4. |
| T068 (cross-host) | Open | Requires a Codex session and a claude.ai session with the plugin installed. |
| T069 (separate large-scope confirmation) | Done | SKILL.md section 5 step 4 requires the question on its own; covered by a test. |
| T070 (Workflow copy from an installed plugin) | Done (section 6) | The copy is refused in a non-interactive `acceptEdits` session; the runner now falls back to the next runner. |

## 2. Steps before the panel (2026-11-05)

### 2.1 Method

The deterministic steps that the skill runs before launching any reviewer were driven directly through `panel.py`, in the order of SKILL.md section 5: `init`, `args --persist`, `scope`, `parts`, `panel --runner claude-workflow`, `clean`. The environment was:

- `XDG_CONFIG_HOME` set to a new temporary directory, so that preferences started empty;
- the seeded fixture of feature 007, built with `tests/fixtures/sci-review/seeded-repo/build.py`;
- `tests/fixtures/sci-review/large-scope/` copied to a temporary directory and committed as a git repository.

After each scenario, `git status --porcelain --ignored` and the current branch were compared with the state before it.

### 2.2 Results

| # | Arguments | Observed | SC-005 |
|---|-----------|----------|--------|
| 1 | (none) | Level `medium`, source `default`; 5 perspectives (theorist, numerical-analyst, experimentalist, methodologist, computer-scientist); 17 files, 526 lines, 1 part. | Unchanged |
| 2a | `low` | Level `low`, source `given`; 3 perspectives; `last_level: low` stored. | Unchanged |
| 2b | (none) | Level `low`, source `reused`; note "Using the effort level `low` from your last review; type a level to choose another." | Unchanged |
| 3a | `--max-findings 2` | Cap 2; `last_max_findings: 2` stored. | Unchanged |
| 3b | (none) | Cap 2 reused, with the note naming `--max-findings default`. | Unchanged |
| 3c | `--max-findings default` | Cap cleared; `last_max_findings` removed from preferences. | Unchanged |
| 4 | `--max-findings zero` | Arguments accepted (exit 0); note "`--max-findings` was ignored: type a whole number above zero, `all`, or `default` after it. Using the usual limit." | Unchanged |
| 5a | `hig` | Rejected by `scope` with exit 2: "`hig` is not a recognised level: use low, medium, high, xhigh or max." No `scope.json` was written, so `parts` exited 3; the driver script went on to `panel`, which the skill does not run after exit 2 (SKILL.md section 5, step 3). | Unchanged |
| 5b | `--post` | Rejected by `args` with exit 2, naming the accepted flags. | Unchanged |
| 5c | `ultra` | Rejected by `args` with exit 2, pointing to `max`. | Unchanged |
| 7 | `--comment` | `comment: true` on a branch target with no pull-request ref; the note that `--comment` was ignored is given by the skill at the posting step (SKILL.md section 7, step 6), not by `panel.py`. | Unchanged |
| 8 | `review-other` (not checked out; `main` checked out) | Branch mode on `review-other`; 18 files including the file committed only on that branch (`extra.py`). Current branch stayed `main`. | Unchanged |
| 10, 11 | (none), repository mode on `large-scope` | 17,782 lines in 9 parts of 1,965 to 1,994 lines; `confirm_required: true`; `solver/kernels.py` cut into lines 1 to 1,994 and 1,995 to 3,298; the last part holds `units/`; no file excluded; no run file contains "over budget". | Unchanged |

A first attempt at scenario 8 used a branch with no commit of its own; `scope` then exited 3 with the "has not diverged" message of SKILL.md section 3, as specified.

### 2.3 Not covered by this method

- The reviewers, the report and the reported findings (scenarios 1 to 4, 7, 8 and 10: report wording, withheld count, defect in the last file).
- The confirmation dialogue of scenarios 10 and 11, which the skill conducts.
- Scenario 6 (`--comment` on a pull request), which needs a throwaway GitHub repository and posts comments.
- Scenario 9 (`--fix`).

## 3. Seeded recall at `medium` (T066, SC-009, 2026-11-05)

### 3.1 Method

1. The seeded fixture of feature 007 was built with `tests/fixtures/sci-review/seeded-repo/build.py`, with `feature` checked out.
2. The opening steps of SKILL.md section 5 ran with this worktree's `panel.py` on the argument `medium`, with no other argument and with empty preferences. The result was:
   - level `medium`, given;
   - 17 files and 526 lines, in 1 part;
   - five perspectives, 2 rebuttal rounds and at most 2 batches;
   - the building-energy extension of idfkit 0.3.1 recorded as not applicable.
3. The panel ran on the `claude-workflow` runner, from this worktree's `workflows/scientific-review.js`. The installed plugin (0.1.0) predates feature 008, so it was not used.
4. The Workflow ran 33 agents with no error and dropped none. `ingest` accepted all 33 messages.
5. `adjudicate` and `report` ran, and the run was scored with `score.py report.json --run RUN`.
6. `git status --porcelain --ignored` showed the fixture unchanged.

### 3.2 Result

| Criterion | This run | Baseline (feature 007, validation.md sections 4.13 and 4.16) |
|-----------|----------|------------------------------------------------------------|
| SC-001 recall | 16 of 16; every dimension and both languages at 100% | 16 of 16 |
| SC-002 look-alikes | 0 of 4 reported | 0 |
| SC-003 complete fields | 17 of 17 | Complete |
| SC-008 panel against best single perspective | Fail: four perspectives alone found 16 of 16 and the numerical analyst 15 of 16, all with 0 false positives | Fail, same pattern |
| SC-009 (feature 007) false positives rejected in debate | Pass (none raised) | Pass |
| SC-010 contested construct | Fail: F10 (`geometry.py`), labelled consensus | Fail, same label |

Labels were 17 consensus, 0 majority, 0 contested and 0 rejected. The 17th finding is F10, the contested construct, which the fixture expects to be contested.

SC-009 of this feature holds: the review with arguments found 16 of 16 seeded defects, the same count as the baseline, so there is no decrease. The baseline cited in tasks.md (11 of 11) refers to the manifest before its extension to 16 defects in feature 007 section 4.13; the comparison above uses the current manifest. The SC-008 and SC-010 failures are open criteria of feature 007 (its section 5) and are not regressions.

## 4. Live scenarios (T067)

### 4.1 Scenario 1: no arguments (2026-11-05)

Setup: `~/sci-review-fixtures/seeded`, built with `build.py`, `feature` checked out; Claude Code 2.1.318 started with `claude --plugin-dir <worktree>/plugins/sci-review`, `XDG_CONFIG_HOME` set to a new temporary directory, and the installed `sci-review@project-kit` (0.1.0) disabled. Command: `/sci-review:scientific-review`.

| Check | Observed |
|-------|----------|
| Entry point | The skill (after the Workflow was renamed; section 4.2) |
| Arguments | `args --text-stdin` with the command text; level `medium`, source `default`, no cap |
| Scope and parts | Branch `feature` against `main` (`f134850`), 17 files, 526 lines, 1 part; building-energy extension not applicable |
| Panel | `claude-workflow` runner; five perspectives, 2 rebuttal rounds, at most 2 batches |
| Report | 18 findings, all consensus, delivered with `ReportFindings` (level `medium`); no cap applied, none withheld |
| SC-005 | `git status --porcelain --ignored` empty before and after; branch `feature`; no ref left under `refs/sci-review/` |

Result: pass. The panel found 18 findings here and 17 in the T066 run of the same scope; the count of a live panel varies between runs.

### 4.2 Defects found while setting up scenario 1

1. **Slash command reached the Workflow.** The panel Workflow and the skill had the same name, so `/sci-review:scientific-review` started the Workflow alone, which finished in 10 ms with "No scope was given." The Workflow was renamed `scientific-review-panel`; scenario 1 above ran with that layout and launched it by name. The script was then moved to `scripts/scientific-review-panel.js` and is launched by path, so that the plugin registers no Workflow and has a single slash command. In scenario 2a (section 4.3), the launch by path was refused; the script is now copied into the session's scratchpad and launched from there.
2. **`$PANEL` as a shell variable in zsh.** The orchestrating model first wrote `PANEL="python3 $SKILL/../../scripts/panel.py"` and `$PANEL args ...`; zsh does not split an unquoted variable, so the command failed, and the model replaced it with a shell function. The review then proceeded normally. Every definition of `$PANEL` (SKILL.md and the four runner files) now says to write the command out in full and never to store it in a shell variable; a test checks each definition.

### 4.3 Scenario 2a: `low` (2026-11-05)

Setup as in section 4.1, in a new session (new temporary `XDG_CONFIG_HOME`), with the panel script moved to `scripts/scientific-review-panel.js` and the `$PANEL` rule of section 4.2 in place. Command: `/sci-review:scientific-review low`.

| Check | Observed |
|-------|----------|
| Entry point | The skill; the slash menu listed one sci-review command |
| Arguments | Level `low`, source `given`; `panel.py` commands written out in full, with no shell variable |
| Panel launch | `Workflow({ scriptPath: <plugin>/scripts/scientific-review-panel.js })` refused four times: "scriptPath must be a script path this tool returned, or a file you can already read (the working directory or a directory you have added)", also after the model had read the file. The model copied the script into its scratchpad and launched the copy, which ran. |
| Report | 18 findings, delivered with `ReportFindings` (level `low`) |
| SC-005 | `git status --porcelain --ignored` empty after the run; branch `feature`; no ref left under `refs/sci-review/` |

Result: pass for the arguments and the report; the launch needed the workaround, which `runners/claude-workflow.md` now prescribes (copy to `$SCRATCH`, then launch; without a scratchpad, the Agent runner). The second run of scenario 2 is recorded in section 4.4.

### 4.4 Scenario 2b: no arguments after `low` (2026-11-05)

In the session of section 4.3, `/sci-review:scientific-review` with no arguments. `args` recorded level `low`, source `reused`, with the note "Using the effort level `low` from your last review; type a level to choose another.", and the model told the user it was reusing the saved level. The user then interrupted the run after the opening steps, so no panel ran; the copy-and-launch step of `runners/claude-workflow.md` has therefore not yet run as written in a live session. `git status --porcelain --ignored` was empty afterwards, on branch `feature`, with no ref under `refs/sci-review/`.

Result: pass for FR-007 (the level is reused and the user is told).


## 5. Live scenarios 3 to 11, headless (T067, 2026-11-05)

### 5.1 Method

Each scenario ran in a new non-interactive Claude Code session:

```text
CLAUDE_CONFIG_DIR=~/.claude claude -p "<command>" \
  --plugin-dir <worktree>/plugins/sci-review \
  --permission-mode acceptEdits \
  --allowedTools "Bash Read Grep Glob Agent Workflow Skill ReportFindings Edit Write" \
  --output-format stream-json --verbose
```

The conditions were as follows:

- Claude Code was version 2.1.318, and the installed `sci-review@project-kit` (0.1.0) was disabled.
- Each scenario had a new empty `XDG_CONFIG_HOME`.
- Where a scenario needed an answer from the user, the session was continued with `--resume <session-id> -p "<answer>"`.
- `git status --porcelain --ignored`, the current branch and `git for-each-ref refs/sci-review/` were recorded before and after every session.

The following fixtures were used:

- **`seeded`.** The fixture of feature 007, with `feature` checked out. A branch `review-other` was added from `main` with one seeded defect: `src/sci/thermal/conduction.py`, in which `heat_flux` multiplies by the wall thickness instead of dividing by it.
- **`fix`.** A clone of `seeded` with `review-other` checked out, used for scenario 9.
- **`large-scope`.** A copy of `tests/fixtures/sci-review/large-scope/`, committed as a single `init` commit on `main`.
- **`pr6`.** The private repository `samuelduchesne/sci-review-scenario6-throwaway`, created for scenario 6. Pull request 1 adds the `review-other` defect against `main`.

Two scenario pairs were combined to reduce the number of panel runs:

- 3a with 7, as `low --max-findings 2 --comment` on `feature`;
- 4 with 8, as `low review-other --max-findings zero`.

Every panel scenario except 11 used the level `low`. Scenarios 3b, 3c and 5 need no panel, and the reuse and clearing of the cap (3b, 3c) were already verified in section 2.

The total cost of the sessions in this section, as reported by Claude Code, was about USD 36.

### 5.2 Results

| # | Command | Observed | SC-005 |
|---|---------|----------|--------|
| 3a, 7 | `low --max-findings 2 --comment` on `feature` | Workflow runner; 18 consensus findings, 2 delivered with `ReportFindings`, and the report stated that 16 were withheld by the cap. The session said that `--comment` was ignored because the target is not a pull request, and posted nothing. | Unchanged; branch `feature`; no ref under `refs/sci-review/` |
| 4, 8 | `low review-other --max-findings zero`, with `feature` checked out | One line said: "`--max-findings zero` was ignored (a whole number above zero, `all`, or `default` is required); the usual limit (none) applies." The scope was branch `review-other` (one file, 16 lines). One consensus finding was reported: the seeded defect at `conduction.py:11`. | Unchanged; branch stayed `feature`; no ref |
| 5a | `hig` | Rejected by `scope`, exit 2: "`hig` is not a recognised level: use low, medium, high, xhigh or max." The run directory was cleaned and no reviewer started. | Unchanged |
| 5b | `--post` | Rejected by `args`, exit 2: "unknown flag `--post`: the accepted flags are --comment, --fix and --max-findings <n>\|all\|default." No preferences were stored. | Unchanged |
| 5c | `ultra` | Rejected by `args`, exit 2: "`ultra` is the cloud review of /code-review and is not available for the scientific review; use `max`." | Unchanged |
| 6 | `low 1 --comment` in `pr6` | The pull-request head was fetched into a temporary ref. One consensus finding (`conduction.py:11`) was delivered with `ReportFindings`. Because the GitHub inline-comment tool was absent, the session posted one inline comment on line 11 through `gh api` ([discussion_r4483365513](https://github.com/samuelduchesne/sci-review-scenario6-throwaway/pull/1#discussion_r4483365513)). The comment opens with the agreement label, severity and dimension. No finding was unanchorable. | Unchanged; branch `main`; temporary ref deleted |
| 9 | `low --fix` in `fix`, on `review-other` | One consensus finding was reported. The session changed `* thickness` to `/ thickness` on line 11, found no test suite, and ran the corrected function on the finding's trigger, which returned 8.0 W/m2 and 80.0 W as expected. The finding was then re-reported with `outcome: fixed`. Nothing was staged (`git diff --cached` was empty) and no reviewer agent was started for the fix. No finding was skipped. | `M src/sci/thermal/conduction.py` only, as expected for `--fix` |
| 10 | `low` in `large-scope`, then "Review the whole repository." | The first turn stopped at precondition 3 (no base: `main` is the only branch and has one commit) and asked for a mode, as SKILL.md section 3 requires. After the answer, the session ran repository mode: 17,782 lines, 25 files, 9 parts, and 37 agents on the Workflow runner. All parts completed and none was listed as over budget (no occurrence of "over budget" in either transcript). The single delivered finding was the seeded defect in `units/conversions.py`, the last file in path order (observation 3 in section 5.4). | Unchanged; branch `main` |
| 11 | (none) in `large-scope`, then "Review the whole repository.", then "no" | After the mode answer, the session said: "This scope has 17,782 lines in 25 files and will be reviewed in 9 parts. Continue?" After "no", it cleaned the run directory, started no reviewer, and offered named paths (`numerics solver`, `low thermal units`). | Unchanged; branch `main` |

### 5.3 Result

Scenarios 3 to 11 pass, subject to the observations below.

### 5.4 Observations

1. **Copying the Workflow script was refused in every headless session.** The copy prescribed by `runners/claude-workflow.md` was refused in sessions 3a/7, 6 and 9. The permission layer reported it as an edit of a sensitive file. The likely cause is the source path, which lies under `<repo>/.claude/worktrees/`; an installed plugin would not be under that directory. This was not verified. The three sessions recovered in different ways:
   - 3a/7 read the script and wrote an identical copy with `Write`;
   - 6 copied it with a shell redirection;
   - 9 switched to the `claude-agents` runner, as the runner selection of SKILL.md section 4 allows, and recorded the switch.

   The panel ran in every case. It should be checked whether the copy is refused for a plugin installed from the marketplace.
2. **In scenario 10, the confirmation was folded into the mode question.** When it asked for a mode, the session described the whole-repository option as about 9 parts over the 6,000-line limit and stated: "Choosing this option counts as your confirmation." It therefore did not ask the "Continue?" question of SKILL.md section 5 step 4 separately. The user had the line count and the part count before any reviewer ran, so the intent of FR-022 holds. However, the exact wording was shown only in scenario 11.
3. **The finding of scenario 10 was anchored five lines above the seeded line.** The finding names the correct file, function and inverted factor (3.412141633 instead of 0.29307107). Its line is 642, the definition of `WATTS_PER_BTU_PER_HOUR`, whereas the manifest gives line 647, the `return` statement. With the 3-line tolerance of `score.py`, a start line of 642 alone would not match. The run directory had been cleaned, so the finding's full line range could not be checked. The defect was found; the anchoring is outside the scoring tolerance.
4. **`gh` needs a token in headless sessions.** The first run of scenario 6 stopped before any reviewer ran, because `gh` inside the session could not read the keyring. The session correctly reported the `auth` precondition of SKILL.md section 3 and offered alternatives. The re-run with `GH_TOKEN` set in the environment is the one recorded above.
5. **Scenario 6 left a throwaway repository.** `samuelduchesne/sci-review-scenario6-throwaway` is private and can be deleted.

## 6. Workflow copy from an installed plugin (T070, 2026-11-05)

This section addresses observation 1 of section 5.4: whether the copy of the panel script into the scratchpad is also refused when the plugin is installed from the marketplace rather than loaded from a worktree.

### 6.1 Method

Two non-interactive sessions ran with Claude Code 2.1.318, `CLAUDE_CONFIG_DIR=~/.claude`, `--permission-mode acceptEdits` and `--allowedTools "Bash Read Write"`. Each was asked to run one command, `cp <source> <scratchpad>/probe-copy.txt`, to make no second attempt, and to report the outcome. Version 0.2.0 is not yet published, so the installed 0.1.0 cache stood in for an installed plugin; the refusal depends on the source path, not on the file's content.

| Probe | Source | Outcome |
|-------|--------|---------|
| Installed plugin | `~/.claude/plugins/cache/project-kit/sci-review/0.1.0/scripts/build_workflow.py` | Refused: "Claude requested permissions to edit <source> which is a sensitive file." |
| Control | a file in the session's scratchpad, outside every `.claude/` directory | Copied |

### 6.2 Result

The refusal is not specific to a worktree. It was observed for both sources tested under a `.claude/` directory: the worktree of section 5.4 and the plugin cache of the configuration directory. Every plugin installed from a marketplace lies in that cache. Other configuration directories (`CLAUDE_CONFIG_DIR`) were not tested. An interactive session can ask the user for permission instead of refusing; this was not tested.

### 6.3 Change

`runners/claude-workflow.md` step 3 now states that a refused copy leads to section 6 (fallback to `claude-agents`, else `sequential`, recorded with `panel.py panel --runner`). It forbids copying the script by another means. `SKILL.md` section 4 states the same fallback. `tests/test_sci_review_workflow_build.py` checks both sentences. The three ad hoc recoveries of observation 1 are therefore no longer permitted.
