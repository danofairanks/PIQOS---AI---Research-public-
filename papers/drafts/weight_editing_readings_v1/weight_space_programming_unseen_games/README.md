# Programs in Network Form: Reading a Controlled Test of Weight-Space Programming on Private Games

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** One paper, "Compiling Known Rules into Compact Neural Agents: Weight-Space Programming on Unseen Games" (arXiv:2611.16981v1, 12 Nov 2026; the paper names Amazon and TU Dresden, and states the work was done outside Amazon). The authors are called "the authors"; works the paper cites are described by role. The paper tests, on games it wrote, a claim made by a post read elsewhere in this series (that a frontier model can write a network's weights from a task's rules), using the same frontier model that post names; it does not touch that post's edit of a language model. No intent is attributed to anyone.

**Disclosure.** AI-assisted (Claude, working under this project's own non-default standard; direction, selection and release decisions are the operator's); single reader. This paper uses Claude models among its nine writers, and states that one evaluated writer (Claude Opus 5.5) designed the harness and analysis. Read from an operator-supplied copy (32 pp.; PDF sha256 beginning a7393dadb706a5bc): the full body and Appendices A.1-A.9 as page images, and the text layer of Table 9. The released code and the private game sources were not retrieved or run. Predictions were written in private notes before reading; their commit was delayed by a path error, so their order is not independently shown.

## What it is
Twenty private ARC-AGI-3-style game families (never published), nine writer models, each writing either the weights of a fixed 57,289-parameter recurrent convolutional actor (one-shot, or with up to three feedback rounds), a network of its own design in a small tensor language ("free architecture"), or a Python player. The writer sees the game's simulator source with held-out levels, renderer templates and solvers removed. Evaluation is on held-out levels, held-out renderings and perturbed starts. Controls: replay and open-loop floors, zero- and first-frame inputs, learned baselines in the same actor (imitation, distillation, PPO), PPO fine-tuning of written weights, weight-noise tests. A second tier uses the 25 public games. Headline: the best writer's fixed-actor weights solve 56% of held-out episodes with feedback, Python players 97-100%; in free architectures the written networks are bounded, branch-free programs (93% of parameters exactly zero, 90% of the rest small integers or powers of two); learned weights in the same actor transfer at most 11%; written weights do not survive PPO's first update.

## Flags (ranked; post hoc; leads, not verdicts)
1. **The headline that weight-space programming "amounts to writing a restricted class of programs" is partly definitional.** The protocol forbids fitting, search and tools, so what a writer can return are hand-set constants; hand-set constants in a network are a program in network form. The paper says it does not show that writers derive a program first (a hypothesis in its conclusions) and does not test writers who may run code and fit. The abstract scopes the claim with "under a protocol that forbids fitting and search". (E3)
2. **The comparison with another work's released language-task networks pools parameters over 21 of 24 models** (three failed on a missing dependency): 252,513,103 parameters, about 99.2% exactly zero. A pooled parameter share is dominated by the largest models; per-model shares are not given in the main text. (E2)
3. **The finding that written weights and PPO do not combine rests on three to four families, three of them the preliminary-study families, and on training in TF32 with evaluation in exact FP32.** Eleven of 60 written actors change decisions under TF32 and the TF32 step-0 score (about 0.37) sits below the exact one (0.50). A random update of the same size is as destructive as PPO's first update, which shows the weights are fragile, not that PPO's direction is special; small-step SGD keeps 0.2-0.3. The abstract scopes the claim to standard PPO on binary-success games. (E2)
4. **The written-against-learned comparison is one of information access, as the paper says:** writers read the source, learners see 15-30 starts per family, and the augmented learners did not fit their own training set. The result supports the reading that the source beats a handful of examples, not that writing beats learning. (E2, acknowledged by the paper)
5. **The difficulty trend is exploratory:** 20 families in strata of 3, 11, 5 and 1, assigned by the game author before results, no fixed test statistic, programs near ceiling; the abstract says the gap "grows". (E2)
6. **Writer involvement is disclosed and its effect untested:** an evaluated writer designed the harness and analysis, the games were authored with language-model help, prompts were piloted with evaluated writers, and Claude writers received a task-budget hint the others did not. (E2)
7. **Outsiders cannot re-run the headline numbers:** the level sources are withheld to keep them unseen, and writers are hosted models. The authors release the harness and result data and offer to evaluate submitted actors on request. (E2)
8. Minor: one run per cell for the ablations and the reactive-program control; bootstrap intervals of zero width at ceiling.

## What holds
Numbers recompute (below). The design is the most controlled of the objects in this series: hypotheses and decision rules dated before data, private games so recall is excluded, held-out level, template and palette separated, feedback compared with the best of k one-shot runs at matched cost, request accounting including refusals and discards, a limits section naming scope, estimation and independence, and a free-architecture condition labelled exploratory because its language was fixed after the fixed-actor results.

## Checks (E1)
`checks_arithmetic.py` and its output: the tensor sizes of the fixed actor sum to 57,289 and recompute from their shapes; the per-step multiply-accumulate counts recompute to 1.323, 0.190 and 1.318 GMAC (printed 1.32, 0.19, 1.31) when the input drive into the recurrence is applied once outside the 128-step loop; the request-accounting table satisfies its row identity and its column totals (5,900 sessions, 12,185 requests, 11,882 completed, 310 re-runs; 204 sessions without an artifact; 29 refusals); pooled means and family macros recompute; Wilson intervals for eight proportions match. The abstract's numbers match the tables.

## Depth rating (rubric in the series overview)
6.5 (D4; claim reach narrow): C1 1, C2 1, C3 0.5, C4 1, C5 1, C6 1, C7 1, C8 0. Non-blind (same reader, after the rubric and table existed), and only loosely comparable: the object is a test of a claim about weight writing, not an edit claim.

## What this adds to the series
It is the first object whose protocol states in advance what would count against its claim and accounts for every piece of target feedback used to build the written weights (feedback rounds, tokens, best-of-k), the two items the series' patterns 7 and the context note's candidate bar ask for. Its central finding, that a training-free writer's output is a program because training and search were forbidden, bears on pattern 3: the trained component upstream of a "training-free" step is the writer itself, and this paper measures what its feedback is worth (choosing the best of several one-shot runs recovers 45-70% of the gain from feedback).

## Limitations: what this does and does not establish
It establishes what the printed tables support and that they are arithmetically consistent. It does not establish that the headline findings hold on tasks with statistical perception or dense rewards (the paper says so), that the private games are representative, or anything about the released code (not run). One reader; figures read as images.

**Tier:** E1 executed (the checks above); E2 read (all 32 pages); E3 interpretation (flag 1). The three tools found no structural or severe gaps beyond those noted in the overview. **Deeper pass:** optional; the cheapest decisive test is re-computing the headline tables from the released per-session results, not done.

## Reproduction
`checks_arithmetic.py` (the Table 9 parser reads the text layer of page 24: regenerate it with `pdftotext -f 24 -l 24 -layout <paper.pdf> page24_text_layer.txt`) and `checks_arithmetic_output.txt`; `quote_checks_output.txt`; `tool_scan_*.json`.

## References
Sources: arXiv:2611.16981v1 (PDF sha256 beginning a7393dadb706a5bc); the numbers in the script are typed from its Tables 1-3, 5, 9, 15, 16, 18 and 19.

## Revision log
- *2026-11-13, v1.* Added to the series.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
