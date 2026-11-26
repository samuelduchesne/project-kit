# Contract: report layout and briefs

## `report.md` (markdown report)

The Scope, Panel, Extensions, Rejected findings, Checked and found correct, Not reviewed and Notices sections are unchanged. The Findings section becomes:

```markdown
## Findings

<finding cap sentence>

### Consensus            ← one subsection per label, as before

#### F3. Cached results are not recomputed after a release

`medium` (lowered from high) · consensus · algorithmic-correctness · trigger: release

<context>

**In practice.** <in_practice>

- **Where:** `src/services/results_cache.py:120-156`
- **Trigger:** <trigger> *(the finding quoted `X`; `file:line` has `Y`)*
- **Wrong output:** <wrong_output>
- **Fix:** <fix>
- **Raised by:** computer-scientist, methodologist

## Design questions

#### F5. <headline>

`medium` · majority · algorithmic-correctness · trigger: release

<context>

**Why it may be intended.** <possibly_intended_reason>

**If it is not intended.** <wrong_output>

- **Where / Trigger / Fix / Raised by** as above
```

A run from an earlier version prints `<summary>` as the heading and "Not recorded by this review." for the prose.

## `ReportFindings` mapping

| Key | Value |
|-----|-------|
| `short_summary` | headline, truncated to 60 characters |
| `summary` | `<headline>. <summary>` |
| `failure_scenario` | `<context> In practice: <in_practice> Trigger: <trigger> Wrong output: <wrong_output>` |
| `category` | `design-question` for a design question; otherwise the dimension, as before |
| `severity` | unchanged mapping |

## Brief changes (text that every implementation must contain)

- **All finder briefs** (theorist, numerical analyst, experimentalist, methodologist, computer scientist, generalist), independent round, step 4, gain: "Write `headline` (at most 90 characters, no code identifiers), `context` (one or two sentences a user of the software would understand: what this code does for them and when the problem arises) and `in_practice` (who or what causes the trigger: a user action, a data condition, a release, an operator changing configuration; roughly how often; and whether anyone would notice the wrong result)."
- **All finder briefs**, step 5 (severity): the definition of research R5.
- **Moderator**: merges `headline`, `context` and `in_practice` under the rule that already applies to `summary`.
- **Verifier**: step 2b of research R4. Step 4 gains: "Mark `possibly_intended` when the behaviour looks like a deliberate trade-off (stability, caching, tolerance, cost) that the code and its documentation neither state nor rule out; give the reason. When the documentation states the trade-off, refute instead and cite it." The output example gains the new fields.
- **Defender** (debate): may mark a position possibly intended, with a reason.
- **Computer scientist**: guiding question 7 of research R7. **`dimensions/algorithmic-correctness.md`**: the stale-caching check of research R7.
- **`protocol.md`**: section 4 (severity definition and cap); section 5.1 (rule 2a, trigger-class combination, cap); report section (layout above).
- **`SKILL.md`**: the delivery step offers `panel.py issue` for any delivered finding the user wants to file, before `panel.py clean`, and states that nothing is posted.
