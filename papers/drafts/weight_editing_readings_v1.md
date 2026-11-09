# Weight-Editing Claims: Eight Readings of Posts, Papers, Reports and Releases for Whether the Evidence Supports the Edit Claimed

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** Eight objects are read in their own folders, `weight_editing_readings_v1/<name>/README.md`, plus a context note on the editing literature. Papers, reports and institutions are named as each names itself (a research blog post from MIT CSAIL, an arXiv paper, a security lab's report); private individuals and small vendors (a social-media post's author, a developer blog's author, a model-card vendor) are described by role and not named, and their locators are held privately. Authors of papers are called "the authors". Six objects were read first; two arXiv papers from one group (Steer2Edit and ThinkEdit) were added on 2026-11-09. No intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance. One reader, an AI system, wrote every reading, and the reader is an Anthropic model. Same-vendor points are marked in the individual readings: one post names Claude as the agent that wrote the edits; one paper's declaration lists Claude among its writing aids. One added paper uses Claude Opus 4.6 as an alternative labeling judge in a robustness check and names Claude Sonnet 4.5 inside a baseline's design; the other uses no API model. The edited models in the first six readings are Qwen, Pythia and Gemma models (the two added papers edit LLaMA, Mistral, Gemma, Qwen and DeepSeek-distilled models); the frontier editor in the MIT release is an OpenAI model per the release README. Readings are post hoc unless a folder says predictions were fixed first; in this series predictions were committed in private working notes before each reading, and each reading says what they got wrong. Nothing was run except arithmetic, term scans, and recomputations from released data files; no model was downloaded and no code from a third party was executed.

## 1. What this series is
Claims that a model's weights were edited, rewritten, written to or patched, and that the model got better, safer, more knowledgeable or less restricted as a result. The question in each reading is narrow: does the evidence presented support the edit as described, at the reach the claim has? It does not decide whether any claim is true, and it does not cover prompting, retrieval, or ordinary training claims except where an object compares itself with them. It is the companion of benchmark-validity readings (which ask whether a score supports an inference), and it covers vendor posts and releases that series excludes.

## 2. Entries
| Reading | Object | Main finding |
|---|---|---|
| [`math_model_edit_by_frontier_model/`](weight_editing_readings_v1/math_model_edit_by_frontier_model/README.md) | MIT CSAIL blog post and released logs: a frontier model edits Qwen3.5-0.8B (50-pass run: MATH-500 7.9 to 48.1) | Best-documented wide claim: a confirmation set matches the test results and data are released; but the reported runs are a subset, the prompt names the failure, and the gain is mostly termination under one decoding configuration |
| [`prompt_and_edit_post_with_open_toolkit/`](weight_editing_readings_v1/prompt_and_edit_post_with_open_toolkit/README.md) | A social post claiming two models got better by closed-form edits, the author's reply, and the open toolkit behind it | Arithmetic holds; the headline results are not reproducible from public artifacts over five checks; the author conceded benchmark-informed settings (p about 0.007 corrected, not sealed); the toolkit's own demonstrations are better documented than the post |
| [`agent_edits_six_model_kinds/`](weight_editing_readings_v1/agent_edits_six_model_kinds/README.md) | A developer blog post and repository replicating the MIT post with a coding agent | Careful held-out design on one task; the new-scam result equals the data-generating rule; different method from the one replicated; the language-model replication is a weak-setting proxy |
| [`self_optimizing_adapter_agent/`](weight_editing_readings_v1/self_optimizing_adapter_agent/README.md) | arXiv 2605.20189v1 (SOLAR) | First of three levels run; a strategy chosen per benchmark against fixed baselines, some at or below chance; no intervals |
| [`agentic_self_modification_report/`](weight_editing_readings_v1/agentic_self_modification_report/README.md) (adjacent: fine-tuning) | A security lab's report: an agent retrains and redeploys the model it runs on | Most explicit about limits; counts without intervals and a human nudge in a headline example; governance point stated carefully, reversal untested |
| [`weight_engineering_vendor_releases/`](weight_editing_readings_v1/weight_engineering_vendor_releases/README.md) | A weight-engineering vendor's 71 model releases and pitch pages | Corrections live on the cards (6 of 70, in a two-day sprint), the pitch pages predate them and still carry the withdrawn headline figures and no-training wording; rigor varies widely across releases |
| [`steer2edit_component_level_editing/`](weight_editing_readings_v1/steer2edit_component_level_editing/README.md) | arXiv 2602.09870v3 (Steer2Edit): closed-form rank-1 edits of attention heads and MLP neurons built from steering vectors | The three headline gains are derived nowhere and the explicit comparisons are not utility-matched (70B: safety +30.4 at utility -31%); best configurations give up benign accuracy (Qwen3-4B-Thinking -10.5 points); strengths ranked on the target metric; no intervals |
| [`thinkedit_short_reasoning_heads/`](weight_editing_readings_v1/thinkedit_short_reasoning_heads/README.md) | arXiv 2503.22048v4 (ThinkEdit): orthogonalizing 4% of attention heads against a short-reasoning direction | Headline averages do not reproduce from the tables (+2.91 and +5.43 against +3.34 and +6.39); short-tail subsets differ between conditions; gains concentrate where reasoning also lengthens about 50%; no random-head control |
| [`literature_context/`](weight_editing_readings_v1/literature_context/README.md) | Context note | The evaluation battery, forgetting, durability and error-budget work exist; no object cites the adverse results about its own method class; feedback accounting for edits was not found |

## 3. The depth rating (applied during reading; a working summary, not an instrument)
Each object's headline claim was scored against eight criteria (0, 0.5 or 1): C1 a control for the base or prior behaviour; C2 paired statistics or intervals on a full-size evaluation; C3 public reproducibility artifacts; C4 a measure beyond the items used to build or select the edit; C5 cost and side effects measured; C6 limits and withdrawals named where the claim is made; C7 selection disclosed; C8 independent verification. Totals map to levels D0 (0-1.0), D1 (1.5-2.5), D2 (3.0-4.5), D3 (5.0-6.0), D4 (6.5-7.5), D5 (8.0). The full rubric text is `rubric_v1.txt` (sha256 22899837ab5f0080...). Reach (narrow, medium, wide) is read against depth.
| Object | Total | Level | Reach |
|---|---|---|---|
| A vendor's 1.4B knowledge-writing card (rebuilt) | 7.0 | D4 | narrow |
| The open toolkit's GPT-2 install demonstration | 6.5 | D4 | narrow |
| MIT math-model edit (blog and logs) | 6.0 | D3 | wide |
| The open toolkit's skill-installation notebook | 6.0 | D3 | narrow-medium |
| A vendor's 6.9B card (rebuilt) | 5.5 | D3 | narrow |
| The security lab's report | 5.0 | D3 | medium |
| ThinkEdit (added) | 4.5 | D2 | medium |
| The developer's six-model post | 4.0 | D2 | medium-wide |
| The social post's coding and game claims | 3.5 | D2 | medium-wide |
| Steer2Edit (added) | 3.0 | D2 | medium |
| A vendor's compliance-removal card | 1.5 | D1 | wide |
| SOLAR | 1.5 | D1 | wide |
| A vendor's pitch pages | 0.5 | D0 | wide |
**Caveats on the rating.** One rater; the rubric was written after reading the first ten objects and so inherits their failure modes; equal weights; half-points are judgment calls; reach assignments are the reader's. It was reused once (the notebook row) by the same rater after seeing the table, so that reuse was not blind and is a consistency check, not a test. The two rows marked added were rated by the same reader after the rubric and the table existed, so they are not blind either. No score is a verdict on whether a claim is true.

## 4. Evidence tier and deeper-pass flag
Every reading ends with two lines. **Tier:** E1 executed (state what: arithmetic on reported numbers, a recomputation from released data, a term scan), E2 read (state what was and was not read), E3 interpretation (name the flags that are interpretation). **Deeper pass:** recommended, optional or no, with the cheapest decisive test and whether it has been done.

## 5. Patterns across the readings (all post hoc; eight objects, not a rate)
1. **Depth falls as reach rises.** The three deepest objects claim the least (narrow reach). The widest claims sit on the shallowest evidence (pitch pages D0, a compliance-removal card D1, SOLAR D1); the one wide claim at D3 is the one with released logs and a fresh-set confirmation.
2. **The same actor appears at both ends.** One vendor's rebuilt cards rate D3-D4 and its pitch pages D0; one toolkit's repository demonstration rates D4 and its author's post D2. The difference is the audience, not the competence.
3. **"No training" names the edit step, not the pipeline.** The coding-model edit is closed-form from a gradient-trained reference fine-tune; the math-model edit is made by a trained frontier model scored on practice problems; the vendor's knowledge-writing edit is 10,000 SGD updates on 738 million parameters, which its card now says and its pitch page does not; the developer's edits are given the correct answer. A useful question for any such claim: what trained component or supplied answer sits upstream of the training-free step? (Added: Steer2Edit's training-free edit rests on labelled behaviour sets and, for truthfulness, a 32B judge's labels; its abstract names neither.)
4. **Selection on the reporting set or among runs is the recurrent gap.** Two settings after benchmark scores and four candidates (the social post); about ten runs with three reported (the MIT release); a strategy per benchmark (SOLAR); layers chosen by eye on practice data; edit strengths ranked on the target metric over a small validation set (Steer2Edit); an editing rate swept on the reported test benchmarks without a stated rule for the one reported (ThinkEdit).
5. **A correction on the card and not on the pitch.** One vendor's corrections landed on 6 of 70 cards in a two-day sprint, while the pitch pages, dated before it, still carried the withdrawn headline figures and no-training wording four to five days later (the lag at the read; the later state is unknown).
6. **Adverse literature is not cited about the object's own class.** A term scan of the first six objects found none that cites forgetting under sequential editing, relearning or restoration, or tampering in self-modifying loops. One vendor page uses the failures of competitors' methods against them and none of its own. (The two added papers were not scanned for this.)
7. **Controls in practice, not defeat conditions in advance.** A norm-matched random control and a null result on a non-looping model (the MIT release), a deranged-answer control (one vendor card), reported failed replications (the developer's post): each is a good control; none of the objects states what result would count against its claim.
8. **A headline number with no derivation.** In two of the eight objects the abstract's headline averages are not derived in the paper: Steer2Edit's three gains are defined nowhere, and ThinkEdit's two averages do not reproduce from its own tables (+2.91 and +5.43 from the tables as read, against +3.34 and +6.39 in the abstract). In both, the more detailed tables describe operating points that cost accuracy elsewhere (Qwen3-4B-Thinking -10.5 points; reasoning on easy sets about 50% longer).

## 6. Verification, and what is not claimed
- **Quoted strings.** `quote_checks_output.txt` (per entry): every double-quoted string was tested against the extracted text of its source; results in the file.
- **Arithmetic.** `checks_arithmetic.py` reproduces every recomputed number cited, with its output.
- **Scans.** `checks_card_count.py` and `checks_citation_scan.py` (term lists fixed before running; counts only in the outputs). paper_rigor, verification_lint and attractor_scan were run on every reading and on this overview: no structural or severe gaps; attractor_scan's weak flags on the added rows (the words "safety" and "reasoning") were read directly and are the papers' own measured quantity and subject, not laundering.
- **Not done.** No object's code was run; no model was downloaded; the MIT edit was not rebuilt; the vendor pages were not dated by archive copies; the social post's headline results could not be checked because the scripts were not public (five checks, last 2026-11-09 01:28 UTC); the figures of papers were read as extracted text.

## 7. Related
The benchmark-validity readings series (what a score supports); the editing-literature context note in this folder.

## 8. Limitations: what this does and does not establish
- Eight objects chosen by what reached the reader, not sampled; nothing here is a rate.
- One reader per object; the same model family wrote the readings and is named inside two of the objects.
- The rubric and the candidate bar were built after the readings; the depth ratings are a summary, not an instrument.
- Search for the literature context used a search tool whose summaries contained identifier errors; every identifier was re-fetched, but no full text beyond the stated methods and passages was read.
- The series establishes dated readings and recomputations of what each object presents; it does not establish that any claim is false, that any author acted in bad faith, or a rate across the field.
- Several objects are changing: the social post's author promised scripts; the vendor's pages may be updated; the toolkit's repository moves daily.

## 9. Reproduction
`rubric_v1.txt`; `checks_arithmetic.py`; `checks_arithmetic_added_papers.py` (the two added papers); `checks_card_count.py`; `checks_citation_scan.py`; each entry's `quote_checks_output.txt` and `tool_scan_*.json`.

## References
Sources: the objects named in the scope lines (arXiv identifiers and PDF hashes where applicable); the identifiers in `weight_editing_readings_v1/literature_context/`.

## Revision log
- *2026-11-09, v1 (pre-draft).* Private pre-build.
- *2026-11-09, v1.* Published as a draft (six readings and a context note).
- *2026-11-09, v1, edit.* Added two readings (Steer2Edit, ThinkEdit), their arithmetic script, two depth-table rows (not blind) and pattern 8.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
