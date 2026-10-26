# Where the Margin Comes From: Reading IdeaScientist ("Orchestrating Agents for Grounded Scientific Ideation")

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one paper, "Orchestrating Agents for Grounded Scientific Ideation" (IdeaScientist, arXiv:2610.04074v2, 9 October 2026, dated 14 October; the paper names CMU and Meta). The authors are called "the authors"; organisations are named only as the paper names them. No individual is named and no intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance; one reader, an AI system. Read from an operator-supplied copy (36 pp; all pages read). Lens: the series overview (applied during reading). Same-source caveat: single Anthropic-model reader; the paper's frontier baseline includes an Anthropic model (Claude Code SDK, Claude-4.8-Opus). Post-hoc status: see the predictions file in this folder. No code or data run.

## What it is
Three-role ideation harness (gap finder, innovator, report writer + orchestrator), per-role LoRA GRPO on Qwen3.6-27B, over an offline 4.7M-paper store (Svalbard Idea Vault; 2.77M decomposed ideas). Cutoff 1 Jan 2026; 14,977 post-cutoff methodology papers split 14,500 / 200 / 277 (train/val/test). Reward = 0.85 x gated(mean of reference-free, reference-grounded, citation-F1) + 0.15 x protocol. Evaluation: LLM-judged novelty (All / Cutoff / In-domain) and six quality dimensions; Overall = mean(novelty Avg, quality Avg).

## Flags (ranked; post-hoc)
1. **Headline margin rides on one judged term that restates the method.** In-domain novelty = binary judgment that the proposal imports a mechanism from another setting and names the shared structure; the innovator is instructed to retrieve cross-domain; baselines' schema (Table 5) does not ask for it. In-domain is 1/3 of novelty Avg and ~75% of Base's novelty-Avg gap over DeepScientist; its overall-score contribution to each headline gap is 8.5-9.3 points. Ex-In-domain overall, (mean(All,Cutoff)+Quality Avg)/2: Trained 74.1 vs Claude Code SDK 77.4 (-3.3), Codex SDK 78.2 (-4.2), DeepScientist 67.8 (+6.3). On GPT-5.4, Base is below Codex SDK on All (-4.6), Cutoff (-4.3) and quality Avg (-1.6). The abstract's claim that IdeaScientist outperforms Claude Code and Codex depends entirely on In-domain; the open-baseline lead survives without it at reduced size.
2. **RL gain small and judged by its own optimiser.** Trained - Base: overall +1.1, quality +0.4, novelty +1.9, no CI, one run. 12.9 of the 14.0 headline points are Base vs DeepScientist. Qwen3.6-27B is backbone, 99.8% of reference-artifact author, reward judge, and sole Table 1 judge. Human pairwise (50 papers, 2 annotators): Trained beats Base 57% (not significant), beats DeepScientist 43%; the paper lists DeepScientist as the one non-significant exception, which is the strongest baseline the 14.0% is measured against.
3. **Alignment to later human work is claimed, not compared.** Abstract: evaluation "assesses how closely proposed directions align with those later explored". Table 1 has no target-alignment metric; the only alignment numbers (Table 12: reference-grounded 0.299, citation F1 0.045) are for Trained, with no baseline. Whether the target paper is excluded from the "All" novelty comparison set is not stated (training rewards matching it; evaluation rewards distance from the literature).
4. **Temporal-holdout claim does not hold for the trained model.** Splits are random within the same post-cutoff window, so concurrent same-topic work is in training. Cutoff limits retrieval only; all five models released after the cutoff (Table 10). Contamination probe is title-only, 50 queries; authors state it cannot detect paraphrased or method-level memory.
5. **Judge validation not like-for-like.** Judge-vs-mean-of-two-humans r (0.51-0.59, top three) is set against single human-vs-human r = 0.56; the averaged reference is more reliable, inflating r. Self-preference is measured on generation systems, not on a policy optimised against that judge. No Table 1 re-score under another judge is shown; cross-judge checks are on 50 proposals.
6. **Smaller.** F.4 compares reported vs superseded checkpoints on the full test split while E.1 says the test split is only for final evaluation (selection basis unclear). One run per system, no seeds/CIs in Table 1; failed runs (Claude Code 5, Codex 8) not stated to score zero. Case studies selected and qualitative.

## Holds
Role-wise ablation (Fig 3); cross-domain retrieval raises novelty on every measure (partly definitional for In-domain); reward-hacking disclosure (pairwise innovator reward drifted toward length, ~0.83, absolute rubric stable ~0.66); contamination and limitation paragraphs; compute sweep (Fig 6).

## Checks (`checks.py`, `checks_output.txt`)
Identities hold on 8 transcribed rows (max residual 0.05). Trained minus: Claude Code +5.9 (In-domain term worth 9.0; ex-In-domain -3.3), Codex +5.1 (8.5; -4.2), DeepScientist +14.0 (9.3; +6.3), AI-Researcher +15.2 (8.6; +8.6). Trained - Base: overall +1.1.

## Open
Not run: the harness (github.com/jiarui-liu/IdeaScientist) and dataset. Unread: nothing in the PDF. Not checked: whether Table 1 baselines were scored zero on failed runs; whether the target paper sits in the "All" comparison set; per-judge Table 1 re-score (not published).

## Evidence tier and deeper-pass flag (added 2026-10-25)
**Tier:** E2 read (all 36 pp). E1 on reported Table 1 rows: score identities and In-domain decomposition (checks.py). E3: flag 2 (judge independence) and flag 4 (temporal-split claim) are interpretation.
**Deeper pass:** recommended. Headline depends on flag 1 (In-domain term) and flag 2 (same judge trains and evaluates); code and the Idea Vault dataset are public. Cheapest decisive test: re-score released Trained / Base / baseline proposals with a judge that did not touch training and without the In-domain term. Not done; repo and data not accessed.

## Limitations: what this does and does not establish

- One reader, an AI system, reading a paper and its tables; the flags above are leads, each tied to a page or table, not verdicts, and a paper may answer them in places not read (see what was read and not read at the top and under Open).
- The number of flags is not a severity ranking (see the series overview).
- Evidence classes: E1 executed here (scripts and their outputs in this folder), E2 read, E3 interpretation, as marked in the text.

## Reproduction

Everything is in `benchmark_validity_readings_v1/ideascientist_ideation_agent/`: `predictions_fixed_2026-10-25.md`; `checks.py`; `checks_output.txt`; `quote_checks_output.txt`; `tool_scan_*.json`. Re-fetched from arXiv on 2026-10-26: the file is byte-identical (sha256 `f1e4954c2de02ba477ad3f18a1475fe1362aebe30a5e66feb0ccae4618fe3b37`). `quote_checks.py` (in the series folder) reports which double-quoted strings of this reading occur in the paper's text layer; strings that did not match were rewritten as paraphrases or corrected to the paper's wording before publication. The paper's PDF is not stored here; the preregistration and the scripts are.
- **Predictions** were fixed before the measurement they concern (`predictions_fixed_2026-10-25.md`); that order is the evaluator's own record and is not independently timestamped.

## References

Sources: the paper named in the scope line above (PDF sha256 `f1e4954c2de02ba477ad3f18a1475fe1362aebe30a5e66feb0ccae4618fe3b37`); the numbers recomputed in the scripts are transcribed from its tables.

## Revision log

- *2026-10-26, v1.* First public version, from the reader's working notes of 2026-10-25. Quotation marks were removed from, or corrected in, phrases that did not match the paper verbatim; cross-references to working notes and workflow remarks were not carried over.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
