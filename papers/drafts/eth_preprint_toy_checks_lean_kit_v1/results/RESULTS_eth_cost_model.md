# Results: cost model of the ETH preprint's counter under its own parameters
Scored against eth_cost_model/PREREG.md (0a5ac47). Script `eth_cost_model/cost_model.py`, raw `cost_model_results.json`, deviations N-1..N-5. Arithmetic on the paper's stated bounds only; the algorithm was not run (that was the previous test, at n <= 9).

Model (per-n log2 cost): e1 (Taylor data, sum_{j<=q} C(n,j) 2^j with q = floor(3nR/Q)) + e2 (measurement tuples (2D+1)^{2 tau n}) + e3 (group assignments 2^{2n/r}). Parameters (2.19): lambda = ceil(log2 n), nu = ceil(log2 lambda), r = floor(sqrt(lambda)/nu^2), Q = floor(lambda/(128 nu)), R = 4 ceil(sqrt(lambda)), tau = 1/(r lambda), D = r^{2Q}.

## Numbers
- First lambda with a valid parameter set (r >= 2, Q >= 1): **521,284**, i.e. n ~ 2^521284 (about 157,000 decimal digits). There, total = 2.59 (cost 2^{2.59 n}, worse than brute force).
- The paper's own "6R <= Q" regime (needed for its step q <= n/2) starts at lambda = 1.23e10 (r=96, Q=2.8e6); total is still **1.49**.
- **Crossover where total < 1: lambda = 61,312,066,560** (r=191, Q=1.33e7, R=9.9e5, delta = 3R/Q = 0.223): n ~ 2^61,312,066,560, about 1.8e10 decimal digits. Total there = 0.99999997; e1 = 0.9895, e2 = 3e-5, e3 = 0.0105. No re-crossing in 20,000 sampled points above it.
- Beyond: total = 0.96 (lambda 7.3e10), 0.39 (1.07e12), 0.085 (5.9e13), 0.029 (8.6e14).
- Rate: total / ((log2 lambda)^2 / sqrt(lambda)) rises slowly from 5 (lambda 5e5) to ~346 (8.6e14) with shrinking increments; hand asymptote e1 ~ 768 (log2 lambda)^2 / sqrt(lambda) in this normalization, so it is bounded by a constant, consistent with (2.12) (and with 2^{O(n (log log n)^2 / sqrt(log n))}).

## Prereg scoring
| id | result | note |
|---|---|---|
| M-1 | Held | crossover 6.1e10 in [1e9, 1e13]. |
| M-2 | Held | total -> 0, ratio bounded (numeric scan + hand asymptote). |
| M-3 | Held | first valid lambda 5.2e5 in [1e5, 1e6]. |
| M-4 | Held | e1 dominates at the crossover (0.99 of 1.0). |
| M-5 | Held | "6R<=Q" regime begins at total 1.49 > 1; Step-5 tail inequality holds from the first valid lambda. |
| M-6 | Held | no n a machine can write down explicitly (< 2^64) is inside the model's saving regime; nor is any n below 2^521284 even a valid instance. |

## Reading
1. **The stated parameter chain is internally consistent: it does give subexponential cost, asymptotically.** The Taylor-data term is the binding constraint, with delta = 3R/Q = 1536 nu / sqrt(lambda) -> 0. Nothing in (2.10)-(2.19) fails at the level of exponents. This supports the claim's structure; it is not a verification of it.
2. **The claim is galactic.** The saving over 2^n begins at n ~ 2^(6.1e10) under these constants, and the saving there is a factor 2^(3e-8 n). For any n that exists physically the model's cost is above brute force. This is a property of the construction (not a flaw): asymptotic statements about 2^{o(n)} are legitimate without being practical. It does mean ETH's refutation, if right, is a statement about limits, with no effect on any solvable instance size, and that "OpenAI refutes ETH" in the press can be read at full strength only as an asymptotic claim.
3. **Consistency with the small-n test:** at n <= 9 the measured cost was 50-1200x brute force (RESULTS_eth_counter.md), matching the model's prediction that everything below the crossover costs more than 2^n.
4. **Limits.** Only Section 2.6's base case is modeled, with my reading of the garbled parameter line (N-1). The headline sparsification and contraction steps (Section 6, Appendix D) are not covered, so this checks the cost accounting of the core routine, not Theorem 1.1's full exponent. The proof's correctness (e.g. that the three costs really are the only ones, Lemma 4.x bounds on coefficient sizes, space) is untouched.

## Not established
Correctness of any lemma; the exponent in Theorem 1.1 as stated; behavior of the sparsification step; Appendix D.
