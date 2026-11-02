# Contributing

Report bugs and propose features in the [issue tracker](https://github.com/samuelduchesne/project-kit/issues). For a change larger than a small fix, open an issue before writing the code.

## Making a change

1. Follow the [Development](README.md#development) section of the README for the repository layout and the checks to run. CI runs the same checks on every pull request.
2. Build features with spec-kit: each has a spec, plan and task list under `specs/`, checked against the constitution in `.specify/memory/constitution.md`.
3. Record user-facing changes under `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md).

## Known test failures

Two helper-script tests currently fail on macOS because of the `/private` temporary path. CI runs on Linux, where they pass.
