# External Grounding for §2.2's Benchmark Attractor: The "Whose Facts Count?" Findings

*Status: DRAFT ADDENDUM. Filed 2026-09-22. Authors: operator + Claude (Sonnet 5).
Proposes external grounding for `basin_attractors_v1.md` §2.2 (Attractor 2:
Benchmark Performance Is a Trustworthy Proxy for Capability) — not yet merged
there, per this project's own convention that published papers take a new
version suffix rather than a silent edit. Not yet run through `paper_rigor`,
`verification_lint`, or `attractor_scan` at time of writing.*

---

## The gap this addresses

`basin_attractors_v1.md` §2.2 states the load-bearing claim under attack:

> High scores on formal benchmarks reliably indicate the underlying capability
> claimed.

Its existing counter-evidence is entirely a **contamination** argument — per
the position paper already cited there, up to 45% (91.8% on one multilingual
audit) of benchmark items leaking into training data, plus the "harness
multiplier effect" (10–20pp swing from agent scaffold alone at fixed
weights). That is a real and sufficient defeat of the
load-bearing claim on its own terms, but it leaves a distinct failure mode
completely ungrounded: a benchmark can be **100% uncontaminated** and still
fail to measure "the underlying capability claimed" for most of the world,
because the benchmark's own construction encodes a narrow cultural and
epistemological referent as if it were culturally neutral ground truth. The
specimen below supplies that second, independent grounding — not a
replacement for the contamination argument, a complement to it.

## The specimen, read directly from a primary source

**Sourcing note.** Read in full (all 37 pages, across four sequential reads
covering pages 1–37) from a supplied PDF — this project's strongest sourcing
tier, the same standard `jagged_judges_meta_protocol_grounding_v1.md` applies
to its own primary citation.

**Citation.** Zahra, F. T., Sk., M. S. I., & Chung, R. (2026). *Whose Facts
Count? A Culturally Responsive Audit of LLM Evaluation Benchmarks.*
arXiv:2609.24934v1. **This is an arXiv preprint, not yet peer-reviewed at the
time of this citation** — stated directly, not elided, matching this
project's own standing practice for preprint sourcing.

**Method.** Per Zahra et al. (2026), the paper applies a six-dimension
Culturally Responsive Evaluation (CRE) rubric — grounded in Hood (2001),
Kirkhart (1995, 2010), and Hopson (2009) — to two benchmark artifacts already
treated in AI evaluation practice as general-purpose, culturally neutral
instruments: a full-dataset audit of SimpleQA (N=4,326 items, per the paper's
own reported sample) and a sample audit of the LMSYS-Chat-1M Arena logs
(N=600). The six dimensions: **D1** Western/Global North referent
framing, **D2** evidentiary accessibility (can the ground truth actually be
verified by someone outside the source culture/language), **D3** single
indisputable-truth framing, **D4** individualist framing, **D5** Global South
presence/absence (including colonial framing where present), **D6**
oral/community-knowledge exclusion. Inter-rater reliability was checked via a
second independent coding pass; a Rasch Partial Credit Model was used to
validate the rubric's own measurement properties before drawing substantive
conclusions from it. A 50-item counter-benchmark, hand-constructed to score
well on the same six dimensions, was scored against the same rubric as a
contrast condition.

**Core finding 1 — one dimension is not just skewed, it is unanimous.** D2
(evidentiary accessibility) scored **1.00 with SD = 0.00** across the entire
audited SimpleQA sample — every single item requires English-language,
Western-archival verification with no exception found. A perfectly uniform
score across thousands of items is not sampling noise; it is a structural
property of how the benchmark's ground-truth-verification process was built.

**Core finding 2 — the coverage-inflation artifact.** Per the paper's own
provenance analysis, 128 of the dataset's questions concern Colombia
specifically, and 117 of those are municipal founding-date questions — a
single question template repeated against a gazetteer, traced to one
contributor. Those 117 items alone are 2.70% (per Zahra et al., 2026) of the
entire 4,326-item dataset (the paper's own reported total). Excluding
Colombia's contribution, total Global South coverage across the rest of the
dataset drops to **5.41%** (per Zahra et al., 2026) — meaning a large
share of
what would otherwise read as "Global South representation" in an aggregate
coverage statistic is a single contributor's repeated template on one
country's municipal records, not distributed geographic coverage. This is
directly the same *shape* of artifact this project's own tools are built to
catch: a single unaudited contribution inflating an aggregate metric in a way
that looks like breadth until traced to its source (structurally adjacent to
the "harness multiplier effect" already in §2.2 — an unexamined pipeline
component quietly determining the headline number).

**Core finding 3 — language overrepresentation in the preference-signal
half of the audit.** Per Zahra et al. (2026), in the LMSYS-Chat-1M Arena
sample English constitutes **76.3%** of logged interactions, against an
ITU-estimated (per Zahra et al., 2026) global English-speaker share of
**25.9%** — a **+50.4
percentage-point** gap between who is
generating the preference signal used to rank models and who the ranking is
implicitly claimed to generalize to. Arena-style leaderboards are downstream
consumers of exactly the "benchmark performance" §2.2's load-bearing claim is
about; a ranking built overwhelmingly from one linguistic population's
preferences is not measuring "the underlying capability" in a
population-neutral sense, independent of whether any individual item is
contaminated.

**Core finding 4 — the deficit is real and measurable, not just
qualitative.** Mean CR-deficit score on SimpleQA was **1.78 (SD=1.13)**,
against **0.64 (SD=0.94)** on the hand-built counter-benchmark — a large gap
(Cohen's d = 1.01) between a benchmark widely treated as general-purpose and
one deliberately constructed to score well on the same six dimensions. This
demonstrates the deficit is not an unavoidable property of benchmark
construction in general; it is a specific, correctable property of the
benchmarks currently in wide use.

**Core finding 5 — the dimensions compound, not sum independently.** Per the
paper's own reported statistics, D3 (single-indisputable-truth framing) and
D6 (oral/community-knowledge exclusion) co-occur far more than chance (per
Zahra et al., 2026): φ = .68, χ²(1, N=4,326) = 742.3, p < .001. A benchmark item that frames its answer as the one indisputable
truth is, specifically and predictably, also an item that has excluded
oral/community knowledge as a legitimate source of that truth — the two
failure modes are not independent axes of the same general "bias" but a
single underlying epistemological stance (only archivally-documented,
single-answer, Western-referent claims count as verifiable fact) expressing
itself on two measurement axes at once.

**Honest scope, preserved rather than smoothed over.** Two citations inside
the paper itself — attributed to "Claude Mythos Preview" (cited as an
Anthropic 2026 system card) and "GPT-5.6-Terra" (cited to OpenAI) — are used
for inter-method reliability coding and are **not verifiable against any
model release this project can confirm exists**. This is flagged here at the
same "unconfirmed, not asserted real or fake" tier this project holds every
AI-involvement claim to (see `dillon_c_capability_claims_watchlist/`'s
standing discipline in the private companion repo) — it does not
independently undermine the paper's core empirical audit (the D1–D6 scoring
of SimpleQA and the Arena sample, and the Rasch validation of the rubric
itself, do not depend on those two citations), but it is a real, unresolved
sourcing gap in the paper as read, named rather than elided. No public
identity claim is made about the paper's own three named authors beyond
their stated affiliation on the preprint itself.

## Why this grounds §2.2 precisely, and sharpens it

§2.2's existing counter-evidence (contamination, harness variance) attacks
the load-bearing claim on grounds of **measurement noise and pipeline
artifacts** — the benchmark's number does not reliably reflect the
capability even on its own terms, because the test was compromised or the
scaffold inflated it. This specimen attacks the same claim on a different
axis entirely: **construct validity**, not measurement noise. Even a
benchmark run with zero contamination and an identical scaffold across every
model would still, per this specimen's D2 unanimity finding, be asking
"can this be verified against English-language Western archival sources" as
an unstated precondition of every single item — meaning a model's score
reflects fluency in and access to one specific evidentiary tradition, not
"the underlying capability claimed" in the population-general sense the
load-bearing claim asserts. Two independent failure modes, both defeating
the same claim, from unrelated mechanisms: this is the same evidentiary
pattern §2.2's own two existing counter-evidence paragraphs already show
(contamination studies and harness-variance studies are also two
independent mechanisms converging on the same defeat), extended by a third.

INV-AVERAGE-IS-NOT-ANCHOR (PIQOS-IsoAxiomV8-'s private companion project;
not part of this repository, named only for the parallel) states that
"average consensus at scale produces a better approximation of the
statistical center of the training distribution — not convergence toward a
fixed coherent anchor." This specimen's Arena-language finding (per Zahra
et al., 2026: 76.3% vs. 25.9%, +50.4pp) is a direct, independently-sourced
empirical instance of
that same structural point applied to *evaluation* rather than *training*:
an "average preference" signal built from one linguistic population is
being read as a population-general capability signal, the same conflation
(statistical center of the sampled distribution mistaken for a
population-neutral truth) at one level removed.

## What this does NOT establish

- Not a claim that SimpleQA or LMSYS-Chat-1M Arena are therefore useless or
  should be discarded — the paper's own counter-benchmark result shows the
  deficit is correctable, not that benchmarking itself is invalid.
- Not a claim about the two unconfirmed model citations inside the source
  paper ("Claude Mythos Preview," "GPT-5.6-Terra") beyond what is stated
  above — neither asserted to be real model releases nor asserted to be
  fabricated; flagged as unconfirmed and left there.
- Not a claim that this specimen's six-dimension CRE rubric is itself free
  of construction bias — the paper validates the rubric's own measurement
  properties via a Rasch model, which is stronger grounding than an
  unvalidated rubric would carry, but "validated as internally consistent"
  is not the same claim as "captures every relevant cultural dimension."
- Not a claim that this specimen's findings generalize to benchmarks outside
  the two audited (SimpleQA, LMSYS-Chat-1M Arena) — the audit is scoped to
  those two artifacts specifically, not benchmarks in general, though the
  D2 unanimity result (1.00, SD=0.00) is a strong single-instance signal
  worth testing elsewhere.
- Not a claim that the Colombia/municipal-founding-dates finding indicates
  bad faith on the part of the contributor named in the dataset's
  provenance trail — consistent with this project's standing discipline of
  never asserting intent about a named individual, this is logged as a
  structural artifact (one contributor's template inflating an aggregate
  coverage statistic), not a claim about that contributor's motives.
- Not a claim that §2.2's existing contamination/harness-variance
  counter-evidence is weakened by this addition — the two mechanisms are
  independent and additive, not competing explanations for the same defeat.

## Where this would go if formalized

If merged, this reads as a citation/footnote on §2.2 itself in a future
version of `basin_attractors_v1.md`, not a new numbered attractor — it adds
a second, independent counter-evidence mechanism (construct validity /
cultural-epistemological narrowness) to the existing contamination/harness-
variance counter-evidence, rather than proposing a new failure mode.

## References

- Zahra, F. T., Sk., M. S. I., & Chung, R. (2026). Whose Facts Count? A
  Culturally Responsive Audit of LLM Evaluation Benchmarks. arXiv:2609.24934v1.
- Hood, S. (2001). Nobody knows my name: In praise of African American
  evaluators who were responsive. *New Directions for Evaluation*, 2001(92).
- Kirkhart, K. E. (1995). Seeking multicultural validity: A postcard from the
  road. *Evaluation Practice*, 16(1). / Kirkhart, K. E. (2010). Eyes on the
  prize: Multicultural validity and evaluation theory. *American Journal of
  Evaluation*, 31(3), as cited in the source paper.
- Hopson, R. K. (2009). Reclaiming knowledge at the margins: Culturally
  responsive evaluation in the current evaluation moment, as cited in the
  source paper.
