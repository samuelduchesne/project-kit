export const meta = {
  name: 'review-docs',
  description: 'Review user-facing docs against a scoped code diff (PR branch by default, or any range you name) to find misalignments',
  whenToUse: 'On a PR branch, before a release, or after code changes, to audit mkdocs (or similar) docs for drift vs code. Accepts a scope: baseline range, paths, topic focus, drift categories.',
  phases: [
    { title: 'Map', detail: 'resolve the diff baseline + docs structure; build code→docs review units' },
    { title: 'Review', detail: 'one agent per code→docs unit finds drift' },
    { title: 'Verify', detail: '3-lens panel confirms each finding' },
    { title: 'Report', detail: 'synthesize severity-ranked report' },
  ],
}

// ---------------------------------------------------------------------------
// Scope (from `args`)
// ---------------------------------------------------------------------------
// The caller can narrow the review along four independent axes. All optional;
// with no args the Map stage picks the narrowest sensible baseline itself
// (branch diff when on a feature branch, last tag otherwise).

const DRIFT_CATEGORIES = ['api', 'cli', 'configuration', 'installation', 'behavioral', 'example-notebook', 'missing-docs']

function toList(v) {
  if (Array.isArray(v)) return v.filter(Boolean)
  if (typeof v === 'string' && v.trim()) return [v.trim()]
  return []
}

const rawArgs = (typeof args === 'string') ? { focus: args } : (args || {})

const requestedCategories = toList(rawArgs.categories)
const ignoredCategories = requestedCategories.filter(c => DRIFT_CATEGORIES.indexOf(c) === -1)

const scope = {
  baseline: typeof rawArgs.baseline === 'string' && rawArgs.baseline.trim() ? rawArgs.baseline.trim() : null,
  paths: toList(rawArgs.paths),
  focus: typeof rawArgs.focus === 'string' && rawArgs.focus.trim() ? rawArgs.focus.trim() : null,
  categories: requestedCategories.filter(c => DRIFT_CATEGORIES.indexOf(c) !== -1),
}

const isScoped = Boolean(scope.baseline || scope.paths.length || scope.focus || scope.categories.length)

// Shared scope block, injected into every stage so the constraint is not lost
// between agents. Kept short when unscoped so it costs nothing in the common case.
// Stages after Map pass the resolved range, because the caller's ref may not have resolved.
function scopeBlock(resolvedBaseline) {
  if (!isScoped) {
    return `## Scope constraints
The caller gave no explicit scope. Resolve the baseline yourself per the rules below, and review everything doc-relevant inside it.`
  }
  const lines = ['## Scope constraints', 'The caller narrowed this review. Honour every constraint below — work outside it is noise to them, even if it is genuine drift.', '']
  if (scope.baseline) lines.push(`- Diff baseline: \`${resolvedBaseline || scope.baseline}\` (use this, do not go looking for a tag).`)
  if (scope.paths.length) {
    lines.push(`- Paths: ${JSON.stringify(scope.paths)}. Keep a review unit only if its changed code files OR its docPaths fall under one of these. A path can name either side of the code→docs mapping, so match on either.`)
  }
  if (scope.focus) lines.push(`- Topic focus: "${scope.focus}". Drop units unrelated to this, even if they changed in the diff.`)
  if (scope.categories.length) {
    lines.push(`- Drift categories: ${JSON.stringify(scope.categories)}. Only these categories count. Do not assign or report others.`)
  }
  return lines.join('\n')
}

// ---------------------------------------------------------------------------
// Schemas
// ---------------------------------------------------------------------------

const MAP_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['lastTag', 'baseline', 'scopeMode', 'scopeNote', 'reviewUnits', 'skippedAutogen'],
  properties: {
    lastTag: {
      type: ['string', 'null'],
      description: 'The most recent git tag, if any. Informational — it is not necessarily the baseline that was used.',
    },
    baseline: {
      type: 'string',
      description: 'The concrete git range actually diffed, resolved to real refs and usable verbatim in `git diff` (e.g. "a1b2c3d..HEAD" or "v0.2.0..HEAD"). Nothing else: any note about the working tree belongs in scopeNote.',
    },
    scopeMode: {
      type: 'string',
      enum: ['explicit', 'branch', 'tag', 'fallback'],
      description: 'How the baseline was chosen: explicit (caller named it), branch (merge-base with the default branch), tag (most recent tag), fallback (no tags and no divergent branch).',
    },
    scopeNote: {
      type: 'string',
      description: 'One plain sentence a human can read stating what was reviewed, e.g. "the 7 commits on per-zone-modeling-assumptions since it branched from main, plus uncommitted work".',
    },
    docsDir: { type: 'string', description: 'The documentation root directory (e.g. "docs").' },
    reviewUnits: {
      type: 'array',
      description: 'One entry per code area that changed inside the scope AND maps to hand-written docs. Empty if nothing doc-relevant changed in scope.',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['id', 'codeArea', 'changedFilesSummary', 'docPaths', 'driftCategories'],
        properties: {
          id: { type: 'string', description: 'Short kebab-case id, e.g. "cli-flags" or "config-model".' },
          codeArea: { type: 'string', description: 'What the code area is (e.g. "CLI entry points in src/foo/cli.py").' },
          changedFilesSummary: { type: 'string', description: 'Concrete summary of what changed in this area within the baseline range, with file paths.' },
          docPaths: { type: 'array', items: { type: 'string' }, description: 'Hand-written doc files/snippets/notebooks that map to this code area.' },
          driftCategories: {
            type: 'array',
            items: { type: 'string', enum: DRIFT_CATEGORIES },
            description: 'Which drift categories are plausible for this unit — focuses the reviewer.',
          },
        },
      },
    },
    outOfScopeNote: {
      type: 'string',
      description: 'Optional. If the caller scoped the review and you dropped doc-relevant changes because they fell outside that scope, say so in one sentence so the report can mention it.',
    },
    skippedAutogen: {
      type: 'array',
      items: { type: 'string' },
      description: 'Auto-generated doc paths intentionally skipped (mkdocstrings :::-directive pages, etc.).',
    },
  },
}

const FINDINGS_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['findings'],
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['severity', 'whatChanged', 'codeLocation', 'docLocation', 'whatsWrong', 'suggestedFix'],
        properties: {
          severity: { type: 'string', enum: ['critical', 'warning', 'info'] },
          whatChanged: { type: 'string', description: 'The specific code change.' },
          codeLocation: { type: 'string', description: 'file:line of the code change.' },
          docLocation: { type: 'string', description: 'file:line of the doc that needs updating.' },
          whatsWrong: { type: 'string', description: 'Concrete description of the misalignment.' },
          suggestedFix: { type: 'string', description: 'What the docs should say instead.' },
        },
      },
    },
  },
}

const VERDICT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['real', 'refuted', 'reason'],
  properties: {
    real: { type: 'boolean', description: 'True only if, through this lens, the finding is a genuine doc/code misalignment.' },
    refuted: { type: 'boolean', description: 'True if this lens refutes the finding (inverse of real). Default true when uncertain.' },
    reason: { type: 'string', description: 'One or two sentences citing what you actually read.' },
  },
}

const REPORT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['critical', 'warning', 'info'],
  properties: {
    lastTag: { type: ['string', 'null'] },
    baseline: { type: 'string', description: 'The git range that was diffed.' },
    scopeNote: { type: 'string', description: 'Plain sentence stating what was reviewed and why that scope.' },
    critical: { type: 'array', items: FINDINGS_SCHEMA.properties.findings.items },
    warning: { type: 'array', items: FINDINGS_SCHEMA.properties.findings.items },
    info: { type: 'array', items: FINDINGS_SCHEMA.properties.findings.items },
    coverageNote: { type: 'string', description: 'What was reviewed, what scope was applied, and which auto-generated docs were skipped.' },
    note: { type: 'string', description: 'Optional overall note (e.g. "docs look aligned").' },
  },
}

// ---------------------------------------------------------------------------
// Prompts
// ---------------------------------------------------------------------------

const AUTO_BASELINE_RULES = `Choose the baseline yourself, and prefer the NARROWER one. This matters: reviewing a feature branch's docs against every release-worth of drift buries the author in findings that are not theirs to fix, and the real drift the branch introduced gets lost in the pile.

1. Find the default branch: \`git symbolic-ref --quiet --short refs/remotes/origin/HEAD\` gives a remote ref such as \`origin/main\`. Use that ref as <default>, because a local branch can be stale or absent. If that fails, use the first of \`origin/main\`, \`origin/master\`, \`main\` or \`master\` that exists.
2. Find the current branch: \`git rev-parse --abbrev-ref HEAD\`.
3. If the current branch is NOT the default branch and \`git rev-list --count <default>..HEAD\` is greater than 0, you are on a feature/PR branch. Set BASE=\`$(git merge-base <default> HEAD)\` and use the range \`$BASE..HEAD\`. Set scopeMode to "branch". This is the PR's own diff — the common case.
4. Otherwise (on the default branch, or detached, or not diverged) use the most recent tag reachable from HEAD: \`git describe --tags --abbrev=0 HEAD\`, range \`<tag>..HEAD\`. Set scopeMode to "tag".
5. If there are no tags and nothing diverged, fall back to the initial commit or another sensible baseline and name it. Set scopeMode to "fallback".`

function mapPrompt() {
  return `You are the MAP stage of a documentation-review workflow. Resolve the diff baseline, map the project's docs, and build the code→docs review units. Do NOT report drift yet.

${scopeBlock()}

## Step 0: Discover project structure
This works with any Python project that uses mkdocs (typically mkdocs-material). Discover it fresh — do not assume paths.

0a. Find the mkdocs config ('mkdocs.yml' or 'mkdocs.yaml' in the project root). Read it for:
  - docs_dir (where docs live; default 'docs/')
  - nav (which docs are hand-written)
  - plugins: mkdocstrings (auto-generated API docs) and mkdocs-jupyter (rendered notebooks)
If there is no mkdocs config, look for whatever user-facing docs exist (README, docs/ tree) and proceed with those.

0b. Identify AUTO-GENERATED docs to SKIP. Docs generated from code don't drift. Skip mkdocstrings pages (files that are >50% ':::' directives, usually under api/ or reference/) and auto-generated indices. EXCEPTION: files that mix ':::' directives with hand-written summaries (e.g. a bullet list of function signatures above the directive) — the hand-written parts DO drift; treat those as review units. List everything you skip in skippedAutogen.

0c. Identify HAND-WRITTEN docs to REVIEW: getting-started/install/quickstart/tutorials, concept/guide pages, how-to/user-guide/CLI reference/configuration, examples, migration guides, troubleshooting.

0d. Identify code snippets and notebooks. Many projects keep snippets in a dir (e.g. docs/snippets/) included via pymdownx.snippets — these are hand-written examples and high priority. Also find .ipynb notebooks if mkdocs-jupyter is enabled. Both are drift-prone.

0e. Build the code→docs mapping. Common patterns: CLI entry points (argparse/click/typer) → CLI reference/usage; public API (__init__.py exports) → concept/how-to/examples; config models (pydantic/dataclass/TypedDict) → config docs/examples; pyproject.toml (entry points, extras, deps) → install/getting-started; exception classes → troubleshooting; constants/enums/Literal → reference/config examples. Concretely: read pyproject.toml for entry points/extras/metadata; read the package __init__.py for the public API surface; skim the mkdocs nav; match code modules to doc pages by topic.

## Step 1: Resolve the diff baseline
The baseline decides what the whole review is about, so get it right before anything else.

${scope.baseline
  ? `The caller named the baseline explicitly: \`${scope.baseline}\`. Use it verbatim — do not go hunting for a tag.
Resolve it to a concrete range:
  - a bare ref (tag, branch, commit) → \`<ref>..HEAD\`
  - a three-dot range \`A...HEAD\` → resolve to \`$(git merge-base A HEAD)..HEAD\`
  - an already-complete two-dot range → use as-is
If it resolves, set scopeMode to "explicit". If it does not resolve, say so in scopeNote and apply these rules instead of failing, setting scopeMode as they direct:

${AUTO_BASELINE_RULES}`
  : AUTO_BASELINE_RULES}

Record the resolved range in \`baseline\` and the most recent tag reachable from HEAD in \`lastTag\` (\`git describe --tags --abbrev=0 HEAD\`, or null if there is none), whichever way the baseline was chosen. Write \`scopeNote\` as one plain sentence a human can read — including the branch name and commit count when you are on a branch, so the caller can immediately tell whether you scoped it the way they meant.

## Step 2: Identify what changed inside that range
With RANGE = the baseline you just resolved:
  1. \`git log RANGE --oneline\` (feature adds, renames, flag/config changes)
  2. \`git diff --name-only RANGE\` (which areas were touched)
  3. \`git diff RANGE -- <paths that map to docs>\` (the actual diffs)
  4. \`git diff\`, \`git diff --cached\` and \`git status --short\` (uncommitted work, including new untracked files — always in scope, whatever the baseline)
Use the mapping from Step 0e to focus. If the only changes are in tests/, there is probably nothing to review.

Note that docs changed inside the range are not automatically fine: a doc edited in this branch can still describe the code wrongly. Judge docs against the code as it stands now.

## Output
Return ONE review unit per changed code area that maps to hand-written docs AND survives the scope constraints. Each unit: a stable kebab-case id, what the code area is, a concrete changedFilesSummary (with paths), the docPaths that map to it, and the plausible driftCategories. If nothing doc-relevant changed in scope, return an empty reviewUnits array — that is a real and useful answer, not a failure. Always fill lastTag, baseline, scopeMode, scopeNote and skippedAutogen. If you dropped doc-relevant changes purely because they fell outside the caller's scope, note that in outOfScopeNote.`
}

function reviewPrompt(unit, map) {
  return `You are a REVIEW stage agent in a documentation-review workflow. Review ONE code→docs unit and report drift. Diff baseline: \`${map.baseline}\` (${map.scopeNote || map.scopeMode}).

${scopeBlock(map.baseline)}

## The unit
id: ${unit.id}
codeArea: ${unit.codeArea}
changedFilesSummary: ${unit.changedFilesSummary}
docPaths to review: ${JSON.stringify(unit.docPaths)}
plausible driftCategories: ${JSON.stringify(unit.driftCategories)}

## Step 2: Read the relevant docs
Read the docPaths above and any code snippets they include that exercise the changed APIs. Read the ACTUAL code diff for this area (\`git diff ${map.baseline} -- <paths>\`, plus \`git diff\` / \`git diff --cached\` and any untracked files from \`git status --short\` for uncommitted work) so you compare docs against real current code, not assumptions.

Stay inside that range. Drift introduced before the baseline is out of scope here — reporting it dilutes the review the caller asked for. If you notice something egregious from outside the range, leave it out; the caller can widen the scope if they want it.

## Step 3: Cross-reference and find misalignments
Check these categories (skip ones that don't apply${scope.categories.length ? `, and only the caller's categories ${JSON.stringify(scope.categories)} count` : ''}):
- API drift: signatures changed (added/removed/renamed params, changed defaults), return types changed, classes renamed/moved, new public API not in guides, deprecated API still shown as current.
- CLI drift: commands/subcommands added/removed/renamed, flags added/removed/renamed (decorator args vs docs), default values changed, help text changed but docs show old text, new commands with no docs.
- Configuration drift: model fields added/removed/renamed, field types changed (e.g. str→list[str]), new validators/constraints, default values changed, enum/Literal values added/removed.
- Installation/dependency drift: new optional extras not documented, removed extras still documented, min Python version changed, new required deps.
- Behavioral drift: algorithm/workflow changes, new output formats, changed error messages/handling, performance characteristics now different.
- Example/notebook drift: snippets using old signatures, YAML/JSON/TOML config examples with old field names/removed options, notebooks calling changed functions (changed imports/calls/kwargs), changed import paths, snippets that would fail lint/type-check against the current API.
- Missing docs: entirely new features/modules/CLI commands with no documentation.

## Severity
- critical: docs are actively wrong and will mislead — renames where docs use the old name, removed features still documented, changed defaults shown as old, examples that would raise errors, import paths that no longer exist.
- warning: docs incomplete/stale — new features with no docs, new CLI commands not in reference, changed behavior not reflected, new extras not documented.
- info: minor/cosmetic — help text wording differs, docs could mention a new optional feature, minor version discrepancies, style inconsistencies.

For each finding give: whatChanged (code change), codeLocation (file:line), docLocation (file:line), whatsWrong (concrete), suggestedFix (brief). Only report REAL misalignments you verified against the actual code and doc text. If this unit's docs are fully aligned, return an empty findings array.`
}

function verifyPrompt(finding, lens, map) {
  const lensInstructions = {
    'correctness':
      `CORRECTNESS lens: read the actual code at the cited codeLocation and the surrounding diff. Does the code change described in "whatChanged" actually exist as claimed, AND does it fall inside the reviewed range \`${map.baseline}\` or the uncommitted work (\`git diff\`, \`git diff --cached\`, untracked files in \`git status --short\`)? If the code does not say what the finding claims, it is refuted. If the change is real but predates the range and is not uncommitted, it is also refuted — it is not part of what the caller asked about.`,
    'doc-accuracy':
      'DOC-ACCURACY lens: read the actual doc at the cited docLocation. Does the doc actually contain the stale/wrong content the finding claims? If the doc already reflects the current code, or the cited location does not say what the finding claims, it is refuted. If the finding reports missing documentation, search the docs instead: it survives if they really do not cover the feature, and is refuted if they do.',
    'misleads':
      'MISLEADS lens: assume both the code change and the doc text are as described. Would a real reader following these docs actually be misled, get a wrong result, or hit an error? Pedantic nitpicks that would not mislead anyone are refuted. If the finding reports missing documentation, ask instead whether a user needs that documentation to discover or use the feature: it survives if so, and internal or trivial additions are refuted.',
  }
  return `You are a VERIFIER in a documentation-review workflow. Adversarially test ONE finding through ONE lens. Default to refuted=true when uncertain — it is better to drop a shaky finding than to ship a false positive.
${isScoped ? `\nThe caller scoped this review. ${scopeBlock(map.baseline)}\n` : ''}
## The finding
severity: ${finding.severity}
whatChanged: ${finding.whatChanged}
codeLocation: ${finding.codeLocation}
docLocation: ${finding.docLocation}
whatsWrong: ${finding.whatsWrong}
suggestedFix: ${finding.suggestedFix}

## Your lens
${lensInstructions[lens] || lensInstructions['correctness']}

Read the real files (do not trust the finding's summary). Return real=true only if, through this lens, the finding survives. Set refuted = !real. Cite what you actually read in one or two sentences.`
}

function reportPrompt(confirmed, map) {
  return `You are the REPORT stage of a documentation-review workflow. Produce the final severity-ranked report from the CONFIRMED findings below (each already survived a 3-lens verification panel). Do not invent new findings.

Diff baseline used: \`${map.baseline}\` (scopeMode: ${map.scopeMode})
What that covers: ${map.scopeNote || '(not stated)'}
Most recent tag: ${map.lastTag || '(none)'}
Auto-generated docs that were skipped (not reviewed): ${JSON.stringify(map.skippedAutogen || [])}
${map.outOfScopeNote ? `Dropped as out of scope: ${map.outOfScopeNote}` : ''}
${isScoped ? `Caller's scope constraints: ${JSON.stringify(scope)}` : 'No caller-supplied scope; the baseline was auto-detected.'}

## Confirmed findings (JSON)
${JSON.stringify(confirmed, null, 2)}

## Output
Group findings into critical / warning / info arrays (same fields as given). Order each group most-severe/most-actionable first.

Set \`baseline\` and \`scopeNote\` from the values above, and \`lastTag\` to the most recent tag. The reader needs to know at a glance which diff this report covers so they can tell whether it matched their intent — put that in coverageNote too, along with the code areas reviewed, any scope constraints applied, and which auto-generated docs were skipped. If changes were dropped as out of scope, say so, so the reader can rerun wider if they want.`
}

// ---------------------------------------------------------------------------
// Reports built without an agent
// ---------------------------------------------------------------------------

// Checks that did not finish. An incomplete run must not read as a clean one.
const incomplete = []

function incompleteNote() {
  return incomplete.length ? ` Incomplete: ${[...incomplete].sort().join('; ')}.` : ''
}

function emptyReport(note) {
  return { lastTag: null, baseline: '', scopeNote: '', critical: [], warning: [], info: [], coverageNote: note, note }
}

function buildReport(findings, map, note) {
  return {
    lastTag: map.lastTag || null,
    baseline: map.baseline,
    scopeNote: map.scopeNote || '',
    critical: findings.filter(f => f.severity === 'critical'),
    warning: findings.filter(f => f.severity === 'warning'),
    info: findings.filter(f => f.severity === 'info'),
    coverageNote: `Baseline ${map.baseline} (${map.scopeMode}). ${map.scopeNote || ''} Skipped auto-generated: ${JSON.stringify(map.skippedAutogen || [])}.${map.outOfScopeNote ? ` Out of scope: ${map.outOfScopeNote}` : ''}${incompleteNote()}`,
    note,
  }
}

// ---------------------------------------------------------------------------
// Orchestration
// ---------------------------------------------------------------------------

if (ignoredCategories.length) {
  const message = `Unknown drift categories ${JSON.stringify(ignoredCategories)}. Valid categories: ${DRIFT_CATEGORIES.join(', ')}.`
  log(message)
  if (!scope.categories.length) return emptyReport(`${message} No review ran.`)
}

if (isScoped) {
  const bits = []
  if (scope.baseline) bits.push(`baseline ${scope.baseline}`)
  if (scope.paths.length) bits.push(`paths ${scope.paths.join(', ')}`)
  if (scope.focus) bits.push(`focus "${scope.focus}"`)
  if (scope.categories.length) bits.push(`categories ${scope.categories.join(', ')}`)
  log(`Scoped review: ${bits.join('; ')}.`)
}

phase('Map')
const map = await agent(mapPrompt(), { schema: MAP_SCHEMA, label: 'map' })

if (!map) return emptyReport('Map stage produced no result.')

if (!(map.reviewUnits && map.reviewUnits.length)) {
  return buildReport([], map, `No doc-relevant code changes in scope (${map.scopeNote || map.baseline}) — nothing to review.`)
}

log(`Mapped ${map.reviewUnits.length} review unit(s) over ${map.baseline} (${map.scopeMode}).`)

const LENSES = ['correctness', 'doc-accuracy', 'misleads']

const reviewed = await pipeline(
  map.reviewUnits,
  unit => agent(reviewPrompt(unit, map), { schema: FINDINGS_SCHEMA, phase: 'Review', label: `review:${unit.id}` }),
  (res, unit) => {
    if (!res) incomplete.push(`review of unit ${unit.id} did not finish`)
    return parallel(((res && res.findings) ? res.findings : []).map(f => () =>
      parallel(LENSES.map(lens => () =>
        agent(verifyPrompt(f, lens, map), { schema: VERDICT_SCHEMA, phase: 'Verify', label: `verify:${unit.id}:${lens}` })))
        .then(votes => {
          const answered = votes.filter(Boolean)
          const realVotes = answered.filter(v => v.real).length
          // Lost votes matter only when they could have changed the outcome.
          if (realVotes < 2 && realVotes + LENSES.length - answered.length >= 2) {
            incomplete.push(`finding at ${f.docLocation} (unit ${unit.id}) was dropped after losing verifier votes`)
          }
          return { ...f, real: realVotes >= 2 }
        })))
  }
)

// A stage that throws leaves null in its slot, so the stage above cannot record it.
reviewed.forEach((result, index) => {
  if (!result) incomplete.push(`review of unit ${map.reviewUnits[index].id} did not finish`)
})

const confirmed = reviewed.flat().filter(Boolean).filter(f => f.real).map(({ real, ...f }) => f)

log(`${confirmed.length} finding(s) survived the 3-lens verification panel.`)
if (incomplete.length) log(`Incomplete checks: ${incomplete.length}.`)

if (!confirmed.length) {
  return buildReport([], map, incomplete.length
    ? 'No confirmed findings, but some checks did not finish, so this does not establish that the docs are aligned.'
    : `The docs look aligned with the code in this scope (${map.scopeNote || map.baseline}).`)
}

phase('Report')
let report = null
try {
  report = await agent(reportPrompt(confirmed, map), { schema: REPORT_SCHEMA, label: 'report' })
} catch (error) {
  log(`Report agent failed: ${error.message}`)
}
if (!report) return buildReport(confirmed, map, 'The report agent did not finish, so these findings are not ranked within each severity.')

if (incomplete.length) report.coverageNote = `${report.coverageNote || ''}${incompleteNote()}`.trim()
return report
