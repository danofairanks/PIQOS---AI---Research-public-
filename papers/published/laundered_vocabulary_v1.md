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

**Addendum (2026-08-16): the distinction is not this project's invention.**
A fair question about §4.1–4.2's grounded/detached split is whether it is a
private vocabulary dressed up to sound rigorous, or whether it names
something that recurs independently once other fields go looking for the
same gap. It is the latter — the same split, or a structurally identical
one, appears across at least three independent literatures that predate and
do not cite each other:

- **Epistemology.** Coherentist theories of truth (a belief is "true" if it
  is internally consistent with the rest of a belief system) versus
  correspondence theories of truth (a belief is true if it matches external
  reality) is a long-standing dispute, not a recent one — the coherentist
  side runs through the British Idealists (F.H. Bradley, and later Brand
  Blanshard), with correspondence theorists objecting on essentially this
  entry's grounds: internal consistency alone cannot certify truth, because
  an entirely self-consistent belief system can still fail to touch reality
  anywhere.
- **Natural language generation research.** The NLG literature separates
  **fluency** (is the text well-formed, grammatical, natural-sounding) from
  **faithfulness** or **factual consistency** (does the text's content
  actually hold given its source or the world) as close-to-orthogonal
  properties, precisely because early automatic metrics optimized for the
  first and were repeatedly found blind to the second. Ji, Lee, Frieske et
  al., "Survey of Hallucination in Natural Language Generation" (*ACM
  Computing Surveys* 55(12), Art. 248, March 2023) is the standard reference
  for the resulting taxonomy of hallucination as fluent-but-ungrounded
  output — a distinct failure mode from a model simply producing broken
  text.
- **Philosophy applied directly to LLMs.** Hicks, Humphries & Slater,
  "ChatGPT is Bullshit" (*Ethics and Information Technology* 26, Art. 38,
  2024) argue directly that LLM hallucination is better modeled as Frankfurt
  bullshit (*On Bullshit*, 1986) — output produced with indifference to
  truth value — than as lying (which requires tracking truth in order to
  invert it) or as noise. Their point is adjacent to this entry's: fluent,
  well-formed, indifferent-to-truth output is a distinct category from
  garbled output, and needs its own name.

One further, narrower, adjacent-but-not-identical term is worth naming
precisely so it is not conflated with the above: Barzilay & Lapata,
"Modeling Local Coherence: An Entity-Based Approach" (*Computational
Linguistics* 34(1), 2008) also uses the phrase "local coherence," but for a
different, narrower thing — how well entity references transition from
sentence to sentence within a discourse, measured via an entity-grid
representation, independent of whether the discourse is grounded in
anything external. It is a real, established, and useful term in
computational discourse linguistics; it is not the same claim as this
entry's grounded/detached distinction, and citing it as if it were would be
exactly the kind of borrowed-precision move §2.8 of `basin_attractors_v1.md`
already names as semantic laundering. The two senses share two words, not a
referent.

**A correction to a common assumption, with a citation.** It is often
assumed that a badly failing or degenerate model would show up as obviously
broken output — garbled, ungrammatical, incoherent in the plain sense. The
best-documented empirical case of a real generative-model degradation
mechanism says otherwise: Shumailov, Shumaylov, Zhao, Gal, Papernot & Anderson,
"AI models collapse when trained on recursively generated data" (*Nature*
631, 2024, 755–759; preprint: "The Curse of Recursion," arXiv:2305.17493,
2023) found that recursive training on model-generated data does not
degrade output into gibberish — it narrows the output distribution, losing
the tails and converging toward a homogenized, low-diversity result, while
remaining fluent and grammatical throughout every generation of the
experiment. The failure signature is narrowing, not babbling. One honest
caveat belongs alongside that citation: "model collapse" itself is
contested terminology in the field. Schaeffer, Kazdan, Arulandu & Koyejo,
"Position: Model Collapse Does Not Mean What You Think" (arXiv:2503.03150,
2025) catalog at least eight distinct, sometimes-conflicting definitions of
"model collapse" in active use and argue the term has drifted from a
specific empirical finding into a loosely-defined threat narrative. The
claim this addendum grounds is therefore the specific, narrow, replicated
empirical result — narrowing without babbling — not "model collapse" taken
as a single settled phenomenon.

None of these three literatures uses this project's vocabulary, and none
was written with this project in mind. That is the point of citing them
here: the grounded/detached split is not a private formalism requiring
this project's own framework to understand — it is a recurring finding
across epistemology, NLG research, and applied philosophy of language,
independently arrived at, because it is tracking something real rather
than something invented for this document's convenience.

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

## Singularity

**The precise sense.** In mathematics and physics, a singularity is a point at
which a model's own equations cease to yield a valid description — a function
is undefined (division by zero), non-differentiable, or a solution's terms
formally diverge (e.g., curvature/density in a general-relativistic solution
at a black hole's center). The standard reading, in every field that uses the
term technically, is that the singularity signals the *model's* incompleteness
at that point, not a literal physical event of infinite magnitude occurring in
the world. A singularity is where the map runs out, not a claim about the
territory.

**The sense it gets confused with.** Vernor Vinge's 1993 essay, "The Coming
Technological Singularity," borrowed the term explicitly and carefully: he
states that "singularities are always mathematical idealizations of natural
phenomena... not present in reality but foreshadow an important transition or
change of regime," and uses it to mean a point beyond which human models of
the future fail — an epistemic claim about prediction breaking down, not an
ontological claim about a literal mathematical blow-up in intelligence or
technology. Kurzweil's later, far more widely circulated version keeps the
exponential-acceleration framing and is on record explicitly denying literal
infinitude — the growth stays finite, just steep enough to look like a
rupture. What has drifted, across popular AI discourse, is the hedge both
originators kept: from "our predictive models fail beyond this point" to a
bare declarative treating an actual, in-progress, quasi-mathematically-
guaranteed intelligence explosion as already underway or imminent.

**The laundering mechanism.** The same shape this glossary already names for
Coherence and Emergence: a term with a genuine, rigorous meaning in one field
(a point where a model demonstrably breaks down) lends its aura of precision
and inevitability to a much looser claim in another (a coming AI intelligence
explosion), and the original hedge drops out through retelling until the
borrowed term is doing rhetorical work — implying mathematical inevitability
— that neither Vinge's nor Kurzweil's own stated definitions license.
`basin_attractors_v1.md` §2.7 documents this drift directly and by name: Sam
Altman's arc runs from the metaphorical "we are past the event horizon" (June
2025) to the flat present-tense declaration "We are now in the singularity"
(*Relentless* interview, July 2026), which that section notes is "the
opposite of Vinge's original definition (unpredictable discontinuity beyond
which human affairs become unmodelable)" — gradualism dressed in apocalyptic
vocabulary, not a returned hedge. §2.8 Case 6 documents the mechanism at its
most literal: an AI-generated image captioned "math Singularity," collaging
real formulas including the Riemann zeta function's genuine pole at s=1,
using the *actual* mathematical meaning of the word as unstated visual
"proof" for the unrelated, Vinge-derived hype meaning — pun standing in for
argument. `case_studies/2026-07-28_grok_x_instant_sycophancy.md` records a
rare instance of the distinction being drawn correctly in the wild, in a
public reply on X, before the same reply builds its own unfalsifiable
framework anyway — worth citing because it shows the conflation named here is
not a subtle scholarly point; it has already been made, in public, in plain
language, and made no difference to the discourse around it.

**The test.** Ask what specifically is being claimed: that a model's ability
to predict what comes next is expected to fail (Vinge's original, epistemic
sense — a modest and largely defensible claim about limits of foresight), or
that an actual, mathematically-inevitable event of unbounded consequence is
under way or fixed in the near future (the popular, ontological sense the
term has drifted into). A claim resting on the second sense should be
checkable independent of the word "singularity" — if removing the word and
restating the claim in plain terms ("intelligence will improve without limit
starting at a specific, nameable point") makes the claim sound like it needs
its own evidence rather than borrowed mathematical certainty, the word was
doing work the underlying argument was not.

---

## Law

**The precise sense.** In physics and the natural sciences, a "law" is a
generalization whose authority is, by design, independent of who stated it.
Newton's second law does not require continued deference to Newton to remain
true; it is re-derivable, falsifiable, and checkable by anyone with no access
to Newton's biography, reputation, or continued endorsement. Foucault's "What
Is an Author?" (lecture to the Société française de Philosophie, Feb. 22,
1969; published as "Qu'est-ce qu'un auteur?," *Bulletin de la Société
française de Philosophie* 63(3), 73–104; English translation by Josué V.
Harari in Rabinow, P. (Ed.), *The Foucault Reader*, 1984) names the specific
historical transition this entry depends on: he traces how, from roughly the
seventeenth century onward, scientific statements came to be received as
true or false "without any question of the meaning of the discourse being
connected with who its author was" — anonymous verifiability replaced
authorial guarantee as the thing that makes a scientific claim stand. A law,
in the technical sense, is precisely a claim built to survive the removal of
its author's name.

**The sense it gets confused with.** Foucault's essay spends most of its
length on the opposite case: discourses — literary and philosophical
foremost among them — where authorial identity never stopped being
load-bearing, because "the meaning and value attributed to the text would be
completely altered" if the identity of who wrote it were unknown. Within
that category he names a further, stronger position: **founders of
discursivity** (his own examples are Marx and Freud) — figures who do not
merely author a text but establish "the possibility and the rules of
formation of other texts," such that later work operates within the
discourse they founded whether or not it cites them directly. When a
self-published framework calls itself a "Law" while also styling its author
as "Founder of" the field the law belongs to, it is claiming the founder-of-
discursivity position — text and rule-for-producing-further-texts fused into
one authorial act — while borrowing the vocabulary ("Law") of the register
Foucault specifically documents as having *shed* that dependency.

**The laundering mechanism.** "Law" sounds like the physics sense — durable,
checkable, author-independent — while the actual claim depends entirely on
continued deference to the namer's self-conferred authority, because there
is no independent discourse outside her own texts against which the claim
could be checked or falsified. This is structurally the same borrowed-
precision move this glossary already names for Coherence, Emergence, and
Singularity — a term with a genuine, rigorous meaning in one register
lending its aura to an unfalsifiable claim in another — but the mechanism
supplying the borrowed authority here is different in kind: not a
mismeasured metric or a drifted definition, but the author-function itself,
performing legitimizing work a physics law is specifically built not to
need.

**A concrete, dated illustration (2026-08-17), specimen redacted.** A
self-published author's promotional material describes a self-conferred
field-founding title (framed as founder of a named psychological/
consciousness discipline) and a self-titled "Law of [X]," stated as a
private formula combining an author-specific subscripted constant and an
undefined cubed variable. No public material sighted defines any of the
formula's terms, states their units, or derives the relation from anything
— the notation asserts precision it never operationalizes. A companion
social-media post announcing a second "manuscript" states it "underwent
structured external review and independent multi-system stress-testing
coordinated by [a named individual], focused on internal consistency,
theoretical boundaries and evidentiary discipline" — naming a review process
with no stated institution, no disclosed methodology, and no stated
credentials for the coordinator, functioning the same way
`case_studies/2026-07-27_ssi_nvidia_partnership.md` names "The Opaque
Promise": an impressive-sounding validation asserted with zero verifiable
specifics, on a book distributed through a print-on-demand platform rather
than a publisher with an editorial process. Running this project's own
tools against the post text directly: `debasinizer` flags
`register_flagged: True` on two co-occurring resonance categories
(`resonance_wave_signal` on "signal," `consciousness_continuity` on
"consciousness" — its own documented bar of 2+ distinct categories, not one
common word); `paper_rigor` flags `credential_substitution` specifically on
the self-conferred founding title — a title doing argumentative work,
distinct from an externally-verifiable credential used only as an
identifying descriptor (contrast §5's treatment of "Nobel laureate John
Jumper" in `mission_premise_v1.md`, judged a false positive on exactly that
distinction); `verification_lint` flags a missing scoping
section above the applicable word-count threshold. This entry evaluates the
specific public text and claims described above, not the author's sincerity,
mental state, or private beliefs — consistent with this project's standing
practice (`case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md`:
"this is not evaluated as bad faith") — and treats a single specimen as a
single specimen, not an ongoing tracking subject.

**A note on redaction.** The specimen's real name, exact self-styled
titles, and exact formula notation are withheld here on a going-forward
policy: when this project's specimens are private individuals rather than
public institutions, public officials, or already-public-record corporate
events, identifying detail is redacted from the published record by
default. Redaction is not the same as unfalsifiability — the specimen is
real, dated, and its full identifying detail (the real name, the source
post, and the exact quoted text) is retained by this project's author and
can be produced to substantiate the claim if a good-faith party seeks to
verify or falsify it, the same accountability BIFP's own Phase 0 (§3.2)
requires of an escrowed claim generally, applied here to specimen identity
rather than to a financial or reputational stake. What is withheld is
public amplification of a private individual's identity; what is not
withheld is the claim's own checkability.

**A documented gap this specimen surfaces in the project's own tooling.**
`debasinizer`'s resonance-vocabulary detector is purely lexical (`resonat-`,
`wave`, `signal`, `pattern`, `echo`, `frequenc-`, `mirror`; see
`tools/debasinizer/debasinizer/resonance.py`) and does not and structurally
cannot match an undefined variable raised to a power — yet the exponent is doing the identical rhetorical job
lexical resonance vocabulary does: borrowing genuine mathematical structure
(here, exponentiation) to imply totalizing, dimensional, or cosmic-scale
amplification, without any operationalization behind it. The mechanism this
glossary tracks is broader than the keyword lists any current tool in this
project implements — notation itself can launder precision, not only words.
This is named here as a scoping note for future tooling work, not built:
a regex-based detector for "unusual exponents/operators applied to
undefined single-letter variables in declarative, non-derivational prose"
would need real negative-testing against legitimate applied-math and
physics writing before shipping, to avoid the false-positive risk of
flagging every genuine equation a paper states without re-deriving inline.

**The test.** Ask whether the "law" would remain true, checkable, and
independently re-derivable if every reference to its author's name, titles,
and self-conferred field were removed from the text. A physics law survives
that removal — the law and the discoverer's continued authority are
separable, which is exactly Foucault's point about what changed in
scientific discourse. A founder-of-discursivity "law" does not survive it,
because the law and the author's authorized position were never separable
objects to begin with.

---

## Closing note

This glossary will grow as new laundered terms are found and verified — the
same incremental, as-we-go discipline the rest of this repository runs on. An
entry is added when a specific instance of the drift has been located and
checked against a primary source, not when a term merely sounds like it might
qualify. Suggested entries without that grounding stay out until they clear
it.
