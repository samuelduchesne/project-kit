# Feature Specification: sci-review plugin

**Feature Branch**: `007-sci-review-plugin`

**Created**: 2026-11-04

**Status**: Draft

**Input**: User description: "Add a second plugin, `sci-review`, to the project-kit marketplace (plugins/sci-review/, listed in .claude-plugin/marketplace.json alongside project-kit, installed separately as sci-review@project-kit). It reviews a codebase for mathematical, physical and statistical correctness, ignoring style and lint. It ships (1) a skill `scientific-review` holding the checklist, severity scale (High/Medium/Low), output format and per-dimension reference files loaded on demand, and (2) an agent `scientific-auditor` that runs the review in its own context and returns only verified findings; where agents are unavailable the skill is applied directly. Review dimensions: mathematical invariants and derivations (equations, matrix shapes, index and summation bounds); numerical stability (float equality, overflow/underflow, catastrophic cancellation, division near zero, log-sum-exp, dtype downcasting, broadcasting producing wrong shapes, NaN propagation through reductions); physical constraints and units (explicit consistent units, unit handling at I/O boundaries, conservation laws, probabilities summing to 1, physically impossible values); data science and statistical integrity (data leakage including temporal leakage and scalers fit on validation data, plotting code that mutates data, unseeded stochastic processes). Default scope is a diff (current branch against its base), with an optional whole-repository or path-scoped mode. Following the review-docs design, the review fans out one reviewer per dimension via the Workflow tool where available, then adversarially verifies each finding before reporting. Every finding must carry evidence: the location, a concrete input or state that triggers the failure and the wrong output it produces, and a recommended derivation or fix; legitimate uses (e.g. float equality on sentinels or exact integer-valued floats) must not be flagged. The report also lists what was checked and found correct. Findings are typed so they can be reported through ReportFindings when that tool is available, otherwise as a structured table. Domain-specific building-energy (EnergyPlus) checks are out of scope and belong in the idfkit plugin."

## Clarifications

### Session 2026-11-04

- Q: Should the review be performed by one reviewer per dimension with a single verification step, or by several reviewers that can reach different conclusions? → A: By a panel of reviewers who approach the code from different scientific perspectives and form their findings independently, then debate them. Disagreement is part of the result: the report shows where the panel agreed, where a majority agreed, and where the question remains contested, with the arguments on each side.
- Q: How should computer-science correctness be covered? → A: As a fifth review dimension, algorithmic and computational correctness, with a fifth default perspective, the computer scientist.
- Q: How deep should the physics coverage go? → A: Broaden the physics dimension to "physical modelling and units", covering discretisation, boundary and initial conditions, stability limits, discrete conservation, frames and sign conventions, and validity regimes, in addition to units and bounds.
- Q: Which languages should the reference material and test fixture cover first? → A: Python first, and also TypeScript, because the primary use is building energy simulation work (idfkit, EnergyPlus) in both languages.
- Q: Where is the line between sci-review and building-energy review? → A: Building-energy specifics stay in the idfkit plugin, and this feature also adds a building-energy review to the idfkit plugin so that the two work together according to what is reviewed.
- Q: How does sci-review bring the idfkit review in? → A: Through a general domain-extension contract: any installed plugin can contribute a domain perspective and reference material and declare the code it applies to; idfkit is the first such extension.
- Q: Which hosts must run the review? → A: Claude (Claude Code, claude.ai chat, Cowork) and Codex, from one source tree. On Codex, `sci-review` is offered without `project-kit`, which depends on Claude-only components.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Review the scientific correctness of a branch (Priority: P1)

A user working on scientific, physics, computer-science or data-analysis code asks Claude to review the current branch for scientific correctness. A panel of reviewers, each approaching the code from a different scientific perspective, reviews the code changed against the base branch across five dimensions (mathematical derivations, numerical stability, physical modelling and units, statistical integrity, algorithmic and computational correctness). Each reviewer forms its findings without seeing the others'. The panel then debates the combined findings: each finding is challenged by the other reviewers and by a reviewer whose role is to defend the code, and a moderator records the outcome. Claude reports the surviving findings ordered by severity, each labelled with the panel's level of agreement. Each finding names its location, the concrete input or state that triggers it, the wrong result it produces, and the recommended derivation or fix. The report also states which changed components were checked and found correct. No file is modified.

**Why this priority**: Reviewing a change before it merges is the most frequent use and the point at which a defect is cheapest to correct. This story alone delivers a usable reviewer. Independent perspectives followed by debate is the core of the feature: a single reviewer tends to miss defects outside its habitual frame and to report plausible but false findings that a challenger would refute.

**Independent Test**: Run the review on a fixture branch that introduces a set of seeded defects (one or more per dimension) alongside correct code that resembles each defect. The report contains every seeded defect with its evidence, contains none of the correct look-alikes, and the working tree is unchanged.

**Acceptance Scenarios**:

1. **Given** a branch that changes a function to divide by a quantity that can reach zero, **When** the user asks for a scientific review, **Then** the report contains a finding at that location with an input that produces the division by zero, the resulting wrong value (infinity or NaN), and a fix.
2. **Given** a branch that fits a scaler on the full dataset before splitting it into training and validation sets, **When** reviewed, **Then** the report contains a data-leakage finding with the affected lines, the mechanism by which validation statistics reach training, and the corrected order of operations.
3. **Given** a branch whose only floating-point equality comparison is against a sentinel value or an exact integer-valued float, **When** reviewed, **Then** no finding is reported for that comparison, and it appears among the items checked and found correct.
4. **Given** a branch with no changes to code that performs mathematical, numerical, physical, statistical or algorithmic computation, **When** reviewed, **Then** Claude states that no reviewable scientific code changed and reports no findings.
5. **Given** any review, **When** it completes, **Then** the project's files are unchanged.
6. **Given** a branch that adds an explicit time-stepping solver whose time step can exceed its stability limit, **When** reviewed, **Then** the report contains a physical-modelling finding with parameter values that violate the limit and the resulting divergent or oscillating output.
7. **Given** a branch that sums floating-point results from parallel workers in completion order, **When** reviewed, **Then** the report contains an algorithmic finding showing that two runs on the same input can produce different totals, and a deterministic alternative.
8. **Given** a seeded defect that only one perspective raises in the independent round, **When** the debate completes and the other reviewers cannot refute it, **Then** it is reported, labelled with the perspective that raised it and the level of agreement reached.

---

### User Story 2 - See where the panel disagrees and why (Priority: P2)

A user reading the report wants to know not only what the panel concluded but how confident that conclusion is. For each finding the report states whether the panel reached consensus, a majority, or remained divided. For a divided finding, it gives the strongest argument for and against, so that the user can weigh them. Findings that were raised and then withdrawn during the debate are listed briefly with the reason, so that the user can see what was considered and rejected.

**Why this priority**: In scientific work a disputed result is information, not noise. Presenting a split verdict as a confident finding, or discarding it silently, would misstate the evidence. This story depends on the panel of User Story 1.

**Independent Test**: Include in the fixture one construct whose correctness depends on an unstated assumption (for example, an approximation that is valid only in a regime the code does not document). The report lists it as contested, with an argument for each position and the assumption on which the disagreement turns.

**Acceptance Scenarios**:

1. **Given** a finding that every reviewer accepts after debate, **When** reported, **Then** it is labelled as consensus.
2. **Given** a finding on which the reviewers remain divided after debate, **When** reported, **Then** it is labelled as contested and the report gives the strongest argument on each side and, where identifiable, the assumption or missing information that would settle it.
3. **Given** a finding raised in the independent round and withdrawn during debate, **When** the review completes, **Then** it appears in a separate list of rejected findings with the reason it was rejected, and not among the reported findings.

---

### User Story 3 - Review a whole repository or selected paths (Priority: P2)

A user inheriting or auditing an existing scientific codebase asks Claude to review the whole repository, or only named directories or files, rather than a diff. The review applies the same panel, dimensions, debate and report format to the requested scope.

**Why this priority**: Audits of existing code are common before a publication, a hand-over or a reuse decision, but they are less frequent than branch reviews and build on the same review behaviour.

**Independent Test**: Run the review in repository mode and then in path mode on a fixture repository with seeded defects in two directories. Repository mode reports the defects in both directories; path mode reports only those inside the named path.

**Acceptance Scenarios**:

1. **Given** a repository with seeded defects, **When** the user asks for a whole-repository scientific review, **Then** every seeded defect is reported regardless of git history.
2. **Given** the user names one directory, **When** reviewed, **Then** no finding lies outside that directory.
3. **Given** a repository too large to review completely in one pass, **When** reviewed, **Then** Claude states which parts were reviewed and which were not, rather than presenting a partial review as complete.

---

### User Story 4 - Review building energy simulation code with the idfkit extension (Priority: P2)

A user working on building energy simulation code (Python or TypeScript code built on idfkit, or EnergyPlus models and their post-processing) asks for a scientific review with both `sci-review` and the idfkit plugin installed. sci-review recognises that building-energy code is in scope, and the idfkit plugin's domain extension adds a building physicist to the panel. The building physicist takes part in the independent round and the debate on equal terms, contributing checks the general panel lacks: heat-transfer and psychrometric relations, energy balances, IP and SI conversions (for example kBtu and kWh), and simulation time conventions (hour-ending timestamps, leap years, daylight saving time, aggregation across timesteps). Where EnergyPlus model files are in scope, the extension validates them with idfkit's own model checks and brings the results into the debate as findings. When the idfkit plugin is not installed, the general review still runs, and the report says that the building-energy extension would add domain checks.

**Why this priority**: Building energy simulation is the author's primary use. The extension makes the reviewer useful for that work without placing EnergyPlus knowledge in a domain-neutral plugin, and it proves that the extension contract works for a real domain.

**Independent Test**: With both plugins installed, review a fixture branch of idfkit-based Python and TypeScript code seeded with building-energy defects (an hour-ending timestamp read as hour-starting, an energy total converted with the wrong factor between kBtu and kWh, a leap-year series truncated to 8760 hours). Each defect is reported with the building physicist among the perspectives that raised it. Uninstall the idfkit plugin and repeat: the general findings remain, the building-energy findings disappear, and the report recommends the extension.

**Acceptance Scenarios**:

1. **Given** both plugins installed and building-energy code in scope, **When** reviewed, **Then** the panel includes the building physicist and the report lists it among the perspectives used.
2. **Given** both plugins installed and no building-energy code in scope, **When** reviewed, **Then** the building physicist does not join the panel.
3. **Given** EnergyPlus model files in scope, **When** reviewed, **Then** findings from idfkit's model checks are debated and reported in the same format as other findings.
4. **Given** only `sci-review` installed and building-energy code in scope, **When** reviewed, **Then** the general review completes and the report recommends the idfkit extension.

---

### User Story 5 - Run the review where agents or parallel workflows are unavailable (Priority: P3)

A user on a surface that supports skills but not agents or multi-agent workflows (for example, claude.ai chat or Cowork) asks for a scientific review. Claude applies the review skill directly in the conversation, taking each panel role in turn: it completes each perspective's independent review before reading the next, then conducts the debate and records the outcome in the same way. The report has the same format and states that the perspectives were not independent agents, so their agreement is weaker evidence than in the parallel review.

**Why this priority**: The plugin must work on every surface where it can be installed, but the multi-agent panel is the primary experience.

**Independent Test**: Run the review on the seeded fixture branch with agents and workflows disabled. The report contains the same report sections and agreement labels as in User Stories 1 and 2, detects the seeded defects within the tolerance of SC-005, and carries the reduced-independence notice.

**Acceptance Scenarios**:

1. **Given** agents are unavailable, **When** the user asks for a review, **Then** the review runs through the skill alone, performs every panel role, and produces a complete report.
2. **Given** the review ran without independent agents, **When** the report is shown, **Then** it states that agreement among perspectives was reached within a single reviewer.
3. **Given** the findings-reporting tool is unavailable, **When** the review completes, **Then** findings are presented as a structured table with the same fields.

---

### User Story 6 - Install the reviewer separately from project-kit (Priority: P3)

A user who wants the scientific reviewer but not the project scaffolding workflows installs only the `sci-review` plugin from the existing project-kit marketplace. A user who installs only `project-kit` does not receive the reviewer.

**Why this priority**: Separate installation keeps each plugin's trigger descriptions from competing with the other's, and lets users adopt one without the other.

**Independent Test**: Add the marketplace, install only `sci-review`, and confirm the review skill and agent are available while no project-kit skill is; repeat with only `project-kit` installed.

**Acceptance Scenarios**:

1. **Given** the marketplace is added, **When** the user lists its plugins, **Then** both `project-kit` and `sci-review` appear with distinct descriptions.
2. **Given** only `sci-review` is installed, **When** the user asks to create a new project, **Then** no project-kit skill is triggered.
3. **Given** the repository is added as a Codex marketplace, **When** the user lists its plugins in Codex, **Then** `sci-review` is offered and `project-kit` is not, and the installed `scientific-review` skill runs a review.

### Edge Cases

- **No base branch can be determined**: Claude asks which base or range to review instead of guessing, and does not fall back silently to a whole-repository review.
- **Not a git repository**: diff mode is unavailable; Claude says so and offers repository or path mode.
- **Code in a language other than Python or TypeScript**: the review still applies the dimensions using their language-neutral guidance, and the report states that its worked examples do not cover that language.
- **Building-energy code without the idfkit plugin installed**: building-energy checks are not performed; general checks still apply, and the report recommends the idfkit extension.
- **Two installed extensions claim the same code**: both domain perspectives join the panel; neither replaces the other.
- **An installed extension is malformed or fails to load**: the review proceeds without it and the report names the extension and the reason.
- **The debate does not converge**: after the maximum number of rebuttal rounds the moderator records the finding as contested with each position's strongest argument; the debate never continues without bound.
- **Several reviewers report the same defect, possibly in different terms or dimensions**: the findings are merged into one before debate, and the merged finding records every perspective that raised it.
- **Every reviewer misses a defect, or the panel agrees on a wrong conclusion**: the spec makes no claim that consensus implies correctness; the report labels agreement, not truth, and the user remains the judge.
- **The user asks for a smaller or larger panel, or a quicker review**: the panel size and the number of rebuttal rounds follow the user's request within the limits of FR-026; a request for more perspectives than are available (five defaults plus the selected domain perspectives) yields all available perspectives. The report states the panel actually used.
- **Notebooks and generated files**: notebooks in scope are reviewed as code; generated or vendored files are excluded unless the user names them.

## Requirements *(mandatory)*

### Functional Requirements

#### Packaging

- **FR-001**: The marketplace MUST list a second plugin, `sci-review`, alongside `project-kit`, each installable independently of the other.
- **FR-001a**: `sci-review` MUST also be installable in Codex from the same source tree. The Codex listing of the marketplace MUST offer `sci-review` and MUST NOT offer `project-kit`.
- **FR-002**: `sci-review` MUST provide a review skill, `scientific-review`, and an agent, `scientific-auditor`, that can take any panel role defined in FR-022. The skill MUST be sufficient on its own to perform a complete review; the agent MUST be optional.
- **FR-003**: The skill's guidance for each review dimension MUST be held in a separate reference document that is loaded only when that dimension is reviewed. Each document MUST state its checks in language-neutral terms and give worked examples in Python and TypeScript.

#### Scope

- **FR-004**: The default review scope MUST be the changes on the current branch relative to its base branch.
- **FR-005**: The user MUST be able to request a whole-repository review or a review restricted to named paths.
- **FR-006**: The review MUST NOT create, modify or delete any file in the reviewed project.
- **FR-007**: The review MUST ignore style, formatting, naming and lint concerns that have no effect on the computed result.

#### Review dimensions

- **FR-008**: The review MUST cover mathematical invariants and derivations: correspondence of equations and transformations to their stated or standard forms, matrix and array shapes, and index and summation bounds (including off-by-one errors).
- **FR-009**: The review MUST cover numerical stability: floating-point equality comparisons, overflow and underflow, catastrophic cancellation, division by quantities that can approach zero, unstable evaluation of exponentials and logarithms (for example log-sum-exp), silent narrowing of numeric precision, implicit array broadcasting that yields an unintended shape, and propagation of missing or not-a-number values through reductions.
- **FR-010**: The review MUST cover physical modelling and units: whether physical quantities have explicit and consistent units, unit handling where data is read or written, conservation laws in both continuous and discrete form, probabilities and fractions that must sum to one, values that cross physically impossible bounds, discretisation of space and time, completeness and consistency of boundary and initial conditions, stability limits of time-stepping schemes (for example the CFL condition), sign conventions and coordinate frames, and use of a model outside the regime in which it is valid.
- **FR-011**: The review MUST cover statistical and data-science integrity: data leakage (including temporal leakage and preprocessing fitted on validation or test data), plotting or reporting code that mutates the data it displays, and stochastic processes without explicit seeding or other reproducibility controls.
- **FR-012**: The review MUST cover algorithmic and computational correctness: algorithm invariants and pre- and postconditions, termination and convergence criteria of iterative methods, integer overflow and index arithmetic, correctness of data-structure edge cases (empty, single-element, duplicate keys), results that depend on evaluation order or on parallel or concurrent execution, nondeterminism across runs or platforms, and caching or memoisation that returns stale results.
- **FR-012a**: Domain-specific checks (for example building-energy checks) MUST NOT be built into `sci-review`; they are contributed by domain extensions (FR-029 to FR-034).

#### Evidence

- **FR-013**: Every candidate finding MUST be challenged in debate (FR-023) before it is reported; no finding is reported on the word of a single reviewer alone.
- **FR-014**: Every reported finding MUST include: the file and line; a one-sentence statement of the defect; a failure scenario; a severity; a recommended derivation or fix; the perspectives that raised it; and its agreement label (FR-024). The failure scenario is a concrete input or program state that triggers the defect and the wrong output or behaviour that results. The only exception is a contested finding under FR-016, whose failure scenario instead states that no concrete trigger was established and gives the reason.
- **FR-015**: The review MUST NOT report constructs that are correct in context, including floating-point equality against sentinel values or exact integer-valued floats, and seeding that is deliberately left to the caller and documented as such.
- **FR-016**: A finding whose failure scenario no reviewer can make concrete MUST NOT be reported as consensus or majority; it is either reported as contested, with the reason no concrete trigger was established, or rejected.
- **FR-017**: Duplicate findings raised by different reviewers or under different dimensions MUST be merged into one before debate, recording every perspective that raised it.

#### Severity and report

- **FR-018**: Each finding MUST carry one of three severities, defined in the skill: **High** (produces a wrong result under realistic inputs), **Medium** (produces a wrong result only under plausible edge-case inputs, or prevents reproduction of a result), **Low** (a latent risk that does not currently produce a wrong result).
- **FR-019**: The report MUST order findings by agreement label (consensus, then majority, then contested) and, within each label, from most to least severe.
- **FR-020**: The report MUST list the components or checks that were reviewed and found correct, the findings rejected during debate with the reason for each, the panel that was used, and any part of the requested scope that was not reviewed, with the reason.
- **FR-021**: Findings MUST be structured records with fixed fields, so that they can be delivered through the host's findings-reporting tool where it exists, and otherwise as a table with the same fields. Contested findings MUST carry their arguments for and against in those fields.

#### Panel and debate

- **FR-022**: The review MUST be performed by a panel with the following roles:
  - **Perspective reviewers**, each reviewing the full scope across all five dimensions from a distinct scientific perspective. The default panel has five: a *theorist*, who rederives the mathematics from first principles; a *numerical analyst*, who considers behaviour in finite precision and at extreme inputs; an *experimentalist*, who checks units, physical modelling choices and whether outputs agree with known results or limiting cases; a *methodologist*, who examines inference, data handling and reproducibility; and a *computer scientist*, who examines algorithms, termination, determinism and the behaviour of concurrent or parallel execution. Domain perspectives contributed by extensions (FR-031) join in addition to these.
  - **A defender**, whose role is to argue that each finding is not a defect, by identifying the context, assumption or documented intent that makes the code correct.
  - **A moderator**, who merges duplicates, runs the debate, and records the reasons and arguments behind the outcome of each finding, without introducing findings of its own and without choosing its label.
- **FR-023**: The review MUST proceed in three phases: (1) an independent round, in which each perspective reviewer forms its findings without access to any other reviewer's findings; (2) a debate, in which each merged finding is put to the other perspective reviewers and the defender, who accept or challenge it with reasons, and the raiser may respond, for at most two rebuttal rounds by default; (3) adjudication, in which each finding receives its agreement label or is rejected, determined from the recorded positions by the rules of FR-024, and the moderator records the reasons and, for contested findings, the arguments of FR-025.
- **FR-024**: Each surviving finding MUST carry one agreement label: **consensus** (no perspective reviewer challenges it after debate and the defender's objection, if any, was answered), **majority** (more than half of the perspective reviewers in the panel, default and domain, the raiser included, accept it), or **contested** (the panel remains divided). Each member's stance is its latest position in the debate; a member not called in a later round keeps its earlier stance. A finding that the reviewer who raised it withdraws, or that no perspective reviewer other than its raiser accepts and whose defender objection stands unanswered, MUST be rejected.
- **FR-025**: For every contested finding, the report MUST give the strongest argument on each side and, where identifiable, the assumption or missing information that would settle the disagreement.
- **FR-026**: The user MUST be able to change the panel size (between two and seven perspective reviewers, counting domain perspectives) and the number of rebuttal rounds (between zero and three). The user selects perspectives from the five defaults; sizes above five are reached only with selected domain perspectives, and a request for more perspectives than are available yields all available perspectives. The defender and moderator roles MUST always be present.

#### Execution

- **FR-027**: Where the host supports parallel multi-agent workflows, each panel role MUST run as a separate agent, the independent round MUST run in parallel, and the debate for one finding MUST be able to start while other findings are still being merged.
- **FR-028**: Where parallel workflows or agents are unavailable, the review MUST perform every panel role and phase sequentially in the conversation, completing each perspective's independent review before starting the next, and MUST state in the report that the perspectives were not independent agents.

#### Domain extensions

- **FR-029**: `sci-review` MUST define a domain-extension contract through which any installed plugin can contribute, without changes to `sci-review`: a domain perspective (name, guiding questions, and the checks it owns), reference material in the same form as the dimension documents, a declaration of the code and files it applies to, and optionally a set of domain checks whose results enter the debate as candidate findings.
- **FR-030**: At the start of each review, `sci-review` MUST discover the installed extensions and select those whose applicability declaration matches the review scope. The report MUST list the extensions selected, those installed but not applicable, and those that failed to load with the reason.
- **FR-031**: A selected extension's domain perspective MUST take part in the independent round and the debate on the same terms as the default perspectives, and its findings MUST use the same fields, severities and agreement labels.
- **FR-032**: When the review scope contains code that a known but uninstalled extension would apply to, the report MUST name that extension and what it would add. For the first version, the only known extension is the idfkit building-energy extension.
- **FR-033**: This feature MUST deliver the first extension in the idfkit plugin: a *building physicist* perspective that applies to Python and TypeScript code using idfkit, EnergyPlus model files (IDF and epJSON), and EnergyPlus inputs and outputs (weather files, simulation results). It MUST cover heat-transfer and psychrometric relations, zone and system energy balances, IP and SI conversions, and simulation time conventions (hour-ending timestamps, leap years, daylight saving time, aggregation across timesteps and reporting frequencies).
- **FR-034**: Where EnergyPlus model files are in scope, the idfkit extension MUST run idfkit's existing schema and model-integrity checks and contribute their failures as candidate findings, so that they are debated and reported with the rest; it MUST NOT run simulations without the user's request.

### Key Entities

- **Review scope**: what is reviewed. One of: branch diff (base and head), whole repository, or a list of paths. Records any parts excluded and why.
- **Review dimension**: one of the five areas of scientific correctness (mathematical derivations, numerical stability, physical modelling and units, statistical integrity, algorithmic and computational correctness), each with its checklist and reference document.
- **Perspective**: a scientific stance from which a reviewer examines the code (theorist, numerical analyst, experimentalist, methodologist, computer scientist, or a domain perspective), with its guiding questions. Distinct from a dimension: every perspective reviews every dimension.
- **Domain extension**: a contribution from another installed plugin: a domain perspective, its reference material, an applicability declaration (languages, libraries, file types), and optional domain checks. The idfkit building-energy extension is the first.
- **Panel**: the perspective reviewers (default and domain), the defender and the moderator used for one review, with the number of rebuttal rounds.
- **Finding**: a defect that survived debate. Attributes: location (file, line), dimension, severity, summary, failure scenario (triggering input or state, and wrong output), recommended fix, perspectives that raised it, agreement label, and, for contested findings, the arguments for and against and the deciding assumption.
- **Debate record**: for one candidate finding, each panel member's position (accept or challenge) and reasons in each round, and the moderator's ruling.
- **Rejected finding**: a candidate withdrawn or rejected in debate, with the reason.
- **Checked item**: a component or check that was reviewed and found correct, with its location and dimension.
- **Review report**: the scope, the panel, the extensions selected, not applicable or failed, the ordered findings, the rejected findings, the checked items, the unreviewed parts with reasons, and, when applicable, the reduced-independence notice.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On the seeded fixture, which contains defects in Python and in TypeScript for each of the five dimensions, the review reports at least 90% of the seeded defects, with at least one seeded defect per dimension and per language detected.
- **SC-002**: On the seeded fixture, no correct look-alike construct is reported as a finding (0 false positives among the designated look-alikes).
- **SC-003**: 100% of reported findings include every field required by FR-014, and every consensus or majority finding has a concrete trigger and wrong output.
- **SC-004**: The reviewed project is byte-for-byte unchanged after every review.
- **SC-005**: With agents and parallel workflows unavailable, the review on the seeded fixture detects the same seeded defects as the parallel review, within one defect.
- **SC-006**: Installing only `sci-review` exposes its skill and agent and no `project-kit` skill; installing only `project-kit` exposes no `sci-review` component. In Codex, the marketplace offers `sci-review` only.
- **SC-007**: A reader can act on any High finding without consulting other sources: for each High finding on the fixture, applying the recommended fix removes the failure described in its failure scenario.
- **SC-008**: On the seeded fixture, the panel detects more seeded defects than the best single perspective reviewer achieves alone in the independent round, or the same number with fewer false positives.
- **SC-009**: On the seeded fixture, at least half of the false positives raised in the independent round are rejected during debate.
- **SC-010**: The seeded construct whose correctness depends on an unstated assumption is reported as contested, with an argument on each side and the assumption named.
- **SC-011**: In no independent round does a perspective reviewer's output depend on another reviewer's findings (verifiable from what each reviewer was given).
- **SC-012**: On the building-energy fixture with the idfkit extension installed, at least 90% of the seeded building-energy defects are reported, each listing the building physicist among the perspectives that raised it; with the extension uninstalled, none of them is attributed to a domain perspective and the report recommends the extension.
- **SC-013**: A test extension written only against the contract of FR-029, in a plugin other than idfkit, is selected, joins the panel and contributes findings without any change to `sci-review`.

## Assumptions

- The primary audience writes scientific, physics, computer-science and data-analysis code, and the author's main use is building energy simulation with idfkit. Reference material is therefore written for Python first, with TypeScript as the second language; other languages are reviewed on the same dimensions with language-neutral guidance only.
- The review reads code statically and reasons about it; it does not require executing the project or its tests. Panel members may construct a small example to support or refute a finding where the environment allows, but the review does not depend on it.
- The base branch is determined from the repository's default branch or the branch's upstream, consistent with how `review-docs` determines its baseline.
- The plugin follows the existing repository practices: its own `version` in its manifest, entries in this repository's `CHANGELOG.md`, and validation of the marketplace and both plugins before merging.
- A panel review costs several times a single-reviewer review. To keep cost proportional, findings are debated in a small, bounded number of batches, and each panel member responds to all findings of a batch in one turn per round, so the number of agent invocations grows with the number of rounds and batches, not the number of findings. The default panel (five perspectives, a defender, a moderator, two rebuttal rounds, plus any selected domain perspectives) is the recommended setting; smaller panels are available through FR-026 for quick checks.
- Diversity of perspective comes from the role each reviewer is given and the questions it is asked to pursue. Whether reviewers should also differ in underlying model is left to the plan.
- Agreement is reported as evidence of robustness, not as proof of correctness; the user remains responsible for accepting or rejecting each finding.
- Automated evaluation of the review's precision and recall beyond the seeded fixture is deferred, consistent with the constitution's deferral of automated skill evals to v2.

## Dependencies

- **Constitution amendment**: the constitution currently scopes this repository to project creation and maintenance workflows and states that the plugin lives under `plugins/project-kit/`. Adding a scientific-correctness reviewer as a second plugin requires a MINOR amendment that widens the repository's scope to a marketplace of plugins and records `sci-review`'s scope. Principle I (templates) does not apply to `sci-review`; Principles II to IV apply, and the plan must check them.
- The parallel execution path depends on the host's multi-agent capability (on Claude, workflows or agents; on Codex, subagents) and findings-reporting tool; both are optional per FR-027, FR-028 and FR-021.
- **idfkit plugin**: the building-energy extension (FR-033, FR-034) is delivered as a change to the idfkit plugin, which lives in a separate repository (`idfkit/idfkit-plugin`, local checkout at `idfkit-workspace/idfkit-plugin`). That change is planned with this feature but merged and released through the idfkit plugin's own process. The extension depends on the contract of FR-029, so the contract must be fixed first; the extension reuses idfkit's existing model-validation capability rather than reimplementing it.
