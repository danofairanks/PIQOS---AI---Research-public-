# Results: Section 3's common routine (Definition 3.1, Lemmas 3.2-3.3, Proposition 3.4, (3.14)-(3.16))
Scored against eth_section3_check/PREREG.md (c725de3). Read: Sections 3.1-3.5 in full. Code `section3_check.py` (reuses the Section 2 construction and Counter from `eth_counter_test`), raw `section3_results.json`. Exact arithmetic throughout (integers, Fractions, Z/12, Q[V]/(V^2), and the mod-(2^61-1) arithmetic of the Section 2 implementation).

## What Section 3 claims and my re-derivation
- **Definition 3.1 + its interpretation:** if C_{t,h}(x'_h - x_h) = 0 for h != g (the factor's assigned group), the kernel condition on rows P_{f,v}(t) gives <P_{f,v}(t), x'> = <P_{f,v}(t), x>; applying this one group at a time, the tuple (<P_{f,v}(t), x>)_{v in I_f} (hence the whole factor, a polynomial in these values) depends only on x_g and the measurements (C_{t,h} x_h)_{h != g}. Re-derived: linear invariance telescopes group by group.
- **Lemma 3.2** (any commutative ring A): for x_h in X_h(y_h), x_h - x_bar_h lies in ker C_h, so successive use of the invariance gives A_g(sum_h x_h) = A_g(x_g + sum_{h != g} x_bar_h); the set of assignments with measurement tuple y is the product of the X_{g,E}(y_g) and distributivity gives prod_g Sigma_g(y); summing over the (2D+1)^c tuples (each assignment has one tuple) gives Z_E. The representative scan and the Sigma scan each look at <= sum_g 2^{|S_g|} vectors per tuple: total <= 2 (2D+1)^c sum_g 2^{|S_g|}. The representatives need not satisfy the fixed bits E because A_g is defined on all of Q^n and the invariance holds there.
- **Lemma 3.3** (Moebius): replace positive powers of X_i by X_i (Boolean evaluations unchanged, degree not increased); multilinear coefficients c_{x,E} = sum_{U subset E} (-1)^{|E|-|U|} p_x(1_U) vanish for |E| > q; setting X = x and summing selects x_i = 1 on E. With (3.9) (the z^j coefficient of G_x has X-degree <= j <= J-1 = q), applied coefficientwise in R = A[z]/(z^J).
- **Hermite uniqueness:** J = floor(d_H/Q) + 1 gives QJ > d_H; the rational Hermite matrix of size QJ is invertible and its inverse acts on A by rational combinations.
- **Prop 3.4 count:** Q points x C_q pairs (U subset E, |E| <= q) x (3.12) = 2 r (2D+1)^{c} 2^{2n/r} vectors (c <= 2 tau n, |S_g| <= 2n/r); (3.15): eta^q C_q <= sum_s binom(n,s)(2 eta)^s = (1+2 eta)^n since eta^q <= eta^s for s <= q; with eta = R/Q and q = O(nR/Q): log C_q = O(n (R/Q) log(2Q/R)); (3.16) is the three costs.
- All steps close. No use of the specific bounded-occurrence structure: the routine is generic, as claimed.

## Numerics
- **Lemma 3.2 (general ring, arbitrary invariant factors):** 120 random instances (n = 3..6, r = 2..3 groups, random C_g with row absolute sums <= D <= 3, random invariant A_g given by lookup tables over (x_g, measurements of the other groups), E random, rings Z/12 [non-domain] and Q[V]/(V^2)): the paper's representative-scan routine equals brute force in 120/120; examined vectors never exceed 2 (2D+1)^c sum_g 2^{|S_g|} (0 violations).
- **Lemma 3.3 standalone:** 120 instances (n = 2..5, q = 0..3, random polynomials p_x of total degree <= q with x-dependent coefficients, over Q and Z/12): 0 failures.
- **(3.15)/(3.16):** 312 (n, q, eta) cases (n up to 200, q up to n+3, eta in {1/100,...,1}): eta^q C_q <= (1+2 eta)^n and log C_q <= q log(1/eta) + n log(1+2 eta), 0 failures.
- **Proposition 3.4 on the real Section 2.7 design** ((r,Q,R) in {(2,3,2),(2,3,3)}, n = 4,5, 12 formulas): the representative-based Z_{t,E,U} equals my earlier lambda-based Z (144 (t,E,U) samples, 0 mismatches); the full Taylor data computed with the representative routine equals brute-force H(t+z) mod z^J in all 12 runs; Hermite recovery returns the exact #F in 12/12.
- The vector-count bound of Prop 3.4 is not tight at toy parameters ((2D+1)^c with D = r^{2Q} dwarfs the realized counts); it was verified for the generic lemma (previous bullet) and re-derived, not stress-tested on the real design.

## Prereg scoring
| id | result | note |
|---|---|---|
| S3-1 | Held | all steps re-derive. |
| S3-2 | Held | 144/144 and 12/12 (representative routine = lambda-based = brute force). |
| S3-3 | Held | 120/120 including non-domain rings; count bound never exceeded. |
| S3-4 | Held | 120/120. |
| S3-5 | Held | 312/312; the vector-count bound on the real design was checked only in the generic Lemma 3.2 test. |
| S3-6 | Held | no gap; the E-restriction remark is correct (A_g lives on all of Q^n). |

## Reading
1. Section 3's routine is correct as written and is the generic core on which Sections 2, 5 and D's overall counting rest: it does not use any property of SAT, only (3.2), Definition 3.1 and the ring structure. My Section 2 implementation validated the same pipeline by a second, independent evaluation (lambda coefficients); the paper's representative-based evaluation agrees with it exactly.
2. The Section 3 -> Section 5 interface is consistent: Section 5 supplies A = Q[V]/(V^l) factors (tested elsewhere: Lemma 5.1/5.2) and the degree d = k(m_test + 2(l-1)) (3.2) (Lemma 5.2's degree control, tested), and Section 4 supplies Definition 3.1 (Lemmas 4.1-4.6, 4.8 tested). Every interface is therefore covered by at least one independent exact check.
3. What this does NOT cover: the bit-complexity statements for general factor evaluators (Appendix B, checked separately); performance at paper scale (not runnable).

## Not established
That Proposition 3.4's vector bound is attained or tight; the full theorem; independent review.
