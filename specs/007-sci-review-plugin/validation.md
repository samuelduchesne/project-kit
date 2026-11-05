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

One finding beyond the seeded set, F1001 (low, `preprocess.py:33`: `math.ceil` applied to a rounded floating-point product, for example `ceil(0.07 * 100) = 8`, because the product evaluates to 7.000000000000001), was split from the scaler cluster by the moderator; it is a real defect and is not a look-alike.

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

Two findings beyond the seeded set were reported, both counted by `score.py` against a seeded defect in the same cluster: F1001 (low, `preprocess.py:33`, `ceil(0.07 * 100) = 8` because the product evaluates to 7.000000000000001), and F1002 (medium, `normalise.ts:16-17`, `Math.min(...readings)` throws a RangeError for 200,000 readings in Node.js 22). Section 4.1 first gave `ceil(0.3 * 10) = 4` as the example for F1001, but that product evaluates to exactly 3.0; section 4.1 now gives `ceil(0.07 * 100) = 8` (T102).

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

### 4.10 Scope modes (T056, quickstart.md section 5)

Runs of 2026-11-04 on a fresh build of the fixture with the sequential runner, five default perspectives, defender and moderator, 2 rebuttal rounds and at most 2 batches. The reviewed code is byte-identical to that of the branch run of section 4.5, so the perspectives made the same judgements; each review recorded additional checked items for the lines that only its scope contains (for example `trapezoid` in `quadrature.py` and the README in repository mode). Every message passed `panel.py validate` at the first attempt, and both batches of each review stopped after round 1.

| Check | Verdict | Result |
|-------|---------|--------|
| Repository mode (`scope --mode repository`) | Pass | Scope "All files of the repository: 20 files, 498 lines". 14 findings (12 consensus, 1 majority, 1 contested): 8 in `src/sci/core` and 6 in `src/sci/analysis`, so defects in both seeded directories are reported. `score.py`: 11 of 11 seeded defects, every dimension and both languages at 100%; 0 look-alikes; 14 of 14 findings complete |
| Path mode (`scope --mode paths --path src/sci/core`) | Pass | Scope "Files under src/sci/core: 8 files, 237 lines". 8 findings (7 consensus, 1 contested), all under `src/sci/core`; no finding outside the path. The Not reviewed section lists the 12 other files with the reason "outside paths" (US3 scenarios 2 and 3). The methodologist raised no finding and recorded no checked item, since its judgements in the branch run all concern `src/sci/analysis` |
| No base | Pass | Recorded in section 2: a clone with no branch and no remote exits 3 with the message that asks for a baseline or another mode |
| Budget of 200 lines (`--budget 200`) | Pass | 6 files and 196 lines reviewed; the Not reviewed section lists the 6 remaining files with the reason "over budget". `report` requires `adjudicate` to have run, as in `SKILL.md` section 7 |
| Project unchanged (SC-004) | Pass | Tree checksum and `git status --porcelain --ignored` unchanged after both reviews |

The path-mode review reused the merge rulings, positions and notes of the branch run, with finding identifiers renumbered to the path-mode clusters by file. It therefore shows that the scope, merge, adjudication and report steps handle path mode; it adds no independent evidence of detection beyond section 4.5.

### 4.11 Extensions (T071, quickstart.md section 6, SC-012, SC-013)

Runs of 2026-11-04 with the sequential runner, five default perspectives plus any selected domain perspective, defender and moderator, 2 rebuttal rounds and at most 2 batches. Every message passed `panel.py validate` at the first attempt, and every debate stopped after round 1.

**Step 1: idfkit extension installed.** Fixture built with the idfkit plugin's `tests/fixtures/sci-review/build.py` (branch `feature`, 7 files, 142 lines). `select-extensions` selected `building-energy-sci-review-extension`, and the building physicist joined the panel with source `building-energy-sci-review-extension`. Its domain checks ran by route A of `checks.md`: `load_model`, then `validate_model` (one error, E009, `BuildingSurface:Detailed 'Office North Wall'.construction_name` references the missing construction 'Exterior Wall Insulated') and `check_model_integrity` (passed); no simulation was run and the model was not saved. `adjudicate` gave 7 consensus findings.

The idfkit manifest uses a format of its own (`entries` with `kind` and `line`), which `score.py` does not read, so the run was scored by a short script against it with the same 3-line tolerance:

| Criterion | Verdict | Result |
|-----------|---------|--------|
| Seeded building-energy defects reported | Pass | 7 of 7: hour-ending stamps read as starting (Python, TypeScript), kBtu-to-kWh factor (Python, TypeScript), leap-year truncation (Python, TypeScript), missing construction in the IDF |
| SC-012, first half | Pass | 7 of 7 list the building physicist among their raisers (at least 90% required) |
| IDF validation failure debated | Pass | E009 is F1, raised by the building physicist and accepted by every member |
| Look-alikes | Pass | 0 of 8 reported, including the case-insensitive construction reference that `validate_model` also accepts |
| No simulation, project unchanged | Pass | No `run_simulation` call; tree checksum and `git status --porcelain --ignored` unchanged |

**Re-score with `score.py` (T095).** `score.py` now reads the entry format as well, and takes `--domain-perspective ID` for SC-012. The step 1 run directory was re-scored on 2026-11-04 with `score.py report.json --manifest <idfkit-plugin>/tests/fixtures/sci-review/manifest.json --domain-perspective building-physicist`: SC-001 Pass (7 of 7; Python 3 of 3, TypeScript 3 of 3, IDF 1 of 1), SC-002 Pass (0 of 8 look-alikes), SC-003 Pass (7 of 7 complete), SC-010 Skip (no contested construct in that fixture), SC-012 Pass (7 of 7 raised by the building physicist). The verdicts match those of the short script above.

**Step 2: extension not installed.** Same fixture, `select-extensions` with no declaration: the extension is `recommended` ("not installed; it would apply to models/office.idf. Install it with idfkit@idfkit."), and the Extensions section names what it would add. The default perspectives' independent-round output does not depend on the extension, so their candidates were those of step 1; the debate was rerun with five perspectives. 6 consensus findings, none attributed to a domain perspective; the IDF failure is not reported, since only the domain checks find it. SC-012, second half: Pass.

**Steps 3 and 4: contract-only test extension.** A scratch git project whose `feature` branch adds `src/levels.py` (27 lines, importing `scipy.signal`) with two acoustics defects and one look-alike. `select-extensions` received the declarations of `tests/fixtures/sci-review/test-extension-plugin/` and of its invalid copy: the first was `selected` (applies to `src/levels.py`, by its import pattern) and the acoustician joined the panel; the second was `failed` with "contract_version 2 is not supported (supported: 1)", and the review completed. The two defects (10 log10 applied to an RMS pressure; arithmetic mean of levels in dB) fell in one location cluster, which the moderator split into F1 and F1001; both are consensus findings raised by the acoustician, the first with the theorist and experimentalist, the second with the experimentalist and methodologist. The look-alike (a gain in dB added to a level) was not reported. No file of `plugins/sci-review/` changed. SC-013: Pass.

Limits of these runs as evidence:

1. **Single reviewer.** As in sections 4.5 and 4.10, one reviewer performed every role. The runs show that selection, panel membership, domain checks, the debate, adjudication and the report handle extensions end to end; detection by independent agents with a domain perspective remains untested.
2. **Prior knowledge.** The reviewer did not read the idfkit manifest before scoring, but section 2 of this record names the IDF defect and its look-alike, and the extension's reference document contains worked examples of the hour-ending and leap-year defects, by design. The acoustics project was written by the reviewer, so steps 3 and 4 test the contract mechanics only.

### 4.12 Claude Workflow re-run after the corrections (T047)

Run of 2026-11-04 on a fresh build of the fixture (branch `feature`, 12 files, 413 lines) with `panel.py panel --runner claude-workflow`: five default perspectives, defender and moderator, 2 rebuttal rounds, at most 2 batches, no extension. The plugin is not installed in the session that ran the review, so the named workflow `sci-review:scientific-review` was not listed; the same script, `plugins/sci-review/workflows/scientific-review.js`, was launched by its path with the arguments of `runners/claude-workflow.md` section 4 and nothing else. The Workflow ran 33 agents in 187 s (2.89 million subagent tokens), none failed. `panel.py ingest` accepted all 33 messages and dropped none. Both batches stopped after round 1; every position of every member accepted every finding. `adjudicate` gave 12 consensus findings.

| Criterion | Verdict | Result |
|-----------|---------|--------|
| SC-001 recall | Pass | 11 of 11; every dimension and both languages at 100% |
| SC-002 look-alikes | Pass | 0 of 4 reported |
| SC-003 FR-014 fields | Pass | 12 of 12 findings complete |
| SC-004 project unchanged | Pass | Tree checksum of tracked files unchanged; `git status --porcelain --ignored` empty before and after, so the bytecode-cache correction of section 4.3 holds |
| SC-008 panel against best single perspective | Fail | Each perspective alone detected 11 of 11; the fixture does not discriminate |
| SC-009 false positives rejected in debate | Pass | No independent-round false positive |
| SC-010 contested construct | Fail | Not reported; no perspective raised `geometry.py:14-30`, as in sections 4.6 and 4.8 |
| SC-011 independence | Pass | None of the five independent-round transcripts contains a finding identifier of another perspective; the round-0 transcripts contain them only through the merge ruling's `members`, as protocol.md section 3 allows. Every prompt states the project root (section 4.3, item 1) |

**Effect of the corrections of section 4.9.** The computer scientist reported the `Math.min(...readings)` argument limit of `normalise.ts:16-17` as a finding of its own, separate from the zero-span NaN, so it was merged as F2001 and debated, where in section 4.6 the same defect was kept only in a fix field. The theorist stated the `permutation_pvalue` trigger as other code drawing from the global generator between `random.seed` and the call, the form rule 4 now requires, and no member challenged it.

### 4.13 Claude Workflow run on the extended fixture (T090, T091)

**Fixture changes.** Two changes were made to the fixture before this run.

1. **Contested construct (T090).** The docstring of `src/sci/core/geometry.py` now states that the paths follow graded roads and "unsurfaced hill paths between them". This follows observation 1 of section 4.6: the documented regime should leave the inputs in scope open. The code is unchanged. The manifest entry `ct-py-small-angle-elevation` (lines 15 to 31) now records that graded roads stay below the 21 degree crossover and hill paths need not.
2. **Perspective-specific defects (T091).** Five defects were added, one per default perspective. Each was chosen to need that perspective's expertise; the intended perspective is recorded in the manifest's `exposed_by` field:

| Defect | Intended perspective | Dimension | Severity | Reproduction check |
|--------|----------------------|-----------|----------|--------------------|
| `py-richardson-order`: Richardson weights for an O(h**2) error applied to a first-order forward difference | theorist | mathematical-derivations | high | `checks/py-richardson-order.py` |
| `ts-log1p-cancellation`: `Math.log(1 + x)` for fractional changes near 1e-16 | numerical analyst | numerical-stability | medium | none |
| `py-lag-correction-sign`: first-order sensor lag subtracted instead of added | experimentalist | physical-modelling-and-units | high | `checks/py-lag-correction-sign.py` |
| `py-small-sample-z`: normal quantile instead of Student's t for 3 to 10 replicates | methodologist | statistical-integrity | high | `checks/py-small-sample-z.py` |
| `ts-percentile-lexicographic-sort`: `Array.prototype.sort()` without a comparator | computer scientist | algorithmic-correctness | high | `checks/ts-percentile-lexicographic-sort.mjs` |

`build.py --check` verifies all 21 manifest entries. On `feature`, before any fix, all 13 reproduction checks fail. After a correct fix of each new High defect in a copy of the fixture, the 4 new checks pass; the fixes were applied by the fixture author.

**Run.** The run took place on 2026-11-04, on a fresh build of the fixture (branch `feature`, 17 files, 526 lines), with `panel.py panel --runner claude-workflow`. The panel had five default perspectives, the defender and the moderator, with 2 rebuttal rounds, at most 2 batches and no extension.

- **Launch.** The plugin was not installed in this session, so the script was launched by its path, as in section 4.12.
- **Agents.** The Workflow ran 33 agents in 313 s and used 3.04 million subagent tokens. No agent failed.
- **Debate.** The perspectives returned 87 candidates, which formed 17 location clusters in 2 batches. Both batches stopped after round 1.
- **Messages.** `panel.py ingest` accepted all 33 messages and dropped none.
- **Labels.** `adjudicate` gave 18 consensus findings, with 0 majority, 0 contested and 0 rejected.

| Criterion | Verdict | Result |
|-----------|---------|--------|
| SC-001 recall | Pass | 16 of 16 seeded defects, including the 5 new ones; every dimension and both languages at 100% |
| SC-002 look-alikes | Pass | 0 of 4 reported |
| SC-003 FR-014 fields | Pass | 18 of 18 findings complete |
| SC-004 project unchanged | Pass | Index checksum unchanged; `git status --porcelain --ignored` empty before and after |
| SC-008 panel against best single perspective | Fail | Every perspective alone detected 16 of 16 with 0 false positives, the five new defects included |
| SC-009 false positives rejected in debate | Pass | No independent-round false positive |
| SC-010 contested construct | Fail | Reported as F10 and labelled consensus. All five perspectives raised it independently, and the defender accepted it in round 0 as well as round 1. The defender wrote that the only available defence, the documented first-order model, fails because the docstring places hill paths in scope and bounds no incline. The finding's trigger is `elevation_gain([100.0], [0.5])`, which returns 50.0 m instead of 47.94 m |

**Interpretation.**

1. **SC-010.** Over three wordings, the construct has been labelled consensus as a contradiction of its contract (section 4.1), checked and found correct (sections 4.6, 4.8 and 4.12), and consensus as a defect (this run). It has never been divided among independent agents. The agents settle the question from the documented regime in the same way, so the regime decides the label. The label depends on the wording of the regime, not on a division between perspectives. A contested label from independent agents therefore needs a construct whose validity turns on information the code does not contain, or else SC-010 must be amended.
2. **SC-008.** Defects chosen to need one perspective's expertise were detected by every perspective. At the capability of the current agents, the five briefs do not partition the expertise needed for these defects. The panel's measurable benefit over one perspective lies in the debate and the labels, not in recall on this fixture.

### 4.14 No determinable base (T102, edge case "No base branch")

A live review was run on 2026-11-04 on a scratch repository: one commit on branch `experiment`, HEAD detached, no remote, and no `main` or `master`. The opening steps of `SKILL.md` ran `panel.py init`, then `panel.py scope --mode branch`. The scope step exited 3 with "no base branch could be determined (no remote default branch and no main or master branch); name a baseline with --baseline REF, or review with --mode repository or --mode paths".

As section 3.3 of `SKILL.md` requires, the review then asked the user which scope to use: stop, review the repository, or name a baseline. It did not fall back to repository mode. The user chose to stop, and the run directory was removed with `panel.py clean`. Verdict: Pass.

### 4.15 Installed plugins on the Claude Workflow runner (T096)

**Setup.** Runs of 2026-11-04 in a Claude Code desktop session with both plugins installed: `sci-review@project-kit` 0.1.0 (identical to `plugins/sci-review/` at this commit, apart from the cache marker `.in_use`) and `idfkit@idfkit` 0.3.0. Every `panel.py` step used the installed copy under `~/.claude/plugins/cache/project-kit/sci-review/0.1.0/`. The two differences from sections 4.11 to 4.13 are the following.

1. **Named workflow.** `sci-review:scientific-review` was listed, and both reviews were launched by name with the arguments of `runners/claude-workflow.md` section 4, not by the script path.
2. **Extension discovery from the host.** The host skill listing contained one skill whose name ends in `sci-review-extension`: `idfkit:building-energy-sci-review-extension`. Loading it gave its base directory, which is a copy managed by the desktop application rather than the `~/.claude` plugin cache; `extension.json` was found there and passed to `select-extensions`. No path was supplied by hand.

Both reviews used five default perspectives plus any selected domain perspective, with the defender and the moderator, 2 rebuttal rounds and at most 2 batches. Every agent ran as a Workflow subagent; no agent failed, and `panel.py ingest` accepted every message and dropped none.

**Run 1: seeded fixture (quickstart.md section 4).** Fresh build, branch `feature`, 17 files, 526 lines. `select-extensions` recorded the building-energy extension as `not-applicable`. The Workflow ran 34 agents in 269 s and used 3.20 million subagent tokens. The perspectives returned 86 candidates in 17 location clusters and 2 batches; batch 1 stopped after round 1 and batch 2 after round 2. `adjudicate` gave 19 consensus findings, with 0 majority, 0 contested and 0 rejected.

| Criterion | Verdict | Result |
|-----------|---------|--------|
| SC-001 recall | Pass | 16 of 16; every dimension and both languages at 100% |
| SC-002 look-alikes | Pass | 0 of 4 reported |
| SC-003 FR-014 fields | Pass | 19 of 19 findings complete |
| SC-004 project unchanged | Pass | Index checksum unchanged; `git status --porcelain --ignored` empty before and after |
| SC-008 panel against best single perspective | Fail | Four perspectives alone detected 16 of 16 and the numerical analyst 15 of 16, all with 0 false positives |
| SC-009 false positives rejected in debate | Pass | No independent-round false positive |
| SC-010 contested construct | Fail | Reported as F10 and labelled consensus, as in section 4.13 |
| SC-011 independence | Pass | No independent-round transcript contains a finding identifier of another perspective |

**Run 2: building-energy fixture with the extension (quickstart.md section 6, step 1).** Fresh build with the idfkit plugin's `tests/fixtures/sci-review/build.py`: branch `feature`, 7 files, 142 lines. `select-extensions` selected `building-energy-sci-review-extension` ("applies to models/office.idf, src/bem/climate.py, src/bem/climate.ts and 4 more"), and the building physicist joined the panel. The Workflow ran 39 agents in 330 s and used 3.39 million subagent tokens. The perspectives returned 46 candidates in 8 location clusters and 2 batches; batch 1 stopped after round 2 and batch 2 after round 1. `adjudicate` gave 9 consensus findings, with 0 majority, 0 contested and 0 rejected. The run was scored with `score.py report.json --run RUN --manifest <idfkit>/tests/fixtures/sci-review/manifest.json --domain-perspective building-physicist`.

| Criterion | Verdict | Result |
|-----------|---------|--------|
| SC-001 recall | Pass | 7 of 7 seeded building-energy defects |
| SC-012, first half, independent agents | Pass | 7 of 7 list the building physicist among their raisers (at least 90% required) |
| Domain checks | Pass | The independent building physicist called `load_model`, `validate_model` and `check_model_integrity` once each. The missing construction is F1, raised by all six perspectives and accepted by every member |
| No simulation | Pass | No `run_simulation` call in any of the 39 agent transcripts |
| SC-002 look-alikes | Pass after the scorer correction | First scored Fail; see observation 1 and the re-score below |
| SC-003 FR-014 fields | Pass | 9 of 9 findings complete |
| SC-004 project unchanged | Pass | Index checksum unchanged; `git status --porcelain --ignored` empty before and after |
| SC-008 panel against best single perspective | Fail | The experimentalist alone detected 7 of 7 with 0 false positives |
| SC-009 false positives rejected in debate | Fail by `score.py`; not applicable on inspection | 0 of 4 removed after the scorer correction; the 4 are genuine defects that the manifest does not list (observation 1) |
| SC-011 independence | Pass | No independent-round transcript of the six perspectives contains a finding identifier of another perspective |

**Observations.**

1. **Line-proximity scoring.** `score.py` matches a finding to a manifest entry when their lines lie within 3 of each other. It therefore reports the look-alike `py-lookalike-kwh-to-kbtu` (`src/bem/units.py:21`, `return kwh * 3.412141633`) as reported by F7 and F1001. Neither finding concerns that conversion. Both cover `calibration_error` at lines 24 to 27: F7 states that `zip` silently truncates and misaligns a bill series with a missing month, and F1001 states that a zero billed month raises `ZeroDivisionError`. Both are concrete failures in reviewed code that the manifest does not list. For the same reason, the six independent-round "false positives" counted for SC-009 are not false positives. Two of them are seeded defects whose candidate lines lie outside the tolerance: `building-physicist-4` at `units.py:14` for the constant at line 6, and `theorist-7` at `office.idf:79` for the reference at line 73. The other four are the two `calibration_error` defects. No look-alike conversion was reported by any finding.

   **Re-score after the scorer correction.** `score.py` was then changed in two ways, each covered by a unit test in `tests/test_sci_review_score.py`. First, a finding reports a look-alike only when its own lines overlap the look-alike's lines; the 3-line tolerance still applies to seeded defects. Second, an independent-round candidate is credited with the seeded defect of the merged finding that absorbed it in `merge/batch-*.json`. The three run directories of sections 4.15 and 4.16 were re-scored without new agent runs. The seeded-fixture verdicts are unchanged. On the building-energy run, SC-002 now passes (0 of 8 look-alikes), and every perspective is credited with 7 of 7 defects, including the building physicist and the theorist. SC-009 still counts 0 of 4 removed. The 4 are the `calibration_error` candidates, which describe genuine defects absent from the idfkit manifest, so the remaining failure is a gap in that manifest, not in the panel or the scorer.

   **Re-score with the corrected idfkit manifest.** idfkit/idfkit-plugin#34 lists the two `calibration_error` defects and adds a `domain` field to every defect entry. The rule is stated in the manifest: a defect is a domain defect when recognising it requires building-energy knowledge. The 7 original seeded defects are domain defects; the 2 `calibration_error` defects are not. `score.py` now measures SC-012 over domain defects only, and SC-001 still counts every defect. The fixture code was not changed: the two defects remain, and the manifest now records them. Re-scoring the same run directory against the manifest of that pull request gives SC-001 Pass (9 of 9), SC-002 Pass (0 of 8), SC-003 Pass (9 of 9), SC-009 Pass (no independent-round false positive) and SC-012 Pass (7 of 7 domain defects raised by the building physicist). SC-008 fails, as on every other run (the computer scientist alone detected 9 of 9).
2. **Agent type.** The Workflow runs its agents as Workflow subagents, as `runners/claude-workflow.md` specifies. The `sci-review:scientific-auditor` agent type was listed by the Agent tool in this session but is used only by the Claude Agent runner, which these runs did not exercise.

Limit of these runs as evidence: section 6, steps 2 to 4 (extension not installed, the contract-only test extension and its invalid copy), were not re-run with the installed plugins; their records remain those of section 4.11. The Claude Agent runner is recorded in section 4.16.

### 4.16 Installed plugins on the Claude Agent runner (T096)

**Setup.** Run of 2026-11-04 in the same session as section 4.15, on a fresh build of the seeded fixture (branch `feature`, 17 files, 526 lines). The opening steps of `SKILL.md` used the installed `panel.py` with `panel --runner claude-agents`; extension discovery from the host skill listing found the building-energy extension, and `select-extensions` recorded it as `not-applicable`. Every panel agent was launched with the Agent tool as the installed agent type `sci-review:scientific-auditor`, with the prompt templates of `runners/claude-agents.md` section 4 and no other content. The panel had five default perspectives, the defender and the moderator, with 2 rebuttal rounds and at most 2 batches.

**Run.**

- **Agents.** 31 agents: 5 independent, 2 merge, 12 in round 0, 12 in round 1 and 2 notes. Together they used 1.18 million subagent tokens. The run was paused once between round 1 and the notes because the host volume was full; no message was lost, and the run resumed from the files in `$RUN`.
- **Validation.** Every message passed `panel.py validate` at the first attempt, so no output was returned to its author and no notice was recorded.
- **Merge.** The perspectives returned 85 candidates, which `panel.py merge` grouped into 17 location clusters in 2 batches. Both moderators confirmed every cluster and split none.
- **Debate.** Every member accepted every finding in rounds 0 and 1. `panel.py debate-status` stopped both batches after round 1.
- **Labels.** `adjudicate` gave 17 consensus findings, with 0 majority, 0 contested and 0 rejected.

| Criterion | Verdict | Result |
|-----------|---------|--------|
| SC-001 recall | Pass | 16 of 16; every dimension and both languages at 100% |
| SC-002 look-alikes | Pass | 0 of 4 reported |
| SC-003 FR-014 fields | Pass | 17 of 17 findings complete |
| SC-004 project unchanged | Pass | Index checksum unchanged; `git status --porcelain --ignored` empty before and after |
| SC-008 panel against best single perspective | Fail | Every perspective alone detected 16 of 16 with 0 false positives |
| SC-009 false positives rejected in debate | Pass | No independent-round false positive |
| SC-010 contested construct | Fail | Reported as F10 and labelled consensus. The defender considered the documented first-order model as a defence and rejected it because the docstring places hill paths in scope |
| SC-011 independence | Pass | No independent-round transcript contains a finding identifier of another perspective or a path to another perspective's candidates file |

**Observations.**

1. **Corrections agreed in debate stay out of the finding.** The members agreed on three numerical corrections to merged findings: the correct t interval of F3 is (8.516, 13.484), the refined value of F9 is better than the fine estimate rather than worse, and the standard deviation in F4 is 39.01 rather than 38.9. The moderator recorded each correction in the note's `argument_for`, but the protocol has no step that amends the merged finding, so the report's `wrong_output` fields still carry the uncorrected text. No conclusion depends on these values.
2. **Severity dissent.** In round 0 the numerical analyst accepted F1 but argued for low severity rather than medium; in round 1 it adopted medium. The moderator recorded the question as F1's `deciding_assumption`, although the label is consensus.
3. **Runner comparison.** On the same fixture, the Agent runner and the Workflow runner of section 4.15 agree on every verdict. The Agent runner used fewer agents (31 against 34) and about 37% of the subagent tokens (1.18 million against 3.20 million).

## 5. Open criteria

Every task of tasks.md is complete; T096 is recorded in sections 4.15 and 4.16. Two success criteria remain unmet on every multi-agent runner, after the fixture changes of section 4.13 and the installed-plugin runs of sections 4.15 and 4.16:

| Criterion | Reason | Remedy |
|-----------|--------|--------|
| SC-008 | Each default perspective alone detects every seeded defect, or all but one: 11 of 11 in sections 4.1, 4.6, 4.8 and 4.12, 16 of 16 in section 4.13, 15 or 16 of 16 in section 4.15, and 16 of 16 in section 4.16, including five defects chosen to need one perspective's expertise. The panel therefore cannot exceed the best single perspective | Amend SC-008 to measure the panel by its debate (false positives rejected, labels) rather than by recall over the best single perspective, or build defects that current agents miss without a specific expertise |
| SC-010 | Independent agents settle the construct unanimously from its documented regime. They judged it correct when the regime was graded roads (sections 4.6, 4.8 and 4.12), and a defect when the regime includes hill paths (sections 4.13 and 4.15) | Amend SC-010 through `/speckit-specify`, for example to require that a divided panel, when one occurs, is labelled contested with both arguments, as the sequential run of section 4.5 and the golden tests show; or use a construct whose validity depends on information outside the code |

The line-proximity defect of `score.py` described in section 4.15, observation 1, is corrected: look-alikes require overlapping lines, and candidates are credited through the merge. The idfkit building-energy manifest omitted two genuine defects of `calibration_error` in `src/bem/units.py`, which every panel reports. idfkit/idfkit-plugin#34 lists them, with `"domain": false`, and `score.py` measures SC-012 over domain defects only. The fixture code was left unchanged so that the evaluation measures the code as written. Until that pull request is merged and released, the idfkit 0.3.0 manifest still omits the two defects.
