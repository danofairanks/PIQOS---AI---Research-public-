# Prereg: cost model of the ETH preprint's Section 2 counter under its own parameters
Written 2026-10-28 before computing. Source: paper (sha256 5b1612dc...8123), eqs (2.10), (2.11), (2.12), (2.19) and Step 5 text as extracted by pdftotext (the extraction garbles some radicals; reading used: lambda = ceil(log2 n), nu = ceil(log2 lambda), r = floor(sqrt(lambda)/nu^2), Q = floor(lambda/(128 nu)), R = 4 ceil(sqrt(lambda)), tau = 1/(r lambda), D = r^{2Q}; the Q reading is cross-checked by the paper's own line "R^2/(8Q) >= 256 nu").
Model: log2(cost)/n = e1 + e2 + e3, with
- e1 = exponent of sum_{j<=q} C(n,j) 2^j with q = floor(3nR/Q), delta = 3R/Q: H2(delta)+delta if delta <= 2/3, else log2(3) (all subsets);
- e2 = 2 tau log2(2D+1);  e3 = 2/r  (group term 2^{2n/r}).
All terms depend on n only through lambda (n ~ 2^lambda).  A parameter set is VALID only if r >= 2 and Q >= 1.
Predictions.
- M-1: e1+e2+e3 > 1 (cost above 2^n) for every valid lambda up to a crossover lambda* with 1e9 <= lambda* <= 1e13 (n ~ 2^lambda*).
- M-2: the model total tends to 0 as lambda -> infinity, and total / ((log lambda)^2 / sqrt(lambda)) stays bounded (consistent with the stated rate (2.12)).
- M-3: valid parameters first exist at lambda of order 1e5 to 1e6 (r >= 2 needs sqrt(lambda) >= 2 nu^2), i.e. n >= 2^(1e5..1e6): no n below that gets a non-degenerate instance of the construction.
- M-4: near the crossover the dominant term is e1 (Taylor data), not e2 or e3.
- M-5: no internal inconsistency: the claim "6R <= Q for sufficiently large n" and "q <= n/2" is satisfied exactly when sqrt(lambda) >= 3072 nu; at that point total is still > 1.
- M-6: the model does not show cost < 2^n for any n a computer can represent explicitly (n < 2^64).
Deviation rule: changes to the model after seeing numbers are logged in DEVIATIONS.md.
