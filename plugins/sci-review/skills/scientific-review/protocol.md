# Panel protocol

This document is the single source of the review protocol. Every runner (Claude Workflow, Codex subagents, Claude agents, sequential) follows it, and `scripts/panel.py` implements its deterministic steps. Section 12 is the procedure that the three file-based runners share; each runner file adds only how it starts a task.

A panel judges findings by one of two protocols (spec 009), recorded as `protocol` in `panel.json`:

- **verify** (every level but `max`): finders review the code, a script merges their candidates, and independent verifiers judge each merged finding. The number of agents grows with the number of findings, not with the panel size times the rounds.
- **debate** (`max`, or when rebuttal rounds are asked for): the feature 007 protocol. Every perspective and the defender state positions on every finding over rebuttal rounds, and the moderator writes notes.

## 1. Roles

- **Perspective reviewers (finders)**: the five defaults (`theorist`, `numerical-analyst`, `experimentalist`, `methodologist`, `computer-scientist`), the `generalist` (the single finder of the low level, verify protocol only) and any selected domain perspective contributed by an extension. In the verify protocol each default perspective focuses on the dimensions listed in its `dimensions` in `panel.json`: together they cover all five, and each still reports a defect it notices outside its focus. The generalist and domain perspectives, and every perspective of a debate, review under all five dimensions.
- **Verifier** (verify protocol): judges every merged finding of its batch independently, trying first to refute it. One to three verifiers per batch (`verifiers` in `panel.json`), with ids `v1`, `v2`, `v3`. Never raises findings and never sees another verifier's verdicts.
- **Defender** (debate protocol): argues that each finding is not a defect. Never raises findings and never withdraws.
- **Moderator**: merges the candidates of a batch that holds a cluster of several candidates (both protocols), and, in a debate, writes notes on each finding after its debate. Never introduces findings and never assigns labels.

## 2. Phases

1. **Independent round.** `panel.py parts` divides the scope into review parts of at most 2,000 lines (section 6). Each perspective reviews every part, one part per task, without access to any other reviewer's output, and writes one candidate-findings message per part, `candidates/<perspective>--<part>.json`, whose `part` field names the part. A reviewer may read any file of the project to follow a reference, but raises findings only on lines of its part. In a review of several parts it numbers its findings `<perspective>-<part>-<n>` (for example `theorist-p2-1`); in a review of one part, `<perspective>-<n>`.
2. **Merge.** `panel.py merge` clusters the candidates of every part by location and groups the clusters into batches (section 7). `panel.py auto-merge` writes the merge ruling of every batch whose clusters each hold one candidate: each merged finding is its candidate. The moderator writes the merge ruling of each other batch, confirming or splitting each cluster.
3. **Judgement.**
   - *Verify*: each verifier of a batch writes one verification message with a verdict on every merged finding of the batch (`verify/batch-<b>/<verifier>.json`). Verifiers of a batch run in parallel and independently.
   - *Debate*: the perspectives and the defender state positions on every merged finding of the batch in round 0, followed by at most `rebuttal_rounds` rebuttal rounds (section 8). When the debate of a batch ends, the moderator writes notes on every finding of the batch.
4. **Adjudication.** `panel.py adjudicate` computes each finding's label, or rejects it, from the verdicts or the positions by the rules of section 5, and attaches the verifiers' arguments or the moderator's notes. No model takes part in this step.

## 3. Role inputs

Each role receives exactly the inputs below and nothing else (SC-011). Besides its inputs, a panel member may read the files of the reviewed project. When `scope.json` has a `target` of kind `branch` or `pull-request`, the reviewed files are not in the working tree: read each one at the scope's `head` with `git -C <project> show <head>:<path>`.

| Phase | Role | Receives | Must not receive |
|-------|------|----------|------------------|
| Independent (one task per part) | perspective | its brief; its focus dimensions and their dimension documents (the others on demand); extension reference material if it is a domain perspective; `scope.json`; its review part (`parts.json`) | any other perspective's output; this protocol |
| Merge | moderator | its brief; all candidate files; the clusters from `panel.py merge` | none |
| Verify | verifier | its brief; the batch's merged findings | candidates, other verifiers' verdicts, labels |
| Debate round 0 | each perspective and defender | its brief; the batch's merged findings; its own independent output (its candidate files of every part) | other members' round 0 positions |
| Debate round k > 0 | each perspective and defender | its brief; the batch's merged findings; all positions from rounds 0 to k-1 | positions from round k |
| Moderator notes | moderator | its brief; the batch's merged findings; all positions of the batch | labels (they are computed afterwards) |

A verifier may also read configuration, environment, deployment and release files outside the scope, to establish how a trigger state comes about (its reach).

### 3.1 Finding prose

Every finding is written for a reader who has not opened the code (spec 010). Finders write three statements on each candidate; the moderator chooses or combines them for a cluster under the rule that applies to `summary`, and the automatic merge copies them. Verifiers check them through reach, and a verifier whose reach contradicts or omits part of the in-practice statement writes a replacement (`in_practice_revision`); the report uses the first non-refuting verdict's replacement, keeps the finder's text, and marks it revised. Finders never drop a concrete defect because it seems rare, and cite line numbers within each file.

- **`headline`**: at most 90 characters, plain words, naming the situation, not the code. It is the finding's heading in the report and the title of its issue.
- **`context`**: one or two sentences on what the code does for its users and the situation in which the finding arises.
- **`in_practice`**: who or what triggers the finding (a user action, a deploy or release, an operator changing configuration, a data condition), roughly how often, and whether anyone would notice the wrong result. It states the triggering conditions in the users' terms, leads with the most common way the defect shows, and cites where the triggering inputs come from, or says that their frequency is unknown.

Each verdict that ran the trigger records the **reproduction** (the code or command and its output) and may record an **extent** table (a few runs, input by input, expected against actual); the report and the issue carry the first non-refuting verdict's, preferring a reproduced one, so that a reader can check the finding rather than trust it. Each verdict records a **trigger class**: `user-action`, `data-condition`, `release`, `operator-change` or `unreachable`, summarising how the trigger state comes about. `unreachable` is only allowed with `refute`.

## 4. Severity

Each finding carries one of three severities (FR-018):

- **High**: produces a wrong result in ordinary use of the software.
- **Medium**: produces a wrong result only in plausible edge cases, or prevents reproduction of a result.
- **Low**: a latent risk that does not currently produce a wrong result.

A merged finding takes the highest severity among its members unless the moderator records a `severity_reason` for a lower one.

Severity is the reviewers' judgement, made from what they read about where the inputs come from and how the project is configured and deployed. The trigger class (section 5.1) is reported beside it and never changes it: how often a release or a configuration change happens differs between projects, and a guess about how rare an input is must not lower a finding.

## 5. Adjudication

### 5.1 Verify protocol

For each merged finding, count the verdicts of its batch's verifiers: `confirm` (the failure scenario was reproduced or traced and no reason the code is correct was found), `refute` (the code is correct, or the trigger cannot occur) and `uncertain` (the verdict turns on an assumption the code does not settle). Each verdict records its `evidence` (`reproduced`, `traced` or `none`) and where the verifier searched for a refutation; a `confirm` whose evidence is `none` counts as `uncertain`. The raisers are the perspectives in its `raised_by`, each of which found it independently. The rules are applied in order; the first that matches decides:

1. **Not verified**: no verifier recorded a verdict. Label `contested`, with a notice.
2. **Refuted**: more verifiers refute than confirm. The finding is rejected, with the first refuting verifier's reason.
2a. **Design question**: at least one verdict is marked possibly intended. The finding is not rejected; its label is computed by the remaining rules with the marked verdicts counted as uncertain, and it is reported with `kind: design-question`, under "Design questions" after the defects.
3. **No concrete failure scenario**: `trigger` or `wrong_output` is null. Label `contested`.
4. **Consensus**: every verifier confirms, and the raisers plus the confirming verifiers number at least two, so that no finding is reported as consensus on one agent's word (FR-013).
5. **Majority**: more verifiers confirm than refute.
6. **Otherwise** (a tie, or every verdict uncertain): label `contested`.

A contested finding carries the strongest `argument_for` of a verifier that did not refute it, the `argument_against` of one that did not confirm it, and the first `deciding_assumption` recorded, preferring an uncertain verdict's. A finding without a concrete scenario carries the first `no_trigger_reason` recorded.

**Trigger class and reach.** The reported trigger class is the most frequent class among the verdicts that do not refute the finding; a tie goes to the more frequent trigger, in the order `user-action`, `data-condition`, `release`, `operator-change`. The reported reach is that of the first such verdict with the reported class. The value corrections of all verdicts are combined, without duplicates, and shown next to the trigger.

### 5.2 Debate protocol

**Stance.** A member's stance on a finding is its latest position on that finding. A member that is not called in a later round (because section 8 did not call it, or the batch stopped early) keeps its latest position. A raiser that recorded no position is taken to accept the finding it raised.

**Position identifiers.** A position is identified as `<member>:<finding_id>:<round>`, for example `defender:F3:0`. The `answers` field of a position lists the identifiers of the positions it responds to.

**Answered objection.** A defender objection is a defender position with stance `challenge`. It is answered when a later position by any perspective reviewer lists it in `answers` and the defender does not challenge again in a subsequent round. A defender objection is therefore unanswered when the defender's latest stance on the finding is `challenge` and either no perspective position has answered any earlier defender position on the finding, or the defender challenged again in a round after the latest such answer. A challenge the defender repeats in the same round as the answer does not reopen the objection, because the defender had not yet seen the answer.

**Design questions.** When the defender's latest position on a finding is marked possibly intended, the finding is reported with `kind: design-question`, under "Design questions" after the defects; its label is computed by the rules below unchanged. Only the defender may mark a position. A debate finding carries no trigger class or reach, so the severity cap does not apply.

**Undebated findings.** A merged finding on which no member recorded a position, and a candidate finding that no merge ruling includes, are reported as notices.

**Perspectives.** For the rules below, "perspectives" means every perspective reviewer in the panel, default and domain, the raiser included, and never the defender. The majority denominator is the number of perspectives in the panel.

The rules are applied in order; the first that matches decides:

1. **Raiser withdrew**: every raiser of the finding has stance `withdraw`. The finding is rejected (reason `withdrawn`).
2. **Only one perspective accepts and a defender objection is unanswered**: fewer than two perspectives have stance `accept`, and a defender objection is unanswered. The finding is rejected (reason `unsupported`). A co-raiser that still accepts counts as a second perspective, because it detected the defect independently.
3. **No concrete failure scenario**: `trigger` or `wrong_output` is null. The finding is at most `contested`, so it is labelled `contested`.
4. **Consensus**: no perspective has stance `challenge` or `withdraw` (a co-raiser that withdraws dissents), at least two perspectives have stance `accept` (so that no finding is reported as consensus on its raiser's word alone, FR-013), and no defender objection is unanswered. Label `consensus`.
5. **Majority**: more than half of the perspectives have stance `accept`. Label `majority`.
6. **Otherwise**: label `contested`.

**Several raisers.** When `raised_by` lists more than one perspective, each raiser is a perspective like any other for rules 2, 4 and 5, and its stance is its own latest position (accept when it recorded none). The finding is rejected as withdrawn only when every raiser withdraws (rule 1). One raiser's withdrawal does not reject the finding and does not remove that raiser from `raised_by`; it is a dissenting stance, so it prevents consensus (rule 4) and does not count towards a majority (rule 5).

`withdraw` is valid only from a member listed in the finding's `raised_by`; any other `withdraw` is a protocol violation and stops adjudication with exit code 1.

The moderator's notes are attached after labelling: `argument_for`, `argument_against` and `deciding_assumption` only to contested findings, `rejection_reason` only to rejected findings (replacing `withdrawn` or `unsupported` unless it is "Not rejected."), and `no_trigger_reason` to every finding whose `trigger` or `wrong_output` is null.

## 6. Limits and cost

- Panel size 1 to 7 perspectives in the verify protocol and 2 to 7 in a debate, counting domain perspectives; a request for more than are available yields all of them.
- Verifiers 1 to 3 per batch. Rebuttal rounds 0 to 3 (debate only). Batches 1 to 4.
- Out-of-range values are clamped, and the report states the panel actually used.
- Effort levels set the panel together:

  | Level | Finders | Protocol | Batches | Verifiers per batch |
  |-------|---------|----------|---------|---------------------|
  | `low` | the generalist, plus selected extensions | verify | 1 | 1 |
  | `medium` | theorist, numerical analyst and methodologist, plus selected extensions | verify | 2 | 1 |
  | `high` | the five defaults plus selected extensions, at most 7 | verify | 3 | 2 |
  | `xhigh` | as `high` | verify | 4 | 3 |
  | `max` | all available, at most 7 | debate, 3 rebuttal rounds | 4 | (defender) |

  Explicit options override single parameters. Rebuttal rounds of 1 or more at a verify level select the debate protocol, recorded as the override `protocol`.
- **Agent estimate.** With P perspectives, K review parts and B batches, the finders make P x K invocations. Each batch adds at most one merge moderator (none when every cluster holds one candidate) and, in the verify protocol, its V verifiers; in a debate, (P + 1) members per round over R + 1 rounds and one notes moderator. `panel.py panel` records the fewest and the most agents as `estimate` (`P x K` and `P x K + B x (1 + V)`, or `P x K + B x (2 + (P + 1)(R + 1))` in a debate). Above 40 agents at most, the skill states the estimate and asks before any reviewer runs.
- Review parts hold at most 2,000 lines, unless a single indivisible definition is larger. No file is excluded for the size of the scope. Above 6,000 lines (the large-scope threshold), the review states its size and asks for confirmation before any reviewer runs.

## 7. Clustering and batching

**Clustering.** Two candidates belong to the same location cluster when they are in the same file and their line ranges are within three lines of each other: candidate B joins the cluster of candidate A when `B.line_start <= max_end + 3`, where `max_end` is the largest `line_end` in A's cluster. Candidates in different files never cluster. Within each file, candidates are taken in order of `(line_start, line_end, id)`. Files are taken in lexicographic order, and clusters are numbered `C1`, `C2`, ... in that order; the suggested merged finding identifier of cluster `Cn` is `Fn`. When the moderator splits a cluster, each additional finding takes the next identifier of its batch's reserved range: batch b reserves `F(1000 b + 1)` onward (`F1001`, `F1002`, ... for batch 1, `F2001`, ... for batch 2), so that moderators of different batches never assign the same identifier.

**Batching.** Clusters are grouped into at most `max_batches` batches by file: all clusters of one file go to the same batch. Files are taken in order of decreasing cluster count (ties broken by file name), and each is assigned to the batch that currently holds the fewest clusters (ties broken by the lowest batch number). Empty batches are dropped, and batches are numbered from 1.

**Automatic merge.** A batch whose clusters each hold a single candidate needs no moderator: its merged finding `Fn` copies the candidate of cluster `Cn` (`members` its id, `raised_by` its raiser, the same location, dimension, severity, summary, trigger, wrong output and fix).

## 8. Debate stop rule

The debate of a batch runs round 0, then rebuttal rounds 1 to `rebuttal_rounds`. Round 0 and round 1 call every member. After each rebuttal round k (k >= 1), each member's stance on each finding (carried forward when the member was not called) is compared with its stance after round k-1.

1. **Stop.** If no stance changed in round k, the batch stops.
2. **Who is called in round k+1.** Otherwise round k+1 calls the members whose stance changed in round k, and, for every finding on which some member newly took the stance `challenge` in round k, every perspective whose current stance on that finding is `accept` (its raisers among them), so that the new objection can be answered. Every other member is settled for that round and keeps its latest position.

`panel.py debate-status --run DIR --batch B --round K` applies this rule to the recorded positions and prints `{"stopped": ..., "call": [...]}`.

An objection first raised in the final rebuttal round cannot be answered, because no round follows it; it counts as unanswered in section 5.2. Raise the number of rebuttal rounds when this matters.

## 9. Message validation

Every message conforms to its JSON Schema in `schemas/`. A message that fails validation is returned once to its author with the validator's errors; a second failure drops the message, and the report carries a notice naming the role.

## 10. Written fallback rules

When `python3` is absent, perform each `panel.py` step by hand, in the conversation, as follows, and add the notice "python3 was not available; the deterministic steps were performed by hand from the written rules of protocol.md." to the report.

- **init**: use a directory under the system temporary directory, never inside the project, as `$RUN`.
- **scope**: for branch mode, find the default branch (`git symbolic-ref --quiet --short refs/remotes/origin/HEAD`, else the first of `origin/main`, `origin/master`, `main`, `master` that exists), take `git merge-base <default> HEAD` as the base, and list the files of `git diff --name-only <base>` plus untracked files from `git ls-files --others --exclude-standard`. If no base can be determined, ask the user. Exclude `node_modules/`, `dist/`, lock files and files marked `linguist-generated` or `linguist-vendored`, recording each with its reason. For repository mode, list `git ls-files`; for paths mode, list the tracked files under the named paths. Exclude binary files and, in branch mode, deleted files. A file the user named in paths mode is kept even when it is generated or vendored. Notebooks (`.ipynb`) are reviewed as Python code. No file is excluded for the size of the scope. Count the lines of the kept files, the changed lines of each in branch mode and all its lines otherwise; the scope note reads "<description>: <n> files, <lines> lines."
- **scope, target**: resolve the target text token by token, without checking anything out. A whole number, `#<n>` or a GitHub pull request URL is a GitHub pull request; `!<n>`, a `/-/merge_requests/<n>` URL, or a number when the `origin` remote is a GitLab host, is a GitLab merge request. A local or remote branch name is a branch. Existing paths inside the project are paths mode; several tokens must all be paths. A token that matches more than one kind is not resolved: ask the user. A path outside the project, or a token that names nothing, is a usage error. A token such as `hig` (the first three letters of a level, but not a level) that is neither a branch nor a path is a usage error naming the levels. For a branch that is not checked out, the scope is the diff from `git merge-base <default> <branch>` to the branch, and its files are read with `git show <branch>:<path>`. For a pull request, read its base with `gh pr view <n> --json baseRefOid,headRefOid` (or `glab mr view <n> -F json`), fetch its head with `git fetch <remote> pull/<n>/head:refs/sci-review/pr-<n>` (GitLab: `merge-requests/<n>/head`), where `<remote>` is the remote of the repository named by the request's URL (the `url` or `web_url` the client reports; that repository's https URL when no remote matches), check that the fetched head is the `headRefOid` (GitLab: `sha`) the client reported, and take the diff from the merge base of the base and that ref; when `gh` or `glab` is absent or not authenticated, say what is missing and offer a branch or paths review.
- **args**: take the level word (`low`, `medium`, `high`, `xhigh`, `max`, in any position, once), `--comment`, `--fix` and `--max-findings <n>|all|default` (the last one wins; any other value is ignored with a note) from the arguments; any other `--flag`, a second level or `ultra` is a usage error. In a written request (a host without an argument field), several distinct level words are ordinary words: take no level from them, and no target. The remaining tokens are the target. Without a level, use the level the user last typed if it is known, else `medium`.
- **parts**: group the scoped files by directory, in path order; fill parts of at most 2,000 lines, keeping a directory's files together where they fit; cut a larger file at top-level definition boundaries (`def`, `class`, `export`, `function`, notebook cells), else into windows of 2,000 lines. Number the parts `p1`, `p2`, ... in path order. Confirmation is required above 6,000 lines.
- **select-extensions**: for each extension declaration, mark it `failed` if a required field is missing or `contract_version` is not 1; otherwise `selected` if any scoped file matches a glob or file type (case-insensitively) or is in a listed language and matches an import pattern; otherwise `not-applicable`. A selected extension whose perspective id is already in the panel is `failed`. Then, if the known extension `building-energy-sci-review-extension` (plugin idfkit) was not discovered, mark it `recommended`, with the reason "not installed; it would apply to <first matching file>. Install it with idfkit@idfkit." and the note that it would add a building physicist (heat transfer, psychrometrics, energy balances, IP and SI conversions, simulation time conventions) and idfkit model checks, if any scoped file matches its applicability (globs `**/*.idf`, `**/*.epJSON`, `**/*.epw`, `**/eplusout*`; file types `.idf`, `.epjson`, `.epw`; or a Python or TypeScript file that imports `idfkit`).
- **panel**: apply the level of section 6, then the limits of section 6; assign focus dimensions as in section 1 (each default perspective its primary dimension, an uncovered dimension to the nearest perspective on the panel: physical modelling to the theorist, algorithmic correctness to the numerical analyst at `medium`); state the agent estimate.
- **validate**: check each message by eye against its schema: every required field present, no unknown field, enumerations respected, `line_end >= line_start`.
- **merge** and **auto-merge**: apply section 7.
- **debate-status**: apply section 8.
- **adjudicate**: apply section 5.1 or 5.2 to every merged finding.
- **report**: state the effort level and whether it was given, reused or defaulted, the protocol, the number of review parts (a part is incomplete when a perspective's candidates file for it is missing or invalid, and its files are then listed as not reviewed), and the finding cap with the number of findings it withheld (deliver the first findings in report order up to the cap). Write the report in the eight sections of the report contract: Scope, Panel, Extensions, Findings (ordered consensus, majority, contested, and within each high, medium, low), Rejected findings, Checked and found correct, Not reviewed, Notices. When the scope holds no file, stop after the Extensions section with the sentence "No reviewable scientific code changed in this scope." When any scoped file is in a language other than Python and TypeScript, add the notice "Files in languages other than Python and TypeScript were reviewed without worked examples: <suffixes>." listing the distinct suffixes (or file names without a suffix) in sorted order.
- **clean**: delete `$RUN` and every git ref under `refs/sci-review/`.

## 11. Domain extensions

A domain extension is a skill, named `<domain>-sci-review-extension`, that any installed plugin can ship; its contract is in `extensions.md`. At the start of a review the orchestrator discovers extensions in the host's skill listing and passes each declaration to `panel.py select-extensions`, which marks it `selected`, `not-applicable` or `failed` (with the reason), and adds known but uninstalled extensions that would apply as `recommended`. A selected extension contributes one domain perspective, which takes part in the independent round (and in a debate) on the same terms as the default perspectives, reviews under every dimension, receives its reference documents in addition to the dimension documents, counts toward the panel limit of seven (and toward the majority denominator of a debate), and, when the extension declares domain checks, runs them during the independent round and reports their failures as candidate findings. Two selected extensions that claim the same file both join the panel.

## 12. Procedure for the file-based runners

The `codex-subagents`, `claude-agents` and `sequential` runners follow this procedure. Each runner file says only how it starts a **task** (one agent, one subagent, or one role played in turn in the conversation), how many tasks may run at once, and when it falls back. The `claude-workflow` runner performs the same phases inside its script.

### 12.1 Notation

| Symbol | Meaning |
|--------|---------|
| `$SKILL` | Absolute path of the skill directory, the directory that holds `SKILL.md`. |
| `$PANEL` | `python3 "$SKILL/../../scripts/panel.py"` (on Claude, `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/panel.py"`). Write the command out in full, with the absolute path, in every shell command: never store it in a shell variable, because zsh does not split a variable into words and the shell is not kept between commands. |
| `$RUN`, `$PROJECT` | The run directory printed by `panel.py init`, and the `project` field of `$RUN/run.json`. |
| `$SCHEMAS` | `$SKILL/schemas`; the schema of a message named `<name>` is `$SCHEMAS/<name>.schema.json`. |
| Perspectives | The entries of `panel.perspectives` in `$RUN/panel.json`, in order, each with `id`, `name`, `brief_path`, `reference_paths` and `dimensions` (empty means all five). |
| Briefs | Verifier `$SKILL/roles/verifier.md`, defender `$SKILL/roles/defender.md`, moderator `$SKILL/roles/moderator.md`. |
| P, V, R | `panel.protocol`, `panel.verifiers` and `panel.rebuttal_rounds` of `$RUN/panel.json`. |

Every path placed in a task is expanded to an absolute path first.

### 12.2 Rules

1. A task's message holds only the inputs listed for its phase in section 12.3 (those of section 3), the absolute path of the schema and of the output file, and the instruction to write that file and nothing else. The orchestrator never summarises, quotes or paraphrases one task's output in another task's message.
2. No task creates, modifies or deletes a file outside `$RUN`, or any file of `$PROJECT`. Git is used for read-only commands only.
3. Validate each output with `$PANEL validate --schema <name> <file>`. When validation fails or the file is missing, return it once to its author with the validator's errors ("Your output file <path> failed validation against <schema> with these errors: <errors>. Correct the file and write it again to the same path. Change nothing else."). After a second failure delete the file and run `$PANEL notice --run $RUN "The output of <role> was dropped after failing validation twice."`, naming the role and message (for example `theorist candidates (part p1)`, `moderator merge (batch 1)`, `v2 verification (batch 1)`).
4. A dropped candidates file removes that perspective's candidates from the merge. A dropped merge ruling removes its batch from the judgement. A dropped verification leaves its batch with fewer verdicts. A dropped position file leaves the member's earlier stances in force; a dropped notes file leaves the batch's findings without notes.
5. Record the project state before the first task: `git -C "$PROJECT" status --porcelain --ignored` for a git repository, otherwise the modification time of `$RUN/run.json`.

### 12.3 Task message

```text
sci-review panel task: <role> (<phase>)

Role brief: <absolute path>. Read it first and adopt it for the whole task.
Task: <phase instruction>
Inputs (read only these, and the files of the reviewed project):
- <absolute path>
Reviewed project (read only): <$PROJECT>
Output schema: <$SCHEMAS/<name>.schema.json>
Output file: <absolute path inside $RUN>

Write exactly one file, the output file, as one JSON object conforming to the output schema. Do not create, modify or delete any other file, and never modify a file of the reviewed project. Reply with the output path and one sentence summarising its content.
```

| Phase | One task per | Role brief | Task | Inputs | Schema, output |
|-------|--------------|------------|------|--------|----------------|
| Independent | perspective `p` and part `q` | `p.brief_path` | `Review part <q.id>. Your focus dimensions: <p.dimensions, or all five>. Review every line of the part; raise findings only on its lines. Set part to <q.id>; number findings <p.id>-<q.id>-<n> when parts.json holds several parts, else <p.id>-<n>.` | the dimension documents of the focus; `p.reference_paths`; `$RUN/scope.json`; `$RUN/parts.json` | `candidate-findings`, `$RUN/candidates/<p.id>--<q.id>.json` |
| Merge | batch `b` listed under `moderator` by `auto-merge` | moderator | `Perform the merge task for batch <b> only; number split findings from the next_finding_id of batch <b>.` | the candidate files; `$RUN/clusters.json` | `merge-ruling`, `$RUN/merge/batch-<b>.json` |
| Verify | batch `b` and verifier `v1` .. `vV` | verifier | `Give your verdict on every merged finding of batch <b>. Your verifier id is <v>.` | `$RUN/merge/batch-<b>.json` | `verification`, `$RUN/verify/batch-<b>/<v>.json` |
| Debate round 0 | member `m` of batch `b` | `p.brief_path`, or defender | `State your round 0 position on every merged finding of batch <b>.` | `$RUN/merge/batch-<b>.json`; for a perspective, its `$RUN/candidates/<m>--*.json` | `debate-positions`, `$RUN/debate/batch-<b>/round-0/<m>.json` |
| Debate round k >= 1 | member `m` called in round k | as round 0 | `State your round <k> position on every merged finding of batch <b>, answering the earlier positions.` | `$RUN/merge/batch-<b>.json`; every `$RUN/debate/batch-<b>/round-<j>/*.json`, j < k | `debate-positions`, `$RUN/debate/batch-<b>/round-<k>/<m>.json` |
| Notes | batch `b` | moderator | `Perform the notes task for every merged finding of batch <b>.` | `$RUN/merge/batch-<b>.json`; every `$RUN/debate/batch-<b>/round-*/*.json` | `moderator-notes`, `$RUN/notes/batch-<b>.json` |

### 12.4 Steps

Tasks of one step that the table lists as independent run concurrently where the runner allows it; a step starts when the previous one has finished.

1. **Independent round.** One task per perspective and part. Validate each candidates file. Write no part status: `panel.py report` derives it.
2. **Merge.** Run `$PANEL merge --run $RUN > $RUN/clusters.json`. When its `batches` is empty, go to step 5. Run `$PANEL auto-merge --run $RUN`; it writes the rulings of the batches it lists under `written` and prints under `moderator` the batches that need the merge task. Start one merge task per listed batch and validate each ruling.
3. **Judgement, verify protocol.** For every batch with a valid ruling, start V verify tasks (`v1` to `vV`), all batches at once. Validate each verification.
4. **Judgement, debate protocol.** For every batch with a valid ruling: round 0 calls every perspective and the defender; when R >= 1, round 1 calls every member; after each round k >= 1, run `$PANEL debate-status --run $RUN --batch <b> --round <k>` and, while it is not `stopped` and k < R, call the members it lists in `call` for round k + 1. When a batch's debate ends, start its notes task. Batches advance independently.
5. **Project check.** Compare the project state with the record of rule 12.2.5 (`find "$PROJECT" -type f -newer "$RUN/run.json" -not -path '*/.git/*'` outside git). When any path changed, run `$PANEL notice --run $RUN "The reviewed project changed during the review: <paths>."` and tell the user. Do not revert anything.
6. Return to the closing steps of `SKILL.md`.
