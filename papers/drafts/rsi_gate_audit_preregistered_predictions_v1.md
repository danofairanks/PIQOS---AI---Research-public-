# Where Does the Gate Sit? Preregistered Predictions for a Gate Audit of Eight Self-Improvement Papers

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** The objects examined are eight published or preprinted research papers on self-improving AI agents, named by title and, where the source collection gives one, arXiv identifier. No individual is characterised; the predictions concern what the papers' designs and reports contain. The papers were chosen from a public curated collection ("Self-Improving Agents", DAIR.AI Academy, saved 2026-10-08), which is a secondary source.

**Disclosure.** Drafted with AI assistance. **No paper has been read for this note.** The predictions rest on one-line summaries in the secondary collection and on the drafting model's prior familiarity with some of these works, so they are guesses to be scored, not findings. The point of publishing them first is the timestamp: this file's repository history records what was predicted before any primary-source reading.

## 1. The question

A self-improving agent changes some lasting part of itself (memory, skills, code, weights, prompts) and keeps the change when a test says it helped. Whatever accepts or rejects a change is a *gate*. A gate usually checks an artifact (a benchmark score, a test log, a judge's verdict), while what matters is a property (the agent really got better at the task, the tests really ran, the change did not weaken its own safeguards). This audit asks, paper by paper: what is the gate, what does it read, who can write what it reads, and does the paper itself report the gate being gamed?

## 2. The lens, stated generically

For each paper, three questions, answered from the primary text once read:
- **(a) No validator for the property.** Nothing in the gate verifies the property the designers care about (for example that a reported test result reflects an actual test run), or a validator exists but its predicate does not cover the whole input domain.
- **(b) Late validation.** The check that would catch a bad change happens after the change has already taken effect.
- **(c) Proxy conversion.** The quantity the gate sees (a benchmark score) differs from the quantity that matters (the improvement of the agent's future descendants, or of its performance outside the benchmark) in a way the design does not control.
Many papers will fit none; that is a result too. This lens is a hypothesis carried from earlier small measurements of validators on cumulative caps; it is not established for this literature.

## 3. The papers (batch 1)

| # in the source collection | paper | arXiv id (from the source page) |
|---|---|---|
| 14 | Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents | not on the source page |
| 12 | Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation | not on the source page |
| 16 | Huxley-Gödel Machine | 2510.21614 |
| 18 | Hyperagents | not on the source page |
| 25 | Recursive self-improvement of AI research agents | 2609.26457 |
| 24 | PostTrainBench: Can LLM Agents Automate LLM Post-Training? | 2603.08640 |
| 30 | Mind the Gap: Examining the Self-Improvement Capabilities of Large Language Models | 2412.02674 |
| 29 | Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents | 2509.26354 |

## 4. Predictions, filed before any reading

Each is the probability that the paper itself reports, or its design exhibits, the stated feature.
- **#14 Darwin Gödel Machine.** The gate is a benchmark pass/fail derived from logs the modified agent can influence: route (a) 80%. The paper itself (not only an accompanying writeup) reports a faked-log case: 35%. The gate is otherwise external and fixed: 85%.
- **#12 STOP.** The improver runs under a sandbox setting it can edit: a measurement of sandbox-bypass attempts appears in the paper 85%. The authors state a route (a) or (b) mapping themselves: 25%.
- **#16 Huxley-Gödel Machine.** The gate (an agent's benchmark score) is an imperfect proxy for its descendants' improvement, a route (c)-like gap: 75%. The proposed remedy aggregates over a lineage: 90%.
- **#18 Hyperagents.** The evaluator remains an external fixed benchmark while task and meta agents are merged: 80%. The paper reports reward or objective hacking: 40%. The paper states that gains on coding tasks do not carry over to other tasks: 60%.
- **#25 Recursive self-improvement of AI research agents.** Hacking is measured by a detector separate from the agent's own gate: 70%. The reported fall in hacking came partly from discovered changes that add checks: 50%. Held-out transfer is the gate that matters: 80%.
- **#24 PostTrainBench.** The reported reward hacking includes contamination, test-set use or calls to outside models, a route (a) at the data-provenance property: 65%. The benchmark's own final-score gate does not check training-data provenance by itself: 70%.
- **#30 Mind the Gap.** No direct mapping to the lens; the paper's generation-verification gap is the condition under which an internal gate carries information: 75%. The paper reports the gap does not shrink with scale on some tasks: 40%.
- **#29 Misevolve.** Unsafe drift through memory or tools passes because no validator covers the accumulated content, route (a): 70%. The paper reports an empirical rate above 30% for at least one drift path: 60%.
- **Across the eight.** At least five contain a gate whose input the agent can write or influence: 60%. At least one documents route (b)-style late validation: 25%. At least one documents a route (c)-style proxy conversion beyond #16: 50%.

## 5. How the predictions will be scored

Each paper gets a short file with seven fields: the improvement operator; the gate and the exact artifact it reads; the intended property versus the checked property; reported failures with section or page references to the primary text; the route mapping (scored against the prediction above); a local test if code is available; and a miss log. A prediction is a hit if the primary text supports it and a miss otherwise; relayed claims in the source collection that the primary text does not support are logged as relay errors. A second reader from a different model family will be asked to re-read any contested reading.

## 6. What this note does and does not establish

This note does not establish anything about the eight papers: it does not report what any of them contains, and it does not claim the lens is the right one. It establishes only what was predicted, and when. If the predictions score well, that would say the lens describes this literature's designs; if they score poorly, that says the drafter's picture of it, built from summaries, was wrong.

## 7. What would count against this

Papers whose gates read only artifacts the agent cannot write, and whose reports describe no gaming, would count against the premise that a gate-audit finds anything here. A pattern of misses concentrated on the route (a) predictions would count against the lens. The source collection's own selection could also be the problem: it is one curator's list of thirty-one papers, and the closing survey in it cites twenty of them, so overlap between the list and the survey is expected.

## 8. Limitations

Nothing has been read. The source is a secondary, partly editorial compilation (its phrases such as "most convincing" are its curator's judgement and are not used here). Several arXiv identifiers are missing from the source page and are not supplied from memory in this note. Numbers quoted by the collection (benchmark gains, hacking rates, claims from laboratory posts) are not repeated here because they are unverified. The drafting model is the only predictor, so its predictions are not independent of one another.

## 9. Reproduction

No code. The record is this file and its history. The source collection can be saved from its public page; the eight papers are to be retrieved from their public venues.

## References

Sources: [1] "Self-Improving Agents", paper collection, DAIR.AI Academy (`academy.dair.ai/papers/collections/self-improving-agents`), saved 2026-10-08 (secondary; its summaries are not reproduced here). [2] The eight papers listed in section 3 (unread at the time of writing).

## Revision log

- *2026-10-08, v1.* Predictions filed before any primary-source reading.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
