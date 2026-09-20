# Substrate Binding Deficit: A Five-Question Instrument for Whether a Formalism Touches Its Named Mechanism

*v1 — filed 2026-09-20. Authors: operator + Claude (Sonnet 5).*

---

## A note on what kind of paper this is

This paper names one specific, narrow question — does a piece of
formal or technical-sounding work actually bind to the mechanism it
claims relevance to, or does it stay entirely inside its own notation —
and gives it a five-question checklist, applied here to three redacted
specimens. It is not a general theory of rigor. `laundered_vocabulary_
v1.md` already separates *Performed Rigor* from *Demonstrated Rigor* in
general form; this paper's contribution is a specific, checkable
instrument for one particular way that gap shows up: formalism (often
genuinely careful, internally consistent formalism) built entirely from
free, uninstantiated symbols that are never connected to a procedure
computable against a real running system. `closed_path_confirmation_
v1.md` asks a related but distinct question for *executable* artifacts
specifically (does the test suite's oracle come from the artifact's own
author); this paper's question is prior to that — it applies to purely
formal or prose claims that may never have executable form at all, and
asks whether the formalism touches a mechanism in the first place,
before any test suite could be relevant.

## Abstract

Five questions, checkable in minutes against any specimen claiming
relevance to a real operating system: (1) **Mechanism** — is there a
stated procedure computing the claimed property against a real system,
or only an algebraic property asserted of a free variable? (2)
**Measurement** — is there a demonstrated or proposed instrumentation
against an actually-operating system, or only scenarios internal to the
formalism's own notation? (3) **Robustness under shift** — is there any
claim about whether the property survives the underlying system
changing (weights updating, an index growing, continued training)? (4)
**Defeat conditions** — are there concrete, checkable failure
conditions against a real system, or only constructive witnesses inside
the theory? (5) **Substrate vocabulary** — does the specimen's own text
ever touch the actual mechanism-level vocabulary of the systems it
claims relevance to? A specimen scoring no/no/no/no on 1–4, with zero
substrate-vocabulary hits outside an opaque state symbol on 5, is
**redescription-only**: it may be a genuine, well-organized contribution
at the level of concepts, but it has not, on its own, bound anything a
real system does. We apply the checklist to three redacted specimens —
a working-paper pair and a companion piece, all circulating in the same
AI-governance-adjacent research community — and find all three score
0/4 on the binding questions with zero substrate-vocabulary hits,
despite each specimen honestly pre-conceding the gap in its own
limitations section. We show, as a load-bearing methodological point,
that this honest self-disclosure does not change the score: disclosure
and binding are independent properties, checked separately.

## 1. The five questions

1. **Mechanism.** Is there a stated mechanism linking the proposed
   property to actual system behavior — a procedure for computing it
   against a real running system, not an algebraic property asserted of
   a free variable?
2. **Measurement.** Is there a measurable instance demonstrated, or
   even proposed as instrumentable, against an actually-operating
   system, or are all "adversarial cases" hypothetical scenarios
   internal to the specimen's own formalism?
3. **Robustness under shift.** Is there any claim, prediction, or
   instrument for whether the property holds as the underlying system
   changes — weights updating, a retrieval index growing, a training
   run continuing?
4. **Defeat conditions.** Are there concrete, checkable failure
   conditions against a real system, or only constructive witnesses
   inside the theory (a proof that picks a hypothetical run and adds
   one stipulated defect)?
5. **Substrate vocabulary.** Does the specimen's own text, anywhere,
   touch the actual mechanism-level vocabulary of the systems it claims
   relevance to (for an ML system: attention, softmax, gradient, loss,
   reward model, RLHF/DPO, embedding computation — or the domain-
   appropriate equivalent) — or does every mechanism-adjacent term stay
   an opaque, uninstantiated symbol?

A **redescription-only** specimen answers no/no/no/no to 1–4, and check
5 finds zero substrate-vocabulary hits outside a single unlabeled state
symbol. That specimen may still be a genuine, well-executed
contribution — organizing concepts, offering normative structure,
producing a clear diagram — but it has not, on its own, bound anything
a real system does, and should not be cited or absorbed as though it
had.

**A necessary caution, stated as its own finding rather than a
footnote.** A specimen can pre-concede the gap in its own limitations
section, honestly, without that concession closing the gap.
Self-disclosure of "this does not guarantee substantive independence in
implementation" is evidence of intellectual honesty, not evidence of
binding — the two are logically independent, and this checklist's job
is to check for binding regardless of how honestly its absence is
disclosed. §3 below tests this directly against a specimen with an
unusually explicit disclaimer and finds the score unchanged.

## 2. Three redacted specimens

All three read in full at primary-source tier by this project; none
identified here per this project's standing redaction policy for
private individuals and small, non-institutional projects
(`laundered_vocabulary_v1.md`'s "A note on redaction";
`closed_path_confirmation_v1.md` §4's precedent applying the same
policy to a small repository).

**Specimens 1 and 2 — a working-paper pair on evidentiary/provenance
governance, self-published on preprint-hosting platforms.** Both build
an apparatus of stipulated predicates over abstract system state — a
basin-consensus function, an admissibility predicate, a "materially
operative system state" symbol — with algebraic properties declared
(e.g. one predicate implies another by definition) but no procedure
given anywhere for computing any of them against a real system.

- **Mechanism** — none. The core functions are free variables with
  stipulated algebraic properties; no procedure computes any of them
  against a real system.
- **Measurement** — none against a real system. A dozen-plus
  "adversarial cases" in each paper are scenarios internal to the
  formalism (system state assumed to behave a certain way), not
  instrumented tests run against an actual pipeline.
- **Robustness under shift** — not addressed. No claim about whether
  any predicate's status survives model weight updates, a growing
  retrieval index, or continued training.
- **Defeat conditions** — none against a real system. The papers'
  central theorem is a constructive witness *inside the theory*: choose
  a hypothetical run, introduce one stipulated defect. This establishes
  a logical separation between two predicates the papers themselves
  defined; it is not an experiment.
- **Substrate vocabulary** — zero hits. Neither paper contains
  attention, softmax, gradient, loss, reward-model, RLHF, DPO, or
  embedding-computation vocabulary anywhere. The two places either
  paper reaches toward a real AI system leave the model state as an
  opaque symbol, with the update function declared "versioned,
  justified" and never given a procedure.

Both papers pre-concede the gap in their own text, close to verbatim:
*"formal separation of [two of the paper's own defined objects] does
not guarantee substantive independence; those elements must also be
justified independently in implementation."* Per §1's caution, this
honest self-disclosure does not change the checklist's verdict: **0/4
on binding**, with the caveat named correctly by its own authors as a
still-open task, not a solved one.

**One genuinely exportable idea from these two specimens, named
precisely so it is not lost in the negative verdict:** the observation
that a real AI-assisted pipeline can retain cached context or outputs
across nominally separate function calls, defeating a claimed
"conclusion-blindness" property even when a process diagram shows clean
separated boxes for the formalism's own stages. That point does not
require substrate vocabulary to be correct or useful — it is a
governance-layer claim about information flow between calls, not a
mechanism-level claim, and this checklist's zero-substrate-hits finding
does not diminish it.

## 3. A third specimen, with an explicit disclaimer — testing §1's caution directly

**A jointly-authored working paper, from one of the same authors as
Specimens 1–2 together with a second author, self-published on a
preprint platform, describing a formal "handoff" architecture for
status carriage between governance boundaries.**

1. **Mechanism** — none, same shape as Specimens 1–2. The entire
   apparatus is symbolic predicate calculus over stipulated objects — a
   handoff function, a governed-object record, applicability/
   satisfaction/status predicates each ranging over `{applicable,
   inapplicable, unresolved}` or similar. No procedure is given
   anywhere for computing any of them against a real running system.
2. **Measurement** — none against a real system. A handful of
   "adversarial and diagnostic cases" are short hypothetical narratives
   — scenarios internal to the formalism, not instrumented tests run
   against real systems. The paper's theorems are proved by
   constructing named hypothetical objects, the same constructive-
   witness-inside-the-theory pattern as Specimens 1–2.
3. **Robustness under shift** — not addressed. No claim anywhere about
   whether any predicate's status survives a change to the systems it
   is nominally about, a corpus update, or repeated real-world
   handoffs over time.
4. **Defeat conditions** — none against a real system. Every
   "violation" case is a hypothetical scenario stipulated to satisfy
   the formalism's own failure predicates, not a reproducible failure
   demonstrated against running code.
5. **Substrate vocabulary** — zero hits, despite "AI systems" appearing
   as a listed keyword. No attention, softmax, gradient, loss,
   reward-model, RLHF, or DPO vocabulary anywhere. The paper's one
   gesture toward AI relevance stays entirely at the governance-object
   level — no AI mechanism is named or touched.

**Result: 0/4 on binding, identical to Specimens 1–2.** Three for three
across three separate papers checked this way.

**A sharper finding this specimen adds, beyond the checklist's own five
questions.** The paper's own references cite its two non-public
"source architectures" as internal, unpublished working records from
one of its authors, explicitly self-described in the paper's own words
as non-canonical, accessed by the authors themselves shortly before the
paper's final version. Both citations are private, unpublished
documents, self-described as non-canonical by the same two people who
co-authored the citing paper. This is distinct from, and sharper than,
the checklist's own substrate-vocabulary check: it is not that the
paper fails to touch AI mechanism vocabulary (already established,
item 5) — it is that the paper's own citation apparatus, for two of its
three foundational citations, resolves to sources that are **citable in
form but unverifiable in substance**, self-attested by the paper's own
authors. The paper's third foundational citation (Specimen 2 above) is
at least a public, permanently-hosted record — already scored 0/4
itself — so of this paper's three foundational citations, one is
public-but-already-failing and two are private-and-uncheckable.

## 4. What this checklist does NOT establish

- Does not establish that any of the three specimens are worthless or
  intentionally deceptive — all three explicitly disclose, in their own
  text, that implementation-level binding is unaddressed and left to
  future work; the 0/4 result is a description of present scope, not
  an accusation.
- Does not establish that formal, taxonomic work without substrate
  engagement is never valuable — §2's exportable idea is a direct
  counter-example inside the same specimens that score 0/4 overall.
- Does not establish that this five-question checklist is complete, or
  that a specimen scoring 0/4 is thereby proven harmful — it names a
  specific, checkable gap, not an overall verdict on a paper's worth.
- Does not establish anything about the systems' actual capabilities
  the specimens gesture toward (e.g. the real capabilities of named
  commercial AI models referenced in passing) — those claims, where
  independently checkable public facts, are treated as such and not
  disputed here; only the specimens' own formal apparatus is scored.
- Does not authorize using this checklist as an automated gate inside
  any production system — it is a human-applied reading instrument for
  paper-evaluation, the same discipline `laundered_vocabulary_v1.md`
  and `closed_path_confirmation_v1.md` apply by hand, encoded here as a
  checklist rather than as new tooling.
- Does not claim these three specimens are connected to each other
  beyond what is stated: two share an author; the third shares an
  author with those two. No claim is made about coordination, intent,
  or a broader "series" beyond the three papers actually read.

## 5. What would strengthen this beyond three specimens

A base rate across a larger, systematically-sampled set of formal
AI-governance papers circulating in the same research community — what
fraction score 0/4, and whether any score positively on items 1–4 while
still failing item 5 (a real mechanism check for a non-ML system, for
instance) — would let this instrument move from "checked on three
specimens" to "checked at scale." This paper does not attempt that; it
names the instrument and demonstrates it, consistent with this
project's own discipline against generalizing past what has actually
been sampled.

---

*Sources: `laundered_vocabulary_v1.md` ("Performed Rigor vs.
Demonstrated Rigor," "A note on redaction"); `closed_path_confirmation_
v1.md` (the related but distinct closed-path/open-path question, and
its redaction precedent, applied identically here);
`execution_gate_channel_collapse_v1.md` (a companion instrument checking
a different property — whether a gate's evidence channel is
independent of its action channel — of the same general specimen
class). All three specimens were read in full at primary-source tier by
this project directly; no other source was consulted for any finding
above.*
