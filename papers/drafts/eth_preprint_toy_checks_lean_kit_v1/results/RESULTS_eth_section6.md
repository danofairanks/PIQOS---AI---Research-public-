# Results: Sections 6.1-6.2 existence arguments of the ETH preprint
Scored against eth_section6_check/PREREG.md (64e2a3d). Read: Lemma 6.1 with its proof (Tanner-code parity checks on a Cayley bipartite graph), Lemma 6.2 with its proof (greedy row selection by averaging over (2m)^P lists), and the introductory paragraphs of 6.1-6.2. Re-derived every inequality by hand, then ran `section6_check.py` (raw `section6_results.json`). The Tanner code itself is not instantiated at the paper's parameters (D0 >= 3.2e5): only its arithmetic is.

## Lemma 6.1 (as read, with my re-derivation)
- Claim: from m <= Bn, mu = floor(log2 m)+1, P = 20000 B^2 mu^2, D0 = 320000 B^2 mu^3: a deterministic A(0) with m columns, <= 3n rows, row weight <= D0, such that every nonzero z with A(0) z = 0 has |supp z| >= m/P.
- Construction: d_G = min(m, D0), q_G = least power of two with q_G d_G >= m (so m <= q_G d_G < 2m); bipartite Cayley graph on F_2^{l_G} with d_G ports and shifts s_j chosen eps-biased (eps = 1/(200 B mu)); local code A_loc (c_G rows, d_G columns, kernel distance >= delta d_G, delta = 1/(100 B mu), c_G = floor(d_G/(8B))); Tanner code on edge coordinates; shorten to m coordinates.
- Re-derived: (i) union bound 2 q_G exp(-eps^2 d_G/2) with d_G = D0 gives exponent 4 mu exactly (eps^2 D0/2 = 4 mu), and 2 q_G < 2^{mu+2}, so the failure probability is <= 2^{mu+2} e^{-4mu} < 1; (ii) a random A_loc has a fixed nonzero word in its kernel w.p. 2^{-c_G}; the number of words of weight < delta d_G is <= (2 d_G)^{2h} < 2^{d_G/(25B)} (uses log2(2 d_G) <= mu+1 <= 2 mu and h < d_G/(100 B mu)), against c_G >= d_G/(8B); (iii) eigenvalues of the bipartite Cayley adjacency are sum_j (-1)^{b.s_j}, so (6.2) gives the mixing bound (6.3); (iv) nonzero accepted word: every touched vertex carries a nonzero local word (weight >= delta d_G), so h' >= delta d_G max(|U|,|V|) >= delta d_G sqrt(|U||V|); combined with h' <= e(U,V) <= d_G|U||V|/q_G + eps d_G sqrt(|U||V|) this gives sqrt(|U||V|) >= (delta - eps) q_G and h' >= delta(delta - eps) q_G d_G = q_G d_G/P >= m/P (delta - eps = 1/(200 B mu), product 1/(20000 B^2 mu^2) = 1/P exactly); (v) rows: q_G = 1: 2 c_G <= m/(4B)+2 <= n/4+2 <= 3n; q_G > 1: d_G = D0 >= 8B so 2 q_G c_G <= q_G d_G/(4B) + 2 q_G <= q_G d_G/(2B) < m/B <= n. Shortening preserves the property (zero-fill) and does not raise row weight above d_G <= D0.

## Lemma 6.2 (as read, with my re-derivation)
- Claim: from A(0), appending 3n rows chosen greedily (each from lists gamma in ([m] x {0,1})^P, minimizing N(A;h_gamma) = #F + D(A;h_gamma)) leaves D(A) = 0 after 3n rounds, using <= 3n (2m)^P common-zero counts; systems have <= 6n equations, each with <= 2^k max(D0,P) monomials.
- Re-derived: for a nonsatisfying x still passing, A(0) z = 0 on its violation vector so |supp v(x)| >= m/P; each list entry hits the support w.p. >= 1/P, so no hit w.p. <= (1-1/P)^P <= 1/e; given a hit, c_j uniform makes h.v uniform (also with repeated indices, since h.v = sum_j c_j v_{e_j}); so each such x is rejected w.p. >= (1-1/e)/2 = 0.316 >= 1/4; hence E[D(A;h_gamma)] <= (3/4) D(A), the minimizing candidate does at least as well, and after 3n rounds D <= (3/4)^{3n} 2^n = (27/32)^n < 1, an integer, so 0. Every satisfying assignment passes every row (parity of violation bits is 0), so N(A) = #F + D(A) throughout.

## Checks run
- **A (arithmetic of Lemma 6.1):** 635 parameter cases (B in {1,2,5,20,100}; mu = 1..60 and 80, 120, 200, 400; m at both ends of [2^{mu-1}, 2^mu - 1]); 241 have q_G > 1, 394 have q_G = 1. All five inequality families hold in every case, 0 failures; delta(delta - eps) = 1/P holds exactly (Fractions); the union bound's margin is >= 134 nats; the local-code margin c_G - log2(#light words) >= 117 bits (exact binomial sums for d_G <= 3e5, entropy bound beyond); 2 q_G c_G <= 3n holds, and the stricter 2 q_G c_G <= n holds for q_G > 1 as the proof states.
- **B (Lemma 6.2 probability):** min over a grid of (P, m, s >= m/P) of (1/2)(1 - (1 - s/m)^P) is 0.3161 > 1/4.
- **C (exact greedy on tiny formulas):** 300 random 3-CNFs (n = 4..6, m = P = 4, empty A(0), all 4,096 lists enumerated): the average over lists of D(A;h_gamma)/D(A) never exceeds 0.658 <= 3/4; the greedy minimizer's ratio never exceeds 0.333; D reaches 0 in at most 3 rounds (bound 3n >= 12); 0 formulas left uncleared.
- **D (mixing inequality (6.3)):** a random 40-shift set on F_2^6 has measured bias eps = 0.4; 2,000 random (U,V) pairs: 0 violations of e(U,V) <= d|U||V|/q + eps d sqrt(|U||V|).

## Prereg scoring
| id | result | note |
|---|---|---|
| E-1 | Held | all five chains re-derive. |
| E-2 | Held | q_G = 1 and floor(d_G/(8B)) = 0 / h = 0 cases harmless: any nonzero word has weight >= 1 >= m/P when m < P, and the Tanner-distance step is not needed. |
| E-3 | Held | min slack 117 bits at the tested parameters (prediction: > 10 bits). |
| E-4 | Held | 0.316 exactly the (1 - 1/e)/2 limit. |
| E-5 | Held | per-round averages <= 0.658; cleared within 3 rounds. |
| E-6 | Held | no gap found; cost caveat recorded below. |

## Reading
1. Existence arguments in 6.1-6.2 are correct as written for everything I could check; the proofs are standard (expander mixing for a Cayley graph with an eps-biased generator set, random local code, pessimistic-estimator greedy), with explicit constants that close.
2. Cost caveat (not an error): the exhaustive searches (shifts: exp(O(d_G log m)); local matrices: 2^{c_G d_G}) are exp(poly(B, log m)) with d_G = D0 ~ 3.2e5 B^2 mu^3. This is "polynomial in log n" in the exponent only after the paper's absorption step (Section 6.3: any fixed power of log n is o(n (loglog n)^2/sqrt(log n))); at the crossover scales modeled earlier (lambda ~ 1e13, mu ~ 1e13) the searches are exp(1e13^{O(1)}), tiny against n = 2^{1e13} but not "polynomial time".
3. Together with Lemmas 4.5, 4.6, Appendix B, Lemma 5.2's congruence and the Section 2 counter, this removes the "existence of the parity-test system" from the unchecked list.

## Not established
That the search procedures are implemented as stated at the paper's parameters (not run: D0 >= 3.2e5 and exp-time searches); the tree-size proof (Appendix A) and Appendix D's D.3-D.5; the degree-control Lemma 5.2 beyond its tested congruence; correctness of the overall theorem.
