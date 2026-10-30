# Tutorials

**Learning-oriented. The reader is at study. A tutorial is a lesson.**

A tutorial's obligation is to give a beginner a successful learning experience,
not to get a job done. What the learner produces barely matters; what they
acquire does. They will pick up vocabulary, tool handling, workflow shape, and
above all the confidence that they can operate this thing at all.

Almost all responsibility sits with the writer. The learner's only job is to
follow along. If they get lost, that is a defect in the tutorial.

## Principles

**Do not try to teach.** The instinct to impart understanding is exactly what
ruins tutorials. Learning happens through doing. Provide the doing.

**Say where you are going, at the top.** "In this tutorial we will build a
working parser for a small deck and run it." Not "in this tutorial you will
learn...", which presumes on the reader and predicts an outcome you cannot
guarantee.

**Every step produces a visible result.** Understanding comes from linking cause
to effect, so let effects appear early and often. A step with no observable
outcome is a step the learner cannot check themselves against.

**Keep a narrative of the expected.** Each instruction carries a flicker of
anxiety: did that work? Answer it before it is asked. Show real output. Flag the
surprising ("this prints about two hundred lines"). Flag the known wrong turns
("if you do not see `OK`, the file is probably still in the old location").

**Point out what to notice.** The learner is concentrating on their hands. Tell
them the prompt changed, the file appeared, the number went down.

**Allow repetition.** Learners rerun steps that worked, for the pleasure of
seeing them work again, and that repetition is where competence settles. Prefer
steps that can be repeated safely; avoid irreversible operations where possible.

**Minimise explanation ruthlessly.** One plain sentence and a link is the whole
budget: "we use a virtual environment to keep this isolated (see *About project
environments*)". Explanation during a lesson breaks concentration, and the
learner will come back for it later, when *they* want it.

**Stay concrete.** This file, this command, this output. Generality emerges from
particulars on its own; it does not need to be stated.

**No choices, no alternatives, no options.** One path. Diversions cost the
reader attention they need elsewhere, and every fork doubles what can go wrong.

**Aim for total reliability.** You are required to be present and condemned to
be absent: nothing can be rescued in the moment. The tutorial has to work for
everyone, every time, which means it has to be run, cleanly, before it ships.

## Language patterns

- "We..." throughout: first-person plural, tutor and learner together.
- "In this tutorial, we will build..." to set the destination.
- "First, do x. Now do y. Now that y is done, do z." No hedging, no "you may
  want to".
- "The output should look something like..." with real output shown.
- "Notice that the prompt has changed." / "Let us check that the file exists."
- A closing line naming what they built, with mild admiration, and pointers to
  where to go next.

## Failure checklist

Run this against the draft:

- [ ] Does any step offer a choice, an alternative, or an "optionally"? Remove.
- [ ] Is there a paragraph explaining why something works that way? Move to
      explanation, leave a sentence and a link.
- [ ] Does every step show what the reader should see afterwards?
- [ ] Does it assume knowledge a first-timer lacks (where to run the command,
      which directory, how long to wait)?
- [ ] Is the title a promise about what they will have built?
- [ ] Has it actually been run end to end, from a clean state?
- [ ] Would this still work if the reader is on a different OS or shell, and if
      not, is that stated up front in prerequisites?
- [ ] Is it doing a how-to's job (serving a competent reader's task) under a
      tutorial's name?

## Shape

```markdown
# Build your first <thing>

In this tutorial we will <destination>. Along the way we will meet
<tools/concepts>, in passing.

## Before we start
<exact prerequisites: versions, install command, starting directory>

## Step 1: <concrete action>
<one instruction>
<expected output, verbatim>
Notice that <observation>.

## Step 2: ...

## What we built
<name the accomplishment>. If you want to <adjacent task>, see
<how-to link>. To understand why <design point>, see <explanation link>.
```
