# Operating Points, Not Matched Utility: Reading "Steer2Edit" for Whether the Tables Support "Superior Attribute-Utility Trade-offs"

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** One paper, "Steer2Edit: From Activation Steering to Component-Level Editing" (arXiv:2602.09870v3, 4 Nov 2026, NeurIPS 2026 format; the paper names the University of California, San Diego). The authors are called "the authors". No individual is named and no intent is attributed.

**Disclosure.** Drafted with AI assistance; one reader, an AI system (an Anthropic model). The paper uses Claude Opus 4.6 as an alternative labeling judge in a robustness check (Appendix Q) and names Claude Sonnet 4.5 inside one baseline's own design (Appendix K), a same-vendor point; its main labeling judge is QwQ-32B. Read from an operator-supplied copy (37 pp.; PDF sha256 beginning f056f49afc130c96) via text extraction: the full body and appendices; figure plots were read through their captions only. The code repository named in the abstract was not retrieved or run.

## What it is
A closed-form method that turns a mean-difference steering vector into rank-1 edits of individual attention-head output projections and MLP down-projection neurons, with magnitudes from an Elastic-Net objective. Claimed "at matched downstream performance": gains over the strongest steering baseline of 17.2% (safety), 9.8% (truthfulness) and 12.2% (reasoning-length reduction), on 2B-8B models in the main text, with appendices on a 70B model, a vision-language model, a diffusion language model, fine-tuning, AlphaEdit, ASC, ITI and AUSteer baselines, an over-refusal benchmark and a labeling-judge swap.

## Flags (ranked; post hoc)
1. **The headline numbers are not derived, and the explicit comparisons are not utility-matched.** The three figures appear only in the abstract and the contributions list; no table or formula defines "matched". The 70B table's "+17.6" over the best steering configuration is 97.0 against 79.4 safety, but that steering configuration keeps 37.9 average utility against the edit's 35.7, and the edit takes utility from 51.8 to 35.7 (about -31%; CommonsenseQA 64.3 to 44.8, GSM8K 48.3 to 26.9). In the AUSteer comparison the edit has 88.2 safety at 28.0 utility against 77.2 at 30.2 for that method's trade-off configuration; the paper says the experiment "does not isolate the effect of intervention form with component selection held fixed". (E1 tables; differences E2)
2. **The reported best configurations give up benign-task accuracy that the main text describes as comparable.** LLaMA-2-7B-Chat: safety 49.9 to 88.2, utility 35.5 to 28.0 (about -21%). Qwen3-4B-Thinking, best configuration (Table 10): average accuracy 87.8 to 77.3, GPQA 66.3 to 42.4, MATH-500 97.7 to 89.7, reasoning length 5,319 to 3,387 tokens; the main text says the edit shortens traces "while maintaining comparable accuracy". The diffusion-model run (n=1) goes from 33.8 to 18.8 average utility. Which configurations the headline averages use is not stated. (E1; differences E2)
3. **Selection and the instrument.** Edit budgets and sparsity are ranked on the target-attribute metric over a "held-out small validation set", results correspond to "the best-performing configurations" unless noted, and the plotted baseline curves sweep one strength knob while the edit has three plus a hand filter (20 prompts) and a second-stage grid narrowed around promising regions. Safety is the refusal rate and the steering vector is built from refusals against benign helpful answers, so the metric measures the variable the construction pushes; the paper's own over-refusal benchmark finds over-refusal rising from 60.1% to 66.4% for the edit, and at matched over-refusal (about 66%) 88.1% safety against 60.5% for steering. ADVBench supplies both the vectors and the evaluation prompts; the split is not stated. (E1 text; reading E2)
4. **"Training-free" names the edit step.** Vectors come from labelled behaviour sets (refusals against Alpaca answers; model generations labelled truthful or hallucinated by a 32B judge; the shortest against longest 5% of GSM8K generations), and the strengths are then chosen by the target metric. The abstract mentions none of it. (E1)
5. **Baselines.** Fine-tuning baselines are trained on the same small positive sets with "comparable training budgets" (details not given) and are full fine-tuning and rank-1 LoRA only; AlphaEdit is adapted to one layer and does nothing; ASC runs with a KL-calibrated strength that changes nothing. Each could be a weak implementation as much as a property of the method. (E1; reading E2)
6. **No uncertainty and no durability.** No intervals or seeds anywhere (one +- column in the judge-swap table); table captions carry n=10, n=3 and n=1 without a definition in the text read. No relearning, fine-tune-recovery or adaptive-attack test of the edited models. (E1)
7. **Interpretability restates the method's own scores.** The edit coefficients come from cosine scores and the Elastic-Net, with a component class switched off by the coarse search; reading attention-dominated safety edits and MLP-dominated efficiency edits as circuit structure rests on varying the same budgets, with no independent patching or ablation reported. (E1/E2)

## What holds
Steering vectors are shared verbatim between the baselines and the edit; the search ranges are given in full; over-refusal, a second hallucination benchmark and a labeling-judge swap (the two judges agree on 342 of 408 candidates, 83.8%, which the paper says measures consistency, not correctness) are reported; ablations include variants that fail badly; the AUSteer comparison states what it does not isolate; the search costs minutes; code is linked; the broader-impact paragraph names dual use. Every arithmetic difference above recomputes from the quoted entries.

## Depth rating (rubric in the series overview)
3.0 (D2; claim reach medium). Non-blind: rated by the same reader after the rubric and table existed.

## Limitations: what this does and does not establish
It establishes that the paper's tables show the edit reaching higher refusal, truthfulness-preference and shorter reasoning than the steering baselines at operating points that cost benign-task accuracy, with strengths chosen on the target metric, and that the abstract's three gains are not derived in the paper. It does not establish that a matched-utility comparison would erase the advantage, that the method fails, or anything about code behaviour (not run).

**Tier:** E1 executed (differences and agreement counts recomputed in `checks_arithmetic_added_papers.py` from typed table entries); E2 read (all 37 pages as text, plots by caption); E3 interpretation (flags 3 and 7 readings). The three tools found no structural or severe gaps; attractor-scan's weak flag (the word "safety") was read and is the paper's own measured quantity (refusal rate), not laundering.
**Deeper pass:** recommended: a utility-matched comparison fixed in advance, with a random-direction control and repeated decoding. Not done.

## Reproduction
`checks_arithmetic_added_papers.py` and its output; `quote_checks_output.txt`; `tool_scan_*.json`.

## References
Sources: arXiv:2602.09870v3 (PDF sha256 beginning f056f49afc130c96); the numbers in `checks_arithmetic_added_papers.py` are typed from its appendix Tables 8-17.

## Revision log
- *2026-11-09, v1.* Added to the series.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
