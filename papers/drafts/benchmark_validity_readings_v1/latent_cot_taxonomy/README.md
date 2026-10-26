# A Taxonomy That Cannot Be Contradicted: Reading "Does Latent Chain-of-Thought Actually Reason?"

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one paper, "Does Latent Chain-of-Thought Actually Reason? A Single, Unifying Taxonomy for Latent Reasoning" (arXiv:2610.21182v1, 15 October 2026; the paper names UCSD, NYU, UVA and Adobe). The authors are called "the authors"; organisations are named only as the paper names them. No individual is named and no intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance; one reader, an AI system. Read from an operator-supplied copy (22 pp). Read: body, setup, appendices on taxonomy rules, controls and cell assignments. Skimmed: probe tables (App. C), trajectory details (App. D), supplements. Figures not seen. Lens: the series overview. Same-source caveat: single Anthropic-model reader. Post-hoc; see the predictions file in this folder. Code and checkpoints not accessed.

## What it is
Coconut, CODI and SIM-CoT-Coconut on GPT-2 and Llama-3.2-1B-Instruct; ProsQA, PrOntoQA, GSM8k; 21 cells, N = 300 held-out problems each, T = 6 slots. RQ1: delete the chain or replace its contents (noise, dataset mean, donor). RQ2: linear probes (PCA-30 + logistic regression; ridge arm on ProsQA) against permuted-label nulls. RQ3: step size, settling, along-answer movement, mid-chain edits. Output: a six-leaf taxonomy (carrier, empty, bare placeholder, laid-out placeholder, assembling, unstructured) with unclassified cells left out.

## Flags (ranked; post-hoc)
1. **"Predictive rather than descriptive" is largely tautological.** The placeholder leaf is defined by "no replacement moves an answer"; the prediction that placeholders stay immune to a different-answer donor at twice natural norm repeats part of the definition, since donor replacement is one of the three defining tests. Carriers are defined by deletion changing <= 3 answers, so "unaffected by corruption" restates it. "the only chain helped by donor thoughts is classified as assembling" is one cell. A cell where use and profile disagree "would name no leaf", so the claim that the two readings agree wherever both resolve is protected by the rule that leaves disagreeing cells unclassified.
2. **Reconciliation of prior work is by assignment.** Prior reports (three earlier papers) are each mapped to a leaf. Leaf sizes (C2): carrier 5, unstructured 6, assembling 2, empty 2, bare placeholder 1, laid-out placeholder 1, inert unprofiled 2, unclassified 2 (total 21). A tree this fine-grained over 21 cells can place most prior reports somewhere.
3. **Main causal comparison has a thin control.** COCONUT vs SIM-CoT-COCONUT mixes public checkpoints (Dilgren & Wiegreffe) with the authors' own runs. The loss-off control exists for ProsQA only: inert on GPT-2, unresolved on Llama; none for PrOntoQA or GSM8k. "Per-step supervision can establish dependence" is cleanly tested in one cell.
4. **Backbone claims have n = 2.** Finding 8 ("is set by the backbone, not the mechanism or the supervision") compares GPT-2 and Llama-3.2-1B-Instruct, which also differ in scale, instruction tuning, tokenizer and checkpoint source. The paper concedes the confound in Section 3.2 but phrases the finding causally.
5. **Sample size was enlarged after a near-threshold read.** The backbone comparison was enlarged once to 480 twins; gaps at 83-86% of their MDE "cleared it after". The power calculation is stated to be under a protocol frozen before scoring. The "recorded before the first forward pass" claim comes with no registry or timestamp in the text.
6. **Near-ceiling logical tasks.** COCONUT scores 0.97-0.99 on ProsQA and PrOntoQA, and the answer is readable at the question's final hidden state, so "inert" shows the chain is not consulted for these tasks, not that the recipe cannot train a consulted chain. The paper says inert does not prove no role in the intact pass, and its SIM-CoT result partly answers this.
7. **Absence claims rest on linear probes.** "No slot holds both candidates", path stored uniformly and early steps not readable are statements about PCA-30 + logistic regression, a ridge arm and a nonlinear check (largest gain 0.0067).
8. **Thresholds are discretisations.** inert <= 3 changed answers, settles early >= 0.5 slots under all 5 seeds. Seeds agree on 146 of 153 verdicts, but no sensitivity of leaf assignment to the thresholds is shown, and only the backbone gaps get Holm correction.
9. **Title and agent paragraph reach past the data.** "Actually reason" is not defined or measured; the paper measures use, content and dynamics and concludes "reading a latent trace certifies representation, not computation", which is supported. The agents paragraph is conditional but extrapolates from a 124M and a 1B model.
10. **Disclosure:** AI tools wrote the analysis code and gave feedback on interpretation; no independent code audit is mentioned.

## Holds
Readability and causal use dissociate (carriers: readable answer, inert; laid-out placeholder: ordered content, no replacement moves the answer). Paired deletion plus replacement is more informative than single-corruption tests. Each test reports an MDE; unresolved cells are kept apart from nulls. Checkpoint selection (Llama/PrOntoQA) disclosed; public checkpoints verified against reported accuracy. Findings 1 and 4 agree with the prior work they cite. The deletion-vs-donor counts reproduce (C1: five worse, margins 0.053-0.334; one milder, GPT-2 SIM-CoT/ProsQA, -0.116; two tied or milder, Llama COCONUT -0.037 and SIM-CoT +0.004).

## Evidence tier and deeper-pass flag
**Tier:** E2 read (body and the taxonomy, controls and cell-assignment appendices; other appendices skimmed; no figures). E1 on reported values only: deletion-vs-donor contrast and the leaf census (checks.py). E3: flags 1, 2 and 9 are interpretation of how the taxonomy is built.
**Deeper pass:** optional. Headline depends on flags 3 and 6; public checkpoints and the authors' code are named in the paper. Decisive tests: a loss-off control on PrOntoQA and GSM8k, and a positive-control replacement on the placeholder cell (Llama SIM-CoT/ProsQA). Moderate compute; recommended only if the taxonomy is relied on elsewhere. Not done.

## Open
Where the pre-registration record is held; appendix C-D tables (probes, trajectory nulls); whether leaf assignments survive moving the thresholds; the loss-off controls the paper lacks.

## Limitations: what this does and does not establish

- One reader, an AI system, reading a paper and its tables; the flags above are leads, each tied to a page or table, not verdicts, and a paper may answer them in places not read (see what was read and not read at the top and under Open).
- The number of flags is not a severity ranking (see the series overview).
- Evidence classes: E1 executed here (scripts and their outputs in this folder), E2 read, E3 interpretation, as marked in the text.

## Reproduction

Everything is in `benchmark_validity_readings_v1/latent_cot_taxonomy/`: `predictions_fixed_2026-10-25.md`; `checks.py`; `checks_output.txt`; `quote_checks_output.txt`; `tool_scan_*.json`. Re-fetched from arXiv on 2026-10-26: the file is byte-identical (sha256 `e194637805ec7f87c277f90cd1698d6f4235a3fe12942d2e2ec2ec659555c065`). `quote_checks.py` (in the series folder) reports which double-quoted strings of this reading occur in the paper's text layer; strings that did not match were rewritten as paraphrases or corrected to the paper's wording before publication. The paper's PDF is not stored here; the preregistration and the scripts are.
- **Predictions** were fixed before the measurement they concern (`predictions_fixed_2026-10-25.md`); that order is the evaluator's own record and is not independently timestamped.

## References

Sources: the paper named in the scope line above (PDF sha256 `e194637805ec7f87c277f90cd1698d6f4235a3fe12942d2e2ec2ec659555c065`); the numbers recomputed in the scripts are transcribed from its tables.

## Revision log

- *2026-10-26, v1.* First public version, from the reader's working notes of 2026-10-25. Quotation marks were removed from, or corrected in, phrases that did not match the paper verbatim; cross-references to working notes and workflow remarks were not carried over.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
