# An Honest, Scoped Paper: Reading "Reasoning with Neural Cellular Automata"

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one paper, "Reasoning with Neural Cellular Automata" (arXiv:2609.36126v1, 28 September 2026; the paper names Google Paradigms of Intelligence, McGill, Mila and Geneva). The authors are called "the authors"; organisations are named only as the paper names them. No individual is named and no intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance; one reader, an AI system. Read from an operator-supplied copy (29 pp). Read: full main text, Table 1 baselines, Appendices A-C (benchmarks, architecture, training, test-time protocol, FLOPs estimation). Figures read by caption only. Lens: the series overview. Same-source caveat: single Anthropic-model reader. Post-hoc; see the predictions file in this folder. Code and data not accessed. **Contrast case.** Read alongside the RAW-RAG reading (`raw_rag_agentic_memory/`): an honest paper whose flags are scope and reading detail, not claims outrunning tables. The paper says "Our objective is not to establish new state-of-the-art results", places baselines that beat it in the same table, and states its limits (non-local training, random-search exploration, propagation delays, implementation-dependent FLOPs, unstable Visual Sudoku training). Do not read the flag count as severity (series overview, section on reading the flag counts).

## What it is
NCAs: recurrent grids, each cell sees its 3x3 neighbourhood, asynchronous Bernoulli firing, weight-tied update. Benchmarks: Maze-OOD, Maze-Hard, Sudoku-OOD, Sudoku-Extreme, ARC-AGI-1, Visual Sudoku (pixel space). Training: BPTT with sample replay and perturbations (noise, damage, target swap). Test-time scaling: parallel stochastic rollouts (K), longer rollouts (D), larger grids, and Niche-Capped Diversity Pruning.

## Holds
- Maze-OOD: 100% from 13x13 to 201x201, trained on 9x9 (about 3 minutes on a TPU); 201x201 at 11.8T FLOPs vs DeepThink 74.0% at 521.7T (44x) (C2). "500x larger" is by area (C2).
- Sudoku-OOD: K=1 66.1% vs AKOrN 51.7% with 160K vs 3M parameters; confidence-selected 98.5% vs 89.5% at 23.9T vs 97.3T (C4).
- Maze-Hard: 86.6% vs PTRM 83.8% on A* at K=1 (about 250x fewer FLOPs, 12.5x more steps); 89.2% vs 86.7% at larger K (C3).
- Ablations over 3 training seeds: perturbations plus sample replay matter for out-of-distribution generalization; asynchronous updates matter for Sudoku.
- Candour as listed above; baselines run from official code with a cross-framework FLOPs validation (under 3%).

## Flags (ranked; post-hoc)
1. **"Strictly local" applies to the update rule, not the pipeline.** Within a rollout cells see only 3x3 neighbours (the "fixed attention" is position-specific 3x3). The high-K accuracies depend on central steps: board-confidence selection among up to K=2048 rollouts, ARC majority voting, ensemble pruning, ARC per-task test-time fine-tuning (51 augmentations, backpropagation over demonstration pairs) and a global task embedding at the start. The fully local figures are the K=1 rows (Sudoku-OOD 66.1%, Sudoku-Extreme 75.6%).
2. **ARC-AGI-1 trails LoopViT at higher cost.** NCA 48.8% pass@2 (K=3264, 2.4P FLOPs), NCA ensemble 51.3% (7.1P), against LoopViT-s/m/l 60.1/63.8/65.8% (80.1T/132.7T/220.5T): the single NCA uses about 11-30x the FLOPs for lower accuracy and the ensemble about 32-89x (C1). It beats TRM (44.6%, K=1000, 3.8P). The 60.3% pass@64 is not comparable with ARC's pass@2 scoring.
3. **Sudoku-Extreme is behind PTRM** at K=1 (75.6 vs 87.3) and at confidence-selected scale (92.7 vs 98.8, 190.1T vs 164.0T FLOPs) (C5).
4. **FLOPs stand in for unmeasured energy and hardware gains.** The decentralised-hardware framing is aspirational; counts ignore latency (201x201 mazes need D=13,000 sequential steps vs 2,000) and memory behaviour (the paper notes the limits).
5. **Maze-Hard accuracy depends on the reference solver:** 86.6% against A* targets, 94.7% against BFS; only the A* row is like-for-like with PTRM.
6. **Interpretability evidence is qualitative** (backtracking, "trial-and-error", "spatial chain-of-thought" from selected trajectories); hedged ("seemingly exact"); the maze algorithm has quantitative support (100% at 201x201); Sudoku dynamics are not quantified.
7. **Two robustness claims rest on few benchmarks and 3 seeds:** test-time noise improves accuracy "across all benchmarks and noise scales" (one figure); adaptive compute (about 30% fewer cell updates, damage recovery) is shown on Maze-OOD 201x201 only. No intervals.
8. **Abstract's pixel-space claim is milder in the text:** 87.8% easy (in-distribution), 18.9% hard (out-of-distribution), described as a "proof-of-concept".
9. **Table 1 has no intervals.** About 400 ARC tasks gives a standard error near 2.5 points (C6); the NCA-TRM gap is 4.2.

## Correction to an earlier informal evaluation (2026-10-26)
The earlier informal evaluation said the ARC compute gap was "roughly 11-32x". The recomputed ratios (C1) are 10.9-30.0x for the single NCA (2.4P) and 32.2-88.6x for the ensemble (7.1P), against LoopViT-l and LoopViT-s respectively.

## Evidence tier and deeper-pass flag
**Tier:** E2 read (main text and Appendices A-C; figures by caption). E1 on Table 1 values (FLOPs ratios and accuracy gaps, checks.py). E3: flags 1, 4 and 6 are interpretation.
**Deeper pass:** not warranted unless the ARC numbers are relied on. If so: rerun the authors' ARC pipeline with K varied and per-task test-time fine-tuning off, to separate the local update rule from the central pieces. Not done.

## Open
Appendix A benchmark details beyond what Table 1 reports; Figure S3 (ARC transfer) and Figure S15 (TRM dynamics); whether code is released.

## Limitations: what this does and does not establish

- One reader, an AI system, reading a paper and its tables; the flags above are leads, each tied to a page or table, not verdicts, and a paper may answer them in places not read (see what was read and not read at the top and under Open).
- The number of flags is not a severity ranking (see the series overview).
- Evidence classes: E1 executed here (scripts and their outputs in this folder), E2 read, E3 interpretation, as marked in the text.

## Reproduction

Everything is in `benchmark_validity_readings_v1/nca_reasoning/`: `predictions_fixed_2026-10-26.md`; `checks.py`; `checks_output.txt`; `quote_checks_output.txt`; `tool_scan_*.json`. Re-fetched from arXiv on 2026-10-26: the bytes differ (stored file sha256 `576eb670aeecc744153d0b9d2f803d0e55ad2f6cd32141b0b02eb70d63ccae59`, current file sha256 beginning `25f8f81eacf251ce`), but the extracted text is word-for-word identical (29 pages each). `quote_checks.py` (in the series folder) reports which double-quoted strings of this reading occur in the paper's text layer; strings that did not match were rewritten as paraphrases or corrected to the paper's wording before publication. The paper's PDF is not stored here; the preregistration and the scripts are.
- **Predictions** were fixed before the measurement they concern (`predictions_fixed_2026-10-26.md`); that order is the evaluator's own record and is not independently timestamped.

## References

Sources: the paper named in the scope line above (PDF sha256 `576eb670aeecc744153d0b9d2f803d0e55ad2f6cd32141b0b02eb70d63ccae59`); the numbers recomputed in the scripts are transcribed from its tables.

## Revision log

- *2026-10-26, v1.* First public version, from the reader's working notes of 2026-10-26. Quotation marks were removed from, or corrected in, phrases that did not match the paper verbatim; cross-references to working notes and workflow remarks were not carried over.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
