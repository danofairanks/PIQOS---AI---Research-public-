# A Printed Bug and a Late Citation: Reading a Softmax Paper's First Version Against Its Third, the Errata It Added, and the Papers It Credits

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

## 1. The question

"A Fix for Softmax and Cross-Entropy" (arXiv:2610.31642; the author block names Google DeepMind) was posted on 22 October 2026 (v1, 10 pages) and revised on 29 October 2026 (v3, 10 pages; v2 was not seen). It argues that standard softmax, log-softmax and cross-entropy have two numerical bugs: "Softmax Collapse" (once the target logit's margin exceeds a precision cliff, the target gradient rounds to exactly zero while the others do not, so gradients stop summing to zero) and "Softmax Cancellation" (in soft-target distillation, subtracting two nearly equal softmaxes leaves a non-zero gradient even when student and teacher logits are equal). It gives log-space replacements, with JAX code, and reports that they remove "Slingshot" loss spikes in grokking experiments, speed up grokking, stop distillation drift and show that margins settle near log(1/epsilon) under AdamW. This draft asks three things of the two versions and of the works around them: what changed, whether the paper's central numerical claim holds when its printed code is run, and what the changes say about where its explanation and its code came from.

## 2. What was read, and how

- Both versions as text layers (v1 and v3 PDFs, not stored here), compared sentence by sentence (`vdiff.py`; 125 sentences in v1, 133 in v3, 66 identical after normalisation; the rest are the changes below).
- The paper's printed JAX snippets, transcribed and run offline on CPU JAX (`checks.py`). This runs the code printed in the paper; it is not the authors' internal codebase and no training experiment was re-run.
- Four works the paper credits, fetched from arXiv: a May 2026 paper on Slingshot spikes (arXiv:2605.06152), an independent report on softmax and cross-entropy testing posted on 27 October 2026 (arXiv:2610.36427, which v3's Errata credits), the 2025 paper that named Softmax Collapse (arXiv:2501.04697) and a Flash Attention analysis (arXiv:2510.04212). Abstracts and introductions of all four; the report in full; the bodies of the other three not read in full.
- Predictions were fixed before each part was opened (`predictions_fixed_2026-11-13.md`): ten about the version change, ten about v3 and eight about the credited works. Same-source note: the reader is an Anthropic model and the paper is a Google DeepMind paper; no model from the assisting model's developer appears in it. The authors are called "the authors"; the report's author is not named here.

## 3. What did not change (E2)

The title; the abstract (punctuation only); the cliffs (about 5.5 in bf16, 16.6 in fp32, 36.7 in fp64) and the margin equilibria (18.4, 27.6, 36.8); the two comparators (a zero-sum gradient projection and a surrogate activation); the experiments' tasks; the page count; and the conclusion's own limit, which says the extreme margins and near-zero student-teacher gaps probed "are uncommon in standard large-scale training".

## 4. Predictions scored (post hoc, one reader)

Version reading: 1 held, 4 partial, 5 missed. The misses are the instructive ones: I expected the title and the fix to be unchanged and a scope sentence to appear; the title and abstract are unchanged and the fix changed. Evaluation of v3: 5 held, 3 partial, 1 held in part, 1 missed. Credited works: 7 held, 1 partial. The full table is in `predictions_fixed_2026-11-13.md`.

## 5. What changed from v1 to v3 (E1 for the strings, E3 for the reading)

1. **An Errata was added.** It reads: "In an earlier version of this paper, the code in Section 2 produced NaN gradients when all but one logit was effectively −∞, as happens with masking in causal attention or with extreme logits." It continues: "This bug was not present in our internal codebase, which produced all results in this paper." It attributes the printed-code bug to "an over-eager agent" that simplified the code, and credits an external reader.
2. **The printed implementation changed.** In v1 the hard-target loss and log-softmax used a log-sum-exp over the logits with the maximum masked to minus infinity, then softplus; in v3 they use an exponential sum then log1p, with an exact-zero shift at the target. In float64 the versions agree with softplus(-m) at margins 1, 10 and 30.
3. **The soft-target method changed.** Equation 9 gained a fallback (when the log-ratio is at least 1 in magnitude, use q minus p directly, to avoid zero times infinity) and the printed code gained the matching branch.
4. **Attribution was added.** v1 said: "These Slingshot spikes are a direct consequence of Softmax Collapse (Section 2)." v3 says the same sentence with two citations appended (the May 2026 paper and the 2025 paper that named the effect), credits the 2025 paper in its abstract with identifying Softmax Collapse, and cites a Flash Attention analysis for the standalone-softmax case and a numerical-analysis reference for log-sum-exp.
5. **Numbers and wording were corrected against the paper's own table.** The Table 1 caption went from "5 seeds" to "3-5 seeds"; the text from "99-100%" to ">=98.9%" (the table's minimum for the fixed loss is 98.9); one comparator's margins from 10^3 to 10^4 to about 10^4; the fp32 distillation result from a brief KL spike to an initial KL spike and a floor near 10^-6. The sentence "This plateau has nothing to do with fp32 precision" was dropped.
6. **New text on experiments.** Hyperparameters for the four grokking benchmarks (weight decay 1 for the two transformers, 0.2 for the two MLPs); a described weight-decay-0 panel of the margin-equilibrium figure (the figure itself not inspected); the epsilon = 0 trajectory keeps growing until the fp32 gradients underflow at a margin of about 81.2.

## 6. The independent report and the works credited (E1/E2)

- **The Errata is confirmed from outside, and the timeline is checkable.** v1 22 October; a public post by one of the authors on 23 October (as dated in the report; not read here); the report 27 October; v3 with the Errata 29 October. The report finds that, for a float64 input of [1.7976931348623157e308, -9.9792015476736e291], the max-shift overflows the second entry to minus infinity, the log-sum-exp excludes the maximum and sees an all minus-infinity vector, and the backward pass gives NaN; it proposes the exponential-sum-plus-log1p replacement that v3's printed code now contains. I reproduced its table with the printed code: on that input and on [1e308, -1e308] the standard softmax gives an all-zero Jacobian, v1's printed softmax gives all NaN and v3's gives all zero.
- **The explanation of the Slingshot spikes predates v1.** The May 2026 paper (first posted 7 May 2026) "proves that this phenomenon is a result of floating-point arithmetic precision limits": the target-class gradient is rounded to zero, the others are not, the zero-sum constraint breaks, and a drift follows. v1 cites that paper for its zero-sum projection comparator and states the same causal link in its own section on the Slingshot mechanism without a citation; v3 adds the citation. The 2025 paper named Softmax Collapse and proposed an activation and an optimiser as remedies, not a rewrite of cross-entropy.
- **What the paper adds relative to them:** the log-space implementation, the soft-target (Cancellation) bug, the margin-equilibrium result under AdamW, and the precision-by-epsilon grid.
- **A statement about AI use that sits outside the paper.** The report says the authors "claim that these issues were found and fixed using Gemini Flash 3.7", citing the public post. Neither v1 nor v3 mentions a language model in its method or acknowledgements (searched); the Errata mentions an agent only as the likely source of the printed-code bug. I did not read the post.

## 7. What holds (E1)

Every closed form recomputes: the cliffs are the number of significand bits times ln 2 (5.545, 16.636, 36.737), and the equilibria are log(1/epsilon) (18.42, 27.63, 36.84); the independent report derives the same thresholds. Every output the paper prints for its worked examples reproduces exactly when v3's printed code is run: at z = [9, -9, -9] in fp32 the standard implementations return 0.0 for the target log-probability, loss and gradient, and v3's return -3.046e-8, 3.046e-8 and a gradient that sums to zero; the soft-target example gives the printed standard gradient [-5.960e-8, 1.452e-8, -1.123e-9] against v3's [-4.596e-8, 4.144e-8, 4.513e-9], and an exact float64 q minus p gives the same values as v3. At fp32 margins of 20, 40, 60 and 80 v3's loss and target gradient equal e^-m to printed precision while the standard implementation returns exactly 0. The central numerical claim is correct and demonstrated by the paper's own code.

## 8. Flags (ranked; post hoc; leads, not verdicts)

1. **The printed code in v1 was not the code that produced the results, by the authors' own account, and it failed on two classes of ordinary input.** Masked attention rows and finite extreme logits gave NaN gradients. An outside reader found it within five days and the authors disclosed it, with a plausible account of the cause. The account (internal code correct, an agent's simplification the source) cannot be checked from the paper. (E1 for the failure; E3 for the cause.)
2. **An explanation presented as the paper's own had been proved and posted months earlier by a paper it cites for something else.** The paper's own contribution survives (flag text in section 6), and v3 corrected the omission. It is the kind of omission a version-to-version reading can see and a single reading of v3 cannot. (E2.)
3. **AI involvement is disclosed in two places and neither is the paper's methods.** One is the Errata (an agent, as a source of error); the other is a public post quoted by a third party (a model, as the discoverer and fixer). For a paper whose subject is a bug found and fixed, where that is stated matters to a reader judging the work. (E2; the post not read.)
4. **The evidence is synthetic and the scope limit sits in the conclusion.** Modular-arithmetic grokking on small transformers and MLPs, a precision grid on one task, a distillation test; the abstract's wording ("Standard implementations of softmax, log-softmax, and cross-entropy have two numerical bugs"; "eliminates the previously-observed") reads as general. (E2.)
5. **The cost claim is unmeasured.** The conclusion says the functions "can be implemented without meaningful slowdown"; no timing or memory figure appears. (E2.)
6. **No release statement, and the experiments cannot be re-run from the paper.** The printed snippets reproduce the worked examples (done here); the training runs cannot be rerun. Table 1's seed count moved from "5 seeds" to "3-5 seeds". (E2.)
7. **One citation I could not support.** v3 cites the Flash Attention analysis for the standalone-softmax backward-rounding case; that paper is about attention in low-precision training and a text search found no such statement. The source may be elsewhere or in a part not read. (E1 for the search; E3 for the paper.)

## 9. What this does and does not establish

- It establishes what two versions, their printed code and four credited works support, with the code run for the examples. It does not establish that the training results are right or wrong, what the authors' internal code is, or anything about intent: a corrected omission, a disclosed bug and an added citation are what careful revision looks like, and the Errata is candid.
- One reader, post hoc on the changes; predictions were fixed before each part was opened and that order is the evaluator's own record.
- v2 was not seen; the bodies of three of the credited works were not read in full; the public post was not read; no training run was repeated.

## 10. What would change this

The authors' internal code (flag 1's cause); the public post (flag 3); v2 (whether the Errata and the attribution changes arrived in one step); a second reader.

## 11. Reproduction

`predictions_fixed_2026-11-13.md`; `checks.py` and `checks_output.txt` (needs CPU JAX and optax; six parts: closed forms, the paper's printed examples, the Errata inputs, v1 against v3 on the Hard-target loss, fp32 large margins, and the independent report's inputs); `vdiff.py` (sentence-level diff of two text layers); `quote_checks_output.txt`; `tool_scan_*.json`. PDF hashes (sha256, first 16 hex): v1 782c5b90c760ecec, v3 03e2274d2bff9ffd, the May 2026 paper (v1) a3d8159e5cba550e, the report 3bebe5a0bd639730, the 2025 paper 78794cb04751f5b1, the Flash Attention analysis 4b5a3040fa117ac1.

## References

Sources: arXiv:2610.31642 (v1, v3); arXiv:2605.06152 (v1); arXiv:2610.36427 (v1); arXiv:2501.04697 (v2); arXiv:2510.04212 (v4). Related, in this series: `dream_rsi_versions_reading_v1.md` (a version-history reading), `papers/published/rsi_gate_audit_results_v1.md`.

## Revision log

- *2026-11-13, v1.* Added to the repository as a draft.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
