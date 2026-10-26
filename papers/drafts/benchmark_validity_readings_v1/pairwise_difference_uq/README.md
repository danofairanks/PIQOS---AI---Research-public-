# A Gamma That Cannot Be Negative: Reading "Uncertainty Quantification in Pairwise Difference Learning for Classification"

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one paper, "Uncertainty Quantification in Pairwise Difference Learning for Classification" (arXiv:2610.21554v1, 15 October 2026; posted after publication in Machine Learning 115, 12; the paper names IDIADA, Porsche and LMU). The authors are called "the authors"; organisations are named only as the paper names them. No individual is named and no intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance; one reader, an AI system. Read from an operator-supplied copy (32 pp). Read via text extraction: full body and Appendices A-C. Not read: Appendix E result tables; figures not visually inspected. Lens: the series overview. Same-source caveat: single Anthropic-model reader. Post-hoc; see the predictions file in this folder. Code (pdll) and data not accessed.

## What it is
PDC: binary classifier gamma(x, x') = P(same class), trained on N^2 pairs with phi(x, x') = (x, x', x - x'); query prediction = average over anchors of a prior-reweighted posterior (eq. 4-5). UQ: base learner first-order / second-order; aggregation strategies UL, UP, ULP; entropy- and variance-based TU/AU/EU. Evaluation: 99 small OpenML datasets, 5x5 CV, macro-F1, five tree-based base learners; UQ scored by "rank correlation" between uncertainty and misclassification (TU/AU) and against a per-point ECE (EU).

## Flags (ranked; post-hoc)
1. **Headline UQ metric inconsistent and not like-for-like.** Defined as Goodman-Kruskal gamma "= C/(C+D)" over (misclassified, correct) pairs; the standard gamma is (C-D)/(C+D). C/(C+D) cannot be negative, yet the text reports "only 5% negative correlations" and values in [-1, 0]. If proper gamma, 0.56 = AUC' of about 0.78 (gamma = 2*AUC' - 1, ties excluded; C1); under the written formula 0.56 would be near chance. Baseline vs PDC is reported as "median 0.23" vs "mean 0.56" (different statistics). Gamma drops tied pairs, so tie-heavy baselines (leaf-constant probabilities) are scored on a different pair set; in the simulation the tie-heavy score gets a higher gamma than the continuous one at equal underlying signal (0.511 vs 0.441; C2), so ties do not explain the reported PDC advantage and may slightly understate it, but the comparison is still not like-for-like. Re-score with a tie-aware metric (AUROC with ties = 1/2). Code check pending.
2. **Epistemic uncertainty validated by proxy and by picture.** EU scored against a per-point "ECE_i" defined as the gap to the bin average, which the text says is an approximation of an unobservable. The AU/EU-separation claim rests on one 2D synthetic figure judged visually although ground truth is known there; no quantitative score. AU-TU Pearson 0.98, so EU is a small remainder. No OOD / shift test.
3. **Significance tests anti-conservative.** "Significant wins" use a Student's t-test over 25 CV runs (5x5) that share training data; App. C.2 reports p = 1e-16 on 26 runs; no multiplicity correction over 99 datasets.
4. **"Unique contribution" (App. C.1) is an oracle-max.** Takes the best estimator per dataset on test scores; adding a model with its own variance raises the maximum by selection. The 32-times-the-best-baseline figure is not a causal contribution.
5. **Accuracy gain modest; tuning parity and dataset provenance unclear.** Macro-F1 gains for ensembles +0.014 (RF), +0.016 (Extra Trees); trees +0.029, +0.055. PDC has extra tuning surface (anchors, joint features) and N^2 pairs; equal tuning budgets not stated. The 99 datasets and the "400+ datasets" performance claim come from the authors' earlier papers.
6. **Efficiency/interpretability claims unsupported.** Discussion: a single PDC tree matches ~100-tree ensembles, "more interpretable", and "significantly reduced computational complexity". Appendix B: training O(p(N^2, ...)), A anchors per query, doubled for symmetry; no timings. A tree plus all training anchors is not a single readable tree.
7. **Causal story (Section 6.1: anchors, binary reduction, ensembling) is asserted without ablation.**
8. **UQ baseline is the base learner's own uncertainty only;** no calibrated probabilities, conformal prediction or deep-ensemble comparison. The regression PDL UQ work is excluded as regression-only.
9. **"Rigorously validated through extensive empirical studies" (Conclusion)** exceeds what 1-8 support.

## Holds
Order-of-learner decomposition (deterministic / probabilistic / second-order) and UL / UP / ULP aggregation clearly defined; variance-based measures matching or beating entropy-based ones agrees with the cited prior work; open library; 99 datasets x 25 runs; Appendix A states the non-i.i.d. pairs and multicollinearity caveats.

## Correction to an earlier informal evaluation (2026-10-25)
The earlier informal evaluation said the tie handling was "not like-for-like"; the simulation (C2) shows ties inflate gamma for the tied score, so ties cut in the baseline's favour, not against it. The reported PDC advantage is not a tie artifact.

## Open
Which formula pdll computes for the rank statistic; Appendix E; whether baselines and PDC shared a tuning budget; timing; whether the 99 datasets overlap those used to design PDC in refs [5, 6].

## Evidence tier and deeper-pass flag (added 2026-10-25)
**Tier:** E2 read (body and Appendices A-C; Appendix E and figures not read). E1 only on random-data simulation of the metric definition, not on the paper's data or code. E3: flags 4-7 are interpretation.
**Deeper pass:** recommended, cheapest of the set. Flag 1 turns on a single line in the open library (pdll): which formula the rank statistic computes. Then re-score with AUROC and a paired test on the same folds. Not done.

## Limitations: what this does and does not establish

- One reader, an AI system, reading a paper and its tables; the flags above are leads, each tied to a page or table, not verdicts, and a paper may answer them in places not read (see what was read and not read at the top and under Open).
- The number of flags is not a severity ranking (see the series overview).
- Evidence classes: E1 executed here (scripts and their outputs in this folder), E2 read, E3 interpretation, as marked in the text.

## Reproduction

Everything is in `benchmark_validity_readings_v1/pairwise_difference_uq/`: `predictions_fixed_2026-10-25.md`; `checks.py`; `checks_output.txt`; `quote_checks_output.txt`; `tool_scan_*.json`. Re-fetched from arXiv on 2026-10-26: the file is byte-identical (sha256 `b2c56cf9544633f4f93d4cf9aa7e701b041d6b9dd4db18161c089172def21606`). `quote_checks.py` (in the series folder) reports which double-quoted strings of this reading occur in the paper's text layer; strings that did not match were rewritten as paraphrases or corrected to the paper's wording before publication. The paper's PDF is not stored here; the preregistration and the scripts are.
- **Predictions** were fixed before the measurement they concern (`predictions_fixed_2026-10-25.md`); that order is the evaluator's own record and is not independently timestamped.

## References

Sources: the paper named in the scope line above (PDF sha256 `b2c56cf9544633f4f93d4cf9aa7e701b041d6b9dd4db18161c089172def21606`); the numbers recomputed in the scripts are transcribed from its tables.

## Revision log

- *2026-10-26, v1.* First public version, from the reader's working notes of 2026-10-25. Quotation marks were removed from, or corrected in, phrases that did not match the paper verbatim; cross-references to working notes and workflow remarks were not carried over.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
