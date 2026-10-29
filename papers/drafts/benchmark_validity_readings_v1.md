# Benchmark-Validity Readings: Twelve Papers Read for Whether the Score Supports the Inference Drawn From It

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** Twelve papers (eleven posted in October 2026 and one in late September 2026) are each read in their own folder, `benchmark_validity_readings_v1/<name>/README.md`. Authors are called "the authors" and are not named; organisations are named only as each paper names them. No intent is attributed to anyone. A thirteenth reading, of a working paper with no stable public copy, is not included (section 7).

**Disclosure.** Drafted with AI assistance. One reader, an AI system, wrote every reading, and the reader is an Anthropic model; where a paper evaluates Anthropic models or has Anthropic-affiliated authors, the individual reading says so. Readings are post hoc unless the folder holds a predictions file.

## 1. What this series is

Papers about whether a benchmark score supports the inference drawn from it: construct validity, dimensionality, differential functioning, saturation, scorer and judge independence, aggregation, contamination. It does not cover studies of how a harness changes scores (one entry, `continual_self_evolving_agents/`, reads such a paper only for whether its metrics support its claim), and it does not cover vendor capability posts.

## 2. Entries

| Reading | Paper | Main finding for the series |
|---|---|---|
| [`harmbench_psychometric_audit/`](benchmark_validity_readings_v1/harmbench_psychometric_audit/README.md) | arXiv 2610.12409v1 (CMU / Indiana / Google) | HarmBench in HELM Safety needs > 1 latent dimension (robust within its design); target construct is authors' own; DIF test mostly restates the dimensionality test; judge-family confound unexamined |
| [`theophyseval_physics_agents/`](benchmark_validity_readings_v1/theophyseval_physics_agents/README.md) | arXiv 2610.16733v1 (TheoPhysEval; 50 physics problems, 5 agents) | Headline (98%, matches experts, memorised literature) rests on one run of 50 network-sourced items at the ceiling; key revised toward the top agent after the fact; two keys widened to observed conventions; the one failure is a pun; memorisation inferred from a null track difference; table is perfectly nested (top two differ on 3 items); no human baseline |
| [`fde_gym_delivery_benchmark/`](benchmark_validity_readings_v1/fde_gym_delivery_benchmark/README.md) | arXiv 2610.22350v1 (FDE-Gym; 95 tasks, 13 configurations) | Score = uplift minus an author-set, undisclosed contact cost; L0->L1 'constraint discovery' drop also removes scoring info and is ~29-61% contact cost; admission anchors self-validate and the discard rate is unreported; CIs over clustered tasks; 'resolved' sits on the shortcut ceiling; budget truncation read as capability |
| [`ideascientist_ideation_agent/`](benchmark_validity_readings_v1/ideascientist_ideation_agent/README.md) | arXiv 2610.04074v2 (IdeaScientist; Qwen3.6-27B, 277 test papers) | Headline margin over frontier agents comes entirely from an In-domain novelty term that restates the method (ex-term: -3.3 / -4.2 vs Claude Code / Codex); RL gain +1.1 overall, judged by its own reward judge; humans do not prefer it to the strongest baseline (43%); alignment-to-target claimed in abstract, not compared; random split within the cutoff window |
| [`memoprobench_proactive_memory/`](benchmark_validity_readings_v1/memoprobench_proactive_memory/README.md) | arXiv 2610.22671v2 (MemoProBench; 800 test clips, synthetic 618K-token memories) | 2x2 'content x timing' collapse is partly metric-by-construction (always-visible evidence + one-fire rule); largest harness gain is the speaking-history signal; train/test share one synthetic generator; content judge unvalidated in text read |
| [`metric_space_accuracy_bounds/`](benchmark_validity_readings_v1/metric_space_accuracy_bounds/README.md) | arXiv 2610.22564v1 (average kernel size; accuracy/error intervals) | Interval holds on a constructed dataset set by a chosen metric and quantile threshold, not on the data; CIFAR-10 upper limit 91.9% is a metric artifact; admissible-set assumption untestable; theory is standard identities; interval width is 2x by construction |
| [`pairwise_difference_uq/`](benchmark_validity_readings_v1/pairwise_difference_uq/README.md) | arXiv 2610.21554v1 (PDL classifier; uncertainty quantification) | UQ headline is a 'gamma' defined as C/(C+D) (cannot be negative, contradicts reported negatives), compared median vs mean; EU scored against a proxy; t-tests over non-independent CV runs; 'unique contribution' is an oracle max over test scores |
| [`latent_cot_taxonomy/`](benchmark_validity_readings_v1/latent_cot_taxonomy/README.md) | arXiv 2610.21182v1 (latent CoT taxonomy; Coconut / CODI / SIM-CoT on GPT-2, Llama-1B) | Readability and use dissociate (well supported); 'predictive' taxonomy is largely definitional and cannot be contradicted by cells it leaves unclassified; main supervision comparison has a control on one cell; sample size enlarged after a near-threshold read; backbone effect has n = 2 |
| [`raw_rag_agentic_memory/`](benchmark_validity_readings_v1/raw_rag_agentic_memory/README.md) | arXiv 2610.30755v1 (RAW-RAG vs 12 memory systems) | Overall-rank claim holds on LoCoMo / LongMemEval in matched settings (0.95-6.93); on MEME RAW-RAG trails the best compared system on aggregation, deletion, cascade, invalidation; MemoryAgentBench lead is 78-90% Conflict Resolution under a benchmark-adapted configuration; main table mixes retrieval stacks; PersonaMem-v2 omitted from the 'six of seven' count |
| [`continual_self_evolving_agents/`](benchmark_validity_readings_v1/continual_self_evolving_agents/README.md) | arXiv 2610.25858v1 (Mila / Google DeepMind; three self-evolving methods, four drifting streams) | Plasticity-stability trade-off is partly an identity of the metrics (forgetting measured from the block-end peak, `S <= -(P - Term)`); no noise floor (null simulation about -0.9 to -1.6 pp vs several reported values); r = -0.72 reproduces over non-independent points; the shared-prompt overwriting mechanism is well documented; 'retrieval cannot prevent' heading rests on top-1, no threshold, one embedder |
| [`nca_reasoning/`](benchmark_validity_readings_v1/nca_reasoning/README.md) (contrast case) | arXiv 2609.36126v1 (neural cellular automata for mazes, Sudoku, ARC-AGI-1) | Honest, scoped; strongest on Maze-OOD (100% to 201x201, 44x fewer FLOPs) and Sudoku-OOD; 'strictly local' holds for the update rule, not the K-rollout selection, voting, pruning or ARC test-time fine-tuning; trails LoopViT on ARC at 11-30x the FLOPs and PTRM on Sudoku-Extreme; efficiency measured in FLOPs, not energy |
| [`mcp_injector_fault_tolerance/`](benchmark_validity_readings_v1/mcp_injector_fault_tolerance/README.md) (contrast case) | arXiv 2610.32555v1 (MCP-Injector; gpt-oss-20B vs -120B under calibrated faults) | Careful, well-controlled; title ('scale does not purchase fault tolerance') stronger than the abstract's two-model, one-setup scope with a wide CI and models indistinguishable at baseline; '60% degradation' belongs to a permanent-heavy stress profile; stack effect is suggestive (p = 0.048 / 0.074, no multiplicity correction) |

## 3. Reading lens (applied during reading, not preregistered)

1. Is the construct the benchmark's own claim or the evaluator's? 2. Can the check fail (a null, a preregistered scope)? 3. What does the audited quantity differ from the reported one by? 4. Which alternative explanation does each test fail to separate? 5. Scorer and judge independence from the compared groups. 6. Does the generalization in the abstract match the sample in the limitations?

## 4. Evidence tier and deeper-pass flag (convention from 2026-10-25)

Every reading ends with two lines. **Tier** states what it rests on: E1 executed (state what: arithmetic on the paper's reported numbers, a simulation, or the paper's own code or data), E2 read (state what was and was not read), E3 interpretation (name the flags that are interpretation). **Deeper pass** is `recommended`, `optional` or `no`, with the cheapest decisive test and whether it has been done. A deeper pass is recommended only when (a) a flag bears on the paper's headline claim, (b) the code or data needed is public, and (c) the test is small. A reading-only flag that settles the question (a metric defined against its own results) does not need one. Provenance caveat: the papers reached the reader mostly through reposts of abstracts, so counts of flags per reading describe that channel, not arXiv in general. The readings dated 2026-10-25 carry the lines retroactively.

## 5. Reading the flag counts

The number of flags in a reading is not a severity ranking. `raw_rag_agentic_memory/`, `nca_reasoning/` and `mcp_injector_fault_tolerance/` are the contrast cases. The RAW-RAG reading carries as many flags as the readings of papers whose claims outran their tables, but they are mostly scope and reporting detail on a paper that states its own limits (an inherited baseline inconsistency, untested significance, reader dependence). Read a reading by what its flags bear on (the headline claim, or the method's own reporting), not by how many there are.

## 6. Verification, and what is not claimed

- **Quoted strings.** `quote_checks.py` tests every double-quoted string in each reading against the text layer of the paper's PDF (three extraction orders, normalised quotes and dashes). Twelve of twelve readings pass after correction; before correction, many phrases that had been put in quotation marks were close paraphrases, and those were either restored to the paper's wording or unquoted. The result of the final run is in each folder as `quote_checks_output.txt`. A pass is a lexical test: it does not show the reading's interpretation is right.
- **Source files.** Eleven of the twelve arXiv PDFs re-fetched (ten on 2026-10-26, `continual_self_evolving_agents` on 2026-10-29) are byte-identical to the copies read; the twelfth (`nca_reasoning`) differs in bytes but is word-for-word identical in text.
- **Scripts.** Every `checks*.py` re-ran in this layout and reproduced its committed output.
- **Not done.** No paper's code or data was run unless a reading says so; figures were mostly read as extracted text; the flags are leads for a deeper pass, not verdicts.

## 7. Related, and one reading not included

Related public drafts: `validation_that_can_fail_v1.md` (published), `two_closed_paths_mutual_audit_v1.md`, `scientisttwo_release_reading_v1.md`, `jagged_judges_meta_protocol_grounding_v2.md` (published). `research_mcp_failure_semantics_probe_v1.md` follows up one finding of `mcp_injector_fault_tolerance/` on this repository's own server.

A reading of a working paper that compares AI and human peer reviews is held back: the copy read has no stable public address, and its supplementary appendix, which several findings depend on, was not in that copy. A reading nobody can check against the source does not meet this series' own bar.

## 8. Limitations: what this does and does not establish

- Twelve papers chosen by what reached the reader, not sampled; nothing here is a rate.
- One reader per paper; the same model family wrote the readings and, in some cases, is the subject.
- The series is a set of reading notes with scripts; it is not a literature review. An open item is a literature table for AI-judging-AI and benchmark-validity work, with inclusion criteria preregistered first.

## 9. Reproduction

`quote_checks.py` (needs `pdftotext` and the paper's PDF, which is not stored here); each folder's scripts; `tool_scan_*.json` for this overview.

## References

Sources: the twelve papers named in the scope lines of the readings (arXiv identifiers and PDF hashes are in each folder's README).

## Revision log

- *2026-10-26, v1.* First public version, from the reader's working notes of 2026-10-17 to 2026-10-26.
- *2026-10-29, v1.1.* Added `continual_self_evolving_agents/` (twelfth reading); counts in the scope line, section 6 and section 8 updated; one scope note in section 1. The earlier eleven readings are unchanged.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
