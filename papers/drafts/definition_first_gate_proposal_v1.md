# A Definition-First Gate: Proposal, Not Yet Built

*Status: PROPOSAL. Filed 2026-08-18. Authors: operator + Claude (Sonnet 5).
This is not a research paper and should not be read as one — it is a staged
idea for future consideration, explicitly lower-commitment than the rest of
`papers/drafts/`. No implementation exists. Nothing here has been through
this project's own verification tooling the way a normal draft would be
expected to before promotion, and it is not on a path to promotion until
that changes.*

---

## The problem, already fully verified elsewhere in this repo

[`case_studies/2026-08-18_grok_falsifiable_agi_definition_oracle_loop.md`](../../case_studies/2026-08-18_grok_falsifiable_agi_definition_oracle_loop.md)
documents a complete, dated, sourced specimen of the failure this proposal
is about. A public formalization of "intelligence" stipulated `R := reality`
as an unexamined ground term, then built a full apparatus on top of it —
`I(S)`, `G(S)`, an `AGI_TEST` procedure, an abstraction-selection operator —
that was iteratively "hardened" against two rounds of counterexamples
without anyone checking whether `R` itself, as defined, carried any value.
`ε` was never once computed against reality directly; only against whatever
procedure supplied `E`, and nothing in the formalism specified or defended
that procedure. Two rounds of apparently convergent revision were locally
valid and globally static, because the vulnerability was never in a clause
that could be patched — it was in the ground term nobody checked first.

The general pattern this specimen instantiates: a formal apparatus can be
internally consistent, iteratively hardened against real objections, and
still rest on a definition that has no value, is lossy, or is unfalsifiable
from its first line — and none of that shows up by inspecting the equations,
because the equations are downstream of the definition, not upstream of it.

## The proposed rule

Check a definition for value, falsifiability, and information-loss *before*
any equation built on it is worth evaluating. Not as a replacement for
existing checks (`Metrics vs. Soundness` and `Performed Rigor vs.
Demonstrated Rigor` in `laundered_vocabulary_v1.md`, and `attractor_scan`'s
`Unglossed Formal Object` detector all describe adjacent failure shapes) but
as a sequencing discipline sitting upstream of all of them: don't spend
verification effort on a formalism's internal consistency until its ground
terms have separately earned scrutiny.

## Why this doesn't reduce to a library dependency

This was checked directly in conversation before this proposal was filed,
not asserted from a fixed prior view, and the answer held up:

- A symbolic algebra system (e.g. SymPy) verifies whether an equation's
  *manipulation* is valid — whether step B follows from step A. It has no
  way to evaluate whether the *symbols* mean anything. The Grok specimen's
  algebra was never wrong; `εn < ε0` failing when `ε0=0` is a correct
  evaluation of a correctly-stated inequality. A symbolic-algebra layer
  bolted onto a pipeline like this would make a hollow definition's
  downstream math look *more* rigorously checked, not less hollow.
- A formal proof assistant (Lean, Coq) goes further — it can check logical
  consistency of a system, not just algebraic steps. But this project
  already has a dated, documented case that even kernel-level formal
  verification is not sufficient: `basin_attractors_v1.md` §2.9's
  CollatzLean incident, where a Lean kernel soundness bug let a formally
  verified proof system accept a proof of something false. Formal
  verification checks a system's internal consistency; it does not and
  cannot check whether that system's ground terms correspond to anything
  real. "Does this definition have value" is a question about the world,
  not about a formal system, and no formal-verification library closes that
  gap because it is not a gap of that shape.

## What would actually be required for the full version

The same close-reading, cross-checked, primary-source-grounded judgment
loop this project already runs by hand for every case study and paper in
this repository — the thing a human or an LLM reviewer does, not a thing a
library does. That doesn't compress into a protocol with a reference
implementation the way the Noether-Temporal Coherence Test Protocol
compresses into `tools/basin_depth/`. This is the concrete reason this
proposal stops at "proposal": there is no honest path to a `protocols/`
entry and a reference tool for the full claim with tooling currently
available to this project, and building a partial version that *looks* like
it checks definitional value while actually only checking definitional
*shape* would be exactly the performed-rigor failure this proposal exists
to name.

## The first honestly-scoped slice that would be buildable, if wanted

A structural check on a `DEFINE`-block: flag any symbol stipulated via `:=`
(or an equivalent assignment form) that no later text in the same document
ever subjects to a defeat condition, falsifiability language, or a named
external procedure. This is a direct extension of `attractor_scan`'s
existing `Unglossed Formal Object` detector's own scope discipline — it
would catch the *shape* of what happened to `R` in the Grok specimen
(asserted, never referenced by anything that could break it), explicitly
without claiming to judge whether the definition is true, valuable, or
non-lossy. Same contract as every other scanner in this toolkit: a lead for
a human to check, not a verdict. Not built. Proposed here so the scope cut
is on record rather than reconstructed later.

## A second, complementary slice: static binding of a mutable referent

Distinct from the slice above (which flags a symbol with no defeat
condition anywhere downstream), this one flags a different, more specific
shape: a `DEFINE`-block symbol whose ordinary referent is understood to be
observationally updated or time-varying, bound instead as a single static
value reused identically at every reference — no time index, no "as of,"
no revision or update mechanism named anywhere in the document.

This is not a new observation about the Grok specimen; it is already on
record in this repo, just not yet folded into this proposal's buildable
slices. `case_studies/2026-08-18_grok_falsifiable_agi_definition_oracle_loop.md`'s
own "A Second, Independent Finding: R Is Treated As a Fixed Primitive"
section names it directly: `R := reality` carries no time-index anywhere
in the DEFINE block or the loop that follows, so `ε := consequential
error(P,R)` cannot in principle distinguish "the model's prediction was
wrong" from "reality itself changed since the model last checked" — both
present identically as a rise in `ε`. If `R` is used as a fixed value, the
formalism has already failed before a single equation is evaluated,
independent of whether `R` ever gets a defeat condition elsewhere. A term
can clear the first slice (someone eventually writes a falsification
condition for it) and still fail this one, because that falsification
condition is being run against a moving target frozen at a single instant.

The check itself: does the term's ordinary meaning denote something
observationally updated over time (reality, the market, consensus, the
field, "what is currently understood")? If so, is it bound with a
time-index or revision hook (a `t` subscript, "as of [date/event]," a
named update procedure), or is it bound once and referenced identically
throughout the document? The latter is the flag. This needs a short,
explicit list of known-mutable-referent terms to trigger on — not an
attempt to infer mutability from first principles, which would
reintroduce the same judgment-call risk the first slice avoids by staying
symbol-agnostic. A narrower net than the first slice, but a more
mechanical one: it does not require confirming an *absence* of language
anywhere in the document (the first slice's hardest part to do reliably),
only a presence check on the binding itself.

**Falsifier, same contract as the first slice:** if a material fraction of
`DEFINE`-block symbols bound to known-mutable referents turn out to cause
no soundness problem despite static binding — treating "reality" or
"consensus" as fixed within a document's scope doesn't actually matter to
most real specimens' arguments — this slice loses its priority and becomes
a narrower, situational check rather than a default flag.

## A provenance note, now checked against the source

*Updated 2026-08-18: an earlier session's repository-access attempt to this
note's sibling project failed for reasons unrelated to either project's own
tooling; a later session's attempt succeeded and the claim below was checked
directly against that project's own internal material, not reconstructed from
memory.*

A sibling, non-public project does carry a rule matching this one — filed
internally as one candidate item in a cluster of related detection-mechanism
proposals, not shipped tooling, not wired into any automated pipeline, and not
itself a citable public source (that project's own scope rules keep its
internal design material out of this repository; this note describes the
match at the level the public statement above already operates at, without
importing that material). Its first line states, close to verbatim, "check
definitions, not derivations": in a stacked-formalism document the load-
bearing failure typically sits at the natural-language-to-formalism binding
step — a definition asserted rather than earned — rather than inside the
downstream math, which is frequently locally sound and therefore reads as
verified once a reader checks the algebra and stops. It was arrived at in
part from a real specimen in that project's own corpus where a downstream
algebraic apparatus was independently confirmed correct while the definition
it was built on was found illegitimate — the "prior paper checked out
structurally while its definition made the work meaningless" shape the
operator recalled, now confirmed rather than reconstructed.

What does not match exactly: the internal item is broader than this proposal
— it also covers prose-based term-binding failures (a word traded between
shifting referents across an argument, not only a symbolic `DEFINE` block)
— and it is filed as one candidate among several related mechanisms, not
promoted past candidate status, with no automated detector built for it
either. So this proposal and that internal item are two independent, unbuilt
statements of close to the same idea, arrived at separately under common
authorship — genuine convergence, not one confirming the other. Per this
project's own standard for external convergence generally (`mirror_test_v1.md`,
`laundered_vocabulary_v1.md`), convergence under shared authorship influence
is suggestive, not independent verification, and is not elevated to grounding
here for that reason. The Grok specimen remains the grounding; this section
is retained as a resolved provenance note, not a citation.

## What this proposal does not claim

Does not claim a definition-first gate is buildable as a full, automated
check in this project's current tooling — the section above states
directly why it is not, and that conclusion, not a call to build toward it,
is this proposal's actual content. Does not claim either narrow structural
slice described above would catch every instance of this failure class:
the first catches only its most literal shape (an unreferenced stipulated
symbol); the second catches only static binding of a term from a short,
explicitly curated list of known-mutable referents.

The second slice's miss-size is not a bounded, known limitation — it is
genuinely unmeasured, and stating a curated list makes it *look* scoped
without actually scoping it. Whether the gap between "terms this list
catches" and "terms that are actually pivotable between fixed and moving
value" is small or huge, in any given domain, is not established here and
is not established by making the list longer. A longer list does not
shrink the gap in a measurable way, because the underlying problem —
deciding whether a given term's referent is fixed or observationally
updated in the context of a specific document — is the same
world-knowledge judgment call the "Why this doesn't reduce to a library
dependency" section already rules out of scope for the whole gate, just
relocated one level down and dressed as a smaller, list-shaped problem.
Building a general classifier for "pivotable" semantics is not a scaled-up
version of the second slice; it is the same open problem the full gate
already fails to reduce to a library, and should not be mistaken for a
tractable engineering task because it can be entered from a shorter list.
This gap is named here explicitly so a future pass does not rediscover it
and re-litigate the same conclusion. Does not claim any implementation
exists, or that this proposal is scheduled for
implementation. Does not claim the sibling-project match strengthens this
proposal's evidentiary basis beyond the Grok specimen — the provenance note is
now confirmed to exist and to match closely, but two unbuilt, commonly-authored
statements of the same idea are convergence, not independent confirmation, and
the note is retained for context rather than as grounding. Does not extend or
supersede `Metrics vs. Soundness` or
`Performed Rigor vs. Demonstrated Rigor` in `laundered_vocabulary_v1.md` —
this is an adjacent, sequencing-focused idea, not a replacement for either.
