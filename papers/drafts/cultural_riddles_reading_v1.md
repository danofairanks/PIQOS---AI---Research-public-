# Reading a Cultural-Riddle Benchmark Against Its Own Counts: CulturalRiddles (arXiv:2610.29968v1)

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one preprint, "CulturalRiddles" (arXiv:2610.29968v1, 22 October 2026, 37 pages). The authors are called "the authors". Model and vendor names are those the paper uses. No individual is named and no intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance; one reader, an AI system. This reading was post hoc: no predictions were fixed before reading. The benchmark scores commercial models and uses LLM judges, and the reader is a commercial model too; the judge-independence findings below apply to that shared position as well.

## 1. What was read, and how

- **Read (E2):** the PDF, 37 pages: main text, Tables 3 and 5, Figures 4 to 9, and the sections of Appendices A.2 to A.4 and B.4 to B.5. The remaining appendix pages were searched by keyword, not read in full. The dataset and code (Hugging Face, GitHub) were not fetched, so no item-level check was possible.
- **E1:** `checks.py` and `checks_output.txt`, arithmetic on numbers printed in the paper. **E3:** interpretation.
- **Re-verification on 2026-10-26.** The PDF was re-fetched from arXiv (sha256 `a827990e…f669b5`, 37 pages). `quote_checks_output.txt` reports how many double-quoted strings in this draft occur in the PDF's text layer (`quote_checks.py` in the series folder is the same tool used for the other readings); strings that did not match were rewritten as paraphrases or corrected to the paper's wording before publication. `checks.py` re-ran and reproduced its committed output.

## 2. What it is

6,191 riddles written by 167 volunteer native speakers for 62 national-linguistic communities (51 languages, 45 countries), 100 per community (8 shared topics + 2 chosen). 28 model configurations answer 6,090 riddles (61 communities) once each (170,520 responses). Scoring: rules (18.87%), native-speaker labels (59.10%, top-10 most frequent unscored answers per riddle), two-judge LLM jury that scores only when both agree (22.04%); 1.78% unscored. Headline: best model 79.4%, none above 22% on Lumasaba/Mongondow; exact match misses ~47% of correct answers; models almost never abstain (0.80%).

## 3. What holds (E1)

Counts reconcile: 28×6,090 = 170,520; rules+native+jury = 170,520; the five score bands sum to 170,520; Table 3's 17 rows sum to 132,940 = rules+native; exact match 28,049 = 16.45% of all = 53.1% of correct, i.e. misses 46.9% (printed ~47%); translation gain 10.3 pp of a 46.9 pp gap = 22% (printed as "about a fifth of the gap"). Reasoning/search deltas recompute (66.0−59.7 = 6.3; 63.8−58.8 = 5.0; 76.3−64.5 = 11.8). The unscored 1.78% bounds overall accuracy to 30.95–32.73%, so the exclusion is not a large effect. The exact-match undercount is the best-supported finding. The paper is candid about single runs, the judge's shared errors, and that its translation experiment "does not causally separate language from cultural knowledge".

## 4. Added angles (E3)

1. **Community ≈ author.** Typically 1–2 writers per community. The four hardest-group communities with 1 writer and 1 evaluator in Table 5: Luganda, Lumasaba, Mongondow, Buginese. The headline (no model exceeds 22% on Lumasaba or Mongondow) therefore rests on one writer's riddles scored by one evaluator each. The paper's own variance model says the individual riddle is 61% of benchmark variance and community 13%: with 1–2 writers, "community" cannot be separated from writer idiosyncrasy. 38 of 41 translations that leaked the full answer came from Lumasaba, which is a writer-practice signal (heterogeneous item quality), not a culture signal.
2. **No human-solver baseline.** No measure of how many native speakers can solve these riddles. Verification only requires "solvable" per one other native speaker; the paper notes riddles may rely on generation, region or interest. Without a solver baseline, a model lacking community content and a riddle that is idiosyncratic or poorly specified are not separated; the conclusion that the gap reflects "content from the communities themselves" is interpretation, not an outcome of the design.
3. **Difficulty calibrated against the models being tested.** 46.1% of surveyed writers (of 76 respondents from 43 of 62 communities; 45% response rate) tested riddles on AI tools to calibrate difficulty. That selects items toward model-hard, so absolute accuracies are not a measure of cultural knowledge, and the high-resource vs low-resource comparison inherits unequal tuning effort by writer.
4. **"Human-only" is self-qualified.** Table 2 marks the benchmark human-only (no LLM-generated item content), yet 39.5% of respondents used AI to brainstorm and 5.3% to paraphrase or co-write (3–4 writers). The claim is "created entirely by humans" in the abstract; the survey shows partial AI involvement in item creation.
5. **Judge panel overlaps the leaderboard's vendors.** Judges are cheaper variants from the same families as the #1 (Gemini) and #5 (DeepSeek) models; names hidden, but jointly accept 9.0% / 6.9% of human-rejected answers from Gemini 3.1 Pro / GPT-5.5, and share about two-thirds of their errors (the paper quantifies shared-error correlation between judges, relevant to treating two judges as independent). The upward bias affects the top of the ranking (jury covers ~22% overall, more for weak models).
6. **Human-labeled subset is not a random sample.** Annotators label the ten most frequent unscored answers per riddle, so labels over-represent answers shared across models (strong models); rare unique answers (weak models) go to the jury. Table 3's error-type distribution is therefore not representative of all errors, and error types are not reliable even among humans (weighted κ 0.41 for the 13 types, H1–H2) versus 0.80 on accuracy.
7. **Hallucination headline depends on denominator.** "24.19% hallucinated" is a share of all rule+human responses including correct ones. Among the 73,940 incorrect responses (score 0), hallucinated = 43.5% (E1). Abstention 0.80% is of all. The qualitative claim (models rarely abstain) survives either denominator; the 24% vs 0.8% contrast in Fig. 1 is not like-for-like. Abstention and hallucination definitions depend on a single English prompt used for all languages.
8. **Rankings without uncertainty.** One run per configuration, one prompt, no seed or prompt variance, no CI on leaderboard positions. Rank 4 (GPT-5.5 [search], 64.5) vs rank 5 (DeepSeek V4 Pro [high], 63.8) differ by 0.7 pp; adjacent ranks 3–5 span 2.2 pp. Not tested here (no item-level data).
9. **Translation experiment confounds.** Five hardest communities, 458 riddles; English responses scored by rules+jury only, original-language responses by humans+jury (unequal pipeline); the high-resource reference (69%) is on different riddles ("not a matched control", their words); 41 translations leaked the answer. The "about a fifth of the gap" figure is a bound on language-only effect (translation also removes wordplay), not an estimate of how much is missing content.
10. **Resource-level estimates rest on few communities.** Low n=4, extremely low n=6 communities; adjusted odds ratios 0.10 (CI 0.02–0.48) and 0.04 (0.01–0.15). Resource level is Common Crawl page counts, dialects inherit macro-language counts (Sudanese Arabic classed high-resource).
11. **Table 5 transcription caveat (the reader's error, not the paper's).** The reader tried to total the writers/evaluators columns from the PDF text layer and got 173/117 vs printed 167/109; the layer is ambiguous for rows with one number. No aggregates from that transcription are used; only the four unambiguous rows above.

## 5. What this does and does not establish

- It supports the paper's counts and its best-supported finding (exact match undercounts correct answers), and it shows several places where the headline wording rests on one writer per community, an unvalidated solver baseline, a judge panel that overlaps the leaderboard's vendors, and single runs without intervals.
- It does not show that the benchmark's conclusions are wrong, and nothing here could be checked at item level.
- Limits: one reader; the dataset was not opened; the appendix was partly skimmed; the findings in section 4 are interpretation (E3) except where marked.

## 6. What would change this

Fetch the HF dataset and check: writers per community vs accuracy; Lumasaba/Mongondow items for ambiguity; whether riddle length/answer-leakage predicts accuracy; reference-answer uniqueness. Read appendix pages B.1–B.3 (crossword details) and A.4 judge calibration fully. A human-solver pilot on a handful of hardest-community riddles would be the single most informative addition.

## 7. Reproduction

Everything is in `cultural_riddles_reading_v1/`: `checks.py` and `checks_output.txt` (standard library; the numbers are transcribed from the paper); `quote_checks_output.txt` (needs the preprint PDF and `pdftotext`; the PDF is not stored here); `tool_scan_*.json`.

## References

Sources: arXiv:2610.29968v1 (22 October 2026), PDF sha256 `a827990e9dffcd0c803a7ab87a386cb1a434ac658e2e43fb0f53ccb266f669b5`.

## Revision log

- *2026-10-26, v1.* First public version, from the reader's working notes of 2026-10-23. Two quoted phrases were corrected to the paper's wording. Notes on an outward comment and a framework-relative aside are not carried over.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
