# Cached results are not recomputed after a release

## Situation

Optimised results are cached and reused while a building's inputs are unchanged, so users get answers without waiting.

## Who hits this and when

After a release that changes the optimiser, users keep seeing results from the old code until their inputs change; nobody is told.

Trigger: a release of new code. settings.py reads SEARCH_GENERATIONS from the environment; .env sets 10 and production uses the default 100. Each deployment has its own store, so the setting does not change under a cache; a release of new optimiser code does.

## Bug or design question

Defect, medium, lowered from high because its only trigger is a release of new code.

## Where

`src/services/results_cache.py:120-156` at `a1b2c3d4e5f6`

## Reproduction

Compute with SEARCH_GENERATIONS=5, change the setting, recompute with unchanged inputs

Note: the finding quoted `SEARCH_GENERATIONS=5`; `.env:3` has `SEARCH_GENERATIONS=10`.

Result: The cached result from the earlier configuration is returned as current

## Proposed fix

Add a digest of the search configuration and the code version to the cache key.

## Suggested owners

No owners found: the project is not a git repository and has no ownership file covering this file.

---

<sub>Found by a medium sci-review (consensus; raised by computer-scientist; 2 verifiers) on `a1b2c3d4e5f6`.</sub>
