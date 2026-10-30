# Quickstart: Validate new-project for Python

Contracts: [new-project-cli.md](./contracts/new-project-cli.md), [skill-conversation.md](./contracts/skill-conversation.md).

## Prerequisites

git, uv, Claude Code 2.1.314; read access to `samuelduchesne/cookiecutter-gi` for steps 3–4.

## 1. Automated tests (no private template needed)

```bash
uv run --no-project python -m unittest discover -s tests -v
```

Expected: all tests pass (fixture template; spec-kit fetched from public GitHub).

## 2. Plugin checks

```bash
claude plugin validate . --strict
claude plugin validate ./plugins/project-kit --strict
python3 .github/scripts/check_manifests.py
```

## 3. Script against the real template

```bash
S=plugins/project-kit/scripts/new_project.py
uv run --no-project $S check
uv run --no-project $S options | python3 -m json.tool | head -40
printf '{"project_name":"demo-proj","project_description":"Demo","author":"Samuel Letellier-Duchesne","email":"samuelduchesne@me.com","author_github_handle":"samuelduchesne","layout":"src"}' > /tmp/answers.json
mkdir -p /tmp/pk && uv run --no-project $S create --answers /tmp/answers.json --dest /tmp/pk --dry-run
ls /tmp/pk                                          # still empty
uv run --no-project $S create --answers /tmp/answers.json --dest /tmp/pk
cd /tmp/pk/demo-proj && git log --oneline && ls -A && uvx cruft check
```

Expected: `check`/`options` succeed; dry run lists files and leaves `/tmp/pk` empty; real run creates `demo-proj` with `.cruft.json`, `.specify/`, one commit; `cruft check` reports the project is up to date.

Negative: `{"project_name":"bad_name"}` → exit 2 with the template's error; `{"type_checker":"nope", …}` → exit 2 listing allowed values; re-running the real create → exit 4.

## 4. Conversation (manual, in Claude Code with the plugin installed)

1. "Create a new Python project called demo-proj" → interview, preview, confirm → project created and reported.
2. "Create a new Node project" → told Node is planned; nothing runs.
3. "Create a project called bad_name" → template's error relayed; asked for another name.
