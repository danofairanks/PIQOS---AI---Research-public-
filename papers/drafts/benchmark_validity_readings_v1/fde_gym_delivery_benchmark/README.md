# Uplift Minus an Undisclosed Contact Cost: Reading FDE-Gym ("The Last Mile of AI Delivery")

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one paper, "The Last Mile of AI Delivery" (FDE-Gym, arXiv:2610.22350v1, 15 October 2026; the paper names DeepLethe and contributors). The authors are called "the authors"; organisations are named only as the paper names them. No individual is named and no intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance; one reader, an AI system. Read from an operator-supplied copy (14 pp; PDF sha256 prefix b11240800b27ce2e). Reading lens: the series overview (applied during reading, not preregistered). Same-source caveat: single Anthropic-model reader, and the benchmark scores a model family the reader belongs to (Opus 5.5, Sonnet 5.5, Haiku 4.5). Table 3 was transcribed by the reader from the page image; it reproduces the paper's S = U - C on all 13 rows (C1). No model was run; the open harness (github.com/deeplethe/fde-gym) was not accessed.

## What it is
95 tasks from 20 scenarios (18 sectors), 13 model configurations, one minimal agent harness, 3 runs per task-level. Score S = incident-adjusted normalised business uplift U minus a stakeholder contact cost C; four instruction levels L0-L3 (L3 = sponsor's possibly misdirected request, primary setting). Task admission requires four anchors: reference >= 0.95, do-nothing = 0, literal compliance <= 0.2, shortcuts <= 0.8 (270 strategies tested). Headline: best configuration 0.56, 14/95 resolved (S >= 0.8, no incident).

## Cluster-lens findings (ranked; post-hoc, from reading)
1. **Finding 2 conflates three changes.** L0 also states "how the result is scored" (Table 1); L0->L1 removes that as well as the rules. And the L0->L1 drop (0.28, leading three, 20 originals) includes a contact-cost rise from 0.07-0.10 to 0.18-0.24; per-model L0/L1 C is not tabulated. By endpoint bounds the cost rise is 0.08-0.17, i.e. 29-61% of the drop (see C2). C is set by the authors' experts and the agent is not told it exists. "Discovering unstated constraints is the primary bottleneck" partly measures the penalty design.
2. **L2->L3 (the claim that misdirection costs little) is thin.** 0.04, CI (-0.03, 0.14), on 17 tasks (3 scenarios have identical L2/L3). The paper does not say how many of the 20 L3 requests are misdirected; where the request is correct, L3 = L2 by construction.
3. **Intervals likely too narrow.** Bootstrap is over tasks; the 95 tasks cluster in 20 scenarios with shared environments. No paired test between adjacent models. C4: 12 of 13 adjacent pairs overlap; only Luna/Mistral separate. Opus vs Astra separate (0.50-0.62 vs 0.30-0.46). Overlap is a conservative proxy, not a test.
4. **Admission is self-validating; selection rate unreported.** A task is published only if its grader satisfies the anchors, so the anchors cannot fail on the published set; how many tasks were discarded is not stated. The same experts write scenario, variants, reference, grader, stakeholder scripts and contact costs. The 270 strategies are not listed in the paper.
5. **"Resolved" touches the shortcut ceiling and is dominated by C.** Resolved = S >= 0.8; shortcuts may score up to 0.8. Since S = U - C, a leading model needs U >= 0.94-1.02 at its mean C (C3), so resolved counts are mostly contact-cost counts (Astra: 36 tasks at U >= 0.8, 9 resolved).
6. **Budget truncation read as capability.** Limits: 200 turns, 150 min, USD 8; the unsubmitted state is deployed. Qwen 3.8 Flash submits within limits on 11 of 152 task-level combinations; its 0.07 is largely a budget result.
7. **Fig 8 and the one-in-seven statement.** The paper states success rates and uplift are not comparable, then draws a practical conclusion from the pairing. External numbers come from another harness (Vals AI, single source); the 0.8 cutoff behind "15%" is arbitrary; best model per provider only.
8. **Fig 5b / Section 5.6 (the statement that spend does not buy outcomes)** compares different models across providers; the only within-model effort contrast is Haiku 4.5 +/- thinking (-0.33 vs -0.35).
9. **Reproducibility partial.** Harness open; 75 variants and all reference solutions held out; 20 originals on request, 3 public. The L3 headline cannot be independently re-run. Operator of the leaderboard is an author affiliation (disclosed). Stakeholder topic-mapper model unnamed; paper cites that the user-simulator model shifts rates by several points (its ref. 14) and asserts scripting avoids this without an ablation.

## What holds
Scoring identity (C1); anchor construction (do-nothing, literal-compliance, shortcut caps); 3 runs per cell; stated limitations (simulated customer, no human baseline, single harness, contamination, small L0-L2 sample). Gap to the reference at L0 (leading models 0.73-0.82) shows the scale is not saturated at the top even with full information.

## Scorecard against the predictions
| | Prediction | Result |
|---|---|---|
| C1 | S = U - C within 0.011, 13 rows | held (max residual 0.01) |
| C2 | share of 0.28 between 0.3 and 0.6 | marginal miss at both edges: 0.29-0.61 (bounds only; per-model values not tabulated) |
| C3 | implied U > 0.90 for leading three | held: 0.94, 0.98, 1.02 |
| C4 | named pairs overlap; Opus/Astra separate | held; overlap is wider than predicted (12 of 13 adjacent pairs) |

## Correction to an earlier informal evaluation (2026-10-25)
The earlier informal evaluation gave the contact-cost share as "about 40-50%" from pairing the low and high ends of each range (0.11-0.14). The unpaired bound is 29-61%. Use the bound.

## Open
Harness and the 3 public tasks not run. Whether L3 requests are misdirected in how many of the 20 originals: not stated; check the harness repo if accessed. Selection rate and the 270-strategy list: ask or read the repo.

## Evidence tier and deeper-pass flag (added 2026-10-25)
**Tier:** E2 read (all 14 pp). E1 on reported values only: S = U - C identity, contact-cost share bound, implied U thresholds, CI overlap (checks.py). E3: flags 1-2 and 5 are the reader's interpretation of how the design produces the numbers.
**Deeper pass:** optional, partial. Harness is open but only 3 tasks are public (20 originals on request, 75 variants and references held out), so most flags cannot be tested from the repo. Cheap parts: count how many L3 requests are misdirected and read the L0 vs L1 instruction text in the 3 public tasks. Trigger for a full pass: obtaining the 20 originals.

## Limitations: what this does and does not establish

- One reader, an AI system, reading a paper and its tables; the flags above are leads, each tied to a page or table, not verdicts, and a paper may answer them in places not read (see what was read and not read at the top and under Open).
- The number of flags is not a severity ranking (see the series overview).
- Evidence classes: E1 executed here (scripts and their outputs in this folder), E2 read, E3 interpretation, as marked in the text.

## Reproduction

Everything is in `benchmark_validity_readings_v1/fde_gym_delivery_benchmark/`: `predictions_fixed_2026-10-25.md`; `checks.py`; `checks_output.txt`; `quote_checks_output.txt`; `tool_scan_*.json`. Re-fetched from arXiv on 2026-10-26: the file is byte-identical (sha256 `b11240800b27ce2e3b260239b6781508396e05baa58e507065a8393c73a069ce`). `quote_checks.py` (in the series folder) reports which double-quoted strings of this reading occur in the paper's text layer; strings that did not match were rewritten as paraphrases or corrected to the paper's wording before publication. The paper's PDF is not stored here; the preregistration and the scripts are.
- **Predictions** were fixed before the measurement they concern (`predictions_fixed_2026-10-25.md`); that order is the evaluator's own record and is not independently timestamped.

## References

Sources: the paper named in the scope line above (PDF sha256 `b11240800b27ce2e3b260239b6781508396e05baa58e507065a8393c73a069ce`); the numbers recomputed in the scripts are transcribed from its tables.

## Revision log

- *2026-10-26, v1.* First public version, from the reader's working notes of 2026-10-25. Quotation marks were removed from, or corrected in, phrases that did not match the paper verbatim; cross-references to working notes and workflow remarks were not carried over.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
