# Two Models Reported Better by Weight Edits: A Social Post's Claims, the Author's Reply, and the Toolkit They Rest On

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** Two objects: (a) a public social-media post with an image card (7 Nov 2026) claiming that an AI agent rewrote the weights of two models, a board-game network and a 1.5B coding model, with no gradient steps on either; the post's author is called "the author" and is not named; (b) the open-source toolkit repository the card names (commit 3188933, 8 Nov 2026), read for the artifacts that bear on the claims. The author's public replies to a reader's comment (7 Nov 2026) are summarised, not quoted. No intent is attributed. Locators are held privately.

**Disclosure.** AI-assisted (Claude, working under this project's own non-default standard; direction, selection and release decisions are the operator's); single reader. The post names Claude as the agent that wrote the edits, which the reader cannot verify; the edited models are Qwen and a game network. Read from screenshots of the card and the post text, the reply, and the repository (shallow clones on 7 Nov, at 21:00 UTC the same day, on 8 Nov at 15:00 and 19:07 UTC, and on 9 Nov at 01:28 UTC: five checks); nothing was run.

## What the claims are
Board-game network: edits built from the model's own probes, two sequential edits, +33 then +16 more Elo (+49 cumulative on the card), "92 neurons", each version required to beat the last in a sequential test on fresh games. Coding model: 13 MLP matrices solved in closed form from a 1-epoch reference fine-tune; MBPP+ 59.5 to 64.6 (fine-tune 57.4), HumanEval+ 65.2 to 68.3 (fine-tune 61.6); 40 problems fixed, 16 broken, p = 0.002; MMLU and WikiText unchanged. The card's headline says both models got better. The post adds a probe AUROC of 0.99 for knowing an open corner and a 45% rate of taking it, says that games and tests decided what stayed, and credits a third-party report that an AI can edit weights.

## Flags (ranked; post hoc)
1. **The headline results are not reproducible from public artifacts.** Across five checks over about a day and a half the repository held no coding-model scripts, no game code or logs, no per-item outputs, no MMLU or WikiText numbers, no probe script and no decontamination method; the author said the scripts exist but were not yet in the repository. (E1 absence by repeated clone and term search)
2. **Selection on the reporting set, conceded in the reply.** The layers (MLPs 6-18) were chosen on decontaminated coding practice problems, by eye from a per-layer comparison; there is no strength parameter. Two settings of the final edit were chosen after seeing an earlier version's benchmark scores and four candidates were scored, so p = 0.002 is for a selected candidate (about 0.007 corrected: recomputed 0.0074 by Bonferroni over four) and is not a sealed test. No fresh-split confirmation exists yet; the plan is a frozen edit paired against the original on new problems. The card's subtitle says held-out; that is true of the layer choice, not of the final settings. (E1 for arithmetic; the settings history is the author's statement)
3. **"No training" names the edit step.** The edit is closed-form but solved from a gradient-trained reference fine-tune; the fine-tune baseline (one epoch, one run) ends below the original model. A tuned or partly interpolated fine-tune is not compared. (E1 card; the baseline point is E2)
4. **The Elo claims rest on numbers the reply supplies.** 4,926 distinct openings with both colours gives 9,852 games; the sequential test called at pair 3,581 (error level 0.0012); score 52.3% with a rough interval of 51.3-53.3% (+9 to +23 Elo, recomputed). About 1,800 games resolve +16 Elo at a fixed sample (two-sided 95%), so the size is adequate. Games within an opening are paired and per-pair outcomes are not public, so a pair-level interval cannot be computed. Across five Othello tests, rejected ones included, the author reports 4.45% error budget spent, not under 0.5%. (E1 arithmetic; counts are the author's)
5. **Probe numbers.** The 0.99 AUROC is in-sample; the 45% corner rate is held out (2024 games; edits designed on 2023 games), per the reply. (author's statement)
6. **The edit's side effects are unquantified on the card.** MMLU and WikiText are said to be unchanged, with no numbers or tolerance.
7. **Authorship.** The post credits an AI model with discovering and writing the edit; no transcripts or logs are public. (E1 absence)

## The repository (a different, better-documented artifact)
The toolkit measures what a prompt, a fine-tune or a weight edit teaches in bits and ships a sequential test where "Undecided is not a pass". Its GPT-2 install demo uses separate pick and judging splits; a notebook installs a three-line review-grading system prompt into Qwen2.5-1.5B-Instruct in closed form and measures it on 256 held-out reviews: task score 0.000 unedited, 0.966 edited, 0.973 prompted; the weights hold 97% of the prompt's bits; WikiText +0.018 bits per token (within 0.05: yes), general chat +0.020 (within 0.05: not sure, reported as undecided); layers are chosen by a trained readout on a split disjoint from the test split. The edit has no gradient steps; the layer-choice readout is trained. This is a stronger artifact than the post's headline claims and is on a different task.

## What holds
The card's arithmetic is consistent (task counts of 378 and 164, the usual sizes of the two benchmarks, are assumed; the card does not state them): every percentage maps to an integer count; 24 net problems equals the gain across 378 + 164 tasks; the exact sign test on 40 vs 16 gives p = 0.0018 (card: 0.002). The author answered the specific questions within hours, conceded the selection, corrected two overclaims, and gave the numbers above.

## Predictions, and what changed
Fixed before each check: that the author's reply would expose benchmark-informed choices (it did); that scripts would appear within a day (they did not); that the repository moved (it did, to different work). Two priors were wrong: the reply was more open than expected; the repository converged on an artifact for the mechanism, not the post's claims.

## Limitations: what this does and does not establish
It establishes that the post's arithmetic is consistent, that its headline results could not be checked against public artifacts as of 2026-11-09, and that the author conceded benchmark-informed settings. It does not establish that the results are wrong, that the edits do not work, or anything about intent; the scripts the author mentions may settle the open items. The post, card and reply are known only from screenshots, and the author's statements in the reply are testimony until the artifacts are public.

**Tier:** E1 executed (arithmetic: `checks_arithmetic.py`; repository term search and notebook text read); E2 read (post and card from screenshots; reply from a screenshot; repository README, docs and the notebook); E3 interpretation (flag 3's baseline remark; flag 7).
**Deeper pass:** recommended when the scripts appear: re-read the selection rule, game logs and the frozen-edit result. Not done.

## Reproduction
`checks_arithmetic.py` with output; `quote_checks_output.txt`; `tool_scan_*.json`. The post, card and reply are held as screenshots (not stored here).

## References
Sources: the social post, its image card and the author's public reply (screenshots, held privately) and the toolkit repository (commit 3188933); the numbers recomputed in `checks_arithmetic.py` are typed from them.

## Revision log
- *2026-11-09, v1 (pre-draft).* Private pre-build.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
