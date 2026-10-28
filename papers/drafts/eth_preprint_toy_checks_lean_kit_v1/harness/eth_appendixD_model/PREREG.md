# Prereg: model of Appendix D (tensor contraction exponent) of the ETH preprint
Written 2026-10-28 before reading Appendix D (pp. 53-63; lines ~3000-3700 of the extraction). Known beforehand: intro says Theorem 1.1 has two bounds, 2^{O_k(n sqrt(loglog n)/sqrt(log n))} general and 2^{O_{k,D}(n/sqrt(log n))} for m <= Dn, both "proved by tensor contraction in Appendix D", versus rho(n) = n (loglog n)^2/sqrt(log n) from Section 6.4. Lemma/Theorem names seen in the extraction index: Theorem D.1 (Boolean tensor contraction), Lemma D.2 (counting sparse polynomial systems by contraction), D.3 (packing into packets), D.4, D.5 (tapered Hermite recovery); a line with r = 64, Delta = ceil(s^{9/10}).
Predictions.
- D-1: the improvement over Section 6.4's rho(n) is only in the loglog factors; the sqrt(log n) denominator is unchanged.
- D-2: Appendix D has its own parameter chain with explicit constants (e.g. r = 64); the per-n exponent as a function of lambda can be modeled from them.
- D-3: with the appendix's constants the crossover (first lambda with total exponent < 1) is NOT earlier than the Section 6 model's (lambda* ~ 1e13 for k=2); i.e. the sharper exponent does not translate into a practically earlier regime.
- D-4: the model still gives a crossover (exponent -> 0), at lambda > 1e9, so galactic.
- D-5: the appendix's own statements are internally consistent at the level of exponents (no mismatch between Theorem D.1 and the 'sharper bound' in Theorem 1.1).
- D-6: Appendix D needs a different sparsification parameter than s = sqrt(lambda)/nu^2 (the sqrt(loglog n) vs (loglog n)^2 difference must come from somewhere).
Method: read the appendix, extract each parameter/inequality, model as before (entropy level, per-n exponent in lambda), log deviations. If the construction's constants cannot be read from the text, that is a stated gap.
