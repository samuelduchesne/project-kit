# Contract: `scripts/panel.py`

Standard library only, Python 3.10 or later. Every subcommand reads JSON files, writes JSON to standard output or into `--run`, logs its arguments to standard error, and never writes inside the reviewed project. `scope --mode branch --baseline REF` records `mode: explicit` in `scope.json`; `explicit` is not accepted as a `--mode` value. Exit codes: 0 success, 1 validation failure, 2 usage error, 3 precondition not met (for example, no base branch). Every subcommand that creates, writes or removes files accepts `--dry-run`, which prints each path and the content it would write, or each path it would remove, and changes nothing (constitution, Principle II).

| Subcommand | Arguments | Output |
|------------|-----------|--------|
| `init` | `--project PATH` | creates a run directory under the system temp dir; prints its path |
| `scope` | `--run DIR --mode {branch,repository,paths} [--baseline REF] [--path P ...] [--budget N]` | writes `scope.json` (ReviewScope) |
| `select-extensions` | `--run DIR --declaration FILE ...` | writes `panel.json` extension statuses, including `recommended` known extensions |
| `panel` | `--run DIR [--perspectives ...] [--rounds N] [--batches N] --runner R [--models ROLE=MODEL ...]` | writes `panel.json` with clamped values |
| `validate` | `--schema NAME FILE` | prints errors; exit 1 if invalid (types, enums, required, `additionalProperties`, patterns, nullable, minimum, `minItems`, `minLength`, `if`/`then` on `const` or `enum`, and the single-message semantic checks) |
| `ingest` | `--run DIR FILE` | writes a Workflow result (every panel message) into the run directory layout of contracts/panel-messages.md section 2, validating each message |
| `merge` | `--run DIR` | prints location clusters grouped into batches, with each batch's `next_finding_id` for split findings (batch b reserves `F(1000 b + 1)` onward); runners redirect it to `$RUN/clusters.json` |
| `debate-status` | `--run DIR --batch B --round K` | prints whether the batch's debate stops after rebuttal round K and which members round K+1 calls (protocol.md section 8); read-only |
| `adjudicate` | `--run DIR` | writes `adjudication.json` (labels per data-model.md section 3, with the moderator notes attached); exit 1 on a semantic violation such as `withdraw` from a non-raiser |
| `report` | `--run DIR [--format {json,markdown}]` | writes `$RUN/report.json` (the JSON form, whatever the format) and prints the report; Markdown follows contracts/report.md |
| `clean` | `--run DIR` | removes the run directory |
| `notice` | `--run DIR TEXT` | appends a notice for the report (a missing tool, a dropped message, a changed project file) to `$RUN/notices.json` |

`build_workflow.py [--check | --dry-run]` regenerates the generated section of `workflows/scientific-review.js` from `protocol.md`, `roles/`, `dimensions/` and `schemas/`. `--dry-run` prints the unified diff it would apply and writes nothing; `--check` prints the same diff and exits 1 if it is not empty.

`init` writes `$RUN/run.json` (`project`, `run`), which every later subcommand reads to find the project and to refuse a run directory inside it.
