# A Stability Metric Measured From the Peak: Reading "Are Self-Evolving Agents Continual Learners?"

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one paper, "Are Self-Evolving Agents Continual Learners?" (arXiv:2610.25858v1, 19 October 2026; the paper names Mila, Université de Montréal and Google DeepMind). The authors are called "the authors"; organisations are named only as the paper names them. No individual is named and no intent is attributed to anyone. This paper studies how self-editing harnesses behave on shifting task streams, which is outside the series' usual scope; it is read here only for whether its plasticity and stability metrics support the trade-off it reports, not for how a harness changes scores.

**Disclosure.** Drafted with AI assistance; one reader, an AI system (an Anthropic model; the paper does not evaluate Anthropic models, its backbone is a Google model). Read from an operator-supplied copy (24 pp; byte-identical to the arXiv file when re-fetched on 2026-10-29, sha256 `e686b84dad4c9b1b145b99a16e198a3e4d00f01de4c63693b39100d89f293617`). Read via text extraction: full body and Appendices A-E; figures read from captions and text only, not visually inspected. Code and data not accessed (no release is stated in the text read). Predictions fixed before the body was read: `predictions_fixed_2026-10-29.md`.

## What it is
Four drifting streams (topic, workflow, domain, compound) from BIRD, BFCL and ScienceWorld; blocks of 50 training tasks per group; disjoint hold-outs of 50 tasks per group (90 for ScienceWorld); one backbone; three methods (ReasoningBank: top-1 memory retrieval; GEPA: rewrites a shared strategy prompt; Meta-Harness: edits prompt, memory, skills and code, accepting an edit only if validation accuracy on the active block improves). Plasticity P is the gain at the end of a group's own block; stability is S = -(I + F), where I is pre-block interference and F is post-block forgetting measured from the block-end peak, each taken as max(0, ·). Claim: "higher plasticity consistently comes at the cost of stability".

## Flags (ranked; post hoc)
1. **The trade-off is partly an identity of the two metrics.** F_k = max(0, A[τ_k] - A[T]) and P_k = A[τ_k] - B_k, so F_k >= P_k - Term_k and S <= -(P - Term) (algebra; `checks.py` shows the bound on the Overall row: ReasoningBank P 3.3, Term 2.5, S -1.9; GEPA 6.2, 3.7, -4.3; Meta-Harness 2.2, 1.4, -2.1). With terminal advantages of +1.4 to +3.7 for every method, more plasticity must show more "forgetting". The most plastic method (GEPA) also has the best terminal and average advantage; its stability cost is a loss from its own peak.
2. **No noise floor.** Each cell is one 50-task hold-out averaged over 8 rollouts at T = 1.0 (rollout-noise SD about 1.6-2.2 pp; assumes mean per-task p(1-p) of 0.10-0.20), and I and F take max(0, ·), so noise alone pushes S negative. A null simulation (zero effect; evaluation SD 1.5-1.9 pp) gives expected S of about -0.9 to -1.6 pp, depending on the stream. Several reported values sit at or below that floor (ReasoningBank topic -1.1, domain -0.4, compound -1.4; Meta-Harness topic -0.3, workflow -0.5); the large cells do not (GEPA topic -4.8, workflow -6.5; Meta-Harness domain -3.1, compound -4.4). No frozen-harness re-evaluation, repeated stream run or interval is reported.
3. **The correlation reproduces but the points are not independent.** r = -0.72, p = 0.008 recomputes from Table 1 (t = -3.29, df = 10), and survives removing scenario or method means (-0.78 and -0.64); the 12 points are three methods repeated over four overlapping streams. The introduction's statement that a larger editable surface raises "plasticity or edit freedom" does not order by surface: Meta-Harness, the largest editable surface, has the lowest Overall plasticity (2.2) yet the worst stability on domain and compound drift.
4. **Heading 4.4 outruns what was tested.** "Similarity-Based Retrieval Cannot Prevent Interference or Collision" rests on top-1 retrieval with no similarity threshold and one embedder; the text itself says "adding a similarity threshold could mitigate this unconditional retrieval" (untested). The collision part is supported for one pair of groups: "No similarity threshold can separate the two groups." The interleaved reference run is read as showing that mixing does not help, but only GEPA degrades (+5.8 to +0.9); Meta-Harness improves (+0.8 to +1.9), on one stream.
5. **Scope and budgets.** "These findings show that current self-evolving agents remain incomplete continual learners" generalises from three methods, one backbone and four short streams. Per-method budgets (mutations, proposer calls, tokens) are not stated, and the Meta-Harness proposer runs in a different coding harness, so differences in plasticity cannot be separated from compute and gate design; the gate ablation (removing the Meta-Harness acceptance gate) is reported in text only. No falsifier or threshold for "high" plasticity or stability is stated.

## Holds
The mechanism evidence for the strongest cases is concrete and checkable in the text: GEPA's prompt composition by block (BIRD-F1 share 100% to 40.2% on topic drift; seven BIRD sections of 3,386 characters condensed to one of 1,034 on compound drift) and behaviour counts (clarification asks on BFCL-Miss 29.8% (119/400) after the Miss block, 11.2% (45/400) after the Base block; Meta-Harness 60.8% to 8.5%). That a single shared instruction surface is overwritten when consecutive blocks need opposite workflows is well supported on the workflow and compound streams. Table 1 and Table 2 agree and averages recompute. Table 4 supports the collision claim for the stated embedder. The environment preamble is stated as not editable ("no method may edit it"); the paper states its streams and metrics openly.

## Open
Per-task variance and the repeated-evaluation SD (to replace the assumed 1.6-2.2 pp); the Meta-Harness gate-ablation table; method budgets; whether a threshold, workflow-aware key or trajectory retrieval changes the collision result; code and seeds.

## Evidence tier and deeper-pass flag
**Tier:** E1 executed: arithmetic on numbers typed from Table 1, and a null simulation whose evaluation-SD input is an assumption (`checks.py`). E2 read: full body and appendices as text, figures from captions only. E3 interpretation: flags 4 and 5, and the assumed SD.
**Deeper pass:** recommended. Cheapest decisive test: re-evaluate one frozen seed harness at every checkpoint with the same 8 rollouts and compute I, F and S from it; that gives the empirical noise floor for flag 2. Not done.

## Limitations: what this does and does not establish
- One reader, an AI system; the flags are leads tied to tables and text, not verdicts, and the paper may answer them in places not read.
- The noise floor is a simulation under an assumed evaluation SD, not a measurement on the paper's data.
- The number of flags is not a severity ranking (see the series overview).
- Evidence classes: E1 executed here (`checks.py` and its output), E2 read, E3 interpretation, as marked.

## Reproduction
Everything is in `benchmark_validity_readings_v1/continual_self_evolving_agents/`: `predictions_fixed_2026-10-29.md`; `checks.py`; `checks_output.txt`; `quote_checks_output.txt`; `tool_scan_*.json`. `quote_checks.py` (in the series folder) reports which double-quoted strings occur in the paper's text layer.

## References
Sources: the paper named in the scope line (PDF sha256 `e686b84dad4c9b1b145b99a16e198a3e4d00f01de4c63693b39100d89f293617`); the numbers recomputed in `checks.py` are typed from its Table 1.

## Revision log
- *2026-10-29, v1.* First public version.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
