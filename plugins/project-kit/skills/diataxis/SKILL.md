---
name: diataxis
description: >-
  Write, place, and reorganize technical documentation using the Diátaxis framework (tutorials, how-to guides, reference, explanation), with MkDocs and Zensical site plumbing. Use this whenever documentation is being written, reviewed, restructured, or planned for a package or project: drafting a new docs page, turning a README into a docs site, deciding where a page belongs, auditing docs that feel messy or redundant, or fixing a page that teaches and explains and describes all at once. Trigger even when the user never says "Diátaxis": requests like "write docs for this module", "add a getting started page", "should this be a tutorial or a how-to", "my docs are a mess", "review this page", or "what's missing from my docs" all belong here. Not for changelogs (use project-kit:changelog-keeper) or inline code comments.
---

# Diátaxis

Diátaxis (diataxis.fr, by Daniele Procida) sorts documentation by the need it
serves. Two questions settle every case: is the reader **acting or thinking**,
and are they **at study or at work**? Four modes fall out of that, and each one
has its own obligations, its own voice, and its own way of failing.

The single most valuable thing this skill does is stop pages from mixing modes.
Left alone, the natural instinct when writing docs is to be helpful in every
direction at once: teach a bit, list the options, explain the design, walk
through a task. The result reads fine sentence by sentence and serves nobody,
because a reader arrives with one need and every switch of mode interrupts it.

## The compass

Use this on the page in front of you, and on paragraphs inside it.

| If the content...  | ...and serves the reader's... | ...it belongs in |
| ------------------ | ----------------------------- | ---------------- |
| informs action     | acquisition of skill (study)  | a tutorial       |
| informs action     | application of skill (work)   | a how-to guide   |
| informs cognition  | application of skill (work)   | reference        |
| informs cognition  | acquisition of skill (study)  | explanation      |

Read the terms loosely: *action* is doing, *cognition* is knowing, *acquisition*
is study, *application* is work. The compass is most useful exactly when
intuition has already answered and something still feels off.

Two distinctions cause most of the trouble:

- **Tutorial vs how-to.** Not basic vs advanced. A tutorial gives a beginner a
  successful learning experience on a controlled path; a how-to helps a
  competent person get a real job done in a messy world. A how-to can cover
  something trivial; a tutorial can cover something hard.
- **Reference vs explanation.** Reference describes the machinery, led by the
  structure of the code. Explanation discusses a topic, led by a *why* question,
  and is the only mode where opinion, history, and alternatives belong.

## Before writing anything, name the mode

State in one line which mode the page is and what need it serves, then draft.
This is cheap and it catches misclassification before a thousand words are spent
in the wrong voice. If a request does not fit one mode (very common: "write docs
for the calibration module"), say so and propose the split, rather than writing
one page that tries to cover all four.

Then read the matching reference file. Do not write from memory of the mode
names alone: the principles are specific and the failure modes are what actually
improve the draft.

- `references/tutorials.md`
- `references/how-to-guides.md`
- `references/reference.md`
- `references/explanation.md`

## Writing a new page

1. Apply the compass and name the mode.
2. Read that mode's reference file.
3. Gather and verify the facts the page needs: signatures, flags, defaults,
   paths, measured numbers. Diátaxis cannot make a page accurate, and neither
   can whoever writes the prose.
4. Delegate the drafting to the `project-kit:editor` agent, which owns the house
   voice. Give it a brief, not an instruction to "write the docs":

   - the mode from step 1, and the reader need it serves
   - the outline, as the heading skeleton you want
   - the verified facts from step 3, quoted exactly
   - the source files it may read to check anything else
   - the target path, and two sibling pages to match for conventions

   It returns the drafted page plus any gaps it could not verify. Those come
   back as `TODO(author):` markers: resolve them, do not leave them.

   Draft inline instead when the page is a few sentences, or when the facts are
   so entangled with the current context that briefing costs more than writing,
   or when agents are not available in this environment. In that case load the
   `project-kit:editorial` skill and write to the same standard.
5. Run the mode's failure checklist against the draft, honestly. Cut or move
   anything that belongs elsewhere. This is yours, not the editor's: it judges
   prose, you judge whether the page is still one mode.
6. Wire it into the nav (see below).

Material that lands in the wrong mode is almost never worthless: it is usually
in the wrong place. Move it to the page where it belongs and leave a link
behind. Deleting good explanation because it was sitting in a tutorial loses
work; relocating it improves two pages at once.

## Auditing and reorganizing existing docs

Diátaxis is a guide, not a plan. Structure is meant to emerge from improving
pages one at a time, not to be imposed first. Three things follow:

- **Never scaffold empty sections.** Creating `tutorials/`, `how-to/`,
  `reference/`, `explanation/` directories with nothing in them is the classic
  misapplication. Top-level structure should appear only when enough real pages
  demand it.
- **Work in small steps and finish them.** One page, or one paragraph, assessed
  and improved and committed. Not a big-bang restructure.
- **Do not rename or move everything at once.** Every move breaks inbound links
  and cross-references. Batch moves need redirects or link fixes in the same
  change.

For an audit, read the docs tree and the nav config first, then deliver a table
that is directly actionable rather than a general critique:

| Page | Serves | Currently | Should be | Single next action |
| ---- | ------ | --------- | --------- | ------------------ |
| `docs/getting-started.md` | new user at study | how-to wearing a tutorial title | tutorial | replace the option matrix in step 3 with one chosen path |

Then offer to do the top few. Rank by reader harm, not by tidiness: a broken
first-run experience matters more than an inconsistent heading level.

Where the next action is prose rather than placement (the page is the right mode
but reads badly, buries its message, or opens with the task instead of the
need), hand the file to the `project-kit:editor` agent in revise mode, or apply
the `project-kit:editorial` skill yourself if agents are not available. Where the
action is placement, do it yourself: the editor proposes structural moves but
does not make them.

## Common misplacements

- A "Getting started" page that assumes competence and lists alternatives is a
  how-to with a tutorial's title. Either rewrite it as a lesson or retitle it.
- A tutorial that pauses to justify a design decision: move the justification to
  explanation, leave one plain sentence and a link.
- A reference page with a worked end-to-end task inside it: split the task out
  as a how-to.
- A how-to with a "Background" section on top: the reader is mid-task, move it.
- Explanation that drifts into numbered steps: those steps are a how-to.
- Hand-maintained API tables that mirror the code: generate them from docstrings
  with mkdocstrings instead, so they cannot drift.
- One giant page covering install, tour, API, and rationale: this is four pages.

## Titles

Titles are the main signal readers use to pick a page, so make the mode legible
from the title alone.

- How-to: *How to configure X*. Not *Configuring X* (ambiguous: might be about
  whether to) and definitely not *X configuration* (might be reference).
- Explanation: it should read naturally with an implicit *about* in front:
  *About connection pooling*, *Why simulations are cached*.
- Reference: name it after the thing in the code.
- Tutorial: name the thing the learner will end up having built or done.

## MkDocs and Zensical plumbing

Zensical is the successor to MkDocs / Material for MkDocs from the same team. It
reads an existing `mkdocs.yml` natively and also supports its own
`zensical.toml`. Check which config file the project has and match it; do not
convert a project's config format unless asked.

A nav that has grown into Diátaxis shape, in both formats:

```toml
# zensical.toml
[project]
nav = [
  "index.md",
  { "Tutorials" = [
    "tutorials/index.md",
    "tutorials/first-model.md",
  ] },
  { "How-to guides" = [
    "how-to/index.md",
    "how-to/parse-a-deck.md",
  ] },
  { "Reference" = [
    "reference/api.md",
  ] },
  { "Explanation" = [
    "explanation/object-model.md",
  ] },
]
```

```yaml
# mkdocs.yml
nav:
  - index.md
  - Tutorials:
      - tutorials/index.md
      - tutorials/first-model.md
  - How-to guides:
      - how-to/index.md
      - how-to/parse-a-deck.md
  - Reference:
      - reference/api.md
  - Explanation:
      - explanation/object-model.md
```

Useful details:

- Section overview pages come from an `index.md` in the folder, listed first,
  with the `navigation.indexes` theme feature enabled. A section index is a good
  home for a short orienting list of what is in that section.
- Reference sections are usually best generated: mkdocstrings pulls API docs
  from docstrings, which keeps reference faithful to the code by construction.
- If the project has no nav block, both tools infer nav from the folder
  structure, so directory names carry the structure and page order follows
  filenames.
- The four section names are not sacred. Explanation is often better labelled
  *Discussion*, *Background*, *Concepts*, or *Topics*, and many projects merge
  tutorials into a single *Getting started* section while there is only one.

## Before calling a page done

Diátaxis cannot make documentation accurate, complete, or consistent: those are
prerequisites, and they come from care and testing, not from the framework.
What Diátaxis addresses is whether the page fits the need and flows.

- Accuracy: every command, path, flag, and output in the draft either came from
  the actual code or was run. If something was not verified, say so rather than
  presenting it as tested.
- Tutorials in particular must be executed start to finish, in a clean
  environment, before publishing. A tutorial that fails at step 4 destroys more
  confidence than having no tutorial.
- Applying Diátaxis tends to expose gaps that were hidden by mixed-mode prose
  (moving the explanation out of a tutorial reveals the step that was never
  actually explained). Report those gaps; do not paper over them.
