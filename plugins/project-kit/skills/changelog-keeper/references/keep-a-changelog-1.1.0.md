# Keep a Changelog 1.1.0 — Full Reference

Source: https://keepachangelog.com/en/1.1.0/

This is a condensed but faithful reference of the full Keep a Changelog 1.1.0 specification. Read this when SKILL.md doesn't cover a situation you've run into.

## What is a changelog?

A changelog is a file which contains a curated, chronologically ordered list of notable changes for each version of a project.

## Why keep a changelog?

To make it easier for users and contributors to see precisely what notable changes have been made between each release (or version) of the project.

## Who needs a changelog?

People do. Whether consumers or developers, the end users of software are human beings who care about what's in the software. When the software changes, people want to know why and how.

## Guiding principles

- Changelogs are *for humans*, not machines.
- There should be an entry for every single version.
- The same types of changes should be grouped.
- Versions and sections should be linkable.
- The latest version comes first.
- The release date of each version is displayed.
- Mention whether you follow Semantic Versioning.

## Types of changes (the six categories)

- **Added** — for new features.
- **Changed** — for changes in existing functionality.
- **Deprecated** — for soon-to-be removed features.
- **Removed** — for now removed features.
- **Fixed** — for any bug fixes.
- **Security** — in case of vulnerabilities.

## Reducing maintenance effort: the Unreleased section

Keep an `Unreleased` section at the top to track upcoming changes. This serves two purposes:

- People can see what changes they might expect in upcoming releases.
- At release time, you move the `Unreleased` section's contents into a new versioned section.

## Bad practices (anti-patterns)

### Commit log diffs

Using commit log diffs as changelogs is a bad idea — they're full of noise (merge commits, obscure titles, doc-only commits, etc.). The purpose of a commit is to document a step in the evolution of the source code; the purpose of a changelog entry is to document the noteworthy difference, often spanning multiple commits, communicated clearly to end users.

### Ignoring deprecations

When users upgrade, it should be painfully clear when something will break. Users should be able to upgrade to a version that lists deprecations, remove what's deprecated, and *then* upgrade to the version where the deprecations become removals. If you do nothing else, list deprecations, removals, and breaking changes.

### Confusing dates

Always use `YYYY-MM-DD` (ISO 8601). It's unambiguous, ordered largest-to-smallest, and is an ISO standard. Regional formats (e.g., `03/14/2025` vs `14/03/2025`) cause real confusion.

### Inconsistent changes

A changelog that only mentions *some* changes is dangerous — users may treat it as the single source of truth and miss what's missing. Either it's complete (within reason — whitespace tweaks don't count) or it's worse than nothing.

## Frequently asked questions

### Is there a standard format?

Not really. GNU's changelog style guide and the GNU NEWS file guideline both exist but are inadequate. Keep a Changelog aims to be a better convention based on observed open-source good practices.

### What should the file be named?

`CHANGELOG.md`. Some projects use `HISTORY`, `NEWS`, or `RELEASES`, but `CHANGELOG.md` is what users look for first.

### What about GitHub Releases?

Useful, but non-portable — they only render inside GitHub. They can be made to look like Keep a Changelog format but it takes effort. Also less discoverable than an uppercase `CHANGELOG.md` file alongside `README.md`.

### Can changelogs be automatically parsed?

Difficult, because real-world formats vary wildly. Vandamme (a Ruby gem) parses many but not all open-source changelogs.

### What about yanked releases?

Yanked releases — versions pulled because of a serious bug or security issue — should still appear in the changelog. Format:

```
## [0.0.5] - 2014-12-13 [YANKED]
```

The `[YANKED]` tag is intentionally loud and surrounded by brackets so it's both human-noticeable and programmatically parseable.

### Should you ever rewrite a changelog?

Yes. Common reasons: fixing missing entries, correcting an oversight about a breaking change, or improving clarity. It's fine and often necessary.

## Canonical example

This is the changelog for the Keep a Changelog project itself, which is the canonical example of the format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- v1.1 Brazilian Portuguese translation.
- v1.1 German Translation.
- v1.1 Spanish translation.

### Changed

- Use frontmatter title & description in each language version template.
- Replace broken OpenGraph image with an appropriately-sized image.

### Removed

- Trademark sign previously shown after the project description in version 0.3.0.

## [1.1.1] - 2023-03-05

### Added

- Arabic translation (#444).
- v1.1 French translation.

### Fixed

- Improve French translation (#377).
- Various broken links, page versions, and indentations.

### Changed

- Upgrade dependencies: Ruby 3.2.1, Middleman, etc.

### Removed

- Unused normalize.css file.

## [1.1.0] - 2019-02-15

### Added

- Danish translation (#297).
- Georgian translation (#337).
- Changelog inconsistency section in Bad Practices.

### Fixed

- Italian translation (#332).
- Indonesian translation (#336).

[unreleased]: https://github.com/olivierlacan/keep-a-changelog/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/olivierlacan/keep-a-changelog/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/olivierlacan/keep-a-changelog/compare/v1.0.0...v1.1.0
```

Things to notice in this example:

- The preamble is exactly two sentences and links the spec + SemVer.
- `[Unreleased]` always sits at the top, even when empty.
- Versions are in reverse chronological order with ISO dates.
- Entries are short, end with periods, and reference issue numbers where relevant.
- Empty categories (e.g., `### Removed` with nothing in it) are simply omitted from a release.
- Compare-URL link definitions live at the bottom of the file. The `[unreleased]` link compares the most recent version to `HEAD`; each versioned link compares to the previous version.

## Notes on adapting compare links

The link definitions at the bottom of the file follow the pattern:

```
[VERSION]: <repo-url>/compare/PREVIOUS_TAG...CURRENT_TAG
```

For GitHub: `https://github.com/OWNER/REPO/compare/v1.0.0...v1.1.0`
For GitLab: `https://gitlab.com/OWNER/REPO/-/compare/v1.0.0...v1.1.0`
For Bitbucket: `https://bitbucket.org/OWNER/REPO/branches/compare/v1.1.0..v1.0.0`

The very first version (the project's initial release) typically uses a tag URL instead of a compare URL, since there's no prior version to diff against:

```
[0.0.1]: https://github.com/OWNER/REPO/releases/tag/v0.0.1
```
