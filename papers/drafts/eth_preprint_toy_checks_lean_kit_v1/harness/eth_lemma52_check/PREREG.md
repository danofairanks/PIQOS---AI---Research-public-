# Prereg: Lemma 5.2's degree control (ETH preprint, Section 5.2-5.3)
Written 2026-10-28 before the dedicated re-derivation and numerics (the congruence half of Lemma 5.2 was tested in the Appendix B check; the degree half was only read). Claim: for integers y_1..y_m, S_l( prod_i B_i(V) mod V^l ) = prod 1{2|y_i} mod 2^l, where B_i(V) = sum_{j<l} e_j(y_i) h(y_i)^j V^j, h(Y) = Y(Y-1), deg e_j <= 1; and for y_i polynomials over Q of total degree <= d*, each retained V^s coefficient (and their sum) has total input degree <= d*(m + 2(l-1)). Consequence (5.5): deg_T H <= d_H = k R (m_test + 2(l-1)) after substituting replacement forms of T-degree <= R-1 into inputs of degree <= d = k(m_test + 2(l-1)).
Predictions:
- LD-1: the proof is correct as written: a term of V-weight s = sum j_i <= l-1 has degree <= sum d*(1 + 2 j_i) = d*(m + 2s) <= d*(m + 2(l-1)).
- LD-2: numerics with explicit multivariate polynomials y_i (3 variables, d* in {1,2}, m in 1..4, l in 1..5, 100+ random draws): the coefficient of V^s has total degree <= d*(m+2s) in every draw; the bound d*(m+2s) is attained (generic y_i) for the leading s.
- LD-3: truncation is necessary: the untruncated product has degree up to d* m (2l-1) which exceeds d*(m + 2(l-1)) for m >= 2, l >= 2; the retained (truncated) product's degree matches the lemma, so any pipeline that skips truncation would violate the linear degree budget of (3.2).
- LD-4: the worked example p_2(Y) = 1 - 3Y^2 + 2Y^3 = (1-Y) + (2Y-1) h(Y) holds, and its two-equation retained terms have degree <= 4 = d*(m + 2(l-1)) at d* = 1, m = 2, l = 2.
- LD-5: after substituting replacement forms of T-degree <= R-1 for each input variable, the T-degree of the truncated product is <= d* (R-1) (m + 2 (l-1)) <= d* R (m + 2(l-1)) (so (5.5) holds with k = d*).
- LD-6: no gap found.
Method: re-derive; implement multivariate polynomial arithmetic with exact Fractions/integers; run; record maxima against bounds.
