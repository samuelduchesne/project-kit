# Contract change: `new_project.py --language`

Extends [002's contract](../../002-new-project-python/contracts/new-project-cli.md).

| Option | Default | Meaning |
|--------|---------|---------|
| `--language {python,node}` | `python` | template folder: repository root for Python, `node/` for Node |

- Every command accepts it; every `ok` result adds `"language": "<python|node>"` and `"directory": "<folder or empty>"`.
- `options` reads `<folder>/cookiecutter.json`; a missing file gives exit 3 with "The template has no <Language> template at <ref>".
- `create` passes `--directory <folder>` to `cruft create` for Node; `.cruft.json` then records `"directory": "node"`.
- The planned steps in a dry run show the `--directory` argument.
