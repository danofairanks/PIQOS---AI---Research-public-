# Reading a Context-versus-Weights Decision Rule Against Its Own Preconditions: One Paper, Its Repository, Three Toys

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

## 1. The question

A preprint ("When Thoughts Become Memory: Unifying In-Context Learning and Fine-Tuning", arXiv:2610.29419v1, 21 October 2026) and a public repository (`github.com/leochlon/bitsy`, commit cf81a50) offer a rule for deciding whether new data belong in a model's context or in its weights. The abstract says the authors are "the first to give a certified rule", that the value of data obeys "an exact law ... for any model, architecture, dataset and task", and that "every certificate the ceilings issue ... is correct". This note asks what each of those statements rests on, and which preconditions each needs. It does not ask whether the authors are right about the real-model results, which cannot be reproduced here.

## 2. What was read, and how

- The paper in full, appendices included, except proofs B.3 to B.9 (not checked line by line).
- The repository, at one commit; it has no tests and no licence file.
- Predictions and checks were fixed on 2026-10-20 from the abstract and the repository, before the paper existed (`predictions_fixed_2026-10-20.md`). The date is the evaluator's own record, not independently timestamped. The abstract and the first introduction paragraphs had been seen before scoring began; the abstract was already known when the predictions were written.
- Evidence classes: **E1** executed here; **E2** read; **E3** interpretation. One reader, AI-assisted; the toys were written by the same system that wrote the checks, so each tests whether a stated precondition matters, not whether the authors are wrong where it holds.
- The authors are called "the authors". No intent is attributed. The paper was supplied by an operator; it was not sampled, so nothing here is a rate.

## 3. What holds

- **The identity (E1).** The expected saving splits into bits stored, plus a prior repair, minus a decoding loss (their Theorem 2). The proof is three lines (a pointwise identity, then an expectation). On 2,000 random discrete distributions it holds to 2e-15; the corollaries I tested (a ceiling on the gain; a cap on what a fine-tune adds when the context fits the window) have no violations. It is an accounting identity: it cannot fail.
- **The certificate bound (E2).** It rests on data processing and on non-negativity of KL divergence, not on a new inequality; the paper says "by data processing".
- **The anytime-valid test (E2, E1).** It is a betting test, cited to existing work ("Theorem 8 is such a comparison"). The repository implements it as the paper defines it (two one-sided tests at level 0.025, threshold 40, bounded increments, mixing with 1% of the uniform law). On 10,000 simulated null streams per case the paper reports false-call rates of 2.87%, 3.25% and 3.31%; the Wilson upper bounds recompute (3.22, 3.62, 3.68).
- **Arithmetic (E1).** The paper's certificate table (36 of 96 issued, 86 checks, none disagree) is the repository's stored table and sums correctly. On GPT-2: 7 rows of 8,000 plus 5,948 gives the abstract's 61,948 correct calls; with 4 wrong and 2,048 undecided the total is 64,000 (32 comparisons of 2,000 streams); 96.8% decided. The tabulated means in Table 10 match the text.
- **Closed forms (E1).** I re-derived the linear-Gaussian model of Appendix A.10 from the printed formulas and simulated it. The adapter ceiling comes out at 13.9% of the cache ceiling (printed: 14%); the one-attention-layer excess risk agrees within about 1%; the Bayes-cache gain at d = 200, N = 400 averages 0.7783 bits over five runs against 0.7775 from the formula; the ordering of channels holds at all seven sizes tried. The mathematical glyphs in the text extraction were partly garbled, so the reading is stated in the script header.

## 4. Predictions scored

Ten predictions were fixed (nine items, with one split in two): **9 held, 1 partial, 0 missed.**

| Prediction | Result |
|---|---|
| The "exact law" is an expectation identity proved in a few lines | held |
| The certificate proof reduces to a data-processing inequality; no new one | held |
| The body states that certificates need the true answer law and designed data | held (sections 5.1, 6.1; there is no limitations section) |
| Related work cites prequential coding / MDL; and cites betting forecast comparison | held, held |
| "First" is scoped in the body more narrowly than in the abstract | **partial**: the introduction says "No previous work has made context and weights comparable this way or turned the comparison into a certified rule"; "this way" is a qualifier and the clause is repeated |
| The 3.3% null error is an observed rate over a stated number of null streams, below 5% | held: 3.31%, 10,000 simulated streams |
| All experiments are by the authors; no external replication | held |
| The paper's certificate table matches the repository's | held |
| The 0.91 AUROC comes from the model's own probability change; the 0.95 target is a default, not tuned | held |

## 5. Where the abstract compresses (definitions before equations)

The equations are defined before they are used. The abstract's words are not.

- **"certificate".** In the paper's Proposition 6 it is an inequality; operationally it is a call issued when the lower end of a 95% interval of a mean margin over 64 tasks is above zero (section 6.1). That is a per-test statistical call, and the paper reports no multiplicity correction across 96 tests. The repository's README reports a Bonferroni variant (z = 3.28: 32 issued, 71 checks, all agree).
- **"correct".** Not defined in the abstract. In the appendix it means agreement with the "measured winner" on the same tasks, itself a 95% interval test on the same data. No out-of-sample check is reported. Given the theorem and exact information terms, agreement is expected up to sampling noise, so the 86 of 86 checks test the preconditions, not the law (E3).
- **"exact".** Three senses: the law is an identity in expectation; "exact information terms" exist only for designed tasks where the true answer law is known; an "exact leave-one-out value" holds in expectation under the paper's Assumption 1, while a single deletion measurement is a sample.
- **Scope.** The abstract says the law holds for "any model, architecture, dataset and task". Assumption 1 (a clean memory) and the true law appear in sections 2 and 3, after the abstract.
- **"first".** Supported at the scope of the certificate on exact-information data. The anytime-valid test is an application of existing results (as the paper says). Neighbouring work on valuing demonstrations in context turned up in a search on 2026-10-20 (snippet level) and is not cited.
- **"recovers a published evidence adjudicator", AUROC 0.91.** It runs the authors' own earlier adjudicator unchanged. The number is the adjudicator's separation of supporting from insufficient evidence on a public benchmark (0.9126 and 0.9143 for two verifiers; 0.899 and 0.930 when refuting evidence is included). About half the scores sit at the adjudicator's clipping bound of 37.58 bits, with ties counted as half. It measures that tool; it is not an independent test of the law, which cannot fail. Three of the paper's 93 references are from the authors' group, with 11 in-text mentions.
- **Three abstract numbers (E1):** "a hundredfold" is 4.99 to 0.046 bits (108-fold); "nearly double" is 4.99 to 9.06 (1.82-fold); "one camera ... beats four" is 8.71 against 10.17 bits. All consistent with Table 8.

## 6. Three toys: which preconditions matter

Preregistered on 2026-10-22 before building (`toys_preregistration_2026-10-22.md`); numpy only; the betting-test toys call the repository's own function unchanged. **6 predictions held, 3 missed**; all three misses are magnitude misses in the direction of a smaller effect than I predicted.

- **CM1, an estimated answer law.** If the true law is replaced by an estimate from n samples (alphabet of 16, prompt short of the bound by 0.05 bit), the false-certificate rate is 0.7% with the exact law, 13.4% at n = 50, 1.4% at n = 500, 0.8% at n = 5,000. I had predicted at least 20% at n = 50 (missed) and at least 10% for a 0.10-bit shortfall (missed; 6.5%). The cause is that an estimated law's cross-entropy exceeds the true entropy, which inflates the bound.
- **CM2, order and drift.** A stream with overall mean zero but an early advantage and a later deficit is called in 100% of streams; the same values randomly reordered give 2.35%. The paper's guarantee is for queries drawn independently from the task; its 200 reorderings concern exchangeable cohorts. A stream favouring one channel by 0.1 bit with a deployment favouring the other is called for the stream's winner in 91.6% (predicted at least 95%; missed) and never for the other.
- **CM3, leakage.** If the answers to a fraction f of the held-out queries sit in one channel's context, the better channel's correct call drops from 100% to 53.5% at f = 3%, the call flips to the leaked channel between 6% and 8%, and it reaches 99.5% at 10%, with the nominal guarantee intact against its own null. The test cannot check independence of queries from context.

Not built: leakage in real models; manipulated evidence against the adjudicator; error control for repeated use as a decision gate (an inference of mine, E3: the paper's error control is per comparison).

## 7. What could not be done

- **The real-model experiments** (GPT-2, TabPFN against XGBoost, the occupancy and stereo networks, the kriging learner, the adjudicator) need models, datasets and APIs; they are not reproduced here. Only the stored certificate table is recomputable from the repository.
- **The supplementary scripts.** Appendix F describes a supplementary package of scripts and saved results. It could not be found: the repository is unchanged (one commit, no `scripts/` directory), the PDF has no code link or embedded files, none of the authors' public repositories is named for this paper, arXiv was unreachable from the evaluation environment, and a web search found nothing. Whoever wants to run the scripts needs to ask the authors for the package.

## 8. What this does and does not establish

- It does not show the authors' real-model results are wrong. Nothing in it tests them.
- It does not show that the mechanics are wrong: the identity, the bound, the test and the repository's implementation hold where their preconditions hold.
- It shows what the abstract's words depend on: exact information terms and designed tasks for "certificate" and "correct"; independence and exchangeable order for the test; the group's own adjudicator for the 0.91.
- The toys show that those preconditions are load-bearing, not that they fail in the authors' experiments.
- One reader; same-source toys; three predictions missed in magnitude; proofs B.3 to B.9 not checked; no limitations section in the paper, so the preconditions are in the body and the appendix and not in the abstract.

## 9. Reproduction

Everything is in `context_vs_weights_certificates_reading_v1/`: `predictions_fixed_2026-10-20.md`; `checks_paper.py` and its output; `closed_forms_check.py` and its output; `toys_preregistration_2026-10-22.md`, `toys.py` and its output. `toys.py` needs a checkout of the repository at commit cf81a50 (`BITSY_PATH=/path/to/bitsy python3 -I toys.py`). The paper is arXiv:2610.29419v1; its numbers were transcribed by hand from the PDF.

## References

Sources: the preprint arXiv:2610.29419v1 ("When Thoughts Become Memory: Unifying In-Context Learning and Fine-Tuning", dated 21 October 2026) and the repository `github.com/leochlon/bitsy` at commit cf81a50 (README, `examples/certificates.py`, `bitsy/core.py`, `bitsy/gate.py`, `bitsy/bakeoff.py`). The paper's numbers (its Tables 8, 10, 12, 13 and 14, Theorem 2, Proposition 6, Appendix A.10) were transcribed by hand from the PDF and are recomputed in `checks_paper.py` and `closed_forms_check.py`. Every statistic in sections 3 and 6 is either a printed value of the paper or an output of the scripts in `context_vs_weights_certificates_reading_v1/` (`checks_paper_output.txt`, `closed_forms_check_output.txt`, `toys_output.txt`).

## Revision log

- *2026-10-22, v1.* First version.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
