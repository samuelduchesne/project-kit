# Confirm intended behaviour: Stored results are reused across schema versions

## Situation

The cache returns stored results directly to the reports users download.

## Who hits this and when

After any release that bumps the schema version, every report stored earlier is served unchanged; the store is a file that persists across releases (store.py). Whether that is meant to keep issued reports stable is not documented. (Revised by the verifier.)

Trigger: a release of new code. The schema version changes only in a release.

## Bug or design question

Possibly intended: Keeping reports byte-identical across releases looks deliberate; no comment says so either way.

If it is not intended: A result in the old schema is served without migration

Please confirm which behaviour is wanted.

## Where

`src/services/results_cache.py:170-180` at `a1b2c3d4e5f6`

## Reproduction

Read a result stored under schema_version 1 after the schema moves to 2

Result: A result in the old schema is served without migration

## Proposed fix

Include schema_version in the lookup, or migrate stored results.

## Suggested owners

No owners found: the project is not a git repository and has no ownership file covering this file.

---

<sub>Found by a medium sci-review (majority; raised by computer-scientist; 2 verifiers) on `a1b2c3d4e5f6`.</sub>
