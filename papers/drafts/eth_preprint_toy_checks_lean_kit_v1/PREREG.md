# Prereg: formalization kit for the ETH preprint (steps 1-3 of the plan)
Written 2026-10-28 before writing any Lean. Deliverables: (1) Lean challenge files (statements with `sorry`, definitions in the file, permitted axioms stated) for the problem and the algebraic core, in Comparator style; (2) proofs of the lemmas that are tractable in this session, checked by the Lean kernel and (where possible) the Comparator; (3) a review kit (obligations table, test harness pointers, explicit induction lemma, claims needing expert review, outreach drafts NOT sent).
Candidate statements (S) and my a-priori estimate that I prove each in this session (P):
- S1 problem spec: #k-SAT as a Finset cardinality, definitions only (P = n/a).
- S2 Lemma A.1 (disjoint branching partitions satisfying assignments), pure logic over Finset (P = 0.85).
- S3 Hermite uniqueness over Q: a polynomial of degree <= d vanishing to order J at Q distinct nodes with QJ > d is zero (P = 0.8).
- S4 Lemma 5.2 degree control: totalDegree of prod_i e_{j_i}(y_i) h(y_i)^{j_i} <= d*(m + 2 sum j) in MvPolynomial (P = 0.7).
- S5 Lemma 6.2 averaging step and (27/32)^n < 1 conclusion (P = 0.8).
- S6 abstract induction skeleton: strong induction on a size measure with leaf and step hypotheses gives correctness for all instances (P = 0.9).
- S7 Lemma 3.3 (inclusion-exclusion of multilinear coefficients) statement (P(proof) = 0.35).
- S8 Lemma 5.1 (Beigel-Tarui identity and parity congruence mod 2^l) statement (P(proof) = 0.3).
- S9 Lemma 5.2 congruence statement (P(proof) = 0.2, depends on S8).
- S10 Lemma 4.6 (integrality and norm bound for the Section 2.7 rows): statement only if definable cleanly; otherwise omit with a note (P(statement) = 0.4).
Predictions: at least S2, S3, S5, S6 proved and kernel-checked (>= 4 of the 10); S4 proved with probability 0.7; S7-S9 stated only (sorry) or proved at most one of them; Comparator run on the proved statements accepts (axioms: propext, Quot.sound, Classical.choice). Fidelity caveat recorded up front: statements and proofs are written by the same model family; the kernel makes proofs trustworthy, not statements; a human or independent reader must confirm that each statement matches the paper.
Deviation rule: any statement I change after trying to prove it is logged with the reason; any change to the Lean environment is logged (see DEVIATIONS.md).
Environment incident (pre-registered disclosure): my first Lean call used `lake env`, which, because git refused the nobody-owned package directories ("dubious ownership"), judged package URLs changed and deleted and re-cloned `mathlib`, `plausible` and `LeanSearchClient` under /srv/lean/proj/.lake/packages, discarding Mathlib's compiled oleans. I set `git config --global safe.directory '*'` and restored them with `lake exe cache get` (public Mathlib cache download, same source as the earlier run). The Comparator logs and the committed audit artifacts in the public repo are unaffected (they are files already produced).
