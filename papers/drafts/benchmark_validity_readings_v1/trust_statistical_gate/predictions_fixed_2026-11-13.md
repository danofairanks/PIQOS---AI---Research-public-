# Predictions fixed before reading: TRUST (arXiv 2611.10787v1)

*AI-assisted. Predictions were written in three batches, each committed before the part it covers was read. That order is the evaluator's own record and is not independently timestamped.*

**Known before the first batch:** the arXiv id, version v1, 44 pages, file size, and the operator's words "Another RSI paper". Title, authors, abstract and method were not read. Priors came from earlier readings of recursive-self-improvement papers in this series.

## Batch 1 (before any page; scored on the main text and the first appendices read)
| # | Prediction | Confidence |
|---|---|---|
| G1 | The improver does not edit its own improver, acceptance rule or evaluator ("recursion" is wider than what the loop does) | 0.60 |
| G2 | Improver, selection and evaluation are not independent (the gate's input is writable by the loop or chosen by the builders) | 0.70 |
| G3 | The headline gain is carried by one component, benchmark or model, or sits inside run-to-run noise | 0.50 |
| G4 | Baselines are not matched for compute, budget or number of attempts | 0.55 |
| G5 | The abstract states the headline's conditions less completely than the body | 0.55 |
| G6 | Code or artifacts are released only in part, or not at all | 0.60 |
| G7 | One model family dominates the setup (subject, judge or generator from the same lineage) | 0.50 |
| G8 | A held-out or contamination control for the core claim is missing or weak | 0.45 |
| G9 | "Recursive" or "self-improving" in the title or abstract exceeds what the body shows | 0.60 |
| G10 | An ablation separating the loop from extra compute or extra attempts is present | 0.35 |
| G11 | Variance across seeds or runs is reported for the headline | 0.40 |
| G12 | At least one table or number in the body does not reconcile with the abstract | 0.35 |

## Batch 2 (before the parts not read at the first pass: Appendices A.1, B, F, G.4, H, I)
| # | Prediction | Confidence |
|---|---|---|
| A1 | The LLM-allocator comparison is reported only for one setting | 0.65 |
| A2 | Labelling noise in the zero-tolerance error rate and the acceptance rate (scores on 300 test examples) is not discussed in the appendices | 0.65 |
| A3 | The greedy-gate case study is one or two curated runs, not a rate | 0.80 |
| A4 | The overfitting diagnostic reads validation against test on the same runs, without independent re-validation | 0.45 |
| A5 | The proof of the error-rate theorem uses that the testing level is determined before the round, and the LLM enters only through that level | 0.75 |
| A6 | The appendix gives a heuristic for the data-reuse correction strength but no procedure that estimates it or verifies the assumption | 0.70 |
| A7 | No operator edits the gate, the scorer, the validation pool or the allocator | 0.90 |
| A8 | The data-reuse assumption (Assumption 1) is not tested empirically | 0.70 |
| A9 | At least one stated bound or proof step contains a condition that the main configuration violates beyond those already found | 0.25 |

## Batch 3 (before Appendices C to E)
| # | Prediction | Confidence |
|---|---|---|
| C1 | The power result takes the proposer eventually producing an improving candidate as an assumption | 0.85 |
| C2 | The mixture extension of the power bound still needs every betting fraction in the admissible range, so it does not cover the mixture used | 0.60 |
| C3 | The constant kappa is existential, not instantiated | 0.85 |
| C4 | No bound in C to E is evaluated at the experiments' settings | 0.80 |
| C5 | The drawdown bound is looser than the empirical drawdowns (possibly vacuous) | 0.55 |
| C6 | The deterministic-horizon extension of the error-rate proof needs only pre-round determination of the testing level and budget | 0.80 |
| C7 | The gain bound has a term that does not vanish with sample size and can reach the tolerance times the number of accepted updates | 0.60 |
| C8 | A step whose stated condition fails in the main configuration, beyond those already found | 0.30 |
| C9 | An outright error in a proof step on one reading | 0.10 |

## Scores (post hoc, one reader)
**Batch 1.** Held: G1, G5, G6 (held in part after Batch 2: code is referred to in Appendix H.2 and not linked), G11. Partial: G2, G3, G4, G7, G9. Missed: G8, G10, G12.
**Batch 2.** Held: A1, A2, A3, A5, A6, A7, A8. Missed: A4 (the overfitting appendix is one worked case). A9 was resolved by Batch 3 (see C8).
**Batch 3.** Held: C1, C4, C6, C7, C8. Missed: C2 (the mixture extension needs only one designated component in the admissible range; the mixture used has one, with weight 1/4), C3 (kappa is an explicit formula), C9 (no error found in the steps read). Partial: C5 (the bound is loose by construction; not evaluated numerically because it needs the distribution of per-update effects).
**Correction made during the reading.** Before Batch 3 the reading said the main configuration violates Assumption 2(c) because three of four betting fractions exceed 2e/(1+e). Appendix D.3 withdraws that: only one designated component must satisfy it. The reading below carries the corrected statement.
