# How-to guides

**Goal-oriented. The reader is at work, already competent, mid-task.**

A how-to guide directs work. It assumes the reader knows what they want and can
follow instructions without hand-holding. Its obligation is to get them to a
correct result safely, in the real world, where conditions vary and things go
wrong.

The list of how-to guides also advertises what the product can do, which is why
a rich set of them is usually the most-read part of any documentation.

## Principles

**Address a human problem, not a machine operation.** The test is whether the
title names something a person needs to accomplish. "How to keep simulation
outputs reproducible across machines" is a problem. "How to use the `--seed`
flag" is the machinery going through its motions, and offers almost nothing:
anyone competent enough to be here can read the flag list.

Guides driven by the tool's surface produce a suspiciously tidy set of pages
that mirror the API and answer no actual question. Guides driven by user
problems often cut across several parts of the system, which is a good sign.

**Assume competence.** No teaching, no familiarisation, no explaining what a
virtual environment is. If a prerequisite skill is genuinely missing, link to
the tutorial.

**Usable beats complete.** A tutorial must be end to end; a how-to may start and
end anywhere reasonable and leave the reader to join it to their own work.

**Be adaptable.** A guide that works only for one exact case is nearly useless.
Say what varies and how to judge it, so the reader can map it onto their
situation.

**Branch where reality branches.** Real problems fork. Conditional imperatives
are the native grammar here: "if the model is already meshed, skip to step 4";
"for a batch run, do y instead". A how-to is not obliged to be a straight line.

**Sequence for flow.** Order by how the work actually proceeds, not by how the
system is organised. Watch for context-switching, held-open thoughts, and forced
backtracking. The best guides feel like they anticipate the reader's next reach.

**Prepare for trouble.** Unlike a tutorial, you cannot promise safety. Flag
destructive steps before they happen, note what cannot be undone, and say what
the failure looks like.

**Include judgement, not just keystrokes.** Deciding is part of doing. Telling
the reader what to look at and how to weigh it is legitimate how-to content.

## Language patterns

- "This guide shows you how to..."
- "If you want x, do y. To achieve w, do z."
- "For the full list of options, see the <reference> page."
- "Check that <condition> before continuing; if it is not true, <alternative>."
- Imperative verbs, no "we".

## Failure checklist

- [ ] Does the title name a real problem someone has, and start with "How to"?
- [ ] Is there a Background or Introduction section? The reader is mid-task:
      move it to explanation.
- [ ] Is it teaching? Familiarising? Reassuring? That is a tutorial's job.
- [ ] Does it exhaustively list options and parameters? Link to reference.
- [ ] Does it work only for the single narrow case the writer had in mind?
- [ ] Are destructive or irreversible steps flagged *before* they are taken?
- [ ] Is it really a description of one function's behaviour dressed up as a
      task? Merge it into reference.
- [ ] Would a competent reader hit an unstated assumption partway through?

## Shape

```markdown
# How to <accomplish the goal>

This guide shows you how to <goal>. It assumes <starting condition>.

## Steps
1. <action>
2. If <condition>, <action>. Otherwise, <alternative>.
3. <action>
   Warning: <irreversible consequence>, so <precaution>.

## Verify
<how the reader knows it worked>

## Related
- <reference link> for the full option list
- <explanation link> for why <design point>
```
