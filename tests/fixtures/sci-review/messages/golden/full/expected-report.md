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

Rebuttal rounds: 2. Debate batches: at most 2.

## Extensions

No extensions were discovered or recommended.

## Findings

Finding cap: none (the usual limit); 0 findings were withheld by it.

### Consensus

| Location | Dimension | Severity | Summary | Trigger | Wrong output | Fix | Raised by | Label |
|---|---|---|---|---|---|---|---|---|
| src/sci/train.py:40-41 | statistical-integrity | high | F5: The scaler is fitted on the full data set before the split. | x = [1, 2, 3, 4, 100] | the first training row scales to -0.538 instead of -1.342 | Fix for the scaler is fitted on the full data set before the split. | methodologist | consensus |
| src/sci/heat.ts:5 | physical-modelling-and-units | medium | F1: Temperature in Celsius is used where kelvin is required. | T = 25 (Celsius) passed to radiate() | 418.7 W/m2 expected, 9.07e-3 W/m2 returned | Fix for temperature in celsius is used where kelvin is required. | experimentalist | consensus |

### Majority

| Location | Dimension | Severity | Summary | Trigger | Wrong output | Fix | Raised by | Label |
|---|---|---|---|---|---|---|---|---|
| src/sci/model.py:10-13 | mathematical-derivations | high | F3: The trapezoidal sum counts the last interior point twice. | y = [1, 1, 1], h = 1 | 3 instead of 2 | Fix for the trapezoidal sum counts the last interior point twice. | theorist, numerical-analyst | majority |

### Contested

| Location | Dimension | Severity | Summary | Trigger | Wrong output | Fix | Raised by | Label | Argument for | Argument against | Deciding assumption | No-trigger reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| src/sci/heat.ts:30-31 | mathematical-derivations | medium | F2: The small-angle approximation is used without a stated range. | n/a | n/a | Fix for the small-angle approximation is used without a stated range. | theorist | contested | The failure scenario of F2 holds at the stated trigger. | The approximation is accurate to 1% below 0.24 rad, which may be the intended range. | Whether input angles are bounded below 0.24 rad. | No member could name an input range the callers actually use. |
| src/sci/model.py:80 | algorithmic-correctness | low | F4: The cache key omits the reference year. | calls with year 2020 then 2021 | the 2020 value is returned for 2021 | Fix for the cache key omits the reference year. | computer-scientist | contested | The failure scenario of F4 holds at the stated trigger. | The reference year is fixed for the lifetime of the process in production. | Whether the reference year can change while the process runs. | n/a |

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
