# Results: model of Appendix D's tensor-contraction exponent
Scored against eth_appendixD_model/PREREG.md (a2c8887). Read: Appendix D in full (D.1-D.4.7) plus rendered pages 2 and 57. Code `appendixD_model.py`, raw `appendixD_results.json`, deviations G-1..G-8. Arithmetic on the paper's derived bounds; algorithm not run; lemma proofs (D.3 packing, D.4 Cauchy deformation, D.5 tapered Hermite recovery) read, not re-derived.

## Correction first
My earlier statement (prereg, RESULTS_eth_paper.md) that Theorem 1.1's general exponent is n sqrt(loglog n)/sqrt(log n) was wrong; the printed theorem is O_k(n loglog n / sqrt(log n)), fixed density O(n / sqrt(log n)) (G-1; fixed in RESULTS_eth_paper.md).

## What Appendix D does (as read)
- Counting = contraction of a Boolean tensor network with <= Cs edges, max degree <= ceil(s^{9/10}) (Theorem D.1): time (s+L)^{O(1)} 2^{O(s/sqrt(log s))}.
- Fixed density (D.2): clause network, s = n+m, exponent O(n/sqrt(log n)). Arbitrary density (D.3): sparsification with sigma = 1/ceil(sqrt(lambda)), parity queries, Lemma D.2 encodes the retained monomials of the parity-lifted product with O(n nu) wires (nu = loglog n), s = n nu, exponent O(n nu / sqrt(lambda)).
- Contraction algorithm: recursion on wires; at depth d, M_d <= C s 8^{-d}, u_d = eps lambda/2^d; "mode" monomials number exp(2 pi sqrt(M p_t/D_t)) with p_t ~ 24 M D_t/u (tapered Hermite multiplicities); r = 64 groups cut edges by 3/32 per level; leaves (<= H = s/floor(sqrt(lambda)) edges) are summed directly.

## Model (leading-order explicit constants, G-2..G-6)
Per-s exponent in bits = 1/floor(sqrt(lambda)) + sum_d (2 pi sqrt(24)/ln2)(M_d/s)/sqrt(u_d) ~ (1 + 19,527 C)/sqrt(lambda), where 19,527 = 16,077 (per-level constant: 2 pi sqrt(24)/(ln 2 sqrt(eps))) x 1.215 (sum_d 2^{-5d/2}). The edge constant C is the dominant lever.

## Crossovers (total exponent per n < 1; no re-crossing above in 3,000 samples)
Fixed density, k = 3, clause network (C = 4kD/(1+D)):

| D | lambda* | n ~ |
|---|---|---|
| 1 | 5.49e10 | 2^(5.5e10) |
| 4.27 | 1.00e12 | 2^(1.0e12) |
| 10 | 5.49e12 | 2^(5.5e12) |
| 100 | 5.49e14 | 2^(5.5e14) |

General density (parity branch, C/s = 75 / 148 / 247 for k = 2/3/4; log2 D0 = 246 / 336 / 435; sigma ~ 1e-8):

| k | lambda* (Appendix D) | lambda* (Section 6 model) | ratio |
|---|---|---|---|
| 2 | 6.03e15 | 1.01e13 | ~600x later |
| 3 | 2.54e16 | 3.48e13 | ~730x later |
| 4 | 7.54e16 | 8.72e13 | ~860x later |

Appendix D's lower asymptotic exponent (nu instead of nu^2) overtakes the Section 6 model only at lambda ~ 6e60 (k=2), 1.6e67 (k=3), 1.6e73 (k=4), n ~ 2^(10^60) and up; below that, Section 6's bound is cheaper in this model (at lambda = 1e16 Appendix D's total is 9.6-14x larger).

## Prereg scoring
| id | result | note |
|---|---|---|
| D-1 | Held | the improvement is in the loglog factors only: nu^2 (Sec 6.4) -> nu (general density) -> 1 (fixed density); the sqrt(log n) denominator is unchanged. |
| D-2 | Held with caveat | explicit eps, r, Delta, H, u_d, a_d; but the exponent constants are O_C(.) in the text; I used the paper's own derivation bound with leading-order p_t (G-2). |
| D-3 | Held | the "sharper" exponent gives a crossover ~600-860x later in lambda for general density than the Section 6 model; fixed-density crossovers (1e10..1e15 depending on D) are not comparable class-for-class. |
| D-4 | Held | every crossover is >= 5.5e10 (n >= 2^(5.5e10)). |
| D-5 | Held | no mismatch between Theorem D.1's s/sqrt(log s), Lemma D.2 (n nu/sqrt(lambda)) and the printed Theorem 1.1 (after my correction G-1). |
| D-6 | Held, premise wrong | different sigma (1/ceil(sqrt(lambda)) vs floor(sqrt(lambda))/nu^2 form), but the nu^2 -> nu gain comes from the contraction size s = n nu, not from sqrt(nu). |

## Reading
1. **The sharper exponent is real at the level of asymptotic form but costs a large constant.** Per unit of C the contraction pays about 2e4 over sqrt(lambda); with C ~ 75-250 (parity branch) this is ~1.5e6-5e6 nu/sqrt(lambda) per n, versus ~2-6e5 for the Section 6 route at its crossover. So Appendix D improves the rate (nu vs nu^2) while worsening the practical onset.
2. **Galactic, again.** The best-case (fixed density D = 1, k = 3) onset is lambda ~ 5.5e10; the general-density algorithm needs lambda ~ 6e15-8e16 (n ~ 2^(10^16)). Same conclusion as before: asymptotic, no solvable instance size benefits.
3. **Theorem D.1's "sufficiently large" threshold is unspecified.** Read literally, (D.5)'s u >= lambda^{4/5} needs lambda >= ~2^546-2^582 (G-7); the paper likely needs far less, but the constant is not stated. A careful reader would want it.
4. **My modeling is leading-order.** A different constant in the Chernoff bound, the 3M/32 shrink (vs 1/8), or tighter p_t would move the crossovers by modest factors; the ~1e10-1e16 range and the ordering (fixed density < Section 6 < Appendix D general) would not change unless those constants change by orders of magnitude.

## Not established
Correctness of D.3-D.5 (packing, Cauchy deformation, tapered Hermite recovery) or of the tuple counting; Appendix B; the proof's required n threshold; that actual runtime follows the modeled leading term.
