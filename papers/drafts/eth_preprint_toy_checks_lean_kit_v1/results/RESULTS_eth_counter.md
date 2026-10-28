# Results: implementation test of Section 2 of the ETH preprint
Scored against eth_counter_test/PREREG.md (d5f834c). Paper sha256 5b1612dc...8123. Code, raw outputs and deviations in `eth_counter_test/` (DEVIATIONS.md lists D-1..D-10). Executed by me: all numbers below are E1 for what ran.

## What was tested
Bounded-occurrence 3-CNF counting (paper Sections 2.1-2.7): construction of M0, C and rows P_u(T) from 2.7 alone; replacement forms by label/copy placement (Step 4); decoupled evaluation by fixing measurement tuples (2.4); Taylor data through inclusion-exclusion (eq 2.9); Hermite-style recovery of H(0) (2.5). Compared against brute-force #F and brute-force H(t+z) mod z^J. Exact arithmetic mod 2^61-1.

## Results
- **L1, construction (r,Q,R) in {(2,3,2),(2,3,3),(3,2,2),(2,4,3),(2,4,2)}:** M0 fixes ker C (every sampled basis vector has M0 psi = (-1)^j f(j) psi; all vectors of ker C fixed); sparsity |E_uw| <= R-1 holds for all nonzero M0 entries (max observed R-1 in every config). All checks true.
- **L2, generic algebra:** H(0) = #F, deg H <= occurrences x (R-1), and Taylor/Hermite recovery from brute-force data returns #F, in all runs.
- **L3, decoupled evaluation:** the measurement-tuple evaluation of Z_{t,E,U} combined by eq (2.9) equals brute-force H(t+z) mod z^J, in all runs; the dependence condition (2.5) (existence of lambda coefficients) held with 0 violations in all runs.
- **L4, end-to-end:** 81 random bounded-occurrence formulas (n=4: 36, n=5: 24, n=6: 12, n=7: 4, n=8: 3, n=9: 2; three parameter sets; satisfying counts 0..20) all return the exact #F; 81/81 pass all stages, 0 design violations.
- **Harness sensitivity (mutations, D-8):** removing the vanishing factors phi (`no_phi`) -> design violations and wrong counts (2 of 3 cases wrong, 1 right by chance); removing all measurements (`no_C`) -> violations and wrong Taylor data in 4/4, wrong counts in 3/4; dropping a single measurement row (`drop_row`) -> NOT detected at these sizes (equivalent mutant: the dropped direction is not occupied by any variable at n=3; not a harness failure but a limit on what small n can see).
- **Cost:** group-assignment evaluations per run divided by 2^n: ~48 (n=3), 65-96 (n=4), 97-192 (n=5), 175-384 (n=6), 291-530 (n=7), 500-864 (n=8), ~1200 (n=9); wall time 0.1 s (n=4) to ~110 s (n=9). Grows roughly like 3^n/2^n times a tuple factor; there is no speedup over brute force at any tested size.

## Prereg scoring
| id | result | note |
|---|---|---|
| C-1 | Held | |
| C-2 | Held | |
| C-3 | **Falsified** | Stage C was fully implementable from Section 2.7 alone; Section 4 was not needed or read. |
| C-4 | Held on range tested | 100% of 81 cases; tested n <= 9 not <= 16. |
| C-5 | Held | evaluation count exceeds 2^n by 50x to 1200x and grows with n. |
| C-6 | Not triggered | no mismatch with the paper on any case. |

## Reading
1. **The algebra of Section 2 is exactly right at small scale.** The construction in 2.7 (swap-permutation matrix V0, polynomial f of degree R-1 interpolating (-1)^j, M0 = V0 f(W0), rows (2.16), measurement rows from the non-fixed eigenvectors) does what the text says: low-degree replacement forms that restore the variables at 0 and decouple groups through shared measurements at t = 1..Q. This removes the cheapest way to doubt the paper (an algebra slip in the overview) for the bounded-occurrence core.
2. **It does not test the claim that matters for ETH.** Subexponential time requires the asymptotic parameter regime (2.19), the Taylor truncation q << n, sparsification, parity tests (Section 6) and tensor contraction (Appendix D). None of that is reached at n <= 9: here q >= n, c is huge, and measured cost exceeds brute force. A pass at small n is necessary, not sufficient. Equally, nothing here contradicts the asymptotic claim.
3. **Where the real risk now sits** (my judgment, not tested): the balance of the three exponential costs in (2.11) under (2.19) (log-cost bounds, Step 5 tail bound), the sparsification-to-bounded-occurrence reduction with polylog occurrence bound (Lemma 6.3/Prop 6.4), and Appendix D's improved exponent. The next test of value would implement the cost model: compute, for growing n, the actual log2 of (sum_j C(n,j)2^j) x (2D+1)^{2 tau n} x 2^{2n/r} with the paper's integer-rounded parameters (2.19) and see at what n it falls below n. That is arithmetic on the stated bounds, not a run of the algorithm; not done here.
4. **Source of truth.** The Lean kernel says nothing about this paper. For this claim, an independent reimplementation that returns exact counts on small instances is the first checkable evidence available outside OpenAI's group; it supports the algebraic core and nothing beyond it.

## Not established
Correctness of Theorem 1.1; Sections 2.8-2.9 and 3-6, Appendices A-D; efficiency of any implementation; behavior for n > 9.
