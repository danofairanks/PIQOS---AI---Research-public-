# Recall Without Precision, Graded by the Builders: Reading the Paper Assistant Tool

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** One paper, "Towards Automating Scientific Review with Google's Paper Assistant Tool" (arXiv:2606.28277v1, 26 June 2026; the paper names Google Research and, for one author, Carnegie Mellon University). The authors are called "the authors"; the paper quotes three named academics in its pilot feedback, and none is named here. No intent is attributed to anyone.

**Disclosure.** AI-assisted (Claude, working under this project's own non-default standard; direction, selection and release decisions are the operator's); single reader. The paper's pipeline uses Gemini models only; no model from the assisting model's developer appears in it. Read from an operator-supplied copy (10 pp.; PDF sha256 beginning 8f201a8abd61b3f1) via text extraction: the full text and Tables 1-3; Figure 1 by caption only. The blog posts the paper cites for the pilots, the SPOT benchmark paper, the survey instrument, and any code or prompts were not read (none is released). Reading lens: the series overview, plus the five questions added on 2026-11-09. Predictions were fixed before the body was read (`predictions_fixed_2026-11-09.md`).

## What it is
A four-stage review agent (segmenter, adaptive budgeting, deep review agents on Gemini Deep Think, a synthesis agent that de-duplicates and grounds with search) for math and CS manuscripts, a four-role taxonomy of AI in peer review, and two claims: recall of the ground-truth error on a filtered SPOT subset (26 papers, 29 equation or proof errors; original SPOT best 21.1%, zero-shot Gemini 3.1 Pro 55.2%, PAT 89.7%, "a 34% improvement"), and opt-in author pilots at STOC (n = 124 respondents) and ICML (n = 733) among "over 4,700 submissions".

## Flags (ranked; post hoc)
1. **The benchmark result is recall alone, on 29 errors, and the "34%" is points.** 26 of 29 against 16 of 29 (95% Wilson intervals about 74-96% and 38-72%; ten more errors found); 34.5 points, a 62% relative gain; unpaired Fisher exact p about 0.007, and paired outcomes are not reported (C1). The text argues that multiplying compute raises recall and degrades precision, then reports no false-positive rate on SPOT or anywhere. A report that lists many issues passes a grader that asks whether any one matches the ground-truth error, so recall also rises with report length and budget. (E1; recomputation E1)
2. **Method and compute are confounded.** PAT spends adaptive, larger compute with a synthesis stage; the baseline is one call. The design section names Pass@k as the obvious alternative and the paper never runs it, nor a budget-matched vote. (E1)
3. **The grader and the subset belong to the authors.** The authors replaced the benchmark's strict keyword grader with their own "logic-aware" LLM grader (model not named), audited by one author, and filtered a benchmark they describe as dominated by multimodal errors down to math and CS "Equation / proof" errors. They say the numbers are not comparable with the original 21.1% yet credit the jump from 21.1% to 55.2% to newer models and the grader without separating the two. Table 2 reads "PAT (Gemini 3.1 Pro)"; the pilots ran an advanced Gemini 2.5 Deep Think, and the text says Deep Think "or another proprietary inference-scaling pipeline", so which system produced 89.7% is not pinned down. Whether the subset and grader were fixed before the runs is not stated. (E1)
4. **From documented errors to "would have caught".** "More than half of the errors in these retracted papers would have been caught" and "nearly all" are recall on papers whose errors were already found and published; there is no false-alarm rate on correct papers and no contamination check (a text search for contamination, leakage and training data finds nothing). (E1/E2)
5. **The pilot evidence is self-selected and self-reported.** Voluntary surveys; no response rate (857 respondents against "over 4,700 submissions", different units, at most 18.2%); no control group; no independent check that flagged items were errors or that fixes helped. By the authors' own table 44.2% (STOC) and 35.2% (ICML) did not say the feedback was mostly or all grounded, which the paper reads as "a strong positive result". Five reported percentages cannot be produced with the stated cohort sizes (STOC 85.1, 75.2, 55.8 and 11.6; ICML 35.4) but fit denominators of 120-121 and 732, consistent with unreported item non-response (C4). (E1/E2)
6. **Table 1 is partly an estimate.** Sums and growth rates recompute (C2), but 40.2% of the 2026 combined total is the NeurIPS figure, extrapolated from the 2024-2025 growth rate, one count is cited to a social-media post, and the 21% AI-generated-review share is a detection vendor's blog figure cited without a caveat on detector accuracy. (E1/E2)
7. **The Role 4 argument supports the statement that human review is noisy, not that AI review is better.** The 23% disagreement against 35% under random selection at 22.7% acceptance recomputes (C3); no figure is given for the consistency or accuracy of AI acceptance judgments, and PAT produces no ratings. (E1/E2)
8. **Builders, engine, baseline, grader and audit come from one organisation, and the tool is proposed at three points of one loop** (authors pre-clear, reviewers assist, a repository ranks by tool survival). The conclusion names gaming, deskilling and bias as open issues, not as that loop. (E2)

## What holds
The paper says plainly that recall without precision is incomplete and why; it states that its numbers are not comparable with the original benchmark; a human audited the grader's outputs; it flags that tools for authors can mask obvious issues and that accuracy against human reviewers must be shown before Role 3 or 4; the survey table shows cohort sizes; Table 1 cites its sources and its arithmetic holds.

## Scorecard against the predictions
9 of 13 held (one-run and no-intervals recall; single-call baseline only; opt-in self-reported pilots; Table 1 estimate; conceptual taxonomy; anecdotal critical errors; builder-run evaluation; no code or prompts; referee-control stance not measured), 2 partial (whether design was tuned on SPOT is not stated; gaming gets one clause and injection and confidentiality none), 2 missed (contamination is not acknowledged; no non-Google model appears). Detail in `predictions_fixed_2026-11-09.md`.

## Evidence tier and deeper-pass flag
**Tier:** E1 executed (intervals, tests, Table 1 and survey arithmetic in `checks.py`); E2 read (all 10 pp.; the cited blog posts, the benchmark paper and the survey instrument not read); E3 interpretation (flags 3 and 8 readings of how the design produces the numbers).
**Deeper pass:** recommended and cheap if the authors release material: precision and false alarms on error-free papers, a Pass@k with voting at PAT's budget, the grader named with a second grader from another vendor. Not done.

## Limitations: what this does and does not establish
- One reader; the flags are leads tied to a page or table, not verdicts, and a paper may answer them in places not read.
- It establishes what the paper's tables and text support. It does not establish that PAT misses or invents errors, or anything about the tool's behaviour; no code was available.
- The number of flags is not a severity ranking (see the series overview).

## Reproduction
`predictions_fixed_2026-11-09.md`; `checks.py` and `checks_output.txt`; `quote_checks_output.txt`; `tool_scan_*.json`. PDF sha256 8f201a8abd61b3f19fea2f60812265b47e08dadc2729c18830dde441fcd772f3. Predictions were fixed before the body was read; that order is the evaluator's own record and is not independently timestamped.

## References
Sources: arXiv:2606.28277v1 (PDF sha256 8f201a8abd61b3f19fea2f60812265b47e08dadc2729c18830dde441fcd772f3); numbers in `checks.py` are typed from its Tables 1-3 and text.

## Revision log
- *2026-11-09, v1.* Added to the series.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
