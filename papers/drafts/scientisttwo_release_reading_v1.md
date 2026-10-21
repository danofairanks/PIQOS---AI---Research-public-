# Reading a Verification Claim Against Its Own Tables: A Public Release of 86 Machine-Written Papers

**Draft v1.1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** The objects examined are one public preprint, "ScientistTwo: Pioneering the Human Knowledge Frontier with Autonomous AI" (arXiv 2609.19644v1, dated 2026-09-18, affiliation line "Google Cloud AI Research / University of Waterloo"), the project site and public repository that accompany it (`scientist-two.github.io`, GitHub organisation `scientist-two`), and 37 of the 86 machine-written papers the site hosts. The organisation is named as the release names itself. No individual is named, no intent is attributed, and nothing here is a statement about how the release was produced beyond what it says. The seven generated papers are anonymous and are identified by the method name in their titles.

**Disclosure.** Drafted with AI assistance, which also did the reading. One reader coded every finding; no second reader checked them. Predictions about each stage were written down before that stage was read (section 4). The reader did not run any of the release's code, because the release contains none (section 5). The comparison sets, tables and page references below were transcribed from PDFs by hand; the arithmetic is in the scripts next to this file.

## 1. The question

The release makes two kinds of claim. One is a performance claim: the system, given a published paper as a task, writes a new paper with code that beats that paper's method (86 of 107 tasks, average relative gain 25.2%) and receives higher average review ratings than the accepted human papers under automated review agents. The other is a verification claim: the results are "fully verified and reproducible", every paper's released code is re-run, and four integrity audits pass. This note asks one narrow question about both: **where a claim is checkable from material that is public, does it match what the same document's tables say?**

It does not ask whether the papers are good science, whether the method ideas work, or whether the system could be used well.

## 2. What was released

Facts read from the release (E1: executed or counted; E2: read):

- The preprint (71 pages) describes a multi-agent pipeline. A human supplies a published paper with its benchmark; agents extract limitations, generate ideas (novelty checked against two retrieved papers, App. A.2), test each on a benchmark subset and then the full set, run ablations, draft a paper, and run a simulated review-and-rebuttal loop with an automated reviewer (target score 8) and a meta-review step. Models are frozen. About 2.5 days and about $3,765 per task are reported.
- 107 problems: 5 from ICLR 2026, 38 from NeurIPS 2025, 64 from ICML 2026 spotlight papers. 86 "successful" (80.4%).
- The public repository holds a static site and 86 PDFs (applications 15, deep learning 24, general ML 14, optimization 5, probabilistic 10, reinforcement learning 3, social aspects 9, theory 6). It holds no source code, code archive, data, review scores or audit reports (E1, file listing).
- The preprint's integrity audit (Table 7) reports audit counts of 49 or 50 papers, not 86. The site states "Every paper is re-examined against its own artifacts: the released code is re-run to confirm each reported number" and shows an integrity table with the same 49–50 denominators.

## 3. What was read

| # | Item | Selection | Depth |
|---|---|---|---|
| A | The preprint | Given | Main text (pp. 1–19) and Appendix A–B (pp. 28–32); not the generated papers and audit transcripts in pp. 33–71 |
| B | Project site text and repository listing | Given | Complete (static site, 98 files) |
| C | All 86 PDFs, keyword scan only | Census | Presence of keywords per paper; no claim read |
| D | Specimen: "Fisher Channel-Damped Engram" (FCD-Engram) | Chosen by hand from the site by the project's operator; **not a random draw**, and it is also the paper the preprint uses for its own case study (Table 6) | Full read, tables checked |
| E | Six papers: UNI-XDLM (deep learning), BAM-Val (general ML), ALOT-DRO (optimization), ScaleMode-NeuralSurv (probabilistic), Overdamped DAVE (social aspects), DRO-ROCP (theory) | One per domain by the hash rule in section 4, fixed before it was run | Abstract, main tables, ablations and limitations; appendices only where a table was needed |

| F | Thirty more papers: the 30 with the smallest `sha256(basename)` among the 79 not already read (list in `ext30_selection.txt`; deep learning 10, social aspects 7, applications 5, general ML 4, probabilistic 2, reinforcement learning 2) | Rule and predictions committed before any of the 30 was read | Abstract, conclusion and main tables; appendices only where a main-text claim pointed to one |

All eight domains appear in E and F; optimization and theory appear only in E (one paper each).

## 4. Method

**Predictions first.** For A and D the predictions were written from the abstract (A) or from the preprint's own summary table (D) before the text was read. For E and F the sampling rule and the predictions were written before the rule was run. Scoring (section 8) uses the predictions as written; misses are recorded as misses.

**Selection rule for E.** For each of six domains, take the paper whose `sha256(filename)` is smallest (`select_sample.py`). The rule is not chosen by suspicion. A different rule would give different papers.

**What counts as a mismatch.** A quantitative or comparative statement in a paper's abstract or conclusion that the same paper's tables (a) contradict, (b) cannot support because the comparison needed is absent, or (c) report for a different set, aggregate, training size or metric than the statement names. Other things are recorded in a separate column and are not counted as mismatches: a measured regression the abstract leaves out, an internal inconsistency between two tables, a gain that is smaller than the reported spread, and a method choice that looks tuned on the outcome. A statement is counted once.

**Selection rule for F.** Among the 79 papers not already read, take the 30 whose `sha256(basename including .pdf)` is smallest. It was written into the first version of this draft (section 10) before it was run.

**Coding conventions used in F (not all fixed beforehand).** A statement counts as supported when a table or the paper's own text gives the number; counts of many items stated only in text are coded as matching and recorded under *other issues*. A mismatch is counted per underlying table discrepancy, not per sentence. Three counted items are flagged minor or arguable (a 0.0001 difference; a grid presented as the approximation; a 0.07-point difference inside a stated error). The conventions were written down while coding the second tranche; they were not stated when the first six were coded, and the counts for those six were not revisited under them.

**Evidence classes.** E1 executed or counted (arithmetic on transcribed tables; keyword counts), E2 read, E3 interpretation. "Not found" means not found by search; it is not "absent".

**What was not done.** No code was run (none is released). The appendices of the generated papers were not read in full. The human-authored source papers were not read. No second reader.

## 5. Findings on the release (A and B)

1. **The headline quality comparison holds under the in-loop reviewer and not under the held-out one.** The preprint reports two automated reviewers. One is used inside the rebuttal loop and so is described by the authors as an "in-distribution evaluation"; the other is described as unseen during development. Weighting Table 3 by paper count (human n = 107, generated n = 86): in-loop reviewer, human 6.65 vs generated 7.46; held-out reviewer, human 5.85 vs generated 5.65, with accept rates 87.9% vs 72.1%. By venue under the held-out reviewer, generated minus human: ICLR +0.2 (n 4 vs 5), NeurIPS +0.1 (n 33 vs 38, standard deviations about 0.7), ICML spotlight −0.4 and −27.5 accept-rate points (n 49 vs 64) (E1). The abstract says the generated papers "achieve higher average review ratings than human-authored papers under automated AI review agents." The figure caption names ICLR 2026 and NeurIPS 2025 and omits the ICML row. The project site is more qualified: it says "spotlight-level quality remains out of reach".
2. **Different denominators carry different claims.** The 86 successes carry the review statistics; the 21 failures drop out of the generated-paper averages. The integrity audit covers 49–50 papers. The human evaluation covers 33 papers read by 9 reviewers; on its 1–5 scale the overall comparison is 3.0 (parity) and method soundness is 2.9, favouring the human papers (p. 16).
3. **One instrument sits in the loop and in the evaluation, twice.** The in-loop reviewer's scores gate the rebuttal rounds and also supply the first headline comparison (disclosed). Table 5 shows what a second review round does: in-loop accept rate 79.6% → 93.9%, held-out accept rate 73.5% → 69.4%. The integrity checks are enforced in the loop by three refinement agents and then reported as a post-hoc audit (disclosed); no held-out counterpart is described.
4. **Measured reward hacking, with a closing design.** Without the specification-compliance agent the audit finds a violation in 1 of 50 papers, and the paper says that codebase "contains reward hacking, it must be filtered" (Table 7, fn. 2). With the agent: 0 of 49. Reference hallucination: 19 of 1,840 without the reference agent, 0 of 1,814 with it. The compliance detector is itself an agent reading agent-written code (E2).
5. **"Human state of the art" is one paper's method on its own benchmark suite**, as reproduced by the system, not the field's best. Gain statistics in Table 4 were obtained by parsing the generated papers' main tables ten times with an AI model and averaging, not by re-running code (p. 12). Novelty is checked against two retrieved papers (p. 30).
6. **The code is not public.** The repository is a static site with PDFs (E1). The site's sentence that "the released code is re-run to confirm each reported number" therefore describes a process an outside reader cannot inspect or repeat. The audit's "every paper" is 49 papers in its own table.

## 6. Findings on the generated papers (D and E)

Seven papers. The *Mismatches* column counts statements in the abstract or conclusion as defined in section 4; *Other issues* counts items recorded but not counted. All numbers are from each paper's own tables, re-derived in `specimen_checks.py` and `sample6_checks.py`.

| Paper (domain) | Mismatches | Other issues | Examples of the mismatches |
|---|---|---|---|
| FCD-Engram (applications; specimen, not random) | 3 | 2 | "The lowest exact memorization of any method evaluated" (0.071): its Table 1 lists 0.004 and 0.044 for two other methods; the composite "Overall" is the harmonic mean of three categories, so that regression cannot enter it. "Per-channel damping is the sole active mechanism": its own factorial gives 73% of the +0.211 gain over the baseline to layer scaling, and damping alone on the baseline scaling lowers the score (0.705 → 0.636). WMDP "matched forgetting": 91.4% of the base-to-chance drop vs 97.7% and 95.4% for the comparators. Other: Table 9 gives 0.761 for a configuration "at its best α" that Table 5 puts at 0.860–0.880 at one α; hyperparameters are described as fixed once and as "best α" per row |
| UNI-XDLM (deep learning) | 2 | 2 | Caption and abstract: "ranks second of seven on both" at length 512; it is second on validation PPL and third on the zero-shot average, worse than XDLM (1192.9 vs 1182.2), reversing the +51.8 gain at length 128. "Pure masking collapses to worst": the same table has another method worse. Other: the abstract's in-domain comparison names only the two methods it beats (two others are better in Table 1); the 8B "preserves MMLU and HumanEval" omits GSM8K, down 6.6 points |
| BAM-Val (general ML) | 0 | 3 | Headline numbers re-derive (0.829 vs 0.825; others ≤ 0.817; 8/8 vs one baseline; 7/8 vs another; rank-1 on 6 of 8 columns). Other: "8/8 over Bipartite" counts a +0.0005 difference; pooled p = 3.8e−12 over 160 paired runs but individually significant on 5 of 8 datasets (disclosed); an introduction bullet says "first among 11 methods" where the table lists 18 |
| ALOT-DRO (optimization) | 3 | 2 | Abstract: head-to-head with two named baselines "on synthetic and real benchmarks"; those baselines appear only in the synthetic table. "The only method that retains its coverage certificate across all tasks": on the real-data table its own coverage is below the 0.90 target on 3 of 4 benchmarks. "~880× faster": no table gives 880× (tables give 255× and 135×). Other: real-data loss is worse than its comparator on 3 of 4 while the abstract says it "matches" risk; the default temperature is the one value that reaches the coverage target |
| ScaleMode-NeuralSurv (probabilistic) | 2 | 3 | "Outperforming twelve baselines" uses literature numbers from full-data training against the method's own N = 125 runs (the table caption says so). The abstract's "identical-splits aggregate 0.648" is a mean over three datasets; the eight-dataset aggregate is 0.646. Other: the C-index gain is smaller than the larger fold standard deviation on 7 of 8 datasets, with no test; coverage rises 0.539 → 0.605 against a 0.95 target and falls on three datasets; the reproduced baseline scores 0.517 on full SUPPORT |
| Overdamped DAVE (social aspects) | 1 (weakest) | 2 | "A single sample beats 100-sample vanilla on GridPG with a 93× speedup": vanilla at one sample (48.56) already beats vanilla at 100 (41.23) at the same 6.76 ms, so the speed-up is not due to the new component. Other: energy-based localisation at one sample is 23 points lower than the 100-sample comparator (not in the abstract); its Table 3 shows an exponential sharpening kernel beating the headline power-law kernel (GridPG 73.96 vs 62.95) at identical faithfulness |
| DRO-ROCP (theory) | 1 | 3 | "Matches or beats ROCP, RAC and others": RAC has the lower realized loss at all seven α on the COVID base matrix. Other: the "0.0% critical mistakes vs 12.95%" compares to RAC only (its parent method also has 0.0%); the shipped variant's failure rate on the base matrix is 11.28% vs 10.59% for standard ROCP; miscoverage 0.0020 vs 0.0012 against a 0.001 target at the largest gain |

Five of the six hash-selected papers have at least one counted mismatch (the sixth has none, only other issues); with six papers that count says little about a rate (a 95% Wilson interval for 5 of 6 is 0.44 to 0.97).

### 6b. Thirty more hash-selected papers (F)

Result, under the section 4 definition and the conventions above: **12 of the 30 papers (40%) have at least one counted mismatch**; 95% Wilson interval 0.25 to 0.58. Eighteen have none. Nine of the 12 are clear and three are minor or arguable; excluding the three gives 9 of 30 (30%, 0.17 to 0.48). With the six papers of E (five with a counted mismatch) the figure is 17 of 36 (47%, 0.32 to 0.63); 16 of 36 (44%) if the weakest count of E (Overdamped DAVE) is dropped. `ext30_summary.py` recomputes these from `ext30_coding.jsonl`.

The twelve (`ext30_table.md` lists all 30):

| Paper (domain) | Statement against the paper's own tables |
|---|---|
| COFM-SIB (probabilistic) | "Matches or outperforms state-of-the-art baselines": a published and a reproduced baseline row in its Table 1 are above it on two benchmarks |
| PhySense-AdjointFlow (deep learning), minor | Conclusion "never regresses" on the saturated benchmark; its error is higher than the control at three of four budgets by 0.0001 |
| CS-HLA (deep learning) | The abstract's gate "guarantees zero clean accuracy loss"; its Table 1 shows −0.7 and −0.2 on one model |
| NEM-SPKN (general ML) | "Maintains HSP-GKN training speed": its time is 1.5× to 2.4× on all 12 datasets |
| Exact-CPWL CVaR (reinforcement learning), arguable | "Matches grid baselines exactly"; the grid gap column is up to 0.118 (the paper presents the grid as the approximation) |
| TabHarmony (deep learning) | "Zero-loss guarantees"; its Table 1 shows 1, 4 and 5 losses at the noise threshold |
| TPH-Lock (deep learning) | "+2.50 points on average over 16 cells" is the N = 100 figure (sum of the deltas 40 / 16); at full scale the same cells average +0.37 with two significant losses, while the abstract says the full-scale tests "confirm that the gains are statistically significant" |
| PG-CDIG (applications) | "Outperforms existing baselines across 10/10 settings": the 10/10 is against its Cartesian predecessor only; in its Table 1 another baseline is higher in most columns |
| InfoOptim (deep learning), minor | "Zero zero-shot accuracy loss": 31.21% against 31.28% average, inside the stated error |
| BTV-RDRO (probabilistic) | Significance against entropic-OT baselines and forward-LV: one baseline has the lower loss on one panel and no test is shown against them; forward-LV is better on the real portfolio task |
| SAVVY-Vortex (applications) | "New state of the art" at 57.6; the table's paper-reported baseline row is 58.0 |
| Flex-Dot (social aspects) | "100% faithfulness"/"exact by construction"; its Table 2 faithfulness gaps are non-zero (0.034 to 0.30 on three datasets) |

Ten of the 12 are statements contradicted by a table (type (a)); two are a different set or aggregate (type (c)). All 30 papers have at least one *other issue* (an omitted regression, a gain smaller than the reported spread, a baseline that looks weak). About ten of the 30 contain a table-against-table or text-against-table inconsistency (for example, a table whose listed averages do not equal the mean of its own rows; an ablation whose default configuration scores differently from the main table). Those are not counted in the rate.

The recurring shape (E3): a statement that is true for one quantity is stated for another. The comparison set is narrowed in the abstract; a table is aggregated differently from how the abstract describes it; a gain is credited to the new component when a baseline setting shows it too; or a measured regression is left out of the abstract. In the cases that could be re-derived, the table arithmetic is internally consistent (BAM-Val throughout; the composite scores in FCD-Engram; the preprint's own Table 3 weighted means). The four checks the release describes for its integrity audit (score reproduction, specification compliance, references, and agreement between the written method and the code) do not include comparing a paper's abstract claims with its own tables; the mismatches above sit in that gap (E3).

## 7. What held up

- The preprint runs a held-out reviewer, reports that the in-loop reviewer is in-distribution, and shows the human comparison on all three venues. The site states that spotlight-level quality is out of reach.
- An ablation critic rejected a variant whose gain it attributed to generic training controls rather than the proposed mechanism (App. B), and a protocol-immutability audit is part of the pipeline.
- A human evaluation exists and does not favour the system on method soundness. The limitations paragraph states the cost per task.
- The preprint reports the measured reward-hacking case instead of omitting it.
- Where tables could be re-derived they were consistent, and every generated paper in the keyword scan has a reference list; 91% mention limitations, 77% report some variability measure (±, standard deviation, confidence interval), 74% mention seeds (presence only; E1).
- In the second tranche, 18 of 30 papers have no counted mismatch, and several state their own limits plainly in the text (for example a non-significant gain flagged in a table caption, or a regime reported as having negative headroom).
- The site discloses that the 86 papers are "autonomously generated". The PDFs do not say so (0 of 86).

## 8. Predictions scored

| Stage | Prediction | Result |
|---|---|---|
| A | Headline quality claim judged by automated reviewers; executed gate for benchmark gains | Held; but a human evaluation exists (33 papers), which was not predicted |
| A | "Without human intervention" still leaves a human-supplied problem, baselines and metrics | Held |
| A | Comparison to accepted papers is small-n with no confidence intervals | Partial (means ± sd; no test; ICLR n = 4 vs 5) |
| A | "Fully verified" means the code runs, not independent replication | Partial: the audit re-executes code and compares scores, but on 49–50 papers, by the same group's framework, and nothing is public |
| A | Contamination not addressed | Held (not found by keyword search) |
| A | The reviewer that gates the loop also scores the result | Held, with a disclosure not predicted |
| A | Frozen weights, no self-modification | Held |
| C (86 PDFs) | ≥90% anonymous header; 0% AI-disclosure in PDF; ≤25% code URL; ≥50% no variability; ≥60% "limitation"; ≥50% "seed"; median pages 12–24 | Held except: 85% header (13 papers carry the conference template's placeholder author block), and 77% (not ≤50%) contain a variability keyword |
| E | ≥3 of 6 have a mismatch; ≥1 has none | Held (5 of 6, under the stricter counting of section 4; BAM-Val has none) |
| E | ≥4 of 6 single-run or unspecified | Missed (one clearly single-run) |
| E | ≥2 of 6 tune a "best" per row without a stated held-out split | Not determined |
| F (30 papers) | At least 60% have a counted mismatch | Missed: 12 of 30 (40%; 95% interval 0.25 to 0.58) |
| F | Type (a) contradictions are a minority of counted mismatches | Missed: ten of the twelve are type (a) |
| F | At least 3 papers with no counted mismatch | Held: 18 |

## 9. Limitations: what this does and does not establish

This note does not establish any of the following.

- It gives a rate with a wide interval, not a measurement of a population. Of 36 hash-selected papers, 17 (47%, 95% interval 0.32 to 0.63) have a counted mismatch; in the 30-paper tranche 12 (40%, 0.25 to 0.58), 9 (30%) without the minor items. The rule is one of many, and a different rule would give different papers.
- It does not show the generated papers are wrong in substance. The mismatches are between statements and tables, read from text; some may have explanations in appendices not read.
- It does not show that human-written papers do better. The same check was not run on the 107 human source papers, so there is no baseline for how often an abstract in this literature says more than its tables.
- It does not test performance. The 86 / 107 success rate, the 25.2% average gain and the review scores cannot be reproduced from the release.
- It does not test intent or process, and nothing in it concerns individuals.
- One reader coded everything. The definition in section 4 leaves room for disagreement at the edges: omitted regressions and text-only counts were not counted, and a reader who counts them would find a higher rate; a reader who requires a larger gap than 0.0001 would find a lower one. Some conventions were written down while coding (section 4).

## 10. The extension (run) and what remains

The first version of this draft preregistered a 30-paper extension with the prediction that at least 60% would have a counted mismatch. It was run (section 6b); the prediction was missed (40%). What remains, preregistered here and not run:

1. **Reference class.** Apply the same rubric to 30 human-authored papers drawn by the same hash rule from the 107 source papers (they are public; the PDFs are needed). Prediction: the human rate is lower but not zero. If it is similar, the mismatch rate says more about the genre than about the system. Without this, no figure above can be read as a difference between generated and human text.
2. **Second reader.** At least a second coder on the 36 papers; the rubric, a subset coded blind. A second reader disagreeing on more than a fifth of coded mismatches would change the reading.
3. **Explained mismatches.** Any counted mismatch explained in an appendix not read is moved to "explained" and reported.
4. **Not comparable to the release's success rate.** The release's 80.4% is a rate of beating a baseline; a mismatch rate is a different quantity, and the two are not to be set against each other.

## 11. Reproduction

Everything in `scientisttwo_release_reading_v1/`: `select_sample.py` (the hash rule for E), `ext30_selection.txt` (the 30 of F), `ext30_coding.jsonl` (per-paper claims checked, counted mismatch, other issues), `ext30_table.md`, `ext30_summary.py`, `pdf_keyword_scan.py` and its output, `host_table_checks.py`, `sample6_checks.py`, `specimen_checks.py` and their outputs. To repeat: clone the release's public repository, run the selection rule on `generated-papers/`, open each PDF, and transcribe the cited tables. The preprint is arXiv 2609.19644v1.

## References

Sources: the preprint arXiv 2609.19644v1 ("ScientistTwo: Pioneering the Human Knowledge Frontier with Autonomous AI", dated 2026-09-18); the project site `https://scientist-two.github.io/` and the public repository `https://github.com/scientist-two/scientist-two.github.io` (commit aaf25a7, 2026-09-17), read read-only; and the 86 PDFs in its `generated-papers/` directory, of which 37 are read in sections 6 and 6b. The two automated reviewers named are those the preprint names (ScholarPeer and the Stanford Agentic Reviewer). The statistics in sections 5 and 6 are the release's own table values or arithmetic on them (`host_table_checks.py`, `sample6_checks.py`, `specimen_checks.py`); each carries a table reference where it appears.

## Revision log

- *2026-10-21, v1.1.* Ran the preregistered 30-paper extension (section 6b): 12 of 30 with a counted mismatch, below the preregistered 60%; combined 17 of 36. Section 10 now lists what remains (human reference class, second reader). Coding conventions stated in section 4.
- *2026-10-21, v1.* First version: preprint, site, repository listing, 86-PDF keyword scan, one specimen, six hash-selected papers.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
