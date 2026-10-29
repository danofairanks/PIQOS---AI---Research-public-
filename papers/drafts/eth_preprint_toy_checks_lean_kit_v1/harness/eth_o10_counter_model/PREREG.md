# Prereg: O10 counter-model search (canonical-lifting consistency, ETH preprint Appendix D.4.1)
Written 2026-10-28 before any code or measurement for this item. Source of the object: `eth_induction_lemma/INDUCTION_LEMMA.md` section 1 (my reconstruction; the "tagged network" and "creation precision" bookkeeping are marked [added] there because the paper does not define the class the recursion acts on). O10 is the one obligation marked "R only" (read, never tested).

## 1. What O10 says (restated so it can fail)
Ring: f in Z[U] monic of degree e, irreducible mod 2; O = Z_(2)[U]/(f); A = O[V]/(V^ell); A_p = A/2^p. An entry created at precision kappa is an integer coordinate vector in [0, 2^kappa)^(e*ell) on the basis U^i V^j; its **canonical lift** is the element of A with exactly those coordinates. Z(N) := sum over bit assignments of the product of lifted entries, computed in A. Contract(N, d, p) must return Z(N) mod 2^p. Children are called at precision p_t >= p (the schedule pi_d is non-decreasing), retained vertices keep their description, packet vertices are created with kappa = p_t as canonical lifts of coordinates reduced mod 2^{p_t}.

Sub-claims:
- **O10a (congruence stability).** If any set of entries is replaced by canonical lifts of their coordinates reduced mod 2^q with q >= p, then Z mod 2^p is unchanged.
- **O10b (monotone chain).** Over a chain of three nested levels with precisions p0 <= p1 <= p2, replacing a random vertex subset at each level by the canonical lift of its value reduced mod 2^{p_i} leaves Z mod 2^{p0} unchanged, and the creation-precision invariant kappa(v) <= (precision of every later call) holds along the chain.
- **O10c (convention sharing).** The result depends on all levels using the *same* lift convention; the claim "reducing F(0) modulo the call's precision gives the required answer" is true only under that sharing.

## 2. Method (to be implemented after this file is committed)
Two independent implementations of the ring arithmetic, compared on every trial: (i) coordinate arithmetic on Python integers with reduction by f and V^ell; (ii) sympy polynomial arithmetic with explicit reduction. Any disagreement between them is a harness bug, fixed before any scoring, and logged.
Toy parameters: f in {U^3+U+1, U^4+U+1}, ell in {2, 3}, bipartite multigraph with 4-6 edges and 3-5 vertices, kappa in [1, 6], p0 in [1, 6], precision increments in [0, 4]. N = 2000 random networks per condition, seeds recorded, committed with the results.
Conditions: O10a; O10b; and three mutations that should fail, to show the test has power: (M1) non-monotone schedule (reduce to q < p, then evaluate at p) with an altered coordinate in [2^q, 2^p); (M2) mismatched lift convention (retained vertices lifted centered in [-2^(kappa-1), 2^(kappa-1)) in the child, canonical in the parent) with kappa < p; (M3) a packet vertex created at kappa > the precision of a later call, then truncated and re-expanded.
Also a mechanical schedule check of the paper's own formulas: pi_{d+1} >= pi_d, and p_t <= pi_{d+1} for the D.11 expression, on the lambda grid already used in `eth_D11_check`.

## 3. Predictions (with my probability)
- P1: O10a has 0 failures in 2000 trials (0.99). It is the statement that reduction A -> A_q is a ring homomorphism, so the products of congruent entries are congruent mod 2^q.
- P2: O10b has 0 failures (0.99); the kappa <= precision invariant holds along every chain.
- P3: M1 fails in at least 80% of trials where the altered coordinate is nonzero, M2 in at least 80% of trials with kappa < p and a nonzero high bit, M3 likewise (0.95 each). If a mutation does not fail where it should, the test lacks power and O10a/b results do not count.
- P4: the schedule check passes at every grid point (0.97; the added terms in pi_{d+1} are nonnegative, so a failure would mean a transcription error on my side).
- P5: overall, **no counter-model is found** (0.97). I expect this to be a null result and to upgrade O10 only from "R" to "T (abstract bookkeeping model)", not to "verified".

## 4. Defeat conditions
**For the O10 reading (the paper's induction is wrong at O10):** any trial in O10a or O10b with Z mod 2^p changed where the preconditions of section 1 hold (non-decreasing precision, shared canonical convention, the two implementations agree). That would be a minimal counter-model, and the instance would be published as is.
**For my check (the test is wrong or empty):** a mutation (M1-M3) that passes where it should fail; disagreement between the two implementations that is not a transcription bug; or a reviewer showing the abstract model omits something the recursion needs (see section 5).
**For the schedule check:** any grid point where pi_{d+1} < pi_d or p_t > pi_{d+1}.

## 5. What a pass does not show
- It tests ring congruence and precision bookkeeping, not the recursion. The identity (D.16), the valuation bounds (D.9, D.10), the mode expansion and Lemma D.5's recovery are other obligations (O2, O4, O5), checked separately at toy scale.
- It does not test that the paper's text defines packet-entry lifts as I reconstruct them (that reconstruction is marked [added]). A reading difference there would not appear in this test.
- Toy ring sizes (e <= 4, ell <= 3) are far from the paper's e = 4 lambda.
- Same model wrote the reconstruction and the test; agreement is not independent verification.

## 6. Deviation rule and stopping
Any change to a condition, parameter range or threshold after seeing data is logged in DEVIATIONS.md with the reason. Stop after the stated N; no additional trials if the results are clean. A counter-model, if found, is minimized and recorded before any interpretation.
