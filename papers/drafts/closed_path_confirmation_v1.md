# Closed-Path Confirmation: When a Governance Artifact's Own Test Suite Is Not Evidence of Binding

*v1 — filed 2026-08-31. Authors: operator + Claude (Sonnet 5).*

---

## A note on what kind of paper this is

This is a narrow, derivative sharpening, not a new mechanism, and it is
worth being explicit about that before anything else. Everything
load-bearing here already exists in this project's published work:
[`governance_binding_axiom_v1.md`](governance_binding_axiom_v1.md) §4
supplies the formal apparatus (policy π, proxy R, constraint set C,
feasible action set `Feasible(s)`) and already names "zero-cost-logged"
enforcement as category (a) with its own defeat condition.
[`laundered_vocabulary_v1.md`](laundered_vocabulary_v1.md)'s "Performed
Rigor vs. Demonstrated Rigor" and "Metrics vs. Soundness" entries
already state the general validity/soundness distinction this paper
narrows to one specific case. This paper's only actual contribution is
applying that existing distinction to a case those entries do not yet
cover explicitly — an **executable test suite** offered as evidence
that a governance artifact enforces its stated constraint — stating a
precise defeat condition for it, and checking that defeat condition
against one independently verified specimen.

An earlier internal pass at this material reached for new vocabulary
("teeth cosplay," a proposed "master attractor") and cited academic
sources that were never checked to exist. Both are dropped here
deliberately. Coining a new term for a distinction this project has
already published, and citing sources nobody verified, are exactly the
failure modes this paper is about — building both into a paper on this
subject would be the paper failing its own test before publication.

## Abstract

`governance_binding_axiom_v1.md` §4 distinguishes four enforcement
mechanisms and gives each a defeat condition, but does not yet address
a narrower, prior question specific to *executable* governance
artifacts: when a repository's own passing test suite is offered as
evidence that it belongs in category (a), (b), or (c), what
specifically makes that evidence weak? This paper states the answer as
a defeat condition rather than an intuition. A test suite authored,
populated, and evaluated entirely by the artifact's own creator
establishes only that the artifact is internally consistent with
itself — a **closed-path** confirmation. It does not establish that the
artifact's constraint holds against a path the creator did not
anticipate or did not write — an **open-path** validation — because a
closed-path pass is an existential statement (there exists a set of
author-chosen inputs on which the rule holds) offered in place of the
universal statement the binding claim actually requires (the rule holds
for all inputs an external, adversarial policy could construct). This
is elementary — the existential-for-universal substitution is a known
proof-theoretic error, not a new discovery — and the paper's contribution
is narrow: naming exactly what distinguishes a closed-path from an
open-path test for *code*, specifically, where "the tests pass" reads
as stronger evidence than the equivalent claim would in prose. We check
this against one independently verified specimen: a public repository
whose own test suite passed in full on independent reproduction (62 of
62 tests), but whose structured attack-fixture set — read fixture by
fixture rather than by pass/fail count alone — showed roughly one in
twelve fixtures (5 of 59) asserting their expected outcome directly
rather than deriving it by exercising the governed decision logic under
test. The specimen is described without identifying detail per this
project's standing redaction policy for individuals and small,
non-institutional projects. We state explicitly, and repeatedly, what
this single specimen does and does not establish.

---

## 1. The gap in the existing category (a) defeat condition

`governance_binding_axiom_v1.md` §4's category (a) — "zero-cost-logged"
— already has a defeat condition: *a trajectory where the logged
refusal did not change what the policy could do.* That defeat condition
is aimed at deployed systems: a live agent whose refusal is recorded
but does not remove the action from `Feasible(s)`.

A distinct, prior question arises for artifacts that are not yet
deployed against a live optimizing policy at all — a repository, a
library, a "policy admission" module — where the only evidence offered
for the artifact's category is its own test suite, run by its own
author, against fixtures its own author wrote. The existing defeat
condition doesn't quite reach this case, because there is no deployed
trajectory yet to inspect. What's needed first is a test of the
*evidence itself*, before the artifact is ever deployed: does a green
test suite, on its own, license the claim the artifact is making?

## 2. Closed-path and open-path, stated formally

Reusing §3's apparatus directly. Let `Feasible(s)` be the action set an
environment actually permits at state `s`, and let a **path** `p` be a
sequence of inputs presented to the artifact under test — a request, a
fixture, a scenario.

- **`P_closed`**: the set of paths authored, selected, and evaluated by
  the artifact's own creator. The oracle that decides whether the
  artifact's behavior on `p` is correct is also supplied by the
  creator.
- **`P_open`**: any path authored by an independent party, evaluated
  against an oracle the artifact's creator did not construct, or drawn
  from a real deployment where the input was not anticipated by the
  artifact's author.

Let `E(S, p)` be 1 if artifact `S` produces the constraint-respecting
outcome on path `p`, else 0. The claim an artifact's README or citation
context typically makes, stated as a universal:

> ∀ p ∈ P_all : E(S, p) = 1

What a passing test suite actually establishes is the weaker,
existential statement:

> ∃ P_closed ⊆ P_all such that ∀ p ∈ P_closed : E(S, p) = 1

**The gap is the substitution of the second for the first.** This is
not a claim about test quality — a closed-path suite can be large,
well-documented, and genuinely well-engineered, and every individual
assertion in it can be true. The gap is structural, not a matter of
rigor: an existential statement over a set the author controls does not
entail a universal statement over a set the author does not control,
regardless of how carefully the existential statement was demonstrated.
This is the same point `laundered_vocabulary_v1.md`'s "Metrics vs.
Soundness" entry already makes in general form — a metric (test pass
rate) can rise while the thing it proxies (the constraint holding
against a real adversary) is untouched — narrowed here to the specific
case where the metric is a test suite and the proxy failure is
invisible precisely because passing tests read, to most readers, as
unusually strong evidence.

**Defeat condition for a `P_closed`-only binding claim:**

> A path `p ∈ P_open` can be constructed — authored independently, or
> drawn from real deployment — on which `E(S, p) = 0`.

**What would move an artifact's evidence from closed-path to open-path
without waiting for a real adversary to find the gap:** fixtures whose
expected outcome is *derived* by re-executing the governed decision
logic against ground truth external to the fixture (a separate,
independently-specified oracle), rather than *asserted* as a literal
constant chosen to match whatever the code under test already returns.
The distinction is checkable by reading the fixture's assertion, not
by running the suite — a fixture that asserts `expected = X` where `X`
was set by hand to equal the code's own output on that input is
closed-path by construction, however many such fixtures exist and
however consistently they pass.

## 3. Relation to existing published vocabulary

This distinction is not new to this project. `laundered_vocabulary_v1.md`
already separates *Performed Rigor* (the formatting of rigorous work —
citations, formal labels, structured argument) from *Demonstrated
Rigor* (whether the argument survives an independent party attempting
to re-derive it), and separately separates *Metrics* (a number from a
defined procedure) from *Soundness* (whether the thing the number
proxies is actually true). `basin_attractors_v1.md`'s Basin-Immune
Falsification Protocol already requires, at Phase 2, an independent
red team — precisely because an author's own test suite is understood
there as insufficient on its own.

What none of the existing entries state explicitly is the code-specific
form: that a test suite is a more persuasive-looking instance of
"performed rigor" than prose is, because "all tests passing" carries
an unusual amount of assumed objectivity — a green checkmark reads as
mechanical, author-independent confirmation even when the mechanism
producing it (fixture authorship, oracle selection) is entirely
author-controlled. Naming that specific case, and giving it its own
checkable defeat condition (§2 above), is this paper's actual and only
new content.

## 4. Specimen (redacted)

**Sourcing tier and redaction, stated up front.** This specimen was
independently checked by this project — the repository was cloned
directly and its test suite executed, not read about secondhand — but
the repository, its author, and any identifying detail are withheld
here per this project's standing policy for private individuals and
small, non-institutional projects (see `laundered_vocabulary_v1.md`'s
"A note on redaction" and its own precedent, the redacted "Metrics vs.
Soundness" specimen). The findings below are the specific, checkable
facts from that audit; nothing about the specimen's identity, its
author's other work, or any broader claim about a "series" of related
repositories is asserted here — see §5 for what is explicitly excluded.

**What was checked.** A public GitHub repository presenting itself as
policy-admission / governance infrastructure — code that evaluates
whether a proposed action should be admitted against a declared policy
— was cloned directly and its test suite run without modification:
**62 of 62 tests passed on independent reproduction.** Separately, the
repository's own attack-fixture set — 59 fixtures, each intended to
exercise the admission logic against an adversarial or edge-case
scenario — was read fixture by fixture, not evaluated by pass/fail
count alone. **5 of the 59 fixtures assert their expected outcome
directly** (a literal constant matching the code's own output on that
input) **rather than deriving it** by computing the expected admission
decision from an independent specification of the policy being tested.
The remaining 54 fixtures do derive their expected outcome from
independently-specified inputs, and are not implicated by this finding.

**Reading this against §2's defeat condition.** The 62/62 pass rate
(source: this project's own reproduction, per §4 above) is real and is
not disputed — the code does what its own test suite says it does.
What the fixture-level read adds is the finding that a non-trivial
fraction (5 of 59, roughly 8.5% — source: this project's own
fixture-by-fixture count, not an external source) of the artifact's own
adversarial evidence is closed-path by the §2 definition: the oracle
for "what should happen" was the code's own behavior, not an
independent specification of correct policy admission. This does not
mean the artifact's constraint fails to bind — no `P_open` path was
constructed and run against it in this check, so the artifact has not
been shown to fail, only shown to be under-evidenced on 5 of 59
fixtures specifically. That is a narrower and more precise finding than
"the artifact doesn't work," and it is stated at exactly that strength,
not beyond it.

## 5. What this paper does NOT establish

- **Does not establish that the specimen's constraint fails to bind in
  deployment.** No `P_open` path was constructed and tested against
  the artifact; §4's finding is about the evidentiary basis offered
  (5 of 59 fixtures under-specified), not a demonstrated defeat of the
  artifact's actual behavior.
- **Does not extend to any other repository, by the same author or
  anyone else.** Only the one repository described in §4 was
  independently cloned and audited fixture-by-fixture. A broader claim
  that a whole series or "wardrobe" of related artifacts shares this
  structure was considered during this project's internal process and
  is explicitly not made here — it was not independently checked for
  any artifact beyond the one in §4.
- **Does not claim intent.** Nothing here establishes that the 5
  under-specified fixtures were written to create a false impression
  rather than as an ordinary, unremarked oversight in test design — the
  two are indistinguishable from the fixture content alone, and this
  paper does not guess between them.
- **Does not propose a numeric threshold or ratio** (e.g., a
  closed-path-to-open-path ratio a community should be judged against).
  A single specimen cannot support a general threshold, and a paper
  proposing one without a base rate across many artifacts would be
  making exactly the evidentiary error §2 describes, aimed at itself.
- **Does not address the social or community layer** — whether
  observers of a governance artifact apply real scrutiny or defer to
  its test-passing status — which this project's internal process
  explored as a separate, distinct question and found no independently
  checked specimen for. That question is out of scope here and is not
  asserted as established anywhere in this paper.
- **Does not use "teeth cosplay," "ETCPC," or any other new coinage.**
  See the opening note: the distinction this paper draws already has
  names in this project's published work (§3), and inventing a new one
  was judged to add branding, not content.

## 6. What would strengthen this beyond a single specimen

A base rate across multiple independently-cloned governance artifacts
— the fraction of each one's adversarial fixtures that derive versus
assert their expected outcome — would let §2's defeat condition move
from "checked once" to "checked at scale," and would be the natural
next step before any claim resembling a general pattern is made. This
is a concrete, tractable measurement a text-scanning tool could partly
automate (flagging fixtures whose expected-value literal matches a
constant found nowhere else in the specification, as a lead for human
or agent review — never as a verdict on its own), rather than a claim
this paper is in a position to make from one specimen.

---

*Sources: `governance_binding_axiom_v1.md` §3–4 (formal apparatus and
existing category taxonomy, cited not restated); `laundered_vocabulary_
v1.md` ("Performed Rigor vs. Demonstrated Rigor," "Metrics vs.
Soundness," and its redaction precedent); `basin_attractors_v1.md`
(Basin-Immune Falsification Protocol, Phase 2's independent-red-team
requirement). The §4 specimen is this project's own direct clone-and-
audit of a public repository, redacted per this project's standing
policy; no other primary source was consulted for that finding.*
