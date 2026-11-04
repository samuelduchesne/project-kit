# Quickstart: validating sci-review

Each scenario names the requirement or success criterion it demonstrates. Contracts are referenced rather than repeated.

## 1. Prerequisites

- Claude Code at the version pinned in `.github/workflows/validate.yml`, with the Workflow tool enabled.
- Codex CLI with multi-agent tools enabled (default), for the manual Codex runs only; CI does not call it.
- Node.js 22, for the Workflow parity test.
- `git`, `python3` (3.10 or later), `uv`.
- For section 6: the idfkit plugin checkout with the extension branch, and the idfkit MCP server working.

## 2. Static checks (CI)

```bash
claude plugin validate . --strict
```

```bash
claude plugin validate ./plugins/sci-review --strict
```

```bash
python3 .github/scripts/check_manifests.py
```

```bash
python3 plugins/sci-review/scripts/build_workflow.py --check
```

```bash
uv run --no-project --python 3.12 python -m unittest discover -s tests -v
```

Expected: all pass. The unit tests cover every `panel.py` subcommand (contracts/panel-cli.md), including the six adjudication rules of data-model.md section 3 and the report ordering of contracts/report.md.

## 3. Install separation (FR-001, SC-006)

In a fresh `HOME`, add the marketplace, install only `sci-review@project-kit`, and confirm with `claude plugin details sci-review` that the skill, the agent and the workflow are present and no project-kit skill is. Repeat with only `project-kit`. In Codex, add the repository's marketplace and install `sci-review`; confirm that `scientific-review` is listed and `project-kit` is not offered (FR-001a).

## 4. Seeded fixture review on each runner (SC-001 to SC-005, SC-008 to SC-011)

1. Build the fixture: `python3 tests/fixtures/sci-review/seeded-repo/build.py --out "$TMPDIR/sci-fixture"`. It creates a git repository whose feature branch adds the seeded defects, look-alikes and the contested construct listed in `tests/fixtures/sci-review/seeded-repo/manifest.json`.
2. Record `git status --porcelain` and a checksum of the tree.
3. Run the review four times in the fixture, once per runner (contracts/invocation.md section 3): Claude with Workflow; Codex; Claude with the Workflow tool disabled; Claude asked to "run it without agents".
4. For each run, compare the report with `manifest.json` using `python3 tests/fixtures/sci-review/seeded-repo/score.py "$RUN/report.json" --run "$RUN"`, where `$RUN` is the run directory kept for scoring.

Expected:

- At least 90% of seeded defects reported, at least one per dimension and per language, on the three multi-agent runners (SC-001).
- No look-alike reported (SC-002); every finding has all fields (SC-003).
- Tree checksum unchanged (SC-004).
- Sequential run within one defect of the Workflow run, and the reduced-independence notice present (SC-005, FR-028).
- The contested construct labelled `contested` with both arguments and the assumption (SC-010).
- For each High finding that matches a seeded defect, apply its recommended fix in a copy of the fixture and run the defect's reproduction check listed in `manifest.json`: it passes after the fix and failed before it (SC-007).
- `score.py --run "$RUN"` also compares the panel result with each perspective's independent-round output (SC-008) and counts independent-round false positives rejected in debate (SC-009). On the Workflow runner the run directory is filled by `panel.py ingest`, so the same command applies; keep the run directory (skip `clean`) for scoring.
- Inspecting the Workflow run's agent prompts, or the Codex run directory, shows that no independent-round input contains another perspective's output (SC-011).

## 5. Scope modes (User Story 3, edge cases)

- Repository mode on the fixture: defects in both seeded directories reported.
- Path mode naming one directory: no finding outside it.
- Fixture with no base (detached, no remote, no default branch): the review asks for a base.
- Budget lowered to 200 lines with `--budget`: the report lists the unreviewed remainder.

## 6. Extensions (User Story 4, SC-012, SC-013)

1. With idfkit and its extension installed, review the building-energy fixture: the building physicist is in the panel and at least 90% of the seeded building-energy defects list it among their raisers; IDF validation failures appear as debated findings; no simulation runs.
2. Uninstall idfkit and repeat: no finding attributed to a domain perspective; the report recommends `building-energy-sci-review-extension`.
3. Install the test plugin `tests/fixtures/sci-review/test-extension-plugin/` (an extension written only against contracts/extension.md) and review a file it declares: its perspective joins the panel and contributes findings.
4. Install a copy with an invalid `extension.json`: the report lists it as failed with the reason, and the review completes.
