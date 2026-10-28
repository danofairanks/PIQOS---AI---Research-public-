# Results: Appendix D, D.4.5-D.4.7 (modes, child networks, time/space) of the ETH preprint
Scored against eth_modes_check/PREREG.md (cc745c4). Read: D.4.5 (page 62 rendered to confirm (D.12)-(D.15)), D.4.6, D.4.7. Re-derived each step by hand, then ran `modes_check.py` (raw `modes_AB.json`, `modes_C.json`, `modes_D.json`, `modes_D_a3.json`, logs). All numerics are exact (Fractions, integers).

## What the section claims (as read) and my re-derivation
- **Locality at t:** W_xy(t) = 0 unless y - x = t; adding an integer of valuation i flips bit i, so surviving pairs have different i-th bits; in a packet whose symbols differ in coordinate i, row slot x and column slot y are in different groups exactly when their i-th bits are equal. For such crossing pairs, with y = y0 + 2^{i+1} j: v2(t - y0 + x) <= i (else y0 = x + 2^i mod 2^{i+1}, contradicting equal i-th bits).
- **(D.12):** since 1/(T-y+x) = (1/(T-y0+x)) sum_b (2^{i+1} j/(T-y0+x))^b with ratio valuation >= 1, W_xy(T) = sum_b [C(T)/(C'(0)(T-y0+x))] (2^{i+1}/(T-y0+x))^b j^b, truncated at b+1 < p_t; the first fraction has valuation >= a+1-i >= 1 (Lemma D.4), so omitted terms (b >= p_t - 1) have valuation >= p_t.
- **Modes:** per (packet, tile y0, b) a variable Z of weight w = b+1 with L_Z(X) = sum_{y in tile} j^b X_y (0^0 = 1); the b-th term has valuation >= (a+1-i) + b >= b+1 = w, giving divisibility of every mode-monomial coefficient by 2^{sum w beta}, so only tuples with sum w beta < p_t matter. At most (3M/L) 2^{i+1} = 6M/D_t variables of each weight (packets <= 3M/L, 2^{i+1} tiles each).
- **Counting (D.15):** #{beta : sum w_Z beta_Z < p} <= e^{theta p} prod_Z (1 - e^{-theta w_Z})^{-1} <= exp(theta p + (6M/D) sum_{j>=1} -ln(1-e^{-theta j})); sum_j -ln(1-e^{-theta j}) = sum_h 1/(h (e^{theta h} - 1)) <= (1/theta) sum 1/h^2 = pi^2/(6 theta); with theta = sqrt(M/(D p)) the exponent is <= (1 + pi^2) sqrt(M p/D). Combined with p_t = O(M D_t/u) from (D.11) this is exp(O(M/sqrt u)).
- **D.4.6 identity (D.16):** for fixed beta, the product over row ports of l_{Y_x}(local + targeted modes) is expanded in the mode variables; each mode has one target group (extraction of its exponent) and one source group (substitution of L_Z(X)^{beta_Z}, which involves only source-group column bits), so the sum over (X,Y) factors over groups: F(t + alpha zeta) = sum_beta prod_g Z_{g,beta} (mod 2^{p_t}). Child g keeps the group-g vertices and ports and adds one packet vertex per packet joined to every retained port; its edges number <= 6M/r = 3M/32 < M/8 (row ports of symbol g <= 3M/r plus column ports <= 3M/r); old degrees unchanged; a packet vertex has <= 2L <= Delta ports.
- **D.4.7:** children of a depth-d call: s^{O(1)} exp(O((s/sqrt(lambda))(sqrt 2/8)^d)) from M <= C s 8^{-d}, u_d = Theta(lambda/2^d): M/sqrt(u_d) ~ C s 2^{-5d/2}/sqrt(eps lambda), and 2^{d/2}/8^d = (sqrt 2/8)^d = 2^{-5d/2}; summing exponents over O(log lambda) depths is geometric; polynomial factors s^{O(1)} per level give exp(O(lambda log lambda)); leaves 2^H poly; space polynomial (depth-first, O(log lambda) stack). All steps close.

## Numerics
- **A (valuation claim, all crossing pairs, a = 1..5, every t in S\{0} with v2(t) < a):** 36,084 crossing (x,y) pairs including the diagonal x = y, 108,252 evaluations at random T = t + alpha zeta; v2(t - y0 + x) <= i in every case (0 violations).
- **B (geometric expansion):** truncated (D.12) equals the exact W_xy(t + alpha zeta) modulo 2^p for p in {1, 2, 5, 9, 14} in every evaluation (0 violations); every kept term has valuation >= b+1 (0 violations, b = 0..5).
- **C (counting bound):** exact DP counts of tuples with sum w beta < p for N = 6M/D in {1,2,6,12,60,600} variables per weight and p in {2,...,300} (42 cases): ln(count) <= theta p + N sum_j -ln(1-e^{-theta j}) <= (1 + pi^2) sqrt(N p/6) in all 42; the bound is loose by a factor of 2-20 in the exponent at these sizes.
- **D (identity (D.16) on a small packet network):** one packet, L = 4 (a = 2) and L = 8 (a = 3), r = 2, row/column vertex tensors with random integer entries, every t in S\{0} with i = v2(t) < a, random zeta, working precision p = 3 and p = 5 (a = 2), p = 3 (a = 3): the direct sum F(t + alpha zeta) = sum_{X,Y} A(Y) B(X) prod_x l_{Y_x}((W X)_x) equals sum_beta prod_g Z_{g,beta} modulo 2^p in 48 + 48 + 14 = 110 of 110 node-trials (0 failures), with child networks built exactly as in D.4.6 (group-g rows/columns, extracted targeted-mode coefficient, source-mode power). The cases cover groupings by coordinate i = 0, 1 (and 2 at a = 3).

## Prereg scoring
| id | result | note |
|---|---|---|
| DM-1 | Held | 0 violations over 36,084 crossing pairs, diagonal included. |
| DM-2 | Held | expansion and term valuations. |
| DM-3 | Held | 42/42; also within the simplified (1+pi^2) sqrt(Mp/D) form. |
| DM-4 | Held | 110/110. |
| DM-5 | Held | 6M/r = 3M/32 < M/8 for r = 64; degree 2L; ratio 2^{-5/2} = sqrt2/8. |
| DM-6 | Held | no gap; the three subtle points resolve: diagonal entries are crossing pairs (equal i-th bits) and are expanded like the rest; modes with weight >= p_t are dropped legitimately; j = 0 gives Z with b = 0 only (0^0 = 1, 0^b = 0 for b >= 1). |

## Reading
1. D.4.5-D.4.7 are correct as written for everything I could test; every claimed inequality re-derives and the structural identity (D.16) holds exactly at small size.
2. This removes the mode counting and child-network construction from the unchecked list; combined with D.3-D.5 the contraction theorem's proof is now checked piecewise except the precision bookkeeping (D.11) and canonical lifting across recursion, and the overall induction.
3. Constant factors: the counting step contributes the explicit (1 + pi^2) sqrt(M p_t/D) bound (vs my cost model's tighter 2 pi sqrt(M p_t/D)); the cost model's crossovers (lambda ~ 6e15..8e16 general density) used the tighter optimized-theta form, so using the paper's own theta would raise the per-level constant by a factor (1+pi^2)/(2 pi) = 1.73 and the crossover lambda by about 3.

## Not established
(D.11) precision accounting with its O_C constants; canonical lifting across recursion levels; multi-packet networks (one packet tested; packets are block-diagonal in W so the extension is by linearity but not run); tested sizes are tiny (L <= 8, p <= 5).
