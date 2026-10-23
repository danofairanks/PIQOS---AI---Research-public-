# A Paper's Second Version Against Its First: Dream-RSI, What Was Added, What Was Dropped, and What Did Not Change

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

## 1. The question

"Dream-RSI: Recursive Self-Improvement through Evolving Worlds" (arXiv:2609.14858; affiliation lines Google, Google DeepMind, University of Maryland, University of Virginia) was posted on 14 September 2026 (v1, 36 pages) and revised on 6 October 2026 (v2, 43 pages). There are two versions. The method records a discovery tree while a policy explores, replays that tree as a simulator to score alternative exploration policies ("dreaming"), and redeploys the best policy. This draft asks what changed between the versions, what did not, and whether the authors' other public surfaces (project site, GitHub repository) follow the revision. It is a version-history reading; it does not evaluate the method.

## 2. What was read, and how

- **Both PDFs through their text layer**, v1 (sha256 `b2d13d59…`) and v2 (sha256 `9d632678…`), re-fetched from arXiv on 2026-10-23; the hashes equal those of the files first supplied by an operator. Appendix E (the discovered programs) was not read; figures were read through their text layer only.
- **Predictions** C1 to C8 were fixed on 2026-10-18 before v2 was read, from a prior reading of v1 (`predictions_fixed_2026-10-18.md`). The date is the evaluator's own record, not independently timestamped.
- **The diff is mechanical but noisy.** `diff_versions.py` compares word lists after normalisation and finds 695 changed blocks (88 of 12 words or more) and similarity 0.74, much of it reflowed captions, moved figures and re-rendered math. Every finding below was therefore re-checked with a targeted string test on both versions (`change_checks.py`); the classification of what is substantive is mine.
- Evidence classes: **E1** executed or recomputed here; **E2** read; **E3** interpretation. One reader, an AI system from the lab whose model ("Claude Opus 4.8") the paper's new domain uses for discovery, policy development and evaluation. That is a same-source condition; the string tests do not depend on it, the classification does.
- The authors are called "the authors". No intent is attributed: revising claims between versions is ordinary. The question is what the revised text supports.

## 3. What did not change (E1)

- **The headline numbers of the original domains.** The Lasso, mathematical-optimisation and kernel results are identical to the digit (for example "3587.1 ms to 2931.0 ms" with "317" against "550" discovery-agent calls; "2.43× and 1.79×"; "2.09× and 1.44×"; the Table 1 values of the Dream-RSI row).
- **The guard text and the boundary sentence.** "Never execute pkill, kill, killall, or terminate unrelated processes." and "Everything else is read-only" are in both versions, word for word. The mutable/fixed boundary is stated in v1 as "Only the exploration-policy code changes; the underlying models, evaluator, and execution interfaces remain fixed" and in v2 as "Only the policy code changes; the models, evaluator, and execution interfaces stay fixed": the same partition, reworded.
- **What is still absent.** Neither version contains a Limitations, Broader Impact, ethics or impact-statement section (the strings do not occur), a code-release statement (the word "release" does not occur), or any account of why the evaluator and model are kept outside the mutable set. The string "Safety" occurs once in each version, in a code comment ("Safety limit check") inside a listed discovered program, not in a section.
- **The links.** `github.com/zhengkid/Dream-RSI` and `dream-rsi.com`.

## 4. Predictions scored

Eight predictions with stated probabilities; outcomes matched the more probable side in seven (C7 was a coin flip at 0.5 and came out no); Brier score 0.115.

| | Prediction [probability] | Outcome |
|---|---|---|
| C1 | v2 carries a "v2" stamp dated after 14 Sep [0.95] | Yes: "arXiv:2609.14858v2 [cs.CL] 6 Oct 2026" |
| C2 | A limitations/ethics/safety section appears [0.35] | No (as the lower probability implied) |
| C3 | The `pkill` line is unchanged [0.8] | Yes |
| C4 | The fixed/mutable partition is unchanged [0.85] | Yes formally (section 3); the scope of what is discovered widened (section 5) |
| C5 | Headline results unchanged within rounding [0.6] | Yes for the original domains; the abstract and introduction wording changed (section 5) |
| C6 | The page count increases [0.6] | Yes, 36 to 43 |
| C7 | A code/data release statement is added or changed [0.5] | No |
| C8 | The reference list grows [0.6] | Yes: the arXiv-identified entries go from 35 to 38 (three added, none removed); a precise count of all entries was not made (the entry boundaries do not extract reliably) |

## 5. What changed (E1 for the strings, E3 for the reading)

1. **A fourth domain, harness optimisation (§4.4, new).** v2: "Across 9 tasks in 4 domains" in the abstract; v1 described "8 scientific discovery tasks spanning three distinct domains". The task: "improve the program surrounding a fixed language model, including how information is stored, retrieved, and presented during agent execution", starting from a seed harness (Terminus-Kira) in the setting of Meta-Harness, scored on "the full Terminal-Bench 2.1 … suite of 89 tasks, with two independent runs per task". "We use Claude Opus 4.8 with Claude Code as both the discovery agent and the policy-development agent, while harness evaluation is also performed with Claude Opus 4.8"; Meta-Harness is reproduced "following its original search protocol, using Opus 4.8". Result: "increasing the full-suite score from 0.7247 to 0.8090", "outperforms Claude Code (0.75) and Meta-Harness (0.79)"; the introduction says "over 8 points".
2. **No controlled comparator in the new domain, and the scope sentence moved.** v1 said "Across all tasks, Dream-RSI and Recursive Fixed Exploration use the same discovery agent, evaluator, initialization, and resource constraints." v2 says "On the scientific discovery tasks, our main controlled baseline is Recursive Fixed Exploration" and, for the new domain, "we focus on end-to-end performance and omit the fixed-policy comparison due to its substantial cost: an additional full search is estimated to cost over $100,000." The paper's own causal comparator, the one that isolates the effect of dreaming, is therefore absent from §4.4; the comparison there is with Claude Code and a reproduced Meta-Harness. The $100,000 estimate is the authors'; it is not checked here.
3. **The margins in the new domain are a few trials.** 0.7247 and 0.8090 equal 129 and 144 passes of 178 (89 tasks × 2 runs). The two comparators are printed to two decimals, which is consistent with 133 to 134 passes (Claude Code) and 140 to 141 (Meta-Harness): Dream-RSI's lead is 10 to 11 trials and 3 to 4 trials respectively. No interval or variance across searches is given (searches: confidence interval, standard deviation, variance: none; "seed" occurs three times, all as "seed harness"). The word "held-out" occurs four times in v2, all in the Lasso domain; Figure 5(a) plots the best-so-far Terminal-Bench 2.1 score over the discovery process, and that curve ends at the reported 0.8090; I found no held-out split described for §4.4. Whether selection and reporting use the same 89 tasks is therefore an E2 reading by absence, not a stated fact.
4. **Claims narrowed in the abstract and introduction.** v1: "competitive or improved discovery quality while substantially reducing discovery cost in several settings". v2: "competitive quality and improves discovery efficiency in several settings". v1's "1.7× over fixed-exploration baselines" and "over 50× budget savings compared to SimpleTES" do not occur in v2. The 162× figure remains, now with "approximately 162× and 27× fewer discovery-agent calls, respectively … although these comparisons use different model backbones" (§4.3; the comparison is against a different system's reported 51,200 generations). v1's "leaving the underlying coding agent unchanged" became "base agent".
5. **The policy-improvement objective was redefined.** v1 scored a replayed policy by solution quality with a penalty on attempted generations; v2 uses a "normalized area dominated by the quality–cost Pareto frontier" over budget-control parameters, with an added term. The headline numbers did not change (section 3). I found no sentence saying whether results were recomputed under the new objective or the description changed; that is a question for the authors.
6. **A new ablation (Table 2), on one task.** On ConvDiv, replay over all history reaches 1.90 against 1.59 for current-round-only. The compute columns read 786 and 430 discovery calls, so the better arm used 83% more compute; the text states the performance gap and not the compute gap. It is not a matched-budget comparison.
7. **An AI Use Statement was added (Appendix A).** "we use Gemini 3.1 Pro in the Section 4.1,4.2,4.3, Gemini 3.7 Flash in Section 4.3 and Claude Opus 4.8 with Claude Code in the Section4.4", Gemini 3.8 Flash "for writing and grammar correction", and "We have reviewed all AI-assisted work".
8. **The reference list gained three arXiv-identified entries** (a multi-model self-evolution paper, a long-horizon terminal-task benchmark and a paper on recursive synthesis for long-horizon terminal tasks) **and the Terminal-Bench conference reference** (no arXiv id), the benchmark of the new domain.

## 6. The authors' other surfaces on 2026-10-23 (E1; `site_repo_check.py`)

- **Project site (`dream-rsi.com`).** It still reads "Three discovery domains" and "Eight discovery tasks", still carries "1.7× against fixed exploration and up to 162× against SimpleTES", and its citation block still has the placeholder `arXiv:XXXX.XXXXX`. The strings Terminal-Bench, harness and Opus do not occur. In other words the site describes v1.
- **Repository (`zhengkid/Dream-RSI`, HEAD 4149ea9, unchanged since 2026-09-16).** Its README badge reads "8 across 3 domains", it says "arXiv posting: In progress" and "arXiv coming soon", its release plan lists the discovered programs, the full codebase and reproduction scripts as "Being prepared", and it quotes "1.22x faster downstream runtime, 1.74x less discovery compute, 162x fewer calls than SimpleTES". It holds a project page and the paper, no code, prompts or configurations; two pull-request refs exist (numbers 2 and 5) and were not examined.
- **Consequence.** Nothing public lets an outside reader run or inspect the system, so the guard text, the fixed/mutable boundary and the §4.4 result can be read but not tested. The repository the paper links on its first page is a project page.

## 7. What this does and does not establish

- It does not show the revision is anything other than ordinary. Narrowing claims and adding a domain are normal.
- It shows that the results of the three original domains did not change, that the added domain's headline (a lead of 3 to 11 trials of 178) has no controlled comparator, no interval and no described held-out split, that the objective's definition changed without a stated effect on the numbers, and that the authors' site and repository still describe the earlier version.
- It shows that a guard text and a safety discussion neither changed nor were added; the guard text cannot be tested because no implementation is public.
- Limits: two versions only; Appendix E and the figures unread; the diff is noisy and the classification is mine; one reader, same-source with the new domain's model; the 8-point claim and Terminal-Bench 2.1 details are the paper's own, not checked; pull-request refs not examined; the site was fetched once and may change.

## 8. What would change this

A code release with the prompts and evaluator; the fixed-policy comparison or a cheaper proxy for it in §4.4; several independent searches with an interval; a stated held-out split for the harness domain; the authors' statement of how the redefined objective affected the reported numbers; an update of the site and README to v2.

## 9. Reproduction

Everything is in `dream_rsi_versions_reading_v1/`: `predictions_fixed_2026-10-18.md`; `diff_versions.py` with `diff_summary.txt` and `diff_blocks.txt` (the 88 blocks of 12 or more words); `change_checks.py` and its output (string tests on both versions, the reference-id comparison, the arithmetic); `site_repo_check.py` and its output (a live fetch of the site and the README at the pinned commit; the site may have changed since). Both PDFs are public on arXiv and are not stored here; the scripts print the expected hashes and need `pdftotext`.

## References

Sources: arXiv:2609.14858 v1 (14 September 2026) and v2 (6 October 2026), "Dream-RSI: Recursive Self-Improvement through Evolving Worlds"; the project site `dream-rsi.com` and the repository `github.com/zhengkid/Dream-RSI` (commit 4149ea9), as fetched on 2026-10-23. Every quotation and count in this draft is taken from those and re-checked by the scripts above.

## Revision log

- *2026-10-23, v1.* First version.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
