# Validation: Findings that say who hits them

Measured on 2026-11-26 with the `claude-workflow` runner at `medium`, empty preferences, the same model for every agent, and the `panel.py` and Workflow script of this branch (sci-review 0.4.0). Each run's panel was theorist, numerical analyst and methodologist (focused finders), the automatic merge or a moderator, and one verifier per batch, as in feature 009.

## 1. Runs

| Run | Scope | Agents | Subagent tokens | Delivered (design questions) | Rejected |
|-----|-------|--------|-----------------|------------------------------|----------|
| practical 1 | `practical-repo`, 99 lines | 7 | 692,710 | 8 (0) | 3 |
| practical 2 | same | 7 | 689,912 | 6 (2) | 1 |
| practical 3 | same | 7 | 691,383 | 5 (1) | 2 |
| practical 4 | same | 7 | 688,121 | 1 (0) | 3 |
| practical 5 | same | 7 | 686,971 | 5 (1) | 1 |
| seeded | `seeded-repo`, 526 lines | 7 | 771,452 | 18 (0) | 0 |
| downstream A | one module, 1,022 lines | 5 | 670,067 | 7 (2) | 0 |
| downstream B | one module, 422 lines | 4 | 473,364 | 2 (0) | 0 |

Every run started no more agents than its estimate (3 to 7). On the seeded fixture the run used 771,452 subagent tokens against 725,233 in feature 009 (+6% for the whole panel, inside the +15% per-verifier budget of the plan).

## 2. Success criteria

- **SC-001** (prose on every finding): pass. 52 of 52 delivered findings across the eight runs carry a headline, context and in-practice statement.
- **SC-002** (evidence): pass for the evidence half. Every finding whose verdict was reproduced carries the code run and its output; 48 of 52 findings carry a reproduction and 48 an extent table. The fixture half (the stale-configuration cache) could not be tested: see section 3.
- **SC-003** (design question on the deliberate cache, 4 of 5 runs): **fail**, 0 of 5. See section 3. The mark itself fired in 3 of 5 runs, on a different construct (a tariff cache with no invalidation), and in one downstream run, on two energy-basis choices that may well be deliberate.
- **SC-004** (no contradicted value repeated): pass, vacuously. No finder quoted the docstring's development setting as the configured value; all attributed it to the docstring and cited the environment file's value. The bait did not bait.
- **SC-005** (seeded recall, look-alikes, agents): pass. 16 of 16, 0 of 4 look-alikes, contested construct labelled contested with both arguments and its deciding assumption, 7 agents.
- **SC-006** (downstream case): section 4.
- **SC-007** (existing tests): pass, 305 tests.

## 3. The practical fixture does not test what it was built for

Two of its three cases rely on state that changes between processes, but both stores are in-memory dictionaries and the settings are read once at start-up. Within one process a cached search result can never meet a different search configuration, and a stored report can never meet a different schema version. The reviewers established this from the code: in 3 of 5 runs the panel rejected the configuration-staleness candidate for exactly that reason, and the finders noted the report-store branch as unreachable. That is the review behaving correctly on a flawed fixture.

They also found real defects the fixture did not intend: the result cache key omits the score function (5 of 5 runs), the search evaluates one hundredth of the configured population (4 of 5), and the issued-report store is overwritten by the dashboard rebuild (latent). A revised fixture needs a persistent store (a file or SQLite) so that the intended cases are reachable, and a manifest entry for the unintended defects. Tracked as a follow-up; SC-002's fixture half and SC-003 are re-run then.

## 4. Downstream case (anonymised)

Two issues filed from an earlier review of a private project, each criticised by the domain reviewer it was sent to, were re-reviewed at the commit of the original review, one module each. The case file, the original issues, the reviewer's comments, the rendered issues and the judge's full output are kept outside this repository.

Both original findings were found again, at the same lines, as consensus defects.

| Criterion | Case A: original | Case A: new | Case B: original | Case B: new |
|-----------|------------------|-------------|------------------|-------------|
| C1 Orientation | fail | pass | fail | pass |
| C2 Who triggers it | weak pass (release named once, in passing) | fail (configuration change only) | fail (led with the rarest form) | fail (excludes the commonest form) |
| C3 How often, who notices | fail | pass | fail | pass |
| C4 Intent / proportion | fail | fail | pass | fail (understates the reach) |
| C5 Quoted values | fail (contradicted setting) | pass | n/a | n/a |
| C6 Checkable evidence | fail | fail (traced, not run) | marginal | pass |
| C7 Owner | fail (sent to the algorithm's author) | pass | pass (assigned by hand) | fail |
| Judge's preference | | new | | new, with a caveat |

Criteria C1 to C4 and the preference come from one blind judge agent per case, given the reviewer's comment and the two bodies in random order; C5 to C7 were checked by script against the case file.

Observations:

1. **Evidence and orientation work.** In case B the judge preferred the new issue for its situation section, its honest "frequency unknown", and a runnable reproduction whose printed output matches the stated rate.
2. **The in-practice prose does not use what the verifier found.** In case B the verifier's reach recorded that quantities entered in other units are converted before rounding, which makes whole-number lots in those units fractional. The in-practice statement, written by the finder, still said whole-number lots are unaffected, and that sentence excluded the commonest way users hit the defect. The finder writes the prose before the verifier checks reach (research R1), so nothing reconciles them.
3. **A rarity guess suppressed a finding.** In case B one finder noticed the defect and did not report it: "rarely an exact multiple of the lot size, so this is unlikely to matter in practice." Another finder reported it, so recall held, but the risk research R5 describes is real at the finder stage too.
4. **The trigger named is not always the realistic one.** In case A the issue names an operator changing the search settings, the trigger the domain reviewer found unlikely; it does not mention a release of new solver code, and it does not raise that reuse across releases may be deliberate. No verifier marked it possibly intended.
5. **Blame is a poor owner signal after a squash merge.** Both modules came from one squash-merged pull request; blame names its merger for every line. That matched the expected owner in case A and not in case B.
6. **Line numbers counted across files.** In two practical runs a finder cited lines past the end of a 35-line file, counting across the part's files; the report's end-of-file check (feature 009) dropped them, and each duplicated a correctly numbered finding. This predates the feature.

## 5. Follow-ups

1. Reconcile in-practice with reach: let the verifier amend or flag an in-practice statement its reach contradicts (observation 2).
2. Tell finders not to drop a candidate on a rarity judgement: report it and say the frequency is unknown (observation 3).
3. Ask finders and verifiers, for cache and reuse findings, to consider code releases as a trigger alongside configuration (observation 4).
4. Prefer CODEOWNERS, and when only blame is available, say that blame shows who last changed the lines, which after a squash merge is the merger (observation 5).
5. Rebuild the practical fixture with a persistent store and re-run SC-002 and SC-003 (section 3).
6. Investigate the cross-file line numbering (observation 6).

## 6. Second round (Phase 10, research R14)

Measured on 2026-11-26 with the Phase 10 plugin (`c73eab0` and later), the same set-up as section 1, the rebuilt practical fixture, and the criteria as tightened after `/speckit-analyze` (SC-001, SC-006, SC-008; whole-panel token budget).

### 6.1 Runs

| Run | Agents | Subagent tokens | Delivered (design questions) | Rejected |
|-----|--------|-----------------|------------------------------|----------|
| practical 1 | 7 | 682,789 | 8 (1) | 0 |
| practical 2 | 7 | 682,406 | 5 (1) | 0 |
| practical 3 | 7 | 685,244 | 6 (0) | 0 |
| practical 4 | 7 | 694,840 | 7 (0) | 0 |
| practical 5 | 7 | 706,674 | 7 (0) | 0 |
| seeded | 7 | 754,006 | 17 (1) | 0 |
| downstream A | 5 | 707,502 | 8 (4) | 0 |
| downstream B | 4 | 455,741 | 2 (0) | 0 |

Seeded tokens: 754,006 against 725,233 in feature 009 (+4%, inside the +15% whole-panel budget). One launch of the seeded run was malformed by the orchestrator (arguments pasted twice; the script started no agent) and was relaunched; it is not counted.

Across the 60 delivered findings: 60 carry the three prose fields, 54 a reproduction, 54 an extent table, 8 a verifier revision of the in-practice statement, and 4 value corrections were recorded. No finding cited a line beyond the end of its file (4 in the first round).

### 6.2 Success criteria

- **SC-001**: **fail**. Prose fields: 60 of 60. Blind classification: 13 of 20 matched the verifier's trigger class (16 required). All 7 mismatches are between `user-action` and `data-condition`, in both directions; every `operator-change` item matched. The prose tells the reader who triggers a defect; the two classes overlap, since a user entering a value is both. See 6.4, item 1.
- **SC-002**: pass. The stored-plan case names a release among its triggers in 5 of 5 runs, citing the settings files; every reproduced verdict carries its code (enforced by validation).
- **SC-003**: **fail**, 0 of 5. The reviewers consistently treat serving an issued report as issued as plainly correct, so the planted case is not a real design question. The mark fired on other constructs (the stored plan in one run, a display-rounding tie rule, the contested small-angle construct, and four energy-basis and scheduling choices downstream).
- **SC-004**: pass. Two runs recorded a correction of the docstring's development setting; no report repeats it uncorrected.
- **SC-005**: pass. 16 of 16, 0 look-alikes, contested construct labelled contested with its deciding assumption, 7 agents. The fixture's scorer read defects only and missed the construct when it was routed to design questions; it now reads both (`tests/fixtures/sci-review/seeded-repo/score.py`).
- **SC-006**: **fail** on one criterion per case, with the new issue preferred in both. Table below.
- **SC-007**: pass.
- **SC-008**: pass. The unit-conversion case is reported in 5 of 5 runs, its in-practice statement names pounds or kilograms in 5 of 5, and no line is beyond the end of its file.

### 6.3 Downstream cases (anonymised)

| Criterion | Case A: original | Case A: round 2 | Case B: original | Case B: round 2 |
|-----------|------------------|-----------------|------------------|-----------------|
| C1 Orientation | fail | pass | fail | pass |
| C2 Who triggers it | fail | pass (names a release) | fail | **fail** (omits the converted-unit route) |
| C3 How often, who notices | fail | pass | fail | pass |
| C4 Intent / proportion (recorded) | fail | pass (design question) | partial | mostly pass |
| C5 Quoted values | fail | pass (one correction) | n/a | n/a |
| C6 Checkable evidence | fail | **fail** (traced, not run) | pass | pass |
| C7 Owner (recorded) | fail | pass (merged PR named) | pass (by hand) | fail (merged PR named) |
| Judge's preference | | round 2 | | round 2 |

Case B's verifier added the most useful context of either round, checked against the code: the application does not yet send the inputs that reach the defect, so only direct callers of the library can hit it today.

### 6.4 Observations and follow-ups

1. **The trigger classes overlap.** `user-action` and `data-condition` both describe "a user enters a value", which accounts for every SC-001 mismatch. Either merge them, or define `data-condition` as a property of values from any source and `user-action` as an action other than entering values.
2. **A single trigger class loses information.** Several findings name both a release and a configuration change; the reported class is one of them (case A's "Trigger:" line says configuration while its text names a release). Allow a list.
3. **A revision does not reach the rest of the finding.** In case B the verifier revised the in-practice statement but the finder's reproduction kept an older rate (1 in 10 against 1 in 8); in case A the correction note says a quoted value does not exist while the reproduction still uses it. Let the verifier flag other fields its evidence contradicts.
4. **Traced findings have no checkable evidence.** Where code cannot run (a database, a GPU library), the verifier traces it; C6 then fails. A short excerpt of the traced lines with their values would give the reader something to check.
5. **Two of the fixture's look-alikes were not correct.** The dashboard summary is stale by its own docstring, and the display rounding has an unexplained tie rule. Fix both, and replace the design-question case with one that is plausibly deliberate.
6. **Contested findings can render "Decided by: n/a".** The verify protocol leaves the deciding assumption empty when no verifier names one; the issue should omit the line.
