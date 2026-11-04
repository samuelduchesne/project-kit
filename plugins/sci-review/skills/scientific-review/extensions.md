# Domain extensions (contract version 1)

This document is the authoritative contract for authors of `sci-review` domain extensions. Any installed plugin, for Claude or for Codex, can extend `sci-review` by shipping one skill that follows it. No change to `sci-review` is needed (FR-029, SC-013). `scripts/panel.py select-extensions` enforces sections 2 and 4; the supported contract version is 1.

## 1. Skill

- Directory: `skills/<domain>-sci-review-extension/`.
- Name: ends in `sci-review-extension`. Description begins with `sci-review extension:` followed by the domain, so that it does not trigger on ordinary requests.
- `SKILL.md` body: states that the skill is consumed by `sci-review`, and instructs a model that loads it directly to run `sci-review` instead.

## 2. `extension.json`

```json
{
  "contract_version": 1,
  "id": "building-energy-sci-review-extension",
  "plugin": "idfkit",
  "perspective": {
    "id": "building-physicist",
    "name": "Building physicist",
    "brief": "perspective.md"
  },
  "reference": ["reference/building-energy.md"],
  "applies_to": {
    "globs": ["**/*.idf", "**/*.epJSON", "**/*.epw", "**/eplusout*"],
    "file_types": [".idf", ".epjson", ".epw"],
    "languages": ["python", "typescript"],
    "import_patterns": ["^\\s*(from|import)\\s+idfkit\\b", "from\\s+['\"]@?idfkit"]
  },
  "checks": "checks.md"
}
```

Paths are relative to the skill directory. Globs and file types match case-insensitively. `checks` is optional; when present it describes domain checks the perspective runs during the independent round, whose failures it reports as candidate findings.

## 3. Obligations

- The perspective brief follows the structure of the default briefs: stance, guiding questions, checks owned, what not to flag.
- Reference documents follow the dimension document form: language-neutral checks, then worked examples in Python and TypeScript.
- Domain checks must not modify project files or run long computations (such as simulations) without the user's request.

## 4. Discovery and failure

The orchestrator finds extensions in the host's skill listing, loads each to obtain its directory, and passes each `extension.json` to `panel.py select-extensions`. A missing or invalid declaration, or an unsupported `contract_version`, gives status `failed` with the reason; the review continues. Two selected extensions claiming the same file both join the panel.

## 5. Known extensions (FR-032)

| id | plugin | install | adds |
|----|--------|---------|------|
| `building-energy-sci-review-extension` | idfkit | `idfkit@idfkit` | building physicist; heat transfer, psychrometrics, energy balances, IP and SI conversions, simulation time conventions; idfkit model checks |

## 6. How a domain perspective takes part

1. A selected extension's perspective joins the panel with `source` set to the extension id, and counts toward the limit of seven perspectives.
2. In the independent round it receives its brief (`perspective.brief`), `protocol.md`, the five dimension documents, its reference documents (`reference`), and the scope, exactly as a default perspective does; when `checks` is present, the checks document is listed with its reference documents, and the failures of those checks are reported as candidate findings.
3. It debates on the same terms as the default perspectives, and counts in the majority denominator.
4. Its findings use the same fields, severities and agreement labels (FR-031).
