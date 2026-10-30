# Reference

**Information-oriented. The reader is at work and needs a fact, fast.**

Reference describes the machinery. It is consulted, not read. Its job is to be
the firm ground a working reader stands on, which means it must be austere,
neutral, exhaustive within its scope, and utterly reliable.

Unlike tutorials and how-to guides, reference is led by the product rather than
by user needs: its shape is the shape of the code.

## Principles

**Describe, and only describe.** Neutral description is unnatural to write. The
pull toward instructing, explaining, and opining is constant, and every
concession dilutes the page. When the urge arrives, link instead.

**Mirror the structure of the code.** The value of a map is that it corresponds
to the territory. Documentation organised like the codebase lets the reader move
through both at once, and makes gaps conspicuous. Do not distort either side to
force the match; just let the code's own conceptual arrangement lead.

**Be consistent to the point of monotony.** Every entry in the same order, the
same headings, the same phrasing. Reference is consulted under time pressure and
peripherally: readers find things by shape. This is the one place where varied
vocabulary and stylistic range are actively harmful.

**Show examples, but keep them illustrative.** A one-line usage example conveys
context cheaply. The moment it becomes a walkthrough it is a how-to and belongs
elsewhere.

**State constraints and warnings plainly.** Limits, error conditions, valid
ranges, thread-safety, units, defaults. These are facts about the machinery and
they belong here.

**Generate where you can.** For Python APIs, mkdocstrings pulls reference
straight from docstrings, which makes drift structurally impossible. Prefer
improving docstrings over hand-writing an API page that will rot. Hand-written
reference is for things with no code to introspect: file formats, CLI grammar,
configuration keys, wire protocols, error codes.

## Language patterns

- "`Deck.parse()` returns a `Deck`. It raises `ParseError` if the input contains
  an unterminated block."
- "Valid values are: `a`, `b`, `c`. The default is `a`."
- "Units are kWh. Values are not rounded."
- "You must call `close()` before reuse. Do not call `close()` twice."
- Present tense, third person, no "we", no "you should probably".

## Failure checklist

- [ ] Is there a sentence of rationale, history, or design opinion? Move to
      explanation.
- [ ] Is there a task walkthrough? Split it into a how-to.
- [ ] Does every comparable entry follow the same template?
- [ ] Are defaults, units, valid ranges, and raised exceptions stated?
- [ ] Does the page order match the code's structure?
- [ ] Is anything asserted that was not verified against the source?
- [ ] Could this have been generated from docstrings instead of typed by hand?
- [ ] Is anything ambiguous or hedged? Reference must be authoritative.

## Shape

Per entry, in a fixed order:

```markdown
### `function_name(arg, *, option=default)`

<One-sentence statement of what it does.>

**Parameters**
- `arg` (`Type`): <description>. <constraints>.
- `option` (`Type`, default `default`): <description>.

**Returns**
`Type`: <description>.

**Raises**
- `SomeError`: <condition>.

**Example**
```python
>>> function_name(x)
<output>
```
```
