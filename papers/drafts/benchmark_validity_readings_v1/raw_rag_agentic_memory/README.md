# Naive RAG Against Twelve Memory Systems: Reading "Is Complex Agentic Memory Always Needed?"

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one paper, "Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought" (RAW-RAG, arXiv:2610.30755v1, 22 October 2026; the paper names Xi'an Jiaotong, SJTU, Zhejiang and CUHK). The authors are called "the authors"; organisations are named only as the paper names them. No individual is named and no intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance; one reader, an AI system. Read from an operator-supplied copy (62 pp). Read: body, Appendices A (settings and results), B (method), C (partly), D.2-D.7 (workflow, baseline configurations, latency), E (review of prior RAG baselines), F (limitations, partly). Not read in full: prompt appendix G, benchmark descriptions in D.1, procedures in C. Figures read only as extracted text. Repository (github.com/Litmeb/RAW-RAG) seen as a landing page via the fetch tool, second-hand; not cloned, not run. Lens: the series overview. Same-source caveat: single Anthropic-model reader; no Anthropic model is an evaluated reader. Post-hoc; see the predictions file in this folder.

## What it is
RAW-RAG: 256-token windows (32 overlap) over timestamped raw history, dense retrieval of 128, cross-encoder rerank to 15, expanded to complete turns, to a reader. Compared with 12 memory systems on LoCoMo, LongMemEval, MEME, MemoryAgentBench (seven benchmark-reader settings) plus PersonaMem-v2 (appendix). Diagnostics: Mem0 mutation audit, coverage vs utilization, complete-store oracle, ablations, cost and latency. Claim: first among compared memory systems in six of seven settings; "challenge the necessity of complex agentic memory for the evaluated conversation tasks".

## Corrections to an earlier informal first pass (2026-10-26)
- First pass said the LoCoMo leads (0.65-0.95) sit near the noise floor. Table 3 mixes retrieval stacks: RAW-RAG's row (text-embedding-3-small + Cohere) is set against EverMemOS's published Qwen3-setting score. Matched appendix leads are 0.95 and 2.01 over MemMachine (Table 10) and 2.37 and 1.50 over EverMemOS (Table 11), 3-8x the paper's 0.28 unchanged-context variability (C3).
- First pass treated the 0.13 LongMemEval lead as a general tie. It is against Memora's published policy-retriever number; under the matched Qwen3 setting the lead over EverMemOS is 6.93, and on the non-abstention set 2.9-7.57 (C3).

## Flags (ranked; post-hoc)
1. **On MEME, RAW-RAG is behind the best compared system on most dynamic tasks.** Against the best of EMem / MemMachine / Memora (a lower bound on the best baseline): aggregation -17 and -15, deletion -11 and -19, cascade -2.44 and -5.49, invalidation -0.77 and -1.54 (GPT-4o-mini and DeepSeek). It ties or wins only on exact recall and tracking. With DeepSeek, deletion is 86% under phase-visible raw oracle evidence and 29% under RAW-RAG retrieval (Table 2 vs Table 4): the gap is retrieval, not state resolution. First place on GPT-4o-mini MEME is a macro-average effect (C1).
2. **The MemoryAgentBench lead is mostly one capability.** Against Memora the 4.48 and 5.53 leads decompose into Conflict Resolution contributions of 78% and 90%; RAW-RAG is at or below Memora on Accurate Retrieval and Test-Time Learning on GPT-4o-mini and about tied on DeepSeek (C2). Its CR configuration is benchmark-adapted (one fact per chunk, no overlap, serial-number cues preserved, turn expansion disabled); baselines run native configurations.
3. **RAW-RAG is task-adapted and sits in EverMemOS's harness.** MEME evidence in source order; per-source chunking on MemoryAgentBench; implementation under `methods/EverCore/evaluation`. The EverMemOS comparison is the most like-for-like; the others are looser (published baseline scores retained; readers, judges and budgets differ).
4. **Metric disagreement on short answers (Table 12, GPT-4.1-mini).** RAW-RAG (minimal) vs Nemori: judge accuracy +11.47, token F1 -3.83, BLEU-1 -4.25; on GPT-4o-mini it leads on all three (C5). Prior "RAG" baselines (30.20 / 32.90 in Nemori's table) vs 85.78 / 90.87 here confound retrieval strength with reader prompt and judge; the paper's own review labels its diagnoses "not controlled estimates".
5. **Headline count omits PersonaMem-v2.** Appendix A.3: RAW-RAG 49.62, third of seven (EverMemOS 53.25 with profile, MemOS 50.72); significance untested; at n = 5,000 the EverMemOS gap (3.63) is well outside the ~0.7 pp standard error, MemOS's (1.1) borderline (C7).
6. **Winning among weak systems on dynamic MEME tasks.** RAW-RAG GPT-4o-mini cascade 4.27%, aggregation 19%, deletion 26%. Reader dependence is large (phase-visible oracle overall 50.50 / 70.25 / 85.48 for GPT-4o-mini / Qwen3.5 / DeepSeek); the paper states this.
7. **Single-system diagnostics generalised.** The mutation audit is Mem0 only (4.39% of 33,902 and 2.46% of 428,858 write decisions; effective 1.90% and 1.34%; ADD/NONE-only +2.06 on LoCoMo) and uses Mem0 1.0.11 while the main evaluation uses 2.0.11; whether 2.0.x keeps the same operations is not stated.
8. **Ablation arms are the authors' constructions** (atomic facts, raw summary, graph expansion); atomic facts cut Test-Time Learning from 47.68 to 15.37, consistent with extraction destroying in-context demonstrations.
9. **Cost claims exclude the reader.** Ingestion and search only; RAW-RAG supplies about 4.8k (LoCoMo), 11.4k (LongMemEval), 12.0k (MEME) evidence tokens per question at default settings. The cross-system 5,000-token cap is on MemoryAgentBench only (six systems); the other three benchmarks cap RAW-RAG alone. Latency on one Windows laptop with API endpoints and self-hosted Docker services.
10. **Inherited baseline inconsistency.** Mem0's published LoCoMo category scores weight to 62.14 against a published 66.88 (the paper reports this; Table 3 carries 66.88) (C6).
11. **"Naive" is rhetorical.** Standard good practice; removing the reranker costs 3.92 points (Holm p = 0.0012), k = 1 costs 11.73.

## Holds
Matched-setting appendix tables; three judge repetitions; paired source-stratified bootstrap with Holm correction on the ablations; retrieval-depth sweep; MemoryAgentBench cross-system cap; complete-store oracle; an independent LoCoMo reproduction linked from the README reports 88.68 / 93.48 (within 0.39 and 0.22; leads over the best compared system 0.56 and 0.43; second-hand) (C4); the paper flags the Mem0 inconsistency itself; explicit limitations (offline benchmarks, privacy and deletion, reader dependence).

## Evidence tier and deeper-pass flag
**Tier:** E2 read (main text and most appendices; prompts and benchmark descriptions not read in full; repository landing page second-hand). E1 on transcribed table values: leads, per-task and per-capability decompositions, noise-floor comparison (checks.py). E3: flags 3, 4 and 11 are interpretation.
**Deeper pass:** done to the reading tier on 2026-10-26. Remaining decisive test: rerun all baselines and RAW-RAG under one reader, judge, retrieval budget and seed set on MEME and MemoryAgentBench, with RAW-RAG's benchmark adaptations ablated one at a time. Needs a repository clone, API keys and datasets. Not done.

## Open
Appendix G prompts; whether the repository commits per-question outputs; which baselines the repository's setup helpers cover; whether Mem0 2.0.x retains UPDATE/DELETE; the other MEME baselines in the per-task comparison (MemU, EverMemOS, MemOS, Mem0).

## Limitations: what this does and does not establish

- One reader, an AI system, reading a paper and its tables; the flags above are leads, each tied to a page or table, not verdicts, and a paper may answer them in places not read (see what was read and not read at the top and under Open).
- The number of flags is not a severity ranking (see the series overview).
- Evidence classes: E1 executed here (scripts and their outputs in this folder), E2 read, E3 interpretation, as marked in the text.

## Reproduction

Everything is in `benchmark_validity_readings_v1/raw_rag_agentic_memory/`: `predictions_fixed_2026-10-26.md`; `checks.py`; `checks_output.txt`; `quote_checks_output.txt`; `tool_scan_*.json`. Re-fetched from arXiv on 2026-10-26: the file is byte-identical (sha256 `7e5d208d9af9a44f3ad1e65b57576e0ddb9855330e16340c5d0063193366a042`). `quote_checks.py` (in the series folder) reports which double-quoted strings of this reading occur in the paper's text layer; strings that did not match were rewritten as paraphrases or corrected to the paper's wording before publication. The paper's PDF is not stored here; the preregistration and the scripts are.
- **Predictions** were fixed before the measurement they concern (`predictions_fixed_2026-10-26.md`); that order is the evaluator's own record and is not independently timestamped.

## References

Sources: the paper named in the scope line above (PDF sha256 `7e5d208d9af9a44f3ad1e65b57576e0ddb9855330e16340c5d0063193366a042`); the numbers recomputed in the scripts are transcribed from its tables.

## Revision log

- *2026-10-26, v1.* First public version, from the reader's working notes of 2026-10-26. Quotation marks were removed from, or corrected in, phrases that did not match the paper verbatim; cross-references to working notes and workflow remarks were not carried over.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
