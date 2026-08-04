# The Conjecture Tracker: Method, Verification, and Register Across AI-Assisted Mathematical Claims

**Research Memo — Compiled August 2026**

---

## Purpose

[`basin_attractors_v1.md`](basin_attractors_v1.md) §2.13 (The Math-Breakthrough Ratio) and §2.15 (The Dramatic-Solution Signature) each make a narrative-level argument about AI-assisted mathematics: that confident output outruns correct output when self-selection isn't controlled for, and that announcement registers routinely overstate the size of the leap relative to the incremental work actually shown. Both arguments are made in prose, once, against a small number of specimens. This tracker exists to hold the same specimens — and future ones — in a structured, comparable form, so the claims in §2.13 and §2.15 stay checkable as new AI-assisted conjecture results arrive, instead of resting on a fixed set of paragraphs written in one window.

It also exists to separate two questions this paper's narrative sections have not yet distinguished cleanly: **what kind of mathematical task was actually solved** (a search problem — find the counterexample — versus a proof that a regularity holds in general, per the distinction applied in the August 2026 revision of §2.13), and **what mode of production generated the result** (a single targeted result aimed at one named problem, versus a mass-scale batch sweep across hundreds of candidate problems). Neither axis is visible in a headline that says "AI solves N open problems."

**External validation of the underlying problem, verified 2026-08-04 and worth naming directly.** This tracker's whole premise — that confident AI-mathematics claims need a structured verification-tier distinction rather than being taken at announcement value — is independently corroborated by a well-resourced, non-narrative-driven actor working the same problem from a different angle. DARPA's **Exponentiating Mathematics (expMath)** program (darpa.mil, launched March 2025; Program Manager Patrick Shafto, Rutgers) is explicitly structured into two technical areas, one of which is **"developing robust evaluation metrics for assessing AI performance at the frontier of mathematical research."** This is not a specimen of the narrative pattern this project otherwise tracks — it is a funded federal research program built specifically to solve the same evaluation gap this table's six axes exist to make visible row by row. Cited here as evidence the underlying problem is real and recognized outside this project, not as a source for any claim in the table itself; expMath's own output, if and when specific results are announced, would be checked against this table's standard the same as any other specimen, not exempted for institutional pedigree.

## How to read this table

Six axes, applied to every row:

1. **Method type** — *search* (counterexample construction against a discrete or checkable space) vs. *regularity* (a proof that a bound or property holds in general) vs. *mixed/unspecified* where the public record doesn't itemize per-problem method. This is Sabine Hossenfelder's distinction, applied first in the August 2026 revision of §2.13 to the OpenAI Astra results — search problems are brute-forceable by a fast enough computer, with or without an LLM; general proofs are not.
2. **Verification tier** — *Lean-certified* (machine-checked proof assistant output, the strongest public bar) > *human-verified, natural language* (checked by named mathematicians post hoc, not machine-checked) > *self-reported / time-boxed, no independent check disclosed*.
3. **Human involvement** — *heavy curation* (humans shape raw model output into a usable proof/manuscript) vs. *verification only* (humans check a claim already in finished form) vs. *not established* (the public record doesn't specify).
4. **Announcement register** — *modest/incremental* vs. *dramatic/leap-framed*, per §2.15's diagnostic: how the result was actually presented publicly, independent of whether the underlying work was itself incremental or discontinuous.
5. **Production mode** — *individual* (one targeted attempt at one named problem) vs. *batch* (many candidate problems attempted in the same run, with a reported hit rate).
6. **Outcome** — hit rate where a denominator exists; single pass/fail where it doesn't.

## The table

| Specimen | Solver | Method type | Verification tier | Human involvement | Announcement register | Production mode | Outcome |
|---|---|---|---|---|---|---|---|
| First Proof Project (10 unpublished, encrypted, time-locked research problems) | Multiple frontier AI systems, tested blind | Mixed/unspecified per-problem | Human-verified against pre-locked ground truth (not Lean) | Not applicable — blind test, no curation of model output before scoring | Not applicable — a controlled measurement, not a claim announcement | Batch, 10 problems, zero prior exposure by design | 10/10 confident, fully-worked output; **2/10 correct (20%)** |
| AlphaProof Nexus | Google DeepMind | Mixed/unspecified per-problem | Lean-certified | Not established by public sources reviewed | Framed as a large-scale sweep result | Batch — 353 Erdős problems + 492 OEIS conjectures attempted | **9/353 Erdős (2.5%)**; **44/492 OEIS (8.9%)** |
| Erdős unit distance conjecture #1196 | An OpenAI model (unspecified) | Search (counterexample, combinatorial geometry) | Human-verified, natural language (verifiers include Fields Medalist Tim Gowers) | Verification only, per public reporting | Dramatic — reported as an 80-year-old problem solved | Individual, single named problem | 1/1, verified correct |
| Maxwell conjecture disproof | 3 named mathematicians (Arathoon, Ball, Kvalheim); GPT-5.6 Sol supplied the initial construction idea | Search (5-point-charge counterexample, 24 critical points) | Human-verified, natural language, fully worked (Taylor expansions, Hessian classification, transversality argument); posted to arXiv | Maximal — AI supplied only the starting construction idea; all proof work is human | Modest/incremental — no AI-capability framing in the paper itself | Individual, single named 150-year-old conjecture | 1/1, verified correct — this paper's negative control (§2.13, §2.15) |
| OpenAI "Ten advances" (Astra) | OpenAI, internal Astra model | **Split: 4 search / 6 regularity** (non-sofic group construction, Connes Rigidity disproof, 2 Erdős/Simonovits extremal-graph disproofs = search; sphere-packing bound, circuit-complexity bounds, quantum parallel repetition, closest-vector-problem hardness, Ehrhart's bound, Ramsey lower bound = regularity) | Lean-certified, all 10 (github.com/openai/ten-proofs) | Heavy curation, per OpenAI's own account — humans prepared manuscripts and extracted arguments from long reasoning transcripts | Dramatic — "solved 10 major open problems," "a major step for scientific reasoning" | Batch, 10 results in one release, ~$2,000 Sol-tier inference cost per problem-set disclosed | 10/10 Lean-verified |
| Graffiti Conjecture 284 (graph theory, ~30 years open, from Fajtlowicz's 1980s Graffiti conjecture-generating system) | xAI, Grok 4.5 Medium (agent "Capy") | Search (counterexample construction) | **Self-reported / time-boxed, no independent check disclosed** — checked only by other xAI-internal models ("adversarial Sol and Fable review tasks"), which cross-referenced 349 indexed citations of the survey stating the conjecture; no independent human mathematician confirmation, no Lean certification, no peer-reviewed publication found associated with the announcement | Minimal/not established — informally prompted in Slack; the verification step was AI-only (other xAI models), not human mathematical curation | Dramatic — "Grok 4.5 just solved a graph theory conjecture that has been open for ~30 years" (Musk); "cracks," "debunking" in press coverage | Individual, single named problem, reported 8-minute solve time | 1/1 self-reported correct; **independently unverified at time of announcement** |

## What this tracker does NOT yet establish

- **No value-density ratio between batch and individual production modes is computed here.** Six specimens is not a powered sample, and the individual-mode rows carry a severe, visible selection bias: a single targeted result reaches public attention *because* it succeeded, while the batch-mode rows (First Proof, AlphaProof Nexus, Astra) report their failures alongside their successes because the denominator is disclosed. First Proof is the only specimen in this table designed specifically to remove that selection (blind, time-locked, pre-committed scoring) — which is exactly why its 20% figure, not the individual 1/1 rows, is the closest thing here to an unbiased read of raw AI mathematical output.
- **The Graffiti Conjecture 284 row is the table's only specimen where the verification step itself was performed by the same lab's own AI systems, not by an independent human, Lean, or peer-reviewed check.** This is a meaningfully weaker verification tier than every other row and is marked as such rather than folded into "human-verified" — self-checking by other models from the same company is not independent verification, and this table treats it as a distinct, named category for exactly that reason.
- **No claim is made about the actual mathematical significance of any result to the field.** Verification tier tells you whether a proof is correct; it does not tell you whether the theorem matters. That judgment requires domain-expert assessment this paper's method — public-source verification — cannot supply, and is not attempted here.
- **"Human involvement" entries reflect what is publicly disclosed, not a measurement of actual labor.** Several rows are marked "not established" rather than "none" — absence of disclosure is not evidence of absence of human curation.
- **This table does not imply search-type results are less valuable than regularity-type results.** The method-type axis exists to make the distinction checkable, per Hossenfelder's own framing (basin_attractors_v1.md §2.13) — it is a calibration of what kind of claim is being made, not a ranking.

## Update discipline

Living document. New rows are added as new AI-assisted conjecture/proof claims clear the same public-source verification standard used throughout [`basin_attractors_v1.md`](basin_attractors_v1.md). Entries are dated at addition. Corrections to existing rows are made as a dated addendum below the table's original commit, not a silent edit — the same discipline `basin_attractors_v1.md`'s revision log already follows.

## Cross-references

- [`basin_attractors_v1.md`](basin_attractors_v1.md) §2.13, The Math-Breakthrough Ratio — the narrative argument this table operationalizes.
- [`basin_attractors_v1.md`](basin_attractors_v1.md) §2.15, The Dramatic-Solution Signature — the announcement-register axis (column 4) is drawn directly from this diagnostic.
- DARPA's Exponentiating Mathematics (expMath) program — external validation that the verification-tier problem this table addresses is recognized and being independently resourced outside this project; see Purpose section above and References below. Not a source for any table entry; noted for the problem's legitimacy, not as evidentiary backing for any specimen.

## References

First Proof Project (2026). 1stproof.org. Ten unpublished research problems, encrypted and time-locked, one week AI attempt window, February 2026.

UNU Campus Computing Centre (2026). Coverage of the First Proof Project results.

DeepMind (2026). AlphaProof Nexus. arXiv preprint and GitHub repository, May 2026.

Scientific American; Forbes (2026). Coverage of an OpenAI model's resolution of Erdős problem #1196 (unit distance conjecture), verified by mathematicians including Tim Gowers. May 2026.

Arathoon, P., Ball, G. & Kvalheim, M.D. (2026). The Maxwell Conjecture is False. arXiv, posted July 29, 2026.

OpenAI (2026). Ten advances in mathematics and theoretical computer science. openai.com/index/ten-advances-in-mathematics/, 2026.

OpenAI (2026). ten-proofs [GitHub repository]. github.com/openai/ten-proofs, 2026.

Brown, N. (@polynoamial); Bubeck, S. (@SebastienBubeck) (2026). Posts on X announcing the Astra "ten advances" results. 2026.

Marcus, G. (2026). Checking the math behind OpenAI and Anthropic's latest headlines. garymarcus.substack.com, 2026.

Hossenfelder, S. (@skdh) (2026). Post on X distinguishing brute-force counterexample-finding from proving general regularities. August 1, 2026.

Musk, E. (@elonmusk) (2026). "Grok 4.5 just solved a graph theory conjecture that has been open for ~30 years." X, 2026.

Sun, J. (@justinsunyt) (2026). Thread describing the Grok 4.5 Medium agent "Capy" producing a counterexample to Graffiti Conjecture 284 in eight minutes, prompted in Slack, checked by internal "Sol" and "Fable" adversarial review tasks against 349 indexed citations. X, 2026.

BigGo Finance (2026). Musk Praises Grok 4.5 for Debunking 30-Year Graph Theory Conjecture in 8 Minutes; GPT-5 Solved It Too. finance.biggo.com, 2026.

DARPA (2025). expMath — Exponentiating Mathematics. darpa.mil/research/programs/expmath-exponential-mathematics, program launched March 2025.

DARPA (2025). Math + AI = Tomorrow's breakthroughs. darpa.mil/news/2025/math-ai-tomorrows-breakthroughs, 2025.

Shafto, P. (@patrickshafto) (2025). Posts on X announcing and describing the DARPA expMath program launch. 2025.

---

## Revision log

*Created August 2026, cross-linked from `basin_attractors_v1.md` §2.13. Seeded with five specimens already verified in that paper's research window: First Proof Project, AlphaProof Nexus, Erdős #1196, the Maxwell conjecture disproof, and OpenAI's Astra "Ten advances" (with the search/regularity split from the same paper's August 2026 §2.13 revision). No new research performed for this initial version — this is a restructuring of already-verified specimens into comparable form, not a new claim.*

*Added 2026-08-04: Graffiti Conjecture 284 (xAI, Grok 4.5), surfaced while checking a separate operator-supplied claim (see companion case study [`2026-08-04_musk_source_code_binary_escalation.md`](../../case_studies/2026-08-04_musk_source_code_binary_escalation.md), third specimen). Introduces a verification-tier value not yet present in this table — self-checked by the same lab's other AI systems, with no independent human, Lean, or peer-reviewed confirmation found at the time of the promotional announcement — noted explicitly in "What this tracker does NOT yet establish" above rather than folded into the existing "human-verified" tier.*

*Cross-referenced 2026-08-04: DARPA's Exponentiating Mathematics (expMath) program, added to Purpose, Cross-references, and References as external validation that the evaluation-tier problem this table addresses is independently recognized and funded outside this project — verified directly against darpa.mil rather than taken from the LinkedIn post that surfaced it. Not used as a source for any table entry; if and when expMath produces specific, checkable results, they would be evaluated against this table's standard like any other specimen.*

---

*Compiled from research sessions July–August 2026. All claims are falsifiable. All sources are publicly verifiable. This tracker inherits the evidentiary discipline of `basin_attractors_v1.md`: no exemption by source, corrections are dated rather than silent, and absence of a figure means it was not found, not that it is zero.*
