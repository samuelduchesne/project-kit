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

**Rationale**: The class drives a deterministic rule (the severity cap, FR-004), so it must come from the agents that check reach against configuration and deployment files, not from the agent that raised the finding. A closed set keeps the cap testable.

**Alternatives considered**: finder-assigned class, checked by verifiers (the criticised finding would have been classed `operator-change` by its finder and `release` by a verifier; letting the verifier decide is simpler than reconciling the two); a free-text frequency estimate (not testable).

## R4. The reach step

**Decision**: Insert a step between the verifier's step 2 (search for a refutation) and step 3 (establish the scenario):

> **2b. Establish practical reach.** When the trigger depends on configuration, a deployment, a release or data provenance, find how that state comes about. Read the project's settings classes and their defaults, environment files (`.env*`, `docker-compose*`), deployment manifests (Kubernetes, Helm, Terraform, Procfile, CI deploy and release workflows), and the release process (version files, changelog, tags). Record in `reach` the files read and what each showed. Choose `trigger_class`. Check every concrete value the finding quotes (a setting, a constant, a version, a count) against the repository and record each contradiction in `value_corrections`.

A verdict whose `trigger_class` is `unreachable` MUST be `refute` (validated by `panel.py validate`).

**Rationale**: In the criticised review, the verifiers followed callers (step 1) but read no configuration. The environment file would have contradicted the value the reproduction quoted, and shown that the setting differs by deployment rather than over time. Listing the usual file locations makes the step concrete without a tool.

**Alternatives considered**: a `panel.py` command that lists configuration and deployment files for the verifier (deterministic, but the relevant files depend on the trigger, and the verifier already searches with `grep`; listed as a possible follow-up); making the step conditional on the dimension (the trigger's dependence on configuration is the condition, not the dimension).

## R5. Severity on realistic use, and the cap

**Decision**: Every role brief and `protocol.md` section 4 adopt this definition:

- **High**: produces a wrong result in ordinary use of the software.
- **Medium**: produces a wrong result only in plausible edge cases, or only after a rare operational event (a release, an operator changing configuration), or prevents reproduction of a result.
- **Low**: a latent risk that does not currently produce a wrong result.

`panel.py adjudicate` lowers a `high` finding to `medium` when its reported trigger class is `release` or `operator-change`, unless the merged finding carries a `severity_reason`. It records `severity_capped: true` on the finding so the report can say so.

**Rationale**: The definition change fixes the reviewer's judgment, and the cap catches findings where the reviewer and the verifier disagree on frequency. `severity_reason` already exists for the moderator (protocol.md section 4). The cap is deterministic, so it belongs in the script (Principle II).

**Alternatives considered**: a cap applied to every class but `user-action` (too strong: a data condition such as a leap-year weather file is ordinary use in building energy work); no cap, only the definition (the criticised finding shows that reviewers already believed their trigger was "realistic").

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
2. a line of badges (severity, label, dimension, trigger class, and "capped" when applied);
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
| C6 | Severity | Severity is at most `medium`. |
| C7 | Owner | Suggested owners come from the file's ownership or history and include an expected owner; they are not the algorithm's author alone. |

The evaluation passes when the treatment passes C1 to C7, the judge prefers it, and the run used no more panel agents than its estimate. It is one case, so it shows the feature works on the motivating example. It does not measure precision or recall; the fixture criteria SC-001 to SC-005 do that.

**Alternatives considered**:
- Re-running the original scope: many review parts and many more agents, for one finding; too costly for a quick check.
- Running sci-review 0.3.0 again as the baseline: it can only produce a report row, and the filed issue is the real artifact.
- Asking the domain reviewer to score: the best judge, but outward-facing; proposed to the user as an optional follow-up, not part of the plan.
- Committing the case to this repository: it is public, and the case belongs to a private project.
