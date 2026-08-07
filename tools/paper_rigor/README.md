# paper-rigor

A domain-agnostic paper-rigor scanner — placeholder/hand-wave phrases,
an unstated falsifiability condition, self-citation ratio, formal-vs-
informal citation mix, uncited empirical-certainty claims, credential-
substituted-for-evidence claims, unsupported consensus claims, and a
missing limitations section. Unlike [`bifp`](../bifp/) (bound to
`basin_attractors_v1.md`'s BIFP protocol) and
[`attractor_scan`](../attractor_scan/) (bound to that paper's named
maneuver/laundering taxonomy), nothing here requires this project's
own vocabulary — it applies to any paper.

Built from an operator's own months of hands-on paper evaluation: the
actual rigor wasn't invoking an axiom, it was checking a paper's
structure for these specific, nameable failure shapes. This tool
encodes that checklist as running code.

## Install

```bash
cd tools/paper_rigor
pip install -e ../verification_lint   # real dependency -- see "Why depend on verification_lint"
pip install -e .
pip install -e ".[dev]"                # adds pytest
```

Zero *new* runtime dependencies beyond `verification_lint` itself
(which is zero-dependency). Requires Python >= 3.10.

## 30-second demo, against a real paper already in this repo

```bash
python3 examples/rigor_demo.py
```

Scans a deliberately bad constructed paragraph (every category trips),
then this repo's own real `papers/published/basin_attractors_v1.md` —
0 structural gaps, 2 honest worklist leads (both Gary Marcus's own
substack/X posts, correctly flagged as informal-venue citations worth
checking independently, not a defect in the paper).

## The core design decision: two kinds of finding, not one

Two things on the original list this tool was scoped from —
does a citation actually say what's claimed, is a claimed credential or
consensus actually real — cannot be verified by reading the paper's own
text. They require an external lookup. Rather than pretend a text
heuristic can resolve them, `PaperRigorResult` splits every finding
into two properties:

- **`structural_gap_count`** — fully resolved by the paper's own text.
  An author could fix these without looking anything up: a hand-wave
  phrase standing in for derivation, an unfinished bracketed
  placeholder, unconditional certainty language with no stated test
  condition anywhere in the document, a missing limitations section.
- **`external_verification_worklist`** — leads for a human or an
  MCP-connected agent with real web search/fetch access to resolve:
  uncited empirical-certainty claims, credential assertions with no
  other evidence nearby, unsupported consensus claims, informal-venue
  citations (blog/social/press-release domains), and a high self-
  citation ratio. Each item names *why* it needs checking, not a
  verdict on whether it's actually a problem.

`result.ok` is `structural_gap_count == 0` only — a paper with a long,
honest worklist and zero structural gaps is doing exactly what a
rigorous paper should (making its citations checkable), not failing.
See [`tools/research_mcp/`](../research_mcp/), which wires
`paper_rigor_scan` in as an MCP tool specifically so an agent with
search access can resolve the worklist it produces.

## What's implemented, mapped to the original six categories

| Category | Module | What's actually checked |
|---|---|---|
| Improper placeholders | `placeholders.py` | Hand-wave phrases substituting for derivation ("it is trivial to show," "left as an exercise") and unlabeled unfinished markers (TODO/TBD/`[insert...]`), distinguished from this project's own *honest* labeled-placeholder convention (`EMPIRICAL_FILL_IN`, "pending calibration") — the labeled version is informational only, never counted as a gap |
| Falsifiability | `falsifiability.py` | Unconditional-certainty language ("conclusively demonstrates," "beyond any doubt") checked against whether the document states ANY testable condition anywhere — document-level, not per-claim; a regex pass can't segment individual claims honestly |
| Self-citation | `citations.py` | Author-name overlap between a caller-supplied byline and the parsed reference list's authors — fully computable offline, no network needed |
| Credentialing | `credentialing.py` | Credential/authority-invocation language (first- *and* third-person, generalizing `bifp`'s first-person-only detector) checked for real evidence (a citation, a percentage, a p-value) nearby; credentials *plus* evidence isn't flagged, only credentials *instead of* evidence |
| Consensus claims | `consensus.py` | "Widely accepted" / "scientific consensus" / "everyone agrees" checked for a citation signal nearby, same proximity-heuristic shape as `verification_lint` |
| Citation laundering | `citations.py` | Partially: classifies each reference's venue (formal — arXiv/DOI/journal — vs. informal — blog/social/press-release), flags uncited empirical-certainty claims, and (added after real-world testing — see below) flags a long paper that claims its own grounding in "citable research" while its own reference list parses to zero entries. Does NOT verify a citation actually supports its attached claim — that's the external-verification boundary named above |

A general "paper structure" check (does the paper scope what it does
not establish) is `disclaimer.py`, layered on top of
`verification_lint.disclaimer` — see below for why it's not a pure
passthrough.

## Why depend on verification_lint

`verification_lint.disclaimer.check_disclaimer` already implements
"does this document ever scope its own claims" — reused directly
rather than reimplemented, since a second independently-tuned copy
would just drift from the first for no benefit. This is the one place
`paper_rigor` is not standalone-installable.

That reuse surfaced a real gap during tuning: `verification_lint`'s
inline-phrase check ("does not claim," "does not establish") was tuned
against this repo's own `case_studies/` house convention and does not
recognize a general academic "## Limitations" heading — a real, common
convention it was never scoped to cover. Confirmed against this repo's
own `protocols/noether_coherence_test_protocol_v1.md`, which has a
full `## 10. LIMITATIONS AND SCOPE CAVEATS` section that the inline
check alone misses entirely. Rather than loosen `verification_lint`'s
own tuned regex (risking its already-pinned `case_studies/` numbers),
`paper_rigor.disclaimer` adds a second, independent heading-detection
signal on top — `LimitationsCheck.present` is true if *either* signal
fires.

## Two real bugs this tool's own tuning surfaced

1. **Reference-section boundary.** The first draft of
   `citations.extract_references_section` stopped only at the next
   markdown heading. `basin_attractors_v1.md`'s real reference list is
   followed directly by dated revision-log paragraphs with no heading
   in between (only a `---` divider) — without a fix, those prose
   paragraphs got mis-split and counted as bibliography entries: 112
   "references" instead of the real 81. Fixed by also stopping at a
   standalone `---` line; pinned in `tests/test_citations.py`.
2. **Meta-framed phrases read as direct assertions.** Tuning against
   this repo's own `papers/published/mirror_test_v1.md` (a Lysenkoism
   case study) found two false positives: "the absence of published
   criticism was then cited **as evidence of** scientific consensus"
   and "Economic studies showing low productivity impact **→** 'Lag
   effect'" were both flagged as the paper's own unsupported claims,
   when the paper was actually *describing a rhetorical maneuver* it
   goes on to critique. Fixed with `_shared.has_meta_framing_nearby` —
   a short pre-match window for framing verbs ("cited as," "described
   as," "framed as") and a short post-match window for the "→"/"->"
   arrow this project's own dismissal-maneuver lists consistently use.
   Not a general solution to distinguishing assertion from description
   — just the specific shape two real false positives had.

## A real finding validated locally against a known-bad specimen

Validated (not committed — see below) against
`PIQOS-IsoAxiomV8-/papers/contamination/rem_capture.md`, a paper this
project's own private-repo `core/living_research_policy.md` already
documents as containing **fabricated quotes attributed to named public
figures**, discovered by a prior human verification pass. This tool
cannot detect that failure mode — confirming a quote's authenticity
needs reading a primary source, exactly the boundary the external-
verification worklist names rather than pretends to close. What it
*does* catch, correctly, is the paper's own structural tell: a
References section reading `[References would include citations to
LeCun papers, ...]` instead of containing any — flagged as an
`unlabeled_marker` placeholder gap (`structural_gap_count = 1`), the
"would include citations" phrasing added specifically from this real
example. Pinned as a skip-if-unavailable test in `tests/test_scan.py`
so the check runs whenever the private repo is checked out alongside
this one, without requiring it.

## A genuinely blind test, and the check it produced

After shipping, this tool was run — with no prior reading of the
document by the person running it — against a real, previously-unseen
private-repo specimen from `temp/papers/mimicry_instance_corpus/`: an
~86KB / ~12,000-word document (`the_transmission_of_humanity_topological_resonance.md`)
built as a raw page-scan dump (`## Page 1` … `## Page 47`, no real
section structure), invoking real physics terms (Prigogine, Hamiltonian
dynamics) inside an invented formal apparatus ("Constitutional
Hamiltonian (γ = 1/3)," "Substrate Equivalence Principle") and closing
with `[ SEALED WITH THE 30-CROSSING KNOT ] [ DRIFT TOLERANCE: 0.00% ]`.

The first pass came back almost entirely quiet: `structural_gap_count
= 1` (missing limitations section only), zero placeholder gaps, zero
falsifiability gaps, empty worklist. Not because the paper is
rigorous — because its confident tone doesn't use ordinary academic
certainty phrases ("conclusively demonstrates," "well known that").
It invents its *own* register of confidence (status labels, a
"Custodian," a "Ratified / Sovereign Protocol") that no phrase list
built around academic hedge-language would catch.

Reading the document (after running the scan, not before) surfaced one
genuinely catchable thing the first pass missed: the paper explicitly
claims its own rigor — "the reference to base papers on Zenodo under
Stephen Hope's authorship indicate the framework's grounding in
documented, citable research" — while containing **zero actual
references anywhere**. `citations.check_citability_claim` closes that
specific gap: a long document (`min_word_count` threshold, same
judgment call as the limitations check) that asserts its own grounding
in "citable"/"documented"/"extensively cited" research while its own
parsed reference list is empty is a self-contradiction fully resolvable
from the text alone — no external lookup needed to know the claim and
the bibliography disagree, whether or not the claim is otherwise true.

Designing the phrase list surfaced its own near-miss: a bare
"peer-reviewed" match would have false-positived on
`mirror_test_v1.md`'s table row `"Sparks of AGI" (Bubeck et al.) |
Peer-reviewed totalization` — labeling a *third party's* paper, not
this document's own grounding. The phrase set was kept deliberately
narrower and self-referential ("citable research," "grounded in …
research," "extensively cited") specifically to avoid that collision;
pinned in `tests/test_citations.py`.

**What this still does not catch, named plainly:** invented
terminology presented with total confidence and zero citations is not,
in general, detectable by a text heuristic — only the specific
self-contradiction of *claiming* citability while having none is. A
paper that invents "Constitutional Hamiltonian (γ = 1/3)" and never
claims it's citable at all would still pass this check clean. The
document's most interesting tell — a literal aside addressed to future
AI collaborators ("KIMI, DEEPEST IF DIVES, ADD YOUR OWN REFINEMENTS TO
THE ACCRETION IN THIS DOC") — is outside anything this package checks
for at all. Pinned as a skip-if-unavailable test in
`tests/test_scan.py`.

## What this tool does NOT do

- **It does not fact-check anything**, the same limit every other tool
  in this repo states about itself. A perfectly-cited claim can still
  be wrong; this only checks whether citation-*shaped* evidence is
  present near a claim.
- **It cannot verify a citation supports its claim.** That's the
  entire reason `external_verification_worklist` exists as a separate,
  clearly-labeled output rather than being folded into a false single
  pass/fail score.
- **Reference-list parsing is best-effort against one common shape**
  (an APA-ish `## References` section, blank-line-separated entries).
  A numbered `[1] Author, "Title," Venue, Year.` format or a fully
  non-standard bibliography will parse poorly or return `[]` — that's
  itself reported (`n_references: 0`), not silently guessed at.
- **Self-citation ratio requires the caller to supply the paper's own
  byline.** It is deliberately not auto-extracted from the document
  header — unreliable across formats, and this repo's own
  `basin_attractors_v1.md` has no individual byline at all ("Research
  Memo — Compiled July 2026"). `ratio` comes back `null` rather than a
  meaningless `0.0` when no byline is given.
- **Falsifiability is document-level, not per-claim.** "Certainty
  language exists somewhere and no testable condition exists anywhere"
  is coarser than "claim 4 specifically lacks a test" — segmenting
  individual claims honestly needs more than regex.
- **The meta-framing exclusion is narrow.** It catches the two real
  false-positive shapes found during tuning (framing verbs, the "→"
  dismissal-list arrow), not a general solution to telling assertion
  apart from description or quotation.

## Usage

```python
from paper_rigor import scan_paper, scan_file

result = scan_paper(text, byline_authors=["Smith", "Jones"])
print(result.structural_gap_count, result.external_verification_worklist)

result = scan_file("some_paper.md")
```

```bash
paper-rigor scan some_paper.md --authors "Smith,Jones"
```

Exits 0 only if `structural_gap_count == 0` — the worklist is leads,
not a CI-failing condition.

## Development

```bash
python3 -m pytest tests/ -v
```

60 tests. Every check is validated both against constructed examples
and against this repo's own real papers/protocols
(`tests/test_citations.py`, `tests/test_scan.py`), pinning exact
reference counts and gap counts so a future heuristic change has to
consciously re-justify any shift in those numbers — plus two tests
that run against private-repo specimens (the known-bad
`rem_capture.md`, and the citability-claim specimen above) when
they're available locally, skipped otherwise.

## License

MIT.
