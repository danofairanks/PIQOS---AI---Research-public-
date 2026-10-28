# Results: Lemmas 4.4-4.5 of the ETH preprint (variable and factor group schedules)
Scored against eth_lemma45_check/PREREG.md (d76ca73). Read: Section 4.4 (the label/copy requirement, Lemma 4.5 with proof) and Remark 4.4 (a worked Q=R=2 example), as the only content between Lemma 4.3 and 4.5. (Lemma 4.4 in the user's request is the numbered Remark 4.4 in the extraction; there is no separate "Lemma 4.4".) Code `lemma45_check.py`, raw `lemma45_results.json`, `lemma45_boundary.json`. Executed: floating-point conditional expectations over exact discrete structures; counts are integers.

## What Lemma 4.5 claims and how it argues
- Hypotheses (4.13): 2(b+w) D^2 <= M and 2 Q r^2 <= n, D = r^{2Q}, with n <= M <= bn, scopes of size <= w, each variable in <= b scopes. Conclusion: schedules a_v, d_f in [r]^Q chosen deterministically (poly time) with (i) every label (a_v, d_f) occurring at most 2M/D times, (ii) every group {v : a_v(t) = g} of size at most 2n/r.
- Proof: random uniform a_v, d_f. Phi = sum_u (c_u - M/D)^2 has E[Phi] <= M(b+w) (pairs of incidences are independent unless they share a factor or a variable; at most b+w such partners each, equality probability 1/D otherwise). Xi = sum_{t,g} (n_{t,g} - n/r)^2 has E[Xi] = Qn(1-1/r) <= Qn. Fixing choices one at a time to not increase E[Phi/(M(b+w)) + Xi/(Qn)] keeps it <= 2; hence Phi <= 2M(b+w), Xi <= 2Qn, so c_u <= M/D + sqrt(2M(b+w)) and n_{t,g} <= n/r + sqrt(2Qn); (4.13) makes both square roots at most M/D and n/r. Conditional probabilities of each indicator depend on <= 4 independent choices, so exact enumeration costs D^2 per indicator, polynomial overall.
- Consistency with Section 2.7: for b = w = 3, (4.13) reads 12 D^2 <= M, 2 Q r^2 <= n, exactly (2.17).

## Re-derivation (by reading)
E[Phi] = (dependent pairs)(1 - 1/D) - ... <= M(b+w): ordered pairs total M^2; independent pairs contribute 1/D each; dependent pairs (<= M(b+w), including the diagonal) contribute <= 1, giving E[Phi] <= M(b+w)(1 - 1/D) + 0 = <= M(b+w). E[Xi] = Qn + Q n(n-1)/r - Qn^2/r = Qn(1 - 1/r). Both check. The two square-root inequalities are equivalent to the stated hypotheses: sqrt(2M(b+w)) <= M/D iff 2(b+w) D^2 <= M; sqrt(2Qn) <= n/r iff 2 Q r^2 <= n. No arithmetic gap found.

## Checks run (implementation of the stated conditional-expectation derandomization, exact conditional probabilities)
- 12 instances: three hypergraph families (random scopes of width <= 3 with b = 3; "clustered" = identical scopes repeated b times, maximal dependence; "star" = three random disjoint-triple partitions), (r,Q) in {(2,1),(2,2),(3,1)}, n from 200 to 1,500, M up to 4,500, including boundary cases n = 1,026 (M = 3,078 against the threshold 2(b+w)D^2 = 3,072) and two instances that violate the first inequality of (4.13) (n = 300, M = 900 < 3,072).
- Exact initial potential Psi_0 = Phi/(M(b+w)) + Xi/(Qn) in expectation: 0.76-0.96 (bound used: <= 2). Final realized Psi: 0.0000-0.0022 (<= 2 in all 12).
- Realized maxima: label count 57..282 vs bound 2M/D = 112..562 (deviation from M/D at most 0.7%); group size at most n/r + 1 vs bound 2n/r. All 12 satisfy both conclusions; the two instances violating (4.13) satisfy them too (the hypotheses are sufficient, not necessary).

## Prereg scoring
| id | result | note |
|---|---|---|
| L4-1 | Held | statement as predicted; "df(t)=1 for empty scope" detail not predicted. |
| L4-2 | Held | second-moment on pairwise-dependent incidences; hypothesis (b+w)D^2 <= M is exactly the step from the sum of squares to the max deviation. |
| L4-3 | Held | same technique for groups with Q r^2 <= n. |
| L4-4 | Held | one combined potential with weights 1/(M(b+w)) and 1/(Qn); the constants of (2.17) and (4.13) agree for b = w = 3. |
| L4-5 | Held | schedules meeting both bounds on all 12 instances, with huge slack. |
| L4-6 | Held | no gap found. |

## Reading
1. Lemma 4.5 is correct as written, and the argument is a standard pessimistic-estimator derandomization; both the inequalities and the poly-time claim re-derive cleanly.
2. The proven bound is far from tight (realized deviations ~ 0.5%), so this step does not constrain the parameters beyond (4.13); in the paper's regime (4.13) holds with huge margin (D <= 2^{lambda/128} vs n = 2^lambda).
3. Remark 4.4's worked example (Q = R = 2, r = 2) was not re-run beyond what the earlier Section 2.7 implementation already covers (the construction passes with (r,Q,R) = (2,3,2),(2,3,3) etc.).
4. Remaining unchecked: 6.1-6.2 existence arguments (Tanner code, greedy selection), Appendix A's tree-size proof, Appendix D's D.3-D.5, Lemma 5.2's degree control beyond the tested congruence; the proofs of Lemmas 5.1's modulus-amplifying identity are numerically tested (Appendix B check) but the degree statements are read-only.

## Not established
Anything beyond the 12 tested instances for performance; the full proof of Theorem 1.1.
