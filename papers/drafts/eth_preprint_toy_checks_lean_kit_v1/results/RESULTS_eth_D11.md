# Results: Appendix D precision bookkeeping (D.11)
Scored against eth_D11_check/PREREG.md (388a64f). Read: (D.11) and its proof (page 61 area: "the input and child precisions satisfy p <= s lambda^{O(1)} 2^{a_{d-1}}, p_t = O_C(M D_t/u)"), the definitions (D.4) of u_d, a_d, L, D_arr, Lemma D.5's p_t = p + 8 h D_t + 8 M (a+1), and the canonical-lifting paragraph of D.4.1. Code `d11_check.py`, raw `d11_results.json`. The simulation is the exact worst-case recursion in the log2 domain, normalized by s (to avoid float absorption at huge lambda); at lambda >= 1e30 some outputs saturate (values printed as 0.0 / 1.00) and are not used.

## What (D.11) says and my re-derivation
- Root: P0 <= C s. A call at depth d with input precision p passes p_t = p + 8 h D_t + 8 M (a_d + 1) to the child for every node t with q_t > 0, where h = ceil(3M/u_d), D_t = L/2^{v2(t)} <= L = 2^{a_d}, M <= C s 8^{-d}, u_d = floor(eps lambda/2^d), a_d = 2 sum_{j<=d} u_j, a_{-1} = 0.
- Claim 1: p <= s lambda^{O(1)} 2^{a_{d-1}}. Re-derivation: each increment is <= 8 (4M/u) 2^{a_{d'}} + 8M(a_{d'}+1) <= 32 C s 2^{a_{d'}} + 8 C s (4 eps lambda + 1) at depth d' < d, with a_{d'} <= a_{d-1}; O(log lambda) increments: p <= C s + O(log lambda) * 32 C s 2^{a_{d-1}} * (1 + lower terms). So the "lambda^{O(1)}" is really C * O(log lambda).
- Claim 2: for a node with q_t > 0 (i = v2(t) < u), D_t >= 2^{a_d - u} = 2^{a_{d-1} + u} (since a_d = a_{d-1} + 2 u_d) hence p/(M D_t/u) <= (s lambda^{c} u)/(M 2^u) < lambda^{c + 1/2} u/2^u (using M > H = s/floor(sqrt lambda)), which is o(1) once 2^u beats lambda^{c+1/2} u; 8 h D_t = O(M D_t/u) directly (h <= 4M/u) and 8M(a+1) = O(M D_t/u) because D_t/u >= 2^{a_{d-1}+u}/u exceeds a+1. Hence p_t = O_C(M D_t/u) with constant 24 + o(1).
- All precisions are polynomial: a_d <= 4 eps lambda, so log2 p <= (1 + 4 eps) lambda + O(log lambda) bits (s^{1+4eps} lambda^c).

## Numerics (worst case: every depth uses M_d = C s 8^{-d} for feeding the recursion; the ratio test uses M just above H and i = u-1)
- **Claim 1 exponent** c = log_lambda max_d [p_d/(s 2^{a_{d-1}})]: C = 12: 0.154 (lambda = 1e7) -> 0.036 (1e30); C = 144: 0.308 (1e7) -> 0.072 (1e30); the value is just log_lambda(C) from the root (p_0 = C s) plus a decaying correction, i.e. a constant, as predicted by the re-derivation; precision bits / lambda = 1.0000 at every tested lambda (the 4 eps lambda excess is a few parts in 1e5).
- **Claim 2:** the quantity p_t/(M D_t/u) at the worst node tends to 24.00 (= 8 * 3) for every lambda >= 1e8 tested (C = 12 and 144); at lambda = 1e7 it is 48.7 (C = 12) and 320 (C = 144): the claim has not yet kicked in.
- **Where claim 2 starts holding at every depth** (log2 [p u/(H D_{t,min})] <= 0, i.e. the inherited precision is below the node's own term): lambda_1 = 2.94e7 (C = 12) and 6.71e7 (C = 144), with 0 failures in 5,000 samples above; at lambda = 1e8, C = 144: log2 rho = -3.0; at 1e10: about -590 and -1,184; super-exponentially decreasing beyond.
- **Literal reading of (D.5)** (u >= lambda^{4/5} at the last level) would require lambda >= 2^546 (C = 12) or 2^582 (C = 144): the statement of the lemma is not tight; what is needed is only 2^{u_min+1} >= C' (d+1) sqrt(lambda) u, which holds from lambda ~ 3e7-7e7.

## Prereg scoring
| id | result | note |
|---|---|---|
| PB-1 | Held | the "lambda^{O(1)}" is C * O(log lambda) in effect. |
| PB-2 | Held | exponent <= 0.31 at lambda >= 1e7. |
| PB-3 | **Falsified in range** | I predicted lambda_1 in 1e9-1e11; actual 2.9e7-6.7e7 (the binding requirement is weaker than I estimated because the inherited term at depth d is not the full s 2^{a_{d-1}} lambda^{c} but p_d/(s 2^{a_{d-1}}) ~ 24 C 8^{-(d-1)}/u_{d-1}, small). The qualitative point (far below the literal 2^546) held. |
| PB-4 | Held | bits <= (1 + 4 eps) lambda + O(log lambda). |
| PB-5 | Held | no gap; the text is loose in two places (lambda^{O(1)}; u >= lambda^{4/5}). |

## Reading
1. The precision bookkeeping (D.11) is correct as written, with a constant K = 24 + o(1) in p_t = K M D_t/u that the cost models (which used p_t ~ 24 M D_t/u) already assumed.
2. Its threshold (lambda ~ 3e7-7e7) is not binding: other requirements of Theorem D.1 and Lemma 4.8 start at ~1e10-1e11 (Lemma 4.8, 6R <= Q) and at the crossover scales (1e13-1e17) all of them hold.
3. The canonical-lifting remark (D.4.1) was read, not tested: it is a definitional device ensuring tensor entries evaluated at precision p_c keep their creation-time representatives.
4. What remains open in the ETH thread: the global induction of Theorem D.1 (correctness of the recursion as a whole, assembled from the pieces checked), the canonical-lifting argument, and independent review.

## Not established
Results for lambda between 1e30 and 1e300 (float saturation); the induction structure of Theorem D.1's proof; the full theorem.
