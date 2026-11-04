# Contract: domain extensions (version 1)

Any installed plugin, for Claude or for Codex, can extend `sci-review` by shipping one skill. No change to `sci-review` is needed (FR-029, SC-013).

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
