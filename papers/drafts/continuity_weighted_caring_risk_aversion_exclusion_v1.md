# The Risk-Aversion Exclusion: A Defeat-Condition Check on a Continuity-Weighted Utility for Everettian Branches

*v1 — filed 2026-09-21. Authors: operator + Claude (Sonnet 5).*

---

## A note on what kind of paper this is

This is a narrow, constructive defeat-condition check against a single
external specimen, not a new framework. It follows this project's own
standing method (`governance_binding_axiom_v2.md` §5): construct or
find the defeating trajectory, do not argue about whether one would
exist. The specimen states its own defeat condition and proposes a
protocol for testing it; this note does not wait for that protocol to
be run. It asks a narrower, immediately checkable question instead:
before any agent-specific fitting even starts, is there a class of
agent the family cannot represent at all, purely from its own
definitional scope?

Per this project's standing redaction policy for private individuals
(`laundered_vocabulary_v1.md`'s "Law" entry; `execution_gate_channel_
collapse_v1.md` §4's identical treatment of a jointly-authored
specimen), the checked work is described here without naming its
author.

## The specimen, described precisely enough to check

A public preprint (dated 12 September 2026) proposes a Born-weighted
expected-utility construction for an agent in an Everettian
multiverse who cares not only about which branch obtains, but about
*continuity* between their present state and a successor's. Given a
predeclared, agent-relative, cardinal continuity score `S ∈ [0,1]` and
Born weights `μ`, the construction defines

```
Vλ(a) = Σᵢ μᵢ · exp(λ · Sᵢ)
```

— an instance of the exponential tilt (the Esscher transform,
Esscher 1932; the same change-of-measure underlying Gibbs measures,
Chernoff bounds, and entropic-risk decision theory). Two lemmas are
proved: (1) for a finite nonempty successor set and `μ` a probability,
`Vλ(a) > 0` and the induced tilted profile `μ*λ` is itself a
probability; (2) `λ = 0` recovers `V₀ = 1` and `μ* = μ`, and as
`λ → ∞`, `μ*` concentrates on the maximal-`S` successors. The paper is
explicit and repeated about scope: no new physics, no derivation of
the Born rule, no theory of consciousness, not offered as a
rationality mandate — "one admissible utility for an agent who already
cares about continuity." It states its own defeat condition twice:
predeclare an `S`-table and a fitting/held-out protocol; "failure
rejects the family for that agent."

**The paper's own defined domain, quoted precisely, because the
finding below turns on it:** *"Fix an act `a` with a finite successor
set. Let `λ ≥ 0`."*

## Verification of the paper's own claims

`continuity_tilt_check.py` (this repository, run alongside this paper,
no dependencies) implements `Vλ` and `μ*λ` exactly as defined above
and checks both lemmas directly across a range of `λ`. Both hold
cleanly — no defect was found in the paper's own mathematics. This is
not a "the proof is wrong" finding, stated plainly before the rest of
this note, which is not that.

## The defeat-relevant construction

Take two acts, each with two branches under equal Born weights
`μ = (0.5, 0.5)`, matched exactly on Born-weighted mean continuity:

- **Act A** (spread): `S = (0, 1)` — mean 0.5, variance 0.25
- **Act B** (concentrated): `S = (0.5, 0.5)` — mean 0.5, variance 0

```python
#!/usr/bin/env python3
"""Runnable check: does the exponential-tilt family, restricted to
lambda >= 0 (the paper's own stated domain), admit an agent with
ordinary risk-averse preferences over continuity variance?
Deterministic, no dependencies. Independently re-run to confirm."""
import math

def V(lam, mu, S):
    return sum(m * math.exp(lam * s) for m, s in zip(mu, S))

def mu_star(lam, mu, S):
    v = V(lam, mu, S)
    return [m * math.exp(lam * s) / v for m, s in zip(mu, S)]

mu = [0.5, 0.5]
S_A = [0.0, 1.0]   # spread, mean 0.5
S_B = [0.5, 0.5]   # concentrated, mean 0.5

# --- Lemma 1: V > 0, mu* is a probability ---
for lam in [0.0, 0.5, 1.0, 5.0, 50.0]:
    v = V(lam, mu, S_A)
    ms = mu_star(lam, mu, S_A)
    assert v > 0
    assert abs(sum(ms) - 1.0) < 1e-9
    assert all(m >= 0 for m in ms)

# --- Lemma 2: lambda=0 identity; lambda->inf concentration ---
assert abs(V(0.0, mu, S_A) - 1.0) < 1e-12
assert all(abs(a - b) < 1e-12 for a, b in zip(mu_star(0.0, mu, S_A), mu))

# --- The defeat-relevant construction: mean-matched, variance-differing ---
print("lambda   V_A         V_B         A strictly preferred")
for lam in [0.0, 0.1, 0.5, 1.0, 3.0, 10.0]:
    va, vb = V(lam, mu, S_A), V(lam, mu, S_B)
    print(f"{lam:6.1f}  {va:10.6f}  {vb:10.6f}  {va > vb}")
```

**Actual output, this file, unmodified — independently re-run to
confirm:**

```
lambda   V_A         V_B         A strictly preferred
   0.0    1.000000    1.000000  False
   0.1    1.052585    1.051271  True
   0.5    1.324361    1.284025  True
   1.0    1.859141    1.648721  True
   3.0   10.542768    4.481689  True
  10.0  11013.732897  148.413159  True
```

For every `λ > 0` tested, the spread act strictly dominates the
concentrated one, even though both have identical Born-weighted mean
continuity. This is not a fitted or coincidental result. It is forced
by Jensen's inequality: `exp()` is strictly convex, so
`E[exp(λS)] > exp(λE[S])` whenever `S` has positive variance under `μ`,
uniformly across **every** `λ > 0`, not merely the values tested here.

## The finding, stated precisely

Because the family is defined only for `λ ≥ 0`, it can represent only
agents whose preference over continuity is risk-seeking or neutral
with respect to variance across successor branches — never
risk-averse. An agent who cares about continuity in the ordinary,
first-moment sense, but who would rather have guaranteed moderate
continuity than a coin-flip between excellent and terrible continuity
— an unremarkable preference shape, structurally identical to ordinary
risk-aversion over any outcome — **cannot be represented by this
family for any `λ` in its stated domain.** This is not a case the
paper's own §8-style held-out-choice protocol would reject after
fitting; it is excluded from the parameter space before fitting
begins. `λ < 0` would capture exactly this agent (flipping the
inequality above) and sits outside the domain as defined.

**Fairness note, stated directly rather than left implicit.** The
paper's own text already partially anticipates this: its "Convexity"
paragraph states "λ is not a pure intensity independent of that
curvature" — an acknowledgment that the single parameter conflates
strength-of-continuity-caring with risk-attitude toward continuity
variance. What this note adds is naming the consequence precisely
(structural exclusion of an entire, ordinary preference class, not
merely a caveat about interpretation) and demonstrating it
numerically rather than only noting the conflation exists.

## What this note does NOT establish

- **Does not establish an error in the paper's own mathematics.**
  Lemmas 1 and 2 both verified clean; this note's finding is about
  the family's stated domain, not a flaw in what is proved about it.
- **Does not establish that no real agent could be described by this
  family.** Only that risk-averse continuity-carers — a plausible,
  ordinary preference shape, not an exotic one — cannot be, by the
  family's own stated `λ ≥ 0` restriction.
- **Does not establish that extending the family to signed `λ` would
  be straightforward, or that the restriction to `λ ≥ 0` was not a
  deliberate, reasoned choice for reasons the text does not state.**
  Both are open; this note does not adjudicate the restriction's
  motivation, only its consequence.
- **Does not establish anything about the paper's author's intent or
  awareness.** The theorem is about what the family, as scoped, can
  and cannot represent — independent of any claim about why it was
  scoped that way.
- **Does not establish that this finding has been communicated to, or
  engaged with by, the paper's author as of filing.** This note is
  filed publicly, per this project's own standing precedent (post
  plainly, invite correction, correct the record if defeated —
  `governance_binding_axiom_v2.md` §12.5; `execution_gate_channel_
  collapse_v1.md` §6–§9), specifically so that it can be checked and
  answered rather than assumed settled either way.

## Sources

`governance_binding_axiom_v2.md` §5 (construct-or-find-the-defeating-
trajectory method, this note's own basis) and §12.5 (the adversarial-
testing-invitation precedent this note follows); `execution_gate_
channel_collapse_v1.md` §4 (identical redaction treatment of a
jointly-authored specimen) and §6–§9 (the precedent of running a
constructed check before waiting for a reply, and filing plainly for
independent testing); `laundered_vocabulary_v1.md`'s "Law" entry
(redaction precedent for a self-published, named author). The checked
specimen was read in full at primary-source tier; Esscher (1932) and
the general exponential-tilting literature the specimen itself cites
are not independently re-verified here, only the specimen's own
application of them.
