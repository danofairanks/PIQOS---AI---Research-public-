# Results: Lemma 4.8's remaining claims (ETH preprint, Section 4.7)
Scored against eth_lemma48_check/PREREG.md (1f20755). Read: Lemma 4.8 statement and proof from rendered pages 34-35 (to resolve the extraction's radical/fraction loss; (4.17) confirmed as r = floor(sqrt(lambda)/nu^2), Q = floor(lambda/(128 nu)), R = (beta+3) ceil(sqrt(lambda)), tau = 1/(r lambda), eps = 1/(b r^2 lambda), D = r^{2Q}). Code `lemma48_check.py`, raw `lemma48_results.json`. Exact integer/rational arithmetic for the interval and parameter conditions; logs in base 2/e for the tail chain.

## Re-derivation by reading
- log2 D = 2Q log2 r <= 2 (lambda/(128 nu)) (nu/2) = lambda/128, using log2 r <= (1/2) log2 lambda <= nu/2.
- Balance: 2(b+w) D^2 <= 4 lambda^beta 2^{lambda/64} <= n (n > 2^{lambda-1}); 2 Q r^2 is a fixed power of lambda.
- Interval: with r >= 2, Q/4 <= mu = Q(r-1)/(2r) <= Q/2; A0 = floor(mu - (R-1)/2) >= Q/4 - R/2 >= Q/6 > 0 and A0 + R - 1 <= mu + (R-1)/2 <= Q/2 + Q/12 <= Q when R <= Q/6; containment of the integers within R/4 of mu needs A0 <= mu - R/4 (true for R >= 2) and A0 + R - 1 > mu + (R-1)/2 - 1 >= mu + R/4 (true for R >= 6): the lemma's "R >= 32" is more than enough.
- Tail: integers within R/4 of mu lie in I, so W outside I forces |W - mu| > R/4; Hoeffding gives 2 exp(-2 (R/4)^2/Q) = 2 exp(-R^2/(8Q)); R^2 >= (beta+3)^2 lambda and Q <= lambda/(128 nu) give R^2/(8Q) >= 16 (beta+3)^2 nu; 2 e^{-16(beta+3)^2 nu} <= 2^{-(beta+2) nu} (since 16 (beta+3)^2 >= 256 and 1/ln 2 slack); 2^{nu} >= lambda gives <= lambda^{-(beta+2)}; b <= lambda^beta and r^2 <= lambda give <= 1/(b r^2 lambda) = eps. (4.8) with eps = tau/(rb) = 1/(b r^2 lambda). tau <= 1/2 once r >= 2.
- (4.18): R/Q ~ 128 (beta+3) nu/sqrt(lambda), log2(2Q/R) = O(nu) (about nu/2 asymptotically), tau log2(2D+1) <= (1 + lambda/128)/(r lambda) = O(1/r), and 1/r <= 2 nu^2/sqrt(lambda) once r is large: the sum is O_beta(nu^2/sqrt(lambda)), dominated by the first term, ~ 64 (beta+3) nu^2/sqrt(lambda).
- Computation: the algorithm checks all hypotheses in poly(log n) bit operations (r from a square-root search, Q by division, R from an integer sqrt, the interval endpoints rationally, the tail probability bound on integers).

## Numerics
- **All hypotheses hold from an explicit lambda_0(beta) on:** at lambda = lambda_0 and in 20,000 samples above it, every check (r >= 2, R >= 32, 6R <= Q, Q > R, D <= 2^{lambda/128}, 2(b+w) D^2 <= n and 2 Q r^2 <= n at the worst case n = 2^{lambda-1}+1, I within {0..Q}, I contains all integers within R/4 of mu, Q/4 <= mu <= Q/2, the whole Hoeffding chain, tau <= 1/2) holds with 0 failures:

| beta | lambda_0 | n >= | r | Q | R |
|---|---|---|---|---|---|
| 1 | 1.09e10 | 2^(1.09e10) | 90 | 2.5e6 | 4.2e5 |
| 2 | 1.81e10 | 2^(1.81e10) | 109 | 4.0e6 | 6.7e5 |
| 3 | 2.60e10 | 2^(2.60e10) | 131 | 5.8e6 | 9.7e5 |
| 4 | 3.75e10 | 2^(3.75e10) | 149 | 8.1e6 | 1.35e6 |
| 5 | 4.89e10 | 2^(4.89e10) | 170 | 1.06e7 | 1.77e6 |
| 6 | 6.19e10 | 2^(6.19e10) | 192 | 1.34e7 | 2.24e6 |
| 8 | 9.77e10 | 2^(9.77e10) | 228 | 2.06e7 | 3.44e6 |
| 10 | 1.44e11 | 2^(1.44e11) | 262 | 2.96e7 | 4.93e6 |
- **Which condition binds:** at beta = 6, r >= 2 first holds near lambda = 6.4e5; Q > R from about 1.2e9 (r >= 2 and the construction not failing: the algorithm's "if r < 2 or Q <= R report failure" stage); at that point every other inequality already holds except 6R <= Q and I within {0..Q} (the latter depends on R <= Q/6); 6R <= Q is the last to hold, at lambda ~ 6.1e10. Thresholds scale roughly linearly in (beta+3)^2 nu^2 (6R <= Q is equivalent to sqrt(lambda) >= 768 nu (beta+3) up to floors).
- **(4.18) ratio** LHS / (nu^2/sqrt(lambda)): beta = 1: 54, 86, 107, 137, 164, 199, 222, 231 at lambda = 1e10, 1e12, 1e14, 1e18, 1e24, 1e40, 1e70, 1e100; beta = 3: 67 -> 345; beta = 6: 81 -> 515. Bounded and slowly approaching the hand asymptote 64 (beta+3) + 1 = 257, 385, 577 (about 90% of it at lambda = 1e100; the difference is the O(1) shift in log2(2Q/R) = nu/2 - log2(128 (beta+3)/2)).

## Prereg scoring
| id | result | note |
|---|---|---|
| P-1 | Held | all steps re-derive, including the weaker-than-stated needs (R >= 6 for interval containment). |
| P-2 | Held | lambda_0 dominated by 6R <= Q: 1.1e10 (beta 1) to 1.4e11 (beta 10); r >= 2 at 6.4e5, Q > R at ~1.2e9 (beta 6). (I had predicted r >= 2 near 5e5 and the balance inequalities in the hundreds; the balance inequalities hold as soon as the parameter set exists, at ~1e9, because Q > R fails earlier.) |
| P-3 | Held | bounded; approaches 64 (beta+3) + 1 from below. |
| P-4 | Held | "finitely many n fail" = n < 2^{1.1e10..1.4e11}; exhaustive search on those is infeasible as an algorithm but legitimate in an asymptotic theorem. |
| P-5 | Held | no gap. |

## Reading
1. Lemma 4.8 is correct as written. The one-line "for sufficiently large n" has an explicit, finite threshold of order 10^10-10^11 in lambda (so n of order 2^{10^10}+), set almost entirely by the requirement 6R <= Q that makes the Hermite interval fit inside {0..Q}.
2. This matches the independent regime boundaries found in the cost models (the 6R <= Q regime began at lambda ~ 1.2e10 in the Section 6 model and the first valid parameter sets near 1.5e9), and tightens the statement: the algorithm of Theorem 1.1 is not even well-defined (its fallback is exhaustive search) below about 2^{10^10}.
3. With Lemmas 4.5, 4.6, 5.2, Appendix A, B, Sections 6.1-6.2, D.3-D.5 and D.4.5-D.4.7 checked piecewise, the remaining open items in the ETH thread are the precision bookkeeping (D.11), the global induction in Appendix D, and, above all, independent review of the whole.

## Not established
That the thresholds are the minimal "sufficiently large" in the paper's sense (they are the minimal ones for the checks I implemented, with b = w = lambda^beta as the worst case); the full theorem.
