# Results: Appendix B (exact arithmetic, bit sizes) of the ETH preprint
Scored against eth_appendixB_check/PREREG.md (5f890db). Read: Appendix B (B.1-B.4) in full. Not read: Lemma 4.6 (the substitution-row coefficient bounds that B.4 and B_P cite). Code `appendixB_check.py`, raw `appendixB_results.json`. Executed checks are exact integer / rational arithmetic (E1 for what ran); the bit-length bounds themselves are the paper's, checked by reading plus the numerics below.

## What Appendix B claims (as read)
- B.1 (Lemma B.1): the coefficients a_j, b_j of e_j (Lemma 5.1's decomposition p_l = sum e_j h^j, h = Y^2 - Y) satisfy |a_j|,|b_j| <= 2^{C l^2}; proof: ||p_l||_1 <= 2^l binom(2l-1,l-1) <= 2^{3l}; each elimination in the monic divisions multiplies the norm by <= 3; O(l^2) eliminations.
- B.2: rows P_{f,v} have common denominator d_den = (R-1)! Q!; integer coefficients of d_den P are <= 2^{B_P} with B_P = O(Q log Q + log D); substituted inputs norm B0 = d_den + 3n(R+1)2^{B_P}(Q+1)^R; lifted factors have denominator Gamma = Delta^{2l-1} (Delta = d_den^k) and numerator norm B1 = l E_l (B+Delta+2)^{2l-1}, E_l = max||e_j||_1; a full contribution over denominator Omega = Gamma^{m_test} has norm <= 2^n B1^{m_test}; the accumulator over M* <= 3^n (2D+1)^c signed updates has norm <= M* 2^n B1^{m_test}. Group sums use measurement representatives x-bar_h with C_h x-bar_h = y_h, so no lambda coefficients are needed. Resulting bit length: log(M*+1) + n + m_test log B1 = poly; log Omega = k m_test (2l-1) log d_den = O(k (m_test l + 1) Q log(Q+2)). "Exponentially many iterations contribute only log(M*+1)" because contributions are added, not multiplied.
- B.3: Hermite interpolation matrix V (entries of O(M_H log(Q+2)) bits, M_H = QJ); H_s(0) = N_H/(Omega D_H) by Cramer; fraction-free (Bareiss) elimination, O(M_H^3) operations, intermediate integers with O(M_H(B_data + M_H log(Q+2) + log(M_H+1))) bits. Final count = least residue of sum_s H_s(0) mod 2^l.
- B.4: for the Section 2 base case, Lemma 4.6 plus polynomial-bit-length lambda coefficients give a common denominator delta^{3n} and polynomial bit cost.

## Checks run
- **T1 (Lemma 5.1/B.1), l = 1..40:** p_l = sum_j e_j h^j holds exactly (integer identity at 25 integer points per l) and p_l(y) = 1{2|y} mod 2^l for y in [-12,12], for every l. Coefficient size: max bit length of a_j, b_j grows linearly, about 1.9 l (l=37: 69 bits; l=40: 75 bits), and log2||p_l||_1 = 105 at l = 37 against the proven <= 3l = 111. So the paper's 2^{C l^2} is a valid but loose bound; the true coefficients are 2^{O(l)}. The "factor three per elimination" growth never appears: the maximum norm along the divisions stays within 1 bit of ||p_l||_1.
- **T2 (Lemma 5.2's modular claim):** 300 random trials (l <= 9, m_test <= 5, |y_i| <= 15): S_l( prod_i B_i(V) mod V^l ) = prod 1{2|y_i} (mod 2^l) in all 300; 0 failures.
- **T3 (denominators, B_P) on the Section 2.7 construction, exact rationals, (r,Q,R) in {(2,3,2),(2,3,3),(3,2,2),(2,4,3)}:** (R-1)! Q! * P_u(T) has integer coefficients for every row (0 non-integral coefficients); the entries of M0 are in fact integers at these sizes (max denominator 1); max |d_den P| coefficient is 6, 18, 2, 96 (log2 2.6, 4.2, 1.0, 6.6) against Q log2 Q + log2 D = 10.8, 10.8, 8.3, 16.0.

## Prereg scoring
| id | result | note |
|---|---|---|
| B-1 | Held | every stated bit-length is polynomial: largest are log B1 = O(l^2 + l log B) ~ n^2 and log Omega = O(k m_test l Q log Q) ~ n^2 Q log Q; M_H*B_data ~ poly via m_test log B1 ~ n^3. Nothing exponential. |
| B-2 | Held | exponentially large VALUES are handled by bounding minors/bit-lengths (Cramer + Bareiss), not magnitudes. |
| B-3 | Held, with a note | the bit length of e_j coefficients is O(l) in practice (measured ~1.9 l); the paper proves the weaker O(l^2), which still gives polynomial bit cost. |
| B-4 | Held | every bound is explicit and re-evaluable; I found no gap inside Appendix B. Two dependencies were not re-derived: Lemma 4.6 (B.4) and Definition 3.1's B_P. |
| B-5 | Held | denominators and coefficient bounds agree with the construction at the tested sizes. |
| B-6 | Held by inspection | C-rows have {0,+-1} entries on <= D coordinates so the row sum <= D; not separately computed. |

## Reading
1. Within Appendix B the bit-size argument is sound as written for what I could check: the central design point, over-one-denominator accumulation, is correct arithmetic (adding numerators), the per-term norms are bounded by explicit expressions, and Cramer + fraction-free elimination gives polynomial bit length. The two numerical claims that are pure statements about integers (Lemma 5.1's identity and congruence, Lemma 5.2's truncated-product congruence) pass.
2. This closes one of the three named unchecked items (Appendix B). It does not close the lemma proofs themselves (Lemma 4.x, Tanner/greedy, Appendix D's D.3-D.5), nor Lemma 4.6.
3. The paper's polynomial bit-length bounds are loose by large factors (l^2 vs l; n^3 total), which is the safe direction for a correctness argument; they do not affect the exponent-level cost models.

## Not established
Lemma 4.6; B_P as a general statement for all parameters (tested at four small parameter sets); the Bareiss/minor bounds beyond reading; anything about the algorithm's actual bit costs at n beyond the tested sizes.
