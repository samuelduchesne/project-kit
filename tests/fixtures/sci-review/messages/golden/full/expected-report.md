# Scientific review

## Scope

Changes since merge-base with origin/main on branch feature (0123456789ab), including uncommitted and untracked files: 3 files, 181 lines.

Runner: `claude-workflow`. The perspectives were independent agents.

Review parts: 1.

## Panel

Effort level: medium (default).

- Theorist (`theorist`, source `sci-review`)
- Numerical analyst (`numerical-analyst`, source `sci-review`)
- Experimentalist (`experimentalist`, source `sci-review`)
- Methodologist (`methodologist`, source `sci-review`)
- Computer scientist (`computer-scientist`, source `sci-review`)
- Defender and moderator

Protocol: debate. Rebuttal rounds: 2. Debate batches: at most 2.

## Extensions

No extensions were discovered or recommended.

## Findings

Finding cap: none (the usual limit); 0 findings were withheld by it.

### Consensus

#### F5. The scaler is fitted on the full data set before the split

`high` · consensus · statistical-integrity

The function at this location computes a value that callers report to users; the problem arises in the situation the trigger describes.

**In practice.** Triggered by ordinary inputs that match the trigger; a user would see a wrong result with no warning.

- **Where:** `src/sci/train.py:40-41`
- **Summary:** The scaler is fitted on the full data set before the split.
- **Trigger:** x = [1, 2, 3, 4, 100]
- **Wrong output:** the first training row scales to -0.538 instead of -1.342
- **Fix:** Fix for the scaler is fitted on the full data set before the split.
- **Raised by:** methodologist

#### F1. Temperature in Celsius is used where kelvin is required

`medium` · consensus · physical-modelling-and-units

The function at this location computes a value that callers report to users; the problem arises in the situation the trigger describes.

**In practice.** Triggered by ordinary inputs that match the trigger; a user would see a wrong result with no warning.

- **Where:** `src/sci/heat.ts:5`
- **Summary:** Temperature in Celsius is used where kelvin is required.
- **Trigger:** T = 25 (Celsius) passed to radiate()
- **Wrong output:** 418.7 W/m2 expected, 9.07e-3 W/m2 returned
- **Fix:** Fix for temperature in celsius is used where kelvin is required.
- **Raised by:** experimentalist

### Majority

#### F3. The trapezoidal sum counts the last interior point twice

`high` · majority · mathematical-derivations

The function at this location computes a value that callers report to users; the problem arises in the situation the trigger describes.

**In practice.** Triggered by ordinary inputs that match the trigger; a user would see a wrong result with no warning.

- **Where:** `src/sci/model.py:10-13`
- **Summary:** The trapezoidal sum counts the last interior point twice.
- **Trigger:** y = [1, 1, 1], h = 1
- **Wrong output:** 3 instead of 2
- **Fix:** Fix for the trapezoidal sum counts the last interior point twice.
- **Raised by:** theorist, numerical-analyst

### Contested

#### F2. The small-angle approximation is used without a stated range

`medium` · contested · mathematical-derivations

The function at this location computes a value that callers report to users; the problem arises in the situation the trigger describes.

**In practice.** Triggered by ordinary inputs that match the trigger; a user would see a wrong result with no warning.

- **Where:** `src/sci/heat.ts:30-31`
- **Summary:** The small-angle approximation is used without a stated range.
- **Trigger:** None established.
- **Wrong output:** n/a
- **Fix:** Fix for the small-angle approximation is used without a stated range.
- **Raised by:** theorist
- **Argument for:** The failure scenario of F2 holds at the stated trigger.
- **Argument against:** The approximation is accurate to 1% below 0.24 rad, which may be the intended range.
- **Deciding assumption:** Whether input angles are bounded below 0.24 rad.
- **No-trigger reason:** No member could name an input range the callers actually use.

#### F4. The cache key omits the reference year

`low` · contested · algorithmic-correctness

The function at this location computes a value that callers report to users; the problem arises in the situation the trigger describes.

**In practice.** Triggered by ordinary inputs that match the trigger; a user would see a wrong result with no warning.

- **Where:** `src/sci/model.py:80`
- **Summary:** The cache key omits the reference year.
- **Trigger:** calls with year 2020 then 2021
- **Wrong output:** the 2020 value is returned for 2021
- **Fix:** Fix for the cache key omits the reference year.
- **Raised by:** computer-scientist
- **Argument for:** The failure scenario of F4 holds at the stated trigger.
- **Argument against:** The reference year is fixed for the lifetime of the process in production.
- **Deciding assumption:** Whether the reference year can change while the process runs.

## Rejected findings

| Id | Summary | Raised by | Reason |
|---|---|---|---|
| F6 | Float equality is used against the sentinel -9999.0. | numerical-analyst | The raiser withdrew: the value is a documented sentinel. |

## Checked and found correct

| Location | Dimension | Note |
|---|---|---|
| src/sci/heat.ts:12-14 | numerical-stability | The log-sum-exp is shifted by the maximum. |
| src/sci/model.py:20-28 | mathematical-derivations | The Simpson weights match the standard form. |

## Not reviewed

| Path | Reason |
|---|---|
| uv.lock | generated (lock file) |

## Notices

None.
