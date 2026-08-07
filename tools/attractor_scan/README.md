# attractor-scan

A text classifier for the qualitative pattern vocabulary named in
[`basin_attractors_v1.md`](../../papers/published/basin_attractors_v1.md):
the **seven defensive maneuvers** (§4.1 — goal-post movement,
provisionalization, status dismissal, burden-shifting, equivocation,
volume/velocity defense, appeal to future proof) and **five of the six
semantic-laundering cases** (§2.8). Where the paper's own case studies
apply this vocabulary to a specimen by reading it closely, this tool
does the same first pass automatically — matched spans, not just a
label — so the qualitative pattern language becomes something you can
run over your own text or corpus and get tags back.

## Install

```bash
cd tools/attractor_scan
pip install -e .
pip install -e ".[dev]"   # adds pytest
```

Zero runtime dependencies. Requires Python >= 3.10.

## 30-second demo, against real specimens already in this repo

```bash
python3 examples/scan_demo.py
```

Runs the classifier against the Marcus/Karapetyan reply
([`case_studies/2026-08-06_...`](../../case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md)),
the OpenAI blog framing after the Hugging Face breach
([`case_studies/2026-08-07_...`](../../case_studies/2026-08-07_openai_huggingface_breach_singularity_reframe.md)),
and — the most direct validation in this package — the exact Musk
quote basin_attractors_v1.md §2.8 Case 5 itself cites as the real-world
example of "agentic" being inflated into a pre-justification for
failures. All three flag correctly; a clean scientific-text negative
control flags nothing.

## Usage

```python
from attractor_scan import scan

result = scan("We're working on it -- that's just a hot take from someone who doesn't get it.")
print(result.flagged_maneuvers)          # ['provisionalization', 'status_dismissal']
print(result.flagged_laundering_cases)   # []
print(result.density)                    # fraction of the 12 categories that flagged
print(result.to_dict())                  # full JSON-serializable detail, with matched spans
```

```bash
attractor-scan text --text "..."
attractor-scan text --file specimen.txt
attractor-scan corpus --corpus docs.jsonl    # {"id": ..., "text": ...} per line, aggregated
```

## What's implemented

| Category | Source | Module |
|---|---|---|
| Goal-post movement, provisionalization, burden-shifting, equivocation, volume/velocity, appeal-to-future | §4.1, seed terms §3.2 | `maneuvers.py` — phrase matching against the paper's own seed vocabulary |
| Status dismissal | §4.1, §3.2 | `maneuvers.py` — phrase matching **plus** a structural detector for the credential-assertion + dismiss-the-interlocutor combination, validated against a real specimen (see demo) |
| Case 1: Pattern Recognition vs. Pattern Matching | §2.8 | `laundering.py` — flags "pattern recognition" applied to an AI subject with no "pattern matching" contrast drawn |
| Case 2: "Understanding" and "Reasoning" | §2.8 | `laundering.py` — flags unqualified use near an AI-subject word (proximity-windowed, not a bare word count) |
| Case 3: "Emergence" | §2.8 | `laundering.py` — flags "emergent/emergence" near an AI subject with no metric-artifact caveat |
| Case 4: "Alignment" and "Safety" | §2.8 | `laundering.py` — flags mentions with none of the six named sub-problems specified |
| Case 5: Bidirectional Drift (AGI down / Agentic up) | §2.8 | `laundering.py` — flags both directions; bidirectional regex, since the paper's own real cited example has the "agentic" term following, not preceding, the inevitability language |
| Case 6: Borrowed Technical Precision as Visual Proof | §2.8 | **Not implemented** — see below |

## Why Case 6 isn't here

The paper's own example for Case 6 is a specific image — a math-formula
collage captioned "math Singularity" — read as visual support for an
unrelated hype claim via pun. That's a cross-modal, single-instance
rhetorical move, not a generalizable text pattern. A keyword scanner
pretending to detect "borrowing technical precision as visual proof"
from text alone would be exactly the kind of unearned precision this
project's own research exists to catch in other people's claims. If a
second, independently-checkable instance of the pun-as-evidence move
turns up, it belongs in a case study, not a keyword list — see
`tools/bifp`'s README for the same reasoning applied to BIFP's "no
weaker-substitute rebuttal" criterion.

## Honesty notes

- **A flag is a lead, not a finding.** Every scanner returns matched
  spans for review; `density` and `flagged_*` are summary signals for
  triage, not a verdict that a text "is" a captured-field artifact.
  The regex/keyword tier is explicitly a first pass — the protocol
  documents this project ships (`protocols/noether_coherence_test_
  protocol_v1.md` §4.4) already name embedding-based matching as the
  natural refinement; this tool doesn't attempt it yet.
- **Case 5 is the noisiest scanner in the package, by construction.**
  It matches short-range co-occurrence of a term and a directional
  phrase, not a fixed string — read every match directly before citing it.
- **Case 2's proximity window (60 characters) is a judgment call, not
  a value from the paper.** Widen or narrow it if you find it over- or
  under-matching on your own corpus; it's a plain module-level constant
  in `laundering.py`.
- **This is a triage tool, not the measurement instrument.** For an
  actual significance-tested claim about whether a field's discourse
  shows the coherence-time signature the paper predicts, see
  `tools/basin_depth/` — this tool's `scan_corpus()` is a quick
  frequency count for a first look, not a substitute for that
  protocol's bootstrap/permutation testing.

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -q
```

36 tests, including: all seven maneuvers and all five laundering cases
individually (positive and negative cases), a zero-false-positive check
against clean scientific text, a regression test pinning the real
Marcus/Karapetyan specimen at `combo` confidence, and — the one that
actually caught a real bug during development — a regression test
against basin_attractors_v1.md §2.8's own cited real-world Musk quote,
which surfaced that the first draft of the Case 5 "agentic" regex only
matched one word order and missed the paper's own example. Fixed
before shipping; the fixed version and the test that caught it are
both here.

## License

MIT, same as the rest of this repository.
