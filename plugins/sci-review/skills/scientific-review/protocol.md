# Panel protocol

This document is the single source of the review protocol. Every runner (Claude Workflow, Codex subagents, Claude agents, sequential) follows it, and `scripts/panel.py` implements its deterministic steps. The Workflow script embeds this file verbatim.

## 1. Roles

- **Perspective reviewers**: the five defaults (`theorist`, `numerical-analyst`, `experimentalist`, `methodologist`, `computer-scientist`) and any selected domain perspective contributed by an extension. Each reviews every review part of the scope across all five dimensions from its own perspective.
- **Defender**: argues that each finding is not a defect. Always present. Never raises findings and never withdraws.
- **Moderator**: merges duplicate candidates, then writes notes on each finding after its debate. Always present. Never introduces findings and never assigns labels.

## 2. Phases

The review proceeds in three phases (FR-023).

1. **Independent round.** `panel.py parts` divides the scope into review parts of at most 2,000 lines (section 6). Each perspective reviewer reviews every part, one part per task, without access to any other reviewer's output, and writes one candidate-findings message per part, `candidates/<perspective>--<part>.json`, whose `part` field names the part. A reviewer may read any file of the project, inside or outside the scope, to follow a reference (for example a unit defined in one file and used in another), but raises findings only on lines of its part. In a review of several parts, it numbers its findings `<perspective>-<part>-<n>` (for example `theorist-p2-1`), so that ids are unique across parts; in a review of one part, `<perspective>-<n>`.
2. **Debate.** `panel.py merge` clusters the candidates of every part by location, so that a defect raised in several parts is debated and reported once, and groups the clusters into debate batches. For each batch, the moderator confirms or splits each cluster (merge ruling). The perspectives and the defender then state positions on every merged finding of the batch in round 0, followed by at most `rebuttal_rounds` rebuttal rounds. When the debate of a batch ends, the moderator writes notes on every finding of the batch.
3. **Adjudication.** The moderator's notes have been written; `panel.py adjudicate` then computes each finding's label, or rejects it, from the recorded positions by the rules of section 5, and attaches the notes. No model takes part in this step.

## 3. Role inputs

Each role receives exactly the inputs below and nothing else (SC-011). Besides its inputs, a panel member may read the files of the reviewed project. When `scope.json` has a `target` of kind `branch` or `pull-request`, the reviewed files are not in the working tree: read each one at the scope's `head` with `git -C <project> show <head>:<path>`.

| Phase | Role | Receives | Must not receive |
|-------|------|----------|------------------|
| Independent (one task per part) | perspective | its brief; `protocol.md`; the five dimension documents (loaded on demand); extension reference material if it is a domain perspective; `scope.json`; its review part (the part's files and line ranges in `parts.json`); output path `candidates/<perspective>--<part>.json` | any other perspective's output |
| Merge | moderator | its brief; all `candidates/*.json`, of every part; the clusters from `panel.py merge` | none |
| Debate round 0 | each perspective and defender | its brief; the batch's merged findings; its own independent output (its candidate files of every part) | other members' round 0 positions |
| Debate round k > 0 | each perspective and defender | its brief; the batch's merged findings; all positions from rounds 0 to k-1 | positions from round k |
| Moderator notes | moderator | its brief; the batch's merged findings; all positions of the batch | labels (they are computed afterwards) |

## 4. Severity

Each finding carries one of three severities (FR-018):

- **High**: produces a wrong result under realistic inputs.
- **Medium**: produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result.
- **Low**: a latent risk that does not currently produce a wrong result.

A merged finding takes the highest severity among its members unless the moderator records a `severity_reason` for a lower one.

## 5. Stances and adjudication

**Stance.** A member's stance on a finding is its latest position on that finding. A member that is not called in a later round (because section 8 did not call it, or the batch stopped early) keeps its latest position. A raiser that recorded no position is taken to accept the finding it raised.

**Position identifiers.** A position is identified as `<member>:<finding_id>:<round>`, for example `defender:F3:0`. The `answers` field of a position lists the identifiers of the positions it responds to.

**Answered objection.** A defender objection is a defender position with stance `challenge`. It is answered when a later position by any perspective reviewer lists it in `answers` and the defender does not challenge again in a subsequent round. A defender objection is therefore unanswered when the defender's latest stance on the finding is `challenge` and either no perspective position has answered any earlier defender position on the finding, or the defender challenged again in a round after the latest such answer. A challenge the defender repeats in the same round as the answer does not reopen the objection, because the defender had not yet seen the answer.

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

## 6. Limits

- Panel size 2 to 7 perspectives, counting domain perspectives; a request for more than are available yields all of them.
- Rebuttal rounds 0 to 3, default 2. Round 0 (initial positions) always runs; rounds 1 to `rebuttal_rounds` follow.
- max_batches 1 to 4, default 2.
- Out-of-range values are clamped, and the report states the panel actually used.
- Effort levels set the panel size, the rebuttal rounds and the debate batches together: `low` (theorist, numerical analyst, methodologist; 1 round; 1 batch), `medium` (the five defaults plus selected extensions; 2; 2), `high` (2; 3), `xhigh` (3; 4) and `max` (all available, at most seven; 3; 4). Explicit options override single parameters.
- Review parts hold at most 2,000 lines, unless a single indivisible definition is larger. No file is excluded for the size of the scope. Above 6,000 lines (the large-scope threshold), the review states its size and asks for confirmation before any reviewer runs.
- With P perspectives and K review parts, the independent round makes P x K reviewer invocations instead of P; the merge, the debate and the notes run on merged findings and do not grow with K.

## 7. Clustering and batching

**Clustering.** Two candidates belong to the same location cluster when they are in the same file and their line ranges are within three lines of each other: candidate B joins the cluster of candidate A when `B.line_start <= max_end + 3`, where `max_end` is the largest `line_end` in A's cluster. Candidates in different files never cluster. Within each file, candidates are taken in order of `(line_start, line_end, id)`. Files are taken in lexicographic order, and clusters are numbered `C1`, `C2`, ... in that order; the suggested merged finding identifier of cluster `Cn` is `Fn`. When the moderator splits a cluster, each additional finding takes the next identifier of its batch's reserved range: batch b reserves `F(1000 b + 1)` onward (`F1001`, `F1002`, ... for batch 1, `F2001`, ... for batch 2), so that moderators of different batches never assign the same identifier.

**Batching.** Clusters are grouped into at most `max_batches` debate batches by file: all clusters of one file go to the same batch. Files are taken in order of decreasing cluster count (ties broken by file name), and each is assigned to the batch that currently holds the fewest clusters (ties broken by the lowest batch number). Empty batches are dropped, and batches are numbered from 1.

## 8. Debate stop rule

The debate of a batch runs round 0, then rebuttal rounds 1 to `rebuttal_rounds`. Round 0 and round 1 call every member. After each rebuttal round k (k >= 1), each member's stance on each finding (carried forward when the member was not called) is compared with its stance after round k-1.

1. **Stop.** If no stance changed in round k, the batch stops.
2. **Who is called in round k+1.** Otherwise round k+1 calls the members whose stance changed in round k, and, for every finding on which some member newly took the stance `challenge` in round k, every perspective whose current stance on that finding is `accept` (its raisers among them), so that the new objection can be answered. Every other member is settled for that round and keeps its latest position.

`panel.py debate-status --run DIR --batch B --round K` applies this rule to the recorded positions and prints `{"stopped": ..., "call": [...]}`.

An objection first raised in the final rebuttal round cannot be answered, because no round follows it; it counts as unanswered in section 5. Raise the number of rebuttal rounds when this matters.

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
- **panel**: apply the level of section 6, then the limits of section 6.
- **validate**: check each message by eye against its schema: every required field present, no unknown field, enumerations respected, `line_end >= line_start`.
- **merge**: apply section 7.
- **debate-status**: apply section 8.
- **adjudicate**: apply section 5 to every merged finding.
- **report**: state the effort level and whether it was given, reused or defaulted, the number of review parts (a part is incomplete when a perspective's candidates file for it is missing or invalid, and its files are then listed as not reviewed), and the finding cap with the number of findings it withheld (deliver the first findings in report order up to the cap). Write the report in the eight sections of the report contract: Scope, Panel, Extensions, Findings (ordered consensus, majority, contested, and within each high, medium, low), Rejected findings, Checked and found correct, Not reviewed, Notices. When the scope holds no file, stop after the Extensions section with the sentence "No reviewable scientific code changed in this scope." When any scoped file is in a language other than Python or TypeScript, add the notice "Files in languages other than Python and TypeScript were reviewed without worked examples: <suffixes>." listing the distinct suffixes (or file names without a suffix) in sorted order.
- **clean**: delete `$RUN` and every git ref under `refs/sci-review/`.

## 11. Domain extensions

A domain extension is a skill, named `<domain>-sci-review-extension`, that any installed plugin can ship; its contract is in `extensions.md`. At the start of a review the orchestrator discovers extensions in the host's skill listing and passes each declaration to `panel.py select-extensions`, which marks it `selected`, `not-applicable` or `failed` (with the reason), and adds known but uninstalled extensions that would apply as `recommended`. A selected extension contributes one domain perspective, which takes part in the independent round and the debate on the same terms as the default perspectives, receives its reference documents in addition to the dimension documents, counts toward the panel limit of seven and toward the majority denominator, and, when the extension declares domain checks, runs them during the independent round and reports their failures as candidate findings. Two selected extensions that claim the same file both join the panel.
