# Contract: targets, review parts and the large-scope threshold

Extends section 2 (`scope`) of [007 contracts/panel-cli.md](../../007-sci-review-plugin/contracts/panel-cli.md).

## 1. `panel.py scope --target`

```text
panel.py scope --run RUN [--target TEXT] [--mode branch|repository|paths] [--baseline REF] [--path P ...] [--dry-run]
```

`--target` is the `target_text` of `arguments.json`. `scope` writes the resolved `Target` to `scope.json`. Resolution (research R5):

| Target text | Kind | Scope |
|-------------|------|-------|
| whole number, `#n`, GitHub pull URL | `pull-request` (GitHub) | merge base of base and head ... head, head fetched to `refs/sci-review/pr-<n>` |
| `!n`, `/-/merge_requests/n` URL, or a number on a GitLab remote | `pull-request` (GitLab) | as above with `glab` |
| existing local or remote branch | `branch` | the branch's diff against its base, without checkout |
| one or more existing paths inside the project | `paths` | paths mode |

Exit codes added:

- 3 with `{"ambiguous": [kinds]}` when the text matches several kinds; the skill asks the user.
- 3 with `{"missing": "gh" | "glab" | "auth" | "network"}` when a pull request cannot be read; the skill says what is missing and offers a branch or paths review (FR-012).
- 2 for a path outside the project root.
- 2 when the target text is the `near_level` token of `arguments.json` and it is not an existing branch or path (contracts/arguments.md section 1 step 4).

Removed: `--budget`, `DEFAULT_BUDGET`, the `over budget` exclusion reason.

Invariant: the working tree, the index and the checked-out branch are unchanged (FR-011). `clean` deletes `refs/sci-review/*`.

## 2. `panel.py parts`

```text
panel.py parts --run RUN [--dry-run]
```

Reads `scope.json`; writes `parts.json` (data-model section 7). Division (research R7): files grouped by directory in path order; parts of at most 2,000 lines; a larger file split at top-level definition boundaries, else fixed windows. Prints a summary line: total lines, files, parts, and whether confirmation is required.

## 3. Large-scope threshold

`confirm_required` is true when `total_lines` exceeds 6,000. The skill then states, before any reviewer runs: "This scope has <L> lines in <F> files and will be reviewed in <K> parts. Continue?" On refusal it runs nothing and offers named paths (FR-022). A review started on the model's own initiative always asks when `confirm_required` is true.

## 4. Independent round per part

Every runner runs each perspective on every part, keeping feature 007's independence rule within and across parts. Candidate files are `candidates/<perspective>--<part>.json` and carry `part`. `merge` reads all of them; nothing else in the debate changes. `panel.py report` derives each part's status, identically on every runner: `reviewed` when the candidate file of every panel perspective for the part exists and validates, `incomplete` otherwise. Incomplete parts are reported as not reviewed, with the reason (FR-023). No runner writes part status.
