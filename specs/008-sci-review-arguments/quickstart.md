# Quickstart: validating code-review-style arguments

Validation scenarios for [spec.md](./spec.md). Contracts: [arguments](./contracts/arguments.md), [targets and parts](./contracts/targets-and-parts.md), [fix and comment](./contracts/fix-and-comment.md).

## 1. Prerequisites

- Claude Code with the `sci-review` plugin installed from this worktree.
- `python3` 3.10 or later, `git`; `gh` authenticated for scenarios 5 and 6.
- The seeded fixture repository of feature 007 (`tests/fixtures/sci-review/`), copied to a temporary directory and initialised as a git repository with a feature branch.
- A throwaway GitHub repository with an open pull request containing one seeded defect, for scenario 6.
- `export XDG_CONFIG_HOME=$(mktemp -d)` so that preferences start empty.

## 2. Automated checks

```bash
python3 -m unittest tests.test_sci_review_arguments tests.test_sci_review_panel tests.test_sci_review_workflow_build
```

Expected: all pass. They cover the grammar table (SC-001, SC-004), level profiles (SC-002, SC-003), preference persistence, target resolution on a fixture repository, part division and the absence of "over budget" (SC-008, partly).

## 3. Manual scenarios

| # | Command (in the fixture repository) | Expected outcome | Spec |
|---|-------------------------------------|------------------|------|
| 1 | `/sci-review:scientific-review` | Panel equals feature 007 defaults; report says "Effort level: medium (default)" | US1, SC-003 |
| 2 | `/sci-review:scientific-review low`, then `/sci-review:scientific-review` | First run uses `low`; second reuses `low` and says so | US1, FR-007 |
| 3 | `/sci-review:scientific-review --max-findings 2`, then `--max-findings default` | At most 2 findings, withheld count stated; cap reused on the next run; cleared by `default` | US3 |
| 4 | `/sci-review:scientific-review --max-findings zero` | Review runs; one line says the value was ignored | FR-003a |
| 5 | `/sci-review:scientific-review hig` and `/sci-review:scientific-review --post` and `/sci-review:scientific-review ultra` | Each rejected before any reviewer runs, naming accepted values | FR-003 |
| 6 | `/sci-review:scientific-review <pr#> --comment` on the throwaway repository | One inline comment per delivered finding; unanchorable findings printed with a note; working tree unchanged | US5, SC-006 |
| 7 | `/sci-review:scientific-review --comment` on a branch | Findings printed; note that `--comment` was ignored; nothing posted | FR-003b |
| 8 | `/sci-review:scientific-review feature/other` (not checked out) | Scope is that branch; `git status` and current branch unchanged | US2, FR-011 |
| 9 | `/sci-review:scientific-review --fix` on a branch with one seeded defect | Defect fixed in the working tree, nothing staged; checks run; findings re-reported with outcomes; skipped findings have reasons | US6, SC-010 |
| 10 | `/sci-review:scientific-review` on `tests/fixtures/sci-review/large-scope/` | Asks before starting (18,000 lines, 9 parts); after "yes", the defect in the last file is reported; no file listed as over budget | US4, SC-008 |
| 11 | Scenario 10, answering "no" | Nothing runs; named paths offered | FR-022 |

After every scenario except 9, run `git status --porcelain --ignored` in the fixture repository and compare with the state before: no change (SC-005).

## 4. Cross-host check

On Codex, write "scientific review, high, --max-findings 3" in the request: the level and cap are applied as on Claude (FR-019, research R9). On claude.ai, confirm that the notice about unavailable preferences appears (FR-018).
