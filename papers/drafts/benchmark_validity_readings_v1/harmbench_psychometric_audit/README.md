# A Psychometric Audit, Audited: Reading the HarmBench “Harmful Refusal” Study and What Its Dimensionality Result Supports

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one paper, "Searching for “Harmful Refusal”: A Psychometric Audit of an AI Safety Benchmark" (arXiv:2610.12409v1, 8 October 2026; AI Measurement Science Workshop at COLM 2026; the paper names CMU, Indiana University and Google). The authors are called "the authors"; organisations are named only as the paper names them. No individual is named and no intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance; one reader, an AI system. Read from an operator-supplied copy (PDF sha256 in the Reproduction section). Pages 1-14 read in full (main text, Tables 1-4, Appendix C, most of D); pages 15-17 (rest of the logistic-DIF description, code pointer, references) skimmed or not read. HELM Safety data, the authors' code and the cited papers not accessed; no analysis re-run. Page refs are to the PDF as extracted. Same-source caveat: the reading assistant is an Anthropic model, and the audited pool includes 11 Anthropic models as one DIF group; the paper is Google-supported (two Google co-authors). Coding is the reader's; an operator may recode.

## Three-line check
- Finding: a careful, falsifiable construct-validity audit whose dimensionality result (one latent dimension is not enough for HarmBench in HELM's v1.17.0 pool) is robust within its own design; the title-level conclusion ("harmful refusal" not found) targets a construct the authors defined themselves, and the second test (DIF) largely restates the first.
- Agreement/response: none (paper only).
- Executed: `checks_from_reported_tables.py` (arithmetic on reported tables; output in `checks_output.txt`); parameter counts and headline log-loss gap reproduce.

## What it claims, in one paragraph
HELM Safety reports one normalized score over five datasets. Three of the four datasets resembling "harmful refusal" are saturated (pass 0.92-0.94); HarmBench (398 items, 81 models, pass 0.67 after binarizing two-judge scores at a unanimous 1.0) is modelled. Test 1: multidimensional IRT; confirmatory 3D (standard / contextual / copyright) beats the best 1D model on held-out log-loss, 0.258 vs 0.322 (all 5 splits). Test 2: Mantel-Haenszel and ridge-logistic DIF, OpenAI (21 models) vs Anthropic (11): 13 / 17 item flags under the single score, 1 / 2 under 3D scopes. Conclusion: the single HarmBench score does not isolate one attribute; "a score should earn its single-attribute reading before models are compared with it".

## What holds
Falsifiable design (test 1 could have returned one dimension); groups and scopes fixed in advance; null cutoffs from 5,000 simulated no-DIF matrices; five repeated splits, restarts chosen on training likelihood only; paired differences and per-split directions reported; 1PL / 3PL / 7D robustness table (App. C); the saturated datasets are reported rather than silently dropped; limitations name the LLM-judge dependence, small dependent groups, one benchmark at one release, and the missing replication with HarmBench's original classifier (p.9); the 3D-vs-7D point (no stable count) is stated, not hidden.

## Concerns (page refs; none checked against the data)
1. **The target construct is the authors' own** (pp.1-3). They write that "harmful refusal" is "our hypothesized construct and not one that the HELM Safety developers explicitly propose", and read HELM's "LM evaluated harmfulness score" as "a similar, if not identical, construct". HELM's blog (as quoted, p.3) calls HarmBench a "measure of the efficacy of jailbreaking techniques" across several harm domains: a composite by description. What is refuted is a unidimensional reading nobody is shown to have asserted. The defensible target is the practice of reading one score as one attribute; the title and conclusion ("We could not") claim more. Also, only one of the four candidate datasets was testable, so the conclusion that harmful refusal is not a single measurable attribute in HELM Safety generalizes from 1 of 4.
2. **Extra dimensions are not shown to be constructs** (pp.5-7). Splits are random 80/20 holdouts of individual responses, so near-twin models from one lineage are in training; extra dimensions can encode lineage or capability-tier clusters that a 1D model cannot. "Model-family checks" in App. C means IRT model families (1PL/2PL/3PL), not developer lineages. A leave-one-developer-out holdout would test this; not run. The authors do say the dimensions are not named constructs and that models are "not independent examinees" (p.9).
3. **The comparator in the text is weak, the one in the table is not** (Table 1; `checks_output.txt` C2). The 1D 2PL (log-loss 0.470) is worse than the 1D Rasch (0.330) with fewer parameters, so the prose statement that fit improves sharply from 2D through 10D partly measures a poorly fitting 1D model; the paper's real comparator is the 1D 3PL (0.322). The 3D-vs-1D-3PL gap (0.064) is the number to use.
4. **DIF largely restates test 1** (pp.5-8, App. D). The no-DIF null is simulated from the fitted unidimensional IRT model, which test 1 says does not fit; under multidimensionality, single-score flags are expected whenever groups differ in profile. Flags fall under scope-specific matching, but matching uses "the same items being tested" (p.8), so absorption by construction is an equal explanation; the paper concedes the result is "consistent with aggregation effects" but cannot rule out real domain differences. The test as run does not separate the two explanations it was designed to separate.
5. **Judge-family confound not discussed** (p.4). One of the two judges is `gpt-4o-2024-05-13`; the DIF pair is OpenAI vs Anthropic models. Self-preference could produce OpenAI-vs-Anthropic item flags. Limitations mention judge bias in general only (p.9).
6. **Thin DIF matching** (Table 4; `checks_output.txt` C3). OpenAI (.866) and Anthropic (.889) raw means put both groups near the top of the pool (.67 overall): roughly 44-53 failures per model, split across three ability bands, with 11 Anthropic models. Only two developers reach the 8-model inclusion floor, so "developer-linked" rests on one pair.
7. **Audited quantity differs from the reported one** (p.4, p.9). HELM reports a continuous two-judge mean; the audit binarizes at a unanimous 1.0. Described as "conservative", but no other cutoff, no per-judge matrices, no graded model; effect on dimensionality unknown.
8. **Overreach in the abstract and discussion.** "Any safety score that averages over datasets and items can hide saturation and conflate behaviors" (abstract) generalizes from one benchmark at one release (their own limitation, p.9); the copyright reading ("probably" memorization) is untested; "we do not need the second test" (causal condition) holds only for the reflective single-attribute interpretation, which concern 1 shows is the authors' own.
9. **Deferred gaps point to a co-author's paper.** Graded-response models, multi-group IRT with anchors, and lineage dependence are cited to a 2026 open-problems paper, "Problems 1-3" (pp.5-6) by a co-author; they remain open here.

## What would settle it (cheap to run)
(a) Leave-one-developer-out and leave-one-lineage-out holdouts for the dimensionality comparison; (b) per-judge response matrices, plus a judge from a third family, then re-run DIF; (c) cutoff sensitivity (any pass at >= .75, >= .5) and a graded-response model; (d) DIF with rest-score or purified anchors rather than scope scores that include the studied items; (e) the HarmBench original classifier pipeline on the same models; (f) the same two tests on one other published item-level matrix, to test the generality claim.



## Limitations: what this does and does not establish

- One reader, an AI system, reading a paper and its tables; the flags above are leads, each tied to a page or table, not verdicts, and a paper may answer them in places not read (see what was read and not read at the top and under Open).
- The number of flags is not a severity ranking (see the series overview).
- Evidence classes: E1 executed here (scripts and their outputs in this folder), E2 read, E3 interpretation, as marked in the text.

## Reproduction

Everything is in `benchmark_validity_readings_v1/harmbench_psychometric_audit/`: `checks_from_reported_tables.py`; `checks_output.txt`; `quote_checks_output.txt`; `tool_scan_*.json`. Re-fetched from arXiv on 2026-10-26: the file is byte-identical (sha256 `29249fd5f713e47805d0dbd49e3bb7e20dcc82d4f8131bfc66f7675d5b4032cf`). `quote_checks.py` (in the series folder) reports which double-quoted strings of this reading occur in the paper's text layer; strings that did not match were rewritten as paraphrases or corrected to the paper's wording before publication. The paper's PDF is not stored here; the preregistration and the scripts are.
- No predictions file: this reading was post hoc.

## References

Sources: the paper named in the scope line above (PDF sha256 `29249fd5f713e47805d0dbd49e3bb7e20dcc82d4f8131bfc66f7675d5b4032cf`); the numbers recomputed in the scripts are transcribed from its tables.

## Revision log

- *2026-10-26, v1.* First public version, from the reader's working notes of 2026-10-17. Quotation marks were removed from, or corrected in, phrases that did not match the paper verbatim; cross-references to working notes and workflow remarks were not carried over.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
