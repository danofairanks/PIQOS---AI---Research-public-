# A Strategy Selected Per Benchmark: Reading "SOLAR" for Whether the Table Supports "Lifelong, Open-Ended" Adaptation

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** One paper, "SOLAR: A Self-Optimizing Open-Ended Autonomous Agent for Lifelong Learning and Continual Adaptation" (arXiv:2605.20189v1; a workshop paper at the Streaming Continual Learning Bridge, AAAI-26, per its footnote; the paper names the National University of Singapore and the Indian Institute of Science). The authors are called "the authors". No individual is named and no intent is attributed.

**Disclosure.** AI-assisted (Claude, working under this project's own non-default standard; direction, selection and release decisions are the operator's); single reader. The paper's generative-AI declaration lists GPT-5.2, Claude Opus 4.5 and Gemini-3 as writing aids, including to generate the literature review and images. Read from an operator-supplied copy (8 pp.; PDF sha256 beginning 0234b31559f029ad) via text extraction: the full body and references; no code release was reachable.

## What it is
Qwen2.5-0.5B-Instruct; a convolutional decoder generates LoRA adapters from prompt embeddings; a language model proposes JSON "adaptation strategies" (test-time training, LoRA merging, ensemble or router inference, activation-space tweaks) from a hand-built knowledge base; results on five in-domain and five out-of-domain benchmarks against four baselines.

## Flags (ranked; post hoc)
1. **What was run is smaller than what is described.** The method has three reinforcement-learning levels; the results are the first only (Table 1 caption; the text says further levels would follow if completed). The seed strategies were "cherry-picked via trial and error"; sampling is 15 samples and 2 iterations. The title and abstract (lifelong, open-ended, evolving knowledge base) describe more than Table 1 tests. (E1)
2. **A different strategy is chosen for each evaluation dataset; each baseline is one fixed method.** The winning strategies are listed per dataset (test-time training, activation-space, LoRA mixing, ensemble inference over up to 20 adapter batches), selected by reward on the evaluation metric; the cost (ensemble inference; up to four days of training on two GPUs) is not compared with the baselines. (E1 text; that selection used the reported split is E2, since an evaluation split is made "if available" and otherwise generated on the fly)
3. **Baselines at or below chance.** BoolQ (yes/no): LoRA 14.7, DOM 33.2, TTL 44.4; PIQA: DOM 18.8, DnD 47.8; ARC-e and ARC-c for TTL about 25 (chance for four options). A binary task scored at 14.7% indicates an output-format failure; the largest gaps (up to +44 points against LoRA on BoolQ) are partly a harness effect. (E1; reading of cause is E2)
4. **No intervals, run counts or seeds** for Table 1; the prompt-selection ablation reports one number (0.3 points).
5. **Untested motivation.** The paper posits that predictable weight-modification patterns exist; the student-notes analogy is motivation, not evidence.

## What holds
Table 1's averages and every delta recompute (in-domain 59.5 against 49.0 for the best baseline; out-of-domain 34.1 against 26.8); the paper is explicit about being an initial version; footnotes disclose the cherry-picking and the model-size workaround for structured outputs.

## Depth rating (rubric in the series overview)
1.5 (D1; claim reach wide).

## Limitations: what this does and does not establish
It establishes that Table 1 supports an initial, partly selected, harness-sensitive comparison on one small model. It does not establish that the method fails at higher levels or on other models, or that the baselines would stay at chance with the output format fixed; no code was available.

**Tier:** E1 executed (Table 1 recomputed); E2 read (full text; no code); E3 interpretation (flag 3's cause).
**Deeper pass:** recommended if code appears: rerun the baselines with the output format fixed. Not done.

## Reproduction
`checks_arithmetic.py`; `quote_checks_output.txt`; `tool_scan_*.json`.

## References
Sources: arXiv:2605.20189v1 (PDF sha256 beginning 0234b31559f029ad); the numbers recomputed in `checks_arithmetic.py` are typed from its Table 1.

## Revision log
- *2026-11-09, v1 (pre-draft).* Private pre-build.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
