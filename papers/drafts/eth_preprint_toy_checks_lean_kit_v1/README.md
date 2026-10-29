# Toy-Scale Checks and a Partial Lean Kit for a Model-Generated ETH Refutation

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** The audited object is a public preprint in the `github.com/openai/math` repository ("The Exponential Time Hypothesis is False", 25 October 2026, sha256 `5b1612dc2eebb2cad5b4cbe62d1fed2982f01ab1908c26f70010a651487e8123`). The organization is named as the repository names itself. No individual is named and no intent is attributed.

**Disclosure.** Everything here (reading, test harnesses, Lean statements and proofs) was produced by one AI model with an operator directing the order of work. No mathematician has reviewed any of it. Agreement among these artifacts is not independent verification.

## In plain terms
A very large computer-generated paper claims a faster way to count the solutions of a certain kind of logic puzzle than anyone believed possible. If it is right, a long-standing belief in computer science is false.

We did what a careful outsider can do without spending months on it. We rebuilt the paper's pieces at toy size and checked that each one works. We found no mistake. We also had a computer proof-checker confirm six small supporting facts.

What this does not tell you is whether the paper is right. The claim is about how fast the method runs on enormous inputs, and nothing we can run comes close to that size. We also showed, with deliberately fake "decoy" programs, that our own checks cannot tell the paper's method from slow brute force at toy size, and that the proof-checker accepts statements that mean nothing. So "no mistake found" is weak evidence. It is not confirmation.

The most useful next step is for someone who knows the area to read the six Lean statements against the paper (`REVIEW_KIT.md` says how).

## 1. Question and result in one paragraph
Can an outside reader gain evidence about a 67-page claimed deterministic subexponential algorithm for exact #k-SAT without trusting its authors? Answer reached: no gap was found, and none was closed. Each component lemma passes at toy scale; six small supporting lemmas are kernel-checked in Lean and accepted by the Comparator; the asymptotic claim and the Appendix D induction were not exercised. A cost model puts the subexponential regime at n above roughly 2^(10^10) to 2^(10^17), so no experiment can test the headline claim directly.

## 2. What was done (all pre-registered before measuring; scores in `results/`)
- Reading and claim extraction: `results/RESULTS_eth_paper.md` (includes a logged misreading of the Theorem 1.1 exponent, corrected from rendered pages).
- Section 2 counter implemented and run on small formulas; Sections 3-5 bounded end-to-end run, 85/85 exact (source: `results/RESULTS_eth_sections345_run.md`); component checks for Lemmas 4.4-4.8, 5.2, 6.2, Appendices A, B, D.3-D.5, D.11, mode counting; sparsification and tensor-contraction cost models. Code in `harness/`, one results file per harness in `results/`.
- Explicit reconstruction of the Appendix D induction with obligations O1-O10 (`INDUCTION_LEMMA.md`). Marked read (R), tested (T) or modeled (M); O10 is read only.
- Lean kit (`lean/`, `RESULTS.md`, `DEVIATIONS.md`): six theorems, Comparator accepted, axioms limited to propext, Quot.sound, Classical.choice.
- O10 counter-model search (`harness/eth_o10_counter_model/`, preregistered): 2,000 random toy networks per condition, two independent ring implementations, no counter-model found; three mutation controls fail as they should (one at 78.6%, just under its 80% preregistered threshold). This moves O10 from read-only to tested on an abstract model of the bookkeeping. It is the fact that reduction modulo 2^q is a ring homomorphism, so a pass was expected.
- Negative controls (`harness/eth_negative_controls/`, preregistered): decoy brute-force counters and vacuous Lean statements, to measure what the checks above cannot see (section 2c).

## 2b. What would falsify the readings here
- "No gap found" fails if any harness in `harness/` is shown to compare against a wrong reference, or if a reviewer finds a counterexample to an obligation O1-O9 at parameters the harnesses did not reach.
- "Cost model puts the regime beyond any testable n" fails if the hidden constants (taken from the paper's stated bounds, per `results/RESULTS_eth_cost_model.md`) are shown to be orders of magnitude smaller.
- "The Lean statements match the paper" is untested; a reviewer who finds a mismatch in `lean/OAI/EthKit/Comparator.lean` falsifies it for that statement.

## 2c. What these checks cannot see
Measured with deliberately wrong "decoy" objects (`harness/eth_negative_controls/RESULTS.md`; these say nothing about the preprint's own algorithm):
- A brute-force 2^n counter wearing the paper's interface passed every end-to-end correctness check in 36 of 36 cases where the real implementation passes, and the Sections 3-5 final-count checks on 6 of 6 systems. At this scale the correctness checks cannot tell the paper's mechanism from brute force, and the cost model puts the subexponential regime out of reach of any test.
- A probe that counts calls to known enumeration functions flagged the decoy that used them (36/36) and missed a decoy that inlined the same loop (0/36); a decoy that added one cosmetic call also evaded the call-count profile. Instrumentation inside the object under test is spoofable.
- Two Lean statements with no content (`satCount F = satCount F`; a hypothesis `1 = 0`) were accepted by the Comparator. It certifies proof against statement, not that the statement is non-trivial or matches the paper.
- Non-vacuity witnesses for the six real theorems compile (`harness/eth_negative_controls/lean/Witnesses.lean`). They show the hypotheses are satisfiable, not that the statements are faithful.

## 3. What this does not establish
- Correctness or incorrectness of Theorem 1.1.
- Any hard content in Lean: Beigel-Tarui lift, Section 2.7 design, Appendix D contraction, precision bookkeeping, the time bound.
- Statement fidelity: the kernel certifies proofs, not that the Lean statements match the paper's lemmas. Same-model authorship of statements and proofs is the weakness a Comparator setup is meant to remove, and here it is not removed.
- That the six statements are faithful to the paper's lemmas (see 2c: non-vacuity witnesses do not settle this).
- Statements for Lemma 3.3, 5.1, 5.2 (congruence), 4.6 were not written (`DEVIATIONS.md` item 3).

## 4. Where a reader can help
`REVIEW_KIT.md` lists the claims that need expert review, in order of importance. A review of the Lean statements against the paper is the cheapest useful contribution.

## 5. Reproduce
`lean/run_cmp.sh EthKit` against a project with Mathlib at revision `d13f23b723b8a846827a245b89c10fc7d3f11612` and the pinned Lean/Comparator versions used by `../openai_math_comparator_audit_v1/` (see its `PINS.txt` and `setup.sh`). Python harnesses run with the system interpreter; each folder's README gives the command.

## Sources
Primary: the preprint named above (`openai/math`, `preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf`). All other numbers are produced by the harnesses in this folder, each with its pre-registration and results file.
