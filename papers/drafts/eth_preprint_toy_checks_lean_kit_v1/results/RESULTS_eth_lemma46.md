# Results: Lemma 4.6 of the ETH preprint (coefficient and denominator bounds of the substitution rows)
Scored against eth_lemma46_check/PREREG.md (78640bb). Read: Sections 4.1-4.3 (Lemmas 4.1-4.3 and the interpolation formula (4.7)), 4.5 (copy placement (4.14)-(4.16)) and 4.6 (Lemma 4.6 with proof). Not read: Lemmas 4.4-4.5 (group choice by conditional expectations) and 4.7-4.8 beyond the parts used earlier. Code `lemma46_check.py`, raw `lemma46_results.json`. Executed: exact integer arithmetic.

## What Lemma 4.6 says and how it argues
- Statement: with d_den = (R-1)! Q!, d_den P_u(T) is integral for every auxiliary row u; the sum of absolute values of all its coefficients is <= 2^{O(Q log Q)}; same for the substituted rows P_{f,v} (placement (4.14) only adds coefficients in common columns and drops unused ones); M0, C^B and the rows are constructible in poly(D, Q, r) bit operations.
- Integrality: f_I(W0) = sum_{j<R} (-1)^{A0+j}/j! prod_{a<j}(2 W0 - 2(A0+a) I), each factor integral since 2 W0 = Q I - sum_s Pi_s; j! | (R-1)!; V0 is a permutation, so (R-1)! M0 is integral; phi_{u,y}'s denominators divide prod_{s in E} s | Q!.
- Norm: ||W0||_inf <= Q, factors <= 4Q, so ||M0||_inf <= R (4Q)^{R-1}, ||phi||_1 <= prod (1+1/s) <= 2^Q; row sum of d_den P_u <= d_den (1 + (1 + 2^Q) R (4Q)^{R-1}), log = O(Q log Q) since R < Q.

## Checks run (r, Q, R) over 19 parameter sets, R from 1 to Q+1, D up to 6,561 (all rows for D <= 1,024-ish, 700 random rows otherwise)
- (R-1)! M0 computed from formula (4.7) in integer arithmetic; for four small sets, compared entrywise with the Lagrange interpolant on R consecutive integers (exact Fractions): identical (4/4). So (4.7) is the intended interpolation.
- Integrality of d_den P_u(T) coefficients: holds for every checked row (0 failures; phi scaled by Q! integral in every case).
- Degree <= R-1 and sparsity |E_{u,y}| <= R-1: hold in all 19 sets.
- Row-sum bound: measured log2 of the largest row sum 2.6 .. 21.8 bits against the lemma's explicit bound 5.9 .. 55.3 bits; slack 3.3 .. 33.5 bits. ||M0||_inf measured 1 .. 129 against the bound R(4Q)^{R-1} = 1 .. 1.3e9. All 19 sets satisfy both bounds.
- At R = Q+1 the interval is {0..Q} and M0 = I (V0 (-1)^{W0} = I), so P_u = delta_u: the lemma is trivially true there (norm 1).

## Prereg scoring
| id | result | note |
|---|---|---|
| L-1 | Held | the lemma states integrality and a coefficient-sum bound; explicit form d_den(1 + (1+2^Q) R (4Q)^{R-1}). |
| L-2 | Held | proof is exactly the structural argument predicted (formula (4.7) with 2 W0 integral; denominators of phi dividing Q!). |
| L-3 | Held | bound is loose by 3-34 bits at the tested sizes. |
| L-4 | Held | no counterexample at 19 sets; all checks pass for R in [1, Q+1]. |
| L-5 | Held | integrality and the norm bound hold without R <= Q/6; only the "log = O(Q log Q)" step uses R < Q. |

## Reading
1. Lemma 4.6 is correct as stated for everything I could test, and its proof is a short exact-arithmetic argument I re-verified by reading (each step is elementary: norms of permutation sums, integrality of 2 W0, divisibility j! | (R-1)!, prod of distinct s | Q!).
2. A minor consistency point: Lemma 4.6 gives 2^{O(Q log Q)} with no log D term; Appendix B writes B_P = O(Q log Q + log D). The latter is weaker and consistent; the log D is unnecessary, since the proof sums rows through ||M0||_inf.
3. With Appendix B's bound on the rest of the arithmetic, the bit-size chain for the interpolation now has no unread dependency: Lemma 4.6 (rows) -> B.2 (sums) -> B.3 (Hermite/Bareiss).
4. Remaining unchecked pieces of the ETH preprint: Lemmas 4.4-4.5 (group choice by conditional expectations), 5.x degree control proofs beyond Lemma 5.2's tested congruence, 6.1-6.2 existence arguments (Tanner code, greedy selection) and Appendix A's tree-size proof, and Appendix D's D.3-D.5.

## Not established
Lemmas 4.4-4.5, 4.7-4.8 proofs; the bounds for parameters outside the 19 tested sets (the lemma is a general statement; evidence is finite); that the paper's overall theorem is correct.
