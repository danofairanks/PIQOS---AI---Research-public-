# A Careful Fault-Injection Study and a Title Stronger Than Its Abstract: Reading MCP-Injector ("Tool-Calling LLM Agents Under Realistic MCP Faults")

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one paper, "Tool-Calling LLM Agents Under Realistic MCP Faults: Scale Does Not Purchase Fault Tolerance" (MCP-Injector, arXiv:2610.32555v1, 23 October 2026, NeurIPS 2026; the paper names SnT Luxembourg, Tilburg, GSSI and Naples). The authors are called "the authors"; organisations are named only as the paper names them. No individual is named and no intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance; one reader, an AI system. Read from an operator-supplied copy (35 pp). Read: main text, results, tables and figure captions; appendices only as referenced. Lens: the series overview. Same-source caveat: single Anthropic-model reader; none of the evaluated models is Anthropic's. Post-hoc; see the predictions file in this folder. Artifact not accessed. **Contrast case.** Careful design (null-operator control with 18 paired non-intrusiveness tests, paired within-task analysis, completed-only secondary analysis, zero-dose analysis, grounded-fulfillment view, explicit labelling of data-derived versus hand-set parameters) and openly hedged claims; the flags are scope, a title stronger than the abstract, and null-inference. Do not read the flag count as severity (series overview, section on reading the flag counts).

## What it is
MCP-Injector: a proxy on the MCP tool-call path with six operators (minor mistake, incorrect output, invalid output, explicit error, delay, silent drop) and three persistence regimes, seeded. Profile mined from 57,240 threads across 1,774 MCP repositories (GPT-4o classifier at temperature 0; 117 threads double-annotated, kappa 0.93 mode, 0.80 persistence). Experiment: gpt-oss-20B and -120B x three agent stacks x {proxy off, null operator OP0, calibrated faults OPP} x 25 tasks x 3 seeds = 1,350 cells; judge gpt-4o-mini, five repeats, median.

## Checks (E1; `checks.py`)
Table 2 recomputes exactly: N = 13,824; permanent 91.26%, intermittent 7.99%, transient 0.75%; explicit-error/permanent 65.65%; all explicit errors 71.19%; silent content modes 19.10%; timing modes 9.71%; cells = 1,350; 8.08 -> 3.23 = -60.0%. One rounding difference (pooled completion gap computes as 4.5 from printed 95.6 and 91.1; paper 4.4).

## Flags (ranked; post-hoc)
1. **Title stronger than the evidence.** Two models from one family (a mixture-of-experts pair), one serving setup (LM Studio, consumer Apple Silicon, 16k context, 3,000 s timeout), one benchmark. The size coefficient's CI is [-0.39, 0.37] (p = 0.96); the paper says it "cannot exclude a modest effect in either direction"; no equivalence test. The abstract is hedged ("for the two gpt-oss backbones we test"); the title is not.
2. **The benchmark may not separate the two models.** Fault-free task-completion 8.37 vs 8.13 (proxy-off 8.11 vs 8.30); a null on a pair indistinguishable at baseline says little about scale (the reader's inference). Fault-free completion is already lower for the 120B (96.9% vs 99.1%), which the paper decomposes.
3. **"60% degradation" belongs to a stress profile.** Permanent-heavy by construction and calibrated to reported failures, not operational rates (the authors say so); a permanent explicit error kills a tool for the run, so the drop partly measures task dependence on tools. Excluding zero-dose cells (55 of 450) raises the drop from 60% to 67%.
4. **Calibration rests on one classifier and a small validation sample.** Transient failures are 104 of 13,824; several parameters are hand-set (delay 0.3 and 30 s, perturbation intensities, transient activation 1), and the paper labels them.
5. **"Framework-level error handling matters more than model scale" compares two uncertain effects.** The stack interaction is p = 0.048 and 0.074 with CIs touching zero, no multiplicity correction, and one stack receives more fault events per cell; the paper itself calls it "suggestive".
6. **Judge and ungrounded answers.** Tool-bypass runs (27 of 450 cells, 6.0%) can score well; the paper reports a grounded-fulfillment view (63% drop vs 58%).
7. **Scope.** Single-server tasks only (25 of 28 servers connected), distraction servers disabled, non-adversarial threat model; end-to-end runs not bit-reproducible (the fault schedule is seeded).

## Holds
Non-intrusiveness controls (18 paired Wilcoxon tests, Bonferroni, all p >= 0.05); paired OPP - OP0 design; completed-only secondary analysis; zero-dose and bypass analyses; explicit data-derived versus hand-set labelling of the profile; open artifacts; candid limits.

## Why it matters for the public MCP server (`tools/research_mcp`)
The fault classes (explicit error, invalid output, silent drop) map onto how that server reports failures: several return a successful JSON payload `{"error": ...}` rather than a protocol-level `isError`. See `research_mcp_failure_semantics_probe_v1.md` (same directory as the series) for a preregistered test of whether a client can tell *scanned, nothing found* from "not scanned" under faults.

## Evidence tier and deeper-pass flag
**Tier:** E2 read (main text; appendices by reference only). E1 on printed table entries (checks.py). E3: flags 2 and 5 are interpretation.
**Deeper pass:** optional. Decisive tests: an equivalence-style analysis of the size effect, and a run of the artifact with a third backbone family; needs an artifact clone. Not done.

## Open
Appendices A-I; whether the 25 task set is released; any reanalysis of the size effect with a prespecified equivalence margin.

## Limitations: what this does and does not establish

- One reader, an AI system, reading a paper and its tables; the flags above are leads, each tied to a page or table, not verdicts, and a paper may answer them in places not read (see what was read and not read at the top and under Open).
- The number of flags is not a severity ranking (see the series overview).
- Evidence classes: E1 executed here (scripts and their outputs in this folder), E2 read, E3 interpretation, as marked in the text.

## Reproduction

Everything is in `benchmark_validity_readings_v1/mcp_injector_fault_tolerance/`: `predictions_fixed_2026-10-26.md`; `checks.py`; `checks_output.txt`; `quote_checks_output.txt`; `tool_scan_*.json`. Re-fetched from arXiv on 2026-10-26: the file is byte-identical (sha256 `6e0231e4af15ab42fc0088b7dbf0c97c4ad3a7b8cea57cadd38453be2964ee85`). `quote_checks.py` (in the series folder) reports which double-quoted strings of this reading occur in the paper's text layer; strings that did not match were rewritten as paraphrases or corrected to the paper's wording before publication. The paper's PDF is not stored here; the preregistration and the scripts are.
- **Predictions** were fixed before the measurement they concern (`predictions_fixed_2026-10-26.md`); that order is the evaluator's own record and is not independently timestamped.

## References

Sources: the paper named in the scope line above (PDF sha256 `6e0231e4af15ab42fc0088b7dbf0c97c4ad3a7b8cea57cadd38453be2964ee85`); the numbers recomputed in the scripts are transcribed from its tables.

## Revision log

- *2026-10-26, v1.* First public version, from the reader's working notes of 2026-10-26. Quotation marks were removed from, or corrected in, phrases that did not match the paper verbatim; cross-references to working notes and workflow remarks were not carried over.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
