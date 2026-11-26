# Scientific review

## Scope

Paths: src/energy/totals.py, src/services/results_cache.py (2 files, 280 lines).

Runner: `claude-workflow`. The perspectives were independent agents.

Review parts: 1.

## Panel

Effort level: medium (default).

- Theorist (`theorist`, source `sci-review`)
- Computer scientist (`computer-scientist`, source `sci-review`)
- 2 independent verifiers per batch, and a moderator for clusters of several candidates

Protocol: verify. Batches: at most 1.

## Extensions

No extensions were discovered or recommended.

## Findings

Finding cap: none (the usual limit); 0 findings were withheld by it.

### Consensus

#### F1. Annual energy totals shown in kBtu are about 12 times too small

`high` · consensus · physical-modelling-and-units · trigger: user-action

This function converts each building's metered electricity into the annual total shown on its dashboard.

**In practice.** Every user who views a total in kBtu for an electric meter sees it; nothing flags the value as wrong.

- **Where:** `src/energy/totals.py:20-22`
- **Summary:** The annual total converts kWh to kBtu by dividing by 3.412 instead of multiplying.
- **Trigger:** annual_total_kbtu(1000) with a meter in kWh
- **Wrong output:** 293.1 kBtu instead of 3412 kBtu
- **Fix:** Multiply by 3.412 kBtu/kWh.
- **Raised by:** theorist

#### F2. Cached results are not recomputed after a release

`medium` (lowered from high) · consensus · algorithmic-correctness · trigger: release

Optimised results are cached and reused while a building's inputs are unchanged, so users get answers without waiting.

**In practice.** After a release that changes the optimiser, users keep seeing results from the old code until their inputs change; nobody is told.

- **Where:** `src/services/results_cache.py:120-156`
- **Summary:** The result cache key covers the inputs but not the search configuration or the code version.
- **Trigger:** Compute with SEARCH_GENERATIONS=5, change the setting, recompute with unchanged inputs *(the finding quoted `SEARCH_GENERATIONS=5`; `.env:3` has `SEARCH_GENERATIONS=10`)*
- **Wrong output:** The cached result from the earlier configuration is returned as current
- **Fix:** Add a digest of the search configuration and the code version to the cache key.
- **Raised by:** computer-scientist

### Majority

None.

### Contested

None.

## Design questions

The reviewers marked these as possibly intended: the behaviour may be a deliberate trade-off that the code does not document. They are questions for the code's owners, not defects.

#### F3. Stored results are reused across schema versions

`medium` · majority · algorithmic-correctness · trigger: release

The cache returns stored results directly to the reports users download.

**In practice.** Only after a release that bumps the schema; the reuse may be deliberate, to keep reports stable across releases.

**Why it may be intended.** Keeping reports byte-identical across releases looks deliberate; no comment says so either way.

**If it is not intended.** A result in the old schema is served without migration

- **Where:** `src/services/results_cache.py:170-180`
- **Summary:** Cache lookup ignores the schema_version field of stored results.
- **Trigger:** Read a result stored under schema_version 1 after the schema moves to 2
- **Wrong output:** A result in the old schema is served without migration
- **Fix:** Include schema_version in the lookup, or migrate stored results.
- **Raised by:** computer-scientist

## Rejected findings

None.

## Checked and found correct

None recorded.

## Not reviewed

Every file in the requested scope was reviewed.

## Notices

- F2: a value quoted in the finding is contradicted by the repository; see the correction under its trigger.
