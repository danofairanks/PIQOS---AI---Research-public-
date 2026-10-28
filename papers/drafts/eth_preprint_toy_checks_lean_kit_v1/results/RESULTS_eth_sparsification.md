# Results: model of the sparsification step and the full algorithm (Prop 6.4)
Scored against eth_sparsification_model/PREREG.md (267d921). Read: Sections 5 (5.1-5.5), 6 (6.1-6.4), Lemmas 4.7-4.8, Appendix A (A.1-A.3). Code `full_model.py`, raw `full_model_results.json`, deviations F-1..F-7. Arithmetic on stated bounds; algorithm not run. Section 5's own derivations (Lemmas 5.1-5.2, Prop 5.3), Lemma 6.1-6.2 proofs and Appendix B/D not re-checked.

## What Section 6 + Appendix A do (as read)
1. Disjoint branching (A.1): split on a shared literal set H occurring in >= M^{c-|H|} width-c clauses; children partition satisfying assignments (Lemma A.1). Depth <= C n, B-branches <= Gamma n / M; node count <= (Cn+1)^2 2^{sigma n} for M the least power of two with Gamma*h <= sigma*M. Leaves: each variable in <= B = 2 sum_{j<k} M^j clauses.
2. Per leaf (Lemma 6.1-6.2): Tanner-code parity tests (<= 3n rows, <= D0 = 320000 B^2 mu^3 entries) then 3n greedily chosen rows of list length P = 20000 B^2 mu^2, each choice by counting common zeros (<= 3n (2m)^P calls). The system has <= 6n equations of <= 2^k max(D0,P) monomials.
3. Each count is a call to Theorem 2.2 (Section 5), which first branches on the <= n/sqrt(lambda) variables occurring in > b0 scopes, then runs the Section 3-4 counter with R = (beta+3) ceil(sqrt(lambda)), where beta is the least integer with b, w <= lambda^beta; precision l = n+1, so the Taylor degree is d_H = k R (m_test + 2(l-1)) ~ 8 k n R.

## Numbers (per-n exponent, model of F-1..F-4)
- At the previous (Section 2.6 base-case) crossover, lambda = 6.1e10, the full algorithm's total is far above 1 (delta = 8k(beta+3)*128 nu/sqrt(lambda) >> 1).
- **Crossover lambda\* (total < 1, no re-crossing above):**

| k | lambda\* | n ~ 2^lambda\* | beta | B at crossover | delta at crossover | sigma | e1 |
|---|---|---|---|---|---|---|---|
| 2 | 1.014e13 | 2^(10,136,111,304,704) | 5 | 5.2e5 | 0.226 | 6.1e-4 | 0.998 |
| 3 | 3.477e13 | 2^(34,773,542,280,669) | 6 (step from 7) | 3.5e13 | 0.211 | 3.4e-4 | 0.954 |
| 4 | 8.715e13 | 2^(87,152,688,623,488) | 8 | 7.6e22 | 0.227 | 2.4e-4 | 0.999 |

  (k=3 sits at a beta step, F-6.) For comparison: base-case model lambda\* = 6.1e10. So the full algorithm's saving regime starts at 165x (k=2), 570x (k=3), 1420x (k=4) larger lambda; n is 2^(10^13..10^14).
- Beyond the crossover the exponent falls like e1: k=3 total 0.69 (lambda 1e14), 0.13 (1e16), 0.019 (1e18); k=2: 0.47, 0.082, 0.012.
- **sigma (the sparsification overhead) is negligible at the crossover:** 3e-4 to 6e-4 of the exponent budget; e1/sigma ~ 1.6e3 to 8e3 for lambda 1e13..1e18 (k=2..4), growing slowly (both are Theta(nu^2/sqrt(lambda)) up to logs). The branching term 1/sqrt(lambda) ~ 3e-7 and e2, e3 are also negligible.
- B grows steeply with k at fixed lambda (k=2: 5e5, k=3: 3.5e13, k=4: 7.6e22 at lambda ~ 1e14), driving beta from 5 to 8 and delta up. B is "a fixed power of log n" only in the O-sense: for k=4 it exceeds lambda by 9 orders of magnitude at the crossover.

## Prereg scoring
| id | result | note |
|---|---|---|
| S-1 | Partly | same order in lambda (both Theta(nu^2/sqrt(lambda))), but constants differ by 10^3-10^4 (e1/sigma ~ 1.6e3..8e3): sigma never matters near the crossover. |
| S-2 | Held | B = 2 sum M^j with M = Theta(Gamma/sigma * log): polylog(n) for fixed k, constants grow fast with k (table). |
| S-3 | Held | m_test <= 6n (c = 6); dependence on B enters only via beta (scope and incidence powers of lambda), then through R = (beta+3) sqrt(lambda) and d_H = 8kRn. |
| S-4 | Held | crossover moves out by 165-1420x in lambda; sparsification does not lower it (it raises the Taylor degree via k, beta, m_test). |
| S-5 | Held | crossover increases with k (1.0e13, 3.5e13, 8.7e13). |
| S-6 | Held | Prop 6.4's "n/s = O(rho(n))" and the per-leaf exponent are consistent with the model: both Theta(n nu^2/sqrt(lambda)); no mismatch found in the exponent bookkeeping. |

## Reading
1. **No exponent-level inconsistency found in Section 6 / Appendix A / Section 5.5 bookkeeping.** The sparsification tree (2^{sigma n}), the branching (2^{n/sqrt lambda}) and the per-leaf Taylor/measurement/group costs all go to 0 per n as lambda grows, with the same ~ (log lambda)^2/sqrt(lambda) rate; the Taylor term dominates. The claim's asymptotic structure survives modeling of the step I had not covered.
2. **The regime where the algorithm beats brute force is far further out than the Section 2.6 toy case:** n ~ 2^(10^13) and up, depending on k. Still galactic; the headline cost is a limiting statement, not an algorithm.
3. **What drives the constant:** the Taylor-degree factor 8k(beta+3) (from l = n+1 precision, m_test <= 6n, scope/incidence powers). This is where an improvement (smaller precision l, fewer test rows, smaller R) would shift the crossover; Appendix D claims a sharper exponent via tensor contraction, which I did not model.
4. **Sensitivity of my reading:** beta depends on my derivation of w and b0 (F-3); a constant-factor change moves beta by 1 and the k=3 crossover by up to a few percent in lambda. The qualitative result (crossover ~ 1e13-1e14) is not sensitive to it; the precise lambda\* is.

## Not established
Correctness of any lemma (Tanner-code existence, the conditional-expectation argument, disjointness, Lemma 5.2's degree control); Appendix B (bit sizes) and Appendix D (improved exponent); that the algorithm's actual running time follows the model (poly factors dropped); behavior for n < 2^(10^9).
