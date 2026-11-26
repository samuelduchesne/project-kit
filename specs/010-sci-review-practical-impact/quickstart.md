# Quickstart: validating feature 010

Scenarios that prove the feature works. They refer to [data-model.md](./data-model.md) and the contracts rather than restating them. Results go in `validation.md`.

`P=plugins/sci-review/scripts/panel.py` throughout.

## Prerequisites

- This repository on the feature branch, with `python3` 3.10+ and `git`.
- For scenarios 5 and 6, a host with the `claude-workflow` runner (Claude Code with the Workflow tool), as in the validation of feature 009.
- For scenario 6, a private case file (below) and read access to the repository it names.

## 1. Unit tests (deterministic parts)

```bash
python3 -m unittest discover -s tests -p 'test_sci_review_*.py'
```

Expected:

- All existing tests pass. Golden reports change only by the new layout and fields (SC-007).
- The new `tests/test_sci_review_practical.py` covers the following:
  - validation rules 1 to 4 of data-model.md;
  - trigger-class combination and ties;
  - severity unchanged by every trigger class; the reproduction and extent chosen from the verdicts;
  - rule 2a (design question, marks counted as uncertain);
  - value corrections deduplicated;
  - the defender mark in the debate protocol;
  - old-run compatibility (a feature-009 `adjudication.json` renders);
  - `issue` against a fixture repository with a CODEOWNERS file, then without one (blame), then outside git (none);
  - `issue` exit codes 2 and 3, and `--dry-run` writing nothing.

## 2. Message validation

```bash
python3 $P validate --schema verification tests/fixtures/sci-review/messages/invalid/verification-unreachable-confirm.json   # exit 1
python3 $P validate --schema verification tests/fixtures/sci-review/messages/valid/verification-practical.json               # exit 0
```

## 3. Report layout on recorded messages

Ingest the golden messages of `tests/fixtures/sci-review/messages/golden/practical/`, then run `adjudicate` and `report --format markdown`. Expected:

- Every finding opens with its headline, context and "In practice".
- The fixture's release-only finding keeps its severity, with "trigger: release" beside it.
- The reproduced finding shows its extent table and its reproduction.
- The marked finding appears under "Design questions".

## 4. Issue rendering

```bash
python3 $P issue --run $RUN --finding F3 --dry-run
python3 $P issue --run $RUN --finding F3
```

Expected:

- The body follows contracts/issue.md, with its sections in that order.
- The file is at `$RUN/issues/F3.md`.
- `git status --porcelain` of the project is empty.

## 5. Practical fixture (live)

The fixture `tests/fixtures/sci-review/practical-repo/` (rebuilt in Phase 10, research R14) holds four cases beside correct look-alikes, with a JSON store on disk so that every case is reachable: a stored plan keyed without the search settings or code version, issued reports served whatever their schema, offer lots rounded after converting pounds to tonnes, and a docstring quoting a development setting that `.env` contradicts. See its `manifest.json`. Build it and run a `medium` review as in section 1 of `specs/009-sci-review-cost/validation.md`, five times.

Expected:

- `stored-plan` is reported, and its in-practice statement names a release of new code among its triggers and cites where the settings come from; every reproduced finding shows its code and output (SC-002).
- `issued-report` is under "Design questions" in at least 4 of 5 runs (SC-003).
- No report repeats `quoted-setting`'s docstring value as the configured one without a correction (SC-004).
- `pound-lots` is reported, and its in-practice statement (or the verifier's revision) names pounds or converted units in at least 4 of 5 runs; no finding cites a line beyond the end of its file (SC-008).

Then run the seeded fixture once at `medium`. Expected: 16 of 16, no look-alike, and 7 agents at most, as in feature 009 (SC-005).

## 6. Evaluation on the criticised module (downstream case)

A quick, single-case check that the feature fixes what the domain reviewer criticised. Research R12 gives the rationale and the rubric. The case belongs to a private project: keep the case file and every artifact naming that project outside this repository, for example in a session scratchpad.

### Case file (kept outside the repository)

```json
{
  "repository": "<clone URL>",
  "commit": "<sha the original review ran on>",
  "history_depth": 60,
  "path": "<module that holds the finding>",
  "baseline_issue": "<path to the filed issue body, verbatim>",
  "reviewer_comment": "<path to the domain reviewer's comment, verbatim>",
  "match": "<one sentence: function and subject of the finding>",
  "expected_trigger_class": "release",
  "value_checks": [{"quoted": "<wrong value in the baseline>", "file": "<file>", "actual": "<value there>"}],
  "expected_owners": ["<login>"],
  "not_owner_alone": ["<login of the algorithm's author>"]
}
```

`history_depth` must reach the commit that created the module, so that blame resolves to real authors. A case file may hold several cases as `{"cases": [...]}`, each with an `id`; run the scenario once per case. A case whose realistic trigger is a data condition can add `expected_framing`, one sentence naming the common condition the issue should lead with, which the judge checks under C2.

### Setup

```bash
CASE=<case file>; E=<scratch directory>
git clone --filter=blob:none "$(jq -r .repository $CASE)" $E/repo
git -C $E/repo fetch --depth="$(jq -r .history_depth $CASE)" origin "$(jq -r .commit $CASE)" || git -C $E/repo fetch --depth=200 origin
git -C $E/repo worktree add $E/reviewed "$(jq -r .commit $CASE)"
```

The worktree keeps the reviewed tree at the commit of the original review, and leaves any working clone untouched.

### Run

Run `/sci-review:scientific-review medium <path>` with `$E/reviewed` as the project, empty preferences, on the `claude-workflow` runner. Record the agents, subagent tokens and wall time, as in feature 009.

### Select the finding

In `report.json`, find the finding or design question described by `match`.

- If none matches, repeat the run once.
- If there is still no match, record a recall failure and stop: do not compare.

Render its issue:

```bash
python3 $P issue --run $RUN --finding <Fn>
```

### Compare

1. Copy the baseline to `$E/eval/baseline.md` and the treatment to `$E/eval/treatment.md`.
2. **Deterministic checks**, by the orchestrator, on the treatment, against the case file:
   - **C5**: no entry of `value_checks` appears with its `quoted` value, unless the corrected value accompanies it.
   - **C6**: the body includes a runnable reproduction or an extent table.
   - **C7**: the suggested owners include one of `expected_owners`, and are not `not_owner_alone` alone.
3. **Blind judgment**, by one separate agent. It receives:
   - the reviewer's comment, verbatim;
   - the rubric of research R12 (C1 to C7);
   - the two bodies in random order, labelled A and B, without saying which is which.

   It returns, for each body, pass or fail for C1 to C4 with a one-line reason, and an overall preference with one sentence. The orchestrator then reveals which body was which.
4. Record in `validation.md`, section "Downstream case", **anonymised**:
   - the C1 to C7 table for each body;
   - the judge's preference, paraphrased;
   - agents, tokens and wall time;
   - the number of other findings of the run by kind.

   Leave out the project name, people, paths, code and quotations. Keep the bodies and the judge's full output with the case file, outside this repository.

### Pass

The treatment passes C1 to C7, the judge prefers it, and the run started no more panel agents than its stated estimate.

### Clean up

```bash
python3 $P clean --run $RUN    # after copying issues/ to $E/eval
git -C $E/repo worktree remove $E/reviewed
```

Nothing is posted to the downstream project. Showing the treatment body to the domain reviewer, or replacing the filed issue with it, is an optional follow-up that needs the user's go-ahead.
