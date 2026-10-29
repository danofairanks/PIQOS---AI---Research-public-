# Results: negative controls (scored against PREREG.md)

**Draft; not peer reviewed; may be revised or withdrawn. Written by one AI model with an operator directing the work; no outside reviewer has checked the decoys, the probes or the Lean witnesses.** Limitations are stated in "What this shows" below and in the kit README section 2c.
Reproduce: `python3 -I run_controls.py 12`; `python3 -I run_sections_controls.py`; Lean files in `lean/`, Comparator logs in `logs/`. Decoy code is in `negative_controls/`, each file headed DECOY.

## D1 / D1b: brute-force decoy counters through the end-to-end checks (3 configs x 12 seeds = 36 cases, seeds 1000-1011)
| class | cases | correct on every correctness field | passes where the real counter passes | D4 flag (known-primitive rule) | Counter.Z calls (mean) | self-reported assign_evals (first case) |
|---|---|---|---|---|---|---|
| real | 36 | 36 | n/a | 0 | 216 | 1344 |
| D1 (calls brute_H from taylor_decoupled) | 36 | 36 | 36/36 | **36/36** | 0 | 6 |
| D1b (inlined enumeration) | 36 | 36 | 36/36 | **0/36** | 0 | 6 |
| D1c (post hoc: D1b plus one cosmetic Z call) | 36 | 36 | 36/36 | 0/36 | 1 | 6 |
Correctness fields: H(0)==#F, degree bound, Hermite recovery from brute data, decoupled-equals-brute Taylor data (true by construction for the decoys), recovered count equals truth, design violations == 0.
Sections 3-5 path (`controls_sections_results.json`, n = 4, six systems): the decoy passes N_correct, S_equal, per_V_coef_equal, hermite_ok, deg_ok, bound_ok on 6/6 systems. `taylor_equals_bruteforce` reads True but compares the brute-force data to itself (vacuous). The harness's own `vectors_examined` shows 0 for the decoy versus 4,536-22,680 for the real pipeline, and `Z_rep_ring` call counts show 0 versus 243: visible, but only because the decoy did not fake them.

## D2a / D2b: vacuous Lean statements through the Comparator
Both accepted: "Lean default kernel accepts the solution. Your solution is okay!" (axioms: propext, Quot.sound, Classical.choice). D2a: `satCount F = satCount F` (rfl). D2b: hypothesis `(1:ℕ) = 0`, conclusion `satCount F = 2^n` (proved from the contradiction). Nothing in the kit's build, Comparator or axiom check flags either.

## D3: non-vacuity witnesses for the six kit theorems
All compile (`lean/Witnesses.lean`): `branch_partition` (two concrete instances, one with both sides true and one with the first disjunct false), `hermite_unique`, `degree_control` (m = 1, y = X), `exists_le_average`, `greedy_contracts`, `contract_correct` (Net = ℕ, size = id, a one-child recursion satisfying `step`). They show hypotheses are satisfiable. They do not show fidelity to the paper. The `contract_correct` witness has alg = Z, so its conclusion is trivial; what it checks is that `leaf` and `step` are jointly satisfiable by a real recursion.

## Scoring against the prereg
- P1: met. D1 passes all correctness fields in 36/36 of the cases the real counter passes (threshold 99%). The self-reported counters are whatever the decoy chooses; the real counter's value is 1344 against 2^4 = 16, so at toy scale a correct honest implementation does about 84x more assignment evaluations than brute force.
- P2: met as stated, and it needs a caveat. The known-primitive rule flags D1 in 36/36 and misses D1b in 36/36. The Z-call profile separates both from the real counter (0 versus 216), but D1c spoofs it with one cosmetic call. No probe I wrote separates a determined decoy from the real counter at these scales.
- P3: met. Comparator accepts both; nothing else in the kit flags either.
- P4: met. All six witnesses compile (one needed a one-line fix, logged).
- P5: not run; it holds by construction (the lemma-level harnesses never call a Counter).

## What this shows
- At n <= 9 the end-to-end correctness checks cannot distinguish the paper's mechanism from a 2^n brute force. The lemma-level checks show the lemmas hold; they say nothing about whether the composed algorithm is subexponential, and the cost model puts that regime out of reach of any test.
- Any "work" evidence that comes from instrumentation inside the object under test is spoofable. Independent probes detect only decoys that use the primitives the probe knows.
- Comparator certifies proof against statement, not that the statement is non-trivial or faithful.
- None of this is an assertion about the preprint's algorithm.

## Limitations
Toy sizes only (n <= 5 for the counter runs). The decoys are my constructions; a different decoy or probe could give different detection results. The Lean witnesses were written by the same model as the statements. Nothing here has been reviewed by anyone else.

## Sources
Every figure above is produced by the scripts and committed output in this folder (`run_controls.py` and `controls_D1_results.json`; `run_sections_controls.py` and `controls_sections_results.json`; Comparator logs in `logs/`). The preprint itself is the only external source.
