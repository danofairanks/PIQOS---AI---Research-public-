# Results: formalization kit (scored against PREREG.md)
Comparator (`lean/comparator_EthKit.log`): "Lean default kernel accepts the solution. Your solution is okay!" for all 6 theorems; axioms limited to propext, Quot.sound, Classical.choice. Reproduce: `lean/run_cmp.sh EthKit` in a project with Mathlib d13f23b7.

| ID | Statement | Prereg P | Outcome |
|---|---|---|---|
| S1 | FormulaSat / satCount definitions | n/a | defined (in challenge file) |
| S2 | Lemma A.1 branch partition (`branch_partition`) | 0.85 | proved, Comparator OK |
| S3 | Hermite uniqueness over Q (`hermite_unique`) | 0.8 | proved, Comparator OK |
| S4 | Lemma 5.2 degree control (`degree_control`) | 0.7 | proved, Comparator OK |
| S5 | Lemma 6.2 averaging + the (27/32)^n contraction (preprint Lemma 6.2) (`exists_le_average`, `greedy_contracts`) | 0.8 | proved, Comparator OK |
| S6 | Abstract induction shell (`contract_correct`) | 0.9 | proved, Comparator OK |
| S7-S10 | Lemma 3.3, 5.1, 5.2 congruence, 4.6 | 0.2-0.4 | not written (DEVIATIONS 3) |

Prediction check: >=4 of 10 proved: met (5 of the 10 IDs, 6 theorems). S4 proved: yes. S7-S9 "stated only": not met (not stated). Comparator accepts: yes.

## What this does and does not establish
- Kernel-checked: six small lemmas that the paper's argument uses. They are the easy parts (pure logic, polynomial degree, a counting step, a generic induction shell).
- Not established: any of the hard content (Beigel-Tarui lift, Section 2.7 design, Appendix D tensor contraction, precision bookkeeping), nor the subexponential time bound. The asymptotic claim is unexercised.
- Fidelity: statements and proofs were written by the same model family. The kernel certifies proofs, not that `branch_partition` etc. mean what the paper's lemmas say. `contract_correct` is an abstract shell: it holds for any network family satisfying leaf/step hypotheses; whether the paper's D.4 child networks satisfy `step` is exactly obligations O5-O8 in `INDUCTION_LEMMA.md`, which stays unformalized.
- Not independent review: nothing here has been seen by anyone else.
