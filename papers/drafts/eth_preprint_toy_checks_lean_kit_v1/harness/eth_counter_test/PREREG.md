# Prereg: implement the ETH preprint's Section 2 counter and test it
Written 2026-10-28 before implementing; before reading Sections 2.5-2.9 and Section 4 (only 1-2.4 read so far, see RESULTS_eth_paper.md). Source of truth is the paper (openai/math 7ef5c0cc5, preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf, sha256 recorded at implementation).

What a test at n <= ~25 can and cannot show.
- CAN: that the algebraic identities and the decoupling-by-measurement claims in Section 2 are exactly correct on small instances (exact rational arithmetic, compared with brute force #F).
- CANNOT: the asymptotic claim 2^{n/sqrt(log n)}. The parameters (r groups, Q points, R degree, tau, D) need n far beyond brute-forceable for any asymptotic gain; at n <= 25 the construction's constants are expected to dominate. Passing small-n tests would NOT validate Theorem 1.1; failing them would be strong evidence against my implementation first, against the paper only after the discrepancy is isolated to a statement in the text.

Stages.
- A (generic forms): H(T) = sum_x prod_e Phi_e(<P_{e,v}(T),x>) with random polynomial rows satisfying P(0)=e_v. Check H(0)=#F, deg H <= M R, and that Taylor/Hermite interpolation from Q points with O(1+nR/Q) coefficients each recovers H(0) exactly.
- B (decoupled evaluation): for a (r,tau,D)-design, check the measurement-fixed evaluation equals brute-force H(t) (the paper's Section 2.4 / Prop 3.4 routine).
- C (the construction): build the Section 2.7 / Section 4 replacement forms (matrix M0, rank bound on I-M0, degree bound R) and run the whole counter end to end on bounded-occurrence 3-CNFs. Section 4 may be read as needed; each read is logged.

Predictions.
- C-1: Stage A identities hold exactly (they are elementary).
- C-2: Stage B holds exactly for any valid design.
- C-3: Stage C cannot be fully implemented from Section 2 alone; Section 4 detail is required. I expect to complete it only partially in this session.
- C-4: if Stage C completes, end-to-end counts equal brute force on 100% of random bounded-occurrence 3-CNFs for n <= 16.
- C-5: operation counts of the Stage C counter at n <= 25 exceed 2^n (no observable speedup at tested sizes).
- C-6: the first mismatch (if any) will be traced to my implementation, not the paper (prior: >= 70%).
Deviation rule: any change to a stage definition after seeing results is logged in DEVIATIONS.md with the reason.
