# Research: sci-review plugin

Each item records the decision, its rationale and the alternatives considered. Items R1 to R5 address the planning directive that the solution use multi-agent workflows on Claude and on Codex.

## R1. Claude multi-agent execution: the Workflow tool

- **Decision**: On Claude Code, the review runs as a plugin Workflow, `sci-review:scientific-review`, shipped in `plugins/sci-review/workflows/scientific-review.js`, following the structure of `project-kit:review-docs`. Phases: `Independent`, `Merge`, `Debate`, `Notes`; scope resolution runs before launch and adjudication and the report after it, in `panel.py`. The independent round uses `parallel()` with one `agent()` per perspective, each given a JSON schema for its output. The debate uses `pipeline()` over debate batches, so a batch's first rebuttal round starts as soon as that batch is merged. Each panel member answers all findings of a batch in one agent call per round. The Workflow returns every panel message (candidates, merge rulings, positions, moderator notes) rather than a finished report; the orchestrating conversation writes them into the run directory with `panel.py ingest`, then runs `panel.py adjudicate` and `panel.py report`. Clustering, batching and the debate stop rule, which the pipeline needs between agent calls, live in a marked pure section of the script that a Node.js test runs against the `panel.py` fixtures.
- **Rationale**: The Workflow tool provides deterministic orchestration, parallelism, schema-validated outputs and resumption, and the repository already ships a workflow with the same shape. Schema-validated agent outputs remove the need for a separate validation step on this runner.
- **Alternatives considered**: Orchestrating with the Agent tool from the main conversation (kept as runner 3, R3, because it lacks schema validation and pipelining); one workflow per phase (rejected: loses pipelining between merge and debate).

## R2. Codex multi-agent execution: native subagents driven by the skill

- **Decision**: On Codex, the `scientific-review` skill drives Codex's native subagents. Codex spawns subagents when skill or `AGENTS.md` instructions request delegation, and subagents inherit the parent's sandbox, approval policy and MCP servers. The skill's Codex runner (`runners/codex-subagents.md`) instructs the parent to: (1) create a run directory with `scripts/panel.py init`; (2) spawn one subagent per perspective in parallel, each given only its role brief, the dimension documents, the scope and the path where it must write its JSON output; (3) validate each output with `scripts/panel.py validate`; (4) cluster and batch with `scripts/panel.py merge`; (5) for each round, spawn one subagent per panel member per batch; (6) compute labels with `scripts/panel.py adjudicate`; (7) render with `scripts/panel.py report`. Subagents use the built-in `default` role unless the user has installed the optional `sci-review-panelist` custom agent (R4).
- **Rationale**: Codex plugins can ship skills, MCP servers, apps and hooks, but not agents or workflow scripts; skill-driven delegation is therefore the only plugin-deliverable route to multi-agent execution on Codex. Codex does not enforce a JSON schema on subagent output, so file-based messages validated by a script supply the guarantee that the Workflow tool gives on Claude.
- **Concurrency**: The default panel needs six concurrent subagents in the independent round plus debate (five perspectives and the defender). If Codex's `agents.max_concurrent_threads_per_session` is lower, the runner spawns in waves of that size. Independence is unaffected because inputs are fixed before any spawn.
- **Alternatives considered**: Calling `codex exec` from a script (rejected: bypasses the user's session, sandbox and approvals); shipping custom agents that the plugin writes into `~/.codex/agents/` (rejected: writes outside the project without consent, Principle III); requiring the user to enable agents (rejected: Principle IV; the sequential runner covers that case).

## R3. Claude surfaces without the Workflow tool

- **Decision**: Where the Agent tool exists but the Workflow tool does not, the skill spawns `sci-review:scientific-auditor` agents in parallel, one per role per phase, passing the role brief path and the JSON schema in the prompt, and uses `scripts/panel.py` for validation, merging, adjudication and the report, exactly as the Codex runner does. Where neither exists, the sequential runner applies.
- **Rationale**: The Agent and Codex runners share one file-based protocol; only the spawn instruction differs. This keeps three of the four runners on identical deterministic steps.
- **Alternatives considered**: Treating the absence of Workflow as the sequential case (rejected: forgoes independence that the Agent tool can provide).

## R4. Agent definitions per host

- **Decision**: Claude: one agent, `scientific-auditor`, with read-only tools (Read, Grep, Glob, Bash for `git` and `python3`), whose system prompt states that it adopts the role brief named in its task and writes nothing in the project. Codex: an optional template, `codex-agents/sci-review-panelist.toml` (`name`, `description`, `developer_instructions`, `model_reasoning_effort = "high"`, `features.apps = false`), which the user may copy into `~/.codex/agents/`; the runner works without it.
- **Rationale**: One generic agent per host, specialised by the role brief, keeps the role definitions in one place. Codex cannot override sandbox mode per agent, so read-only behaviour is enforced by instruction and verified by SC-004.
- **Alternatives considered**: One agent per role (rejected: seven agent files per host duplicating the briefs).

## R5. Model diversity across the panel

- **Decision**: All roles use the host's current model by default; diversity comes from the role briefs (spec, Assumptions). The Workflow runner accepts an optional `models` map in its arguments that assigns a model per role. Cross-vendor panels (Claude perspectives and Codex perspectives in one review) are deferred.
- **Rationale**: Cross-vendor panels would require one host to call the other's CLI outside the user's session, with separate authentication and sandboxing. The benefit is unmeasured; SC-008 can be evaluated first with single-model panels.
- **Alternatives considered**: A mixed panel via `codex exec` from a Claude Workflow agent (deferred to a later version, recorded as an open idea).

## R6. One protocol source for all runners

- **Decision**: `protocol.md`, `roles/*.md`, `dimensions/*.md` and `schemas/*.json` are the source. `scripts/build_workflow.py` embeds them into `workflows/scientific-review.js` between generated-section markers. CI runs the generator in check mode and fails on drift.
- **Rationale**: Workflow scripts are self-contained and cannot read plugin files at run time; generating them keeps the Claude Workflow runner identical to the file-based runners. `build_workflow.py --dry-run` prints the diff it would write (Principle II); `--check` prints the same diff and exits 1 when it is not empty.
- **Alternatives considered**: Having Workflow agents read the briefs from the plugin cache path (rejected: the cache path is version-dependent and not exposed to the script).

## R7. Debate batching and pipelining

- **Decision**: After the independent round, `panel.py merge` clusters candidates whose locations overlap (same file, line ranges within three lines) and groups clusters into at most `max_batches` (default 2) debate batches by file. The moderator confirms or splits each cluster semantically in one call per batch. Each debate round sends each panel member every finding of one batch at once. The pipeline starts a batch's debate when its merge ruling arrives.
- **Rationale**: Satisfies FR-027 (debate may start while other findings are merged) and the cost assumption (invocations grow with rounds and batches, not findings). Invocations are bounded by `P + B + R x B x (P + 1) + B`: P independent reviews, B merge rulings, R debate rounds per batch with every perspective and the defender, and B moderator-notes calls, where P is the number of perspectives, B the number of batches and R the number of debate rounds, that is the rebuttal rounds plus the initial positions round. Default worst case (P = 5, B = 2, two rebuttal rounds, so R = 3): 5 + 2 + 36 + 2 = 45. Largest permitted panel (P = 7, B = 4, three rebuttal rounds, so R = 4): 7 + 4 + 128 + 4 = 143. A round is skipped for a batch when no position changed in the previous round, and a later round calls only members whose stance changed, plus the perspectives that accept a finding someone newly challenged, so that new objections can be answered.
- **Alternatives considered**: One debate unit per finding (rejected: cost proportional to findings); a single batch (rejected: no pipelining).

## R8. Agreement labels computed by script

- **Decision**: `panel.py adjudicate` applies FR-024 to the recorded positions: consensus if no perspective reviewer challenges after the final round and any defender objection was answered; majority if more than half of the perspective reviewers accept; contested otherwise; rejected if withdrawn by its raiser, or accepted only by its raiser with an unanswered defender objection. A finding without a concrete failure scenario is capped at contested (FR-016). Each member's stance is its latest recorded position, carried forward when it was not called in a later round. The majority denominator is the number of perspective reviewers in the panel, default and domain, the raiser included; the defender is not counted. Before labels are computed, the moderator writes notes for every merged finding of a batch (strongest argument for and against, deciding assumption, rejection reason if rejected), without seeing labels; `panel.py adjudicate` keeps the arguments only for contested findings and the reason only for rejected ones. This lets every runner, the Workflow included, finish all model work before the script computes labels.
- **Rationale**: The labelling rule is deterministic; scripting it makes labels reproducible and testable (Principle II).
- **Alternatives considered**: Moderator assigns labels (rejected: unverifiable).

## R9. Domain-extension discovery

- **Decision**: An extension is a skill whose name ends in `sci-review-extension` and whose directory holds `extension.json` (contracts/extension.md). Discovery uses the host's skill listing, which every surface exposes to the orchestrating model; the orchestrator loads each matching skill to obtain its base directory and declaration, then `panel.py select-extensions` matches declarations against the scope's files (globs, import patterns, file types). The known-extension registry (FR-032) is a constant in `panel.py` containing the idfkit entry.
- **Rationale**: Skills are the one component both Claude and Codex plugins can ship and that is visible on every surface, so the contract works without changes to `sci-review` on either host.
- **Alternatives considered**: Scanning plugin caches on disk (rejected: host-specific paths, unavailable in claude.ai chat); a registry in `sci-review` (rejected: violates FR-029).

## R10. idfkit extension model checks

- **Decision**: The building physicist's brief instructs it to run idfkit's `validate_model` and `check_model_integrity` through the idfkit MCP server for each in-scope IDF or epJSON file, falling back to the `idfkit` Python package (`uvx --from idfkit` or an installed interpreter) and, failing both, to reporting the checks as not run. Each failure becomes a candidate finding in the extension's independent-round output. No simulation runs (FR-034).
- **Rationale**: Reuses idfkit's existing capabilities. MCP servers are inherited by subagents on Codex and by agents on Claude, so the check runs inside the domain perspective on every multi-agent runner.

## R11. Packaging for Claude and Codex

- **Decision**: `plugins/sci-review/.claude-plugin/plugin.json` and `plugins/sci-review/.codex-plugin/plugin.json` (with `skills: "./skills/"` and an `interface` block) share one version. The Claude marketplace at `.claude-plugin/marketplace.json` lists both plugins; a Codex marketplace at `.agents/plugins/marketplace.json` lists only `sci-review` with a `local` source. The idfkit plugin already ships both manifests, which confirms the pattern.
- **Rationale**: One source tree for both hosts; `project-kit`, which depends on Claude-only components, stays off Codex.
- **Open verification**: Confirm during implementation that Codex prefers `.agents/plugins/marketplace.json` over the legacy `.claude-plugin/marketplace.json` when both exist; if not, document the install command that names the Codex marketplace explicitly.

## R12. Scope resolution

- **Decision**: `panel.py scope` resolves the base as `review-docs` does (remote default branch, merge-base, uncommitted and untracked files included), lists changed files with line ranges, excludes generated and vendored files (linguist-generated attributes, `node_modules/`, `dist/`, lock files) unless named, and stops with a question when no base can be determined. Repository and path modes enumerate tracked files. Scopes over a budget (default 6,000 lines) are partitioned and the unreviewed remainder is recorded.
- **Rationale**: Deterministic and shared by all runners.
