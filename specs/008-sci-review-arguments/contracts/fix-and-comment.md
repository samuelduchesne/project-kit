# Contract: `--comment` and `--fix` sections of SKILL.md

These sections reproduce `/code-review` as shipped in Claude Code 2.1.317 (research R1, R2). They are prompt text executed by the orchestrating conversation after the delivery step of `SKILL.md` section 7, in this order: post (`--comment`), then fix (`--fix`), then clean. No `panel.py` subcommand, runner or panel member performs them.

`<FR-TOOL>` below is `ReportFindings` where the host provides it. The text is reproduced verbatim except where marked **[adapted]**, each adaptation citing its reason.

## 1. Posting to GitHub (`--comment`)

Included when `arguments.json` has `comment: true` and the target host is not GitLab.

```text
## Posting to GitHub (--comment)
The `--comment` flag was passed. After producing the findings list, if the
review target is a GitHub PR, post each finding as an inline PR comment via
`mcp__github_inline_comment__create_inline_comment` (one call per finding;
include a suggestion block only when it fully fixes the issue). If that tool
is not available in this session, fall back to `gh api`
(repos/{owner}/{repo}/pulls/{pr}/comments) or print the findings instead. If
the target is not a PR, print the findings to the terminal and note that
`--comment` was ignored.
[adapted, spec FR-015] Each comment states the finding's agreement label,
severity and dimension, then the issue and the scenario. A finding that does
not anchor to a line of the PR diff is printed with a note, not posted.
[adapted, spec US5] Post nothing when the review has no findings.
```

## 2. Posting to GitLab (`--comment`)

Included when `comment: true` and the target host is GitLab.

```text
## Posting to GitLab (--comment)
The `--comment` flag was passed. After producing the findings list, if the
review target is a GitLab merge request, post the findings as one general MR
note via `glab mr note <iid> [-R <project>] -m "<body>"` (every finding with
its file:line, the issue, and the suggested fix). glab has no single verb for
line-anchored comments; those require
`glab api projects/:id/merge_requests/:iid/discussions`, so post the general
note unless the user asks for inline threads. If glab is not available in this
session, print the findings instead. If the target is not an MR, print the
findings to the terminal and note that `--comment` was ignored.
```

## 3. Applying fixes (`--fix`)

Included when `fix: true`. Two variants, selected by whether `<FR-TOOL>` is available.

```text
## Applying fixes (--fix)
The `--fix` flag was passed. After producing the findings list, apply the
findings to the working tree instead of stopping at the report: fix each one
directly [adapted, scientific review reports only scientific-correctness
findings: "every delivered finding"]. Skip any finding whose fix would change
intended behavior, require changes well outside the reviewed diff, or that you
judge to be a false positive; note the skip rather than arguing with it.
[adapted, spec FR-016b] Skipping a finding never changes its agreement label.
[adapted, spec FR-016c, from the /code-review ultra variant] Run the relevant
checks after.
<with FR-TOOL>    Then call <FR-TOOL> again with the same findings, each
                  carrying an `outcome`: `fixed`, `no_change_needed` (the
                  finding was wrong or already handled), or `skipped` (real
                  but not applied). Do not repeat the findings as text; after
                  the call, give one line per skipped finding saying why.
<without FR-TOOL> Finish with a brief summary of what was fixed and what was
                  skipped.
```

Constraints carried by `SKILL.md` around this section (spec FR-016, FR-016a, FR-016e):

1. Nothing is staged or committed.
2. The section runs only after the findings are reported; the project check of `SKILL.md` section 7 step 3 runs before it, so that any change it reports was made by the panel, not by the fix step.
3. Only delivered findings (after `--max-findings`) are considered.
4. Without `--fix`, this section is absent and the review is read-only.
5. No clean-working-tree check is made, as in `/code-review`: passing `--fix` is the user's explicit acceptance of the risk of writing to a tree with uncommitted changes (constitution 1.3.0, Principle III exception).

## 4. If findings are fixed later

Included whenever `<FR-TOOL>` is available, with or without `--fix` (spec FR-016d).

```text
## If findings are fixed later
Whenever reported findings get fixed later in this session (the user asks you
to fix them, or later work fixes them incidentally) you MUST call <FR-TOOL>
again with the same findings, each carrying an `outcome`: `fixed`,
`no_change_needed` (the finding was wrong or already handled), or `skipped`
(real but not applied). Do not repeat the findings as text.
Make that call immediately after the fixes land, before any prose summary; the
host UI's per-finding status updates only from it, and without it the findings
stay marked unresolved.
```

## 5. Outcome lines

Appended after sections 3 and 4 when the findings are delivered as a message rather than rendered by the host:

```text
After the call, give one line per finding with its outcome: this session can
also be read from a client that does not show the tool call.
```

## 6. Not reproduced

- The `/verify` hand-off of `/code-review`'s "After the review" section (research R1).
- `--post` and `--no-post`, which belong to `ultra` (spec, Assumptions).

## 7. Version tracking

`SKILL.md` cites "Source text: Claude Code 2.1.317" above these sections. `tests/test_sci_review_arguments.py` asserts the citation and that the verbatim lines above are present in `SKILL.md`.
