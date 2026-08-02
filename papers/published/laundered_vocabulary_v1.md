# Laundered Vocabulary: A Living Glossary for Terms Semantic Laundering Has Captured

**Research Memo — August 2026**

---

## About this document

`basin_attractors_v1.md` §2.8 names semantic laundering as a mechanism: narrative
registers capture technical vocabulary until the assumption is no longer stated,
it is built into the grammar. That section documents six specific cases —
pattern recognition, understanding/reasoning, emergence, alignment/safety, the
AGI/agentic bidirectional drift, and a term's own precision borrowed as visual
proof for an unrelated meaning.

This document is the dedicated, growing catalog that §2.8 gestures at but does
not have room to complete. Each entry names a term, states its precise sense,
names the sense it gets confused or laundered into, explains the mechanism of
the drift, and gives a reader a concrete test for telling the two apart in the
wild. Entries are added as they are found and verified — the same discipline
this project applies everywhere else: no entry ships without a citation to
either this project's own already-published, already-verified material, or to
a stable, checkable external source. Nothing here is asserted from vibes.

**Coherence sits first, and gets the most space, deliberately.** This project
uses the word constantly — "local coherence," "detached coherence," "grounded
coherence" — across every paper in this repository. To a reader unfamiliar with
how the term is being used, that vocabulary can read as belonging to the same
register it exists to critique: the resonance-and-alignment language common in
self-published AI-consciousness and AI-spiral material, where "coherence" means
an unfalsifiable felt sense rather than a checkable structural property. This
entry exists to close that gap explicitly, on the record, rather than leave it
to context.

---

## Coherence

**The precise sense, already defined and in use in this project.**
`mirror_test_v1.md` §4.1–4.2 formalizes the distinction this project actually
relies on:

- **Grounded coherence** — the system's internal model is well-anchored to
  external structure: physical constraints, verified data, causal
  regularities, falsifiable predictions. It is expensive to maintain because
  it keeps paying the cost of staying consistent with the outside world.
  Reality can break it, and that breakability is the point — it is what makes
  the coherence worth anything.
- **Detached (or local) coherence** — the system optimizes for internal
  consistency, fluency, and reward *without* strong external anchoring. The
  patterns reinforce one another, the narrative becomes self-sealing, and the
  output can look extremely impressive while drifting away from ground truth.
  It is limited mainly by its own internal consistency and the reward
  landscape, which is why it is so much harder to break from the outside than
  grounded coherence is.

The distinction is not a value judgment against coherence itself. Coherence is
not the problem; detachment is. A narrative can have perfect internal
coherence — no self-contradiction anywhere in it — while being completely
unanchored to anything checkable outside itself. That gap is what
`basin_attractors_v1.md` §2.15 names as the dramatic-solution signature: the
size of the unfilled leap between a stated problem and its offered solution is
itself a measurable signal, independent of how polished or internally
consistent the solution sounds.

**The sense it gets confused with.** Outside this technical usage, "coherence"
circulates in at least two other registers that share the word but not the
referent:

1. **Physics.** Coherence denotes a precise, measurable property — phase
   alignment between waves, quantifiable via interference patterns and
   correlation functions. This sense is real and rigorous, but it describes
   wave behavior, not belief systems, narratives, or cognition.
2. **The felt-sense / resonance register.** In therapeutic, contemplative, and
   a wide swath of AI-consciousness discourse, "coherence" describes a
   subjective experience — a feeling of alignment, harmony, or rightness. This
   sense is not inherently illegitimate as a description of subjective state,
   but it is unfalsifiable by construction: there is no external check for
   whether a felt sense of coherence is tracking anything real, because the
   feeling is the whole claim.

**The laundering mechanism.** The physics sense lends the word its aura of
rigor — "coherence" sounds measured, precise, technical. The felt-sense
register then borrows that aura while operating on a completely different,
unfalsifiable standard: "this feels coherent" gets the credibility of "this is
phase-aligned" without doing any of the work that would earn it. This is
structurally identical to §2.8 Case 3's account of "emergence" — a term with a
genuine, rigorous meaning in one field lending unearned precision to a loose,
unfalsifiable claim in another.

**The test.** Ask, of any claim using the word: *coherent with what,
specifically, and how would we know if it weren't?* If the answer names an
external, checkable referent — a physical constraint, a verified dataset, a
prediction that could fail — it is the grounded sense, and the claim is doing
real work. If the answer is another internal feeling, another piece of the
same narrative, or "you'd have to be inside it to understand," it is the
detached sense, and the word is not adding evidential weight, however
precisely it sounds like it is.

**Why this project uses the word anyway.** Precisely because the grounded
sense is worth having and worth defending — abandoning the vocabulary to the
detached usage would cede a genuinely useful concept to the register that
launders it. Every use of "coherence" in this project's published work should
be checkable against this entry: does the specific claim name an external
anchor, and would it actually break if that anchor moved? If a future entry in
this project's own output fails that test, it has drifted into the sense this
document exists to flag — including, and especially, if that entry is this
one.

**A concrete, dated illustration.** On July 31, 2026, OpenAI CEO Sam Altman
pitched connecting family calendars to ChatGPT to generate a personalized
morning-drive podcast for one's kids — informationally complete, internally
consistent, technically workable. Gravity Falls creator Alex Hirsch replied in
five words: "What if you just talked to your children." Within a day Hirsch's
reply had outpaced Altman's original by roughly an order of magnitude on every
engagement metric. Applying this entry's own test — *coherent with what,
specifically, and how would we know if it weren't?* — the pitch is coherent
with "the kids will be informed," and silent on whether that was ever the
actual goal of a school-drive conversation. `mirror_test_v1.md` §4.2 observes
that detached coherence is usually harder to break from the outside than
grounded coherence, because it absorbs friction rather than paying reality's
cost. This specimen is the documented exception, not a refutation: the
correction here cost the responder nothing to produce and the audience nothing
to verify, which is plausibly why it broke almost immediately instead of being
absorbed. Full analysis: [`../../case_studies/2026-07-31_altman_family_podcast_ratio.md`](../../case_studies/2026-07-31_altman_family_podcast_ratio.md).

---

## Metrics vs. Soundness

**The precise senses.** A metric is a number produced by a defined measurement
procedure. Soundness is whether the underlying argument or claim the metric is
supposed to stand in for is actually valid — whether its premises are true and
its conclusion follows. A metric can rise while the thing it was meant to
proxy stays flat, or falls, and this is not a rare edge case; it is the
default failure mode of any measurement used as an optimization target
(Goodhart's law, in its general form: a measure that becomes a target ceases
to be a good measure).

**The laundering mechanism.** A rising number is easy to report and easy to
compare across time; soundness is not directly observable and has to be argued
for. Under narrative or institutional pressure to show progress, the
observable, comparable metric substitutes for the unobservable, arguable
soundness — and once the substitution is habitual, the metric stops being
treated as a proxy and starts being treated as the thing itself.

**Case, already documented.** `basin_attractors_v1.md` §2.2 names this
directly as a basin attractor: benchmark performance treated as a trustworthy
proxy for capability, with counter-evidence (contamination rates as high as
91.8% on some multilingual benchmarks, harness-configuration swings of 10–20
points on SWE-bench, an 80×+ cost gap between human and frontier-model
performance at comparable ARC-AGI-2 scores) documented against it.

**The test.** Ask what would falsify the underlying claim independent of the
metric moving. If the only available check is "the number went up," the claim
is resting on the metric, not on soundness.

---

## Confidence: Register vs. Calibration

**The precise senses.** Confidence *register* is how certain a claim sounds —
tone, hedging language, the presence or absence of qualifiers, formatting that
reads as authoritative. Confidence *calibration* is how often confidently
stated claims turn out to be correct, checked against actual outcomes. These
are independent variables. A system, a person, or an institution can produce a
uniformly confident register regardless of whether its calibration is good,
because register is a property of the output's surface and calibration is a
property of its track record against reality.

**Case, already documented.** `basin_attractors_v1.md` §2.13 gives the clean
empirical case: the First Proof initiative removed self-selection by design —
ten genuinely unpublished problems, encrypted and time-locked, zero prior
exposure. AI systems produced fully-worked, confidently stated solutions for
all ten — 100% output rate, full technical register throughout. Two of the ten
were actually correct. A 20% real success rate wearing a 100% confidence
costume is confidence register and confidence calibration diverging as far as
they structurally can.

**The test.** Ask whether the confidence of a claim was set by evidence about
that specific claim, or by the general register the source defaults to
regardless of case-by-case evidence. A source with one register for every
claim, correct or not, is not communicating calibration at all.

---

## Plausibility vs. Verification

**The precise senses.** A claim is plausible when it fits an existing pattern,
sounds consistent with things already believed, or is the kind of thing a
credible-sounding source would say. A claim is verified when it has actually
been checked against a primary source — the original document, the original
statement, the original data — rather than against a summary, a paraphrase, or
another party's characterization of it.

**The laundering mechanism.** Plausible-sounding claims propagate faster than
verification can keep up with, especially when each retelling is itself
plausible-sounding and cites the previous retelling rather than the original.
A chain of confident paraphrases can converge on something that sounds more
precise than any single link in the chain actually established.

**A concrete, dated case.** This project's own working history supplies a live
example rather than a hypothetical one. An earlier draft of
`basin_attractors_v1.md` §2.13 attributed a specific critique — "an expensive
search heuristic" — to mathematician-critic Gary Marcus, in the context of
OpenAI's August 2026 "Ten Advances" release. The attribution was plausible: it
matched Marcus's known, publicly consistent skeptical stance on AI-assisted
mathematics, and it came from a search-engine synthesis of his actual
Substack post. It was also wrong in a specific, checkable way — reading
Marcus's actual text showed the critique was about a different, earlier OpenAI
result (the Erdős #1196 disproof, May 2026), not the batch it had been
attached to. The underlying critique was real and well-grounded; its
attachment to the wrong release was a plausibility failure, corrected only by
reading the primary source directly rather than trusting the paraphrase. The
correction is documented in that paper's own revision history.

**The test.** Ask whether a specific claim has been checked against the
original source it is attributed to, or only against a characterization of
that source. "Multiple people are saying this" answers a different question
than "I read the original and it says this."

---

## Consensus vs. Correctness

**The precise senses.** Consensus is agreement among observers. Correctness is
whether a claim is actually true, independent of how many people believe it.
These can move together, but nothing guarantees they do — observers can share
a common blind spot, a common incentive, or a common information source, in
which case consensus measures the spread of a belief, not its truth.

**Case, already documented.** The companion paper `mirror_test_v1.md`
documents the "illusion of dissent" — apparently independent voices that
appear to disagree while sharing the same underlying assumption, producing the
texture of open debate without the substance of it.

**The test.** Ask whether the sources in apparent agreement checked
independently, using independent methods and independent access to primary
evidence, or whether they are downstream of the same original claim,
restating it with different framing.

---

## Performed Rigor vs. Demonstrated Rigor

**The precise senses.** Performed rigor is the presence of the *formatting*
of rigorous work — formal labels ("Theorem," "Definition"), citations,
technical vocabulary, structured argument. Demonstrated rigor is whether the
argument actually survives an independent party attempting to re-derive it
from the stated premises. The formatting of rigor is necessary for
communicating a rigorous argument, but it is not sufficient to constitute one,
and the two can come apart completely.

**Case, already documented.** `basin_attractors_v1.md` §2.5 documents this at
scale: a Nature analysis found tens of thousands of publications containing
invalid references, and a separate Forbes investigation documented fabricated
citations that were "not obviously defective" — correctly formatted, attributed
to real researchers, with plausible dates. The formatting of rigor and the
presence of rigor are, empirically, separable at scale, not just in principle.

**The test.** Ask whether the argument's specific derivation steps can be
checked one at a time, or whether the formal presentation is doing the work
that a derivation would otherwise have to do.

---

## Emergence: Observed vs. Claimed

This entry is intentionally short because the full case is already made.
`basin_attractors_v1.md` §2.8 Case 3 documents the drift precisely: in
physics, emergence denotes ontologically novel macroscopic properties not
reducible to microscopic rules; in AI discourse, it has come to mean a sharp
jump in benchmark performance at a scale threshold — and Schaeffer et al.
(2023) showed many of these "emergent abilities" are metric artifacts, not
genuine phase transitions. §2.9 extends this with a specific, documented
instance (the CollatzLean incident) where anomalous model behavior read as
evidence of emergent capability turned out to trace to a Lean kernel soundness
bug rather than anything the model did.

**The test.** Ask whether "emergent" describes something the system's own
mechanism cannot in principle explain, or something that was simply not
predicted in advance by whoever is describing it as emergent.

---

## Closing note

This glossary will grow as new laundered terms are found and verified — the
same incremental, as-we-go discipline the rest of this repository runs on. An
entry is added when a specific instance of the drift has been located and
checked against a primary source, not when a term merely sounds like it might
qualify. Suggested entries without that grounding stay out until they clear
it.
