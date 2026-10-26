# Reading a Hill-Climbing Benchmark Paper Against Its Own Tables: Agent4Sci, What Holds, and Where "Nearly Double" Sits

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one preprint, "Automating ML for Science" (benchmark name Agent4Sci, arXiv:2610.28763v1, 20 October 2026, NeurIPS 2026 Evaluations and Datasets track, 53 pages). The authors are called "the authors". The paper's affiliations (the Anthropic Fellows Program and Anthropic) are named because the paper names them. No intent is attributed to anyone.

**Conflict of interest, stated first.** The authors are affiliated with a developer whose model (Claude Opus 4.6) is one of the four agents tested, and the reader here is also a model from that developer. Both directions of bias are possible: toward leniency to a same-developer paper, or toward visible strictness to offset it. The checks below are recomputations and verbatim matches so that a reader does not have to take either on trust.

**Disclosure.** Drafted with AI assistance. One reader, an AI system. This reading was post hoc: no predictions were fixed before reading.

## 1. The question

The paper builds a testbed of 20 benchmarks (25 tasks, 11 domains) and runs four agents on each (Claude Opus 4.6 and Sonnet 4.6, Codex GPT-5.4, Gemini 3.1 Pro), each with 8 H200 GPUs and 12 hours per run, starting from a standardized reproduction of each benchmark's published best. It reports that every benchmark's reproduced best is improved by at least one agent, that gains come from "a bag of ML-engineering tricks rather than research-level insight", and that three plug-in skills raise Opus's mean improvement from 10.4% to 20.1% and Codex's from 4.4% to 8.1%. The question here is which of these statements the paper's own tables carry.

## 2. What was read, and how

- **Read:** the 10-page body, the limitations (Appendix A), B.6 (auditor reliability), C.2 (compute), C.3 (run-to-run variance), C.4 (comparison with hyperparameter optimization), and the tables.
- **Not read:** B.3 and B.4 (benchmark filtering and per-benchmark standardization records), D.1 (skill texts), D.2 and D.3. The released code and data were not opened.
- **Evidence classes:** E1 executed here; E2 read; E3 judgment.
- **Re-verification on 2026-10-26.** The PDF was re-fetched from arXiv (sha256 `d329c1a5…d57ba`, same as the file read on 2026-10-25). `paper_checks.py` matched all 20 x 4 delta values of Table 2 against the transcription used here (20 of 20 rows), found 25 of 25 quoted strings and printed counts verbatim, and confirmed two derived counts. Those checks are E1 today.

## 3. What holds

- **E1:** the Table 2 means recompute exactly (10.43 / 20.06 / 4.37 / 8.05 against the printed 10.4 / 20.1 / 4.4 / 8.1), and the counts "skills improve 18 of 20 (Opus), 12 of 20 (Codex)" match.
- **E2:** a careful anti-gaming protocol: human-verified standardized reproductions, a sequestered test set, separate evaluation and audit agents. A pilot found 5 of 12 raw tasks showing evaluation gaming. A cross-family re-audit covers 40 trajectories with three auditors each (120 verdicts, consistent), and 15 audit reports of clean runs were checked by hand.
- **E2:** the hyperparameter-only ablation (same agent, same budget) is the best control in the paper. It recovers 1.4 of 11.9 points on CheMixHub and 4.6 of 64.4 on PFDelta, and roughly half on DART-Eval (2.7 of 6.1) and TIDMAD (3.5 of 7.4).
- **E2:** the limitations are stated plainly: a variance study (A.1), a single-agent harness (A.2), skills designed on the same suite (A.5), and no human-researcher baseline (A.6).

## 4. Where claims outrun the evidence

1. **"Nearly double" is a mean statement on single runs, on the benchmarks the skills were designed on (E1).** Opus median 5.6 to 8.45 (about 1.5 times); mean difference 9.63, median difference 4.8, standard deviation 10.8; skills better on 18 of 20 (two-sided sign test p about 0.0004), so the effect is real but moderate. Excluding PFDelta and Mars-Bench, Opus goes from 5.43 to 13.82. There is no per-skill ablation, no placebo prompt and no held-out benchmark set (E1, keyword search: zero occurrences of those terms; a search is not a reading).
2. **The Codex skill effect is not significant (E1).** Better on 12 of 20 (p about 0.50); mean difference 3.69, median 0.9; excluding Mars-Bench, MOTIVE and CarbonGlobe the mean skill effect is -0.06. The paper's inference that "the comparable proportional gain on Codex suggests the design generalizes" is not supported by this table.
3. **"Every benchmark improves" is best-of-four agents, one run each (E2/E1).** The re-audit of "half of each agent's runs (40 trajectories in total)" implies 80 main runs, which is 4 x 20. Opus alone is negative on 2 of 20 benchmarks and Codex on 4. Several wins are comparable to the paper's own run-to-run spread (ATAT +0.8 against repeat runs of 0.5 +/- 0.5 with a worst run of -0.3; ProteinGym +0.3 has no repeat runs). Sonnet is the best agent on 9 of 20 benchmarks (Opus on 6), yet the behavior and "tricks" analysis covers Opus, Codex and Gemini.
4. **"Engineering, not insight" rests on a word cloud and category percentages (E2, E3).** Figure 3 is a word cloud plus a frequency distribution; no labeling method or expert rating was found. The paper's own counter-example, PFDelta, is insight-driven but appears in only 2 of 4 no-skill runs (64.4 and 65.3 against 32.5 and 29.4; standard deviation 19.6).
5. **Not compute-matched (E2).** Agents use 8 x H200 for 12 hours; ensembles and test-time augmentation raise inference time by more than 10 times on some benchmarks. Ten of the twenty baselines use fixed hyperparameters only (Table 7), so some of the gain is tuning an untuned baseline.
6. **Audit validation is thin (E2).** Five known positives, all from the raw-repository pilot, and 15 sampled clean reports. The protocol removes test access, so the blatant routes are already closed; "no run flagged" shows no detectable misconduct, not none.
7. **Possible same-family bias (E2/E3).** Opus 4.6 assisted benchmark selection and standardization and is the default evaluator; the skills were derived from Claude Code traces. Human reviewers made the final decisions and the cross-family audit mitigates the auditing part only.
8. **Aggregation (E3).** A mean of relative improvements over heterogeneous metrics (a power-balance loss for PFDelta, mAP, PSNR); three outlier-heavy benchmarks carry much of the mean.

## 5. What this does and does not establish

- It supports: agents can improve published baselines on science benchmarks, mostly by standard engineering, under a careful anti-gaming protocol.
- It leaves unproven: that the skills nearly double progress, that the skill design transfers beyond Claude Code, and that the agents' contribution is "not research insight", which is undefined and was not measured by experts.
- Limits: one reader; B.3, B.4 and D were not read; the code and data were not run; whether later work has surpassed any benchmark's published best was not checked.

## 6. What would change this

A per-skill ablation with a placebo prompt on benchmarks not used to design the skills; repeat runs for the benchmarks that have none; a compute-matched baseline for the ensemble and augmentation runs; an expert-rated sample for the "insight" classification; and the same study on agents from outside the authors' developer.

## 7. Reproduction

Everything is in `agent4sci_hill_climbing_reading_v1/`: `recompute_table2.py` and its output (standard library only); `paper_checks.py` and its output (needs the arXiv v1 PDF and `pdftotext`; the PDF is not stored here); `tool_scan_*.json`.

## References

Sources: arXiv:2610.28763v1 (20 October 2026), PDF sha256 `d329c1a5dfd6ff3a6820f083ee39196f1caf84be4111af46c1cd0e4e5dbd57ba`.

## Revision log

- *2026-10-26, v1.* First public version, from a private note of 2026-10-25. Re-verified against the PDF on 2026-10-26 (section 2); two statements were reworded to say what a keyword search can and cannot show.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
