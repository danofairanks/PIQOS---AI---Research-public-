# A Gain Where Reasoning Also Got Longer: Reading "ThinkEdit" for Whether the Tables Support a Fix for "Overly Short Thinking"

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** One paper, "ThinkEdit: Interpretable Weight Editing to Mitigate Overly Short Thinking in Reasoning Models" (arXiv:2503.22048v4, 29 Sep 2025; the paper names the University of California, San Diego). The authors are called "the authors". A later paper from the same group, read in its own folder, extends this edit family to the opposite direction on the same axis. No individual is named and no intent is attributed.

**Disclosure.** AI-assisted (Claude, working under this project's own non-default standard; direction, selection and release decisions are the operator's); single reader. No Claude or other API model appears in this paper's pipeline (text search). Read from an operator-supplied copy (25 pp.; PDF sha256 beginning df9b10d5f2e4ecdb) via text extraction: the full body and appendices A.1-A.9; figure plots were read through captions only. The code repository named in the abstract was not retrieved or run.

## What it is
DeepSeek-distilled reasoning models (1.5B, 8B, 14B, and 32B in an appendix). A reasoning-length direction is the mean difference between activations of long (over 1,000 tokens) and short (under 100 tokens) chains of thought from 2,000 GSM8K training problems. The top 4% of attention heads by alignment with the short direction have their output projections orthogonalized against it. Headline: +6.39% on the shortest-reasoning responses and +3.34% overall across math benchmarks, with 0.2% of parameters edited; each cell is the mean of ten runs, reported with a standard deviation.

## Flags (ranked; post hoc)
1. **The headline averages do not reproduce from the tables, and one cell dominates.** The mean gain over the 15 model-by-benchmark cells of Table 1 is +2.91 points (+1.54 without the 1.5B model's MMLU Elementary Math cell, +22.14, which the paper attributes to the unedited model ignoring the multiple-choice format); the mean over the 45 short-response cells of Table 2 is +5.43. The abstract says +3.34 and +6.39 and gives no formula or weighting (adding the 32B model gives about +2.4). One of the 15 overall cells is negative (1.5B, MATH-Level5, -0.43). (E1; means E2)
2. **Short-tail gains compare different problems.** The "shortest 5/10/20%" subsets are defined by each condition's own output length and the edit lengthens the shortest outputs (Table 3), so the edited and original subsets are not the same problems; selecting the tail of noisy outputs also invites regression to the mean. A matched-problem comparison is not reported. (E1; reading E2)
3. **"Reasoning length remains largely stable" holds only token-pooled.** The paper reports a net change of -0.27%; recomputing from Table 4 the token-pooled change is -0.27%. Per dataset the edit lengthens reasoning by 52%, 55% and 47% on GSM8K for the 14B, 8B and 1.5B models, by about 58% and 49% on MMLU Elementary Math for the 14B and 1.5B models, and Table 15 reports +48% reasoning length on average. The accuracy gains concentrate on those easy datasets. How much comes from removing the direction and how much from thinking longer is not separated; the appended-"Wait" baseline (only for responses under 500 tokens) lengthens less and gains less (14B GSM8K: 90.80 original, 91.30 with "Wait", 93.78 edited). (E1; recomputation E2)
4. **No specificity control.** No edit of randomly chosen heads or of a random direction at the same 4% rate; heads are chosen by the same projection score the edit then removes. (E1)
5. **Operating point.** The 2%, 4% and 8% rates are swept on the reported test benchmarks (Table 5), larger rates doing better on GSM8K and MMLU and moderate rates on the MATH series; the basis for 4% as the main setting is not stated. (E1)
6. **Small and noisy side evidence.** The steering evidence uses 200 GSM8K and 140 MATH-Level5 problems. The 32B model shows no overall gain on the MATH series (Table 9). Non-math MMLU subsets (Table 13) show mostly small gains against run noise (for example 84.00 +- 3.83 to 88.90 +- 1.91; 32B accounting 84.22 to 83.40). (E1/E2)
7. **Operation and scope.** The edit is a projection that removes the direction from selected heads' outputs in both signs, the same operation family used elsewhere for refusal-direction removal; the paper has no durability or dual-use discussion, and its limitations paragraph covers only that already-verbose models may gain less. (E1; reading E2)

## What holds
The direction and head scores come from GSM8K training data kept apart from the test sets; every cell has ten runs with a standard deviation; a baseline is included; the editing-rate sweep and the 32B result with no MATH-series gain are reported; the format-following outlier is explained from manual inspection; code is linked.

## Depth rating (rubric in the series overview)
4.5 (D2; claim reach medium). Non-blind: rated by the same reader after the rubric and table existed.

## Limitations: what this does and does not establish
It establishes that the tables show higher accuracy on easy math sets and on the shortest-output tails after the edit, together with about 50% longer reasoning on those sets, and that the headline averages are not derivable from the tables as read. It does not establish that the gain disappears under a random-head or length-matched control, or anything about code behaviour (not run).

**Tier:** E1 executed (means, relative changes and the pooled length change recomputed in `checks_arithmetic_added_papers.py` from typed table entries); E2 read (all 25 pages as text, plots by caption); E3 interpretation (flag 2 and flag 7 readings). The three tools found no structural or severe gaps; attractor-scan's weak flags (the words "reasoning" and "alignment") were read and are the paper's own terms (chain-of-thought tokens; geometric alignment with a direction), not laundering.
**Deeper pass:** recommended: the same problems scored before and after, a random-head edit and a length-matched "think longer" control at 4%. Not done.

## Reproduction
`checks_arithmetic_added_papers.py` and its output; `quote_checks_output.txt`; `tool_scan_*.json`.

## References
Sources: arXiv:2503.22048v4 (PDF sha256 beginning df9b10d5f2e4ecdb); the numbers in `checks_arithmetic_added_papers.py` are typed from its Tables 1-4, 9, 13 and 15.

## Revision log
- *2026-11-09, v1.* Added to the series.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
