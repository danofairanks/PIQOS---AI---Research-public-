# Results: Appendix A (disjoint sparsification, tree-size proof) of the ETH preprint
Scored against eth_appendixA_check/PREREG.md (9ce7cf7). Read: A.1 (branching rule), Lemma A.1, A.2 (Lemmas A.2, A.3), A.3 (tree size) in full; re-derived every step; implemented the branching algorithm and ran it (`appendixA_check.py`, raw `appendixA_results.json`). Executed numerics are exact (integer sets, brute-force satisfiability over all 2^n assignments).

## What Appendix A claims
- Rule (A.1): choose the smallest width c, then the largest |H|, with H a nonempty proper subset of a width-c clause with deg_c(H) >= theta_{c-|H|} = M^{c-|H|}. Children F_A = G ^ H, F_B = G ^ (and_a P_a) ^ (and_{l in H} not-l), where H u P_a are the width-c clauses containing H; each child re-normalized to an antichain; no unit propagation.
- Lemma A.1: children partition the parent's satisfying assignments; every new clause (H; the distinct P_a, at least theta_j of them; new units) survives normalization; every removed old clause contains a new strict subset.
- Lemma A.2: at every node, for 1 <= i < j < k and every literal set S of size i, fewer than 2 theta_{j-i} marked width-j clauses present contain S.
- Lemma A.3: along any path T_j <= 4 (3M)^{j-1} n (T_j = width-j insertions); so depth <= Cn with C = 4 sum_{j<=k-2}(3M)^j and B-children <= Gamma n/M with Gamma = 2(3^{k-1} - 1).
- Tree size: nodes <= (Cn+1) sum_{a <= Gamma n/M} binom(Cn,a) <= (Cn+1)^2 2^{(Gamma n/M) log2(4CM)} for M >= Gamma; M = least power of two >= Gamma with Gamma h <= sigma M gives <= (Cn+1)^2 2^{sigma n}; leaves have each variable in <= B = 2 sum_{j<k} M^j <= 4 M^{k-1} clauses.

## Re-derivation by reading
- A.1: disjointness (some literal of H true vs all false); new clauses survive: H, P_a not supersets of old clauses (otherwise a strict subset of H u P_a is present, contradicting the antichain); distinct P_a of equal width are incomparable; P_a is disjoint from the variables of H so it contains no unit {not l}; old units already present are not counted.
- A.2: induction over branches that insert width-j clauses (selected width c > j). Child A: smallest-width priority means fewer than theta_{j-i} present width-j clauses contain S before insertion, +1 for H; Child B: those before (same bound) plus new petals P_a containing S; S inside P_a is disjoint from H, so H u S is a larger proper subset of the width-c clause H u P_a, and largest-|H| priority gives deg_c(H u S) < theta_{c-|H|-i} = theta_{j-i}; deletions cannot increase the count; total < 2 theta_{j-i}. The proof also needs j-i >= 1 so theta_{j-i} is defined, which i < j gives.
- A.3: L_j <= 4 n theta_{j-1} (sum of A.2 over the 2n single literals) and D_j <= 2 sum_i theta_{j-i} T_i (each deleted marked clause charged to a new strict subset, each such insertion charged < 2 theta_{j-i} times); T_j/(n M^{j-1}) <= 4 + 2 sum_{i<j} 4 * 3^{i-1} = 4 * 3^{j-1}; base T_1 <= 2n since units are never deleted and a literal is inserted as a unit once.
- Node count: a node is determined by its depth and the positions where its path chose B (the branching rule is deterministic); the number of such descriptions is (Cn+1) sum_{a <= Gamma n/M} binom(Cn,a); with a <= Gamma n/M <= n <= Cn/4 (needs M >= Gamma, C >= 4) one has binom(Cn,a) <= (4Cn/a)^a, increasing in a on that range, so the sum <= (Cn+1)(4CM/Gamma)^{Gamma n/M}.
- Leaf bound: no valid H at a leaf, so each literal lies in fewer than theta_{c-1} = M^{c-1} width-c clauses (c >= 2) and in at most one unit clause: per variable < 2 (1 + sum_{c=2}^{k} M^{c-1}) = B.

## Numerics
- 18 runs (nine (n,k,M,density) settings x two seeds; n = 9..12, k = 3 and 4, M in {2,3,4,16}; initial clause sets 322-1,293; trees of 23 to 8,647 nodes; none hit the 40,000-node cap): every run partitions exactly: each of the 2^n assignments satisfies exactly one leaf iff it satisfies the input (leaf counts sum to #F), 18/18.
- Insertions: T_j <= 4(3M)^{j-1} n in every node of every run (0 violations); observed maxima e.g. T_1 up to 22 (bound 2n = 24 at n = 12), T_2 up to 48 (bound 4*3*... = 4(3M)n >= 480 for M=4,n=12).
- Lemma A.2 invariant at every node (all marked width-j<k clauses, all literal subsets): 0 violations.
- Path depth <= Cn (max seen 84 vs C n >= 392), B-choices <= Gamma n/M (max 7 vs bound 8n for M=2): 0 violations.
- New clauses survive normalization in every branch: 0 failures.
- Leaf occurrence bound: max per-variable occurrence 3-255 vs B = 2 sum M^j (up to 546 at M = 16): 0 violations.
- Node counts are tiny against the bound (log2 nodes 4.5-13.1 vs log2 bound 186-1,754).
- Combinatorial inequality sum_{a <= floor(Gamma n/M)} binom(Cn,a) <= 2^{(Gamma n/M) log2(4CM)}: exact check for k in {3,4}, M in {16,32,64,128} with M >= Gamma, n = 1..200: 0 failures.

## Prereg scoring
| id | result | note |
|---|---|---|
| A-1 | Held | all of A.1-A.3 and the counting re-derive. |
| A-2 | Held | (i) partition exact 18/18; (ii) T_j bounds, (iii) A.2 invariant, (iv) depth and B-choices, (v) leaf occurrence: 0 violations. The tree-size bound itself applies only when M >= Gamma (M = 16 at k = 3 here); the lemmas A.1-A.3 were exercised at M in {2,3,4,16} since they hold for any M >= 2. |
| A-3 | Held | realized nodes are 100+ bits below the bound. |
| A-4 | Held | 0 failures for n <= 200. |
| A-5 | Held | (a) T_1 <= 2n observed (e.g. 20 <= 24); (b) contradictory unit pairs are legal in leaves, handled by counting (their satisfying set is empty); (c) per-literal at most one unit clause is used in the bound and all runs respect B. |

## Reading
1. Appendix A's proof is correct as written for what I can check: each lemma re-derives, the counting argument has no gap (including the M >= Gamma and C >= 4 side conditions), and an implementation of the algorithm confirms partition, insertion accounting, the marked-clause invariant, depth, and leaf occurrence on 18 runs.
2. The bounds are loose (insertion counts and node counts are orders of magnitude below), which is the safe direction and matches the earlier cost model: sigma n enters only through the sparsification term, already shown negligible near the crossover.
3. One item to keep in mind rather than a flaw: the bound's constants (C ~ 4(3M)^{k-2}, Gamma = 2(3^{k-1}-1)) enter only through h = ceil(log2(4CM)) and hence the least M with Gamma h <= sigma M, which the earlier models already included.
4. Appendix A is now off the unchecked list. Remaining: Appendix D's D.3-D.5 (packing, Cauchy deformation, tapered Hermite recovery), Lemma 5.2's degree control beyond its tested congruence, and Lemma 4.8's remaining claims.

## Not established
Instances beyond n <= 12; the paper's claim that M can be taken as Theta(sigma^{-1} log(2/sigma)) (exercised arithmetically in the earlier sparsification model, not by running trees at large n); correctness of the full theorem.
