# Predictions fixed before reading: "A Fix for Softmax and Cross-Entropy" (arXiv 2610.31642), v1 to v3, and the works it credits

*AI-assisted. Predictions were written in three batches, each committed before the text it covers was opened. That order is the evaluator's own record and is not independently timestamped.*

**Known before batch 1:** the arXiv id; v3 is 10 pages (1,578,331 bytes); an earlier v1 of 10 pages (1,520,908 bytes) had been read once on 2026-10-25 (one-line note: a numerical-precision result; cliffs at ln(1/u); margin equilibrium near log(1/epsilon)). Nothing of v2 or v3, not even the title.

## Batch 1: version reading (v1 to v3)
| # | Prediction | Confidence |
|---|---|---|
| V1 | The title or subtitle changed between v1 and v3 | 0.40 |
| V2 | The abstract's headline claim is the same, with a broader scope sentence added | 0.55 |
| V3 | At least one experiment, task or architecture is in v3 that was not in v1 | 0.70 |
| V4 | The related-work or baseline set grew: another remedy is compared or discussed in v3 | 0.70 |
| V5 | The numerical claims reproduced from v1 (cliff values; margin fit) are unchanged | 0.85 |
| V6 | A limitations or scope paragraph was added or expanded | 0.50 |
| V7 | Code or artifact availability is stated in v3 and was not in v1 | 0.50 |
| V8 | The proposed fix itself (its definition) is unchanged | 0.75 |
| V9 | No claim of v1 is withdrawn in v3 | 0.80 |
| V10 | The page count stayed at 10 | 0.50 |

## Batch 1: evaluation of v3
| # | Prediction | Confidence |
|---|---|---|
| E1 | The main demonstrations are small or synthetic tasks, not large-language-model training | 0.70 |
| E2 | Variance across seeds is reported for the headline comparisons | 0.50 |
| E3 | The fix is compared against a small baseline set whose tuning is not matched | 0.55 |
| E4 | The rounding explanation rests on a demonstration that removing the rounding removes the failures, not on a separate test that it is the only cause | 0.60 |
| E5 | The abstract's generality exceeds the tested scope, with the conditions in the body | 0.55 |
| E6 | The closed-form statements recompute exactly or within stated approximation | 0.85 |
| E7 | Precision and hardware conditions are matched across compared methods | 0.60 |
| E8 | At least one number in the text does not reconcile with its figure or table | 0.20 |
| E9 | The paper states costs of the fix (runtime, memory) | 0.50 |
| E10 | Code is released or an implementation snippet is given | 0.60 |

## Batch 2 (before fetching the four works v3 credits)
| # | Prediction | Confidence |
|---|---|---|
| R1 | The May 2026 paper states that Slingshot spikes are caused by low-precision rounding of the target gradient and proposes a zero-sum gradient projection | 0.85 |
| R2 | That paper was posted before v1 and is cited in v1 only for the projection comparator, not for the mechanism | 0.80 |
| R3 | The 2025 paper introduces the term "Softmax Collapse" and a surrogate (StableMax); it does not propose an exact-arithmetic rewrite of cross-entropy | 0.85 |
| R4 | The independent report finds the NaN gradient in the printed implementation of the first version under masked logits, and may report further findings | 0.75 / 0.45 |
| R5 | That report tests implementations with randomised inputs against a high-precision reference | 0.70 |
| R6 | The Flash Attention paper concerns attention softmax, not cross-entropy over logits | 0.65 |
| R7 | What v3 adds relative to the two earlier papers is the log-space implementation, the soft-target bug, the margin equilibrium and the precision grid | 0.75 |
| R8 | None of the four contradicts v3's closed forms or printed examples | 0.90 |

## Scores (post hoc, one reader)
**Version reading.** Held: V10. Partial: V3 (a lambda = 0 panel described and four-task hyperparameters disclosed; no new task), V4 (a few references added; no new comparator), V5 (the cliff values and margins are unchanged; surrounding numbers and wordings changed), V9 (no claim withdrawn outright; one sentence dropped, two results re-described). Missed: V1 (title unchanged), V2 (abstract unchanged), V6 (no limitations paragraph; an Errata was added), V7 (no availability statement), V8 (the fix changed: the printed code and an equation).
**Evaluation.** Held: E1, E2, E5, E6, E7. Partial: E3, E4, E9. Held in part: E10. Missed: E8 (no mismatch in v3; v1's "99-100%" against a table minimum of 98.9 was corrected).
**Cited works.** Held: R1, R2, R3, R4, R6, R7, R8. Partial: R5 (property-based tests against exact properties, not a reference implementation).
