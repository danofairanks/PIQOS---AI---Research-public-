# Reading a Self-Improvement Paper Against Its Own Counts: DiscoveryRSI, Its Two Repositories, and Where the Gain Sits

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

## 1. The question

A preprint ("DiscoveryRSI: Recursively Learning to Discover Valuable Hypotheses", arXiv:2610.23839v2, 20 October 2026, 40 pages) reports a model that learns from its own research histories. Its abstract says mean hypothesis quality rises "from 4.86 for the base model to 5.39 after two rounds of self-improvement", that human reviewers see "greater human-rated improvement along research paths", and that the model has "a 6.3% rate of hypothesis correspondence with research published after the model cutoff" and "largely outperform[s] GPT-6 with 2.5% and Claude Opus 5 with 2.3%". Two public repositories accompany it. This draft asks what the paper's own tables support, where the headline numbers get their size, and what the repositories can and cannot reproduce.

## 2. What was read, and how

- **The paper**, v2 (the abstract page lists a v1 submitted 16 October; v1 was not read and v1 to v2 was not compared). Coverage as recorded on 2026-10-21: pages 1 to 19 (main text), Appendix B, D.1 to D.3, F and parts of C. Not read: Appendix A, the rest of C, D.4 onward, and Appendix E beyond a keyword hit on its cohort paragraph. Figures were read only through their text layer.
- **Predictions** were fixed on 2026-10-21 after the title page, Figure 1 and the abstract, before the rest (`predictions_fixed_2026-10-21.md`). The date is the evaluator's own record, not independently timestamped.
- **Re-verification on 2026-10-23.** Every quoted string and count below was checked verbatim against the arXiv v2 PDF (sha256 `f9df65e4…a1bb0`) by `quote_checks.py`: 48 of 48 present. The repository statements were checked against single public files at the pinned commits by `repo_quote_checks.py`.
- **Repository runs were not repeated.** The test and demo results in section 7 were executed on 2026-10-21 in scratch copies of read-only shallow clones; the outputs were not stored with this draft.
- Evidence classes: **E1** executed or recomputed here; **E2** read; **E3** interpretation. One reader, an AI system from one of the labs whose models the paper compares (Anthropic, via "Claude Opus 5"). The Claude comparison below is arithmetic on the paper's own printed counts, so it does not depend on that reader's judgment, but the reading of everything else does.
- The authors are called "the authors". No intent is attributed. The paper was supplied by an operator, not sampled, so nothing here is a rate.

## 3. What holds

- **The accounting is careful.** Counts are printed for every comparison group, the weights are stated, and the appendices disclose most of the limits discussed below: judgments are "correlated AI perspectives, not three independent expert opinions"; human calibration "remains pending"; the weights are "frozen internal protocol conventions, not empirically established optimal weights"; the cutoff boundaries "do not identify internal model knowledge cutoffs"; and "a retrospective maximum over final-snapshot scores is monotone by construction and cannot demonstrate learning".
- **The composite reproduces (E1).** Rebuilding the eight-axis composite from the printed axis means and weights gives 4.862 and 5.385 against the printed 4.86 and 5.39.
- **The gain is where the paper says it is.** Section 7.1 states that improvements "concentrate on the specification of testable investigations" and that importance and novelty decline.
- **The counts are internally consistent (E1).** The four domain rows of Table 6 sum to 74 of 1,176.

## 4. Predictions scored

Seven predictions: **3 held, 3 held in part, 1 not determined.**

| Prediction | Result |
|---|---|
| The quality score is model-judged with a rubric overlapping the training signal | **Held in part.** One model family produces the score (three role prompts "to the same model family"). Overlap of the training critique rubric with the evaluation rubric was not shown in the parts read. |
| 6.3% vs 2.5% / 2.3% rests on small counts and carries no test | **Held.** Counts are printed (74/1,176; 59/2,341; 3/131; DeepSeek 14/257; GLM 1/36); Appendix F reports "descriptive percentages without significance tests". |
| Human evaluation is small and preliminary | **Held in part.** 292 proposals, 27 reviewers, three senior supervisors; the abstract says "Preliminary". Searches for an inter-rater statistic (inter-rater, kappa, Krippendorff, Cohen) found none. |
| Post-cutoff windows are not equalised across models | **Held.** Month-level proxies from April 2025 (Qwen-based) to September 2026 (DeepSeek). |
| "Recursive self-improvement" is two bounded rounds | **Held.** One epoch of fine-tuning per round plus harness edits accepted on a development set; the gain per round falls from 0.32 to 0.21. |
| Development and evaluation questions share a distribution | **Not determined.** No sentence in the text states whether the 241 evaluation questions are disjoint from the questions used to collect training trajectories (searched: disjoint, overlap, held-out). The paper describes "fresh questions for rediscovery" each round and development-set acceptance. |
| Code is linked; results are single runs without seed variance | **Held in part.** Links are given. The word "seed" does not occur; behaviour is measured over six campaigns of 20 episodes. |

## 5. Executed checks (E1; `calc.py`, arithmetic on printed numbers)

1. **The 6.3% comparison.** Naive Fisher exact tests, ignoring dependence between versions of one research family (which makes them generous): against GPT 2.5%, p < 0.001; against DeepSeek 5.4%, p = 0.67; against GLM 2.8%, p = 0.72; against Claude 2.3%, p = 0.076. Claude's 95% interval is [0.8, 6.5] and contains 6.3. The abstract names GPT and Claude and not DeepSeek, the nearest competitor.
2. **The Claude comparison is a retrieval comparison.** Appendix F.4 reports that 15 of 131 Claude proposals (11.5%) pass the lexical retrieval gate against 355 of 1,176 (30.2%) for the trained model, and that Claude's median proposal is 41,134 characters while retrieval reads the first 6,000. Among gate-passers the positive rates are 20.0% and 20.8% (3/15 and 74/355; Fisher p = 1.0). The paper says this in the appendix; the abstract does not.
3. **The pooled rate depends on one domain.** Therapeutic-target prioritisation is 15.1% of the trained model's versions and 40.5% of its positives (30/178 = 16.9%). Without it the rate is 44/998 = 4.4%. In clinical and population health, 13/557 = 2.3%, which Figure 10's per-domain panel shows below DeepSeek (5.2%), GLM (5.9%) and Claude (4.4%) in that domain and equal to GPT (2.3%). The other groups' domain counts are not printed, so a like-for-like pooled comparison cannot be made; the paper notes that "Group sizes and domain composition differ".
4. **The quality gain is in the testability axes.** With the paper's weights, the four axes I group as testability (falsifiability, data resolvability, feasibility, alternatives) contribute +0.608 to the +0.523 composite change; the other four (importance, novelty, grounding, actionability) contribute -0.085. Importance fell 6.48 to 6.04 and novelty 4.87 to 4.58 (weighted -0.146 together); falsifiability rose 4.00 to 6.20. The grouping is mine; `calc.py` prints all eight per-axis changes. Grounding and actionability values come from Figure 6's text layer; the other six are in the Section 7.1 prose.

## 6. Findings (E2/E3)

1. **The thing measured and the thing defined are the same list.** The paper's Definition 1 represents a hypothesis as a claim, an investigation plan, decision criteria and alternative explanations, and the judge scores falsifiability, alternatives and data resolvability. Training reinforces histories scored well on those, and those scores rise most. That is the signature of improving the measured parts of a definition. It is not evidence that the hypotheses became more valuable; the paper itself says the improvement "concerns investigation design more strongly than the perceived significance or originality of research questions". Whether the critique rubric used in training and the evaluation rubric overlap was not established.
2. **The literature comparison has several confounds beyond the retrieval gate.** The reference window runs from 1 April 2025 to 14 October 2026 and each group is filtered by its own cutoff proxy: Qwen April 2025 (the trained model is initialised from a Qwen model), Claude Opus 5 May 2026, GLM August 2026, DeepSeek September 2026. The group with the earliest proxy has the longest period in which to match literature, 13 months longer than Claude's. The semantic judgments come from one model, "GPT-6 Luna", 145 successful judgments from 149 sampled records, propagated to 903 versions; that model is in the compared GPT group, and I found no self-preference check (search: self-preference, favor, bias). The measure counts correspondence with later literature, not adoption: "Prospective tracking is needed."
3. **Absolute human ratings are mixed; the revision outcomes are the stronger result.** The trained model scores higher than GPT-6 Luna on importance (3.10 vs 2.94) and on plausible, evidence-bounded claims (3.37 vs 3.16), ties at 2.31 on advance over known work, and scores lower on data fit, alternative explanations and informative results. Revisions improve the mean human score in 41% of cases (12% worse) against 31% (32% worse) and 25% (31% worse) for the two comparison models. The per-revision means (+0.07, +0.03, -0.01) are printed without an interval in the parts read.
4. **"Recursive self-improvement" is a bounded loop.** Two rounds, one epoch each, accepted on a development set, diminishing gain. That is a sound engineering claim; the title's word carries more than the evidence.
5. **The abstract is the softest layer.** The comparative language ("largely outperform", "greater human-rated improvement") and the contribution line "Empirical evidence for learning from scientific research" sit above appendices that state narrower limits. This is a statement about where the caveats live, not about intent.

## 7. The repositories

**`github.com/Gen-Verse/DiscoveryRSI` at 7389e0b** (one commit, Apache-2.0; checked 2026-10-23: HEAD unchanged). Recorded 2026-10-21 from a read-only shallow clone (E2, with a local run): about 25 KB of Python, five tiny role prompts, six tests that pass, and a demo whose critic is a keyword rule, so it shows the wiring and cannot show research improvement. Of the paper's components, the repository has a propose/critique/select loop with a linear parent chain. It does not contain the evolve/repair/crossover/restart operations, blinded pairwise critique with TrueSkill, hypothesis credit optimisation, the 27B fine-tuning, harness replay and edit acceptance, compilation to executable tasks, or the literature audit. **None of the paper's numbers can be reproduced from it.** Its README (verified today) ranks "DiscoveryRSI-27B ... 6.3%, followed by DeepSeek (5.4%), GLM (2.8%), GPT (2.5%), and Claude (2.3%)" and contains none of the words gate, cutoff, window or retrieval. Its limitations section is plain: it "can produce plausible but unsupported claims".

**`github.com/Gen-Verse/DFM-Bench` at 224712b** (one commit; checked 2026-10-23: HEAD unchanged). Recorded 2026-10-21: 111 unit tests pass with a deterministic fake judge; a free smoke path runs end to end with no external calls and withholds scores. No root `LICENSE`, `LICENSE.md`, `LICENSE.txt` or `COPYING` and no licence text in `pyproject.toml` (checked 2026-10-23; other file names were not tried).

**How the benchmark describes itself (verified 2026-10-23).** `docs/EVALUATION.md`: "This is an **internal AI-reviewed preview**; human calibration is pending, and the scores do not establish scientific truth or verified discoveries", and "A maximum score increasing over episodes does not prove learning." `PROTOCOL-V1.json`: weight status `locked_internal_pilot_convention_not_validated`; `forbidden_claims` of `expert_calibrated`, `online_as_of_progress`, `confirmed_discovery` and `system_superiority`; release claim "no claim of completed human calibration, system superiority or verified discoveries".

**Tension, not contradiction.** The paper's contribution list and abstract use comparative and learning language. The benchmark's own protocol forbids the claim of system superiority for its scores. The paper's comparisons rest partly on the literature audit and human review rather than on benchmark scores, and its round-over-round scores compare final snapshots of different model versions, so the protocol's disclaimer does not apply one to one. The two documents are written to different standards, and the benchmark's is the stricter.

**Definition drift between documents.** The paper names its five objects hypotheses, revisions, development paths, research runs and scientific contributions; the benchmark names them hypothesis, transition, trajectory, campaign and discovery. A historical benchmark archive (`FIVE-LEVEL-PROTOCOL.md`, marked "Historical archive (2026-09-27)") defines the hypothesis level as a comparative preference, "(child wins + 0.5 ties) / assessable pairs", and says "no new absolute hypothesis scale is invented"; the paper's quality score is an absolute weighted score on 1 to 10. The archive is historical, but these are different quantities under one name. The archive lists "367 battery edge comparisons" for a pilot; the paper's battery panel reports "214 of 366 transitions". They may be different panels; not reconciled.

## 8. What this does and does not establish

- It does not show the paper's results are wrong. No model was run and no model result was tested.
- It does not show the engineering is careless; the accounting and the appendices are unusually candid.
- It shows what the abstract's comparisons depend on: a retrieval gate that Claude's long proposals mostly fail, a domain that supplies 40% of the trained model's positives, unequal windows, and a judge from a compared family.
- It shows that the quality gain sits in axes the definition and the judge share, so the number measures how well specified hypotheses became.
- Limits: one reader; the figure values used come from text layers; Appendix A, D.4 onward and most of C and E were not read; the repository runs were not repeated for this draft; v1 of the paper was not compared.

## 9. What would change this

Human-calibrated scores on the same hypotheses; a re-run of the literature audit with equal windows, a judge outside the compared families and an unconditional retrieval step; per-domain counts for every comparison group; training-seed variance; a statement of whether evaluation questions are disjoint from training questions; prospective tracking, which the authors themselves propose.

## 10. Reproduction

Everything is in `discoveryrsi_reading_v1/`: `predictions_fixed_2026-10-21.md`; `calc.py` and `calc_output.txt` (standard library only); `quote_checks.py` and its output (needs the arXiv v2 PDF and `pdftotext`; the PDF is not stored here); `repo_quote_checks.py` and its output (fetches single public files at the pinned commits). Counts and axis values were transcribed by hand from the PDF.

## References

Sources: the preprint arXiv:2610.23839v2 ("DiscoveryRSI: Recursively Learning to Discover Valuable Hypotheses", dated 20 October 2026) and the repositories `github.com/Gen-Verse/DiscoveryRSI` (7389e0b) and `github.com/Gen-Verse/DFM-Bench` (224712b). Every count, percentage and axis value in this draft is taken from the preprint's text, its Table 6, its Figures 6, 8 and 10 (text layer) or its Appendices D.1 and F, and is recomputed in `calc.py`; the repository statements are taken from the files named in section 7. Numbers were transcribed by hand.

## Revision log

- *2026-10-23, v1.* First version.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
