# Explanation

**Understanding-oriented. The reader is at study, away from the keyboard.**

Explanation is discussion of a topic. It takes a wider view than the other three
modes: not the close-up of reference, not the eye-level of a how-to, but the
perspective from which things connect to each other. It answers "can you tell me
about...?"

It is the only documentation that makes sense to read while not using the
product at all. It is also the mode most often missing, or scattered in
fragments across pages where it interrupts something else.

## Principles

**Bound it with a why-question.** The other three modes get their scope for
free: from what must be learned, what must be done, or what the machinery
contains. Explanation has no natural edges, which is why it is hard to start and
harder to stop. Pick a real question ("why does the object model separate decks
from simulations?") and let it fix the boundary.

**Make connections.** The value here is weaving: relating this thing to that
thing, to adjacent tools, to how the reader already thinks. Reach outside the
immediate topic when the connection earns its place.

**Give context and causes.** Design decisions, historical accidents, constraints
that forced a shape, implications the reader would not derive alone. This is
where "we did it this way because the alternative broke under X" lives.

**Admit opinion and alternatives.** Explanation is discussion, so it can judge,
weigh, and disagree with itself. "Some projects prefer W; that works well when
Z, but it costs you Y." Perspective is honest here in a way it is not anywhere
else in the docs.

**Keep it bounded.** Explanation absorbs neighbours: mid-discussion the urge to
add the command or the parameter list is strong. Resist it. Those things exist
elsewhere, and pulling them in both damages the discussion and hides them from
the readers looking in the right place.

**Do not be urgent.** This mode is less urgent than the others and no less
important. A practitioner without it holds their craft loosely and works
anxiously. That is the case for writing it, and the reason not to apologise for
its existence.

## Language patterns

- "The reason for x is that historically, y..."
- "W is usually better than z, because..."
- "An x here is analogous to a y in <other system>. The difference is..."
- "Some users prefer w. That can work well, but it assumes..."
- "An x interacts with a y as follows..."
- Prose paragraphs. Discussion, not instruction.

## Naming

Titles should read with an implicit *about* in front: *About the object model*,
*Why simulations are cached*, *Design of the deck parser*. If a title reads like
a command or a spec, the page is probably in the wrong mode.

The section itself does not have to be called Explanation. *Discussion*,
*Background*, *Concepts*, and *Topics* are all reasonable, and often land better
with readers.

## Failure checklist

- [ ] Are there numbered steps? Those belong in a how-to.
- [ ] Is there a parameter table or option list? That is reference.
- [ ] Does it drift into teaching the reader to do something? Tutorial.
- [ ] Does the title read with an implicit "about"?
- [ ] Is the scope bounded by an actual question, or does it wander?
- [ ] Does it make at least one connection the reader could not have made alone?
- [ ] Are alternatives and trade-offs acknowledged, or is it one-sided?
- [ ] Would this be readable away from the machine? If not, it is not this mode.

## Shape

```markdown
# About <topic>

<The question this page answers, stated plainly.>

## <Aspect>
<Discussion: context, causes, consequences.>

## Alternatives
<What else could have been done, and what that would cost.>

## See also
- <how-to link> to actually do it
- <reference link> for the exact parameters
```
