# Results: O10 counter-model search (scored against PREREG.md)
Run: `python3 -I o10_check.py 2000 1` (2,000 random networks per condition; rings U^3+U+1 and U^4+U+1 over Z, ell in {2, 3}, 4-6 edges, precisions p0 <= p1 <= p2 up to 14). Two independent implementations (explicit coefficient arithmetic; Kronecker-product matrices) disagreed on 0 of all computed contractions.

| condition | trials | applicable | failures | rate |
|---|---|---|---|---|
| O10a (lift of reduction mod 2^q, q >= p) | 2000 | 2000 | **0** | 0 |
| O10b (3-level monotone chain; kappa <= later precision) | 2000 | 2000 | **0** | 0; kappa violations 0 |
| M1 non-monotone (reduce below p) | 1661 | 1661 | 1653 | 99.5% |
| M2 mismatched lift convention (kappa < p) | 1661 | 1661 | 1305 | 78.6% |
| M3 truncate then re-expand | 1934 | 1934 | 1921 | 99.3% |
Schedule grid (preconditions from my reconstruction, M <= M_d): 5,058 points, 0 violations of pi_{d+1} >= pi_d or of p_t - p <= pi_{d+1} - pi_d.

## Scoring against the prereg
- P1: met (0/2000). P2: met (0/2000, no kappa violation). P4: met (0 violations after the grid precondition fix, DEVIATIONS 2).
- P3: partly missed. M1 and M3 exceed 80%; **M2 is 78.6%, below the 80% threshold**. The mutation still fails in 1305 of 1661 trials against 0 in 4000 for the clean conditions, so the test discriminates; the shortfall comes from trials where the changed coordinates cancel in the contraction mod 2^p (post hoc: rates 63-85% across p - kappa = 1..5 with no clear trend, not investigated further). No threshold was changed.
- P5: no counter-model found.

## What this establishes
O10 moves from "read only" to "tested on an abstract bookkeeping model": reducing an entry mod 2^q and re-lifting it canonically leaves the contraction unchanged mod 2^p whenever q >= p, and the monotone precision schedule of the lemma keeps creation precision below every later call's precision. This is the statement that A -> A/2^q is a ring homomorphism, so a pass was expected.
## What it does not establish
It does not test the identity (D.16), the valuation bounds (D.9, D.10), the mode expansion, or whether the paper's text defines packet-entry lifts the way I reconstructed them. Toy sizes (e <= 4, ell <= 3). Same model wrote the reconstruction and the test.

## Sources
Every figure above is produced by `o10_check.py` and the committed output `o10_results_N2000_s1.json`. The ring and precision definitions follow `../../INDUCTION_LEMMA.md` (a reconstruction of the preprint, Appendix D.4.1).
