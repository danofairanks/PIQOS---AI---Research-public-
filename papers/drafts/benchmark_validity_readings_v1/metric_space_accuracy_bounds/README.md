# An Interval Set by the Metric: Reading "Deterministic Bounds on Accuracy and Stability of Metric-Space Regression and Classification"

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one paper, "Deterministic Bounds on Accuracy and Stability of Metric-Space Regression and Classification" (arXiv:2610.22564v1, 15 October 2026; the paper names ORNL, DLR and Warwick). The authors are called "the authors"; organisations are named only as the paper names them. No individual is named and no intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance; one reader, an AI system. Read from an operator-supplied copy (45 pp). Read via text extraction: abstract, Sections 1-3, experiments, discussion; appendix dataset details and proofs not read. Lens: the series overview. Same-source caveat: single Anthropic-model reader. Post-hoc; see the predictions file in this folder. Code (open-source per the paper) and data not accessed.

## What it is
Algorithm 1 builds an enlarged dataset D_M' by reassigning, to each anchor input, targets of samples within tau_X (input) OR tau_Y (target). Average kernel size K = mean pairwise target distance within each feasible set. Theorem 2.9: (1/2)K <= best empirical error <= K on D_M' (regression); Corollary 2.11: accuracy in [1-K, 1-K/2]. Lower bound is the triangle inequality on several distinct targets sharing one input. Proposition 2.5: accuracy-stability trade-off (small error at separated ambiguous targets forces a large local Lipschitz constant). Distributional analogue: Bayes squared risk = (1/2) K^2.

## Flags (ranked; post-hoc)
1. **Bound is on the constructed dataset, not the data.** Transfer to D_M needs Proposition 2.13 (Lipschitz regressors, equal feasible-set sizes, balanced weights); the experiments call the comparison "descriptive" and compute model errors on D_M' for only some datasets. The abstract's "best achievable" error/accuracy carries the qualification only in "on a constructed dataset".
2. **K is set by free parameters.** K grows with tau_X; where no noise model exists tau_X comes from an empirical quantile q (0.02-0.1 in the tables). For most tabular and image datasets the "bound" is a function of a chosen quantile. Sensitivity analyses are reported; the dependence is not removed.
3. **For images K measures the metric, not label ambiguity.** Wavelet-l2 pseudo-metric on CIFAR-10 gives K = 0.144 (train) / 0.162 (test), upper accuracy 92.81 / 91.88 (C1). The paper's "state-of-the-art" CIFAR-10 accuracies are 89.6 / 91.2; from the reader's own knowledge, not checked, public CIFAR-10 results have been well above 99% for years, which would exceed the interval; "differing evaluation protocols" is the stated reason the comparison is not a violation. MNIST returns [100, 100] (K = 0). The paper concedes that a poor metric can "fail to detect genuine ambiguity".
4. **Central assumption untestable from the data.** Assumptions 1.2 / 2.6 posit an unobserved admissible multiset R containing the reassigned pairs; nothing in the data checks it, and the paper states the constructed frequencies carry no probabilistic meaning.
5. **Theory largely standard.** Bayes squared risk = (1/2) E||Y - Y'||^2 for conditionally i.i.d. Y, Y' is the textbook variance identity; Proposition 2.18 (positive gap when training error is below the Bayes level) follows from test risk >= Bayes risk > train error. Cover-Hart and Bayes-error estimation are cited; no comparison against Bayes-error estimators or conditional variance on the same datasets (the paper says those need extra assumptions).
6. **Interval width is a factor of 2 by construction** (synthetic ratio 1.99; C2); models landing inside it is weak evidence of tightness.
7. **Noise-injection checks are designed-in** (random labels or sigma raise K, which the construction produces); they show sensitivity to noise, not agreement with a true floor.
8. **Synthetic example (C3), inconclusive.** Target noise U([0, 0.03]) has std 0.00866; bounding the input-noise effect with Lipschitz 0.9 gives a true-floor bracket [0.0087, 0.0114]. The reported lower interval ends (0.0102 train, 0.0113 test) fall inside it, so whether the "lower bound" exceeds the real noise floor cannot be decided without the exact f and noise draw. Not a finding; a check to run with the code.

## Holds
Accuracy-stability trade-off (Proposition 2.5) is clearly derived and illustrated (GP/SVR models below K/2 have larger empirical Lipschitz constants and larger test error); explicit scope paragraph (depends on (D_M, d_X, d_Y) and thresholds); open code; limitations section; reported intervals are internally consistent (C1: [1-K, 1-K/2] reproduced to 0.01 on all six rows).

## Correction to an earlier informal evaluation (2026-10-25)
The earlier informal evaluation put K at 8-16% of accuracy on CIFAR-10; the intervals imply K = 14.4% (train) and 16.2% (test), with K/2 = 7.2-8.1%. The earlier informal evaluation also called the synthetic floor "about 0.009" and suggested the lower end may exceed it; the stated noise supports only the bracket [0.0087, 0.0114] (C3), so that suggestion is not established.

## Open
Appendix proofs and dataset details; exact synthetic f and noise draw; whether published CIFAR-10 / RESISC45 models were evaluated on D_M' anywhere; a run against kNN Bayes-error estimators on the same datasets.

## Evidence tier and deeper-pass flag (added 2026-10-25)
**Tier:** E2 read (main text and experiments; appendix proofs not read). E1 on reported values: interval self-consistency and the synthetic floor bracket (checks.py, inconclusive). E3: flags 3 and 4 are interpretation.
**Deeper pass:** recommended. Headline depends on flag 3 (metric artifact) and flag 1 (bound on D_M'); code is open and the synthetic example is reproducible. Decisive tests: reproduce the synthetic floor exactly, run a kNN Bayes-error estimator on the same datasets, and vary q. Not done.

## Limitations: what this does and does not establish

- One reader, an AI system, reading a paper and its tables; the flags above are leads, each tied to a page or table, not verdicts, and a paper may answer them in places not read (see what was read and not read at the top and under Open).
- The number of flags is not a severity ranking (see the series overview).
- Evidence classes: E1 executed here (scripts and their outputs in this folder), E2 read, E3 interpretation, as marked in the text.

## Reproduction

Everything is in `benchmark_validity_readings_v1/metric_space_accuracy_bounds/`: `predictions_fixed_2026-10-25.md`; `checks.py`; `checks_output.txt`; `quote_checks_output.txt`; `tool_scan_*.json`. Re-fetched from arXiv on 2026-10-26: the file is byte-identical (sha256 `374e5957361615373b926709dc69461f8d32db243c62f9a91df13f41308f06eb`). `quote_checks.py` (in the series folder) reports which double-quoted strings of this reading occur in the paper's text layer; strings that did not match were rewritten as paraphrases or corrected to the paper's wording before publication. The paper's PDF is not stored here; the preregistration and the scripts are.
- **Predictions** were fixed before the measurement they concern (`predictions_fixed_2026-10-25.md`); that order is the evaluator's own record and is not independently timestamped.

## References

Sources: the paper named in the scope line above (PDF sha256 `374e5957361615373b926709dc69461f8d32db243c62f9a91df13f41308f06eb`); the numbers recomputed in the scripts are transcribed from its tables.

## Revision log

- *2026-10-26, v1.* First public version, from the reader's working notes of 2026-10-25. Quotation marks were removed from, or corrected in, phrases that did not match the paper verbatim; cross-references to working notes and workflow remarks were not carried over.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
