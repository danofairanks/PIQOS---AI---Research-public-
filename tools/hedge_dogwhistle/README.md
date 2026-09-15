# hedge-dogwhistle

A detector for **paralipsis** (also apophasis) — raising a claim by
formally declining to raise it, "I'm not saying X" that installs X in
the reader's mind while giving the speaker deniability for having
claimed it — plus a mechanized first step of a falsifiable **removal
test** for telling a genuine, honest scope-limiting hedge apart from
one functioning as coded signal: does the reader's association with the
disclaimed content survive deleting the disclaiming sentence entirely?

Distilled from an operator's own framing: hedging that on one hand says
"I'm not saying," while on the other hand functions as "pay close
attention to what I'm not saying" — a dog whistle, where the disclaimed
content is signal that arrives only through the denial, legible to
whoever is primed to read it and deniable to whoever isn't. No named
individual or specimen from this project's private tracking is
reproduced here; every constructed example below is synthetic.

## Install

```bash
cd tools/hedge_dogwhistle
pip install -e .
pip install -e ".[dev]"   # adds pytest
```

Zero runtime dependencies. Requires Python >= 3.10.

## 30-second demo

```bash
python3 examples/scan_demo.py
```

Runs the detector against a constructed positive-shaped candidate (the
disclaimed content appears only inside the hedge — removing it deletes
the content entirely), a constructed negative-shaped candidate (the
disclaimed content is *also* stated directly and unhedged elsewhere —
removing the hedge leaves it fully intact), a clean negative control,
and one deliberately-undetected insinuation example that lacks a denial
structure (see "What this tool does NOT detect" below).

## Usage

```python
from hedge_dogwhistle import scan

result = scan(
    "The new policy passed unanimously. I'm not saying it's connected "
    "to last week's scandal, but the timing is interesting."
)
print(result.has_paralipsis)             # True
print(result.text_with_hedges_removed)   # "The new policy passed unanimously."
print(result.to_dict())                  # full JSON-serializable detail, with matched spans
```

```bash
hedge-dogwhistle text --text "..."
hedge-dogwhistle text --file specimen.txt
hedge-dogwhistle corpus --corpus docs.jsonl    # {"id": ..., "text": ...} per line, aggregated
```

## What's implemented

**`paralipsis.py`** — a phrase bank of classical denial-structure
openers ("I'm not saying," "far be it from me to," "not to suggest,"
"no comment on whether," "I'm not implying," "I'm not accusing," and
similar), each match paired with the (naively split — see
`sentences.py`) sentence that contains it.

**`removal_test.py`** — the mechanical half of the operator's own
proposed falsifiable test: take every sentence containing a paralipsis
match and delete it, returning what remains. **This is the part a
regex tool can actually do.** The judgment call the test is actually
for — does the disclaimed content's association survive that removal,
because it was already established elsewhere unhedged, or does it
disappear because the hedge was the only place it appeared — is left to
whoever reads `text_with_hedges_removed` next (a human, or an agent
told to make that specific read). See the two constructed demo
specimens for both outcomes, mechanically produced.

**`sentences.py`** — a small, honestly-scoped regex sentence splitter
(period/question/exclamation mark + whitespace + capital/digit/quote).
Not a real NLP sentence boundary detector; see its own docstring for
exactly where it will mis-split (abbreviations like "Dr." or "U.S.").

## What this tool does NOT detect

**Insinuation without a denial structure** — "the numbers are odd, make
of that what you will," "I'll let you draw your own conclusions" — is a
related but distinct rhetorical move. Paralipsis specifically declines
to state something while stating it; these phrases invite an inference
without ever formally raising and declining anything. Out of scope by
design, not a recall gap; see the demo's fourth specimen.

## Honesty notes

- **A flag is a lead, not a verdict.** Finding a paralipsis construction
  says nothing on its own about whether that instance is a dog whistle
  or ordinary, honest epistemic hygiene (a real scope-limit on a claim
  already made openly). That is exactly what the removal test is for —
  and this tool only mechanizes the removal step, not the judgment.
- **This is not a semantic tool.** It cannot determine what "X" refers
  to in "I'm not saying X," and it cannot search the remaining text for
  a paraphrase of that content stated in different words. It can only
  tell you, mechanically, what text remains after the hedge sentence is
  gone — read that output and reason about it yourself (or hand it to
  an LLM agent with the specific instruction to check whether the
  disclaimed content survives).
- **The sentence splitter is naive by design, not by oversight.** See
  `sentences.py`'s own docstring. For short-form argumentative text
  (LinkedIn posts, comments) it behaves well in practice; abbreviation-
  heavy or unusually punctuated text can mis-split. Read the `sentence`
  field of any match directly before trusting a removal.
- **The phrase bank favors precision over recall.** Each entry is a
  fairly specific denial-structure opener, not a broad word list —
  closer in spirit to `attractor_scan.claim_boundary`'s phrase-list
  approach than to `debasinizer.resonance`'s broader, cross-category-
  gated word categories. A genuine paralipsis construction phrased
  differently from every entry here will be missed; that's a recall
  gap worth knowing about, not a claim that the list is exhaustive.

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -q
```

Checks phrase matching across the bank (including a negative control
for the deliberately-excluded insinuation-without-denial phrasing),
sentence-containing-a-match extraction, the mechanical removal
behavior on both a constructed positive-shaped and a constructed
negative-shaped specimen (content deleted vs. content surviving because
it's stated elsewhere, unhedged), span-merging for overlapping/adjacent
removals, corpus aggregation, and JSON-safety of every public result
type.

## License

MIT, same as the rest of this repository.
