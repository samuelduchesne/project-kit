# Feature Specification: Bounded-cost scientific review

**Feature Branch**: `009-sci-review-cost`

**Created**: 2026-11-22

**Status**: Draft

**Input**: User description: "The /sci-review:scientific-review skill works well but it has been shown to use a ton of agents and millions of tokens. Revisit how it is configured and implemented to align with best practices for Anthropic and OpenAI agent workflows."

## Overview

Feature 007 judged every candidate finding by debate. Every perspective and a defender stated a position on every finding over up to three rebuttal rounds, and each debate batch ran its own full panel. For P perspectives, K review parts, B batches and R rebuttal rounds, a review started up to

    P*K finders + B merge moderators + B*(P+1)*(R+1) debaters + B notes moderators

agents. Every agent is a fresh context that re-reads the code, so a `medium` review of a 526-line diff started 34 agents and used 3.4 million subagent tokens; the debate alone used 71% of them (validation.md section 2). On the seeded fixture the debate added nothing: four of the five perspectives each found all 16 seeded defects on their own (SC-008 of feature 007 fails in every recorded run).

Anthropic's and OpenAI's guidance for agent systems says the same three things. Start with the simplest structure that works. Scale the number of agents to the task, with explicit budgets. Check findings by verifying them, not by multiplying reviewers. `/code-review` and the `review-docs` workflow of this repository already work this way: finders, a deterministic merge, then a verifier per finding.

This feature applies that structure to the scientific review. The agreement labels, the script-computed adjudication, the read-only guarantee, the extension contract and the argument grammar of feature 008 are unchanged.

### Defined terms

- **Finder**: a perspective reviewer in the independent round.
- **Focus dimensions**: the dimensions a finder checks exhaustively; it still reports a defect it notices in another dimension.
- **Verifier**: an agent that judges every merged finding of one batch, trying first to refute it, and returns `confirm`, `refute` or `uncertain` with its arguments.
- **Verify protocol**: finders, then a deterministic merge (a moderator only for clusters of several candidates), then independent verifiers.
- **Debate protocol**: the protocol of feature 007.
- **Agent estimate**: the fewest and the most panel agents a run can start, computed before any reviewer runs.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A default review costs a small, predictable number of agents (Priority: P1)

A user runs `/sci-review:scientific-review` on a branch. The review starts a handful of agents, says how many before it starts them, and finds the same defects as before.

**Acceptance Scenarios**:

1. **Given** a 526-line scope of one part, **When** the user runs a `medium` review, **Then** the panel starts at most 7 agents: 3 finders, at most 2 merge moderators and 2 verifiers.
2. **Given** any review, **When** the panel is configured, **Then** the user is told "This review will start <min> to <max> panel agents" before any reviewer runs.
3. **Given** a configuration whose estimate exceeds 40 agents, **When** the panel is configured, **Then** the skill asks before any reviewer runs, as a separate question.

### User Story 2 - Findings are verified, not debated (Priority: P1)

Each merged finding is judged by one or more verifiers who did not raise it and do not see each other's verdicts. A script computes its label from the number of raisers and the verdicts.

**Acceptance Scenarios**:

1. **Given** a finding that its single verifier confirms, **Then** it is labelled `consensus`, since a raiser and a verifier support it independently.
2. **Given** a finding that more verifiers refute than confirm, **Then** it is rejected with the refuting verifier's reason.
3. **Given** a finding whose verdict turns on an unsettled assumption, **Then** it is labelled `contested`, with that assumption as its deciding assumption.

### User Story 3 - The debate stays available on request (Priority: P2)

A user who wants the feature 007 debate gets it at `max`, or at a lower level by asking for a debate or for rebuttal rounds.

**Acceptance Scenarios**:

1. **Given** `max`, **Then** the panel uses the debate protocol with three rebuttal rounds, and the agent estimate (up to 109 agents for one part) is stated and confirmed.
2. **Given** `high` with "two rebuttal rounds", **Then** the debate protocol is used and the override `protocol` is recorded.

### Edge Cases

- A batch whose clusters each hold one candidate needs no moderator; its ruling is written by `panel.py auto-merge` or by the Workflow script, identically.
- A verifier's output that fails validation twice is dropped; a finding left with no verdict is labelled `contested` with a notice.
- A `panel.json` written before this feature has no `protocol` and is adjudicated as a debate.
- At `low`, a single generalist finder cannot take part in a debate; a debate requested at `low` uses the default perspectives.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every level but `max` MUST use the verify protocol; `max` MUST use the debate protocol. Rebuttal rounds of 1 or more, or `--protocol debate`, MUST select the debate protocol at any level and be recorded as an override.
- **FR-002**: The levels MUST configure: `low`, one generalist and 1 verifier per batch, 1 batch; `medium`, theorist, numerical analyst and methodologist and 1 verifier, 2 batches; `high`, the five defaults and 2 verifiers, 3 batches; `xhigh`, as `high` with 3 verifiers, 4 batches; `max`, as feature 008. Selected extensions join at every level.
- **FR-003**: In the verify protocol each default perspective MUST focus on its primary dimension, and every dimension without its primary owner on the panel MUST be assigned to another perspective on the panel, so that the finders cover all five dimensions.
- **FR-004**: Finder prompts MUST NOT include `protocol.md`; they include the role brief, the focus dimensions and their documents, the scope and the part.
- **FR-005**: A batch whose clusters each hold one candidate MUST be merged without an agent; the merged finding copies its candidate.
- **FR-006**: Verifiers MUST receive only their brief and the batch's merged findings, MUST NOT see another verifier's verdict, and MUST write one `verification` message per batch.
- **FR-007**: `panel.py adjudicate` MUST apply protocol.md section 5.1 to a verify-protocol run and section 5.2 to a debate.
- **FR-008**: `panel.py panel` MUST record the agent estimate; the skill MUST state it before any reviewer runs, and ask when its maximum exceeds 40.
- **FR-009**: The three file-based runners MUST share one procedure (protocol.md section 12); each runner file states only how it starts a task and when it falls back.

### Key Entities

- **Verification message** (`schemas/verification.schema.json`): `batch`, `verifier`, and one verdict per merged finding (`verdict`, `reason`, `argument_for`, `argument_against`, `deciding_assumption`, `no_trigger_reason`).
- **Panel** gains `protocol`, `verifiers` and `estimate`; each perspective gains `dimensions`.

## Success Criteria *(mandatory)*

- **SC-001**: On the seeded fixture at `medium`, recall of seeded defects is at least that of the debate protocol (16 of 16) and no look-alike is reported.
- **SC-002**: On the same run, the panel starts at most a quarter of the agents and uses at most a third of the subagent tokens of the debate protocol at `medium`.
- **SC-003**: Every existing test of features 007 and 008 that concerns the debate protocol passes unchanged in meaning.

## Assumptions

- The per-agent cost is dominated by each agent's fixed context and its reading of the code, so the number of agents, not the length of each prompt, sets the cost.
- A verifier that tries to refute a finding with the code in front of it catches the false positives that the debate's defender caught; the seeded fixture has none in either protocol, so this is checked on the look-alikes (SC-002 of feature 007).
