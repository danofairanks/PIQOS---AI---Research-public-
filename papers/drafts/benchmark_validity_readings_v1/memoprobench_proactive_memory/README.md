# A 2x2 That Partly Measures Its Metric: Reading MemoProBench ("Toward Memory-Driven Proactive Assistance")

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one paper, "Toward Memory-Driven Proactive Assistance" (MemoProAgent / MemoProBench, arXiv:2610.22671v2, 21 October 2026; the paper names MSU and Meta). The authors are called "the authors"; organisations are named only as the paper names them. No individual is named and no intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance; one reader, an AI system. Read from an operator-supplied copy (32 pp). Read via text extraction: body, Sections 3-6, data-construction appendix, metric and judge-prompt sections; figures read as extracted text only (numbers in Tables 4/5 and the ablation taken from the text; per-figure values not visually checked). Lens: the series overview. Same-source caveat: single Anthropic-model reader; Claude-sonnet-5 is one of the evaluated backbones. Post-hoc; no arithmetic checks run; no code or data accessed.

## What it is
Memory-driven proactive assistance: no query; system sees an egocentric stream plus a ~618K-token year-long synthetic memory and must fire once, inside a trigger window, with LLM-judged Good content. 1,804 human-verified pairs (904 train / dev / 800 test; 150 negatives). Metric Perfect = exactly one fire, in window (+2 s), Good content. 2x2 study (oracle vs retrieved memory x timing given vs chosen, n = 150, two models). MemoProAgent = graph memory + gate + speaking-history, optional GRPO on the generator.

## Flags (ranked; post-hoc)
1. **The 2x2 conflates timing skill with always-visible evidence.** In "timing not given" cells evidence is shown at every step; Perfect requires one fire, so a model that always sees the oracle memory fails by repeated firing (77.3 -> 26.0, 96.0 -> 38.0). The retrieved-memory, timing-given setting injects noisy retrieval only in-window, so its 15.3% mostly measures retrieval noise. n = 150, two models, no CIs, no interaction test. Supports "gating matters"; supports the claim that timing is a separate necessary skill less.
2. **Headline gain is metric-coupled.** Largest ablation drop is hiding the model's own speaking history (to 8.0); gate -13.3, structured memory -16.6. The text does not say whether Standard RAG / All-history / Summary baselines receive the speaking-history signal, so part of 7.0 -> 37.5 may be a baseline-handicap difference. Baseline k is chosen per model at its best result; the harness's hyperparameter selection is not described the same way.
3. **"When to speak" = when the target object first appears** (first-to-last visible timestamp, gaps <= 8 s merged). Whether a reminder is worth the interruption rests on the LLM judge and the generated worth-triggering gate.
4. **Synthetic memory, one pipeline for train and test.** LLM proposes the target evidence from localised frames; persona, timeline and distractors are generated around it; target is 0.19% of the stream. Train (904) and test (800) share the generator; "generalisation" is 100 EPIC-Kitchens clips through the same pipeline. Stylistic separability of target memory from distractors is not examined. The paper discloses that memory is synthetic.
5. **RL gain modest and unqualified:** 37.5 -> 42.4 (windowed), 33.3 -> 40.6 (streaming); no CI or seeds. Judge-gaming check is sensible (Hit flat 54.6 -> 54.0; over-trigger falls 22.3 -> 13.5) but the improvement is mostly "fire once", which the reward encodes (-1 for any non-first fire).
6. **Judge not named or validated against humans in the text read** (Appendix H is referenced; no agreement statistic found). Human verification (32 annotators, majority vote, 87.7% of samples triple-reviewed) covers sample construction, not the judge.
7. **Table 1 related-work columns are authored so only the row for this work is full.**

## Holds
Task formulation (memory as trigger, not only content); negative clips included (150) so silence is scored; early/late/over-trigger breakdown reported; judge-gaming probe; ablations; explicit limitations (synthetic, text captions, single trigger window, no latency).

## Open
Appendix H (judge); whether baselines get speaking history (Appendices A, B); whether the harness was tuned on dev; HF data (facebook/MemProBench) and code not accessed.

## Evidence tier and deeper-pass flag (added 2026-10-25)
**Tier:** E2 read, text extraction only; figures not visually checked and no arithmetic run (so no E1). E3: flags 1 and 2 are the reader's reading of the 2x2 design and the ablation.
**Deeper pass:** recommended, and cheap first step is reading-only: finish Appendix H (judge) and A, B (whether baselines get the speaking-history signal) before anything is run. Code and data are public (Meta HF); a baseline re-run with speaking history added would decide flag 2. Not done.

## Limitations: what this does and does not establish

- One reader, an AI system, reading a paper and its tables; the flags above are leads, each tied to a page or table, not verdicts, and a paper may answer them in places not read (see what was read and not read at the top and under Open).
- The number of flags is not a severity ranking (see the series overview).
- Evidence classes: E1 executed here (scripts and their outputs in this folder), E2 read, E3 interpretation, as marked in the text.

## Reproduction

Everything is in `benchmark_validity_readings_v1/memoprobench_proactive_memory/`: `quote_checks_output.txt`; `tool_scan_*.json`. Re-fetched from arXiv on 2026-10-26: the file is byte-identical (sha256 `cf088d4c980c858bdf7c4d16f0c8e88b649c5ab9e8d4b9b07f6495820a0af19a`). `quote_checks.py` (in the series folder) reports which double-quoted strings of this reading occur in the paper's text layer; strings that did not match were rewritten as paraphrases or corrected to the paper's wording before publication. The paper's PDF is not stored here; the preregistration and the scripts are.
- No predictions file: this reading was post hoc.

## References

Sources: the paper named in the scope line above (PDF sha256 `cf088d4c980c858bdf7c4d16f0c8e88b649c5ab9e8d4b9b07f6495820a0af19a`); the numbers recomputed in the scripts are transcribed from its tables.

## Revision log

- *2026-10-26, v1.* First public version, from the reader's working notes of 2026-10-25. Quotation marks were removed from, or corrected in, phrases that did not match the paper verbatim; cross-references to working notes and workflow remarks were not carried over.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
