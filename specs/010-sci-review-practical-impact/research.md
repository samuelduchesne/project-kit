# Research: Findings that say who hits them

Decisions for feature 010, each with its rationale and the alternatives considered. The source facts come from the sci-review plugin at `ae8bc1b` (sci-review 0.3.0) and from the downstream review that motivated the feature (see spec Overview).

## R1. Who writes context and in practice

**Decision**: Finders write `headline`, `context` and `in_practice` on every candidate. The merge moderator chooses or combines them for a cluster of several candidates, under the same rule as `summary` (no claim that no member made). The automatic merge copies them.

**Rationale**: Finders have already read the code and its callers. Verifiers would duplicate that reading if they wrote the prose; instead they check it through reach (R4). The rule keeps the agent count unchanged (FR-013).

**Alternatives considered**: a separate "editor" agent that rewrites each finding for a lay reader (one more agent per batch, against FR-013 and the cost work of feature 009); having the verifier write the prose (verifiers see merged findings only after the merge, so the report would lack prose for findings no verifier reached, such as those in a run whose verify phase did not complete).

## R2. A headline field

**Decision**: Add `headline` to the candidate: at most 90 characters, plain words, naming the situation, not the code (for example "Cached results are not recomputed after a release"). It is the issue title and the heading of the finding in the report.

**Rationale**: Story 5 requires an issue title "phrased as the situation, not the code". `summary` is a technical sentence and is kept for the table and for `ReportFindings`. Deriving a title from `context` by truncation gives broken sentences.

**Alternatives considered**: reuse `summary` (fails Story 5.1 on the criticised finding, whose summary names hashes); take the first sentence of `context` (too long for a title in most cases).

## R3. Trigger class: who records it and how it is combined

**Decision**: Verifiers record `trigger_class` on every verdict, from the closed set `user-action`, `data-condition`, `release`, `operator-change`, `unreachable`. The reported class is the most frequent class among non-refuting verdicts. A tie goes to the more frequent trigger, in the order `user-action`, `data-condition`, `release`, `operator-change`. A finding with no non-refuting verdict has no class. Finders do not record the class: they write `in_practice` in prose.

**Rationale**: The class must come from the agents that check reach against configuration and deployment files, not from the agent that raised the finding. A closed set keeps the report consistent across runs. The class is shown to the reader and changes no outcome (R5).

**Alternatives considered**: finder-assigned class, checked by verifiers (the criticised finding would have been classed `operator-change` by its finder and `release` by a verifier; letting the verifier decide is simpler than reconciling the two); a free-text frequency estimate (not testable).

## R4. The reach step

**Decision**: Insert a step between the verifier's step 2 (search for a refutation) and step 3 (establish the scenario):

> **2b. Establish practical reach.** When the trigger depends on configuration, a deployment, a release or data provenance, find how that state comes about. Read the project's settings classes and their defaults, environment files (`.env*`, `docker-compose*`), deployment manifests (Kubernetes, Helm, Terraform, Procfile, CI deploy and release workflows), and the release process (version files, changelog, tags). Record in `reach` the files read and what each showed. Choose `trigger_class`. Check every concrete value the finding quotes (a setting, a constant, a version, a count) against the repository and record each contradiction in `value_corrections`.

A verdict whose `trigger_class` is `unreachable` MUST be `refute` (validated by `panel.py validate`).

**Rationale**: In the criticised review, the verifiers followed callers (step 1) but read no configuration. The environment file would have contradicted the value the reproduction quoted, and shown that the setting differs by deployment rather than over time. Listing the usual file locations makes the step concrete without a tool.

**Alternatives considered**: a `panel.py` command that lists configuration and deployment files for the verifier (deterministic, but the relevant files depend on the trigger, and the verifier already searches with `grep`; listed as a possible follow-up); making the step conditional on the dimension (the trigger's dependence on configuration is the condition, not the dimension).

## R5. Severity on ordinary use, without a cap (revised)

**Decision**: Every role brief and `protocol.md` section 4 adopt this definition:

- **High**: produces a wrong result in ordinary use of the software.
- **Medium**: produces a wrong result only in plausible edge cases, or prevents reproduction of a result.
- **Low**: a latent risk that does not currently produce a wrong result.

Reviewers judge ordinary use from what they read: where the inputs come from and how the project is configured and deployed. Adjudication never changes a severity on the trigger class; the class is shown beside it.

**Rationale**: The first version of this decision added an automatic cap: `high` lowered to `medium` when the only trigger was a release or an operator change, unless a `severity_reason` was recorded. It was implemented and then removed, for three reasons:

1. **The rarity it assumed is not known.** How often a project releases, or changes a setting, differs between projects. A cache that silently serves stale results to every user after every release is not obviously `medium` in a project that releases weekly.
2. **It fired almost always.** In the verify protocol most batches are merged without a moderator, so no `severity_reason` is recorded to keep a finding high.
3. **It generalises badly.** A second downstream issue was dismissed as "unlikely to ever be hit in practice", although its own check found about a third of whole-lot bounds rounded wrongly. The issue had led with its rarest case. A rule that lowers severity on a guessed rarity would make that error systematic. The remedy is better evidence and better framing (R13, and the in-practice rule of R1), not a downgrade.

**Alternatives considered**: keeping the cap with a mandatory moderator (one more agent per batch, against FR-013, for a rule whose premise is unreliable); a severity cap on a guessed prevalence of the input (rejected for reason 3).

## R6. Possibly intended: a mark, not a fourth verdict

**Decision**: A verdict gains `possibly_intended` (boolean, default false) and `possibly_intended_reason` (required when true). A `confirm` or `uncertain` verdict can carry the mark; a `refute` cannot. When labels are computed, a marked verdict counts as `uncertain`. After the existing rule 2 (Refuted) of protocol.md section 5.1, a new rule applies:

> **2a. Design question**: at least one verdict is marked possibly intended. The finding is not rejected; its label is computed by the remaining rules with the marked verdicts counted as uncertain, and it is reported with `kind: design-question`.

All other findings have `kind: defect`. In the debate protocol (`max`), the defender's position gains the same optional mark and reason. A finding with a defender mark that is not withdrawn is a design question.

**Rationale**: A fourth verdict would change every label rule and every test of feature 009. A mark leaves those rules as they are and adds one routing decision (FR-007). Counting the mark as uncertain keeps a design question from being reported as `consensus` on the strength of a verifier who doubted it was a defect.

**Alternatives considered**: a fourth verdict value (larger change, same outcome); a moderator decision after verification (one more agent).

## R7. The stale-cache question

**Decision**: Replace guiding question 7 of the computer-scientist brief with: "Can a cache or memoised value be returned after something it depends on has changed, including the code or configuration that computed it? If so, is the reuse deliberate (stability, cost), and what in the code or its documentation says so?" Add the matching check to `dimensions/algorithmic-correctness.md`, under stale caching: "State whether the reuse looks intended; if it might be, say so in `in_practice`, so that a verifier can mark it."

**Rationale**: Without this change, the brief asks whether staleness is possible and never whether it is wanted. That is what produced a defect report for what may be a stability choice.

## R8. Report layout

**Decision**: In `report.md`, the findings table is replaced by one block per finding. Each block has:

1. a heading `Fn. <headline>`;
2. a line of badges (severity, label, dimension and trigger class);
3. the context paragraph;
4. an "In practice" paragraph;
5. a compact list: location, trigger (with value corrections inline), wrong output, fix, raised by.

Design questions follow the defects under their own heading "Design questions". There they are introduced by the possibly-intended reason and the wrong output, under "If this is not intended". `report.json` carries every new field. The `ReportFindings` mapping (contracts/report.md of feature 007, section 3) prefixes `summary` with the headline and puts `context` and `in_practice` at the start of `failure_scenario`.

**Rationale**: The table puts nine technical columns side by side, so prose does not fit in it. Story 1 requires the prose to come first.

## R9. The issue command

**Decision**: `panel.py issue --run RUN --finding Fn [--dry-run]` renders `issues/Fn.md` in the run directory and prints it. Its layout is fixed by [contracts/issue.md](./contracts/issue.md). Owners:

1. **Ownership file.** The first existing file among `.github/CODEOWNERS`, `CODEOWNERS`, `docs/CODEOWNERS` and `.gitlab/CODEOWNERS`, read at the scope's head. Patterns follow the gitignore subset that the hosts document (anchored `/`, trailing `/` for directories, `*`, `**`), and the last match wins. GitLab sections are read as plain rules.
2. **Otherwise, blame.** `git blame --line-porcelain -L start,end <head> -- file`, counting lines by author. The command lists up to three authors, ordered by count and then by most recent commit. Boundary commits of a shallow clone are reported as "history truncated".
3. **Otherwise** (no git, or a file not in history), no owners, with a sentence saying why.

The issue command must run before `panel.py clean`, which removes the run directory. The SKILL.md closing steps offer the command for each delivered finding and never post the issue.

**Rationale**: Ownership files and blame are deterministic and need only files and `git` (Principle IV). Posting is outward-facing and is left to the user (Principle III; spec Assumptions).

**Alternatives considered**: a host API for owners or teams (needs `gh` or `glab` and network access, and adds nothing over CODEOWNERS); `git log -L` (slower, and it follows moved lines that are irrelevant to ownership).

## R10. Runs from earlier versions

**Decision**: Every new field is optional in the dataclasses (`_optional`) and defaults to null. `report` and `issue` print "not recorded" for missing prose and omit the trigger-class badge and owners' section reasons that depend on it. Schemas for *new* messages make the fields required, so new runs always carry them.

**Rationale**: FR-012. Run directories live under the system temporary directory and can outlive a plugin upgrade within a session.

## R11. Extensions and generated runners

**Decision**: Extension perspective briefs need no change. Every perspective's task names `candidate-findings.schema.json`, and an output that lacks the new fields fails `panel.py validate` and is returned to the agent with the errors (feature 007 behaviour). The building-energy extension in the idfkit plugin is updated separately, outside this repository, to add an "In practice" paragraph to its brief. `build_workflow.py` embeds the schemas and briefs, so the Workflow script `scripts/scientific-review-panel.js` is regenerated. The Codex panelist agent file needs no change.

## R12. Evaluation on the criticised module

**Decision**: A quick, single-case evaluation runs after implementation and is recorded in `validation.md`. Its full method is in [quickstart.md](./quickstart.md), scenario 6.

The case comes from a private downstream project, so this repository names neither the project nor its people. The evaluator keeps a **case file** outside the repository (format in quickstart scenario 6). It holds:

- the repository and the commit the original review ran on;
- the module to review;
- the issue as filed (the baseline) and the domain reviewer's comment;
- a one-sentence description of the finding to match;
- the expected trigger class;
- the quoted values to check, with the files that hold them;
- the expected owners.

`validation.md` records only anonymised results: criterion verdicts, counts, agents, tokens, and paraphrased observations, with no names, paths or quotations from the downstream project.

- **Scope**: paths mode on the single module that holds the criticised finding, at the original commit, in a separate worktree. The original review covered a much larger change (many review parts); narrowing to the module keeps the run to about 7 agents. Verifiers may still read configuration and environment files outside the scope, because they read outside it to judge a finding.
- **Level and runner**: `medium`, `claude-workflow`, empty preferences, as in the validation of feature 009.
- **Baseline**: the issue as filed, verbatim. sci-review 0.3.0 has no issue renderer, and the filed issue is the artifact that drew the criticism.
- **Treatment**: the `panel.py issue` output for the finding that matches the case file's description. If no finding matches, the run is repeated once. If it still does not match, the evaluation reports a recall failure and no comparison.
- **Comparison**: a blind judge agent receives the domain reviewer's comment, the rubric below and the two bodies in random order, labelled A and B. It returns a verdict per criterion and a preference. The orchestrator checks the deterministic criteria (C5 to C7) itself, against the case file.

| # | Criterion (from the domain reviewer's comment) | Pass when |
|---|------------------------------------------------|-----------|
| C1 | Orientation | The title and first section are understandable without opening the code. |
| C2 | Who triggers it | It names the realistic trigger of the case file (here, a release of new code). |
| C3 | How often and who notices | It states frequency and whether users would notice. |
| C4 | Intent | It is a design question, or it states that the behaviour may be deliberate. |
| C5 | Quoted values | It contains no value that the repository contradicts, in particular the value the baseline got wrong. |
| C6 | Checkable evidence | It includes a runnable reproduction or an extent table that the reader can check without trusting the prose. |
| C7 | Owner | Suggested owners come from the file's ownership or history and include an expected owner; they are not the algorithm's author alone. |

The evaluation passes when the treatment passes C1 to C7, the judge prefers it, and the run used no more panel agents than its estimate. It is one case, so it shows the feature works on the motivating example. It does not measure precision or recall; the fixture criteria SC-001 to SC-005 do that.

A second downstream issue was later reviewed by the same domain reviewer. It joins the case file as a second case, with the same seven criteria: its realistic trigger is a data condition (offers entered in pounds with whole-lot bounds), and C2 asks that the issue lead with that common condition rather than its rarest form.

**Alternatives considered**:
- Re-running the original scope: many review parts and many more agents, for one finding; too costly for a quick check.
- Running sci-review 0.3.0 again as the baseline: it can only produce a report row, and the filed issue is the real artifact.
- Asking the domain reviewer to score: the best judge, but outward-facing; proposed to the user as an optional follow-up, not part of the plan.
- Committing the case to this repository: it is public, and the case belongs to a private project.

## R13. Evidence a reader can check, and what the review leaves to the reviewers

**Decision**: A verdict with evidence `reproduced` records `reproduction`: the code or command the verifier ran and the output it observed. `panel.py validate` rejects a reproduced verdict without one. A verdict may also record `extent`: a few runs, input by input, with the expected and the actual result, including ordinary inputs the code handles correctly. The report and the issue show those of the first non-refuting verdict, preferring a reproduced one. Tables of different verifiers are not merged, because each is a set of runs to be checked as a whole.

The in-practice statement (R1) must state the triggering conditions in the users' terms and lead with the most common way the defect shows. It must cite where the triggering inputs come from (a form, an API schema or validator, a default, seed data, a configuration file), or say that their frequency is unknown.

**Rationale**: The domain reviewer's comment "valid, if we trust what the LLM has written" names the real limit of prose: context and in-practice statements are more claims by the same model. A runnable reproduction and a short input table are evidence the reader can check in a minute. The reviewer also asked for a compact table of inputs and outputs, to judge the extent of a defect.

**What is deliberately not specified**:
- **How a fix is chosen.** The same reviewer preferred an interface change to the proposed tolerance fix, and also said that whatever is simple and expedient is fine. The two remarks pull against each other, and choosing an interface is a decision for the module's owners. The review proposes the fix it judges best.
- **A prevalence estimate that changes outcomes.** Covered in R5.

**Alternatives considered**:
- Merging the extent tables of all verifiers (rows from different runs and set-ups read as one experiment);
- A required extent table (some defects, such as a wrong unit everywhere, have no meaningful input dependence).

## R14. Closing the gaps the first validation found (validation.md section 5)

**Decision**:

1. **The verifier revises the in-practice statement.** A verdict may carry `in_practice_revision`: a full replacement statement, written when the verifier's reach contradicts or omits part of the finder's. The reported finding uses the first non-refuting verdict's revision, keeps the finder's text as `in_practice_original`, and is marked revised. The report and the issue say "(revised by the verifier)".
2. **No dropping on rarity.** Finder briefs: a concrete defect is reported even when it seems rare; its frequency is stated as unknown or as what it depends on. Verifier brief: rarity is not grounds for refutation; unreachability is.
3. **Releases as a trigger.** For a cached, stored or memoised result, finders and verifiers ask whether a release of new code that changes how the result is computed is a trigger, as well as configuration and inputs. The algorithmic-correctness dimension's stale-caching check says so.
4. **What blame shows.** History-based owners are introduced as "Last changed these lines". When every cited line comes from one commit whose subject ends in a pull request reference (`(#123)` or `!123`), the issue says the lines come from that merged pull request, so the suggestion names its author or merger, not necessarily the owner.
5. **Line numbers per file.** Finder briefs: line numbers are those of the file itself (as `grep -n` on that file shows), never counted across the files of a part. The first validation's cross-file numbers came from finders reading several files as one text.
6. **Superseding issues.** `panel.py issue --supersedes <ref>` (repeatable) opens the body with "Supersedes <ref>, <ref>." The user decides which issues a new one replaces.
7. **A fixture that can fail.** `practical-repo` is rebuilt with results and reports stored in a JSON file on disk that persists across processes and releases, so the stored-result and deliberate-reuse cases are reachable, and gains a unit-conversion case: quantities entered in pounds are converted to tonnes before whole-lot rounding.

**Rationale**: Each closes a failure observed in the first validation where the review's own evidence could have prevented a wrong issue. The revision is a verifier field, not a new agent (FR-013). Items 2, 3 and 5 are brief text; items 1, 4 and 6 are deterministic and live in `panel.py` (Principle II).

**Alternatives considered**: having the finders write in-practice after verification (a second finder pass, one more agent per finder); merging finder and verifier statements automatically (two partly contradictory statements cannot be merged without judgement); detecting squash merges from the hosting API (needs a network client; the commit subject is enough).
