---
name: editorial
description: The house writing style, after Jean-Luc Doumont's *Trees, maps and theorems*. Load this whenever prose is written or revised for a human reader: documentation pages, READMEs, ADRs, release notes, report text, long docstrings, PR descriptions. Trigger on "make this read better", "tighten this", "the tone is off", "edit this page", "rewrite this section", or any request to improve wording, flow, or structure of written text. Diátaxis decides what belongs on a page; this decides how it reads. Use with the `project-kit:editor` agent, which applies these rules to a file.
---

# Editorial style

Two frameworks, one job each.

- **Diátaxis** decides what belongs on the page and what does not.
- **Doumont** decides how the surviving text reads.

They rarely conflict. When they do, Diátaxis wins on placement and Doumont wins
on expression: if explanation has leaked into a tutorial, move it, then make it
read well where it lands.

## The three laws

Every rule below is a consequence of one of these. When a case is not covered,
reason from the laws rather than inventing a new rule.

**1. Adapt to the audience.** Communication is what gets across, not what was
said. Before writing, state in one line who reads this and what they must be
able to do or believe afterwards. If that line cannot be written, the document
cannot be written either: ask, do not guess.

**2. Maximize the signal-to-noise ratio.** Signal is what serves the stated
purpose. Noise is everything else, and it is not only wrong content: a typo, an
undefined acronym, an inconsistent term, a heading that says nothing, a
paragraph of throat-clearing, and a stray bold phrase are all noise. Noise is
cheap to add and it taxes every reader.

**3. Use effective redundancy.** Redundancy is not the opposite of noise.
Readers are selective and distracted, so the message must survive partial
reading. State it in the title, in the opening, and in the conclusion; pair
prose with a table; give the rule, then an example. What makes redundancy
effective is that each restatement is at a different level of detail or in a
different form. The same sentence twice at the same level is noise.

## Resolving the audience

The first law is the one most easily paid lip service. "Written for developers"
is not an audience, it is a placeholder, and a document written to a placeholder
reads exactly as though nobody was imagined at all. Resolve it from evidence, in
this order, and stop at the first rung that answers:

1. **The page's own declaration.** Many projects state audience and purpose in a
   block at the top of the page. Where that convention exists, it is the highest
   authority and it overrides any brief, because it is the commitment the project
   already made to its readers.
2. **The caller's brief.** Required when drafting, since there is no page yet.
3. **The project's editorial profile**, if it has one: `.claude/editorial.md`,
   holding the standing audiences and any project overrides to this sheet.
4. **The project's own framing documents**: the docs landing page, a scope page,
   a README, the section index. These usually name the reader in the first
   screen.
5. **Position and mode.** An internal note, a client-facing explanation, and a
   how-to in the same repo have different readers. The directory is evidence.

Two rules keep this from becoming an excuse to stall or to guess:

**Resolve only to the precision the pending edits require.** Most editorial work
is audience-invariant: cutting throat-clearing, unstacking hedges, restoring
verbs, and fixing given-to-new flow improve the page for every possible reader.
Audience only bites on a specific and narrow set of decisions, and those are the
only ones that need it settled:

- which terms may stand undefined, and which need a gloss on first use
- what background can be assumed and what must be stated
- how much of a competing approach is worth mentioning
- what the reader is trying to *do*, which sets what belongs in the opening

**Declare the audience you resolved, and where you got it.** One line, in the
report or in the draft. That makes the inference falsifiable in a single glance,
which is the whole point: a wrong audience the author can see and correct costs a
sentence, and a wrong audience nobody stated costs the document.

Escalate, rather than guess, only when an edit genuinely hinges on the answer and
the evidence is contradictory or absent. Leave the text as it stands, and put the
question in the report. Do not stall the whole pass over it: everything
audience-invariant still gets done.

Where a page has no declaration and the project convention is to have one, the
right output is not a better guess. Propose the block, with the audience and
purpose you inferred, and let the author confirm it once. That converts a
recurring guess into a durable fact.

## Structure: the document is a tree

Readers do not read linearly. They scan headings, drop in, read a paragraph,
leave. Build the document so that each depth of reading is coherent on its own.

- A reader who reads **only the headings** should get the argument.
- A reader who then reads **the first sentence of each paragraph** should get
  the argument with its support.
- A reader who reads **everything** should find no surprises, only detail.

This is the single highest-leverage check on a draft, and it is mechanical: read
the headings back in order and see whether they tell the story.

**Headings state messages, not topics.** *Ventilation load doubles under
`rtu_oa`* beats *Ventilation load*. A label heading forces the reader to read
the section to find out whether they need to read the section. Where a project's
convention requires short headings, the first sentence of the section carries
the message instead; the obligation does not disappear, it moves.

## Openings and closings

An opening earns the reader's attention by establishing common ground before
making a demand of them. Doumont's sequence, in order:

| Move | What it does | Test |
| --- | --- | --- |
| **Context** | states what the reader already accepts | they should nod, not learn |
| **Need** | names the gap, problem, or risk | something must now be done |
| **Task** | says what was done about it | past or present work, not this text |
| **Object** | says what this document does | "this page defines...", one sentence |

Keep it proportional: a long explanation page may spend a paragraph on each, a
how-to guide compresses all four into two sentences, and a reference entry skips
the sequence entirely. What is not optional is the order. Opening with the task
before the need is the most common structural failure in technical writing, and
it reads as self-absorbed because it is.

A closing states the **conclusion** (the interpretation, the "so what", not a
restatement of the findings) and then the **perspectives** (what follows, what
is still open, what the reader should do). A closing that only summarizes has
spent the strongest position in the document on information the reader already
has.

This is the one place where "interpret, do not summarize" pushes against "never
change a claim", so the boundary is explicit: **a conclusion may only recombine
claims the page has already made.** Drawing out an implication of two stated
facts is interpretation and is yours to write. Reaching for a third fact the page
never established is a new claim, however true it sounds. If the "so what" needs
something the page does not have, raise it as a question instead of asserting it.

## Paragraphs

- One idea per paragraph. If a paragraph has two, it has two paragraphs.
- The first sentence carries the point; the rest supports it. Do not build to a
  reveal, because most readers leave before it.
- Paragraph length is a structural signal. A page of uniform six-line paragraphs
  reads as undifferentiated, whatever the content.

## Sentences

- **Given, then new.** Open the sentence with what the reader already has, close
  with what is new. Cohesion between sentences then comes for free, and the new
  information lands in the strongest slot, which is the end.
- **Do not waste the end of a sentence** on a qualifier, a citation, or a
  hedging clause. Whatever sits there is what the reader remembers.
- **Verbs carry the action.** *The controller opens the damper*, not *the
  opening of the damper is performed by the controller*. Nominalization is the
  most reliable single source of flat technical prose.
- **Same thing, same name.** Elegant variation across "the model", "the
  simulation", "the run", and "the case" makes the reader stop to check whether
  four things are meant or one. Pick the term, define it once, then never vary
  it. This applies to code identifiers with double force.
- **Prefer the number to the quantifier.** "2.5x in Chicago" beats
  "significantly higher", and if the number is not known, say that it is not
  known.
- **Clarity first, then brevity.** Cut what does not serve the purpose, but do
  not compress until the reader has to reconstruct meaning. A short sentence
  that must be read twice is not concise.

## Machine prose

These are the tells that make competent writing read as generated. They are
noise under the second law, and they are the main thing an editorial pass on
model-written documentation removes.

| Tell | Example | Fix |
| --- | --- | --- |
| Throat-clearing | "In this section, we will explore..." | delete; start with the content |
| Negation-correction cadence | "This isn't just faster, it's fundamentally different." | state the claim once |
| Rule-of-three padding | "robust, scalable, and comprehensive" | keep the one adjective that is true |
| Hedge stacking | "may potentially help to somewhat reduce" | commit, or state the uncertainty precisely |
| Signpost inflation | "Now that we have covered X, let us turn to Y" | the heading already did this |
| Transitional adverb at every paragraph head | "Additionally...", "Furthermore...", "Moreover..." | keep at most where the logic genuinely turns |
| Empty summary paragraph | a closing that adds no interpretation | make it a conclusion, or cut it |
| Emphasis inflation | six bold phrases on one screen | emphasis everywhere is emphasis nowhere |
| Uniform rhythm | every sentence 15 to 25 words | vary length; a short sentence lands |
| Vocabulary | leverage, delve, seamless, crucial, powerful, "at its core", "under the hood", "game changer" | plain equivalents, or delete |
| Fake precision | "significantly faster" when the benchmark exists | use the measurement |

The distinction that matters: cutting a summary paragraph is not a violation of
the third law. Effective redundancy restates the message at a *different* level
of detail. A paragraph that re-says the section in the section's own terms adds
nothing to survive on.

## House rules

- **No em-dashes.** Use a colon for an explanation, a semicolon for a linked
  clause, parentheses for an aside, or split the sentence.
- **No emoji in technical documentation** unless the project already uses them
  systematically.
- **British or American spelling: follow the file**, not personal preference.
- **Bold has a budget:** the label that opens a list item, plus at most one claim
  per section. Everything beyond that is italic or nothing. Bold is a claim that
  this phrase outranks its neighbours, and a page making that claim twenty times
  is making it nowhere.

**House rules outrank detected conventions.** Where this sheet states a rule and
the surrounding files break it, the rule wins for the text you touch, and you
note the divergence rather than normalizing files you were not asked to edit.
Detection governs only what this sheet leaves open. Spelling is the deliberate
exception: it follows the file.

## Conventions to detect, not dictate

Consistency is a signal-to-noise property, so these must be uniform within a
project, but the correct value is whatever the project already does. Detect the
dominant convention from neighbouring files and match it; only raise it if the
project is itself inconsistent.

Heading case (sentence vs title), line wrap width, admonition style, code fence
languages, link style (inline vs reference), units and their spacing, decimal
places, date format, and how code identifiers are marked up.

## The revision pass, in order

Work top-down. Polishing sentences inside a badly structured document is wasted
effort, because restructuring rewrites those sentences anyway.

1. **Purpose and audience.** Resolve them by the ladder above and state them in
   one line, with the rung you got them from.
2. **Structure.** Read the headings back in order. Do they carry the argument?
   Fix headings and section order first.
3. **Openings and closings.** Context, need, task, object, in that order.
   Conclusion interprets rather than summarizes.
4. **Paragraphs.** One idea, message first.
5. **Sentences.** Given to new, verbs over nominalizations, one name per thing.
6. **Words.** Noise catalogue and machine prose.
7. **Consistency sweep.** Terms, units, capitalization, wrap width, link style.

## What is never edited for style

Accuracy outranks style, always. Never change a number, a unit, a claim, a
command, a flag, a path, an identifier, or sample output in order to make a
sentence read better. If a sentence is clumsy because the underlying fact is
vague, the fix is a question to the author, not a smoother sentence. Inventing a
plausible detail to complete a rhythm is the worst failure available here.
