# Contract: new-project conversation

What the user can rely on when they ask project-kit to create a project.

1. **Language check**: a request for Node (or any non-Python language) gets "Node support is planned, not available yet"; nothing runs unless the user then asks for Python.
2. **Environment check** (`check`): on failure, Claude names what is missing (git, uv, access to `samuelduchesne/cookiecutter-gi`, network) with how to fix it, and stops. Without a shell, Claude says the workflow needs Claude Code or Cowork on the user's computer.
3. **Interview** (`options`): Claude asks for project name, one-line description, and author name, email and GitHub handle (suggesting the user's git identity when available). It then lists the template's remaining questions with their defaults in one compact list and asks whether to keep them or change any. Answers in plain language are mapped to allowed values; anything ambiguous is asked again.
4. **Preview** (`create --dry-run`): Claude shows destination, template version, derived package name, answers that differ from defaults, and the top-level files. A template error is relayed verbatim with a request for a corrected answer.
5. **Confirmation**: nothing is created until the user confirms the preview.
6. **Creation** (`create --expect-commit`): on success Claude reports folder, template version, main options, and next steps:
   - `cd <project>` and `make install` (the template's install command)
   - create a remote repository (e.g. `gh repo create`) and push
   - start a first spec with `/speckit-constitution` then `/speckit-specify`
   On failure Claude reports the step, what exists, and that nothing was deleted.
