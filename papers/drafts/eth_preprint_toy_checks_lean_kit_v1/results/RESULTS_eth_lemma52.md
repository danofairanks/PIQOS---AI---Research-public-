# Results: Lemma 5.2's degree control (ETH preprint, Sections 5.2-5.3)
Scored against eth_lemma52_check/PREREG.md (a499ef5). Read: Section 5.1 (integer lift L_i, Lemma 5.1 statement), 5.2 (Lemma 5.2 and its proof, the l = 2 worked example), 5.3 (degree d = k(m_test + 2(l-1)), d_H = kR(m_test + 2(l-1)), equation (5.5)). Code `lemma52_check.py`, raw `lemma52_results.json`. Exact integer multivariate arithmetic; e_j taken from the exact decomposition computed in the Appendix B check.

## The claim and my re-derivation
- Setting: m_test equations with polynomial arguments y_i of total degree <= d*; factor B_i(V) = sum_{j<l} e_j(y_i) h(y_i)^j V^j with deg e_j <= 1, h(Y) = Y(Y-1); product taken in Q[V]/(V^l); S_l sums the retained coefficients.
- Degree control: a term contributing to the coefficient of V^s has the form prod_i e_{j_i}(y_i) h(y_i)^{j_i} with sum_i j_i = s <= l-1; its degree is at most sum_i d*(1 + 2 j_i) = d*(m_test + 2s) <= d*(m_test + 2(l-1)). The bound holds coefficient by coefficient and for their sum. Without truncation the product has V-degree up to m_test(l-1) and input degree up to d* m_test (2l-1), which is quadratic in the budget (m_test ~ cn, l = n+1); truncation at V^l is what keeps the degree linear: an omitted term with j_i total >= l is divisible by 2^l at integer arguments (the congruence half, tested in the Appendix B check).
- Consequence (5.5): substituting replacement forms of T-degree <= R-1 into inputs of degree <= d gives deg_T H <= d(R-1) <= kR(m_test + 2(l-1)) with d* = k.
- The reading is exact: all steps are elementary.

## Numerics
- **Degree of each retained coefficient:** 120 random instances (l in 1..5, m in 1..4, d* in {1,2}, 3 variables, random integer polynomials of degree exactly d*), 347 retained coefficients (V^s, s < l): 0 violations of deg <= d*(m + 2s), and in all 347 the bound is attained exactly (for generic y_i the bound is tight); the summed polynomial's degree <= d*(m + 2(l-1)) in every instance.
- **Truncation necessary:** in the 60 instances (l <= 3, m <= 3) where the untruncated product was also computed, 22 had total degree strictly above d*(m + 2(l-1)) (those with m >= 2 and l >= 2); the retained product never exceeded it.
- **Worked example (text, l = 2):** p_2(Y) = 1 - 3Y^2 + 2Y^3 = (1-Y) + (2Y-1) h(Y) holds for all integers in [-20,20]; for two equations with y_1 = x, y_2 = y (d* = 1): retained degrees (V^0, V^1) = (2, 4), bound d*(m + 2(l-1)) = 4; untruncated degrees (2, 4, 6): the omitted V^2 term has degree 6, as the paper states.
- **Substitution (5.5):** 40 instances with random T-polynomial substitutions of degree <= R-1 (R in 2..4) for each variable: T-degree <= d*(R-1)(m + 2(l-1)) in 40/40 (equality in many), hence <= d* R (m + 2(l-1)).

## Prereg scoring
| id | result | note |
|---|---|---|
| LD-1 | Held | |
| LD-2 | Held | and the bound is attained: tight at 347/347 coefficients. |
| LD-3 | Held | 22/60 untruncated cases exceed the linear budget. |
| LD-4 | Held | identity and degrees (2,4) vs untruncated (2,4,6) as stated. |
| LD-5 | Held | |
| LD-6 | Held | no gap found. |

## Reading
1. Lemma 5.2's degree control is correct, tight for generic inputs, and does what Section 5.2 says it does: it converts the quadratic degree k m_test (2l-1) of the full product into the linear d*(m_test + 2(l-1)), the hypothesis (3.2) the common counter needs.
2. Together with the congruence tested earlier, Lemma 5.2 is fully checked (at the level of exact small cases plus the elementary proof).
3. Open in the ETH thread: Lemma 4.8's remaining claims (parameter feasibility, partly modeled), the precision bookkeeping (D.11), the overall induction in Appendix D, and the overall theorem; plus the paper's central claim itself remains unverified by any independent reviewer.

## Not established
Instances beyond l <= 5, m <= 4, 3 variables (tightness is generic, not proven by this test); (3.2)'s role in the Section 3 counter was checked in the Section 2 implementation only for the bounded-occurrence case.
