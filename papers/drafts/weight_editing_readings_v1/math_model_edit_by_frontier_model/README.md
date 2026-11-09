# A Weight Edit Written by a Frontier Model, Read Against Its Released Logs: Qwen3.5-0.8B and the 48.1% Headline

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is a research blog post from MIT CSAIL titled "Sparks of Weight-Space Programming" (four authors, read 2026-11-07/08) and the release of its complete experiment logs (a public repository, commit 4d09ba6, 2026-10-29), restricted to Experiment 8: a frontier model edits the weights of Qwen3.5-0.8B without gradients to improve its math scores. The authors are called "the authors". The release README identifies the editing model as OpenAI's gpt-6-astra; the reading says "the editor". No individual is named and no intent is attributed to anyone. The post is a blog, not a peer-reviewed paper.

**Disclosure.** Drafted with AI assistance; one reader, an AI system (an Anthropic model); neither the editor nor the edited model is an Anthropic model. Read: the post text, the release README and the Experiment 8 README, the results-table excerpt, the editor's final report and run record for the 50-pass run, the four experimenter notices, and the per-problem evaluation files (recomputed, below). Not read: Experiments 1-7, the code, the per-step explanations.

## What it is
A frontier model gets a Python kernel over the weights of Qwen3.5-0.8B (CPU only), practice problems from the GSM8K and MATH training sets (never the evaluation sets) and a budget of 10, 25 or 50 forward passes; it may not train or use gradients. It submits an edit. The post reports MATH-500 7.9% to 48.1% and GSM8K 13.8% to 67.1% for the 50-pass run, and a Gemma 3 270M follow-up where the editor "could not improve" the model.

## Flags (ranked; post hoc)
1. **The reported runs are a subset of the runs done.** The release README states: "Only the runs the post reports are here. Trial runs of earlier prompt versions are left out." The results-table excerpt lists additional rows that are not in the post: a 0-pass run on an earlier prompt, a 5-pass run and a v4 10-pass run that submitted no edit, a v4 25-pass run with the same scores as the reported 25-pass run, two unsubmitted candidates (MATH-500 8.6 and 10.1), and four rows of a later prompt version with no results yet. The 50-pass effect is one run with no replicate released. The three reported edits are three different edits (a direction removed from 30 matrices; one attention head zeroed; a direction removed from the MLP outputs of two layers), so the budgets are not a dose-response of one method. (E1)
2. **The task prompt names the failure.** The first message tells the editor to look at answers that are "cut off at the token limit" often while repeating themselves, and that repairing a specific failure mechanism is in scope. The post's wording that the editor spots and fixes a common failure leaves out that the prompt points at it; the choice of layers and direction is the editor's own. (E1)
3. **The gain is mostly termination.** Under the evaluation protocol the unedited model reaches the 32,768-token limit on 93.0% of MATH-500 answers (98.7% of OlympiadBench, 100% of AIME24/25). The editor's own report says 576 of 579 rescues on its confirmation set were originally truncated outputs and that accuracy on originally finished outputs was unchanged. The post says "Fixing loops, however, is not the same as making a model better at math", and the Gemma control (6.8% to 7.7%, a model that rarely loops) agrees. (E1; the editor's statement is testimony)
4. **One baseline configuration.** Sampling is thinking on, temperature 0.6, top-p 0.95, top-k 20, presence penalty 1.5, 32,768 tokens. The logs hold no unedited run under another configuration, so how much of the 7.9% base is a property of this configuration and how much of the model is not measured. (E1 absence)
5. **Human intervention inside the runs.** The release holds four experimenter notices sent to running sessions (pass-size guidance, tool corrections, a changed submission rule to submit the best edit even if not significant, a grader-count correction); the README says the first two reached these runs. One turn was refused by a content filter, one was redone after a restart, one run waited 4.7 hours for the model. All are listed in the README. (E1)
6. **No adverse literature is cited.** The post's one sentence on forgetting says editing can avoid the catastrophic forgetting that fine-tuning often causes; it does not cite the work on forgetting under sequential editing, relearning after removal, or tampering in self-modifying loops (see `literature_context/`). (E1 term scan of the post text)

## What holds
The strongest point: the editor's confirmation on 1,152 fresh practice problems (10.6% to 60.4%, paired gain +49.8 points, standard error 1.5, 579 rescues, 5 losses) matches the later test results, so there is no sign of selection on the evaluation sets, which the editor never saw. The per-problem evaluation data and the exact weight diff are released, beyond-math benchmarks are reported (MMLU-Pro 40.3 to 45.5, GPQA Diamond 22.7 to 36.6, IFEval 21.0 to 62.3), and the null Gemma result is in the post. Recomputed from the per-problem files (bootstrap over problems, 2,000 draws): MATH-500 7.9 [6.1, 9.8] to 48.1 [44.4, 51.7], paired +40.2 [36.9, 43.6]; GSM8K 13.8 [12.3, 15.4] to 67.1 [64.8, 69.3], paired +53.3 [51.0, 55.6]; the 10- and 25-pass runs are not distinguishable from each other on either benchmark. Sampling noise is not the issue; run-level replication is.

## Predictions, and what changed
Predictions were fixed before the logs were read (selection among candidates, benchmarks never in the practice set, a single run per budget, per-problem data possibly absent). Two were wrong: the per-problem data are released (so the intervals above could be recomputed), and the loop awareness came from the prompt, not the model card.

## Limitations: what this does and does not establish
It establishes that, in these logs, the edit repaired a looping failure on this model under this protocol, with a confirmation set that matches the test results. It does not establish capability gain beyond termination, replication of the 50-pass result, behaviour under other decoding settings, or generality to other models (Gemma control: no gain).

**Tier:** E1 executed (bootstrap intervals from the released per-problem files; the release tables and the editor's final report read; counts from run records); E2 read (README and Experiment 8 README in full; the rest of the release not read); E3 interpretation (flags 3 and 4 read the logs as showing termination repair and an untested configuration).
**Deeper pass:** optional. Cheapest decisive test: rebuild the edited tensors from the public weights with the released diff tool and score the unedited model under two other decoding configurations. Not done (needs a model download).

## Reproduction
`checks_arithmetic.py` (typed totals); the bootstrap used the released per-problem files (not stored here); `quote_checks_output.txt`; `tool_scan_*.json`.

## References
Sources: the MIT CSAIL post "Sparks of Weight-Space Programming" and its released experiment logs (repository commit 4d09ba6, 2026-10-29); the numbers recomputed here are typed from the release tables and computed from its per-problem evaluation files.

## Revision log
- *2026-11-09, v1 (pre-draft).* Private pre-build; not for publication until the operator asks.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
