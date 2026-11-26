# Feature Specification: Findings that say who hits them

**Feature Branch**: `010-sci-review-practical-impact`

**Created**: 2026-11-26

**Status**: Draft

**Input**: User description: "sci-review: report practical impact, not only computational correctness." (Full description: a consensus finding filed as an issue was criticised by the domain reviewer it was sent to; see Overview.)

## Overview

A `medium` review of a downstream project produced a consensus finding: a cache of computed results is keyed on the inputs, not on the configuration or version of the algorithm that computed them, so a result computed under an older configuration can be served as current. The finding was filed as an issue in the reviewed project. Its body was the finding's row, field for field: summary, trigger and wrong output as the reproduction, fix as the proposed fix, and the agreement label as the source.

The domain reviewer it was sent to agreed the code path was real but judged the issue badly written, for reasons that trace back to the review itself:

1. **No orientation.** The issue opened on hash keys and settings, with no sentence on what the code does for its users or when the problem arises.
2. **No practical reach.** Nothing said who triggers it or how often. The algorithm's settings differ between deployments, each with its own store, so the only realistic trigger is a release of new algorithm code: a rare, operator-driven event, not the settings change the reproduction described.
3. **Intent not considered.** Keeping cached results stable across releases may be deliberate. The finding presented the behaviour as a defect, not as a question for the code's owners.
4. **An unchecked value.** The reproduction quoted a development setting that the project's own environment file contradicts.
5. **Wrong owner.** The issue went to the algorithm's author; the cache belongs to another team.

The panel's data model explains each one. A finding has no field for context or practical reach. Severity is defined on "realistic inputs", not on how the software is used. Verifiers follow callers but never read configuration or deployment files, so they cannot tell how a trigger state comes about. A verifier can only confirm, refute or call a finding uncertain, so an undocumented trade-off is confirmed as a defect. Nothing renders a finding for a reader outside the review.

This feature makes every finding say, in plain words, what situation it arises in, who or what triggers it, how often, and whether the behaviour may be intended; checks that against the project's configuration and deployment files; and renders a finding as an issue a domain reader can act on. The protocols, labels, levels, agent counts and read-only guarantee of features 007 to 009 are otherwise unchanged.

### Defined terms

- **Context**: one or two plain sentences, free of code identifiers where possible, on what the code does for its users and the situation in which the finding arises.
- **In practice**: who or what triggers the finding (a user action, a deploy or release, an operator changing configuration, a data condition), roughly how often, and whether anyone would notice the wrong result.
- **Reach**: the verifier's account of whether and how the trigger state occurs in the project as configured and deployed, with the files it read.
- **Trigger class**: one of `user-action`, `data-condition`, `release`, `operator-change`, `unreachable`, summarising how the trigger state comes about.
- **Possibly intended**: a verifier's judgment that the behaviour looks like a deliberate trade-off (stability, caching, tolerance, performance) that the code and its documentation neither confirm nor rule out.
- **Design question**: a finding reported to the code's owners as a decision to confirm, not as a defect.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Every finding orients its reader (Priority: P1)

A user reads the review report, or hands one finding to a colleague who has not seen the code. Before any line number or variable name, the finding says what the code is for, in what situation the problem arises, who or what causes that situation, how often, and whether anyone would notice.

**Why this priority**: This is the domain reviewer's main complaint and applies to every finding, whatever happens to it next.

**Independent Test**: Run a review on the seeded fixture. Every reported finding has a non-empty context and in-practice statement, and in the rendered report they appear before the technical details.

**Acceptance Scenarios**:

1. **Given** any reported finding, **When** the report is rendered, **Then** its context and in-practice statements appear as prose above its location, trigger, wrong output and fix.
2. **Given** a finder's candidate without a context or in-practice statement, **When** the panel validates the finder's message, **Then** the message is rejected as not conforming, as for any other missing required field.
3. **Given** a finding whose trigger is a data condition met by ordinary inputs, **When** it is reported, **Then** its in-practice statement says so in terms a user of the software would recognise (for example, "any building with a leap-year weather file").

---

### User Story 2 - Findings carry evidence a reader can check (Priority: P1)

A user reading a finding, or the domain reviewer it is sent to, can check it without trusting the reviewer's prose: the finding shows what was run, what came out, and how the result varies with the input. Severity stays the reviewers' judgement, and nothing lowers it on a guess about how rare a trigger is.

**Why this priority**: A domain reviewer's first reaction to an issue from the review was "valid, if we trust what the LLM has written". More confident prose does not answer that; evidence does. A second issue showed the risk of rarity guesses: it led with its most dramatic case (a minimum equal to the maximum), which invited "unlikely to be hit in practice", although its own exhaustive check found about a third of whole-lot bounds rounded wrongly, a common input for anyone who enters round numbers.

**Independent Test**: In the practical fixture, a finding the verifier reproduces carries the code it ran with its output, and a table of a few inputs with the expected and actual results, including ordinary inputs; both appear in the report and the issue.

**Acceptance Scenarios**:

1. **Given** a verdict with evidence `reproduced`, **When** it is validated, **Then** it carries the code or command run and its output, or it is rejected as not conforming.
2. **Given** a finding whose verifiers recorded an extent table, **When** it is reported or rendered as an issue, **Then** the table appears under "Who hits this and when", with ordinary inputs as well as failing ones.
3. **Given** a finding of any trigger class, **When** it is adjudicated, **Then** its severity is the merged finding's: the trigger class is shown beside it and never changes it.
4. **Given** a finding whose verifiers record trigger class `unreachable`, **When** it is adjudicated, **Then** it is treated as refuted (the trigger cannot occur).

---

### User Story 3 - Verifiers check practical reach and quoted values (Priority: P1)

A verifier, before confirming a finding, establishes how the trigger state arises in the project as it is configured and deployed, and checks every concrete value the finding quotes against the repository.

**Why this priority**: Without this step the in-practice statement is the finder's guess. The criticised finding quoted a setting that the repository contradicts and described a trigger that does not occur in the way it said.

**Independent Test**: In the fixture, a finding's trigger quotes a configuration value that the fixture's environment file sets differently. The verifier's reach records the file and the actual value, and the reported finding quotes the actual value or carries a notice that the quoted value was wrong.

**Acceptance Scenarios**:

1. **Given** a finding whose trigger depends on configuration, **When** a verifier judges it, **Then** its verdict records a reach naming the configuration, environment, deployment or release files it read (or that none exist) and the trigger class those files support.
2. **Given** a trigger that quotes a value contradicted by a file in the repository, **When** the verifier judges it, **Then** the verdict records the contradiction with file and line, and the report shows the corrected value or a notice.
3. **Given** a finding whose trigger state the reach shows cannot occur in any configuration the project ships, **When** the verifier judges it, **Then** the verdict is `refute` with trigger class `unreachable`.

---

### User Story 4 - Possibly deliberate behaviour is raised as a question (Priority: P2)

A user receives, separately from defects, a short list of design questions: behaviours that look like deliberate trade-offs the code does not document, each addressed to the code's owners with the trade-off stated both ways.

**Why this priority**: Reporting a deliberate choice as a bug costs credibility with exactly the people who must act on the report. It matters less than P1 because it affects a minority of findings.

**Independent Test**: Add to the fixture an undocumented cache that deliberately ignores a version field. The review reports it under "Design questions", with the reason it may be intended and the consequence if it is not, and does not report it among confirmed defects.

**Acceptance Scenarios**:

1. **Given** a finding that at least one verifier marks possibly intended and that no verifier refutes outright on other grounds, **When** it is adjudicated, **Then** it is reported as a design question, with the verifier's reason it may be intended and the finding's wrong output as the consequence if it is not.
2. **Given** a possibly-intended mark, **When** labels are computed, **Then** that verdict does not count as a confirmation.
3. **Given** the code or its documentation states the trade-off, **When** the verifier judges the finding, **Then** the verdict is `refute`, citing that statement, not possibly intended.
4. **Given** a stale-cache candidate, **When** a finder raises it, **Then** its in-practice statement says whether the reuse looks deliberate, because the finder brief asks whether invalidation is intended and not only whether it is possible.

---

### User Story 5 - A finding becomes a well-routed issue (Priority: P2)

A user who wants to file a finding in the reviewed project's tracker runs one command and gets an issue body that reads in the domain reader's order, with suggested owners.

**Why this priority**: Issues are where findings meet people outside the review; the criticised one was hand-transcribed from the report and sent to the wrong person. It depends on Stories 1 to 4 for its content.

**Independent Test**: On a completed run, render the issue for one finding. The body's sections appear in the order below and the suggested owners come from the fixture's ownership file or, failing that, its history.

**Acceptance Scenarios**:

1. **Given** a completed run and a finding id, **When** the user renders its issue, **Then** the body has, in order: a title phrased as the situation, not the code; Situation (context); Who hits this and when (in practice and reach); Bug or design question; Where (location); Reproduction (trigger and wrong output, with checked values); Proposed fix; Suggested owners; Review provenance (label, raisers, verifiers, review commit). With `--supersedes`, a line naming the superseded issues follows the title (FR-019); the exact layout is in contracts/issue.md.
2. **Given** the repository has an ownership file covering the finding's file, **When** the issue is rendered, **Then** it lists those owners as suggested owners; otherwise it lists the most frequent recent authors of the finding's lines, labelled as derived from history.
3. **Given** a design question, **When** its issue is rendered, **Then** the title and body ask the owners to confirm the intended behaviour, not to fix a bug.
4. **Given** the user renders an issue, **When** the command finishes, **Then** nothing is posted; the body is printed or written to the run directory for the user to file.

### User Story 6 - What the review learned reaches the reader (Priority: P1)

Added after the first validation (validation.md, sections 4 and 5). A user filing a finding gets an issue whose "who hits this" statement agrees with what the verifier established, that names every realistic way the trigger arises (a code release included), that was not silently dropped for seeming rare, and that says what the suggested owners actually are. The issue can say which earlier issue it supersedes.

**Why this priority**: In the first validation the verifier recorded that quantities are converted between units before rounding, yet the finder's in-practice statement, written earlier, excluded the commonest way users hit the defect; a finder dropped a real defect as "unlikely to matter in practice"; a stale-result finding named only a configuration change, not a release of new code; and blame after a squash merge named the merger as owner. Each made a reviewed issue wrong in a way its own evidence could have prevented.

**Independent Test**: On the rebuilt practical fixture, the unit-conversion case's reported in-practice statement names the converted units (revised by the verifier when the finder's did not), the stored-result case names a release of new code among its triggers, and every finding cites line numbers within its own file.

**Acceptance Scenarios**:

1. **Given** a verifier whose reach contradicts or omits part of a finding's in-practice statement, **When** it judges the finding, **Then** it records a revised statement, and the report and the issue show the revised statement, marked as revised by the verifier.
2. **Given** a finder that establishes a concrete failure but judges it rare, **When** it writes its candidates, **Then** it reports the finding and states that the frequency is unknown or what it depends on, and does not drop it.
3. **Given** a finding about a cached, stored or memoised result, **When** finders and verifiers describe its trigger, **Then** they consider a release of new code that changes how the result is computed, as well as configuration and inputs.
4. **Given** owners suggested from history in which every cited line comes from one commit whose message ends in a pull request number, **When** the issue is rendered, **Then** it says that the lines come from one merged pull request and that history shows who last changed them, not who owns them.
5. **Given** `--supersedes <ref>` (repeatable), **When** an issue is rendered, **Then** its body opens with a line saying it supersedes those issues.

---

### Edge Cases

- A finding with no concrete trigger (contested, no trigger reason): its in-practice statement says the trigger could not be established and why; it can still be rendered as an issue, marked contested.
- A repository with no configuration, environment or deployment files: the verifier records that none exist and judges reach from the code and callers alone.
- Verifiers disagree on trigger class: the report shows the most frequent class recorded by a non-refuting verifier, preferring the more frequent trigger on a tie.
- One verifier marks possibly intended and another confirms: the finding is a design question, with the confirming verifier's argument as the case that it is a defect.
- A run produced before this feature (no context, in practice or reach): rendering the report or an issue still succeeds, with those sections marked "not recorded".
- The ownership file names a team, not a person: the team is listed as given.
- Debate protocol (`max`): finders and the moderator provide context and in practice; the defender may argue possibly intended; the reach check and trigger class come from the verify protocol only, and debate findings carry no reach.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every candidate finding MUST carry a non-empty `headline` (the situation in plain words, used as the issue title), `context` and `in_practice`; every merged and reported finding MUST carry them, a merge of several candidates taking the moderator's wording.
- **FR-002**: Finder briefs MUST instruct finders to write context without code identifiers where possible, and in practice naming the trigger's actor, rough frequency and whether a wrong result would be noticed. In practice MUST state the triggering conditions in the users' terms, lead with the most common way the defect shows rather than the most dramatic, and cite where the triggering inputs come from (a form, an API schema or validator, a default, seed data, a configuration file), or say that their frequency is unknown.
- **FR-003**: Severity MUST be defined on ordinary use of the software, judged from what the reviewer read (where the inputs come from, how the project is configured and deployed): `high` when the wrong result occurs in ordinary use; `medium` when it occurs only in plausible edge cases, or prevents reproduction; `low` when latent. Every role brief and protocol.md section 4 MUST use this definition.
- **FR-004**: Adjudication MUST NOT change a finding's severity on its trigger class; the class is reported beside the severity. A verdict with evidence `reproduced` MUST record the code or command run and its output (`reproduction`), and MAY record an extent table (input, expected, actual); the report and the issue MUST show the first non-refuting verdict's, preferring a reproduced one.
- **FR-005**: The verifier procedure MUST include a reach step: read the project's configuration, environment, deployment and release files relevant to the trigger, record which were read, the trigger class they support, and any contradiction between a value quoted in the finding and the repository.
- **FR-006**: A verdict MUST record `reach` and `trigger_class`; a `refute` because the trigger cannot occur MUST use trigger class `unreachable`.
- **FR-007**: A verdict MAY carry `possibly_intended` with a reason; such a verdict MUST NOT count as a confirmation, and a finding with at least one such verdict and not rejected MUST be reported under "Design questions", not among defects. protocol.md section 5.1 MUST state where this rule sits in the order of rules.
- **FR-008**: The computer-scientist brief and the algorithmic-correctness dimension MUST ask, for every stale cache or memoised value, whether the reuse is intended and what documentation would settle it.
- **FR-009**: The markdown report MUST render each finding as a short block that opens with context and in practice, followed by the technical details; design questions MUST have their own section after the defects.
- **FR-010**: A new report command MUST render one finding of a completed run as an issue body with the sections and order of Story 5, write it to the run directory and print it, and MUST NOT post it anywhere.
- **FR-011**: The issue command MUST suggest owners from the repository's ownership file when one covers the finding's file, and otherwise from the recent authors of the finding's lines, saying which source was used.
- **FR-012**: Runs recorded before this feature MUST still render (report and issue), marking missing fields as not recorded.
- **FR-013**: The agent count, the agent estimate and the read-only guarantee MUST be unchanged; the reach step runs inside the existing verifiers.
- **FR-014**: A verdict MAY carry `in_practice_revision`, a replacement in-practice statement, when the verifier's reach contradicts or omits part of the finding's statement; the reported finding MUST use the first non-refuting verdict's revision, keep the finder's statement, and be marked as revised.
- **FR-015**: Finder briefs MUST forbid dropping a concrete defect because it seems rare; the finding is reported with its frequency stated as unknown or as what it depends on. The verifier brief MUST state that rarity is not grounds for refutation.
- **FR-016**: Finder and verifier briefs, and the algorithmic-correctness dimension, MUST ask for cached, stored or memoised results whether a release of new code that changes the computation is a trigger, alongside configuration and inputs.
- **FR-017**: When owners come from history, the issue MUST say that history shows who last changed the lines; when every cited line comes from one commit whose subject ends in a pull request reference such as `(#123)`, it MUST say the lines come from that merged pull request.
- **FR-018**: Every finding MUST cite line numbers within its own file; finder briefs MUST say so.
- **FR-019**: `panel.py issue` MUST accept `--supersedes <ref>` (repeatable) and open the body with a line naming the superseded issues.

### Key Entities

- **Candidate finding** gains `headline`, `context` and `in_practice`.
- **Merged finding** and **reported finding** gain `context`, `in_practice`, `trigger_class`, `reach` (the representative verifier's), `possibly_intended` (with reason) and `value_corrections`.
- **Verdict** gains `reach`, `trigger_class`, `possibly_intended` and `possibly_intended_reason`, `value_corrections` (quoted value, actual value, file, line), `reproduction` and `extent` (rows of input, expected, actual).
- **Reported finding** also gains `kind` (defect or design question), `reproduction`, `extent` and `in_practice_original` (the finder's statement when a verifier revised it).
- **Verdict** also gains `in_practice_revision` (research R14).
- **Issue body**: a markdown file in the run directory, one per rendered finding.

## Success Criteria *(mandatory)*

- **SC-001**: On the seeded and practical fixtures, every delivered finding has a headline, context and in-practice statement. For a sample of 20 delivered findings across the runs, a blind judge shown only the headline, context and in-practice statement assigns a trigger class (user action, data condition, release, operator change), and its class matches the verifier's reported class for at least 16 of the 20.
- **SC-002**: On the practical fixture, every finding with evidence `reproduced` shows the code it ran and its output, and the stored-result finding's in-practice statement names a release of new code among its triggers and cites the file the settings come from.
- **SC-003**: On the fixture's deliberate-reuse case, the finding appears under design questions and not among defects in at least 4 of 5 runs.
- **SC-004**: On the fixture's wrong-quoted-value case, the report never repeats the wrong value without a correction or notice.
- **SC-005**: Recall of the 16 seeded defects at `medium` is unchanged (16 of 16), no look-alike is reported, and the number of panel agents is unchanged from feature 009.
- **SC-006**: For each case in the private case file (research R12), the issue rendered from the re-review passes C1, C3, C5 and C6 of the rubric, names the case's expected trigger (C2), and a blind judge prefers it to the issue originally filed. C4 and C7 are recorded but do not decide the criterion.
- **SC-007**: Every existing sci-review test passes, updated only where it asserts the old severity wording or the old report layout.
- **SC-008**: On the practical fixture's unit-conversion case, the defect is reported in 5 of 5 runs, its reported in-practice statement names the converted units as a trigger in at least 4 of 5, and no finding in any run cites a line beyond the end of its file.

## Assumptions

- Context and in practice are written by the finders, who have already read the code; asking verifiers to write them would duplicate reading. Verifiers check them through reach.
- Trigger class is a small closed set; finer distinctions belong in the in-practice prose.
- No rule lowers a severity on how rare a trigger seems. An LLM has no production data; a rule that downgrades on a guessed rarity would systematically suppress real defects. An automatic cap for release and operator-change triggers was built and then removed for this reason: how often releases happen differs between projects, and in the verify protocol most merges have no moderator to record a reason to keep a finding high.
- How a fix is chosen is left to the reviewers. The spec asks for the fix the reviewers judge best, not for a particular kind of fix.
- "Possibly intended" is a mark on a verdict, not a fourth verdict, so the label rules of feature 009 stay as they are apart from FR-007.
- Ownership files are found at the locations the major hosts use (`CODEOWNERS`, `.github/CODEOWNERS`, `docs/CODEOWNERS`, `.gitlab/CODEOWNERS`); the issue command does not query a host API.
- Posting the issue is left to the user, consistent with Principle III and the read-only guarantee.

## Constitution Check

- **II. Scripts for predictable steps**: the design-question routing, the choice of the reported evidence, owner suggestion and issue rendering are deterministic and belong in `panel.py`; judging context, reach and intent stays with the agents.
- **III. Show before changing**: the issue command writes only to the run directory and posts nothing.
- **IV. Works wherever installed**: owner suggestion uses only files and `git`; with no history available it says so and lists no owners.
