# Six Kinds of Model, One Agent With a Command Line: Where the Edits Held and What They Were Told

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** One developer blog post (6 Nov 2026) and the repository it links (a single commit, 6 Nov 2026), which replicates parts of the MIT CSAIL weight-editing post with an AI coding agent and a command-line toolkit. The post's author is a private individual and is called "the author"; the agent's model is not named in the post. No intent is attributed. Locators are held privately.

**Disclosure.** Drafted with AI assistance; one reader, an AI system (an Anthropic model). Read: the post, the repository README and article, the generating script of the synthetic fraud data, the weather data file (row counts only). Nothing was run.

## What it claims
On classic and small models (logistic regression, small networks, boosted trees, a small RL agent, a CNN) an agent diagnoses a flaw, writes a small edit, tests before and after, and commits a reversible patch; a gradient-boosted model written from a program with no labels reaches AUC 0.809 on next-day rain, against 0.839 for the same model trained on 2.5 years and 0.747 on 60 days; on a 0.8B language model finding the cause works but its own edit moved the end-of-reasoning token 1.2x against 29x for the published edit. The post says "Short version: on classic and small models, it works, sometimes remarkably well."

## Flags (ranked; post hoc)
1. **The new-scam result is closed by the data generator.** In the shipped generator the fraud probability is raised when a gift-card purchase exceeds 500 dollars; the edit adds a rule block for exactly that condition; catch rate 10% to 98% follows from the rule equalling the data-generating condition. The currency-bias fix likewise supplies the target risk level from recent data. What these cases show is that a patch can be surgical (nothing outside the rule moves); they do not show diagnosis or discovery. The router and delivery cases use the same synthetic-flaw design. (E1)
2. **A different method from the one replicated.** The MIT experiment has a frontier model read and write weights natively with a forward-pass budget; here an agent calls a fixed set of edit operations with before-and-after evaluation as feedback, on models where the answer is known. The statement that it works on classic and small models rests on five or six synthetic or toy cases, one run each, no intervals; the further claim about most models running in production is outside the evidence. (E1 README; E2)
3. **The language-model replication tests a weaker setting with a proxy.** A 0.8B model on a laptop under a 6 GB cap; both numbers (1.2x and 29x) are teacher-forced probabilities of the end-of-reasoning token, not task accuracy. The MIT table shows its own 10- and 25-pass runs barely worked, so a failure under tight compute does not contradict the 50-pass run. (E1)
4. **"This matches what others replicating the paper report: diagnosis transfers, edits often don't."** No source is linked for "others"; the only outbound links in the post are the MIT page, the weather data source and the repository. (E1)
5. **Weather result precision.** One test set of 1,220 city-days (373 rain); Hanley-McNeil 95% half-widths about 0.03 for each AUC (recomputed), so 0.809 vs 0.839 is not resolvable on one test set; the 60-day baseline is one random draw and the trained baseline is stated as untuned; the second-round gain (+0.006) is inside the interval. The held-out design itself is sound: a validation period was used before one final test run on a period after the writer's stated knowledge cutoff. (E1)

## What holds
The arithmetic: The post's claim that the zero-label model recovers about 75% of the gain over persistence checks out: it is (0.809 - 0.719) / (0.839 - 0.719) = 0.75. Honest negatives are reported (a CNN skill not recoverable by edit, the failed language-model replication, a bug in the author's own script). Code and data are in the repository.

## Predictions, and what changed
Fixed before reading: single runs and no intervals (met); an honest negative-results section (met); a tautology-type flag (met, flag 1); overreach in the title (partly). The weather held-out design was better than predicted.

## Limitations: what this does and does not establish
It establishes the flags above on this post and repository. It does not establish that the toolkit fails on real flaws, that the language-model edit cannot work with more compute or a stronger editor, or anything about intent; the scripts were not run.

**Tier:** E1 executed (generator read, shipped data counted, intervals recomputed); E2 read (post and repository); E3 interpretation (flag 2's reading of the methods as different).
**Deeper pass:** optional: run the weather scripts and the command-line demos. Not done.

## Reproduction
`checks_arithmetic.py`; `quote_checks_output.txt`; `tool_scan_*.json`.

## References
Sources: the developer blog post (6 Nov 2026) and its repository (commit 8e71558), held privately; the numbers recomputed in `checks_arithmetic.py` are typed from them or computed from the shipped data file.

## Revision log
- *2026-11-09, v1 (pre-draft).* Private pre-build.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
