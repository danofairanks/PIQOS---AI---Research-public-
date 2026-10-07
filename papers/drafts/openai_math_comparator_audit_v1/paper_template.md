# What Compiles: Auditing a Model-Generated Mathematics Release with the Lean Comparator

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** The audited object is a public repository, `github.com/openai/math`, and the organization that published it is named as the repository names itself. No individual is named, no intent is attributed, and nothing here is a statement about how the results were produced beyond what the release says. The unit of analysis is a formal statement and a machine verdict.

**Disclosure.** Drafted with AI assistance. The statement-fidelity readings in section 5 were made by one reader (the model that drafted this paper); no mathematician reviewed them. The controls and the logs are mechanical; the readings are not.

## 1. The question

In October 2026 an organization published 722 manuscripts in 372 "result families", produced by an unreleased internal model, with Lean formalizations for a subset. The question put to this audit was whether the formalized results are real reasoning or "harnessmaxxing": output tuned to pass a checker without establishing the claim. Four routes could make that suspicion true for a formalized result, and they are separable:

1. **The proof is unsound but accepted** (kernel bug, forbidden axiom, `sorry`, a computation trusted outside the kernel).
2. **The theorem checked is not the claim made** (a faithful-looking Lean statement that is weaker, vacuous, or junk-value-dependent).
3. **The checking setup can be steered** (the party that wrote the proof also wrote the thing it is checked against).
4. **The checked subset is not representative** (what is formalized is what is easy to formalize, and its pass rate is read as evidence for the rest).

Routes 1 and 3 are what the Lean Comparator is built to close; route 2 needs a human reading each statement; route 4 is a property of the catalogue. This paper reports what was run for 1 and 3, what was read for 2, and what was counted for 4. It does not test whether any process was "reasoning": a valid proof is valid regardless of its author, and the released reasoning summaries were not read.

## 2. What the release is (counted, not trusted)

From the repository at commit `adc7f1241` (single commit, 2026-10-06), by the companion script `census.py`:

- 722 manuscripts in 372 families; 162 manuscripts (22%) in 127 families (34%) have a formalization listed in `lean/formalization.yaml`; 405 Comparator configs with 507 theorem names, every one permitting exactly `propext`, `Quot.sound`, `Classical.choice`.
- The catalogue's own review field reads `status: "unchecked"`; its automation field lists the method as `agent`; its scope reads "Partial progress." The README says "Some of the unformalized results could have issues."
- Text checks over `OAI/` and `ComparatorChallenges/`: no `native_decide`, `ofReduceBool`, `unsafe`, `implemented_by`, `@[extern` or `sorryAx`; `sorry` appears in 404 of 405 challenge files and in no solution file (by design: the challenge states the theorem, the solution proves it); one challenge file states its claim with an `axiom`; three `axiom` hits in `OAI/` are inside comments. These are text checks, not verification.
- **Selection (route 4).** Of the ten results for which the release publishes reasoning summaries, six have no formalization listed (two-point correlations of multiplicative functions, the irrationality exponent of π, quasipolynomial Szemerédi bounds, the Mézard–Parisi formula, Bloch's law, free-group-factor isomorphism). Other high-stakes titles with none: the full BSD formula from low Selmer corank, Milne's rationality conjecture, Hilbert's tenth problem over ℚ. Formalization coverage tracks the tractability of a statement, not the significance of the claim, so the 22% that is machine-checked cannot vouch for the other 78%.

## 3. Method

Lean 4.34.1; Mathlib at the repository's own pin, built from source (the cache host was unreachable); the Comparator and `lean4export` at their v4.34.0 commits, rebuilt against 4.34.1; `landrun` for sandboxing. Exact pins are in `PINS.txt`. For each config the project contained only the OAI modules in the solution's import closure, copied unmodified, plus the challenge and its JSON, unmodified, with the repository's own compiler option (`autoImplicit false`). Each run was the Comparator's own procedure: build the challenge, export its statement, build the solution, export it, compare, and check axioms and the kernel.

Only 23 of the 405 configs have a challenge file and a solution closure that avoid a full `import Mathlib` and external packages; 377 challenge files import all of Mathlib, which on this 4-core host would have been a multi-hour build. The configs run were therefore chosen by build feasibility, then by short statements, not by significance, and they are not a sample of the 405.

**Deviations from the Comparator's documented setup, all in the weaker direction.** `landrun` could apply only a partial Landlock sandbox (kernel ABI v7; it ran with the `--best-effort` flag the Comparator passes); the systemd-run guard was not used; the builds ran as an unprivileged user with no network and a stripped environment instead; the Lean default kernel was the only kernel (no external kernel); `landrun` was v0.1.17 from `go install`, not a build of `main`.

## 4. Controls

Two negative controls on the first config show the harness discriminates:

- A challenge whose `GoodVertex` uses strict instead of non-strict inequality, paired with the real solution: rejected, `Const does not match between challenge and target 'OAI.SeymourSecondNeighborhood.GoodVertex'`.
- A solution module that states the theorem with `sorry`: rejected, `Illegal axiom detected: 'sorryAx'`.

In addition, `#print axioms` on the Seymour main theorem reports `[propext, Classical.choice, Quot.sound]`, and the solution contains 192 theorems and lemmas in 4861 lines with no `decide`-style bulk proofs.

## 5. Results

Eleven configs were attempted; {{ACC}} accepted, {{REJ}} rejected, {{UNF}} did not finish when this draft was last updated. "Accepted" is the Comparator's `Your solution is okay!`: the exported statement matches the challenge's, only the three permitted axioms are used, and the Lean default kernel accepts it.

{{TABLE}}

**Statement readings (route 2), for the accepted configs.** Reading the challenge statement against the English claim, as one reader:

- *Seymour's second-neighborhood conjecture.* An oriented graph is loopless and asymmetric; first neighbors are out-neighbors; second neighbors are vertices other than `v`, not first neighbors, reachable by a path of length two (so sinks are included); a good vertex has at most as many first as second neighbors; the theorem asserts one exists in any nonempty finite oriented graph. This is the standard statement. The proof is a minimal-counterexample argument (reduction, pruning, extremal contradiction) in 43 modules.
- *`FiniteCongruenceGraph`.* A characterization: a finite lattice is the congruence lattice of a finite nonempty algebra if and only if it has a finite colored-graph witness. It is a criterion, not a solution of the finite lattice representation problem; the Lean statement defines algebras, congruences and the witness conditions from scratch, so its fidelity to the manuscript's witness definition is the part a specialist would have to check.
- *`GrahamSpherical`.* A specific 12-point subset of the unit circle (built from the parameter Σ 10^-(m+1)!) with a 50-coloring of every Euclidean space avoiding monochromatic isometric copies, and the denial that the set is Euclidean Ramsey. The statement bundles the witness, the 12-point count, the sphere condition and the coloring claim, so the verdict is about that construction.
- *`AbhyankarSathaye`.* For every n at least 4, a polynomial F in n variables over ℂ with ℂ[x]/(F) isomorphic to a polynomial ring in n−1 variables and F not the image of a variable under any ℂ-algebra automorphism. This is the standard shape of a counterexample to the Abhyankar–Sathaye conjecture in high dimension.

Where a config rejected or did not finish, the table says so and no reading is offered.

## 6. What a pass does and does not establish

**Established, for each accepted config.** A kernel-checked derivation of the Lean statement, from the three standard axioms, with the statement the challenge file exports. A model, a human or a script could have written it; the verdict does not depend on which. The controls show the harness rejects both a changed statement and a `sorry`.

**Not established.**

- *Fidelity beyond my reading.* The challenge files, and every definition in them, come from the same repository as the solutions. The Comparator's trust model assumes the challenge is written by the verifier; here the verifier has to read it. The statements above are short and their readings are stated, but one reader of the same model family is not an independent mathematical review. Statements with many from-scratch definitions (`FiniteCongruenceGraph`, `GrahamSpherical`) carry more of this risk than Seymour's.
- *Kernel and sandbox.* One kernel, one sandbox configuration weaker than documented.
- *Anything about the other configs and the other manuscripts.* The configs run were chosen for build feasibility; most of the 405 configs, and most manuscripts, were not run. The "22% formalized" figure carries no information about the unformalized claims, which include the largest ones.
- *Reasoning versus harness-fitting as a process.* A passing config shows the output is correct, which excludes the hypothesis that the checked artifact is a harness exploit. It does not show how it was found, and the model's reasoning summaries were not read.

**Where "harnessmaxxing" could still live.** In the unformalized majority, in statement fidelity for the formalized ones, and in selection: a release in which the machine-checked part is the part that is easy to check will show a clean pass rate on exactly the subset where a clean pass rate is cheap. None of these is excluded by this audit.

## 7. Limitations

{{ACC}} accepted configs out of 405; configs chosen for build feasibility; one reader; a weaker sandbox; a single kernel; the Lean proofs themselves were not read beyond the top-level structure of one of them; the manuscripts were not read; the controls were run on one config; nothing here is independent of the model family that drafted the paper.

## 8. Reproduction

The companion folder `openai_math_comparator_audit_v1/` holds `PINS.txt`, `setup.sh` (the steps used), `run_cmp.sh`, `census.py`, `make_table.py`, `build_paper.py`, the controls (`controls/`), and every Comparator log (`logs/`). Counts in section 2 come from `python3 -I census.py <clone>`; the results table from `make_table.py` over the logs. Builds need several GB of disk and tens of minutes per config the first time (Mathlib compiles incrementally across configs).

## References

Sources: the repository itself (https://github.com/openai/math, commit adc7f1241); the Lean Comparator (https://github.com/leanprover/comparator) and its README for the trust model; `lean4export` (https://github.com/leanprover/lean4export); Lean 4 (https://github.com/leanprover/lean4); Mathlib (https://github.com/leanprover-community/mathlib4); `landrun` (https://github.com/Zouuup/landrun). Related in this repository: [`model_local_proofs_travel_v1.md`](model_local_proofs_travel_v1.md) (a check that passes inside one harness does not carry to a different one).
