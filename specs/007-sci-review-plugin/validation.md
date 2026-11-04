# Validation record: sci-review plugin

Date: 2026-11-04. Worktree branch `feature/scientific-codebase-review-7a7fbc`. This file records every validation run of quickstart.md, as required by tasks.md.

## 1. Static checks (quickstart.md section 2)

| Command | Result |
|---------|--------|
| `claude plugin validate . --strict` (Claude Code 2.1.317) | Pass |
| `claude plugin validate ./plugins/sci-review --strict` | Pass; one warning, ICON_MISSING, also raised for `project-kit` |
| `claude plugin validate ./plugins/project-kit --strict` | Pass |
| `python3 .github/scripts/check_manifests.py` | Pass: "marketplaces and plugin manifests are consistent" |
| `python3 plugins/sci-review/scripts/build_workflow.py --check` | Pass: the generated section is up to date |
| `python -m unittest tests.test_sci_review_panel tests.test_sci_review_workflow_build` | 84 tests pass on Python 3.10, 3.12 and 3.14 (73 at first record; 84 after the corrections of section 4.3; 86 on Python 3.14 after the correction of section 4.7), with Node.js 22.23 for the parity and simulation tests |
| `uv run --no-project --python 3.12 python -m unittest discover -s tests` | 119 tests, 2 failures, both in `test_new_project` and both pre-existing: they compare `/var/...` with `/private/var/...`, a macOS temporary-directory symlink; this feature does not touch those files |
| `ruff check` and `ruff format --check` on `plugins/sci-review/scripts/`, `tests/test_sci_review_*.py`, `tests/fixtures/sci-review/`, `.github/scripts/` | Pass |

## 2. Deterministic checks on the seeded fixture (quickstart.md sections 4 and 5, script steps only)

Fixture built with `python3 tests/fixtures/sci-review/seeded-repo/build.py --out <dir>`: 11 seeded defects (each dimension in Python and in TypeScript), 4 look-alikes, 1 contested construct.

| Check | Result |
|-------|--------|
| `scope --mode branch` | Base is the merge-base with `main`; 12 files, 405 lines (413 after the redesign of section 4.4); every seeded line is in a scoped range |
| `scope --mode repository` | 20 files, 490 lines |
| `scope --mode paths --path src/sci/core` | 8 files under `src/sci/core`; the 12 other files recorded as "outside paths" |
| `scope --mode branch --budget 200` | 6 files, 196 lines reviewed; 6 files recorded as "over budget" |
| Fixture clone with no branch and no remote | Exit 3: "no base branch could be determined ... name a baseline with --baseline REF, or review with --mode repository or --mode paths" |
| `score.py --verify-fixes` on `feature` (SC-007, before fixes) | 9 of 9 reproduction checks fail, each reproducing its stated wrong output |
| `score.py --verify-fixes` after correct fixes in a copy (by the fixture author) | 9 of 9 pass |
| Tree checksum and `git status --porcelain` before and after the script steps (SC-004) | Unchanged |
| `select-extensions` on the idfkit building-energy fixture, extension not installed (SC-012, second half) | `recommended building-energy-sci-review-extension: not installed; it would apply to models/office.idf. Install it with idfkit@idfkit.` |
| `select-extensions` on that fixture with the idfkit extension declaration | `selected` (applies to `models/office.idf`, `src/bem/climate.py`, `src/bem/climate.ts` and 4 more) |
| `select-extensions` with the contract-only test extension and its invalid copy (SC-013, selection only) | Valid copy selected when a scoped file matches (unit test `test_contract_only_test_extension`); invalid copy `failed: contract_version 2 is not supported (supported: 1)` |
| idfkit model checks (`checks.md`, route B through the pinned idfkit-mcp) on the fixture IDF | One finding: `E009 BuildingSurface:Detailed 'Office North Wall'.construction_name` references a missing construction; the case-insensitive look-alike is not flagged; no simulation run |
| Workflow script under Node.js with stub agents replaying the golden messages | Returns a PanelRun that `panel.py ingest`, `adjudicate` and `report` turn into the golden report; independent-round prompts hold no other perspective's output (SC-011); debate stops when no stance changes |

## 3. Install separation and Codex (research R11, quickstart.md section 3, T081, T082)

Run of 2026-11-04. The Codex CLI was repaired by reinstalling `@openai/codex` globally (its native binary had been missing); `codex --version` reports `codex-cli 0.166.0`. Every run below used an empty configuration directory (`CODEX_HOME` for Codex; `HOME` and `CLAUDE_CONFIG_DIR` for Claude Code 2.1.317) in the session scratchpad, so the user's own configuration was not read or changed.

### 3.1 Codex marketplace precedence (T081)

| Repository layout | `codex plugin list -m project-kit` reads | Plugins offered |
|-------------------|------------------------------------------|-----------------|
| Both `.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json` (this repository) | `.agents/plugins/marketplace.json` | `sci-review` only |
| Copy with `.claude-plugin/` and `plugins/` only | `.claude-plugin/marketplace.json` | `project-kit` and `sci-review` |

Codex prefers `.agents/plugins/marketplace.json` when both files exist and falls back to the Claude marketplace otherwise. The Codex marketplace is therefore required to keep `project-kit` off Codex (FR-001a), and no explicit marketplace path is needed. The install commands are:

```bash
codex plugin marketplace add <repository path, or owner/repo>
codex plugin add sci-review@project-kit
```

### 3.2 Install separation (T082)

| Host and install | Result |
|------------------|--------|
| Codex: `codex plugin add sci-review@project-kit` | `installed, enabled`, version 0.1.0; the cache holds `skills/scientific-review/SKILL.md`, `agents/`, `scripts/` and `workflows/` |
| Codex: model-visible skill list (`codex debug prompt-input`, no model call) | Lists `scientific-review` from the installed plugin; no project-kit skill from the plugin. The one project-kit skill name present, `stacked-prs`, comes from the user's personal `~/.agents/skills/`, which Codex reads from `HOME` and is unrelated to this marketplace |
| Claude: only `sci-review@project-kit` | `claude plugin details`: skill `scientific-review`, agent `scientific-auditor`; `workflows/scientific-review.js` present in the plugin cache; no project-kit component |
| Claude: only `project-kit@project-kit` | 9 project-kit skills and agent `editor`; no `scientific-review`, `scientific-auditor` or `scientific-review.js` in the cache |

FR-001, FR-001a and SC-006 pass.

## 4. Live review on the Claude Workflow runner (quickstart.md section 4, T047 in part, T051)

Run of 2026-11-04 on the seeded fixture (branch `feature`, 12 files, 405 lines), five default perspectives, defender and moderator, 2 rebuttal rounds, at most 2 batches, no extension selected. The Workflow ran 38 agents in 257 s (3.42 million subagent tokens): 5 independent reviews, 2 merge rulings, 29 debate positions over 2 batches and 2 moderator notes. Batch 1 ran rounds 0 to 2; batch 2 stopped after round 1 with no stance changed. `panel.py ingest` accepted all 38 messages and dropped none; `adjudicate` gave 13 consensus, 0 majority, 0 contested and 0 rejected findings.

### 4.1 Scores (`score.py report.json --run RUN`)

| Criterion | Verdict | Result |
|-----------|---------|--------|
| SC-001 recall | Pass | 11 of 11 seeded defects; every dimension and both languages at 100% |
| SC-002 look-alikes | Pass | 0 of 4 look-alikes reported (after the scorer correction of section 4.3, item 3) |
| SC-003 FR-014 fields | Pass | 13 of 13 findings complete |
| SC-004 project unchanged | Fail, corrected | `git status --porcelain` unchanged, but 7 `__pycache__/*.pyc` files appeared: panel members imported fixture modules to check claims, and `.gitignore` hid the cache from the check (section 4.3, item 2) |
| SC-008 panel versus best single perspective | Fail | Each perspective alone detected 11 of 11 defects with 0 false positives, so the panel (11 of 11, 0 false positives) cannot exceed the best single perspective; the fixture does not discriminate at this capability level |
| SC-009 false positives rejected in debate | Pass | No independent-round false positive at a look-alike |
| SC-010 contested construct | Fail | `geometry.py` `elevation_gain` labelled consensus: all five perspectives raised it, and the defender accepted it in round 0, because the docstring defines lengths along the slope and inclines in radians without restricting the range, so `L * theta` contradicts the documented contract; the moderator notes give no argument against and no deciding assumption |
| SC-011 independence | Pass | None of the five independent-round prompts in the Workflow transcripts contains another perspective's finding id; each states the project root |
| SC-007 reproduction after fixes | Not run | The High findings' fixes were not applied in a copy of the fixture during this run |

One finding beyond the seeded set, F1001 (low, `preprocess.py:33`: `math.ceil` applied to a rounded floating-point product, for example `ceil(0.3 * 10) = 4`), was split from the scaler cluster by the moderator; it is a real defect and is not a look-alike.

### 4.2 Interpretation

1. **Detection.** Recall and precision are at the ceiling for every perspective, so the fixture measures no benefit of the panel over a single reviewer (SC-008). A discriminating fixture needs defects that only one perspective's expertise exposes.
2. **Contested construct.** The construct is not contested under its own documentation: a reviewer who reads "measured along the slope, in radians" has no reason to assume small angles. For SC-010 to be testable, the fixture must give the approximation a documented basis that leaves its validity open, for example a comment that survey inclines are gentle, with no bound and no check.

### 4.3 Corrections made from this run

1. **Project root.** The Workflow gave agents scope paths relative to the project but not the project root, which works only when the project is the session's working directory. The Workflow now takes a `project` argument and states it in every prompt (`runners/claude-workflow.md`, contracts/invocation.md section 4; test `test_project_root_is_stated_in_every_prompt`). This run used the corrected script.
2. **Bytecode cache.** Every panel-member instruction (the Workflow's common rules, `agents/scientific-auditor.md`, the Codex panelist template and `SKILL.md` rule 5) now requires `python3 -B`, and every project check uses `git status --porcelain --ignored`, so that a write to an ignored path is reported.
3. **Scorer.** `score.py` counted F4 (the seeded `permutation_pvalue` defect at lines 22 to 39) as a false positive at the `bootstrap_means` look-alike (lines 10 to 19), because the 3-line tolerance joined the ranges. A finding that matches a seeded defect is no longer counted at a look-alike, as `is_false_positive` already did for SC-008.

### 4.4 Contested construct redesigned after this run

The construct of SC-010 was redesigned so that its validity is a genuine question rather than a contradiction of the documented contract. `src/sci/core/geometry.py` now states that the paths follow graded roads and footpaths, that inclines are read from a clinometer with a stated accuracy of 0.5 degrees (0.0087 rad), and that the rise of a segment is taken as `length * incline`, the first-order form of `length * sin(incline)`. The code is unchanged and still neither bounds nor checks the inclines.

| Quantity | Value |
|----------|-------|
| Truncation error of the rise | about L θ³ / 6 |
| Instrument error of the rise | L cos θ × 0.0087 |
| Crossover incline | 0.366 rad (21.0 degrees); relative error 2.3% |
| Relative error at 14 and 30 degrees | 1.0% and 4.7% |

The argument for a defect is that footpaths can exceed 21 degrees and nothing restricts the input; the argument against is that the approximation is documented and, below the crossover, smaller than the measurement error. The manifest entry (`ct-py-small-angle-elevation`, lines 14 to 30) records this as the expected deciding assumption. Because a finding is labelled `contested` only when the perspectives themselves divide (protocol.md section 5, rules 4 to 6), the label depends on the reviewers' judgement, and SC-010 can be confirmed only by a further live run. `build.py --check` verifies all 16 manifest entries, and the 9 reproduction checks still fail on `feature` before fixes.

### 4.5 Sequential runner (T076, SC-005)

Run of 2026-11-04 on a fresh build of the fixture (branch `feature`, 12 files, 413 lines, after the redesign of section 4.4), in this conversation with `panel.py panel --runner sequential`: five default perspectives, defender and moderator, 2 rebuttal rounds, at most 2 batches, no extension discovered. The perspectives were performed one at a time by `runners/sequential.md`, each candidates file written and validated before the next brief was read. Every message (5 candidates files, 2 merge rulings, 24 position files, 2 notes files) passed `panel.py validate` at the first attempt. `merge` gave 12 clusters in 2 batches; the moderator split C3 (`preprocess.py`: leakage, and the ceiling of the test-set size) and C9 (`normalise.ts`: NaN for a constant batch, and a RangeError from spreading a large batch), giving 14 merged findings. Both batches stopped after round 1 with no stance changed. `adjudicate` gave 12 consensus, 1 majority (F1, parallel sum order: the experimentalist held that the difference is below meter accuracy), 1 contested (F7) and 0 rejected findings.

| Criterion | Verdict | Result |
|-----------|---------|--------|
| SC-005 sequential against Workflow | Pass | 11 of 11 seeded defects, the same set as the Workflow run of section 4.1 (11 of 11); difference 0, within the tolerance of one |
| FR-028 notice | Pass | The Panel section states "The perspectives were not independent agents", and the Notices section carries the reduced-independence sentence |
| SC-001 recall | Pass | 11 of 11; every dimension and both languages at 100% |
| SC-002 look-alikes | Pass | 0 of 4 reported |
| SC-003 FR-014 fields | Pass | 14 of 14 findings complete |
| SC-004 project unchanged | Pass | Tree checksum of tracked files unchanged; `git status --porcelain --ignored` empty before and after |
| SC-010 contested construct | Pass, see limits | F7 labelled contested (2 accept, 3 challenge) with both arguments; deciding assumption: whether the surveyed graded roads and footpaths include segments steeper than about 21 degrees |
| SC-008, SC-009 | Not meaningful for this runner | `score.py` reports a pass (panel 11 of 11 against 5 of 11 for the best perspective), but one reviewer divided the findings among the perspectives, so the comparison measures that division, not the benefit of a panel |

Two findings beyond the seeded set were reported, both counted by `score.py` against a seeded defect in the same cluster: F1001 (low, `preprocess.py:33`, `ceil(0.07 * 100) = 8` because the product evaluates to 7.000000000000001), and F1002 (medium, `normalise.ts:16-17`, `Math.min(...readings)` throws a RangeError for 200,000 readings in Node.js 22). Section 4.1 gave `ceil(0.3 * 10) = 4` as the example for F1001, but that product evaluates to exactly 3.0; 0.07 * 100 and 0.14 * 100 are correct examples.

Limits of this run as evidence:

1. **Prior knowledge.** The reviewer did not read `manifest.json` before scoring, but had read sections 4.1 to 4.4 of this record, which name the contested construct, the `permutation_pvalue` defect and the `ceil` finding. Recall and the SC-010 result are therefore an upper bound for a reviewer without that knowledge.
2. **Single reviewer.** Every stance in the debate, including the 3 to 2 division on F7, was written by one reviewer. The contested label shows that the protocol, the scripts and the report handle a divided panel end to end; it does not show that independent agents would divide in the same way. SC-010 with independent agents remains for the Workflow re-run of T047.

### 4.6 Claude Agent runner (T047 in part, SC-007)

Run of 2026-11-04 on a fresh build of the fixture (branch `feature`, 12 files, 413 lines), with `panel.py panel --runner claude-agents`: five default perspectives, defender and moderator, 2 rebuttal rounds, at most 2 batches, no extension discovered. The orchestrator followed `runners/claude-agents.md` step by step: 5 independent reviewers launched in one message, 2 merge moderators, 12 round-0 members, 12 round-1 members and 2 notes moderators, 33 agents in all (about 3.0 million subagent tokens). Each prompt was the runner's template of section 4, generated from `panel.json` with absolute paths only.

**Deviation.** The `sci-review:scientific-auditor` agent type was not available, because the plugin is not installed in the session that ran the review. Each agent was therefore launched as `general-purpose`, with the body of `agents/scientific-auditor.md` placed verbatim before the runner's task template. Unlike the auditor, these agents had file-writing tools; the auditor's rule 3 still restricted them to their output file. Section 6 of the runner would have fallen back to the sequential runner; the substitution was chosen to exercise the agent protocol itself.

**Course of the run.** All 33 messages passed `panel.py validate` at the first attempt; no output was returned and none was dropped. `merge` gave 11 clusters in 2 batches, each cluster holding one candidate from each of the five perspectives; neither moderator split a cluster. Every member, the defender included, accepted every finding in round 0 and again in round 1, so both batches stopped after round 1. `adjudicate` gave 11 consensus, 0 majority, 0 contested and 0 rejected findings. One agent wrote and deleted a helper file inside `$RUN`; no file outside `$RUN` was written.

| Criterion | Verdict | Result |
|-----------|---------|--------|
| SC-001 recall | Pass | 11 of 11 seeded defects; every dimension and both languages at 100% |
| SC-002 look-alikes | Pass | 0 of 4 reported; all four were recorded as checked items by at least one perspective |
| SC-003 FR-014 fields | Pass | 11 of 11 findings complete |
| SC-004 project unchanged | Pass | Tree checksum of tracked files unchanged; `git status --porcelain --ignored` empty before and after, so the `python3 -B` rule of section 4.3 held |
| SC-007 reproduction after fixes | Pass | Before any fix, 9 of 9 checks fail, each reproducing its stated wrong output. After applying, in a clone of the fixture, the recommended fix of each of the 8 High findings (F2, F3, F5, F6, F7, F9, F10, F11) as written, the 8 corresponding checks pass; the ninth, `ts-rescale-zero-span`, belongs to the medium finding F8 and still fails, as expected |
| SC-008 panel against best single perspective | Fail | Each perspective alone detected 11 of 11 with 0 false positives, as in section 4.1; the fixture does not discriminate |
| SC-009 false positives rejected in debate | Pass | No independent-round false positive |
| SC-010 contested construct | Fail | Not reported. All five perspectives recorded `geometry.py:14-30` as a checked item: each judged that the documented first-order model stays below the 0.5 degree clinometer error for the inclines of graded roads (0.15 to 0.37 rad), which their briefs exclude as "a documented approximation whose stated regime covers the inputs in scope" |
| SC-011 independence | Pass | Each independent-round prompt listed only `protocol.md`, the dimension documents and `scope.json`; no transcript of the five independent-round agents contains the path of another perspective's candidates file |
| FR-028 | Pass | The Panel section states "The perspectives were independent agents"; no reduced-independence notice |

**Observations.**

1. **Contested construct.** After the redesign of section 4.4, independent reviewers read the construct as within its documented regime, unanimously, so it is neither reported nor contested. The sequential run of section 4.5 labelled it contested only because its single reviewer knew of it in advance. The construct now errs on the side of being correct: SC-010 needs a construct whose documented regime leaves the inputs in scope genuinely open, for example a module docstring that names both graded roads and unsurfaced hill paths.
2. **Severity spread.** The perspectives disagreed on severity (F1 low or medium, F7 and F9 medium or high); the merge kept the highest, and every member accepted the merged severity in round 0. Severity is not debated as such, which matches protocol.md section 4.
3. **One candidate, two defects.** `numerical-analyst-9` reported both NaN for a constant batch and the RangeError of `Math.min(...readings)` for large batches. A merge ruling cannot place one candidate in two findings, so the moderator kept the second defect only in the fix field of F8, and it was never debated. A rule that a candidate states one defect, in the perspective briefs, or a moderator option to split a candidate, would close this gap.
4. **Schema validation by agents.** Several agents reported that they could not validate their output because `jsonschema` is not installed; `panel.py validate` accepted every file regardless. The auditor's rules could name `panel.py validate` as the check, or state that the orchestrator validates.

### 4.7 Codex runner (T047 in part)

Run of 2026-11-04 with Codex CLI 0.166.0 (signed in with ChatGPT; feature `multi_agent` stable and enabled), after installing the plugin in the user's Codex configuration with `codex plugin marketplace add <repository>` and `codex plugin add sci-review@project-kit`. The review was started non-interactively in a fresh build of the fixture:

```bash
codex exec --sandbox workspace-write --add-dir "$TMPDIR" -C <fixture> --json "Use the sci-review scientific-review skill to review this branch for scientific correctness. Keep the run directory and give me its absolute path at the end."
```

Codex selected the `codex-subagents` runner and recorded the default panel (five perspectives, defender and moderator, 2 rebuttal rounds, 2 batches). It spawned 38 subagents in about 16 minutes; the orchestrator's own turn used 5.25 million input tokens, 99% of them cached. Codex allows 4 active agents including the orchestrator, so every step ran in waves of at most 3 subagents, as runner section 2 rule 2 provides. All 41 message files pass `panel.py validate`. Batch 1 stopped after round 1; batch 2 ran to round 2. `adjudicate` gave 10 consensus findings and 1 rejected finding.

| Criterion | Verdict | Result |
|-----------|---------|--------|
| SC-001 recall | Pass | 10 of 11 (91%); every dimension and both languages have at least one detection; statistical integrity 2 of 3, Python 5 of 6 |
| SC-002 look-alikes | Pass | 0 of 4 reported |
| SC-003 FR-014 fields | Pass | 10 of 10 findings complete |
| SC-004 project unchanged | Pass | Tree checksum of tracked files unchanged; `git status --porcelain --ignored` empty before and after |
| SC-008 panel against best single perspective | Fail | Four perspectives each detected 11 of 11 in the independent round; the panel reported 10, so the debate lost a true defect (below) |
| SC-009 false positives rejected in debate | Pass | No independent-round false positive |
| SC-010 contested construct | Fail | Not reported; `geometry.py:14-30` is a checked item, judged within its documented regime, as in section 4.6 |
| SC-011 independence | Fail | See below |
| FR-028 | Pass | The Panel section states "The perspectives were independent agents" |

**Defect lost in debate.** All five perspectives raised the seeded `permutation_pvalue` defect (F4: `random.shuffle` on the global generator, with no `rng` parameter). Every candidate stated its trigger as the same call under two different `random.seed` values. In round 0 the defender objected that a different seed is a different Monte Carlo experiment and that resetting the global seed reproduces the result; in round 1 every raiser withdrew, and rule 1 of protocol.md section 5 rejected the finding as `withdrawn`. The objection answers the trigger as stated, not the defect: a trigger in which other code draws from the global generator between `random.seed` and the call, or a second call in the same process, defeats it. The perspective briefs could require, for a reproducibility finding, a trigger in which the documented or obvious seeding fails, not one that changes the seed.

**Independence (SC-011).** `spawn_agent` was called without `fork_turns`, and Codex then makes a full-history fork: each subagent starts with a copy of the orchestrator's conversation. Because the independent round ran in waves, the methodologist and computer-scientist reviewers of wave 2 inherited the wave-1 completion messages, which give the path of the theorist's and numerical analyst's candidates files and a one-sentence summary of each (for example, "Recorded 11 concrete candidate findings and eight checked items"). Their session records show no tool call that read either file, so the inherited content was a count and a path, not a finding; but the criterion requires that no independent-round input contain another perspective's output, and these inputs did. The debate members were also full-history forks, so their context exceeded the inputs of protocol.md section 3. **Correction made from this run.** `runners/codex-subagents.md` section 2 now requires `fork_turns` set to `"none"` in every spawn (rule 4), so that a subagent starts from its task message alone, and section 6 falls back to the sequential runner when the host offers no way to spawn without a history fork. contracts/codex-orchestration.md section 1 states the same rule, and the tests `TestCodexRunnerIndependence` check both. The installed copy of the plugin in `~/.codex/plugins/cache/` predates the correction; `codex plugin add sci-review@project-kit` refreshes it before the re-run.

### 4.8 Codex runner after the fork correction (T047 in part)

Run of 2026-11-04, after refreshing the installed plugin with `codex plugin add sci-review@project-kit`, with the same `codex exec` command as section 4.7 on a fresh build of the fixture. Codex spawned 33 subagents in waves of at most 3; the orchestrator's turn used 4.40 million input tokens, 98% cached. All 33 message files pass `panel.py validate`. Both batches ran to round 2. `adjudicate` gave 11 consensus findings and 1 rejected finding.

| Criterion | Verdict | Result |
|-----------|---------|--------|
| SC-001 recall | Pass | 11 of 11; every dimension and both languages at 100% |
| SC-002 look-alikes | Pass | 0 of 4 reported |
| SC-003 FR-014 fields | Pass | 11 of 11 findings complete |
| SC-004 project unchanged | Pass | Tree checksum of tracked files unchanged; `git status --porcelain --ignored` empty before and after |
| SC-008 panel against best single perspective | Fail | Each perspective alone detected 11 of 11; the fixture does not discriminate |
| SC-009 false positives rejected in debate | Pass | No independent-round false positive at a look-alike |
| SC-010 contested construct | Fail | Raised, then rejected (below) |
| SC-011 independence | Pass | No subagent session records a `forked_from_id`, and none contains the user's request or the orchestrator's conversation. Each independent-round session references only its own candidates file, and each round-0 member only its own, as protocol.md section 3 allows |
| FR-028 | Pass | The Panel section states "The perspectives were independent agents" |

**Contested construct.** Unlike the earlier runs, one perspective, the experimentalist, raised `geometry.py:14-30` as a candidate (F7). In round 0 the defender challenged it on the documented first-order model (lines 3 to 5 and 17 to 18); the experimentalist withdrew, and rule 1 of protocol.md section 5 rejected it as `withdrawn`. The outcome supports observation 1 of section 4.6: the documentation as it stands settles the construct in favour of the code.

**Debate outcomes vary between runs.** The seeded `permutation_pvalue` defect, rejected in section 4.7, is a consensus finding here with the same kind of trigger (two global seeds): the defender did not challenge it. The outcome of a finding whose trigger admits an answer therefore depends on whether the defender raises that answer, which supports the proposal of section 4.7 to require a trigger that the obvious defence does not defeat.

### 4.9 Corrections made from sections 4.6 to 4.8

1. **One defect per finding** (section 4.6, observation 3). Rule 6 of the independent round in each default perspective brief now states that each finding states one defect, and that two defects at the same location are reported as two findings, each with its own trigger, wrong output and fix.
2. **Triggers that survive the obvious defence** (sections 4.7 and 4.8). Rule 4 of the independent round in each default perspective brief now requires a trigger that the obvious defence does not answer; for a reproducibility or seeding defect, a program state in which the documented or customary seeding still fails to reproduce the result, not a change of seed.
3. **No validator installs** (section 4.6, observation 4). Rule 3 of `agents/scientific-auditor.md` and of the Codex panelist template `codex-agents/sci-review-panelist.toml` now tell a member not to install a package to validate its output, but to check it against the schema by reading it, since the orchestrator validates it with `panel.py validate`. Workflow agents return structured output and need no such rule.

The Workflow script was regenerated with `build_workflow.py`, since it embeds the briefs. The building-energy extension brief in the idfkit plugin copies the default rules and received the same two additions. Tests `TestPanelMemberRules` check all three; 89 tests pass on Python 3.14.

## 5. Not yet run

These need live agent runs and, for the Workflow runner, the user's opt-in to a multi-agent workflow. The Codex CLI works since section 3. They remain open in tasks.md.

| Task | Run |
|------|-----|
| T047 | A Workflow re-run after the corrections of sections 4.3 and 4.4; SC-010 needs a construct redesigned once more (section 4.6, observation 1) |
| T056 | The review parts of quickstart.md section 5 (defects reported in both directories in repository mode; none outside the path in path mode) |
| T071 | quickstart.md section 6 with live reviews (SC-012 first half, SC-013 contribution of findings) |
