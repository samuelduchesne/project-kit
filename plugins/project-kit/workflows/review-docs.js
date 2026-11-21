export const meta = {
  name: 'review-docs',
  description: 'Review user-facing docs against a scoped code diff at an effort level (high, xhigh or max) and report misalignments',
  whenToUse: 'Launched by the project-kit:review-docs skill for the high, xhigh and max levels, usually with the code→docs map the skill already built. low and medium run inline without this workflow.',
  phases: [
    { title: 'Map', detail: 'only when the caller passed no map: resolve the baseline and build code→docs units' },
    { title: 'Review', detail: 'one agent per code→docs unit, units capped by level' },
    { title: 'Verify', detail: 'high: one agent per unit; xhigh: one per finding; max: 3-lens panel per finding' },
  ],
}

// ---------------------------------------------------------------------------
// Levels
// ---------------------------------------------------------------------------
// Cost grows with the level, as in /code-review. The agent count is roughly:
//   high:  units (≤4) + units          → at most 8 agents
//   xhigh: units (≤8) + findings       → typically 15–30 agents
//   max:   units      + 3 × findings   → the old behaviour; only on explicit request
// low and medium never reach this script: the skill runs them inline.

const LEVELS = {
  high: { maxUnits: 4, perUnitFindings: 5, verify: 'unit', defaultCap: 15 },
  xhigh: { maxUnits: 8, perUnitFindings: 8, verify: 'finding', defaultCap: 25 },
  max: { maxUnits: Infinity, perUnitFindings: Infinity, verify: 'panel', defaultCap: Infinity },
}

const DRIFT_CATEGORIES = ['api', 'cli', 'configuration', 'installation', 'behavioral', 'example-notebook', 'missing-docs']
const SEVERITY_RANK = { critical: 0, warning: 1, info: 2 }

function toList(v) {
  if (Array.isArray(v)) return v.filter(Boolean)
  if (typeof v === 'string' && v.trim()) return [v.trim()]
  return []
}

function str(v) {
  return typeof v === 'string' && v.trim() ? v.trim() : null
}

const rawArgs = (typeof args === 'string') ? { focus: args } : (args || {})

const levelName = LEVELS[rawArgs.level] ? rawArgs.level : 'high'
const level = LEVELS[levelName]

// maxFindings: a positive number, 'all', or absent (the level's default).
const maxFindings = rawArgs.maxFindings === 'all'
  ? Infinity
  : (Number(rawArgs.maxFindings) > 0 ? Math.floor(Number(rawArgs.maxFindings)) : level.defaultCap)

const requestedCategories = toList(rawArgs.categories)
const ignoredCategories = requestedCategories.filter(c => DRIFT_CATEGORIES.indexOf(c) === -1)

const scope = {
  baseline: str(rawArgs.baseline),
  paths: toList(rawArgs.paths),
  focus: str(rawArgs.focus),
  categories: requestedCategories.filter(c => DRIFT_CATEGORIES.indexOf(c) !== -1),
}

const isScoped = Boolean(scope.baseline || scope.paths.length || scope.focus || scope.categories.length)

function scopeBlock(resolvedBaseline) {
  if (!isScoped) return ''
  const lines = ['## Scope constraints', 'The caller narrowed this review. Work outside these constraints is noise to them, even when it is genuine drift.', '']
  if (scope.baseline) lines.push(`- Diff baseline: \`${resolvedBaseline || scope.baseline}\`.`)
  if (scope.paths.length) lines.push(`- Paths: ${JSON.stringify(scope.paths)}. Keep a unit only if its changed code OR its docPaths fall under one of these.`)
  if (scope.focus) lines.push(`- Topic focus: "${scope.focus}". Drop anything unrelated.`)
  if (scope.categories.length) lines.push(`- Drift categories: ${JSON.stringify(scope.categories)}. Report no other category.`)
  return lines.join('\n') + '\n'
}

// ---------------------------------------------------------------------------
// Schemas
// ---------------------------------------------------------------------------

const UNIT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['id', 'codeArea', 'changedFilesSummary', 'docPaths', 'driftCategories'],
  properties: {
    id: { type: 'string', description: 'Short kebab-case id, e.g. "cli-flags".' },
    codeArea: { type: 'string' },
    changedFilesSummary: { type: 'string', description: 'What changed in this area within the range, with file paths.' },
    docPaths: { type: 'array', items: { type: 'string' } },
    driftCategories: { type: 'array', items: { type: 'string', enum: DRIFT_CATEGORIES } },
  },
}

const MAP_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['lastTag', 'baseline', 'scopeMode', 'scopeNote', 'reviewUnits', 'skippedAutogen'],
  properties: {
    lastTag: { type: ['string', 'null'] },
    baseline: { type: 'string', description: 'The concrete git range diffed, usable verbatim in `git diff`.' },
    scopeMode: { type: 'string', enum: ['explicit', 'branch', 'tag', 'fallback'] },
    scopeNote: { type: 'string', description: 'One plain sentence stating what was reviewed.' },
    reviewUnits: { type: 'array', items: UNIT_SCHEMA, description: 'Most important first.' },
    outOfScopeNote: { type: 'string' },
    skippedAutogen: { type: 'array', items: { type: 'string' } },
  },
}

const FINDING_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['severity', 'category', 'whatChanged', 'codeLocation', 'docLocation', 'whatsWrong', 'readerImpact', 'suggestedFix'],
  properties: {
    severity: { type: 'string', enum: ['critical', 'warning', 'info'] },
    category: { type: 'string', enum: DRIFT_CATEGORIES },
    whatChanged: { type: 'string', description: 'The specific code change.' },
    codeLocation: { type: 'string', description: 'file:line of the code change.' },
    docLocation: { type: 'string', description: 'file:line of the doc that needs updating.' },
    whatsWrong: { type: 'string', description: 'The misalignment, concretely.' },
    readerImpact: { type: 'string', description: 'What a reader following the doc does or gets wrong.' },
    suggestedFix: { type: 'string', description: 'What the doc should say instead.' },
  },
}

const FINDINGS_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['findings'],
  properties: { findings: { type: 'array', items: FINDING_SCHEMA } },
}

const VERDICT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['real', 'reason'],
  properties: {
    real: { type: 'boolean' },
    reason: { type: 'string', description: 'One or two sentences citing what you read.' },
  },
}

const BATCH_VERDICT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['verdicts'],
  properties: {
    verdicts: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['index', 'real', 'reason'],
        properties: {
          index: { type: 'integer', description: 'The finding number given in the prompt.' },
          real: { type: 'boolean' },
          reason: { type: 'string' },
        },
      },
    },
  },
}

// ---------------------------------------------------------------------------
// Prompts
// ---------------------------------------------------------------------------

const AUTO_BASELINE_RULES = `Prefer the NARROWER baseline:
1. Default branch: \`git symbolic-ref --quiet --short refs/remotes/origin/HEAD\`, else the first of origin/main, origin/master, main, master that exists.
2. If HEAD is not the default branch and \`git rev-list --count <default>..HEAD\` > 0: range \`$(git merge-base <default> HEAD)..HEAD\`, scopeMode "branch".
3. Otherwise the most recent tag: \`git describe --tags --abbrev=0 HEAD\`, range \`<tag>..HEAD\`, scopeMode "tag".
4. No tag and nothing diverged: a sensible fallback you name, scopeMode "fallback".`

function mapPrompt() {
  return `You are the MAP stage of a documentation review. Resolve the diff baseline and build code→docs review units. Do not report drift.

${scopeBlock()}
## Baseline
${scope.baseline
  ? `The caller named \`${scope.baseline}\`. A bare ref becomes \`<ref>..HEAD\`; \`A...HEAD\` becomes \`$(git merge-base A HEAD)..HEAD\`. scopeMode "explicit". If it does not resolve, say so in scopeNote and apply:\n${AUTO_BASELINE_RULES}`
  : AUTO_BASELINE_RULES}
Uncommitted work (\`git status --short\`, \`git diff\`, \`git diff --cached\`) is always in scope. Set lastTag to the most recent tag or null.

## Docs
Read mkdocs.yml (docs_dir, nav, plugins). Skip auto-generated pages (mostly \`:::\` mkdocstrings directives) and list them in skippedAutogen; keep hand-written parts of mixed pages. Snippets (pymdownx.snippets) and notebooks (mkdocs-jupyter) are hand-written and drift-prone.

## Units
From \`git diff --name-only RANGE\` and the uncommitted work, return one unit per changed code area that maps to hand-written docs, most important first, at most ${level.maxUnits === Infinity ? 'as many as needed' : level.maxUnits} (merge related areas to stay within it). Do not read every doc in full: locate the docPaths with grep. An empty list is a valid answer.`
}

function reviewPrompt(unit, map) {
  const cap = level.perUnitFindings === Infinity ? '' : ` Report at most ${level.perUnitFindings} findings, the most misleading first.`
  return `You are a REVIEWER in a documentation review. Review ONE code→docs unit for drift. Range: \`${map.baseline}\` (${map.scopeNote || map.scopeMode}) plus uncommitted work.

${scopeBlock(map.baseline)}
## The unit
id: ${unit.id}
codeArea: ${unit.codeArea}
changed: ${unit.changedFilesSummary}
docPaths: ${JSON.stringify(unit.docPaths)}
plausible categories: ${JSON.stringify(unit.driftCategories)}

## Method
Read \`git diff ${map.baseline} -- <the unit's code paths>\` and the uncommitted diff for them. Then read only the doc passages that mention the changed names (grep the docPaths for each renamed or changed symbol, flag, field and default) rather than whole pages. Judge docs against the code as it stands now; a doc edited in this range can still be wrong. Drift that predates the range is out of scope.

Categories${scope.categories.length ? ` (only ${JSON.stringify(scope.categories)} count)` : ''}: api (signatures, defaults, renames, moved import paths), cli (commands, flags, defaults), configuration (fields, types, enum values, defaults), installation (extras, Python version, deps), behavioral (outputs, errors, workflow), example-notebook (snippets, config examples, notebooks using old names), missing-docs (a user-facing feature with no docs).

Severity: critical = actively wrong, a reader is misled or hits an error; warning = incomplete or stale; info = cosmetic.

## Before you report
Check each candidate yourself before returning it: re-open the cited code line and the cited doc line and confirm both say what you claim, and that a real reader would be misled. Drop anything you cannot confirm, and drop pedantic nitpicks.${cap} An empty list is a good answer.`
}

const LENS_TEXT = {
  correctness: `CORRECTNESS: the code change in whatChanged exists at codeLocation as claimed, inside the range or the uncommitted work.`,
  'doc-accuracy': `DOC ACCURACY: the doc at docLocation really contains the stale content claimed (for missing-docs: search the docs; refuted if the feature is covered).`,
  misleads: `MISLEADS: a real reader following the doc would be misled, get a wrong result or hit an error (for missing-docs: a user needs the doc to find or use the feature). Pedantry is refuted.`,
}

function findingText(f, i) {
  return `${i !== undefined ? `### Finding ${i}\n` : ''}severity: ${f.severity}
category: ${f.category}
whatChanged: ${f.whatChanged}
codeLocation: ${f.codeLocation}
docLocation: ${f.docLocation}
whatsWrong: ${f.whatsWrong}
readerImpact: ${f.readerImpact}`
}

function verifyChecklist() {
  return `A finding is real only if it passes all three checks:\n- ${LENS_TEXT.correctness}\n- ${LENS_TEXT['doc-accuracy']}\n- ${LENS_TEXT.misleads}`
}

function verifyBatchPrompt(findings, map) {
  return `You are a VERIFIER in a documentation review. Try to refute each finding below. Range: \`${map.baseline}\` plus uncommitted work. Read the real files; do not trust the summaries. When uncertain, mark it not real.

${verifyChecklist()}

${findings.map((f, i) => findingText(f, i)).join('\n\n')}

Return one verdict per finding, using its number as index.`
}

function verifyOnePrompt(f, map) {
  return `You are a VERIFIER in a documentation review. Try to refute ONE finding. Range: \`${map.baseline}\` plus uncommitted work. Read the real files; do not trust the summary. When uncertain, real=false.

${verifyChecklist()}

${findingText(f)}`
}

function verifyLensPrompt(f, lens, map) {
  return `You are a VERIFIER in a documentation review. Test ONE finding through ONE lens. Range: \`${map.baseline}\` plus uncommitted work. Read the real files. When uncertain, real=false.

Lens: ${LENS_TEXT[lens]}

${findingText(f)}`
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const incomplete = []

function report(findings, map, note) {
  const ranked = findings.slice().sort((a, b) => SEVERITY_RANK[a.severity] - SEVERITY_RANK[b.severity])
  const delivered = ranked.slice(0, maxFindings)
  const withheld = ranked.length - delivered.length
  return {
    level: levelName,
    baseline: map ? map.baseline : '',
    scopeNote: map ? (map.scopeNote || '') : '',
    lastTag: map ? (map.lastTag || null) : null,
    findings: delivered,
    withheld,
    coverageNote: map
      ? `Level ${levelName}. Baseline ${map.baseline} (${map.scopeMode}). ${map.scopeNote || ''} Units: ${(map.reviewUnits || []).map(u => u.id).join(', ') || 'none'}. Skipped auto-generated: ${JSON.stringify(map.skippedAutogen || [])}.${map.outOfScopeNote ? ` Out of scope: ${map.outOfScopeNote}` : ''}`
      : '',
    incomplete: incomplete.slice().sort(),
    note,
  }
}

// Merge units beyond the level's cap into the last kept units, so nothing is silently dropped.
function capUnits(units) {
  if (units.length <= level.maxUnits) return units
  const kept = units.slice(0, level.maxUnits).map(u => ({ ...u, docPaths: u.docPaths.slice(), driftCategories: u.driftCategories.slice() }))
  units.slice(level.maxUnits).forEach((u, i) => {
    const k = kept[i % kept.length]
    k.id = `${k.id}+${u.id}`
    k.codeArea = `${k.codeArea}; ${u.codeArea}`
    k.changedFilesSummary = `${k.changedFilesSummary}\n${u.changedFilesSummary}`
    u.docPaths.forEach(p => { if (k.docPaths.indexOf(p) === -1) k.docPaths.push(p) })
    u.driftCategories.forEach(c => { if (k.driftCategories.indexOf(c) === -1) k.driftCategories.push(c) })
  })
  log(`Merged ${units.length} units into ${kept.length} (the ${levelName} limit).`)
  return kept
}

async function verifyUnit(findings, unit, map) {
  if (!findings.length) return []
  if (level.verify === 'unit') {
    const res = await agent(verifyBatchPrompt(findings, map), { schema: BATCH_VERDICT_SCHEMA, phase: 'Verify', label: `verify:${unit.id}` })
    if (!res) {
      incomplete.push(`verification of unit ${unit.id} did not finish; its ${findings.length} finding(s) were dropped`)
      return []
    }
    const realIdx = new Set(res.verdicts.filter(v => v.real).map(v => v.index))
    return findings.filter((_, i) => realIdx.has(i))
  }
  if (level.verify === 'finding') {
    const votes = await parallel(findings.map((f, i) => () =>
      agent(verifyOnePrompt(f, map), { schema: VERDICT_SCHEMA, phase: 'Verify', label: `verify:${unit.id}:${i}` })))
    return findings.filter((f, i) => {
      if (!votes[i]) incomplete.push(`verification of a finding at ${f.docLocation} did not finish; it was dropped`)
      return votes[i] && votes[i].real
    })
  }
  // panel: three lenses per finding, majority wins.
  const LENSES = ['correctness', 'doc-accuracy', 'misleads']
  const judged = await parallel(findings.map((f, i) => () =>
    parallel(LENSES.map(lens => () =>
      agent(verifyLensPrompt(f, lens, map), { schema: VERDICT_SCHEMA, phase: 'Verify', label: `verify:${unit.id}:${i}:${lens}` })))
      .then(votes => {
        const answered = votes.filter(Boolean)
        const yes = answered.filter(v => v.real).length
        if (yes < 2 && yes + LENSES.length - answered.length >= 2) {
          incomplete.push(`finding at ${f.docLocation} was dropped after losing verifier votes`)
        }
        return yes >= 2 ? f : null
      })))
  return judged.filter(Boolean)
}

// ---------------------------------------------------------------------------
// Orchestration
// ---------------------------------------------------------------------------

if (rawArgs.level && !LEVELS[rawArgs.level]) {
  log(`Level "${rawArgs.level}" does not run as a workflow (low and medium run inline); using high.`)
}

if (ignoredCategories.length) {
  const message = `Unknown drift categories ${JSON.stringify(ignoredCategories)}. Valid: ${DRIFT_CATEGORIES.join(', ')}.`
  log(message)
  if (!scope.categories.length) return report([], null, `${message} No review ran.`)
}

// The skill normally maps inline and passes the result, which saves an agent and a second read of the repository.
let map = rawArgs.map && Array.isArray(rawArgs.map.reviewUnits) && str(rawArgs.map.baseline) ? rawArgs.map : null
if (!map) {
  phase('Map')
  map = await agent(mapPrompt(), { schema: MAP_SCHEMA, label: 'map' })
  if (!map) return report([], null, 'The map stage produced no result.')
}
map = { scopeMode: 'explicit', scopeNote: '', lastTag: null, skippedAutogen: [], ...map }

if (!map.reviewUnits.length) {
  return report([], map, `No doc-relevant code changes in scope (${map.scopeNote || map.baseline}).`)
}

const units = capUnits(map.reviewUnits)
log(`Level ${levelName}: ${units.length} unit(s) over ${map.baseline}; verification per ${level.verify}.`)

const results = await pipeline(
  units,
  unit => agent(reviewPrompt(unit, map), { schema: FINDINGS_SCHEMA, phase: 'Review', label: `review:${unit.id}` }),
  (res, unit) => {
    if (!res) {
      incomplete.push(`review of unit ${unit.id} did not finish`)
      return []
    }
    const found = level.perUnitFindings === Infinity ? res.findings : res.findings.slice(0, level.perUnitFindings)
    return verifyUnit(found, unit, map)
  },
)

results.forEach((r, i) => {
  if (r === null && !incomplete.some(m => m.indexOf(units[i].id) !== -1)) incomplete.push(`unit ${units[i].id} did not finish`)
})

const confirmed = results.filter(Boolean).flat()
log(`${confirmed.length} finding(s) confirmed.${incomplete.length ? ` ${incomplete.length} check(s) incomplete.` : ''}`)

return report(confirmed, map, confirmed.length
  ? undefined
  : (incomplete.length
    ? 'No confirmed findings, but some checks did not finish, so this does not show the docs are aligned.'
    : `The docs look aligned with the code in this scope (${map.scopeNote || map.baseline}).`))
