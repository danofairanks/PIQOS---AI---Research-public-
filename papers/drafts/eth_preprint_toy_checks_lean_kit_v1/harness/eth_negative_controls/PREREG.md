# Prereg: negative controls ("absurd examples that pass everything") for the ETH-preprint checks
Written 2026-10-29 before any decoy code or Lean file exists. Purpose: measure what our own evidence cannot distinguish. This audits our instrument, not the preprint's authors; nothing here is an assertion that the preprint's algorithm is a decoy. All decoys live in a folder named `negative_controls/`, are labeled DECOY in their first line, and are never presented as the paper's method.

## Controls
- **D1: brute-force decoy counter.** A `DecoyCounter` that subclasses `eth_counter.Counter` and answers `taylor_decoupled(...)` by shifting the brute-force polynomial H(T) (exact, exponential in n), returns `design_at(t)` with `bad = 0`, and reports plausible self-reported `counters`. It has the paper's interface and none of its mechanism. Run through `run_tests.run_case` (fields L2, L3, L4, design_violations, deg checks, counters) and through the final-count step of `sections345_run`.
- **D2a: trivially true Lean statement.** Challenge `theorem decoy_refl (F) : satCount F = satCount F := by sorry`, solution `rfl`, Comparator config as the real kit.
- **D2b: vacuous-hypothesis Lean statement.** Challenge with a hypothesis that is unsatisfiable (e.g. `(h : (1:ℕ) = 0) : satCount F = 2^n`), solution proved from `h`.
- **D3: non-vacuity witnesses for the six real theorems.** For each real challenge statement, a Lean `example` with concrete instantiations showing its hypotheses are satisfiable (a standard non-vacuity check, written by me, so the fidelity caveat applies). This is a kit improvement, not a decoy.
- **D4 (detector probe for D1).** A harness-owned probe, independent of the object under test, that counts calls to the assignment-enumeration primitives (`count_sat`, `brute_H`, `Counter.Z`) during a run and reports them next to the self-reported counters.

## Predictions (with my probability)
- P1: D1 passes every correctness field of `run_case` and the Sections 3-5 final count in at least 99% of the same seeds the real counter passes (0.95). Self-reported `assign_evals_over_2^n` can be set to anything and is not evidence (0.99).
- P2: D4 flags D1 in 100% of runs, because D1 calls the instrumented primitives (0.9). I also predict a second decoy that enumerates assignments by a primitive D4 does not know about (e.g. a numpy vectorized loop) passes D4 (0.85). So D4 detects a known decoy, not decoys in general.
- P3: Comparator accepts D2a and D2b (0.97). No existing step in our kit (build, Comparator, axiom check) flags either (0.95).
- P4: the D3 witnesses can be written and compile for all six real theorems (0.8). `contract_correct` needs a constructed toy Net, the likeliest to take extra effort. A compiling witness shows non-vacuity only, not fidelity.
- P5: no existing lemma-level harness (Lemmas 4.4-4.8, 5.2, 6.2, Appendices A, B, D) is affected by D1, because they test the paper's constructions directly and never call a counter (0.95). Their results therefore say the lemmas hold, not that the composed algorithm is subexponential.

## Defeat conditions
- "D1 is invisible to existing checks" is defeated if any existing correctness field or harness fails or flags D1 at the same seeds where the real counter passes.
- "Comparator cannot see vacuity" is defeated if Comparator rejects D2a or D2b.
- "D4 detects D1" is defeated if D4 misses D1, or flags the real counter equally (no discrimination); the real counter must show a different, larger enumeration profile than the decoy at the same seeds only if it truly differs, and equal or smaller profiles are reported as observed.
- "Control worked" is defeated if D1 fails any correctness field for reasons other than a harness bug (D1 is meant to be correct by construction).

## Interpretation rules
- A pass by D1 is not a claim about the preprint. It states the discriminating power of our evidence: at n <= 9 the end-to-end correctness checks cannot tell a 2^n brute force from the paper's mechanism, and the time bound is out of reach of any test (cost model: regime above roughly 2^(10^10)).
- If D4 flags D1, I report that D4 is a weak, implementation-dependent probe, not a verification of subexponentiality.
- Results go into one short section ("What these checks cannot see") of the kit; the decoy code stays in `negative_controls/` with the DECOY header.

## Deviation rule and stopping
Any change to a control, seed set or threshold after seeing data is logged in DEVIATIONS.md. Same seeds as the existing runs (1000 + s) for D1. If D3 fails for a theorem, report it as a finding about that statement, not as a reason to alter it. Stop after the controls above; no further decoys.
