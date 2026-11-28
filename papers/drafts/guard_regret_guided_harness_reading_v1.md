# A Guarantee on the Gate's Own Objective: Reading a Self-Improving-Harness Paper's Non-Regression Claim, Its Headline Row and Its Cost Accounting

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

## 1. The question

"GUARD: Stabilizing Recursive Self-Improvement with Regret Guidance" (arXiv:2611.23476v1, cs.AI, 17 November 2026, 38 pages; the author block names Google Cloud) describes a method for improving an AI agent after deployment by editing its *harness* (prompts, skills, tool rules, memory) while the underlying model stays frozen. Its abstract says [1] that the method "consistently improves performance without catastrophic forgetting or memory pollution", that a gate promotes an edit only when gains outweigh regressions "guaranteeing non-regression on its gated buffer", and that it is "substantially cutting deployment token usage".

This reading asks three narrow questions that a non-specialist can check against the text: **what does the guarantee cover, what exactly is the headline result row, and which cost does the token claim measure?** It does not ask whether the method is a good idea.

## 2. What was read, and how

- The paper's text layer (PDF not stored here; sha256 in `quote_checks_output.txt`): the abstract, the introduction, the problem formulation, the self-review construction (Section 4.1), the algorithm and the statements of the two theorems and the proposition, the conclusion and its summary table, the results sections, Table 2 and its caption, the caption of the continual-stream table (Table 3), the appendix proofs and cost accounting, the appendix setup (including its release statement) and the evaluation protocol, and the appendix ablation paragraphs and table captions. In v1.1 the read was extended to Tables C.4 to C.8 in full, the prompt-template boxes (B.1 to B.4) and the paragraph on adaptation complexity and runtime, and the absence statements below were re-checked by searching the whole text layer and the PDF's link annotations. **Not read:** the figure panels (graphics only) and prompt-template text outside Boxes B.1 to B.4. The reference list was not checked. No code or data were fetched; the text and the PDF's link annotations were searched for a code or data link (section 5.9).
- Arithmetic on printed numbers and printed statements (`checks_arithmetic.py`, standard library only; 11 checks, all pass), and in v1.1 a recomputation of the table numbers in sections 5.7 and 5.8 (`checks_appendix_ext2.py`).
- Thirty-three quoted strings and twenty-nine cited numbers were checked against the text layer (`quote_checks.py`; 33 of 33 and 29 of 29 found).
- Predictions were fixed before the paper was opened (`predictions_fixed_2026-11-26.md`), from a one-line description, again before the coverage extension (`predictions_fixed_coverage_extension_2026-11-27.md`), and again before the v1.1 appendix extension (`predictions_fixed_appendix_extension_2026-11-28.md`, with its scoring).
- Same-source note: the reader is an AI model from a different company than the one in the author block. The paper's second model setting (section 5.5) uses a model from the reader's own company as the reviewing and distilling model. This is a reading, not a referee report.

## 3. What holds (E1)

- The printed numbers agree with each other: 59,651 against 131,032 tokens per task is a 54.5% reduction; 167.6 against 158.8 minutes is within 6%; 233.8 seconds per task follows from 167.6 minutes over 43 tasks; the 8× factor in Theorem 1(iv) follows from its formula; and a paired exact sign-flip test with 8 tasks better and none worse gives p = 0.0078, matching the printed p = 0.008 (`checks_arithmetic.py`).
- The proofs read are algebraically sound as printed: the lower bound in Theorem 2(i) holds for a grid of (J, ε) values by exact summation; the identity behind the proposition holds; the proof of Theorem 1(iii) states its independence and sub-Gaussian assumptions.
- The paper states its own caveats about the guarantee in the text of Theorem 1 (section 5).
- The paper reports a comparison of its self-review scores with the benchmarks' own labels (section 5.6), which is an independent check of its own proxy.

## 4. Predictions scored (post hoc, one reader)

| # | Prediction | Result |
|---|---|---|
| P1 | A formal-model treatment of controllability, not an empirical study | MISS: an empirical method on real agent benchmarks with theorems about its own gate; the word controllability does not occur in the paper |
| P2 | Central result conditional on stated assumptions the abstract omits | PARTIAL: the theorems state assumptions; the abstract keeps "on its gated buffer" |
| P3 | The headline conclusion follows from the paper's own definition with no independent test | PARTIAL HIT for the guarantee (section 5.1); the benchmark scores and the calibration against official labels are independent tests |
| P4 | Empirical section is toy or small-scale | MISS: real agent benchmarks; the continual-stream result is one seed |
| P5 | A limitations or discussion section, shorter than the results | MISS: none found by text search |
| P6 | A flaw shared by controller and improver is not addressed | HIT: no discussion found by full-text search (v1.1) |
| P7 | A headline step rests on an external or unverified citation | HIT: benchmarks and baselines are cited, not checked here |

Predictions fixed before the coverage extension (E1 to E7):

| # | Prediction | Result |
|---|---|---|
| E1 | A code or data availability statement exists | HIT as a plan: the appendix says the authors plan to release reference code, checklist self-reviewers and prompt templates, subject to approval; no link was found |
| E2 | A table beyond Table 2 reports a spread for a headline cell | HIT: confidence intervals and replicate standard deviations on the professional suites; a three-pass spread for the unchanged initial harness |
| E3 | Removing a component lowers the headline on some benchmark and not on another | PARTIAL: removing the regret-ranking stage and removing the gate each lower the macro accuracy; no removal that left it unchanged was found in the parts read |
| E4 | A measured adaptation-time cost is reported | MISS by full-text search (v1.1): an asymptotic count, and a measured test-time wall-clock only |
| E5 | How the final configuration was chosen is stated | PARTIAL: all five configurations and their scores are listed, and the paper names the components that changed between the initial and final runs (section 5.3); the choice of the reported one is not described |
| E6 | A caveat on shared reviewer-and-solver flaws appears | MISS by search |
| E7 | A table shows the method not beating the best baseline somewhere | HIT: an interval that includes zero, domains where the method abstains, a trade-off on one strict metric, and (v1.1) a continual stream where its final mean is below three prior methods (section 5.7) |

## 5. Findings (E1 for quotations and arithmetic, E2 for reading; leads, not verdicts)

**5.1 The guarantee covers the gate's own objective, on recorded scores.** The paper's own wording is in two places. The abstract says the gate guarantees "non-regression on its gated buffer"; the conclusion says "formal non-regression guarantees on the self-review objective". The proof of Theorem 1(i) says the increments telescope because "The incumbent score used by the gate is the score recorded when the incumbent was itself evaluated". Read plainly, a candidate is promoted only if its recorded score on the buffer does not fall, so the recorded score cannot fall. The objective is a checklist that the model itself derives once from the task prompt, the tool declarations and the schema: the paper says the self-reviewer "reads only the task prompt, visible tool declarations, and schema once at Turn 0". One layer of grading "checks execution predicates deterministically on an ephemeral sandbox copy", the other "grades semantic predicates individually" with a model call. The paper says [1] it adds two limits in the text of Theorem 1: the statements "hold within each round’s gated task buffer rather than telescoping unconditionally across distribution shifts", and the concentration bound is "rather than a non-vacuous finite-sample certificate at our benchmark task counts". So the continual-stream result ("zero post-block forgetting" under hidden drift) is empirical, not implied by the theorem.

**5.2 Theorem 2 carries its conclusion in its assumptions.** It compares a passive learner with a targeted one and concludes that dense checklist grading removes a 1/ε penalty. The comparison depends on assumptions including that "every unresolved invariant fails a derived criterion" and that resolved invariants stay resolved. That says: if the derived checklist covers the invariants and repairs persist, targeted repair beats passive discovery. The theorem does not say how likely coverage is for a checklist the same model derives. Proposition 1 is an identity on the priority formula, with no performance content.

**5.3 The headline row is the best of five configurations.** The Table 2 caption says [1] "The GUARD row is the final of five hosted configurations evaluated on this test split", with "mean 77.09%, range 75.57–80.80%; all five above every baseline" [1]. The table's 80.80% [1] is the top of that range. The appendix says the five are: the reported main arm, "its original-distiller control at 75.57%", "the initial one-layer run at 75.98% in Table 4", a fixed-persona variant at 76.69% [1] and a four-candidate pool at 76.42% [1]. Four of the five are therefore a control, an earlier one-layer run and two variants, not repeated draws of the same method, and the paper discloses all five scores. The paper also says the final hosted configuration differs from the initial one-layer run in three named components (two-layer review, cumulative-source gating and a completeness-first distiller instruction), so the configurations are design iterations on the same test split; how the reported one was chosen is not described anywhere in the text layer (searched in v1.1). Against the best prior-method row (74.52% [1]) the gain is 6.28 points for the headline row and 2.57 points for the five-configuration mean (arithmetic on the printed numbers [1]). The caption reports exact sign-flip tests over the 43 paired tasks: significant against the initial harness (8 tasks better, none worse) and two prior methods, "p = 0.11; 95% bootstrap CI [−0.4, +14.5]pp" against the strongest. The abstract does not carry the five-configuration mean or the range.

**5.4 The token figure is test-time tokens of the final row; adaptation cost is accounted asymptotically.** The conclusion says "cutting hosted tokens per task by 54.5%", and the abstract says "deployment token usage": a deployed harness runs in a single pass with no reviewer calls. Part of the saving is attributed in the text to the final configuration reaching no eight-step budget exhaustions where the baselines and the initial harness had several. The appendix gives adaptation cost as an asymptotic count (rollouts and additional model calls for the semantic grading layer); the measured runtime given is test-time (43 test tasks in 167.6 minutes against 158.8 for the unchanged initial harness and 439.4 for one prior method); no measured adaptation-time total for the method against its baselines was found by searching the whole text layer for cost, wall-clock and token terms (v1.1). Token figures for the other four configurations were not found.

**5.5 Reviewer and solver are the same model in the primary regime; the paper's other settings do not address shared flaws.** The headline experiments are labelled as a single-model setting. The appendix adds a cross-model setting in which one company's model is the agent and a different company's model "serves as distiller, self-reviewer, critic, and rubric judge", and two suites "in which solver, distiller, critic, and grader all use the exact same model", said to be run so that the gains do not rest on a stronger teacher. The paper does not frame either as a test of flaws shared by reviewer and solver, and a search for bias, correlation, sharing and self-preference language found no such discussion; the word "limitation" does not occur anywhere in the text layer, so there is no limitations section. A flaw the reviewer cannot see is invisible to the gate in any setting, by Theorem 2's assumption about derived criteria. The paper does not say which calculations or text were AI-assisted; no statement was found by search.

**5.6 The paper's contact with an external grader is moderate by its own numbers.** The conclusion reports [1] that tasks failing the first (execution) grading layer score 45.97% [1] on the official labels against 73.90% [1] for tasks passing it, on 4,059 test tasks [1] (82.6% [1] negative predictive value), and a within-family concordance of 82.2% [1] on 169 playbook pairs (75.6% [1] on non-tied pairs), with a reported correlation of 0.369 [1] in a calibration. This is real evidence, measured against labels outside the method, and it measures agreement of scores, not coverage of the invariants the checklist must catch.

**5.7 One seed for the continual-stream headline, with a spread reported elsewhere.** The appendix says that "Held-out evaluation draws one rollout per task" and gives "360 adaptation / 360 held-out test rollouts per arm" for the continual streams; the run is labelled "seed 42" and no interval for the method itself was found. The paper does give a spread for the unchanged initial harness re-sampled three times ("69.86% ± 0.18pp" [1]), small against the reported gains, and it reports bootstrap confidence intervals and replicate standard deviations on the professional suites, where one interval ("the 95% CI [+0.00, +31.25] touches 0") includes zero. The hosted benchmark has paired tests, as above. Table C.4 reports the four continual streams with one run per stream and 30 held-out tasks per group (so a difference of 1 to 5 points is 1 to 2 tasks per group): the method's final mean is the sole best in one stream (the four-group compound stream, by 0.84 points, one held-out task of 120), ties the best prior method in two (70.00% [1] in the two-group and three-group streams), and is below three prior methods in the domain-drift stream (78.69% [1] against 79.31% [1], 79.29% [1] and 79.17% [1]). The recomputation is in `checks_appendix_ext2.py`.

**5.8 The ablations support the gate on the paper's own scores.** The appendix says that removing the regret-ranking stage "reduces five-domain macro accuracy by −7.33pp" and that promoting the top candidate without the gate "drops five-domain macro accuracy by −10.35pp", with, in one domain, "an unvetted Stage-v4 candidate instructs a hallucinated MCP tool call"; the full method, it says, "maintains 0/5 regressed domains" [1] (it also abstains on two local domains and reports "with a minor trade-off on strict all-or-nothing solve rate" in one). Table C.7 prints 65.81% [1] macro accuracy for the unchanged initial harness and 66.46% [1] for the full method, so the method's own gain over the initial harness on these five domains is +0.65 points (macro strict-solve 37.73% [1] to 38.31% [1]); the ablation drops above are measured from the full method and are −6.68 and −9.70 points from the initial harness. Three of the five domains end equal to the initial harness (two by abstention, as the caption says; one after a promotion returned to the initial harness at a later stage, per the Table C.6 footnote), and the strict-solve rate in one domain falls from 30.56% [1] to 25.00% [1] (Table C.5). These are measured with the benchmarks' own scoring, which is also how the method is evaluated; they show the gate prevents bad promotions there and do not test how well the derived checklist covers the invariants that scoring penalizes.

**5.9 Code and data are planned, not linked.** The appendix says "we plan to release reference harness code" and describes the release as "subject to approval"; no link to code or data was found in the text, and the only link annotation in the PDF is the arXiv abstract page.

**5.10 The promotion count includes ties.** The Table C.6 footnote reports gated promotions with a held-out change of at least zero in "19/19" [1] cases, of which "15/19 strictly > 0" [1]; four are ties at +0.00 points. For the critic-scored suite the same footnote says there is "no gate-discrimination signal" (all 24 round winners admitted).

## 6. What this does and does not establish

It establishes what the guarantee covers (the self-review objective on recorded scores within a buffer), that the headline accuracy is the top of five configurations evaluated on the same test split, and that the token claim is a test-time measurement. It does **not** establish that the method fails or that its held-out gains are not real: against the initial harness the paired result is significant, the ablations support the gate on the benchmark scores, and against the strongest prior method the paired result is not significant. The mathematics was checked only as printed identities and bounds; the figure panels and the reference list were not read; nothing was run, and no code was available.

## 7. What would change this

- Run-to-run variation for the method itself on the continual-stream suite (a spread is reported for the initial harness only).
- A measured adaptation-time cost (tokens or dollars) for the method and its baselines.
- A check of whether the derived checklists cover the invariants that the benchmarks' own scoring penalizes.
- A statement of how the reported configuration was selected, and results for a test split not used in choosing it.
- A discussion of shared flaws between reviewer and solver, with a test designed for them (the paper's cross-model and same-model suites address teacher strength).
- The planned code release, so that the checks above can be run.

## 8. Reproduction

`quote_checks.py` (needs the paper's text extracted with `pdftotext` in default reading order; sha256 of the PDF in `quote_checks_output.txt`), `checks_arithmetic.py` (standard library only; output in `checks_arithmetic_output.txt`), and the three scanner outputs (`tool_scan_*.json`) of this repository's own tools on this file.

## References

- [1] arXiv:2611.23476v1 [cs.AI], 17 November 2026 (38 pages).

## Revision log

- v1, 2026-11-27: first staging copy.
- v1.1, 2026-11-28: read extended to Tables C.4 to C.8, Boxes B.1 to B.4 and the runtime paragraph; absence statements (adaptation cost, seed, final-configuration choice, shared flaws and limitations, code link) re-checked by full-text search and all stand; sections 5.3, 5.4, 5.5, 5.7, 5.8, 5.9 extended; new section 5.10; predictions file and recomputation script added. No earlier statement was withdrawn.
- v1 staged in the public drafts folder on 2026-11-27; the paper's arXiv listing showed v1 only that day and the fetched PDF matched the one read (same sha256).
