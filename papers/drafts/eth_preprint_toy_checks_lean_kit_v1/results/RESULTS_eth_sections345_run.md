# Results: bounded execution of Sections 3-5 (Theorem 2.2's pipeline) at toy scale
Scored against eth_sections345_run/PREREG.md (fd15498). Code `eth_sections345_run/sections345_run.py` (reuses `eth_counter_test` for the Section 2.7 design and the Section 3 representative routine, `eth_appendixB_check` for Lemma 5.1's exact e_j), raw `run_all.json`, `run_sweep.json`, logs. Arithmetic: exact over Z via the prime 2^127 - 1 with a signed lift, after checking that a computed bound on |S_l(H(0))| (<= 2^64 in all runs) is below half the prime; verified against exact integer brute force. First draft of the 6 named systems used a Python-hash-dependent random seed (non-reproducible designs); fixed to a deterministic seed (sum of character codes) and rerun; all results below are from the deterministic runs.

## What was executed (the composition not previously run end to end)
Input: a system of m_test F_2 polynomial equations over n variables (monomials of degree <= k, reduced mod 2, identically-zero equations dropped). Pipeline: integer lifts L_i; ring A = Q[V]/(V^l), l = n+1; factors B_i = sum_{j<l} e_j(L_i) h(L_i)^j V^j (Lemma 5.1's exact e_j); degree d = k(m_test + 2(l-1)), d_H = kR(m_test + 2(l-1)), q = floor(d_H/Q), J = q + 1; design from the Section 2.7 construction with random schedules (each equation a "factor", scope = its variable set, neutral factors for unused variables); Taylor data in A[z]/(z^J) by the Section 3 representative routine (Lemma 3.2) with inclusion-exclusion over all (E,U) (q >= n in every run, so all 3^n pairs); Hermite recovery per V-coordinate; answer = least nonnegative residue of S_l(H(0)) mod 2^l. Reference: brute-force N(P), brute-force exact integer S_l(H(0)) and its V-coefficients, brute-force H(T) in A[T] (for n <= 5).

## Results
- **6 named systems** (n = 4; m_test 2-3; k 1-3; one unsatisfiable): 6/6 return the exact N(P); exact integer S_l(H(0)) equal; every V-coefficient of H(0) equal; decoupled Taylor data equal brute-force H(t+z) mod z^J; Hermite consistent.
- **Random sweep, 79 systems** (n = 4: 40 with (r,Q,R) = (2,3,2), 12 with (2,3,3), 12 with (3,2,2); n = 5: 12 with (2,3,2); n = 6: 3 with (2,3,2)); m_test in {1,2,3}, k in {1,2,3}, 1-3 monomials per equation, constants allowed):
  - N(P) correct: **79/79** (values seen: 0, 1, ..., 10, 12, 13, 16, 20, 37; 18 unsatisfiable systems; 31 with N not a power of two).
  - exact integer S_l(H(0)) equal to brute force: 79/79 (33 of them negative integers, so the signed lift and the mod-2^l reduction are exercised); all l V-coefficients equal: 79/79.
  - deg_T H <= d(R-1) <= d_H: 79/79 (brute-force H(T) computed for the 76 systems with n <= 5; its degrees up to 23 against bounds up to 36(R-1) or more); decoupled Taylor data = brute force: 76/76; Hermite systems full rank and consistent: 79/79.
  - largest run (n = 6, l = 7, J = 29-31): 11 s; 2.98 million Boolean vectors examined in total; no errors or exceptions.
- Magnitude: |S_l(H(0))| up to 2^64 (bound bits <= 64) while the answer is below 2^l <= 2^7: the pipeline relies on the mod-2^l reduction exactly as Section 5 states (Sl(H(0)) = N mod 2^l with N < 2^l).

## Prereg scoring
| id | result | note |
|---|---|---|
| X-1 | Held (N = 2^n not constructible) | exact N and exact integer S; I had hoped for N = 2^n; a nonzero F_2 polynomial always has a non-root, so such a system doesn't exist with nonzero equations (an empty system is handled separately in the paper). |
| X-2 | Held | degree and Taylor data. |
| X-3 | Held | minutes -> seconds: 0.1-11 s per system. |
| X-4 | Held | no mismatch. |
| X-5 | Held | see Reading. |

## Reading
1. The composition of Lemma 5.1's decomposition, Lemma 5.2's V-truncation and degree control, the Section 3 routine over A = Q[V]/(V^l), the Section 2.7/4 design with equation-sized scopes, Taylor data by inclusion-exclusion, and per-coordinate Hermite recovery returns the exact count on 79 + 6 systems, with the exact big integer S_l(H(0)) matching, not just its residue. This closes the one interface that had been checked only piece by piece.
2. What it does not do: nothing here exercises the asymptotic parameter regime (r = 2 groups; Q = 3 points; q >= n so the Taylor truncation is idle), the Section 6 sparsification-and-greedy front end beyond the small tests already reported, or Appendix D.
3. The earlier Section 2 bounded-occurrence test (81/81) and this run share the Section 2.7 construction and my Section 3 implementation; independent evidence for those pieces is the separate Lemma 4.6/4.5/Section 3 checks (exact, different code paths).

## Not established
Anything at scale; independent review; correctness of the headline theorem.
