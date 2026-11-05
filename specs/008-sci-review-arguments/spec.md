# Feature Specification: Code-review-style arguments for sci-review

**Feature Branch**: `008-sci-review-arguments`

**Created**: 2026-11-04

**Status**: Draft

**Input**: User description: "copy the skill arguments that /code-review has"

## Overview

The `sci-review:scientific-review` skill currently reads its arguments from the wording of the request (contracts/invocation.md section 2 of feature 007). The host's built-in `/code-review` skill accepts a compact, explicit argument grammar instead:

```text
/code-review [low|medium|high|xhigh|max|ultra] [target] [--comment] [--fix] [--max-findings <n>|all|default]
```

where `target` is a pull request number, a branch or a path, a level given without a target persists as the user's level for later runs, and the `--max-findings` choice persists until `--max-findings default` is passed.

This feature gives the scientific review the same argument grammar, so that a user who knows `/code-review` can invoke a scientific review with the same words, and so that a review can be started reproducibly from a single command line. The natural-language arguments of feature 007 remain supported.

The feature also removes the fixed review budget of feature 007. Today, once the scope reaches 6,000 changed lines, every further file is recorded as "over budget" and is not reviewed. `/code-review` has no such limit. After this feature, the whole requested scope is reviewed: a large scope is divided into parts that are each reviewed in full, instead of being cut off.

### Defined terms

- **Effort level**: one of `low`, `medium`, `high`, `xhigh`, `max`. It selects a predefined panel configuration (number of perspectives, rebuttal rounds, debate batches, finding cap).
- **Target**: the object under review, given as a pull request reference, a branch name or one or more paths.
- **Finding cap**: the maximum number of findings delivered in the report, after ranking.
- **Persisted preference**: a value (effort level or finding cap) stored for the user outside every reviewed project and reused by later reviews when the argument is omitted.
- **Explicit argument**: an argument written in the command-line grammar above, as opposed to one inferred from the wording of the request.
- **Review budget**: the maximum number of lines of feature 007 (default 6,000) beyond which files were excluded from the review as "over budget".
- **Review part**: a subset of the scope, small enough for one reviewer to examine in full, into which a large scope is divided.
- **Large-scope threshold**: the scope size above which the review states its size and asks for confirmation before starting.

## Clarifications

### Session 2026-11-04

- Q: When `--fix` is passed, who applies the fixes: the user's session model, a specialised fixing agent, or the panel member that raised each finding? → A: The user's session model, in the conversation that ran the review, as in `/code-review`; no additional agent is started.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Select the review depth with an effort level (Priority: P1)

A user types `/sci-review:scientific-review high` on a feature branch. The review runs on the branch diff with the panel configuration defined for `high`, and the report states the level and the panel actually used.

**Why this priority**: The effort level is the first and most frequently used argument of `/code-review`; it replaces the need to know the individual panel parameters.

**Independent Test**: Invoke the review at each of the five levels on the same fixture branch and confirm that the panel recorded in the report matches the level's documented configuration.

**Acceptance Scenarios**:

1. **Given** a branch with reviewable changes, **When** the user invokes the review with `low`, **Then** the review uses the `low` configuration and the report states "Effort level: low".
2. **Given** no level in the command and no persisted level, **When** the user invokes the review, **Then** the review uses `medium`, whose configuration equals the defaults of feature 007 (five default perspectives plus selected extensions, 2 rebuttal rounds, 2 debate batches).
3. **Given** the user previously invoked the review with `xhigh`, **When** the user invokes the review with no level, **Then** the review uses `xhigh` and the report states that the level was reused.
4. **Given** the user invokes the review with `max`, **When** the review starts, **Then** it runs the `max` configuration; **and given** the model would start a review on its own initiative, **Then** it never selects `max`.

---

### User Story 2 - Name the target: pull request, branch or path (Priority: P1)

A user types `/sci-review:scientific-review <number>`, `/sci-review:scientific-review <branch>` or `/sci-review:scientific-review <path>`. The review resolves the target to the pull request diff, the named branch's diff against its base, or the named paths, without checking anything out in the project.

**Why this priority**: Reviewing something other than the current branch is the second most common use of `/code-review`, and today it requires a phrased request that the model must interpret.

**Independent Test**: Invoke the review with each target form on a fixture repository and confirm the scope recorded in the report.

**Acceptance Scenarios**:

1. **Given** a repository whose remote hosts pull request `<number>`, **When** the user passes `<number>`, `#<number>` or the pull request URL, **Then** the scope is the pull request's diff against its base branch, and the report names the pull request.
2. **Given** a local branch `<branch>` that is not checked out, **When** the user passes `<branch>`, **Then** the scope is that branch's diff against its base, and the working tree and current branch are unchanged.
3. **Given** an existing path `<path>`, **When** the user passes it, **Then** the review runs in paths mode on that path; several paths may be given.
4. **Given** a target that is both an existing path and a branch name, **When** the user passes it, **Then** the review asks which was meant instead of guessing.
5. **Given** a pull request target and no means of reading the pull request from its host, **When** the review starts, **Then** it says what is missing and offers a branch or paths review instead of failing partway.

---

### User Story 3 - Cap the number of reported findings (Priority: P2)

A user types `/sci-review:scientific-review --max-findings 5`. The report delivers at most five findings, chosen in the existing ranking order (consensus, majority, contested; within each, high, medium, low), and states how many further findings were withheld. The cap persists for later reviews until the user passes `--max-findings default`; `--max-findings all` removes the cap.

**Why this priority**: It controls the length of the report but does not change what the panel examines.

**Independent Test**: Run a review whose fixture yields at least eight adjudicated findings with caps of 5, `all` and `default`, and compare the delivered counts.

**Acceptance Scenarios**:

1. **Given** eight adjudicated findings, **When** the cap is 5, **Then** five findings are delivered, they are the top five by ranking, and the report states that three were withheld.
2. **Given** a cap of 5 persisted by an earlier review, **When** the user invokes the review without `--max-findings`, **Then** the cap of 5 applies and the report says it was reused.
3. **Given** a persisted cap, **When** the user passes `--max-findings default`, **Then** the persisted cap is cleared and the level's default cap applies.
4. **Given** `--max-findings 0` or a non-numeric value other than `all` and `default`, **When** the review starts, **Then** the value is ignored, the review runs with the persisted cap or, when there is none, the level's default cap, and the user is told in one line that `--max-findings` was ignored and which values it accepts (a whole number above zero, `all` or `default`).

---

### User Story 4 - Review the whole scope, however large (Priority: P2)

A user asks for a review of a branch with 15,000 changed lines, or of a whole repository. Instead of reviewing the first 6,000 lines and listing the rest as "over budget", the review divides the scope into parts, reviews every part, and merges the results into one report.

**Why this priority**: A review that silently covers only part of a large change gives false assurance about the remainder; scientific defects are often in the files that a size cut-off drops. It is independent of the argument grammar and can be delivered on its own.

**Independent Test**: Run a review on a fixture scope of about three times the former budget, with a known defect placed in the last file, and confirm that the defect is reported and that no file is listed as "over budget".

**Acceptance Scenarios**:

1. **Given** a scope of 15,000 reviewable lines, **When** the review runs, **Then** every reviewable file is reviewed, the report lists no file as not reviewed for reasons of size, and it states the number of review parts used.
2. **Given** a defect in a file that would have fallen beyond the former 6,000-line budget, **When** the review runs, **Then** the defect is reported.
3. **Given** two review parts that each raise a candidate finding on the same defect, **When** the results are merged, **Then** the defect appears once in the report.
4. **Given** a scope above the large-scope threshold, **When** the review starts, **Then** it states the scope size and the number of review parts, and asks for confirmation before any reviewer runs; **and given** the user declines, **Then** it offers a narrower target (named paths) and runs nothing.
5. **Given** a scope at or below the large-scope threshold, **When** the review starts, **Then** it runs without asking.
6. **Given** a single file larger than one review part, **When** the review runs, **Then** the file is divided at function or section boundaries where possible and every line of it is reviewed.

---

### User Story 5 - Post findings as pull request comments (Priority: P3)

A user types `/sci-review:scientific-review <number> --comment`. After the findings are reported, each delivered finding is posted to pull request `<number>` as an inline review comment, one comment per finding, as `/code-review --comment` does. On a GitLab merge request, the findings are posted as one general note.

**Why this priority**: Useful for sharing a review with collaborators, but it depends on User Story 2 and on write access to the hosting service.

**Independent Test**: Run the review with `--comment` against a test pull request and compare the posted comments with the delivered findings.

**Acceptance Scenarios**:

1. **Given** a GitHub pull request target and `--comment`, **When** the review completes, **Then** every delivered finding appears on the pull request exactly once, as an inline comment; a finding that cannot be anchored to a line of the pull request diff is printed in the reply with a note instead.
2. **Given** `--comment` without a pull request target, **When** the review completes, **Then** the findings are printed in the reply as usual, nothing is posted, and the reply notes that `--comment` was ignored because the target is not a pull request.
3. **Given** `--comment` and a review with no findings, **When** the review completes, **Then** nothing is posted, as with `/code-review`.
4. **Given** the review cannot post (no access, no network), **When** posting fails, **Then** the local report is still delivered in full and the failure is reported with the reason.
5. **Given** a GitLab merge request target and `--comment`, **When** the review completes, **Then** the delivered findings are posted as one general merge request note listing each finding with its location, issue and suggested fix.

---

### User Story 6 - Apply fixes after the review (Priority: P3)

A user types `/sci-review:scientific-review --fix`. The review runs and reports its findings as usual. Then, exactly as `/code-review --fix` does, the user's own session model applies the findings to the local working tree, one finding at a time, skips those it should not apply, runs the relevant checks, and reports each finding again with its outcome.

**Why this priority**: It completes the parity with `/code-review`, but it depends on the report of User Stories 1 to 4 and is the only part of the feature that writes to the project. It requires a documented exception to the read-only guarantee of feature 007 (FR-006, SC-004) and an amendment of constitution Principle III for `sci-review` (see Assumptions).

**Independent Test**: Run the review with `--fix` on a fixture branch with a known defect, then inspect the working-tree diff, the outcome recorded for each finding and the checks that were run.

**Acceptance Scenarios**:

1. **Given** `--fix` and a review that delivers findings, **When** the findings have been reported, **Then** each finding is fixed directly in the working tree, without a confirmation prompt and without staging or committing anything.
2. **Given** `--fix` and a delivered finding whose fix would change the intended behaviour of the code, would require changes well outside the reviewed scope, or that is judged to be a false positive, **When** fixes are applied, **Then** that finding is skipped and the skip is noted, without arguing the finding.
3. **Given** `--fix` and a host with a findings-reporting tool, **When** the fixes have landed, **Then** the same findings are reported again through that tool, each with an outcome of `fixed`, `no_change_needed` (the finding was wrong or already handled) or `skipped` (real but not applied), the findings are not repeated as text, and the reply gives one line per skipped finding saying why.
4. **Given** `--fix` and a host without a findings-reporting tool, **When** the fixes have landed, **Then** the reply ends with a brief summary of what was fixed and what was skipped.
5. **Given** `--fix`, **When** the fixes have landed, **Then** the relevant checks of the project (for example its test suite for the changed modules) are run and their result is reported.
6. **Given** `--fix` and `--max-findings 3`, **When** eight findings are adjudicated, **Then** only the three delivered findings are considered for fixing.
7. **Given** `--fix`, **When** the panel phases run, **Then** no panel member writes to the project; only the closing fix step, after the findings are reported, changes files.
8. **Given** a review reported earlier in the session, with or without `--fix`, **When** some of its findings are fixed later in the session (at the user's request or incidentally), **Then** the findings are reported again with their outcomes immediately after the fixes land, as `/code-review` requires.

---

### Edge Cases

- `ultra` is given as the level: the review states that the cloud multi-agent level is specific to `/code-review` and is not available for the scientific review, suggests `max`, and runs nothing.
- Arguments are given in a different order (target before level): the level is recognised by its value wherever it appears, as long as it appears once; two levels in one command are a usage error.
- An unknown flag is given (for example `--post`): usage error naming the accepted flags; nothing runs.
- Explicit arguments and natural-language wording conflict (for example `low` together with "a thorough review with all seven perspectives"): explicit arguments win and the report records the override.
- A level and individual panel parameters are both given in words (for example `high` with "only one rebuttal round"): the individual parameter overrides that part of the level's configuration, and the report states the panel actually used.
- The host offers no persistent storage outside the project (for example claude.ai chat): persisted preferences are unavailable; the review uses the defaults and adds a notice saying that preferences could not be stored or read.
- A pull request target from a fork or a closed pull request: the diff is still reviewed when it can be read; a merged pull request is reviewed against the base commit at the time of merge.
- The target is a path outside the project root: usage error; nothing runs.
- A branch target that has not diverged from its base: same handling as feature 007 (ask for a baseline or another mode; never fall back silently).
- A finding whose evidence spans two review parts (for example a unit defined in one file and misused in another): each part's reviewers may read files outside their part to follow a reference, and the merge treats findings on the same defect from different parts as one.
- The review is started by the model on its own initiative on a scope above the large-scope threshold: it asks first, as for any large multi-agent run.
- The host stops the review partway through a large scope (context or time limit): the report lists the parts that were not completed as not reviewed, with that reason, instead of presenting the review as complete.

## Requirements *(mandatory)*

### Functional Requirements

**Grammar**

- **FR-001**: The skill MUST accept the explicit arguments `[level] [target] [--comment] [--fix] [--max-findings <n>|all|default]`, in any order, where `level` is one of `low`, `medium`, `high`, `xhigh`, `max`.
- **FR-002**: The skill MUST publish an argument hint with this grammar so that hosts that display one show it when the user types the skill's command.
- **FR-003**: The skill MUST reject, with a usage error naming the accepted values and before any reviewer runs, an unknown flag, a repeated level, `ultra`, and a token that begins with the first three letters of a level but is not one (for example `hig`) unless that token is an existing branch or path, in which case it is the target.
- **FR-003a**: As in `/code-review`, a malformed `--max-findings` value MUST NOT be an error: the review MUST ignore it, apply the persisted cap or, when there is none, the level's default cap, and tell the user in one line that the value was ignored and which values are accepted.
- **FR-003b**: As in `/code-review`, `--comment` without a pull request target MUST NOT be an error: the review MUST run, print its findings in the reply, post nothing, and note that `--comment` was ignored because the target is not a pull request.
- **FR-004**: Explicit arguments MUST take precedence over arguments inferred from the wording of the request; natural-language arguments defined by feature 007 MUST continue to work when no explicit argument covers them.

**Effort level**

- **FR-005**: Each effort level MUST map to one fixed, documented panel configuration (perspective count, rebuttal rounds, debate batches, default finding cap), within the limits of feature 007 (2 to 7 perspectives, 0 to 3 rounds, 1 to 4 batches), and no parameter MAY decrease from one level to the next in the order `low`, `medium`, `high`, `xhigh`, `max`.
- **FR-006**: `medium` MUST equal the defaults of feature 007, so that a review invoked with no arguments by a user with no persisted level behaves as it does today.
- **FR-007**: A level given explicitly by the user (typed as a command argument or written in the request) MUST be stored as the user's persisted level; a level chosen by the model when it starts a review on its own initiative MUST NOT be stored; a review with no level MUST reuse the persisted level, or `medium` when there is none.
- **FR-008**: The model MUST NOT select `max` on its own initiative; `max` is used only when the user, or an instruction file, asks for it explicitly.
- **FR-009**: The report MUST state the effort level used, whether it was given, reused or defaulted, and the panel actually used after any override.

**Target**

- **FR-010**: A target MUST resolve as follows: a pull request number, `#number` or pull request URL to the pull request's diff against its base; an existing branch name to that branch's diff against its base; one or more existing paths to paths mode. A target matching more than one form MUST cause the review to ask the user.
- **FR-011**: Resolving a target MUST NOT check out a branch, modify the working tree or the index, or create a file in the project (FR-006 and SC-004 of feature 007 continue to hold).
- **FR-012**: When a pull request target cannot be read, the review MUST say what is missing and offer a branch or paths review, never switching silently.

**Finding cap**

- **FR-013**: `--max-findings <n>` (n at least 1) MUST limit the delivered findings to the first n in report order; `all` MUST remove the limit; `default` MUST clear the persisted cap and apply the level's default cap.
- **FR-014**: A cap given by the user as `<n>` or `all` MUST persist for later reviews until `--max-findings default` is passed. The report MUST state the cap applied and the number of findings withheld by it; withheld findings MUST still be available in the run directory when the user keeps it.

**Posting**

- **FR-015**: With `--comment` and a pull request target, the review MUST behave as `/code-review --comment`: after the findings are reported, it MUST post each delivered finding once as an inline comment on a GitHub pull request (or all findings as one general note on a GitLab merge request), MUST print instead any finding it cannot post or anchor, with a note, and MUST post nothing when there are no findings. Its failure MUST NOT suppress the local report. The implementation MUST match that of `/code-review --comment`; it is specified in the plan.

**Fixing**

- **FR-016**: With `--fix`, the review MUST behave as `/code-review --fix`: after the findings have been reported, it MUST apply each delivered finding to the local working tree, without a confirmation prompt, and MUST NOT stage or commit anything. The fixes MUST be applied by the user's session model (the model the user selected, in the conversation that ran the review); no fixing agent, perspective reviewer or other panel member is started for them. The implementation MUST match that of `/code-review --fix`; it is specified in the plan.
- **FR-016a**: With `--fix`, the panel phases (independent round, merge, debate, moderator notes, adjudication, report) MUST remain read-only; only the closing fix step MAY write to the project, after the findings are reported, and no panel member MAY write to it.
- **FR-016b**: The review MUST skip, and note the skip of, any delivered finding whose fix would change intended behaviour, would require changes well outside the reviewed scope, or that is judged to be a false positive. A skip MUST NOT alter the finding's agreement label, which remains the one computed by adjudication.
- **FR-016c**: After applying fixes, the review MUST run the relevant checks of the project and report their result. Where the host has a findings-reporting tool, the review MUST then report the same findings again through it, each with an outcome of `fixed`, `no_change_needed` or `skipped`, without repeating the findings as text, followed by one line per skipped finding saying why; otherwise the reply MUST end with a brief summary of what was fixed and what was skipped.
- **FR-016d**: Whenever reported findings are fixed later in the same session, with or without `--fix`, they MUST be reported again with their outcomes immediately after the fixes land, before any prose summary.
- **FR-016e**: Without `--fix`, the read-only guarantee of feature 007 (FR-006, SC-004) MUST hold unchanged.

**Scope size**

- **FR-020**: The review MUST NOT exclude any reviewable file from the scope because of the scope's size; the fixed 6,000-line review budget of feature 007, and the "over budget" exclusion reason, MUST be removed.
- **FR-021**: A scope larger than one review part MUST be divided into review parts that together cover every reviewable line, with related files (same module or directory) kept in the same part where they fit; each part MUST receive the full independent round of every perspective, and candidate findings from all parts MUST be merged before the debate, so that a defect raised in several parts is debated and reported once.
- **FR-022**: Before any reviewer runs on a scope above the large-scope threshold, the review MUST state the scope size in lines and files and the number of review parts, and MUST ask the user for confirmation; when the user declines, it MUST run nothing and offer a narrower target. The threshold MUST be documented; its initial value is 6,000 lines, the former budget.
- **FR-023**: The report MUST state the number of review parts; any part not completed MUST be listed as not reviewed, with the reason.

**Persistence and portability**

- **FR-017**: Persisted preferences MUST be stored per user, outside every reviewed project, separately from `/code-review`'s own stored preferences, and MUST be readable on every host that offers such storage.
- **FR-018**: Where persistent storage is unavailable, the review MUST use defaults for omitted arguments and add a notice to the report; it MUST NOT fail.
- **FR-019**: The grammar MUST work identically on Claude and on Codex, and with every runner of feature 007; on hosts that cannot pass a command line to the skill, the same arguments MUST be accepted when written in the request.

### Key Entities

- **Invocation arguments**: the parsed level, target, flags and finding cap of one invocation, each marked as given, reused or defaulted.
- **Effort-level profile**: the fixed panel configuration associated with one level.
- **User preferences**: the persisted level and finding cap of one user.
- **Resolved target**: the review scope derived from the target (mode, baseline, paths, pull request reference), as recorded in the report.
- **Review part**: one subset of the scope, with its files and line ranges, its completion status, and the candidate findings its reviewers raised.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every argument form accepted by `/code-review`, except `ultra` and its `--post` and `--no-post` flags, is accepted by the scientific review with the same meaning; this is verified by a test table covering each form.
- **SC-002**: For each of the five levels, the panel recorded in the report matches the level's documented configuration in 100% of test runs.
- **SC-003**: A review invoked with no arguments by a user with no persisted preferences produces the same panel configuration as feature 007 in 100% of test runs.
- **SC-004**: Every invocation in the test table that FR-003 rejects is rejected before any reviewer runs, with a message that names the accepted values; every invocation covered by FR-003a or FR-003b runs to completion with a one-line note saying what was ignored.
- **SC-005**: The reviewed project is byte-for-byte unchanged after every review, for every target form and every flag other than `--fix`; with `--fix`, the only changes are uncommitted working-tree changes made after the findings are reported, and every delivered finding carries an outcome.
- **SC-006**: With `--comment` on a pull request target, every delivered finding is either posted exactly once or printed with a note saying why it was not posted, in 100% of test runs.
- **SC-007**: A user familiar with `/code-review` can start a scientific review of a pull request at a chosen level on the first attempt, without consulting the documentation.
- **SC-008**: On a fixture scope of 18,000 reviewable lines (three times the former budget), 100% of reviewable files are reviewed, and a defect placed in the last file is reported.
- **SC-009**: On scopes at or below the large-scope threshold, the number of findings reported for the seeded defects of feature 007's fixtures does not decrease compared with feature 007.
- **SC-010**: With `--fix`, every delivered finding is reported again with an outcome (`fixed`, `no_change_needed` or `skipped`), and every `skipped` finding has a stated reason, in 100% of test runs.

## Assumptions

- The arguments copied are those of the host's `/code-review` skill as described in its skill listing on 2026-11-04: the five effort levels, the target forms, `--comment`, `--fix` and `--max-findings`. `ultra` and its `--post` and `--no-post` flags are a cloud service of the host and are not reproduced.
- The persisted level is the scientific review's own and is not shared with `/code-review`, because the two reviews have different costs at the same level.
- Reading and commenting on a pull request rely on the hosting service's command-line client being installed and authenticated; when it is not, the review says so (Principle IV).
- Posting comments is an outward-facing action; passing `--comment` is taken as the user's explicit request for it, as with `/code-review`.
- The default finding cap of every level is unbounded in the Markdown report, so that a review with no arguments delivers every finding, as feature 007 does (FR-006). When findings are delivered through a host's findings-reporting tool, they are clamped to that tool's maximum (32), as `/code-review` does. The ranking used for the cap is the report order of feature 007.
- This feature extends feature 007 and does not change its adjudication rules or report schema beyond adding the level, the cap, the withheld count and the number of review parts. The independent round changes only in that it runs once per review part.
- Removing the budget raises the cost of large reviews roughly in proportion to their size. Confirmation above the large-scope threshold (FR-022) replaces silent truncation as the guard against an unexpectedly expensive run; the effort level does not change the threshold.
- The size of one review part is a planning decision, set so that one reviewer can read the whole part together with the dimension documents and its role brief; it is not a user-facing argument.
- `--fix` reproduces `/code-review --fix` as shipped in Claude Code 2.1.317 (2026-11-04), in behaviour and in implementation. The behaviour is specified here; how it is implemented, and the reference text it reproduces, are recorded in the plan.
- `--fix` conflicts with two rules in force, which the plan must amend before implementation: the read-only scope of `sci-review` in the constitution's Scope and Constraints section and FR-006 of feature 007, which this feature narrows to reviews without `--fix`; and constitution Principle III ("Show Before Changing"), which requires a diff and confirmation before writing. Matching `/code-review` requires a recorded exception to Principle III for an explicit `--fix` request, which is a constitution amendment (MINOR version).
- Contested findings are delivered and therefore considered for fixing; as in `/code-review`, the skip rules of FR-016b are the filter, and the user narrows the set further with `--max-findings` or by discarding changes.
- A pull request target, or a branch that is not checked out, is not in the working tree; `/code-review` has no special rule for this case, and its findings are then skipped under FR-016b as requiring changes outside the reviewed code.
- The undocumented `--budget` option of feature 007's helper script is removed together with the budget; a user who wants a smaller review names paths instead.
