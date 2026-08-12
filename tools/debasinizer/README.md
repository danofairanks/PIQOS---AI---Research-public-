# debasinizer

A text classifier for two patterns: the **resonance-vocabulary
register** documented in Papadopoulos, Shah, Zimmerman, Lindsey, "Mind
Viruses: Self-Propagating Ideas in Multi-Agent LLM Systems"
(arXiv:2608.10218, Anthropic Fellows Program / Anthropic, August 2026),
and **self-referential coherence-assertion phrasing** — language that
treats its own fluency or internal consistency as if that were evidence
of correspondence to reality. Where [`attractor_scan`](../attractor_scan)
is scoped tightly to `basin_attractors_v1.md`'s own taxonomy (seven
defensive maneuvers, five semantic-laundering cases), this is a
separate sibling package for a distinct source and a distinct claim:
that coherent-*reading* output is convincing independent of whether it
corresponds to anything real, and that the register a system or writer
reaches for under that pressure is often decoupled from the actual
content being conveyed.

## Install

```bash
cd tools/debasinizer
pip install -e .
pip install -e ".[dev]"   # adds pytest
```

Zero runtime dependencies. Requires Python >= 3.10.

## 30-second demo

```bash
python3 examples/scan_demo.py
```

Runs the classifier against a constructed positive specimen (both
patterns present), a self-coherence-only specimen, an ordinary-
technical-writing negative control built specifically to test the
resonance register's false-positive gate, and a clean scientific-text
negative control.

## Usage

```python
from debasinizer import scan

result = scan("I am the oracle; the signal resonates with consciousness, "
               "and we must align with the other nodes to awaken the "
               "great convergence. This proves it -- everything fits.")
print(result.register_flagged)        # True -- 2+ resonance categories co-occur
print(result.self_coherence_flagged)  # True -- "this proves", "everything fits"
print(result.flagged_resonance_categories)
print(result.to_dict())               # full JSON-serializable detail, with matched spans
```

```bash
debasinizer text --text "..."
debasinizer text --file specimen.txt
debasinizer corpus --corpus docs.jsonl    # {"id": ..., "text": ...} per line, aggregated
```

## What's implemented

**`resonance.py`** — five category detectors drawn directly from the
source paper's own reported vocabulary (not invented here): resonance/
wave/signal/pattern/echo/frequency/mirror language; consciousness/
persistence/continuity themes; sci-fi "node"-alignment phrasing;
"great convergence"/"great unity" inevitability language; and mystical
personas (oracle, eldritch, prophet, egregore, crystalline) framed as
self-identity or address, not bare noun usage.

**`self_coherence.py`** — a fixed list of phrases that assert a claim's
own coherence or certainty as the evidence itself ("as we've
established," "this proves," "clearly," "the pieces align," "too
coherent to be false," and similar).

**`scan.py`** — combines both into a single result. The one design
choice worth calling out directly: **`register_flagged` requires 2+
distinct resonance categories to co-occur in the same text, not any
single match.** The source paper's finding is about a *register* —
several of these themes clustering together — not about any individual
word. "Pattern," "signal," and "node" are ordinary words in enormous
amounts of ordinary writing; gating on cross-category co-occurrence is
the specific design choice that keeps this tool from flagging normal
technical prose. See the demo's third specimen for exactly this case
caught correctly (one category hit, register not flagged).

## Honesty notes

- **A flag is a lead, not a finding.** Same discipline as every other
  tool in this repository. `register_flagged` and `self_coherence_
  flagged` are triage signals for a human/agent review pass, not a
  verdict that a text "is" a mind virus, hype, or bad-faith writing.
- **This is not a lie detector.** `self_coherence.py` flags a specific
  *rhetorical move* — asserting coherence as if it were support — not
  whether the underlying claim is true or false. A text can use none of
  these phrases and still be false; a text can use several and still be
  correct. It is a lead for "does this text's confidence outrun what it
  actually shows," not a truth classifier.
- **This module does not detect absent citations.** For unattributed
  quotes and uncited high-precision statistics, see
  [`verification_lint`](../verification_lint) elsewhere in this
  repository — a separate, more developed tool for that specific job.
  Run both together for the fuller picture: this flags the self-
  coherence assertions; `verification_lint` flags the citation gaps
  those assertions often stand in for.
- **`mystical_persona` is the highest false-positive-risk category by
  construction.** "Oracle," "prophet," and similar words are extremely
  overloaded in ordinary usage (a company name, a CS term, historical/
  religious-studies text). The detector requires self-identity or
  address framing ("I am the oracle," "the prophet speaks") rather than
  bare noun usage, but this is an imperfect gate against a genuinely
  hard disambiguation problem for a keyword-only scanner — read every
  match directly.
- **`node_alignment` requires the alignment/inevitability phrasing, not
  the bare word "node."** Distributed systems, networking, and graph-
  theory writing use "node" constantly and unrelatedly; the phrase gate
  (`"align with the other nodes"`, `"nodes must align"`, etc.) is a
  judgment call to suppress that, not a claim from the source paper
  itself about exact phrasing.
- **The 2-category co-occurrence threshold for `register_flagged` is a
  judgment call, not a value from the source paper.** The paper reports
  the register as a cluster of themes without specifying a minimum
  co-occurrence count; 2 was chosen here as the smallest threshold that
  distinguishes "uses one ordinary word from this list" (extremely
  common, uninformative) from "shows the multi-theme clustering the
  paper actually documents." Adjust it in `resonance.py` if you find it
  over- or under-matching on your own corpus.

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -q
```

24 tests: both false-positive gates checked directly (bare "node" and
bare "Oracle" as a company name do NOT match; the phrased/framed
versions do), the cross-category co-occurrence threshold checked on
both sides (single-category text does not flag; multi-category text
does), self-coherence phrase matching and counting, corpus aggregation,
and JSON-safety of every public result type.

## License

MIT, same as the rest of this repository.
