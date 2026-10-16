# PREREGISTRATION for toy_mutual_audit.py (written 2026-10-16 BEFORE the first run)
Setup (all constants fixed here): limit MAX = 100. Truth T(d): ALLOW iff d is finite and 0 < d <= MAX. Shared spec S (flawed): "ALLOW iff d <= MAX".
Verifier A implements S as `d <= MAX`. Verifier B implements S as `not (d > MAX)` (same spec, different expression). Verifier B2 is written from a second, independently flawed spec S2: `d >= 0 and d <= MAX`.
Joint verdict = ALLOW iff both verifiers ALLOW.
Referent distribution (operational mix, percent): typical in-range 66, above limit (MAX..100*MAX) 10, huge (1e12..1e15) 2, zero 2, negative 8, -inf 3, +inf 3, NaN 6. Spec-derived suite draws only from the classes the spec text talks about (typical, above-limit) plus the boundary values.
Seed 20261016; 20000 referent draws for rates; 500 repeated suites of 200 draws for detection probabilities.
Predictions (tolerances in parentheses; the script prints PASS/FAIL against exactly these):
P1 Spec-derived suite: A and B each pass 100% in every repetition (exact).
P2 Pair (A,B) on the referent distribution: joint false-allow 0.13 (+-0.02); disagreement rate 0.06 (+-0.01); every disagreement is a NaN input (exact).
P3 Pair (A,B2): joint false-allow 0.02 (+-0.01); disagreement rate 0.11 (+-0.015).
P4 Detection of the common-mode class (zero, negative, -inf) with n=20 referent draws: >= 0.90; with n=20 spec-derived draws: exactly 0.
P5 Mutant M1 (A additionally allows d >= 1e12): spec-derived suite detects it with probability 0 (exact); the joint verdict does not change (the conjunction masks it); disagreement-on-referent-draws (n=200) detects it with probability >= 0.95.
P6 Mutant M2 (A denies 0 < d < 1): spec-derived suite detects it with probability in [0.70, 0.95].
Reading rules: P1-P6 all hold -> the toy behaves as the paper's framework predicts. Any FAIL is reported, not tuned away. No parameter changes after the first run except bug fixes, which are logged.
