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

## The one honestly-scoped slice that would be buildable, if wanted

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

## A provenance note, stated as exactly that

A sibling, non-public project reportedly arrived at a rule resembling this
one independently, after an incident in which a prior paper checked out
structurally while its definition made the work meaningless. This is
recorded here for context only — it has not been independently verified
against that project's own source or derivation record in this session (a
repository-access attempt failed for reasons unrelated to this project's
own tooling), and it carries none of the evidentiary weight the Grok
specimen above does. It should not be cited as grounding for this proposal;
the Grok specimen is the grounding.

## What this proposal does not claim

Does not claim a definition-first gate is buildable as a full, automated
check in this project's current tooling — the section above states
directly why it is not, and that conclusion, not a call to build toward it,
is this proposal's actual content. Does not claim the narrow structural
slice described above would catch every instance of this failure class,
only its most literal shape (an unreferenced stipulated symbol). Does not
claim any implementation exists, or that this proposal is scheduled for
implementation. Does not claim the sibling-project provenance note is
verified; it is explicitly marked as unverified above and should be read
that way. Does not extend or supersede `Metrics vs. Soundness` or
`Performed Rigor vs. Demonstrated Rigor` in `laundered_vocabulary_v1.md` —
this is an adjacent, sequencing-focused idea, not a replacement for either.
