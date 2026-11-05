# Large-scope fixture (feature 008)

This fixture verifies SC-008 of `specs/008-sci-review-arguments/spec.md`: a scope of about 18,000 reviewable lines (17,782), nearly three times the former 6,000-line budget, is reviewed in full, and a defect placed in the last file in path order is reported.

## 1. Layout

| Item | Value |
|------|-------|
| Reviewable lines | 17,782: 17,726 lines of Python in 23 files under eight directories, plus this README and `manifest.json` |
| File larger than one review part | `solver/kernels.py` (3,298 lines, cut at a top-level `def` boundary into lines 1 to 1,994 and 1,995 to 3,298) |
| Last file in path order | `units/conversions.py` |
| Expected division | 9 review parts of at most 2,000 lines, one per directory except `solver/` (two); `confirm_required` is true |

Every function except the seeded one is correct; the filler functions are deliberately simple so that a correct review raises no finding on them.

## 2. Seeded defect

| Field | Value |
|-------|-------|
| Id | `py-btuh-to-watts` |
| Location | `units/conversions.py:647` |
| Dimension | physical-modelling-and-units |
| Severity | high |
| Defect | `btu_per_hour_to_watts` multiplies by 3.412 (BTU/h per W) instead of 0.29307 (W per BTU/h): the conversion factor is inverted. |
| Trigger | `btu_per_hour_to_watts(3412.14)`, a heat flow of 1 kW |
| Wrong output | 11,642.7 W instead of 1,000 W |

`manifest.json` records the defect in the format of `tests/fixtures/sci-review/seeded-repo/manifest.json`, so that the score helper of feature 007 can match a finding to it:

```bash
python3 tests/fixtures/sci-review/seeded-repo/score.py REPORT --manifest tests/fixtures/sci-review/large-scope/manifest.json
```

## 3. Regeneration

The files were generated once and are committed as they are. Changing a file changes the line of the defect; update `manifest.json` and the table above when that happens.
