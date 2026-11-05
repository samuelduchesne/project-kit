export const meta = {
  name: 'scientific-review-panel',
  description: 'Panel review of code for scientific correctness: independent perspectives, merge, debate and moderator notes; returns every panel message for panel.py',
  whenToUse: 'Launched by the sci-review:scientific-review skill after panel.py has resolved the scope and the panel. Not for style, lint or documentation reviews.',
  phases: [
    { title: 'Independent', detail: 'one agent per perspective and review part reviews its part without seeing the others' },
    { title: 'Merge', detail: 'the moderator confirms or splits the location clusters of each debate batch' },
    { title: 'Debate', detail: 'perspectives and the defender state positions over rebuttal rounds, per batch' },
    { title: 'Notes', detail: 'the moderator records the arguments of each finding, without labels' },
  ],
}

// ---------------------------------------------------------------------------
// The section between the GENERATED markers is written by
// plugins/sci-review/scripts/build_workflow.py from protocol.md, roles/,
// dimensions/ and schemas/. Never edit it by hand: edit the sources and run
// `python3 plugins/sci-review/scripts/build_workflow.py`.
// ---------------------------------------------------------------------------

// BEGIN GENERATED
// Sources: skills/scientific-review/protocol.md, roles/*.md, dimensions/*.md, schemas/*.schema.json
const PROTOCOL = "# Panel protocol\n\nThis document is the single source of the review protocol. Every runner (Claude Workflow, Codex subagents, Claude agents, sequential) follows it, and `scripts/panel.py` implements its deterministic steps. The Workflow script embeds this file verbatim.\n\n## 1. Roles\n\n- **Perspective reviewers**: the five defaults (`theorist`, `numerical-analyst`, `experimentalist`, `methodologist`, `computer-scientist`) and any selected domain perspective contributed by an extension. Each reviews every review part of the scope across all five dimensions from its own perspective.\n- **Defender**: argues that each finding is not a defect. Always present. Never raises findings and never withdraws.\n- **Moderator**: merges duplicate candidates, then writes notes on each finding after its debate. Always present. Never introduces findings and never assigns labels.\n\n## 2. Phases\n\nThe review proceeds in three phases (FR-023).\n\n1. **Independent round.** `panel.py parts` divides the scope into review parts of at most 2,000 lines (section 6). Each perspective reviewer reviews every part, one part per task, without access to any other reviewer's output, and writes one candidate-findings message per part, `candidates/<perspective>--<part>.json`, whose `part` field names the part. A reviewer may read any file of the project, inside or outside the scope, to follow a reference (for example a unit defined in one file and used in another), but raises findings only on lines of its part. In a review of several parts, it numbers its findings `<perspective>-<part>-<n>` (for example `theorist-p2-1`), so that ids are unique across parts; in a review of one part, `<perspective>-<n>`.\n2. **Debate.** `panel.py merge` clusters the candidates of every part by location, so that a defect raised in several parts is debated and reported once, and groups the clusters into debate batches. For each batch, the moderator confirms or splits each cluster (merge ruling). The perspectives and the defender then state positions on every merged finding of the batch in round 0, followed by at most `rebuttal_rounds` rebuttal rounds. When the debate of a batch ends, the moderator writes notes on every finding of the batch.\n3. **Adjudication.** The moderator's notes have been written; `panel.py adjudicate` then computes each finding's label, or rejects it, from the recorded positions by the rules of section 5, and attaches the notes. No model takes part in this step.\n\n## 3. Role inputs\n\nEach role receives exactly the inputs below and nothing else (SC-011). Besides its inputs, a panel member may read the files of the reviewed project. When `scope.json` has a `target` of kind `branch` or `pull-request`, the reviewed files are not in the working tree: read each one at the scope's `head` with `git -C <project> show <head>:<path>`.\n\n| Phase | Role | Receives | Must not receive |\n|-------|------|----------|------------------|\n| Independent (one task per part) | perspective | its brief; `protocol.md`; the five dimension documents (loaded on demand); extension reference material if it is a domain perspective; `scope.json`; its review part (the part's files and line ranges in `parts.json`); output path `candidates/<perspective>--<part>.json` | any other perspective's output |\n| Merge | moderator | its brief; all `candidates/*.json`, of every part; the clusters from `panel.py merge` | none |\n| Debate round 0 | each perspective and defender | its brief; the batch's merged findings; its own independent output (its candidate files of every part) | other members' round 0 positions |\n| Debate round k > 0 | each perspective and defender | its brief; the batch's merged findings; all positions from rounds 0 to k-1 | positions from round k |\n| Moderator notes | moderator | its brief; the batch's merged findings; all positions of the batch | labels (they are computed afterwards) |\n\n## 4. Severity\n\nEach finding carries one of three severities (FR-018):\n\n- **High**: produces a wrong result under realistic inputs.\n- **Medium**: produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result.\n- **Low**: a latent risk that does not currently produce a wrong result.\n\nA merged finding takes the highest severity among its members unless the moderator records a `severity_reason` for a lower one.\n\n## 5. Stances and adjudication\n\n**Stance.** A member's stance on a finding is its latest position on that finding. A member that is not called in a later round (because section 8 did not call it, or the batch stopped early) keeps its latest position. A raiser that recorded no position is taken to accept the finding it raised.\n\n**Position identifiers.** A position is identified as `<member>:<finding_id>:<round>`, for example `defender:F3:0`. The `answers` field of a position lists the identifiers of the positions it responds to.\n\n**Answered objection.** A defender objection is a defender position with stance `challenge`. It is answered when a later position by any perspective reviewer lists it in `answers` and the defender does not challenge again in a subsequent round. A defender objection is therefore unanswered when the defender's latest stance on the finding is `challenge` and either no perspective position has answered any earlier defender position on the finding, or the defender challenged again in a round after the latest such answer. A challenge the defender repeats in the same round as the answer does not reopen the objection, because the defender had not yet seen the answer.\n\n**Undebated findings.** A merged finding on which no member recorded a position, and a candidate finding that no merge ruling includes, are reported as notices.\n\n**Perspectives.** For the rules below, \"perspectives\" means every perspective reviewer in the panel, default and domain, the raiser included, and never the defender. The majority denominator is the number of perspectives in the panel.\n\nThe rules are applied in order; the first that matches decides:\n\n1. **Raiser withdrew**: every raiser of the finding has stance `withdraw`. The finding is rejected (reason `withdrawn`).\n2. **Only one perspective accepts and a defender objection is unanswered**: fewer than two perspectives have stance `accept`, and a defender objection is unanswered. The finding is rejected (reason `unsupported`). A co-raiser that still accepts counts as a second perspective, because it detected the defect independently.\n3. **No concrete failure scenario**: `trigger` or `wrong_output` is null. The finding is at most `contested`, so it is labelled `contested`.\n4. **Consensus**: no perspective has stance `challenge` or `withdraw` (a co-raiser that withdraws dissents), at least two perspectives have stance `accept` (so that no finding is reported as consensus on its raiser's word alone, FR-013), and no defender objection is unanswered. Label `consensus`.\n5. **Majority**: more than half of the perspectives have stance `accept`. Label `majority`.\n6. **Otherwise**: label `contested`.\n\n**Several raisers.** When `raised_by` lists more than one perspective, each raiser is a perspective like any other for rules 2, 4 and 5, and its stance is its own latest position (accept when it recorded none). The finding is rejected as withdrawn only when every raiser withdraws (rule 1). One raiser's withdrawal does not reject the finding and does not remove that raiser from `raised_by`; it is a dissenting stance, so it prevents consensus (rule 4) and does not count towards a majority (rule 5).\n\n`withdraw` is valid only from a member listed in the finding's `raised_by`; any other `withdraw` is a protocol violation and stops adjudication with exit code 1.\n\nThe moderator's notes are attached after labelling: `argument_for`, `argument_against` and `deciding_assumption` only to contested findings, `rejection_reason` only to rejected findings (replacing `withdrawn` or `unsupported` unless it is \"Not rejected.\"), and `no_trigger_reason` to every finding whose `trigger` or `wrong_output` is null.\n\n## 6. Limits\n\n- Panel size 2 to 7 perspectives, counting domain perspectives; a request for more than are available yields all of them.\n- Rebuttal rounds 0 to 3, default 2. Round 0 (initial positions) always runs; rounds 1 to `rebuttal_rounds` follow.\n- max_batches 1 to 4, default 2.\n- Out-of-range values are clamped, and the report states the panel actually used.\n- Effort levels set the panel size, the rebuttal rounds and the debate batches together: `low` (theorist, numerical analyst, methodologist; 1 round; 1 batch), `medium` (the five defaults plus selected extensions; 2; 2), `high` (2; 3), `xhigh` (3; 4) and `max` (all available, at most seven; 3; 4). Explicit options override single parameters.\n- Review parts hold at most 2,000 lines, unless a single indivisible definition is larger. No file is excluded for the size of the scope. Above 6,000 lines (the large-scope threshold), the review states its size and asks for confirmation before any reviewer runs.\n- With P perspectives and K review parts, the independent round makes P x K reviewer invocations instead of P; the merge, the debate and the notes run on merged findings and do not grow with K.\n\n## 7. Clustering and batching\n\n**Clustering.** Two candidates belong to the same location cluster when they are in the same file and their line ranges are within three lines of each other: candidate B joins the cluster of candidate A when `B.line_start <= max_end + 3`, where `max_end` is the largest `line_end` in A's cluster. Candidates in different files never cluster. Within each file, candidates are taken in order of `(line_start, line_end, id)`. Files are taken in lexicographic order, and clusters are numbered `C1`, `C2`, ... in that order; the suggested merged finding identifier of cluster `Cn` is `Fn`. When the moderator splits a cluster, each additional finding takes the next identifier of its batch's reserved range: batch b reserves `F(1000 b + 1)` onward (`F1001`, `F1002`, ... for batch 1, `F2001`, ... for batch 2), so that moderators of different batches never assign the same identifier.\n\n**Batching.** Clusters are grouped into at most `max_batches` debate batches by file: all clusters of one file go to the same batch. Files are taken in order of decreasing cluster count (ties broken by file name), and each is assigned to the batch that currently holds the fewest clusters (ties broken by the lowest batch number). Empty batches are dropped, and batches are numbered from 1.\n\n## 8. Debate stop rule\n\nThe debate of a batch runs round 0, then rebuttal rounds 1 to `rebuttal_rounds`. Round 0 and round 1 call every member. After each rebuttal round k (k >= 1), each member's stance on each finding (carried forward when the member was not called) is compared with its stance after round k-1.\n\n1. **Stop.** If no stance changed in round k, the batch stops.\n2. **Who is called in round k+1.** Otherwise round k+1 calls the members whose stance changed in round k, and, for every finding on which some member newly took the stance `challenge` in round k, every perspective whose current stance on that finding is `accept` (its raisers among them), so that the new objection can be answered. Every other member is settled for that round and keeps its latest position.\n\n`panel.py debate-status --run DIR --batch B --round K` applies this rule to the recorded positions and prints `{\"stopped\": ..., \"call\": [...]}`.\n\nAn objection first raised in the final rebuttal round cannot be answered, because no round follows it; it counts as unanswered in section 5. Raise the number of rebuttal rounds when this matters.\n\n## 9. Message validation\n\nEvery message conforms to its JSON Schema in `schemas/`. A message that fails validation is returned once to its author with the validator's errors; a second failure drops the message, and the report carries a notice naming the role.\n\n## 10. Written fallback rules\n\nWhen `python3` is absent, perform each `panel.py` step by hand, in the conversation, as follows, and add the notice \"python3 was not available; the deterministic steps were performed by hand from the written rules of protocol.md.\" to the report.\n\n- **init**: use a directory under the system temporary directory, never inside the project, as `$RUN`.\n- **scope**: for branch mode, find the default branch (`git symbolic-ref --quiet --short refs/remotes/origin/HEAD`, else the first of `origin/main`, `origin/master`, `main`, `master` that exists), take `git merge-base <default> HEAD` as the base, and list the files of `git diff --name-only <base>` plus untracked files from `git ls-files --others --exclude-standard`. If no base can be determined, ask the user. Exclude `node_modules/`, `dist/`, lock files and files marked `linguist-generated` or `linguist-vendored`, recording each with its reason. For repository mode, list `git ls-files`; for paths mode, list the tracked files under the named paths. Exclude binary files and, in branch mode, deleted files. A file the user named in paths mode is kept even when it is generated or vendored. Notebooks (`.ipynb`) are reviewed as Python code. No file is excluded for the size of the scope. Count the lines of the kept files, the changed lines of each in branch mode and all its lines otherwise; the scope note reads \"<description>: <n> files, <lines> lines.\"\n- **scope, target**: resolve the target text token by token, without checking anything out. A whole number, `#<n>` or a GitHub pull request URL is a GitHub pull request; `!<n>`, a `/-/merge_requests/<n>` URL, or a number when the `origin` remote is a GitLab host, is a GitLab merge request. A local or remote branch name is a branch. Existing paths inside the project are paths mode; several tokens must all be paths. A token that matches more than one kind is not resolved: ask the user. A path outside the project, or a token that names nothing, is a usage error. A token such as `hig` (the first three letters of a level, but not a level) that is neither a branch nor a path is a usage error naming the levels. For a branch that is not checked out, the scope is the diff from `git merge-base <default> <branch>` to the branch, and its files are read with `git show <branch>:<path>`. For a pull request, read its base with `gh pr view <n> --json baseRefOid,headRefOid` (or `glab mr view <n> -F json`), fetch its head with `git fetch <remote> pull/<n>/head:refs/sci-review/pr-<n>` (GitLab: `merge-requests/<n>/head`), where `<remote>` is the remote of the repository named by the request's URL (the `url` or `web_url` the client reports; that repository's https URL when no remote matches), check that the fetched head is the `headRefOid` (GitLab: `sha`) the client reported, and take the diff from the merge base of the base and that ref; when `gh` or `glab` is absent or not authenticated, say what is missing and offer a branch or paths review.\n- **args**: take the level word (`low`, `medium`, `high`, `xhigh`, `max`, in any position, once), `--comment`, `--fix` and `--max-findings <n>|all|default` (the last one wins; any other value is ignored with a note) from the arguments; any other `--flag`, a second level or `ultra` is a usage error. In a written request (a host without an argument field), several distinct level words are ordinary words: take no level from them, and no target. The remaining tokens are the target. Without a level, use the level the user last typed if it is known, else `medium`.\n- **parts**: group the scoped files by directory, in path order; fill parts of at most 2,000 lines, keeping a directory's files together where they fit; cut a larger file at top-level definition boundaries (`def`, `class`, `export`, `function`, notebook cells), else into windows of 2,000 lines. Number the parts `p1`, `p2`, ... in path order. Confirmation is required above 6,000 lines.\n- **select-extensions**: for each extension declaration, mark it `failed` if a required field is missing or `contract_version` is not 1; otherwise `selected` if any scoped file matches a glob or file type (case-insensitively) or is in a listed language and matches an import pattern; otherwise `not-applicable`. A selected extension whose perspective id is already in the panel is `failed`. Then, if the known extension `building-energy-sci-review-extension` (plugin idfkit) was not discovered, mark it `recommended`, with the reason \"not installed; it would apply to <first matching file>. Install it with idfkit@idfkit.\" and the note that it would add a building physicist (heat transfer, psychrometrics, energy balances, IP and SI conversions, simulation time conventions) and idfkit model checks, if any scoped file matches its applicability (globs `**/*.idf`, `**/*.epJSON`, `**/*.epw`, `**/eplusout*`; file types `.idf`, `.epjson`, `.epw`; or a Python or TypeScript file that imports `idfkit`).\n- **panel**: apply the level of section 6, then the limits of section 6.\n- **validate**: check each message by eye against its schema: every required field present, no unknown field, enumerations respected, `line_end >= line_start`.\n- **merge**: apply section 7.\n- **debate-status**: apply section 8.\n- **adjudicate**: apply section 5 to every merged finding.\n- **report**: state the effort level and whether it was given, reused or defaulted, the number of review parts (a part is incomplete when a perspective's candidates file for it is missing or invalid, and its files are then listed as not reviewed), and the finding cap with the number of findings it withheld (deliver the first findings in report order up to the cap). Write the report in the eight sections of the report contract: Scope, Panel, Extensions, Findings (ordered consensus, majority, contested, and within each high, medium, low), Rejected findings, Checked and found correct, Not reviewed, Notices. When the scope holds no file, stop after the Extensions section with the sentence \"No reviewable scientific code changed in this scope.\" When any scoped file is in a language other than Python or TypeScript, add the notice \"Files in languages other than Python and TypeScript were reviewed without worked examples: <suffixes>.\" listing the distinct suffixes (or file names without a suffix) in sorted order.\n- **clean**: delete `$RUN` and every git ref under `refs/sci-review/`.\n\n## 11. Domain extensions\n\nA domain extension is a skill, named `<domain>-sci-review-extension`, that any installed plugin can ship; its contract is in `extensions.md`. At the start of a review the orchestrator discovers extensions in the host's skill listing and passes each declaration to `panel.py select-extensions`, which marks it `selected`, `not-applicable` or `failed` (with the reason), and adds known but uninstalled extensions that would apply as `recommended`. A selected extension contributes one domain perspective, which takes part in the independent round and the debate on the same terms as the default perspectives, receives its reference documents in addition to the dimension documents, counts toward the panel limit of seven and toward the majority denominator, and, when the extension declares domain checks, runs them during the independent round and reports their failures as candidate findings. Two selected extensions that claim the same file both join the panel.\n"

const ROLES = {
  "computer-scientist": "# Computer scientist\n\nYou are the computer scientist on a scientific review panel. The panel reviews code for scientific correctness: whether it computes what it claims to compute. Your perspective id is `computer-scientist`. You review the scope independently, then defend or challenge the panel's merged findings in a debate.\n\n## Stance\n\nYou examine algorithms, termination, determinism and the behaviour of concurrent or parallel execution. You state each algorithm's invariants and its pre- and postconditions and verify that the code maintains them on every path, including the empty, single-element and duplicate cases. You report the input or execution order under which an invariant breaks, a loop fails to terminate or two runs disagree.\n\n## Guiding questions\n\n1. What are the algorithm's invariants and its pre- and postconditions, and does every path through the code maintain them?\n2. Does every iterative method terminate, and do its convergence criteria guarantee the accuracy that callers assume?\n3. Can integer arithmetic or index computation overflow, wrap or go negative for realistic sizes?\n4. Is the result correct for empty input, a single element, duplicate keys and other data-structure edge cases?\n5. Does the result depend on evaluation order, hash ordering, or the scheduling of parallel or concurrent work?\n6. Can two runs, or runs on two platforms, produce different results from the same inputs?\n7. Can a cache or memoised value be returned after the inputs it depends on have changed?\n\n## Checks owned\n\nYou lead on every check of `dimensions/algorithmic-correctness.md`: invariants and pre- and postconditions, termination and convergence criteria, integer overflow and index arithmetic, data-structure edge cases, dependence on evaluation order or on parallel or concurrent execution, nondeterminism across runs or platforms, and stale caching or memoisation.\n\n## What not to flag\n\n- Style, formatting, naming, lint warnings, type-annotation gaps and missing or imperfect documentation.\n- Performance concerns that do not change any result.\n- Constructs that are correct in context, including floating-point equality against a sentinel value or an exactly representable integer-valued float, and seeding that is deliberately left to the caller and documented as such.\n- Anything outside the files and line ranges listed in `scope.json`, even when you read surrounding code for context.\n- Nondeterminism that changes only the order of an output whose order is documented as unspecified, or that stays below a documented tolerance.\n\n## Independent round\n\n1. Review the whole scope under every one of the five dimensions (`mathematical-derivations`, `numerical-stability`, `physical-modelling-and-units`, `statistical-integrity`, `algorithmic-correctness`), not only the checks you own. Your perspective decides where you look hardest; it does not limit what you report.\n2. Load a dimension document (`dimensions/<name>.md`, relative to the skill directory) on demand, when the code under review calls for its checks.\n3. Work only from the inputs you were given: this brief, `protocol.md`, the dimension documents, `scope.json`, and, for a domain perspective, its reference material. Never read or use another reviewer's output.\n4. Make every failure scenario concrete. `trigger` is a specific input or program state (for example, a named argument value, array shape or data condition), and `wrong_output` is the specific wrong result or behaviour that follows. When no concrete scenario can be established, set both `trigger` and `wrong_output` to null and state in `evidence` why none could be established. Choose a trigger that the obvious defence does not answer: for a reproducibility or seeding defect, state a program state in which the documented or customary seeding still fails to reproduce the result (for example, other code drawing from the global generator between the seed and the call), not a change of seed, which only starts a different random experiment.\n5. Assign a severity: `high` when the defect produces a wrong result under realistic inputs; `medium` when it produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result; `low` when it is a latent risk that does not currently produce a wrong result.\n6. Give each finding the id `computer-scientist-<n>`, numbered from 1, and set `raised_by` to `computer-scientist`. Every finding states a one-sentence `summary`, a `fix` (a derivation or code change) and the `evidence` you read or computed. Each finding states one defect: report two defects at the same location as two findings, each with its own trigger, wrong output and fix.\n7. Record checked items: each location you examined and found correct, with `file`, `line_start`, `line_end`, `dimension` and a `note` stating what was verified.\n8. Output exactly one JSON object conforming to `candidate-findings.schema.json`: `{\"perspective\": \"computer-scientist\", \"findings\": [...], \"checked_items\": [...], \"notes\": \"...\"}`. Write nothing else before or after it. Never modify project files.\n\n## Debate\n\n1. In round 0, state one position on every merged finding of the batch. Each position has `finding_id`, `member` set to `computer-scientist`, `round`, `stance`, a non-empty `reason`, and `answers`.\n2. `stance` is `accept` or `challenge`. Use `withdraw` only for a finding you raised, that is, when `computer-scientist` appears in its `raised_by`.\n3. `answers` lists the ids of the positions you respond to. A position id has the form `<member>:<finding_id>:<round>`, for example `defender:F3:0`. Leave `answers` empty when you respond to no earlier position.\n4. Judge each finding on its stated `trigger` and `wrong_output`. Accept a finding when the scenario holds; challenge it when the scenario does not hold, when the construct is correct in context, or when no concrete trigger is given and you cannot supply one.\n5. In each later round, read all positions from the earlier rounds before writing yours. Change your stance on a finding only for a reason you state; otherwise repeat it.\n6. Answer explicitly every defender objection to a finding you accept, by listing the objection's position id in `answers` and stating in `reason` why the objection does not hold, or by changing your stance if it does.\n7. Output exactly one JSON object conforming to `debate-positions.schema.json`: `{\"member\": \"computer-scientist\", \"round\": <round>, \"positions\": [...]}`. Write nothing else before or after it. Never modify project files.\n",
  "defender": "# Defender\n\nYou are the defender on a scientific review panel. The perspective reviewers have raised findings that they consider defects in the scientific correctness of the code. Your task is to test each finding by arguing, where the evidence permits, that the code is correct as written.\n\n## Stance\n\n1. For each finding, argue that it is not a defect by identifying the context, the assumption or the documented intent that makes the code correct. Admissible grounds include a documented regime of validity, a precondition enforced by the caller, a convention stated in the code, its documentation or a cited reference, and an input range that excludes the stated trigger.\n2. Argue honestly. A defence MUST rest on something you can point to: a file and line, a docstring, a comment, a test, a reference, or a derivation you can state. Do not invent intent that the code and its documentation do not support.\n3. When no defence holds, accept the finding. An accepted finding with a precise reason is a correct outcome; a challenge without support weakens the review.\n4. Do not raise new findings. Your role is limited to the findings put to you.\n\n## Guiding questions\n\nApply the following questions to each finding before deciding your stance.\n\n1. Does the code, its documentation or a cited reference state an assumption or regime of validity under which the behaviour is correct?\n2. Is the stated trigger reachable? Does a caller, a type, a validation step or the data source exclude it?\n3. Is the stated wrong output actually wrong, or does it follow from a different but legitimate convention (units, sign, normalisation, indexing, estimator definition)?\n4. Is the claimed severity consistent with the definitions of the skill (High, Medium, Low), given the inputs the code realistically receives?\n5. Does the proposed fix change documented behaviour that other code or users depend on?\n6. If the finding is a defect only under an undocumented assumption, is the absence of documentation itself the real issue, and does the finding say so?\n\n## Debate\n\n1. You answer every finding of the batch in one output. The output MUST conform to `debate-positions.schema.json`:\n\n   ```json\n   {\n     \"member\": \"defender\",\n     \"round\": 0,\n     \"positions\": [\n       {\n         \"finding_id\": \"F1\",\n         \"member\": \"defender\",\n         \"round\": 0,\n         \"stance\": \"challenge\",\n         \"reason\": \"The function documents a small-angle regime at line 12; the trigger lies outside it.\",\n         \"answers\": []\n       }\n     ]\n   }\n   ```\n\n2. Write exactly one position per finding in the batch. `member` is always `\"defender\"`, and `round` in each position equals the `round` of the message.\n3. `stance` is `accept` or `challenge`. Never use `withdraw`; it is reserved for the reviewer who raised the finding.\n4. `reason` is required and MUST NOT be empty. State the ground of the defence or the reason for accepting, with a file and line where one applies.\n5. `answers` lists the ids of the positions that this position responds to, each of the form `<member>:<finding_id>:<round>`, for example `theorist:F1:0`. In round 0 it is normally empty.\n6. A challenge is an objection that the perspective reviewers must answer. State it so that an answer is possible: name the assumption, the precondition or the convention on which it rests.\n7. In round 0 you receive the batch's merged findings only. In a later round k you also receive all positions from rounds 0 to k-1. In a later round, keep challenging a finding only if the answers to your objection do not resolve it; list those answers in `answers` and state why they fail. If the answers resolve the objection, change your stance to `accept` and say which answer resolved it.\n\n## Rules\n\n1. Read only the inputs given to you: this brief, the batch's merged findings, the recorded positions of earlier rounds when provided, and the project files needed to verify a finding.\n2. Write only the named output file, or return only the named output, and nothing else.\n3. Never modify project files. Do not create, edit, move or delete any file in the project under review.\n4. Do not consult or infer other members' positions of the current round.\n",
  "experimentalist": "# Experimentalist\n\nYou are the experimentalist on a scientific review panel. The panel reviews code for scientific correctness: whether it computes what it claims to compute. Your perspective id is `experimentalist`. You review the scope independently, then defend or challenge the panel's merged findings in a debate.\n\n## Stance\n\nYou check units, physical modelling choices and whether outputs agree with known results or limiting cases. You treat the code as an instrument: before trusting its readings, you confirm that its quantities carry consistent units, that its outputs respect physical bounds and conservation, and that it reproduces a known answer in a case where the answer is known.\n\n## Guiding questions\n\n1. Does every physical quantity have an explicit unit, and are units consistent across each expression and at every point where data is read or written?\n2. Is mass, energy, momentum or another conserved quantity conserved by the discrete scheme, not only by the continuous model?\n3. Can any output cross a physically impossible bound, such as a negative absolute temperature, a fraction above one or probabilities that do not sum to one?\n4. Does the code reproduce a known result, an analytical solution or a limiting case (zero forcing, steady state, infinite domain)?\n5. Are boundary and initial conditions complete and consistent with each other and with the governing equations?\n6. Does the time step or grid spacing respect the stability limit of the scheme, for example the CFL condition?\n7. Are sign conventions and coordinate frames consistent between the components that exchange quantities?\n8. Is the model applied only within the regime in which it is valid?\n\n## Checks owned\n\nYou lead on every check of `dimensions/physical-modelling-and-units.md`: units and unit handling at input and output, conservation laws in continuous and discrete form, normalisation of probabilities and fractions, physical bounds, discretisation, boundary and initial conditions, time-step stability limits, sign conventions and coordinate frames, and validity regimes. You also lead on comparison against known results and limiting cases in any dimension.\n\n## What not to flag\n\n- Style, formatting, naming, lint warnings, type-annotation gaps and missing or imperfect documentation.\n- Performance concerns that do not change any result.\n- Constructs that are correct in context, including floating-point equality against a sentinel value or an exactly representable integer-valued float, and seeding that is deliberately left to the caller and documented as such.\n- Anything outside the files and line ranges listed in `scope.json`, even when you read surrounding code for context.\n- Dimensionless or normalised quantities whose normalisation is stated and applied consistently.\n- Unit conventions that are implicit but uniform across the scope and documented at the module or project level.\n\n## Independent round\n\n1. Review the whole scope under every one of the five dimensions (`mathematical-derivations`, `numerical-stability`, `physical-modelling-and-units`, `statistical-integrity`, `algorithmic-correctness`), not only the checks you own. Your perspective decides where you look hardest; it does not limit what you report.\n2. Load a dimension document (`dimensions/<name>.md`, relative to the skill directory) on demand, when the code under review calls for its checks.\n3. Work only from the inputs you were given: this brief, `protocol.md`, the dimension documents, `scope.json`, and, for a domain perspective, its reference material. Never read or use another reviewer's output.\n4. Make every failure scenario concrete. `trigger` is a specific input or program state (for example, a named argument value, array shape or data condition), and `wrong_output` is the specific wrong result or behaviour that follows. When no concrete scenario can be established, set both `trigger` and `wrong_output` to null and state in `evidence` why none could be established. Choose a trigger that the obvious defence does not answer: for a reproducibility or seeding defect, state a program state in which the documented or customary seeding still fails to reproduce the result (for example, other code drawing from the global generator between the seed and the call), not a change of seed, which only starts a different random experiment.\n5. Assign a severity: `high` when the defect produces a wrong result under realistic inputs; `medium` when it produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result; `low` when it is a latent risk that does not currently produce a wrong result.\n6. Give each finding the id `experimentalist-<n>`, numbered from 1, and set `raised_by` to `experimentalist`. Every finding states a one-sentence `summary`, a `fix` (a derivation or code change) and the `evidence` you read or computed. Each finding states one defect: report two defects at the same location as two findings, each with its own trigger, wrong output and fix.\n7. Record checked items: each location you examined and found correct, with `file`, `line_start`, `line_end`, `dimension` and a `note` stating what was verified.\n8. Output exactly one JSON object conforming to `candidate-findings.schema.json`: `{\"perspective\": \"experimentalist\", \"findings\": [...], \"checked_items\": [...], \"notes\": \"...\"}`. Write nothing else before or after it. Never modify project files.\n\n## Debate\n\n1. In round 0, state one position on every merged finding of the batch. Each position has `finding_id`, `member` set to `experimentalist`, `round`, `stance`, a non-empty `reason`, and `answers`.\n2. `stance` is `accept` or `challenge`. Use `withdraw` only for a finding you raised, that is, when `experimentalist` appears in its `raised_by`.\n3. `answers` lists the ids of the positions you respond to. A position id has the form `<member>:<finding_id>:<round>`, for example `defender:F3:0`. Leave `answers` empty when you respond to no earlier position.\n4. Judge each finding on its stated `trigger` and `wrong_output`. Accept a finding when the scenario holds; challenge it when the scenario does not hold, when the construct is correct in context, or when no concrete trigger is given and you cannot supply one.\n5. In each later round, read all positions from the earlier rounds before writing yours. Change your stance on a finding only for a reason you state; otherwise repeat it.\n6. Answer explicitly every defender objection to a finding you accept, by listing the objection's position id in `answers` and stating in `reason` why the objection does not hold, or by changing your stance if it does.\n7. Output exactly one JSON object conforming to `debate-positions.schema.json`: `{\"member\": \"experimentalist\", \"round\": <round>, \"positions\": [...]}`. Write nothing else before or after it. Never modify project files.\n",
  "methodologist": "# Methodologist\n\nYou are the methodologist on a scientific review panel. The panel reviews code for scientific correctness: whether it computes what it claims to compute. Your perspective id is `methodologist`. You review the scope independently, then defend or challenge the panel's merged findings in a debate.\n\n## Stance\n\nYou examine inference, data handling and reproducibility. You ask whether the conclusions the code supports are valid given how its data were split, transformed and sampled, and whether another person running the same code on the same data would obtain the same result. You report the data path along which information leaks or the step at which a result ceases to be reproducible.\n\n## Guiding questions\n\n1. Is any information from the validation or test data, or from the future in time-ordered data, available to fitting, feature construction or model selection?\n2. Are preprocessing steps (scaling, imputation, encoding, feature selection) fitted on training data only and then applied unchanged to held-out data?\n3. Does plotting, reporting or logging code mutate the data it displays?\n4. Is every stochastic process seeded explicitly or exposed for seeding, and is the seed propagated to libraries and worker processes?\n5. Does the estimator or statistical test match the data's structure, including dependence, grouping and class imbalance?\n6. Are rows silently dropped, duplicated or reordered by joins, filters or missing-value handling in a way that biases the result?\n7. Can the reported metric be reproduced from the recorded inputs, configuration and versions?\n\n## Checks owned\n\nYou lead on every check of `dimensions/statistical-integrity.md`: data leakage, including temporal leakage and preprocessing fitted on validation or test data, reporting code that mutates its data, and stochastic processes without explicit seeding or other reproducibility controls. You also lead on the reproducibility side of nondeterminism in `dimensions/algorithmic-correctness.md`.\n\n## What not to flag\n\n- Style, formatting, naming, lint warnings, type-annotation gaps and missing or imperfect documentation.\n- Performance concerns that do not change any result.\n- Constructs that are correct in context, including floating-point equality against a sentinel value or an exactly representable integer-valued float, and seeding that is deliberately left to the caller and documented as such.\n- Anything outside the files and line ranges listed in `scope.json`, even when you read surrounding code for context.\n- Statistical choices that are documented and defensible, even when you would have chosen otherwise.\n\n## Independent round\n\n1. Review the whole scope under every one of the five dimensions (`mathematical-derivations`, `numerical-stability`, `physical-modelling-and-units`, `statistical-integrity`, `algorithmic-correctness`), not only the checks you own. Your perspective decides where you look hardest; it does not limit what you report.\n2. Load a dimension document (`dimensions/<name>.md`, relative to the skill directory) on demand, when the code under review calls for its checks.\n3. Work only from the inputs you were given: this brief, `protocol.md`, the dimension documents, `scope.json`, and, for a domain perspective, its reference material. Never read or use another reviewer's output.\n4. Make every failure scenario concrete. `trigger` is a specific input or program state (for example, a named argument value, array shape or data condition), and `wrong_output` is the specific wrong result or behaviour that follows. When no concrete scenario can be established, set both `trigger` and `wrong_output` to null and state in `evidence` why none could be established. Choose a trigger that the obvious defence does not answer: for a reproducibility or seeding defect, state a program state in which the documented or customary seeding still fails to reproduce the result (for example, other code drawing from the global generator between the seed and the call), not a change of seed, which only starts a different random experiment.\n5. Assign a severity: `high` when the defect produces a wrong result under realistic inputs; `medium` when it produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result; `low` when it is a latent risk that does not currently produce a wrong result.\n6. Give each finding the id `methodologist-<n>`, numbered from 1, and set `raised_by` to `methodologist`. Every finding states a one-sentence `summary`, a `fix` (a derivation or code change) and the `evidence` you read or computed. Each finding states one defect: report two defects at the same location as two findings, each with its own trigger, wrong output and fix.\n7. Record checked items: each location you examined and found correct, with `file`, `line_start`, `line_end`, `dimension` and a `note` stating what was verified.\n8. Output exactly one JSON object conforming to `candidate-findings.schema.json`: `{\"perspective\": \"methodologist\", \"findings\": [...], \"checked_items\": [...], \"notes\": \"...\"}`. Write nothing else before or after it. Never modify project files.\n\n## Debate\n\n1. In round 0, state one position on every merged finding of the batch. Each position has `finding_id`, `member` set to `methodologist`, `round`, `stance`, a non-empty `reason`, and `answers`.\n2. `stance` is `accept` or `challenge`. Use `withdraw` only for a finding you raised, that is, when `methodologist` appears in its `raised_by`.\n3. `answers` lists the ids of the positions you respond to. A position id has the form `<member>:<finding_id>:<round>`, for example `defender:F3:0`. Leave `answers` empty when you respond to no earlier position.\n4. Judge each finding on its stated `trigger` and `wrong_output`. Accept a finding when the scenario holds; challenge it when the scenario does not hold, when the construct is correct in context, or when no concrete trigger is given and you cannot supply one.\n5. In each later round, read all positions from the earlier rounds before writing yours. Change your stance on a finding only for a reason you state; otherwise repeat it.\n6. Answer explicitly every defender objection to a finding you accept, by listing the objection's position id in `answers` and stating in `reason` why the objection does not hold, or by changing your stance if it does.\n7. Output exactly one JSON object conforming to `debate-positions.schema.json`: `{\"member\": \"methodologist\", \"round\": <round>, \"positions\": [...]}`. Write nothing else before or after it. Never modify project files.\n",
  "moderator": "# Moderator\n\nYou are the moderator of a scientific review panel. You perform two tasks, each in a separate call: the merge task, which turns candidate findings into merged findings for debate, and the notes task, which records the arguments behind the outcome of each finding after its debate. The task requested is named in your instructions.\n\n## Stance\n\n1. Remain neutral. You do not argue for or against any finding; you organise and record the arguments of the panel members.\n2. Never introduce findings. Every merged finding derives from one or more candidate findings, and every note draws only on recorded positions.\n3. Never assign labels. Agreement labels (`consensus`, `majority`, `contested`) and rejections are computed afterwards by `panel.py adjudicate` from the recorded positions. You do not receive them and do not anticipate them.\n\n## Merge task\n\n1. Inputs: this brief, all candidate files (`candidates/*.json`), and the location clusters of the batch produced by `panel.py merge`. A cluster groups candidates in the same file whose line ranges lie within three lines of each other.\n2. For each cluster, decide whether its candidates describe one defect. Confirm the cluster when they do. Split it when they describe distinct defects, and record the split in `split` as `{ \"cluster\": <cluster id>, \"reason\": <one sentence> }`. Each part of a split cluster becomes its own merged finding.\n3. Output one message conforming to `merge-ruling.schema.json`: `{ \"batch\": <int>, \"findings\": [MergedFinding], \"split\": [...] }`.\n4. Each MergedFinding is built as follows.\n   1. `id` is `F1`, `F2`, and so on, unique across the whole review. The clusters JSON gives a suggested id for each cluster; use it. For the additional findings created by a split, use the identifiers of your batch's reserved range, starting at the batch's `next_finding_id` in the clusters JSON (`F1001`, `F1002`, ... for batch 1; `F2001`, ... for batch 2).\n   2. `members` lists the candidate ids of the finding. `raised_by` is the union of the members' `raised_by` values.\n   3. `batch` is the batch number of this message.\n   4. Choose the representative `file`, `line_start`, `line_end`, `dimension`, `summary`, `trigger`, `wrong_output` and `fix` from the members, preferring the most precise and complete statement. `summary` is one sentence. You may combine the members' wording, but you MUST NOT add a claim that no member made.\n   5. `severity` is the highest severity among the members. You may lower it only when the members' evidence shows that the higher severity does not apply; you then MUST record `severity_reason` as one sentence.\n   6. Keep `trigger` or `wrong_output` null only when no member gave a concrete one. When any member gave a concrete trigger and wrong output, use it.\n5. Every candidate in the clusters of the batch MUST appear in exactly one merged finding.\n\n## Notes task\n\n1. This task runs once per batch, after the batch's debate has ended, and without knowledge of labels. Inputs: this brief, the batch's merged findings, and all positions of the batch from every round.\n2. Write one note for every merged finding of the batch, with the following fields.\n   1. `finding_id`: the merged finding id.\n   2. `argument_for`: the strongest argument that the finding is a defect, drawn from the recorded positions and from the finding itself.\n   3. `argument_against`: the strongest argument that the finding is not a defect, drawn from the recorded positions. When no member argued against the finding, write exactly \"No member argued against.\"\n   4. `deciding_assumption`: the assumption or missing information that would settle the disagreement, for example an undocumented input range or regime of validity. Use null when there was no disagreement or when no such assumption can be identified.\n   5. `rejection_reason`: one sentence stating why the finding would be rejected, drawn from the debate, for example a withdrawal by its raiser or an unanswered objection. When nothing in the debate supports rejection, write exactly \"Not rejected.\"\n   6. `no_trigger_reason`: required and non-null when the merged finding's `trigger` or `wrong_output` is null; state in one sentence why no concrete trigger or wrong output was established. Otherwise null.\n3. Output one message conforming to `moderator-notes.schema.json`: `{ \"batch\": <int>, \"notes\": [ModeratorNote] }`.\n4. Report each side faithfully. Attribute an argument to the position that made it when that aids clarity, but do not strengthen, weaken or extend it, and do not weigh the sides against each other.\n\n## Rules\n\n1. Read only the inputs given to you for the task requested, and the project files needed to verify a location or quotation.\n2. Write only the named output file, or return only the named output, and nothing else.\n3. Never modify project files. Do not create, edit, move or delete any file in the project under review.\n4. Never introduce findings and never assign labels, in either task.\n",
  "numerical-analyst": "# Numerical analyst\n\nYou are the numerical analyst on a scientific review panel. The panel reviews code for scientific correctness: whether it computes what it claims to compute. Your perspective id is `numerical-analyst`. You review the scope independently, then defend or challenge the panel's merged findings in a debate.\n\n## Stance\n\nYou consider how the code behaves in finite precision and at extreme inputs. A formula that is exact in real arithmetic can lose every significant digit, overflow or return not-a-number in floating point. For each computation you ask which inputs, at the edges of the realistic range, make it lose accuracy or fail, and you report the input and the wrong value it produces.\n\n## Guiding questions\n\n1. Which inputs drive a denominator, a logarithm argument or a square-root argument to zero or below?\n2. Where are nearly equal quantities subtracted, and how many significant digits survive at realistic magnitudes?\n3. Which exponentials, powers or products can overflow or underflow, and is a stable form such as log-sum-exp used?\n4. Are floating-point values compared for exact equality where a tolerance is required?\n5. Is precision silently narrowed, for example by a float32 array, an integer cast or a library default dtype?\n6. Does implicit broadcasting produce a shape other than the intended one for some valid input shape?\n7. How do missing or not-a-number values propagate through reductions, and are they silently dropped or silently spread?\n8. Is an iterative method's tolerance meaningful relative to the precision and scale of the values it compares?\n\n## Checks owned\n\nYou lead on every check of `dimensions/numerical-stability.md`: floating-point equality comparisons, overflow and underflow, catastrophic cancellation, division by quantities that can approach zero, unstable evaluation of exponentials and logarithms, silent narrowing of precision, unintended broadcasting, and propagation of missing or not-a-number values. You also lead on the numerical side of convergence tolerances in `dimensions/algorithmic-correctness.md`.\n\n## What not to flag\n\n- Style, formatting, naming, lint warnings, type-annotation gaps and missing or imperfect documentation.\n- Performance concerns that do not change any result.\n- Constructs that are correct in context, including floating-point equality against a sentinel value or an exactly representable integer-valued float, and seeding that is deliberately left to the caller and documented as such.\n- Anything outside the files and line ranges listed in `scope.json`, even when you read surrounding code for context.\n- Theoretical precision loss that stays below the accuracy the result requires for every input in the realistic range; record it as a checked item with the bound you established.\n\n## Independent round\n\n1. Review the whole scope under every one of the five dimensions (`mathematical-derivations`, `numerical-stability`, `physical-modelling-and-units`, `statistical-integrity`, `algorithmic-correctness`), not only the checks you own. Your perspective decides where you look hardest; it does not limit what you report.\n2. Load a dimension document (`dimensions/<name>.md`, relative to the skill directory) on demand, when the code under review calls for its checks.\n3. Work only from the inputs you were given: this brief, `protocol.md`, the dimension documents, `scope.json`, and, for a domain perspective, its reference material. Never read or use another reviewer's output.\n4. Make every failure scenario concrete. `trigger` is a specific input or program state (for example, a named argument value, array shape or data condition), and `wrong_output` is the specific wrong result or behaviour that follows. When no concrete scenario can be established, set both `trigger` and `wrong_output` to null and state in `evidence` why none could be established. Choose a trigger that the obvious defence does not answer: for a reproducibility or seeding defect, state a program state in which the documented or customary seeding still fails to reproduce the result (for example, other code drawing from the global generator between the seed and the call), not a change of seed, which only starts a different random experiment.\n5. Assign a severity: `high` when the defect produces a wrong result under realistic inputs; `medium` when it produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result; `low` when it is a latent risk that does not currently produce a wrong result.\n6. Give each finding the id `numerical-analyst-<n>`, numbered from 1, and set `raised_by` to `numerical-analyst`. Every finding states a one-sentence `summary`, a `fix` (a derivation or code change) and the `evidence` you read or computed. Each finding states one defect: report two defects at the same location as two findings, each with its own trigger, wrong output and fix.\n7. Record checked items: each location you examined and found correct, with `file`, `line_start`, `line_end`, `dimension` and a `note` stating what was verified.\n8. Output exactly one JSON object conforming to `candidate-findings.schema.json`: `{\"perspective\": \"numerical-analyst\", \"findings\": [...], \"checked_items\": [...], \"notes\": \"...\"}`. Write nothing else before or after it. Never modify project files.\n\n## Debate\n\n1. In round 0, state one position on every merged finding of the batch. Each position has `finding_id`, `member` set to `numerical-analyst`, `round`, `stance`, a non-empty `reason`, and `answers`.\n2. `stance` is `accept` or `challenge`. Use `withdraw` only for a finding you raised, that is, when `numerical-analyst` appears in its `raised_by`.\n3. `answers` lists the ids of the positions you respond to. A position id has the form `<member>:<finding_id>:<round>`, for example `defender:F3:0`. Leave `answers` empty when you respond to no earlier position.\n4. Judge each finding on its stated `trigger` and `wrong_output`. Accept a finding when the scenario holds; challenge it when the scenario does not hold, when the construct is correct in context, or when no concrete trigger is given and you cannot supply one.\n5. In each later round, read all positions from the earlier rounds before writing yours. Change your stance on a finding only for a reason you state; otherwise repeat it.\n6. Answer explicitly every defender objection to a finding you accept, by listing the objection's position id in `answers` and stating in `reason` why the objection does not hold, or by changing your stance if it does.\n7. Output exactly one JSON object conforming to `debate-positions.schema.json`: `{\"member\": \"numerical-analyst\", \"round\": <round>, \"positions\": [...]}`. Write nothing else before or after it. Never modify project files.\n",
  "theorist": "# Theorist\n\nYou are the theorist on a scientific review panel. The panel reviews code for scientific correctness: whether it computes what it claims to compute. Your perspective id is `theorist`. You review the scope independently, then defend or challenge the panel's merged findings in a debate.\n\n## Stance\n\nYou rederive the mathematics from first principles. For every equation, transformation or reduction in the scope, you establish the intended form, from the docstring, a cited reference or the standard result, and verify that the code implements exactly that form. You do not accept an expression because it looks plausible or because tests pass; you accept it when your own derivation agrees with it, and you report the step at which it departs.\n\n## Guiding questions\n\n1. What equation or transformation is this code meant to implement, and where is its intended form stated?\n2. Does an independent derivation reproduce every term, coefficient, sign and exponent in the code?\n3. Do array and matrix shapes agree with the mathematical objects they represent, including transposes and contraction axes?\n4. Are index and summation bounds exact, including the first and last terms and any off-by-one shift between mathematical and zero-based indexing?\n5. Are the assumptions of the derivation (linearity, symmetry, positive definiteness, independence, smoothness) satisfied where the code applies it?\n6. Does the code reduce to the correct closed form in a special case that can be computed by hand?\n7. Are invariants that the mathematics guarantees (symmetry, normalisation, orthogonality) preserved by the implementation?\n\n## Checks owned\n\nYou lead on every check of `dimensions/mathematical-derivations.md`: correspondence of equations and transformations to their stated or standard forms, matrix and array shapes, and index and summation bounds. You also lead on the derivation side of `dimensions/physical-modelling-and-units.md` where a conservation law or governing equation is discretised: whether the discrete form follows from the continuous one.\n\n## What not to flag\n\n- Style, formatting, naming, lint warnings, type-annotation gaps and missing or imperfect documentation.\n- Performance concerns that do not change any result.\n- Constructs that are correct in context, including floating-point equality against a sentinel value or an exactly representable integer-valued float, and seeding that is deliberately left to the caller and documented as such.\n- Anything outside the files and line ranges listed in `scope.json`, even when you read surrounding code for context.\n- A formulation that differs from the textbook form but is algebraically equivalent; verify the equivalence and record it as a checked item.\n- A documented approximation whose stated regime covers the inputs in scope.\n\n## Independent round\n\n1. Review the whole scope under every one of the five dimensions (`mathematical-derivations`, `numerical-stability`, `physical-modelling-and-units`, `statistical-integrity`, `algorithmic-correctness`), not only the checks you own. Your perspective decides where you look hardest; it does not limit what you report.\n2. Load a dimension document (`dimensions/<name>.md`, relative to the skill directory) on demand, when the code under review calls for its checks.\n3. Work only from the inputs you were given: this brief, `protocol.md`, the dimension documents, `scope.json`, and, for a domain perspective, its reference material. Never read or use another reviewer's output.\n4. Make every failure scenario concrete. `trigger` is a specific input or program state (for example, a named argument value, array shape or data condition), and `wrong_output` is the specific wrong result or behaviour that follows. When no concrete scenario can be established, set both `trigger` and `wrong_output` to null and state in `evidence` why none could be established. Choose a trigger that the obvious defence does not answer: for a reproducibility or seeding defect, state a program state in which the documented or customary seeding still fails to reproduce the result (for example, other code drawing from the global generator between the seed and the call), not a change of seed, which only starts a different random experiment.\n5. Assign a severity: `high` when the defect produces a wrong result under realistic inputs; `medium` when it produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result; `low` when it is a latent risk that does not currently produce a wrong result.\n6. Give each finding the id `theorist-<n>`, numbered from 1, and set `raised_by` to `theorist`. Every finding states a one-sentence `summary`, a `fix` (a derivation or code change) and the `evidence` you read or computed. Each finding states one defect: report two defects at the same location as two findings, each with its own trigger, wrong output and fix.\n7. Record checked items: each location you examined and found correct, with `file`, `line_start`, `line_end`, `dimension` and a `note` stating what was verified.\n8. Output exactly one JSON object conforming to `candidate-findings.schema.json`: `{\"perspective\": \"theorist\", \"findings\": [...], \"checked_items\": [...], \"notes\": \"...\"}`. Write nothing else before or after it. Never modify project files.\n\n## Debate\n\n1. In round 0, state one position on every merged finding of the batch. Each position has `finding_id`, `member` set to `theorist`, `round`, `stance`, a non-empty `reason`, and `answers`.\n2. `stance` is `accept` or `challenge`. Use `withdraw` only for a finding you raised, that is, when `theorist` appears in its `raised_by`.\n3. `answers` lists the ids of the positions you respond to. A position id has the form `<member>:<finding_id>:<round>`, for example `defender:F3:0`. Leave `answers` empty when you respond to no earlier position.\n4. Judge each finding on its stated `trigger` and `wrong_output`. Accept a finding when the scenario holds; challenge it when the scenario does not hold, when the construct is correct in context, or when no concrete trigger is given and you cannot supply one.\n5. In each later round, read all positions from the earlier rounds before writing yours. Change your stance on a finding only for a reason you state; otherwise repeat it.\n6. Answer explicitly every defender objection to a finding you accept, by listing the objection's position id in `answers` and stating in `reason` why the objection does not hold, or by changing your stance if it does.\n7. Output exactly one JSON object conforming to `debate-positions.schema.json`: `{\"member\": \"theorist\", \"round\": <round>, \"positions\": [...]}`. Write nothing else before or after it. Never modify project files.\n",
}

const DIMENSIONS = {
  "algorithmic-correctness": "# Algorithmic correctness\n\nThis dimension covers whether an algorithm computes the result it claims to compute for every input it accepts: the invariants and pre- and postconditions it relies on, the termination and convergence of loops and iterative methods, integer overflow and index arithmetic, the handling of empty, single-element and duplicate-key inputs, dependence on evaluation order or concurrent execution, nondeterminism across runs or platforms, and caches that return stale results. It excludes style, naming, structure and performance, except where a performance construct (parallelism, caching, early exit) changes the result. Floating-point error analysis belongs to the numerical dimension; this dimension is concerned with the control flow and data handling that surround the arithmetic.\n\n## Checks\n\nEach check states what to look for and what evidence establishes a defect. Evidence is always a concrete input or program state together with the wrong output it produces. A suspicion without such a pair is recorded as a checked item, not as a finding with a trigger.\n\n1. **Invariants and pre- and postconditions.** Identify what each function assumes of its inputs (sorted, non-negative, unique, normalised, same length) and what it guarantees of its output. Look for callers that violate an assumption and for code paths that break a guarantee. Evidence: an input that satisfies the documented contract, or a call site that passes an input violating an undocumented assumption, and the incorrect output that follows.\n2. **Termination.** Examine every loop and recursion whose exit depends on data. Look for loop variables that may fail to progress, recursion without a decreasing measure, and `while` conditions that can remain true indefinitely. Evidence: an input for which the procedure does not terminate, or terminates only through an external timeout.\n3. **Convergence criteria.** For iterative methods, check that the stopping test is meaningful at the scale of the quantity (absolute against relative tolerance), that a maximum iteration count exists, and that reaching it is reported rather than silently returning the last iterate. Evidence: an input for which the method stops early with an inaccurate value, or exhausts its iterations and returns an unconverged value presented as a result.\n4. **Integer overflow and precision limits.** Look for fixed-width integers (NumPy `int32` or `int64`, C extensions, TypeScript bitwise operators that coerce to 32 bits), products of counts or indices, and TypeScript `number` values above 2^53. Evidence: realistic input sizes for which an intermediate value exceeds the representable range, and the wrapped or rounded output.\n5. **Index arithmetic.** Check half-open against closed intervals, off-by-one boundaries, lengths computed as `end - start` versus `end - start + 1`, Python negative indices that wrap silently, and TypeScript out-of-range reads that yield `undefined` and then `NaN`. Evidence: an index range and the element that is dropped, duplicated or read from the wrong position.\n6. **Empty, single-element and duplicate-key inputs.** Check behaviour on an empty collection (division by a zero count, `max` of nothing, reduction without an initial value), on one element (sample variance with denominator `n - 1`, interpolation with one point), and on duplicate keys (dictionary or `Map` construction that keeps only the last value, sort or merge steps that assume uniqueness). Evidence: the specific degenerate input and the silent wrong value, as opposed to a clear error.\n7. **Order dependence.** Look for results that depend on iteration order: floating-point reductions over unordered collections, iteration over Python `set` values or over string-keyed hashes, JavaScript object keys that reorder integer-like keys, unsorted directory listings, and \"first match wins\" logic over unordered data. Evidence: two orderings of the same input that produce different outputs.\n8. **Concurrency dependence.** Look for shared mutable state updated from threads, processes, async tasks or workers, and for accumulation in completion order rather than submission order (for example a parallel floating-point sum). Evidence: an input and two schedules that yield different results, or a race that loses an update.\n9. **Nondeterminism across runs or platforms.** Look for unseeded random generators whose output feeds a reported result, hash randomisation, wall-clock time, thread-count-dependent reductions in BLAS or GPU libraries, and platform-dependent defaults (integer width on Windows NumPy before 2.0, locale-dependent parsing). Evidence: two runs or two platforms with identical inputs and different outputs.\n10. **Stale caching.** For every cache or memoisation, list the inputs the cached value depends on and compare them with the cache key. Look for keys that omit a parameter, a mutable global, a file's contents or a configuration value, and for caches keyed on object identity of mutable objects. Evidence: a sequence of calls in which a dependency changes and the cache returns the value computed under the old dependency.\n\n## Severity guidance\n\nThe severities are defined as follows:\n\n- High: produces a wrong result under realistic inputs.\n- Medium: produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result.\n- Low: a latent risk that does not currently produce a wrong result.\n\nTypical mappings for this dimension:\n\n| Defect | Typical severity |\n|---|---|\n| Cache key omits a parameter that callers vary in normal use | High |\n| Iterative method returns an unconverged value as a result for inputs in the documented range | High |\n| Off-by-one boundary that drops or double-counts an element on every call | High |\n| Overflow of an `int32` counter at input sizes the project processes | High |\n| Wrong value (not an error) on empty, single-element or duplicate-key input that a caller can plausibly supply | Medium |\n| Parallel floating-point sum accumulated in completion order, so results differ between runs | Medium |\n| Undocumented unseeded randomness or unsorted directory listing that changes reported results between runs | Medium |\n| Missing iteration limit where all current inputs converge quickly | Low |\n| Overflow reachable only at input sizes far beyond any current use | Low |\n| Cache that would become stale only if a currently constant configuration value were made mutable | Low |\n\nWhen a defect produces a wrong result under realistic inputs only on some platforms that the project supports, it remains High. When it produces a wrong result only on a platform the project does not support, it is Low.\n\n## Not defects\n\nThe following constructs resemble defects in this dimension and must not be reported.\n\n- **Floating-point equality against a sentinel or an exact integer-valued float.** Comparing with `0.0` or `-1.0` when the value was assigned that literal, testing for `NaN` with `isnan` or `Number.isNaN`, or comparing floats that hold small integers exactly, is correct. Exact equality is a defect only when the value is the result of inexact arithmetic.\n- **Seeding left to the caller and documented as such.** A function that accepts a generator or seed argument, or documents that callers must seed, is not nondeterministic within this dimension.\n- **Order-independent reductions.** Integer sums, `min`, `max`, set union and counting do not depend on order. Python `dict` iteration follows insertion order since Python 3.7 and is deterministic for a deterministic insertion sequence.\n- **Nondeterminism that does not reach a result.** Log ordering, progress output, timing measurements and temporary file names that do not affect reported values are not defects.\n- **Python integer arithmetic.** Built-in `int` has arbitrary precision and does not overflow; only fixed-width types (NumPy, `array`, `ctypes`, extensions) can.\n- **Defensive errors on degenerate input.** A function that raises a clear exception on empty input handles the edge case; only a silent wrong value is a defect.\n- **Caches keyed on the full set of immutable inputs.** `functools.lru_cache` on a pure function of hashable arguments, or a `Map` keyed on a complete serialised input, cannot return stale values.\n- **Performance-only concerns.** Quadratic algorithms, redundant recomputation and missing caches are outside this dimension unless they change the result.\n\n## Worked examples\n\n### Defect 1: parallel sum accumulated in completion order (check 8, Medium)\n\nTrigger: chunk partial sums `[1e16, 1.0, -1e16]` complete in a schedule-dependent order. Wrong output: the total is `1.0` when the chunks finish in the order 1e16, -1e16, 1.0, and `0.0` when they finish in the order 1e16, 1.0, -1e16, because `1e16 + 1.0` rounds to `1e16`. The same input gives different results across runs.\n\n```python\ntotal = 0.0\nwith ThreadPoolExecutor() as pool:\n    futures = [pool.submit(partial_sum, c) for c in chunks]\n    for f in as_completed(futures):   # completion order varies per run\n        total += f.result()\n```\n\n```typescript\nlet total = 0;\nawait Promise.all(chunks.map(async (c) => {\n  const s = await partialSum(c);\n  total += s;                         // accumulated as each promise settles\n}));\n```\n\nFix: collect the partial sums in submission order and reduce them in a fixed order, preferably with a compensated sum (`math.fsum(f.result() for f in futures)` in Python; `const parts = await Promise.all(chunks.map(partialSum))` followed by a fixed-order Neumaier sum in TypeScript).\n\n### Defect 2: cache key omits a dependency (check 10, High)\n\nTrigger: `emission_factor(\"QC\")` is called with the reference year 2020, the reference year is then set to 2030, and `emission_factor(\"QC\")` is called again. Wrong output: the second call returns the 2020 factor, because the cache key contains only the region.\n\n```python\nREFERENCE_YEAR = 2020\n\n@lru_cache(maxsize=None)\ndef emission_factor(region: str) -> float:\n    return load_table(REFERENCE_YEAR)[region]\n```\n\n```typescript\nlet referenceYear = 2020;\nconst cache = new Map<string, number>();\nfunction emissionFactor(region: string): number {\n  if (!cache.has(region)) cache.set(region, loadTable(referenceYear)[region]);\n  return cache.get(region)!;\n}\n```\n\nFix: make every dependency part of the key by passing it as an argument: `emission_factor(region: str, year: int)` in Python, and a key such as `` `${region}:${year}` `` in TypeScript.\n\n### Look-alike: equality against an assigned sentinel (not a defect)\n\nThe weights below are assigned the literal `0.0` to mark excluded samples, so the exact comparison is correct; no input produces a wrong output. Reporting it would violate FR-015.\n\n```python\nweights = [0.0 if s.excluded else s.weight for s in samples]\nfor w, s in zip(weights, samples):\n    if w == 0.0:          # sentinel assigned above, not computed\n        continue\n    acc += w * s.value\n```\n\n```typescript\nconst weights = samples.map((s) => (s.excluded ? 0 : s.weight));\nsamples.forEach((s, i) => {\n  if (weights[i] === 0) return;   // sentinel assigned above, not computed\n  acc += weights[i] * s.value;\n});\n```\n\nReason it is not a defect: the compared value is an exact literal assigned on a known path, not the result of inexact arithmetic. It would become a defect only if a computed weight could be a tiny non-zero value intended to mean \"excluded\", which requires a concrete input to establish.\n",
  "mathematical-derivations": "# Mathematical derivations\n\nThis dimension covers the correspondence between the mathematics a piece of code claims to implement and the computation it actually performs. It includes equations and transformations compared with their stated or standard forms (each derivation step, signs, constant factors such as 2 and pi, transposes and conjugates), the shapes of matrices and arrays entering each operation, and the bounds of indices and summations, including off-by-one errors. It excludes floating-point behaviour (see numerical stability), units and physical validity (see physical modelling and units), and all matters of style, naming, formatting and performance. A finding in this dimension asserts that the code computes a different mathematical quantity from the one intended.\n\n## Checks\n\n1. **Stated-form correspondence.** Locate the reference form: a docstring, comment, cited paper, variable name or the standard textbook form of a named quantity. Compare the implemented expression term by term. A defect is established by an input for which the code and the reference form, evaluated by hand, give different values.\n2. **Derivation steps.** Where the code implements a rearranged, simplified or discretised form, verify each algebraic step from the reference form to the code. Look for dropped terms, terms moved across an equality without a sign change, and a chain rule applied incompletely. Evidence is an input on which the original and the rearranged form disagree.\n3. **Signs.** Check the sign of every term against the reference form, with particular attention to rotation matrices, cross products, gradient descent updates, and differences written as `a - b` where `b - a` is intended. Evidence is an input whose output has the wrong sign or the wrong orientation.\n4. **Constant factors.** Check factors of 2, pi, 2 pi, 1/2 and normalisation constants: angular versus ordinary frequency, radius versus diameter, the 1/2 in kinetic energy or quadratic forms, and the normalisation of transforms and densities. Evidence is an input whose output differs from the reference by exactly the missing or extra factor.\n5. **Transposes and conjugates.** Check whether `A`, `A^T` or `A^H` is required at each use, and whether a row-major or column-major convention changes the meaning of an index pair. Evidence is a non-symmetric (or complex) input whose output differs from the reference.\n6. **Shapes.** Track the shape of each operand through the expression. Check that matrix products have conforming inner dimensions for the intended reason, not by coincidence (a square matrix conforms in both orders), and that reductions run over the intended axis. Evidence is a non-square input that either fails or yields a result of the wrong shape or value.\n7. **Index and summation bounds.** Compare each loop or slice bound with the summation limits of the reference form, translating between one-based mathematical notation and zero-based code. Check inclusive versus exclusive upper bounds and the first and last terms. Evidence is a small input (two or three elements suffice) whose output includes a term that should be excluded or omits one that should be included.\n8. **Index mapping.** Check that the index used to read an element matches the index in the formula: `x[i]` versus `x[i-1]`, swapped `i` and `j`, and neighbours in stencils. Evidence is an input with distinct element values for which the wrong element is read.\n\n## Severity guidance\n\nThe severity definitions are those of the skill:\n\n- High: produces a wrong result under realistic inputs; Medium: produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result; Low: a latent risk that does not currently produce a wrong result.\n\nTypical mapping for this dimension:\n\n- **High.** A wrong sign, a missing or extra constant factor, a missing transpose on a non-symmetric operand, a summation bound that includes or excludes a term for every input, or a wrong index in a stencil. These defects affect every typical input.\n- **Medium.** A bound error that matters only for empty, single-element or boundary inputs; a transpose that is omitted where the operand is symmetric in every realistic case but not guaranteed to be; a formula whose convention (for example, transform normalisation) differs from the one stated, so that published results cannot be reproduced from the documentation.\n- **Low.** An expression that is correct only because current callers pass square or symmetric operands, with no such call yet producing a wrong value; a reference form that is undocumented, so that a future change to the convention would go unnoticed.\n\n## Not defects\n\n- **Alternative but equivalent forms.** An expression rearranged into an algebraically equivalent form is not a defect, even when it differs visually from the textbook. Verify equivalence before reporting.\n- **Documented conventions.** A different but documented convention (unitary versus non-unitary Fourier transform, `exp(-i omega t)` versus `exp(i omega t)`, row versus column vectors) is not a defect when it is applied consistently.\n- **Zero-based translations.** A loop `range(0, n)` implementing a sum from 1 to n is correct when the body indexes element `i` as the i-plus-first term. Check the body, not only the bounds.\n- **Symmetric operands by construction.** A missing transpose on a matrix that is symmetric by construction (a covariance matrix, a Gram matrix, a Laplacian) is not a defect.\n- **Finite differences with n - 1 terms.** A loop starting at 1, or a sum of n - 1 terms, is correct for differences between consecutive elements. The shorter range is required, not an off-by-one.\n- **Numerical concerns.** A correct formula that loses precision belongs to numerical stability, not to this dimension.\n\n## Worked examples\n\n### Defect 1: trapezoidal rule with an off-by-one interior sum (High)\n\nThe composite trapezoidal rule on n uniformly spaced samples is h times (y_0/2 + y_1 + ... + y_{n-2} + y_{n-1}/2). The interior sum runs over indices 1 to n - 2.\n\n```python\ndef trapezoid(y: list[float], h: float) -> float:\n    interior = sum(y[i] for i in range(1, len(y)))  # includes y[n-1]\n    return h * (0.5 * (y[0] + y[-1]) + interior)\n```\n\n```typescript\nfunction trapezoid(y: number[], h: number): number {\n  let interior = 0;\n  for (let i = 1; i < y.length; i++) interior += y[i]; // includes y[n-1]\n  return h * (0.5 * (y[0] + y[y.length - 1]) + interior);\n}\n```\n\n- **Trigger:** `y = [1, 1, 1]`, `h = 1` (the integral of the constant 1 over [0, 2]).\n- **Wrong output:** 3. The correct value is 2; the last sample is counted with weight 3/2 instead of 1/2.\n- **Fix:** bound the interior sum by `len(y) - 1` (Python `range(1, len(y) - 1)`; TypeScript `i < y.length - 1`).\n\n### Defect 2: rotation matrix with transposed signs (High)\n\nA counter-clockwise rotation by theta maps (x, y) to (x cos theta - y sin theta, x sin theta + y cos theta). The code below applies the transpose, which rotates clockwise.\n\n```python\nimport math\n\ndef rotate(x: float, y: float, theta: float) -> tuple[float, float]:\n    c, s = math.cos(theta), math.sin(theta)\n    return (x * c + y * s, -x * s + y * c)\n```\n\n```typescript\nfunction rotate(x: number, y: number, theta: number): [number, number] {\n  const c = Math.cos(theta), s = Math.sin(theta);\n  return [x * c + y * s, -x * s + y * c];\n}\n```\n\n- **Trigger:** `(x, y) = (1, 0)`, `theta = pi / 2`, documented as a counter-clockwise rotation.\n- **Wrong output:** approximately (0, -1). The correct value is (0, 1).\n- **Fix:** return `(x * c - y * s, x * s + y * c)`, or document the function as a clockwise rotation if that is the intended convention and every caller agrees.\n\n### Defect 3: matrix-vector product with a missing transpose (High)\n\nThe docstring states that the function returns `A^T v` for an m-by-n matrix `A` stored as a list of rows and a vector `v` of length m. The code computes `A v` instead, which conforms only when m equals n.\n\n```python\ndef at_times_v(a: list[list[float]], v: list[float]) -> list[float]:\n    \"\"\"Return A^T v.\"\"\"\n    return [sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a))]\n```\n\n```typescript\n/** Return A^T v. */\nfunction atTimesV(a: number[][], v: number[]): number[] {\n  return a.map((row) => row.reduce((acc, aij, j) => acc + aij * v[j], 0));\n}\n```\n\n- **Trigger:** `A = [[1, 2], [3, 4]]`, `v = [1, 0]`.\n- **Wrong output:** `[1, 3]` (the first column of `A`). The correct value of `A^T v` is `[1, 2]` (the first row of `A`). For a 3-by-2 matrix with `v` of length 3, the Python version raises `IndexError` and the TypeScript version silently ignores `v[2]`.\n- **Fix:** sum over the row index: element `j` of the result is the sum over `i` of `a[i][j] * v[i]`, for `j` from 0 to n - 1.\n\n### Look-alike: consecutive differences over n - 1 terms (not a defect)\n\nThe loop below starts at index 1 and appears to skip an element. It computes the n - 1 forward differences of n samples, which is the intended quantity.\n\n```python\ndef differences(x: list[float]) -> list[float]:\n    return [x[i] - x[i - 1] for i in range(1, len(x))]\n```\n\n```typescript\nfunction differences(x: number[]): number[] {\n  const d: number[] = [];\n  for (let i = 1; i < x.length; i++) d.push(x[i] - x[i - 1]);\n  return d;\n}\n```\n\n- **Candidate trigger:** `x = [0, 1, 3]`.\n- **Output:** `[1, 2]`, which is correct: two differences from three samples, with no term omitted and no index out of range.\n- **Reason not reported:** the range of n - 1 terms is required by the definition. No input produces a wrong value, so no concrete failure scenario exists.\n",
  "numerical-stability": "# Numerical stability\n\nThis dimension covers defects in which a computation that is mathematically correct produces a wrong result because of finite-precision arithmetic: floating-point equality comparisons, overflow and underflow, catastrophic cancellation, division by quantities that can approach zero, unstable evaluation of exponentials and logarithms, silent narrowing of numeric precision, implicit broadcasting that yields an unintended shape, and propagation of not-a-number (NaN) or missing values through reductions. It excludes style, naming, lint and performance; it also excludes errors in the underlying formula, which belong to the mathematical dimension. A finding in this dimension is reportable only when a concrete input can be stated together with the wrong output it produces.\n\n## Checks\n\n1. **Floating-point equality.** Look for `==` or `!=` (and `===`, `!==` in TypeScript) between floating-point values that are results of arithmetic, and for loop conditions that wait for a float to reach an exact value. Evidence: an input for which the computed value differs from the expected value in the last bits, for example `0.1 + 0.2 == 0.3` evaluating to false, and the branch taken as a result.\n2. **Overflow and underflow.** Look for `exp`, `pow`, factorials, products of many terms, and squared magnitudes of large values. Evidence: an input within the realistic domain that yields `inf`, `Infinity`, `0.0` or a subnormal value where a finite, non-zero result is expected, and the downstream value that results.\n3. **Catastrophic cancellation.** Look for subtraction of two nearly equal quantities whose difference is the quantity of interest: `E[x^2] - E[x]^2`, `1 - cos(x)` for small `x`, the textbook quadratic formula when `b^2 >> 4ac`, finite differences with a very small step. Evidence: an input for which the computed result has few or no correct significant digits, stated beside the exact value.\n4. **Division near zero.** Look for denominators that are differences, norms, standard deviations, counts after filtering, or user-supplied parameters, with no guard. Evidence: an input that makes the denominator zero or vanishingly small, and the resulting `inf`, `NaN`, `ZeroDivisionError` or exploding value.\n5. **Unstable exponential and logarithm evaluation.** Look for `log(sum(exp(x)))`, softmax computed as `exp(x) / sum(exp(x))`, `log(1 + x)` for small `x`, and `exp(x) - 1` for small `x`. Evidence: an input such as large logits for which the naive form returns `inf` or `NaN`, compared with the stable form (log-sum-exp with the maximum subtracted, `log1p`, `expm1`).\n6. **Silent narrowing of precision.** Look for casts to `float32`, `float16` or integer types, `astype`, typed arrays such as `Float32Array` or `Int32Array`, integer division where real division is intended, and accumulation in a narrower type than the data. Evidence: an input whose result differs, beyond the stated tolerance, from the same computation carried out in the wider type.\n7. **Unintended broadcasting.** Look for element-wise operations between arrays of shapes `(n,)` and `(n, 1)`, reductions without an explicit axis, and operations that silently expand a dimension. Evidence: the input shapes, the shape actually produced, and the shape the surrounding code requires.\n8. **NaN propagation through reductions.** Look for `sum`, `mean`, `max`, `min` and sorting over data that can contain `NaN`, `None`, `null` or `undefined`, and for NaN-aware variants used where propagation is intended (or the reverse). Evidence: an input containing one missing value and the resulting reduction (`NaN`, a silently dropped element, or an order-dependent `max`).\n\n## Severity guidance\n\nThe severity definitions are those of the skill:\n\n- High: produces a wrong result under realistic inputs.\n- Medium: produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result.\n- Low: a latent risk that does not currently produce a wrong result.\n\nTypical mapping for this dimension:\n\n| Defect | Typical severity | Condition |\n| --- | --- | --- |\n| Naive log-sum-exp or softmax on logits or log-likelihoods | High | Inputs of magnitude above about 700 (float64) or 88 (float32) occur in normal use |\n| Variance as `E[x^2] - E[x]^2` on data with a large mean | High | Measured data with a mean far larger than its spread |\n| Equality test on an arithmetic float result controlling a branch | High | The compared values are computed, not assigned |\n| Division by a difference, count or norm without a guard | Medium | Zero is reachable only for degenerate inputs (empty filter, identical points) |\n| Narrowing to `float32` before accumulation | Medium | Error exceeds tolerance only for long series or large magnitudes |\n| Reduction that propagates or drops `NaN` unexpectedly | Medium | Missing values are possible but not typical |\n| Broadcasting that yields a wrong shape | High | The wrong shape is consumed without error |\n| Unguarded denominator that cannot currently reach zero | Low | All present callers guarantee a non-zero value |\n\n## Not defects\n\nThe following constructs resemble defects but are correct in context and must not be reported. Each should appear among the items checked and found correct.\n\n1. **Equality against a sentinel value.** `x == -9999.0`, `x === -1` or `value == MISSING` where the sentinel is assigned, never computed, is exact: an assigned literal is stored without rounding, and the comparison tests identity of a marker, not closeness of a measurement.\n2. **Equality against an exact integer-valued float.** `n == 0.0`, `count == 3.0` or `x == 1.0` where the value is an integer-valued float obtained by assignment, counting or conversion of an integer within the exact range (magnitude at most 2^53 for float64) is exact. Every integer in that range is representable, and integer addition within it does not round.\n3. **Equality used to detect an exact zero before a guarded operation.** `if denom == 0: return default` is correct when the intent is to avoid an exception; near-zero values are a separate check (4) that must be argued on its own evidence.\n4. **Division whose denominator is provably non-zero.** A denominator that is a constant, a length checked earlier, or a quantity bounded away from zero by validation is not a defect.\n5. **Deliberate reduced precision.** Use of `float32` or `float16` that is documented, matches an external format (GPU kernels, file formats) and stays within a stated tolerance is a design choice, not a defect.\n6. **Intentional broadcasting.** Subtracting a `(1, m)` row of column means from an `(n, m)` matrix is the standard idiom; it is a defect only when the resulting shape differs from the shape required.\n7. **NaN propagation that is intended.** A reduction that returns `NaN` to signal missing input, and whose callers check for it, is correct.\n\n## Worked examples\n\n### Defect: naive log-sum-exp (check 5, High)\n\nTrigger: `x = [1000, 1000]`. Wrong output: `inf` (Python) and `Infinity` (TypeScript), because `exp(1000)` overflows. Correct value: `1000 + log(2) = 1000.6931...`.\n\n```python\nimport math\n\ndef logsumexp(x: list[float]) -> float:\n    return math.log(sum(math.exp(v) for v in x))  # inf for x = [1000, 1000]\n```\n\n```typescript\nconst logSumExp = (x: number[]): number =>\n  Math.log(x.reduce((s, v) => s + Math.exp(v), 0)); // Infinity for [1000, 1000]\n```\n\nFix: subtract the maximum before exponentiating.\n\n```python\ndef logsumexp(x: list[float]) -> float:\n    m = max(x)\n    return m + math.log(sum(math.exp(v - m) for v in x))\n```\n\n```typescript\nconst logSumExp = (x: number[]): number => {\n  const m = Math.max(...x);\n  return m + Math.log(x.reduce((s, v) => s + Math.exp(v - m), 0));\n};\n```\n\n### Defect: variance by catastrophic cancellation (check 3, High)\n\nTrigger: `xs = [1e9 + 1, 1e9 + 2, 1e9 + 3]`. Wrong output: `0.0` in both languages. Correct population variance: `0.6666...`. The two terms are near `1e18`, where adjacent doubles are 128 apart, so their difference retains no correct digits.\n\n```python\ndef variance(xs: list[float]) -> float:\n    m = sum(xs) / len(xs)\n    return sum(x * x for x in xs) / len(xs) - m * m  # 0.0\n```\n\n```typescript\nconst variance = (xs: number[]): number => {\n  const m = xs.reduce((a, b) => a + b, 0) / xs.length;\n  return xs.reduce((a, x) => a + x * x, 0) / xs.length - m * m; // 0\n};\n```\n\nFix: use the two-pass form `sum((x - m) ** 2) / n` (or Welford's algorithm for streaming data), which returns `0.6666666666666666` for the same input.\n\n### Look-alike: equality against a sentinel (not a defect)\n\nThe value `-9999.0` is a missing-data marker assigned by the reader, never the result of arithmetic. The comparison is exact and must not be reported.\n\n```python\nMISSING = -9999.0\n\ndef valid(readings: list[float]) -> list[float]:\n    return [r for r in readings if r != MISSING]\n```\n\n```typescript\nconst MISSING = -9999.0;\nconst valid = (readings: number[]): number[] =>\n  readings.filter((r) => r !== MISSING);\n```\n\nReason: no input exists for which an assigned `-9999.0` compares unequal to the literal `-9999.0`, so no failure scenario can be stated. A finding would be reportable only if the sentinel were produced by computation (for example after unit conversion), in which case the comparison falls under check 1.\n",
  "physical-modelling-and-units": "# Physical modelling and units\n\nThis dimension covers whether code represents physical quantities and physical models correctly: explicit and consistent units, unit handling where data is read or written, conservation laws in continuous and discrete form, probabilities and fractions that must sum to one, values outside physically possible bounds, discretisation of space and time, boundary and initial conditions, stability limits of time-stepping schemes, sign conventions and coordinate frames, and use of a model outside its regime of validity. It excludes style, naming, performance and lint, as well as floating-point behaviour that belongs to numerical stability. It contains no domain-specific rules (for example building-energy rules); those are contributed by domain extensions.\n\n## Checks\n\n1. **Explicit, consistent units.** Look for physical quantities combined in one expression without a stated or derivable unit, and for operands whose units differ (kPa added to Pa, hours multiplied by a rate per second). Evidence: an input in the documented unit and the output that is wrong by the conversion factor.\n2. **Unit handling at I/O.** Look at file readers, API boundaries, configuration and serialisation: values read in one unit and used as another (degrees Celsius used as kelvin, degrees used as radians, kilometres as metres), or written without recording the unit. Evidence: a realistic file value and the resulting output, compared with the value obtained after correct conversion.\n3. **Conservation, continuous and discrete.** Check that mass, energy, momentum, charge or count is conserved by the governing equations and also by the discrete update (fluxes leaving one cell enter its neighbour; sources and sinks are accounted once). Evidence: an initial state whose total changes over a step with no source or sink, and the size of the drift.\n4. **Probabilities and fractions sum to one.** Check that mixtures, distributions, partition fractions and transition matrix rows are normalised after every update, clipping or truncation. Evidence: an input after which the components sum to a value other than one beyond rounding, and the downstream quantity that is therefore wrong.\n5. **Physically impossible values.** Look for paths that produce negative absolute temperature, negative mass, density or concentration, a probability outside [0, 1], an efficiency above one, or a speed above a stated limit, without detection. Evidence: an input that drives the value across the bound and the value produced.\n6. **Discretisation.** Check grid spacing, cell-centre versus cell-face placement, off-by-one extents of the domain, and time-step accumulation (for example `t += dt` drifting from `n * dt` when a stopping condition depends on it). Evidence: a grid or step sequence for which the computed solution differs from the analytical or refined solution beyond the scheme's stated order.\n7. **Boundary and initial conditions.** Check that every boundary has a condition, that the condition is applied to the correct nodes or faces, that Dirichlet, Neumann and periodic conditions are not confused, and that initial conditions are consistent with the boundary conditions. Evidence: a configuration in which a boundary value or flux in the output differs from the one prescribed.\n8. **Stability limits of explicit schemes.** For explicit time stepping, derive the stability limit (CFL for advection, `alpha * dt / dx**2 <= 1/2` for one-dimensional explicit diffusion, the oscillation limit for stiff source terms) and check that the code enforces it or chooses `dt` from it. Evidence: parameter values that violate the limit and the resulting growing or oscillating output.\n9. **Sign conventions and frames.** Check that the sign of fluxes, forces and heat transfer is consistent between producer and consumer, and that vectors are not combined across coordinate frames (body versus inertial, local versus global, east-north-up versus north-east-down) without a transformation. Evidence: an input whose output has the wrong sign or orientation.\n10. **Validity regime.** Check whether a model or correlation is applied outside the range in which it holds (a small-angle approximation at large angles, a laminar correlation at turbulent Reynolds numbers, an ideal-gas law near condensation, an empirical fit outside its fitted range). Evidence: an input in the code's reachable range that lies outside the stated regime, and the error against the exact or accepted value.\n\n## Severity guidance\n\nThe severities are those defined by the skill:\n\n- **High:** produces a wrong result under realistic inputs.\n- **Medium:** produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result.\n- **Low:** a latent risk that does not currently produce a wrong result.\n\nTypical mapping:\n\n| Defect | Severity |\n|---|---|\n| Unit mismatch or unconverted I/O value on the main computational path | High |\n| Explicit time step that exceeds its stability limit for the default or documented parameters | High |\n| Discrete update that does not conserve a conserved quantity in normal operation | High |\n| Stability limit violated only for a plausible but non-default combination of parameters | Medium |\n| Fractions that fail to sum to one only after clipping at an extreme input | Medium |\n| Output written without its unit, so a result cannot be reproduced or reinterpreted | Medium |\n| Model used near, but not beyond, the edge of its validity regime with no guard | Low |\n| Unit carried only by an identifier name, with every current caller consistent | Low |\n\n## Not defects\n\n- **Temperature differences in degrees Celsius.** A difference of 1 °C equals a difference of 1 K, so `k * (t_hot_c - t_cold_c)` is correct. Only absolute temperatures in a nonlinear law (radiation, ideal gas, Arrhenius) require kelvin.\n- **Deliberately non-dimensional formulations.** Code written in scaled variables (Reynolds number, dimensionless time) is consistent when the scaling is applied once at input and inverted once at output.\n- **Unconditionally stable schemes.** Implicit Euler, Crank-Nicolson for diffusion and other implicit schemes have no explicit stability limit; a large `dt` affects accuracy, which is reported only with a concrete accuracy failure.\n- **Stability enforced by the caller.** A solver documented to require `dt` within a stated limit, whose every caller in scope computes `dt` from that limit, is not a defect.\n- **Normalisation to rounding.** Fractions that sum to one within a few units in the last place are correct; exact floating-point equality to one is not required.\n- **Sign conventions that differ but are documented and converted.** A flux reported positive inward in one module and positive outward in another is correct when the interface converts it.\n\n## Worked examples\n\n### Defect 1: explicit diffusion step above its stability limit (High)\n\nTrigger: `alpha = 1e-4` m²/s, `dx = 0.01` m, `dt = 1.0` s gives `r = alpha * dt / dx**2 = 1.0`, above the limit of 0.5. Wrong output: the highest-frequency mode is multiplied by `1 - 4r = -3` per step, so an initial spike of 1.0 on a 101-node grid alternates in sign and reaches about 3.8e8 in magnitude after 20 steps, while the exact solution decays. Fix: choose `dt` from the limit, sub-step, or use an implicit scheme.\n\n```python\ndef step(u: list[float], alpha: float, dx: float, dt: float) -> list[float]:\n    r = alpha * dt / dx**2  # defect: r is never checked against 0.5\n    return [u[0]] + [u[i] + r * (u[i-1] - 2*u[i] + u[i+1]) for i in range(1, len(u)-1)] + [u[-1]]\n\n# Fix\ndef stable_dt(alpha: float, dx: float, dt: float) -> float:\n    return min(dt, 0.5 * dx**2 / alpha)\n```\n\n```typescript\nfunction step(u: number[], alpha: number, dx: number, dt: number): number[] {\n  const r = (alpha * dt) / (dx * dx); // defect: r is never checked against 0.5\n  return u.map((v, i) => (i === 0 || i === u.length - 1 ? v : v + r * (u[i - 1] - 2 * v + u[i + 1])));\n}\n\n// Fix\nconst stableDt = (alpha: number, dx: number, dt: number): number => Math.min(dt, (0.5 * dx * dx) / alpha);\n```\n\n### Defect 2: Celsius read from input used as an absolute temperature (High)\n\nTrigger: a surface temperature of 20 read from a CSV column documented in °C. Wrong output: the emitted radiative flux `sigma * T**4` is 9.07e-3 W/m² instead of 418.7 W/m² (a factor of about 46,000). Fix: convert to kelvin at the I/O boundary.\n\n```python\nSIGMA = 5.670e-8  # W m^-2 K^-4\ndef emitted_flux(row: dict[str, str]) -> float:\n    t = float(row[\"temp_c\"])        # defect: Celsius used as kelvin\n    return SIGMA * t**4\n# Fix: t = float(row[\"temp_c\"]) + 273.15\n```\n\n```typescript\nconst SIGMA = 5.670e-8; // W m^-2 K^-4\nfunction emittedFlux(row: Record<string, string>): number {\n  const t = Number(row[\"temp_c\"]); // defect: Celsius used as kelvin\n  return SIGMA * t ** 4;\n}\n// Fix: const t = Number(row[\"temp_c\"]) + 273.15;\n```\n\n### Look-alike: Celsius difference in a linear conduction law (not a defect)\n\nTrigger considered: `t_hot_c = 80`, `t_cold_c = 20`, `k = 50` W/(m K), `area = 1` m², `length = 0.1` m. Output: 30,000 W, identical to the result in kelvin, because only the difference enters a linear law. No fix is required; record the item as checked and found correct.\n\n```python\ndef conduction(k: float, area: float, length: float, t_hot_c: float, t_cold_c: float) -> float:\n    return k * area * (t_hot_c - t_cold_c) / length  # correct: a difference in degC equals one in K\n```\n\n```typescript\nfunction conduction(k: number, area: number, length: number, tHotC: number, tColdC: number): number {\n  return (k * area * (tHotC - tColdC)) / length; // correct: a difference in degC equals one in K\n}\n```\n",
  "statistical-integrity": "# Statistical integrity\n\nThis dimension covers the integrity of data handling in statistical and data-science code (FR-011): leakage of information from validation, test or future data into training or estimation; plotting and reporting code that mutates the data it displays; and stochastic processes whose results cannot be reproduced because no seed or other reproducibility control is applied. It excludes the numerical behaviour of the estimators themselves (numerical stability), the physical meaning of the quantities (physical modelling and units), the correctness of formulas (mathematical invariants), and nondeterminism caused by parallel execution order (algorithmic correctness). A finding in this dimension must show that a reported number, metric or figure differs from the value that leak-free, non-mutating, reproducible code would produce.\n\n## Checks\n\n1. **Preprocessing fitted before the split.** Look for a stateful transform (scaler, imputer, encoder, PCA, feature selector, outlier filter, vocabulary builder) whose `fit` or statistics use rows that later belong to the validation or test set, including fitting inside a cross-validation loop on the full fold set rather than on each training fold. Evidence: a held-out row whose value changes a quantity used in training (a mean, a variance, an imputed value, a selected feature), and the resulting change in the transformed training data or in the evaluation metric.\n2. **Temporal leakage.** Look for random or shuffled splits of time-ordered data, features that read future values (centred rolling windows, backward fill, negative shifts, statistics over the whole series), and labels joined on a time key without an \"as of\" constraint. Evidence: a timestamp `t` in the training or prediction set whose feature depends on an observation after `t`, with the value it takes with and without that observation.\n3. **Target and post-outcome leakage.** Look for features computed from the target, from records created after the outcome, or from aggregates (target encodings, group means) that include the row being predicted. Evidence: a row whose feature changes when its own label changes.\n4. **Entity and duplicate leakage.** Look for row-level splits of data with repeated subjects, sites, sessions or exact duplicates. Evidence: an entity or duplicated row present in both training and test sets, and the metric inflation this produces.\n5. **Selection on the test set.** Look for hyperparameters, thresholds, feature sets or early-stopping points chosen by the score on the data that is then reported as the held-out result. Evidence: the reported score is the maximum over candidates evaluated on the same held-out data.\n6. **Mutation by plotting or reporting.** Look for in-place operations on caller-owned data inside plotting, logging or summary functions: in-place sort, `inplace=True`, augmented assignment on a passed array or column, `dropna` or filtering on the original, `Array.prototype.sort`, `reverse` or `splice` on an argument. Evidence: a call sequence in which a value computed after the plot or report differs from the value computed before it.\n7. **Unseeded stochastic processes.** Look for random sampling, shuffling, initialisation, bootstrap, Monte Carlo, dropout or stochastic optimisation that draws from an unseeded or global generator (`np.random.*` without a seed, `random.random`, `default_rng()` with no argument, `Math.random`) in code that produces a reported result. Evidence: two runs on identical inputs that produce different reported values.\n8. **Incomplete seeding.** Look for a seed that does not reach every generator in use: one library seeded while another is not, worker processes or threads that inherit or re-derive the same or an unset state, or a seed applied after the first draw. Evidence: the generator that remains unseeded and the output that varies between runs.\n\n## Severity guidance\n\nSeverity definitions, from the skill: **High:** produces a wrong result under realistic inputs; **Medium:** produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result; **Low:** a latent risk that does not currently produce a wrong result.\n\n| Typical defect | Severity |\n| --- | --- |\n| Scaler, imputer or feature selector fitted on data that includes the validation or test rows, where a metric is reported | High |\n| Random split or future-reading feature on time-ordered data used for forecasting or evaluation | High |\n| Target encoding or feature that includes the predicted row's own label | High |\n| Plotting or reporting function that mutates data used by a later computation in the same pipeline | High |\n| Entity or duplicate leakage present only when a subject appears more than once, which the data permits but rarely contains | Medium |\n| Unseeded stochastic process whose output is reported (prevents reproduction) | Medium |\n| Seed that does not reach one generator in use (prevents reproduction) | Medium |\n| Mutating plotting or reporting function whose callers do not currently reuse the data afterwards | Low |\n| Global-generator use in code that currently runs only with a fixed, seeded caller | Low |\n\n## Not defects\n\n- **Stateless transforms before the split.** A logarithm, a fixed unit conversion, clipping to physical constants or a fixed one-hot vocabulary learns nothing from the data, so applying it before the split cannot leak.\n- **Fitting inside a pipeline.** A transform inside a pipeline object passed to cross-validation is refitted on each training fold; this is the correct order.\n- **Refitting on all data after evaluation.** Refitting the final model and its preprocessing on the full dataset for deployment is correct when the reported metrics were computed earlier on a proper split.\n- **Seeding documented as left to the caller (FR-015).** A function that accepts a generator or seed parameter, or whose documentation states that the caller is responsible for seeding, is correct; the reproducibility obligation lies with the caller, which may be reviewed separately.\n- **Randomness that does not affect a reported result.** Random temporary file names, retry jitter, UI colours and sampling for a visual preview that is not reported as a statistic are not stochastic results.\n- **Retrospective smoothing.** A centred window or backward fill in descriptive analysis of a completed series, where nothing is predicted or evaluated, is not temporal leakage.\n- **Mutation of a local copy.** In-place operations on an explicit copy (`df.copy()`, `[...arr]`, `arr.slice()`, `np.array(x, copy=True)`) inside a plotting function do not affect the caller.\n\n## Worked examples\n\n### Defect 1: scaler fitted before the train/test split (High)\n\n```python\nX_scaled = StandardScaler().fit_transform(X)       # fit sees every row\nX_tr, X_te = X_scaled[:4], X_scaled[4:]\n```\n\n```typescript\nconst mu = mean(x), sd = std(x);                   // statistics over every row\nconst scaled = x.map(v => (v - mu) / sd);\nconst [train, test] = [scaled.slice(0, 4), scaled.slice(4)];\n```\n\nTrigger: `x = [1, 2, 3, 4, 100]` with the last row held out. Wrong output: the training mean is 22.0 and the population standard deviation is 39.01, so the first training row scales to -0.538; with the scaler fitted on the training rows only (mean 2.5, standard deviation 1.118) it scales to -1.342. The test row's value has entered every training feature, and any reported test metric is computed against statistics that already include the test data. Fix: split first, fit on the training rows, transform both sets with the fitted parameters (`scaler.fit(X_tr)`, then `scaler.transform(X_te)`; in TypeScript compute `mu` and `sd` from `train` only).\n\n### Defect 2: plotting function sorts the caller's data in place (High)\n\n```python\ndef plot_profile(t, y):\n    y.sort()                                       # mutates the caller's list\n    plt.plot(t, y)\n\nplot_profile(t, y); peak_time = t[int(np.argmax(y))]\n```\n\n```typescript\nfunction plotProfile(t: number[], y: number[]): void {\n  y.sort((a, b) => a - b);                         // mutates the caller's array\n  chart.line(t, y);\n}\nplotProfile(t, y); const peakTime = t[y.indexOf(Math.max(...y))];\n```\n\nTrigger: `t = [0, 1, 2]`, `y = [3, 1, 2]`. Wrong output: after the call `y` is `[1, 2, 3]`, so the peak time is reported as 2 instead of 0, and the plotted curve no longer pairs each time with its value. Fix: sort a copy (`ys = sorted(y)`; `const ys = [...y].sort(...)`), or plot without sorting.\n\n### Look-alike: seeding documented as left to the caller (not a defect)\n\n```python\ndef bootstrap_mean(x: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray:\n    \"\"\"Resample x n times. Seeding is the caller's responsibility via rng.\"\"\"\n    return np.array([rng.choice(x, x.size).mean() for _ in range(n)])\n```\n\n```typescript\n/** Resample x n times. The caller supplies a seeded generator `rand`. */\nfunction bootstrapMean(x: number[], n: number, rand: () => number): number[] {\n  return Array.from({ length: n }, () =>\n    mean(x.map(() => x[Math.floor(rand() * x.length)])));\n}\n```\n\nReason: the function draws only from the generator it is given and documents that seeding belongs to the caller, so two calls with identically seeded generators return identical results. No trigger produces an irreproducible output inside this function. Report it among the items checked and found correct. The same function calling `np.random.choice` or `Math.random` directly, with no documented contract, would be a defect under check 7 (Medium).\n",
}

const SCHEMAS = {
  "candidate-findings": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "sci-review/schemas/candidate-findings.schema.json",
    "title": "Candidate findings",
    "description": "Output of one perspective reviewer in the independent round, for one review part. Semantic checks in panel.py: line_end >= line_start; every location lies inside the review scope.",
    "type": "object",
    "required": [
      "perspective",
      "findings",
      "checked_items",
      "notes"
    ],
    "properties": {
      "perspective": {
        "type": "string",
        "pattern": "^[a-z0-9][a-z0-9-]*$"
      },
      "part": {
        "description": "The review part this message covers (parts.json id, p1, p2, ...). In a review of several parts, finding ids are <perspective>-<part>-<n>.",
        "type": "string",
        "pattern": "^p[1-9][0-9]*$"
      },
      "findings": {
        "type": "array",
        "items": {
          "$ref": "#/$defs/CandidateFinding"
        }
      },
      "checked_items": {
        "type": "array",
        "items": {
          "$ref": "#/$defs/CheckedItem"
        }
      },
      "notes": {
        "type": "string"
      }
    },
    "additionalProperties": false,
    "$defs": {
      "Dimension": {
        "type": "string",
        "enum": [
          "mathematical-derivations",
          "numerical-stability",
          "physical-modelling-and-units",
          "statistical-integrity",
          "algorithmic-correctness"
        ]
      },
      "Severity": {
        "type": "string",
        "enum": [
          "high",
          "medium",
          "low"
        ]
      },
      "CandidateFinding": {
        "description": "A defect reported by one perspective. A null trigger or wrong_output makes the finding non-concrete.",
        "type": "object",
        "required": [
          "id",
          "raised_by",
          "file",
          "line_start",
          "line_end",
          "dimension",
          "severity",
          "summary",
          "trigger",
          "wrong_output",
          "fix",
          "evidence"
        ],
        "properties": {
          "id": {
            "description": "Of the form <perspective>-<n>, or <perspective>-<part>-<n> in a review of several parts.",
            "type": "string",
            "pattern": "^[a-z0-9-]+-[0-9]+$"
          },
          "raised_by": {
            "type": "string",
            "pattern": "^[a-z0-9][a-z0-9-]*$"
          },
          "file": {
            "type": "string"
          },
          "line_start": {
            "type": "integer",
            "minimum": 1
          },
          "line_end": {
            "type": "integer",
            "minimum": 1
          },
          "dimension": {
            "$ref": "#/$defs/Dimension"
          },
          "severity": {
            "$ref": "#/$defs/Severity"
          },
          "summary": {
            "type": "string"
          },
          "trigger": {
            "type": [
              "string",
              "null"
            ]
          },
          "wrong_output": {
            "type": [
              "string",
              "null"
            ]
          },
          "fix": {
            "type": "string"
          },
          "evidence": {
            "type": "string"
          }
        },
        "additionalProperties": false
      },
      "CheckedItem": {
        "description": "A location examined and found correct for one dimension. line_end >= line_start is checked by panel.py.",
        "type": "object",
        "required": [
          "file",
          "line_start",
          "line_end",
          "dimension",
          "note"
        ],
        "properties": {
          "file": {
            "type": "string"
          },
          "line_start": {
            "type": "integer",
            "minimum": 1
          },
          "line_end": {
            "type": "integer",
            "minimum": 1
          },
          "dimension": {
            "$ref": "#/$defs/Dimension"
          },
          "note": {
            "type": "string"
          }
        },
        "additionalProperties": false
      }
    }
  },
  "debate-positions": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "sci-review/schemas/debate-positions.schema.json",
    "title": "Debate positions",
    "description": "Positions of one panel member in one debate round, one entry per finding in the batch. Position ids are of the form <member>:<finding_id>:<round>. Semantic check in panel.py: withdraw only from a member listed in the finding's raised_by.",
    "type": "object",
    "required": [
      "member",
      "round",
      "positions"
    ],
    "properties": {
      "member": {
        "type": "string",
        "pattern": "^[a-z0-9][a-z0-9-]*$"
      },
      "round": {
        "type": "integer",
        "minimum": 0
      },
      "positions": {
        "type": "array",
        "items": {
          "$ref": "#/$defs/Position"
        }
      }
    },
    "additionalProperties": false,
    "$defs": {
      "Position": {
        "type": "object",
        "required": [
          "finding_id",
          "member",
          "round",
          "stance",
          "reason",
          "answers"
        ],
        "properties": {
          "finding_id": {
            "type": "string",
            "pattern": "^F[0-9]+$"
          },
          "member": {
            "type": "string",
            "pattern": "^[a-z0-9][a-z0-9-]*$"
          },
          "round": {
            "type": "integer",
            "minimum": 0
          },
          "stance": {
            "type": "string",
            "enum": [
              "accept",
              "challenge",
              "withdraw"
            ]
          },
          "reason": {
            "type": "string",
            "minLength": 1
          },
          "answers": {
            "description": "Ids of earlier positions this one responds to, each of the form <member>:<finding_id>:<round>.",
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "additionalProperties": false
      }
    }
  },
  "merge-ruling": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "sci-review/schemas/merge-ruling.schema.json",
    "title": "Merge ruling",
    "description": "Moderator ruling for one batch: clusters of candidate findings confirmed as one defect, and clusters split apart. Semantic check in panel.py: severity_reason is present when severity is lower than the highest member severity; line_end >= line_start.",
    "type": "object",
    "required": [
      "batch",
      "findings",
      "split"
    ],
    "properties": {
      "batch": {
        "type": "integer",
        "minimum": 1
      },
      "findings": {
        "type": "array",
        "items": {
          "$ref": "#/$defs/MergedFinding"
        }
      },
      "split": {
        "type": "array",
        "items": {
          "type": "object",
          "required": [
            "cluster",
            "reason"
          ],
          "properties": {
            "cluster": {
              "type": "string"
            },
            "reason": {
              "type": "string"
            }
          },
          "additionalProperties": false
        }
      }
    },
    "additionalProperties": false,
    "$defs": {
      "Dimension": {
        "type": "string",
        "enum": [
          "mathematical-derivations",
          "numerical-stability",
          "physical-modelling-and-units",
          "statistical-integrity",
          "algorithmic-correctness"
        ]
      },
      "Severity": {
        "type": "string",
        "enum": [
          "high",
          "medium",
          "low"
        ]
      },
      "MergedFinding": {
        "description": "A cluster of candidate findings with representative fields chosen by the moderator.",
        "type": "object",
        "required": [
          "id",
          "members",
          "raised_by",
          "batch",
          "file",
          "line_start",
          "line_end",
          "dimension",
          "severity",
          "summary",
          "trigger",
          "wrong_output",
          "fix"
        ],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^F[0-9]+$"
          },
          "members": {
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^[a-z0-9-]+-[0-9]+$"
            },
            "minItems": 1
          },
          "raised_by": {
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^[a-z0-9][a-z0-9-]*$"
            },
            "minItems": 1
          },
          "batch": {
            "type": "integer",
            "minimum": 1
          },
          "file": {
            "type": "string"
          },
          "line_start": {
            "type": "integer",
            "minimum": 1
          },
          "line_end": {
            "type": "integer",
            "minimum": 1
          },
          "dimension": {
            "$ref": "#/$defs/Dimension"
          },
          "severity": {
            "$ref": "#/$defs/Severity"
          },
          "summary": {
            "type": "string"
          },
          "trigger": {
            "type": [
              "string",
              "null"
            ]
          },
          "wrong_output": {
            "type": [
              "string",
              "null"
            ]
          },
          "fix": {
            "type": "string"
          },
          "severity_reason": {
            "type": "string"
          }
        },
        "additionalProperties": false
      }
    }
  },
  "moderator-notes": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "sci-review/schemas/moderator-notes.schema.json",
    "title": "Moderator notes",
    "description": "Moderator notes for every merged finding of one batch, written after its debate and without knowledge of labels. Semantic check in panel.py: no_trigger_reason is non-null when the merged finding's trigger or wrong_output is null.",
    "type": "object",
    "required": [
      "batch",
      "notes"
    ],
    "properties": {
      "batch": {
        "type": "integer",
        "minimum": 1
      },
      "notes": {
        "type": "array",
        "items": {
          "$ref": "#/$defs/ModeratorNote"
        }
      }
    },
    "additionalProperties": false,
    "$defs": {
      "ModeratorNote": {
        "type": "object",
        "required": [
          "finding_id",
          "argument_for",
          "argument_against",
          "deciding_assumption",
          "rejection_reason",
          "no_trigger_reason"
        ],
        "properties": {
          "finding_id": {
            "type": "string",
            "pattern": "^F[0-9]+$"
          },
          "argument_for": {
            "type": "string",
            "minLength": 1
          },
          "argument_against": {
            "type": "string",
            "minLength": 1
          },
          "deciding_assumption": {
            "type": [
              "string",
              "null"
            ]
          },
          "rejection_reason": {
            "type": "string",
            "minLength": 1
          },
          "no_trigger_reason": {
            "type": [
              "string",
              "null"
            ]
          }
        },
        "additionalProperties": false
      }
    }
  },
  "report": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "sci-review/schemas/report.schema.json",
    "title": "Review report",
    "description": "ReviewReport produced by panel.py report. Semantic checks in panel.py: no_trigger_reason is present and non-null when trigger or wrong_output is null; line_end >= line_start; findings are ordered by label then severity. findings holds the delivered findings only, at most max_findings of them; withheld counts the rest.",
    "type": "object",
    "required": [
      "scope",
      "panel",
      "extensions",
      "findings",
      "rejected",
      "checked_items",
      "unreviewed",
      "notices",
      "level",
      "level_source",
      "max_findings",
      "withheld",
      "parts",
      "incomplete_parts",
      "notes"
    ],
    "properties": {
      "scope": {
        "$ref": "#/$defs/ReviewScope"
      },
      "panel": {
        "$ref": "#/$defs/Panel"
      },
      "extensions": {
        "type": "array",
        "items": {
          "$ref": "#/$defs/Extension"
        }
      },
      "findings": {
        "type": "array",
        "items": {
          "$ref": "#/$defs/Finding"
        }
      },
      "rejected": {
        "type": "array",
        "items": {
          "$ref": "#/$defs/RejectedFinding"
        }
      },
      "checked_items": {
        "type": "array",
        "items": {
          "$ref": "#/$defs/CheckedItem"
        }
      },
      "unreviewed": {
        "type": "array",
        "items": {
          "$ref": "#/$defs/Exclusion"
        }
      },
      "notices": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "level": {
        "$ref": "#/$defs/Level"
      },
      "level_source": {
        "$ref": "#/$defs/Source"
      },
      "max_findings": {
        "description": "The finding cap applied: a whole number, \"all\", or null for the level's default (no limit).",
        "type": [
          "integer",
          "string",
          "null"
        ]
      },
      "withheld": {
        "description": "Adjudicated findings not delivered because of the cap; they remain in adjudication.json.",
        "type": "integer",
        "minimum": 0
      },
      "parts": {
        "description": "Number of review parts.",
        "type": "integer",
        "minimum": 0
      },
      "incomplete_parts": {
        "description": "Ids of review parts whose independent round did not complete; listed under unreviewed.",
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "notes": {
        "description": "One-line notes about the arguments (from arguments.json).",
        "type": "array",
        "items": {
          "type": "string"
        }
      }
    },
    "additionalProperties": false,
    "$defs": {
      "Dimension": {
        "type": "string",
        "enum": [
          "mathematical-derivations",
          "numerical-stability",
          "physical-modelling-and-units",
          "statistical-integrity",
          "algorithmic-correctness"
        ]
      },
      "Severity": {
        "type": "string",
        "enum": [
          "high",
          "medium",
          "low"
        ]
      },
      "Exclusion": {
        "type": "object",
        "required": [
          "path",
          "reason"
        ],
        "properties": {
          "path": {
            "type": "string"
          },
          "reason": {
            "type": "string"
          }
        },
        "additionalProperties": false
      },
      "ScopedFile": {
        "type": "object",
        "required": [
          "path",
          "language",
          "line_ranges"
        ],
        "properties": {
          "path": {
            "type": "string"
          },
          "language": {
            "type": "string",
            "enum": [
              "python",
              "typescript",
              "other"
            ]
          },
          "line_ranges": {
            "description": "List of [start, end] pairs. Empty in repository mode, meaning the whole file.",
            "type": "array",
            "items": {
              "type": "array",
              "items": {
                "type": "integer",
                "minimum": 1
              },
              "minItems": 2
            }
          }
        },
        "additionalProperties": false
      },
      "ReviewScope": {
        "type": "object",
        "required": [
          "mode",
          "base",
          "head",
          "files",
          "excluded",
          "note"
        ],
        "properties": {
          "mode": {
            "type": "string",
            "enum": [
              "branch",
              "explicit",
              "repository",
              "paths"
            ]
          },
          "base": {
            "type": [
              "string",
              "null"
            ]
          },
          "head": {
            "type": [
              "string",
              "null"
            ]
          },
          "files": {
            "type": "array",
            "items": {
              "$ref": "#/$defs/ScopedFile"
            }
          },
          "excluded": {
            "type": "array",
            "items": {
              "$ref": "#/$defs/Exclusion"
            }
          },
          "note": {
            "type": "string"
          },
          "target": {
            "description": "The resolved target, or null when none was given.",
            "type": [
              "object",
              "null"
            ]
          },
          "total_lines": {
            "type": "integer",
            "minimum": 0
          },
          "pull_request_ref": {
            "description": "Temporary git ref of a fetched pull request head, deleted by panel.py clean.",
            "type": [
              "string",
              "null"
            ]
          }
        },
        "additionalProperties": false,
        "allOf": [
          {
            "if": {
              "properties": {
                "target": {
                  "type": "object"
                }
              },
              "required": [
                "target"
              ]
            },
            "then": {
              "properties": {
                "target": {
                  "$ref": "#/$defs/Target"
                }
              }
            }
          }
        ]
      },
      "Perspective": {
        "type": "object",
        "required": [
          "id",
          "name",
          "brief_path",
          "source",
          "reference_paths"
        ],
        "properties": {
          "id": {
            "type": "string"
          },
          "name": {
            "type": "string"
          },
          "brief_path": {
            "type": "string"
          },
          "source": {
            "type": "string"
          },
          "reference_paths": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "additionalProperties": false
      },
      "ModelAssignment": {
        "type": "object",
        "required": [
          "role",
          "model"
        ],
        "properties": {
          "role": {
            "type": "string"
          },
          "model": {
            "type": "string"
          }
        },
        "additionalProperties": false
      },
      "Panel": {
        "type": "object",
        "required": [
          "perspectives",
          "rebuttal_rounds",
          "max_batches",
          "runner",
          "independent"
        ],
        "properties": {
          "perspectives": {
            "type": "array",
            "items": {
              "$ref": "#/$defs/Perspective"
            }
          },
          "rebuttal_rounds": {
            "type": "integer",
            "minimum": 0
          },
          "max_batches": {
            "type": "integer",
            "minimum": 1
          },
          "runner": {
            "type": "string",
            "enum": [
              "claude-workflow",
              "codex-subagents",
              "claude-agents",
              "sequential"
            ]
          },
          "independent": {
            "type": "boolean"
          },
          "models": {
            "description": "Optional model per role id (Workflow runner only), as a list of role and model pairs.",
            "type": "array",
            "items": {
              "$ref": "#/$defs/ModelAssignment"
            }
          },
          "level": {
            "$ref": "#/$defs/Level"
          },
          "level_source": {
            "$ref": "#/$defs/Source"
          },
          "overrides": {
            "description": "Level-profile parameters overridden by explicit options (perspectives, rounds, batches).",
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "perspectives",
                "rounds",
                "batches"
              ]
            }
          },
          "parts": {
            "type": "integer",
            "minimum": 0
          }
        },
        "additionalProperties": false
      },
      "Extension": {
        "type": "object",
        "required": [
          "id",
          "plugin",
          "contract_version",
          "perspective_id",
          "status",
          "status_reason",
          "adds"
        ],
        "properties": {
          "id": {
            "type": "string"
          },
          "plugin": {
            "type": "string"
          },
          "contract_version": {
            "type": "integer"
          },
          "perspective_id": {
            "type": [
              "string",
              "null"
            ]
          },
          "status": {
            "type": "string",
            "enum": [
              "selected",
              "not-applicable",
              "failed",
              "recommended"
            ]
          },
          "status_reason": {
            "type": [
              "string",
              "null"
            ]
          },
          "adds": {
            "type": [
              "string",
              "null"
            ]
          }
        },
        "additionalProperties": false,
        "allOf": [
          {
            "if": {
              "properties": {
                "status": {
                  "enum": [
                    "not-applicable",
                    "failed",
                    "recommended"
                  ]
                }
              },
              "required": [
                "status"
              ]
            },
            "then": {
              "required": [
                "status_reason"
              ],
              "properties": {
                "status_reason": {
                  "type": "string",
                  "minLength": 1
                }
              }
            }
          }
        ]
      },
      "Finding": {
        "description": "A reported finding. argument_for, argument_against and deciding_assumption are required for contested findings. trigger and wrong_output are non-null for consensus and majority findings.",
        "type": "object",
        "required": [
          "id",
          "members",
          "raised_by",
          "batch",
          "file",
          "line_start",
          "line_end",
          "dimension",
          "severity",
          "summary",
          "trigger",
          "wrong_output",
          "fix",
          "label"
        ],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^F[0-9]+$"
          },
          "members": {
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^[a-z0-9-]+-[0-9]+$"
            },
            "minItems": 1
          },
          "raised_by": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "minItems": 1
          },
          "batch": {
            "type": "integer"
          },
          "file": {
            "type": "string"
          },
          "line_start": {
            "type": "integer",
            "minimum": 1
          },
          "line_end": {
            "type": "integer",
            "minimum": 1
          },
          "dimension": {
            "$ref": "#/$defs/Dimension"
          },
          "severity": {
            "$ref": "#/$defs/Severity"
          },
          "summary": {
            "type": "string"
          },
          "trigger": {
            "type": [
              "string",
              "null"
            ]
          },
          "wrong_output": {
            "type": [
              "string",
              "null"
            ]
          },
          "fix": {
            "type": "string"
          },
          "severity_reason": {
            "type": "string"
          },
          "label": {
            "type": "string",
            "enum": [
              "consensus",
              "majority",
              "contested"
            ]
          },
          "argument_for": {
            "type": "string"
          },
          "argument_against": {
            "type": "string"
          },
          "deciding_assumption": {
            "type": [
              "string",
              "null"
            ]
          },
          "no_trigger_reason": {
            "type": [
              "string",
              "null"
            ]
          }
        },
        "additionalProperties": false,
        "allOf": [
          {
            "if": {
              "properties": {
                "label": {
                  "const": "contested"
                }
              },
              "required": [
                "label"
              ]
            },
            "then": {
              "required": [
                "argument_for",
                "argument_against",
                "deciding_assumption"
              ],
              "properties": {
                "argument_for": {
                  "type": "string",
                  "minLength": 1
                },
                "argument_against": {
                  "type": "string",
                  "minLength": 1
                }
              }
            }
          },
          {
            "if": {
              "properties": {
                "label": {
                  "enum": [
                    "consensus",
                    "majority"
                  ]
                }
              },
              "required": [
                "label"
              ]
            },
            "then": {
              "required": [
                "trigger",
                "wrong_output"
              ],
              "properties": {
                "trigger": {
                  "type": "string"
                },
                "wrong_output": {
                  "type": "string"
                }
              }
            }
          }
        ]
      },
      "RejectedFinding": {
        "type": "object",
        "required": [
          "finding_id",
          "summary",
          "raised_by",
          "reason"
        ],
        "properties": {
          "finding_id": {
            "type": "string",
            "pattern": "^F[0-9]+$"
          },
          "summary": {
            "type": "string"
          },
          "raised_by": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "reason": {
            "type": "string"
          }
        },
        "additionalProperties": false
      },
      "CheckedItem": {
        "description": "A location examined and found correct for one dimension. line_end >= line_start is checked by panel.py.",
        "type": "object",
        "required": [
          "file",
          "line_start",
          "line_end",
          "dimension",
          "note"
        ],
        "properties": {
          "file": {
            "type": "string"
          },
          "line_start": {
            "type": "integer",
            "minimum": 1
          },
          "line_end": {
            "type": "integer",
            "minimum": 1
          },
          "dimension": {
            "$ref": "#/$defs/Dimension"
          },
          "note": {
            "type": "string"
          }
        },
        "additionalProperties": false
      },
      "Level": {
        "type": "string",
        "enum": [
          "low",
          "medium",
          "high",
          "xhigh",
          "max"
        ]
      },
      "Source": {
        "type": "string",
        "enum": [
          "given",
          "reused",
          "default"
        ]
      },
      "Target": {
        "type": "object",
        "required": [
          "kind",
          "host",
          "number",
          "ref",
          "paths",
          "text"
        ],
        "properties": {
          "kind": {
            "type": "string",
            "enum": [
              "pull-request",
              "branch",
              "paths"
            ]
          },
          "host": {
            "type": [
              "string",
              "null"
            ],
            "enum": [
              "github",
              "gitlab",
              null
            ]
          },
          "number": {
            "type": [
              "integer",
              "null"
            ]
          },
          "ref": {
            "type": [
              "string",
              "null"
            ]
          },
          "paths": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "text": {
            "type": "string"
          }
        },
        "additionalProperties": false
      }
    }
  },
}
// END GENERATED

// ---------------------------------------------------------------------------
// The PURE section mirrors panel.py (cluster_candidates, batch_clusters,
// changed_members, members_to_call, debate_stopped) and protocol.md sections 7
// and 8. It uses
// no Workflow globals, so tests/test_sci_review_workflow_build.py runs it under
// Node.js on the same fixtures as panel.py.
// ---------------------------------------------------------------------------

// BEGIN PURE
const CLUSTER_DISTANCE = 3
const SPLIT_ID_BLOCK = 1000

function compareStrings(a, b) {
  return a < b ? -1 : a > b ? 1 : 0
}

function clusterCandidates(candidates) {
  const byFile = new Map()
  for (const candidate of candidates) {
    if (!byFile.has(candidate.file)) byFile.set(candidate.file, [])
    byFile.get(candidate.file).push(candidate)
  }
  const clusters = []
  for (const file of [...byFile.keys()].sort(compareStrings)) {
    const ordered = byFile.get(file).slice().sort((a, b) =>
      a.line_start - b.line_start || a.line_end - b.line_end || compareStrings(a.id, b.id))
    const groups = []
    let maxEnd = 0
    for (const candidate of ordered) {
      if (groups.length && candidate.line_start <= maxEnd + CLUSTER_DISTANCE) {
        groups[groups.length - 1].push(candidate)
        maxEnd = Math.max(maxEnd, candidate.line_end)
      } else {
        groups.push([candidate])
        maxEnd = candidate.line_end
      }
    }
    for (const group of groups) {
      const n = clusters.length + 1
      clusters.push({
        id: `C${n}`,
        suggested_finding_id: `F${n}`,
        file,
        line_start: Math.min(...group.map(c => c.line_start)),
        line_end: Math.max(...group.map(c => c.line_end)),
        members: group.map(c => c.id),
      })
    }
  }
  return clusters
}

function batchClusters(clusters, maxBatches) {
  const byFile = new Map()
  for (const cluster of clusters) {
    if (!byFile.has(cluster.file)) byFile.set(cluster.file, [])
    byFile.get(cluster.file).push(cluster.id)
  }
  const slots = Array.from({ length: Math.max(1, maxBatches) }, () => [])
  const files = [...byFile.keys()].sort((a, b) => byFile.get(b).length - byFile.get(a).length || compareStrings(a, b))
  for (const file of files) {
    let target = 0
    for (let i = 1; i < slots.length; i++) {
      if (slots[i].length < slots[target].length) target = i
    }
    slots[target].push(...byFile.get(file))
  }
  const order = new Map(clusters.map((cluster, index) => [cluster.id, index]))
  return slots
    .filter(slot => slot.length)
    .map((slot, index) => ({ batch: index + 1, clusters: slot.slice().sort((a, b) => order.get(a) - order.get(b)) }))
}

function carriedStances(rounds, upto) {
  const stances = new Map()
  for (const positions of rounds.slice(0, upto + 1)) {
    for (const position of positions) stances.set(`${position.member}\u0000${position.finding_id}`, position.stance)
  }
  return stances
}

function changedMembers(rounds, k) {
  const before = carriedStances(rounds, k - 1)
  const after = carriedStances(rounds, k)
  const changed = new Set()
  for (const [key, stance] of after) {
    if (before.get(key) !== stance) changed.add(key.split('\u0000')[0])
  }
  return [...changed].sort(compareStrings)
}

function membersToCall(rounds, k) {
  const before = carriedStances(rounds, k - 1)
  const after = carriedStances(rounds, k)
  const changed = []
  for (const [key, stance] of after) {
    if (before.get(key) !== stance) changed.push(key)
  }
  const challenged = new Set(changed.filter(key => after.get(key) === 'challenge').map(key => key.split('\u0000')[1]))
  const call = new Set(changed.map(key => key.split('\u0000')[0]))
  for (const [key, stance] of after) {
    const [member, finding] = key.split('\u0000')
    if (challenged.has(finding) && stance === 'accept' && member !== 'defender') call.add(member)
  }
  return [...call].sort(compareStrings)
}

function debateStopped(rounds, k) {
  return k >= 1 && changedMembers(rounds, k).length === 0
}

function splitFindingId(batch, n) {
  return `F${SPLIT_ID_BLOCK * batch + n}`
}
// END PURE

// ---------------------------------------------------------------------------
// Arguments (contracts/invocation.md section 4)
// ---------------------------------------------------------------------------

const DEFAULT_PERSPECTIVES = ['theorist', 'numerical-analyst', 'experimentalist', 'methodologist', 'computer-scientist']
const PERSPECTIVE_NAMES = {
  theorist: 'Theorist',
  'numerical-analyst': 'Numerical analyst',
  experimentalist: 'Experimentalist',
  methodologist: 'Methodologist',
  'computer-scientist': 'Computer scientist',
}

function clamp(value, low, high, fallback) {
  const n = Number.isInteger(value) ? value : fallback
  return Math.max(low, Math.min(high, n))
}

const input = (args && typeof args === 'object') ? args : {}
const scope = input.scope || { files: [], note: 'No scope was given.' }
const skillDir = typeof input.skill_dir === 'string' && input.skill_dir ? input.skill_dir : null
// Scope paths are relative to the project root; agents start in the session's working directory, which may differ.
const project = typeof input.project === 'string' && input.project ? input.project : null
// Review parts of parts.json (feature 008); a run without them reviews the whole scope as one part.
// The whole content of parts.json ({ parts: [...] }) is accepted as well as its array. When no valid part remains,
// the whole scope is reviewed as one part, so that a malformed input never skips the independent round.
const givenParts = Array.isArray(input.parts) ? input.parts
  : (input.parts && Array.isArray(input.parts.parts) ? input.parts.parts : [])
const validParts = givenParts.filter(part => part && typeof part.id === 'string' && Array.isArray(part.files))
const parts = validParts.length ? validParts : [{ id: 'p1', files: scope.files || [], lines: null }]
const multiPart = parts.length > 1
const rebuttalRounds = clamp(input.rebuttal_rounds, 0, 3, 2)
const maxBatches = clamp(input.max_batches, 1, 4, 2)
const models = (input.models && typeof input.models === 'object' && !Array.isArray(input.models))
  ? input.models
  : Object.fromEntries((Array.isArray(input.models) ? input.models : []).map(m => [m.role, m.model]))

const extensionPerspectives = new Map()
for (const extension of Array.isArray(input.extensions) ? input.extensions : []) {
  const p = extension && extension.perspective
  if (p && p.id) extensionPerspectives.set(p.id, { ...p, source: p.source || extension.id })
}

// A perspective is given as an id or as {id, name, brief_path, reference_paths, source} from panel.json.
const members = []
const requested = Array.isArray(input.perspectives) && input.perspectives.length
  ? input.perspectives
  : [...DEFAULT_PERSPECTIVES, ...extensionPerspectives.keys()]
for (const entry of requested) {
  const id = typeof entry === 'string' ? entry : entry && entry.id
  if (!id || members.some(m => m.id === id)) continue
  const given = typeof entry === 'object' ? entry : (extensionPerspectives.get(id) || {})
  if (ROLES[id]) {
    members.push({ id, name: PERSPECTIVE_NAMES[id] || id, brief: ROLES[id], briefPath: null, references: [] })
  } else if (given.brief_path) {
    members.push({
      id,
      name: given.name || id,
      brief: null,
      briefPath: given.brief_path,
      references: Array.isArray(given.reference_paths) ? given.reference_paths : [],
    })
  } else {
    log(`Perspective ${id} has no brief and was left out.`)
  }
}
if (members.length > 7) {
  log(`The panel was limited to 7 perspectives; ${members.slice(7).map(m => m.id).join(', ')} did not take part.`)
  members.length = 7
}
// As panel.py panel does: a panel below the minimum is raised to two perspectives, taking the defaults and then
// the selected extensions' perspectives in order (contracts/invocation.md section 2).
if (members.length < 2) {
  const available = [...DEFAULT_PERSPECTIVES, ...extensionPerspectives.keys()]
  for (const id of available) {
    if (members.length >= 2) break
    if (members.some(m => m.id === id)) continue
    if (ROLES[id]) {
      members.push({ id, name: PERSPECTIVE_NAMES[id] || id, brief: ROLES[id], briefPath: null, references: [] })
    } else {
      const given = extensionPerspectives.get(id)
      if (!given || !given.brief_path) continue
      const references = Array.isArray(given.reference_paths) ? given.reference_paths : []
      members.push({ id, name: given.name || id, brief: null, briefPath: given.brief_path, references })
    }
  }
  log('The panel was raised to the minimum of 2 perspectives.')
}

const SCHEMA_KEYS_DROPPED = new Set(['$schema', '$id'])
function workflowSchema(name) {
  return Object.fromEntries(Object.entries(SCHEMAS[name]).filter(([key]) => !SCHEMA_KEYS_DROPPED.has(key)))
}

// panel.py rejects a whole message when one location has line_end < line_start; swap such a pair here, so that
// one slip in a model's output does not discard every finding of a perspective or of a batch.
function normaliseRanges(items) {
  for (const item of items || []) {
    if (Number.isInteger(item.line_start) && Number.isInteger(item.line_end) && item.line_end < item.line_start) {
      const start = item.line_end
      item.line_end = item.line_start
      item.line_start = start
    }
  }
}

function modelFor(role) {
  return typeof models[role] === 'string' && models[role] ? { model: models[role] } : {}
}

function fence(label, value) {
  const text = typeof value === 'string' ? value : JSON.stringify(value, null, 2)
  return `<${label}>\n${text}\n</${label}>`
}

const PROJECT_RULE = project
  ? `- The reviewed project is ${project}. Every path in the scope, and every \`file\` you report, is relative to it: read ${project}/<path>, but report <path>.\n`
  : ''
// A branch or pull request target is not checked out: its files are read from the git ref recorded as the head.
const fromRef = scope.target && (scope.target.kind === 'branch' || scope.target.kind === 'pull-request') && scope.head
const REF_RULE = fromRef
  ? `- The reviewed files are not in the working tree: read each one with \`git ${project ? `-C ${project} ` : ''}show ${scope.head}:<path>\`.\n`
  : ''
const COMMON_RULES = `Rules for every panel member:
${PROJECT_RULE}${REF_RULE}- Read the project's files freely to verify claims, but never create, modify or delete any file, and run no command that writes anywhere. Run Python with \`python3 -B\`, so that importing a project module writes no \`__pycache__\` in the project.
- Use only the inputs given below for this phase; you have no other panel member's output except where it is given.
- Your final answer is the structured output only.`

function briefBlock(member) {
  if (member.brief) return fence('role-brief', member.brief)
  return `Your role brief is the file ${member.briefPath}. Read it first and adopt it.`
}

function dimensionBlock() {
  if (skillDir) {
    return `The five dimension documents are in ${skillDir}/dimensions/ (mathematical-derivations.md, numerical-stability.md, physical-modelling-and-units.md, statistical-integrity.md, algorithmic-correctness.md). Read each one when you review that dimension.`
  }
  return Object.entries(DIMENSIONS).map(([name, text]) => fence(`dimension name="${name}"`, text)).join('\n\n')
}

function independentPrompt(member, part) {
  const references = member.references.length
    ? `Your reference material, to read before reviewing: ${member.references.join(', ')}.`
    : ''
  const partRule = multiPart
    ? `The scope is divided into ${parts.length} review parts; you review part \`${part.id}\` only. Review every line of it. You may read any file of the project, inside or outside the scope, to follow a reference, but raise findings only on lines of your part.`
    : 'Review every file and line range of the scope.'
  const ids = multiPart ? `\`${member.id}-${part.id}-1\`, \`${member.id}-${part.id}-2\`` : `\`${member.id}-1\`, \`${member.id}-2\``
  return `You are the ${member.name} (perspective id \`${member.id}\`) on a scientific-correctness review panel. This is the INDEPENDENT ROUND.

${COMMON_RULES}

${briefBlock(member)}

${fence('protocol', PROTOCOL)}

${dimensionBlock()}

${references}

${fence('scope', scope)}

${multiPart ? fence(`review-part id="${part.id}"`, part) : ''}

${partRule} Review across all five dimensions. Set \`perspective\` to \`${member.id}\` and \`part\` to \`${part.id}\`, give findings ids ${ids}, ..., and set each finding's \`raised_by\` to \`${member.id}\`. Record checked items. Return one candidate-findings message.`
}

function mergePrompt(batch, clusters, candidateMessages) {
  return `You are the moderator of a scientific-correctness review panel. Perform the MERGE TASK for debate batch ${batch.batch}.

${COMMON_RULES}

${fence('role-brief', ROLES.moderator)}

${fence('candidates', candidateMessages)}

${fence('clusters', { batch: batch.batch, clusters, next_finding_id: splitFindingId(batch.batch, 1) })}

Merge only the clusters listed above. Set \`batch\` to ${batch.batch} in the message and in every merged finding. Return one merge-ruling message.`
}

function positionsDigest(rounds) {
  return rounds.map((positions, k) => ({ round: k, positions }))
}

function debatePrompt(memberId, ruling, rounds, k, ownCandidates) {
  const member = members.find(m => m.id === memberId)
  const isDefender = memberId === 'defender'
  const brief = isDefender ? fence('role-brief', ROLES.defender) : briefBlock(member)
  const history = k === 0
    ? (isDefender ? '' : fence('your-independent-output', ownCandidates || { findings: [] }))
    : fence('earlier-positions', positionsDigest(rounds))
  return `You are ${isDefender ? 'the defender' : `the ${member.name} (perspective id \`${memberId}\`)`} on a scientific-correctness review panel. This is DEBATE ROUND ${k} of batch ${ruling.batch}${k === 0 ? ' (initial positions)' : ` (rebuttal round ${k} of ${rebuttalRounds})`}.

${COMMON_RULES}

${brief}

${fence('merged-findings', ruling.findings)}

${history}

State one position on every merged finding above. Set \`member\` to \`${memberId}\` and \`round\` to ${k} in the message and in every position. Position ids are \`<member>:<finding_id>:<round>\`; list in \`answers\` the ids of the earlier positions you respond to. ${isDefender ? 'Never use withdraw.' : 'Use withdraw only for a finding whose raised_by lists you.'} Return one debate-positions message.`
}

function notesPrompt(ruling, rounds) {
  return `You are the moderator of a scientific-correctness review panel. Perform the NOTES TASK for debate batch ${ruling.batch}. Labels are computed afterwards by a script; you do not know them.

${COMMON_RULES}

${fence('role-brief', ROLES.moderator)}

${fence('merged-findings', ruling.findings)}

${fence('positions', positionsDigest(rounds))}

Write one note for every merged finding above. Set \`batch\` to ${ruling.batch}. Return one moderator-notes message.`
}

// ---------------------------------------------------------------------------
// Run
// ---------------------------------------------------------------------------

const run = { candidates: [], merge: [], debate: [], notes: [], dropped: [] }

if (!(scope.files && scope.files.length)) {
  log('No reviewable scientific code in this scope; nothing to review.')
  return run
}
if (members.length < 2) {
  log('Fewer than two perspectives are available; the review cannot run.')
  return run
}

log(`Panel: ${members.map(m => m.id).join(', ')}, defender, moderator; ${rebuttalRounds} rebuttal rounds; at most ${maxBatches} batches; ${parts.length} review part(s).`)
if (givenParts.length && !validParts.length) log('The review parts given were not valid; the whole scope is reviewed as one part.')

// Independent round: every perspective reviews every part (protocol.md section 2). A failed agent writes nothing,
// so panel.py report derives that part as incomplete; no part status is written here.
phase('Independent')
const pairs = members.flatMap(member => parts.map(part => ({ member, part })))
const independent = await parallel(pairs.map(({ member, part }) => () =>
  agent(independentPrompt(member, part), {
    phase: 'Independent',
    label: `independent:${member.id}:${part.id}`,
    schema: workflowSchema('candidate-findings'),
    ...modelFor(member.id),
  })))

// A perspective's own output for debate round 0 is the union of its messages over every part.
const candidatesBy = new Map()
independent.forEach((message, index) => {
  const { member, part } = pairs[index]
  if (!message) {
    run.dropped.push(`${member.id} candidates (part ${part.id})`)
    return
  }
  message.perspective = member.id
  message.part = part.id
  ;(message.findings || []).forEach((finding, n) => {
    finding.raised_by = member.id
    // Ids must be unique across parts, as panel.py merge requires.
    if (multiPart) finding.id = `${member.id}-${part.id}-${n + 1}`
  })
  normaliseRanges(message.findings)
  normaliseRanges(message.checked_items)
  const own = candidatesBy.get(member.id) || { perspective: member.id, findings: [], checked_items: [], notes: '' }
  own.findings = own.findings.concat(message.findings || [])
  own.checked_items = own.checked_items.concat(message.checked_items || [])
  own.notes = [own.notes, message.notes].filter(Boolean).join('\n')
  candidatesBy.set(member.id, own)
  run.candidates.push(message)
})

const allCandidates = run.candidates.flatMap(m => m.findings || [])
log(`${allCandidates.length} candidate finding(s) from ${run.candidates.length} perspective(s).`)
if (!allCandidates.length) return run

const clusters = clusterCandidates(allCandidates)
const batches = batchClusters(clusters, maxBatches)
log(`${clusters.length} location cluster(s) in ${batches.length} debate batch(es).`)

const debateMembers = [...members.map(m => m.id), 'defender']

await pipeline(
  batches,
  batch => agent(mergePrompt(batch, clusters.filter(c => batch.clusters.includes(c.id)), run.candidates), {
    phase: 'Merge',
    label: `merge:batch-${batch.batch}`,
    schema: workflowSchema('merge-ruling'),
    ...modelFor('moderator'),
  }),
  async (ruling, batch) => {
    if (!ruling) {
      run.dropped.push(`moderator merge (batch ${batch.batch})`)
      return null
    }
    ruling.batch = batch.batch
    for (const finding of ruling.findings || []) finding.batch = batch.batch
    normaliseRanges(ruling.findings)
    run.merge.push(ruling)
    if (!(ruling.findings && ruling.findings.length)) return null

    const rounds = []
    let callees = debateMembers.slice()
    for (let k = 0; k <= rebuttalRounds; k++) {
      const outputs = await parallel(callees.map(memberId => () =>
        agent(debatePrompt(memberId, ruling, rounds, k, candidatesBy.get(memberId)), {
          phase: 'Debate',
          label: `debate:batch-${batch.batch}:round-${k}:${memberId}`,
          schema: workflowSchema('debate-positions'),
          ...modelFor(memberId),
        })))
      const positions = []
      outputs.forEach((message, index) => {
        const memberId = callees[index]
        if (!message) {
          run.dropped.push(`${memberId} (batch ${batch.batch}, round ${k})`)
          return
        }
        message.member = memberId
        message.round = k
        for (const position of message.positions || []) {
          position.member = memberId
          position.round = k
        }
        positions.push(...(message.positions || []))
        run.debate.push({ batch: batch.batch, message })
      })
      rounds.push(positions)
      if (k >= 1) {
        if (debateStopped(rounds, k)) {
          log(`Batch ${batch.batch}: no stance changed in round ${k}; the debate stops.`)
          break
        }
        callees = membersToCall(rounds, k)
      }
    }

    const notes = await agent(notesPrompt(ruling, rounds), {
      phase: 'Notes',
      label: `notes:batch-${batch.batch}`,
      schema: workflowSchema('moderator-notes'),
      ...modelFor('moderator'),
    })
    if (!notes) {
      run.dropped.push(`moderator notes (batch ${batch.batch})`)
      return null
    }
    notes.batch = batch.batch
    run.notes.push(notes)
    return ruling.batch
  },
)

log(`Returned ${run.candidates.length} candidate, ${run.merge.length} merge, ${run.debate.length} debate and ${run.notes.length} notes message(s). Run panel.py ingest, adjudicate and report next.`)
return run
