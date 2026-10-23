# Reading a Record-Setting Research Agent Against Its Own Tables: Épi, Its Released Certificates, and One Table That Does Not Reconcile

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

## 1. The question

A technical report ("Épi: Towards a Persistent, Self-Improving Agent for Autonomous Research", arXiv:2610.24944v1, 18 October 2026, 23 pages, from Bake AI and collaborators at other institutions) describes an agent that runs investigations across model sessions, with persistent history, hierarchical memory, branching and independent review, and a fixed verifier that checks outputs. The abstract reports "120 record-setting results", an "approximately 84-fold narrower interval for the n-queens constant", a "computer-assisted proof of Tuza's conjecture" for a restricted family of split graphs, and a configuration, Épi-turbo, that "achieves a 5.4% higher total benchmark score than Codex at 64% of its model cost". A results repository (`github.com/BakeLab/Epi-results`, commit 97fa6a4) releases the constructions and certificates. This draft asks which of these claims can be re-derived from released artifacts, what the headline counts consist of, and where the report's own tables disagree with each other.

## 2. What was read, and how

- **The paper**, v1 only: the main text and the appendix passages cited below; figures through their text layer. The proofs and witnesses for the 20 numerical bound records were not re-derived except where named under E1.
- **Predictions** were fixed on 2026-10-21 after the title page, abstract and introduction, before the rest was read (`predictions_fixed_2026-10-21.md`). The date is the evaluator's own record, not independently timestamped.
- **Re-verification on 2026-10-23.** Every quoted string and printed count was checked verbatim against the arXiv v1 PDF (sha256 `0ddaa6e7…480b`) by `paper_checks.py`: 33 of 33 present. The repository's `data/records.json`, Tuza certificate and Ramsey construction were fetched as single files at commit 97fa6a4 (still the repository's HEAD today) and re-checked; those checks are **E1 today**. The packing, pentagon and octagon checks were executed on 2026-10-21 against a read-only checkout and are **not repeated** here; their scripts and outputs are in `geometry_2026-10-21/`.
- Evidence classes: **E1** executed or recomputed here; **E2** read; **E3** interpretation. One reader, an AI system; the agent under study runs on OpenAI models ("GPT-5.6 Sol and GPT-6-Astra"), the reader on another lab's.
- The authors are called "the authors". No intent is attributed. The paper was supplied by an operator, not sampled, so nothing here is a rate.

## 3. What holds

- **The released numbers are what the files say (E1).** Of 100 construction records, the 87 circle and ball packings recompute from the released coordinates to the claimed radius within 5.6e-17 and each exceeds its registry reference by 1.5e-6 to 2.8e-4 relative (outputs of 2026-10-21; Packomania container conventions assumed). The nine pentagon records match their claimed enclosing-triangle side within 7.1e-15. The Ramsey-multiplicity construction (a 1,024-vertex graph) evaluates, with my own graph decoder and clique counter, to exactly 4427841832181/2^49 as claimed (rational equality), and the exact match also confirms the loop convention (without loops the value would be 0.0074735). The Tuza certificate passes the repository's checker (872 classified profiles, 560 certified, 18,444 boxes), and an independent re-implementation agrees on all 18,444 boxes.
- **The checker is not vacuous (E1).** Six mutations of the certificate (drop a cover edge, duplicate a packing triangle, drop a box, flip a mask bit, drop a profile, shrink a packing) are each rejected by the repository's checker.
- **The paper's arithmetic (E1).** The Spencer matrix read from the paper's text layer has discrepancy exactly 5 over all 256 sign vectors (224 of 256 vectors give 5, 32 give 7); the Cohn–Elkies separations recompute to 0.352% and 1.918% (printed: 0.35% and 1.92%); the interval ratios are 83.8 and 3.66 million (printed: about 84 and more than 3.6 million); the Tuza profile count is 872 with 35 nested, as printed; in Table 3 the total gap 2.75 equals gains minus losses (4.54 − 1.79).
- **Candour in the body.** The counting rule, the single run per task, the weak solver references, the 1% speed band and the instance-level direct comparison are all stated in the paper.

## 4. Predictions scored

Seven predictions: **6 held (one with a sub-part missed), 1 partial.**

| Prediction | Result |
|---|---|
| A closed, deterministic verifier; no measured attempt to bypass it | **Held (E2).** "A fixed verifier evaluates their outputs"; reward hacking is cited as motivation; no adversarial test is reported (search: bypass, adversarial, exploit). |
| The "120" counts instances or settings inside fewer families, with small margins | **Held, with a correction.** The counting rule is stated openly (section 6, item 1); the margins are small (section 5). |
| Validity depends on a community registry reference that may lag | **Held (E2).** Comparisons use references "available as of September 16, 2026"; "some evolving registries already list the new results". |
| Tuza result restricted and computer-assisted; full proof not in the paper | **Held, with a correction.** The restriction is in the abstract. The paper does give the argument (Appendix A.13) and cites two external results for parts of it (section 6, item 6). |
| Épi-turbo vs Codex rests on a single run, with no interval | **Held, one sub-part missed.** "We did one run for each task and system, so we do not report statistical significance." I expected baseline parity to be unstated; the paper states the same model and reasoning effort (prompt parity is still unstated). |
| "Self-improving" means memory and methods with no controlled ablation | **Held (E2).** "We keep model weights fixed in the campaigns reported here." The words "ablation" and "Limitations" do not occur. |
| Independent review is by a same-family model, with limited human review | **Partial.** The paper uses "a different model" for review and "record[s] the reviewer's identity" (not printed in the text I searched). No human review of results is reported at all (search: human review, human expert, domain expert). Review was off in the Épi-turbo runs. |

## 5. Executed checks (E1)

1. **Margins over the earlier values (`records_checks.py`).** `data/records.json` holds the 100 construction records. Relative gain over each record's earlier comparison value: minimum 1.5e-6, median 2.1e-5 (0.002%), 99 of 100 at or below 0.1%, maximum 0.19%. For the 89 records with status `improves_registry` the maximum is 2.8e-4 (0.028%).
2. **Two statuses under one headline.** The 100 records are 89 `improves_registry` and 11 `listed_record`. The paper says why: "Some evolving registries already list the new results. Our tables retain the earlier values used for comparison." For those 11 (the nine pentagon packings, the autocorrelation record and the vehicle-routing record), an outside reader can verify that the result beats the archived reference but not that it beats the current registry.
3. **Table 3 does not reconcile (`paper_checks.py`).** For Codex, mean quality (1.032) plus mean speed (0.675) is 1.707, and the total 51.21 over 30 tasks is 1.707: the terms add up. For Épi-turbo, 1.030 + 0.784 = 1.814, while 53.96 over 30 tasks is 1.799. The difference is 0.46 points on the total. Each printed mean carries at most ±0.0005, so rounding can explain at most ±0.03. The gap between the two totals (2.75) is consistent with the per-task gains and losses (4.54 − 1.79), so the mean terms, not the totals, are the inconsistent numbers. The report does not describe a term or a rule (for example, for the one infeasible solution) that would account for it. This is a flag, not a verdict.
4. **Pentagon overlaps (2026-10-21 output).** Five of the nine pentagon records overlap pairwise by about 5.1e-13, inside the verification field's stated "tolerance 1e-12" but not strictly feasible. The overlaps do not change any comparison with the earlier listing: the pentagon gains are 2e-4 to 2e-3 relative, about ten orders of magnitude above the overlaps.
5. **Octagon (2026-10-21 output).** The claimed radius 0.14729738… is reproduced only if the octagon's flats lie on the axes; with vertices on the axes the clearance is 0.0833. The orientation is inferred from which one fits, not stated in the repository.

## 6. Findings (E2/E3)

1. **What "120 record-setting results" counts.** One result per "distinct instance or parameter setting"; "multiple parameter settings within a family count separately". The 100 construction records are 97 geometric packings in five categories (46 circular-quadrant, 36 four-dimensional-ball, 9 pentagon, 5 semicircle, 1 octagon) plus 3 others. The 20 numerical records include 4 Cohn–Elkies dimensions (9, 10, 11, 13), 5 Bₕ[g] coefficients and 2 quantum-noise channels, 11 of the 20 in three families. The report counts 21 families in all, and the count is disclosed, so this is a statement about what the headline number measures, not a concealment: 120 is not 120 independent results, and the abstract's single figure does not say so.
2. **The margins are small and relative to a snapshot.** Median improvement 0.002%; every comparison is against a reference "as of September 16, 2026". The impressive numbers (the 84-fold and 3.6-million-fold interval reductions; the non-sharpness of the Cohn–Elkies bound in dimensions 10 and 11) are in the bound records and are exact-arithmetic claims that the report supports with released witnesses I did not re-derive.
3. **Épi-turbo versus Codex.** Thirty tasks chosen "in the official hardness order" excluding those with "unreliable reference values"; one run per task and system; a $20 budget per task; scores on four held-out instances per task. The 5.4% total is mainly the speed term: the report says "the higher score comes mainly from the speed term", and the mean quality terms are 1.030 and 1.032. Épi-turbo has the higher score on 18 tasks and Codex on 12, and the report adds that "on 10 of these tasks, the difference is less than 0.01". On the direct instance comparison (objective values only), Épi-turbo is better on 18 instances and Codex on 61 (40 ties among 119 comparable), and Épi-turbo is more than 1% worse on 29 instances against 10, with 1 infeasible solution against 0. The report says the commercial-solver references are sometimes weak, which is why it adds the direct comparison. The reader should hold the 5.4% and the instance counts together; the report prints both. Review and extra validation were off in these runs.
4. **"Self-improving" is accumulated memory and methods.** Weights are fixed; no ablation isolates the contribution of memory or experience, and the word "Limitations" does not occur. The record-setting results show the system plus its model produced verified artifacts; they do not show that the accumulation, rather than the model's capability or the compute budget ("a few days", per-problem budgets), produced them.
5. **The gate is closed and untested.** The verifier is separate from the agent and fixed; improvement is accepted only past a pre-fixed gain floor (the report defines δ and says it is fixed before the investigation). Nothing in the report tests whether the agent could influence the verifier's inputs. The review model's identity is recorded but not printed in the text searched.
6. **The Tuza argument has external dependencies.** Appendix A.13 gives the structure: 872 profiles; 35 nested (a cited threshold-graph theorem); 277 satisfying a maximum-cut criterion from the cited preprint; 560 covered by exact certificates (18,444 integer boxes); and a multiplicity-truncation step, attributed to the same preprint, that extends the finite checks to arbitrary multiplicities. The repository's `PROOF.md` also argues the truncation step analytically. The finite certificate is machine-checked (section 3); the truncation argument and the two cited results are not.

## 7. What this does and does not establish

- It does not show any record is wrong; where an artifact could be executed it reproduced exactly.
- It does not test the registry-novelty claim, the attribution to the agent rather than its model and harness, or the Épi-turbo benchmark (the results repository's README does not mention Épi-turbo, FrontierOR or Codex; the repository's other contents were not listed).
- It shows what the headline numbers measure: instances and settings, small margins over snapshot references, a total score driven by a speed term, and one table whose terms do not add up.
- Limits: one reader; the packing, pentagon and octagon checks were not repeated for this draft; 13 of 100 construction records and all 20 numerical bound records were not independently re-derived (vehicle routing and the Zhang–Zagier construction need an external instance or an interval-arithmetic certificate; the numerical-bound witnesses are large and formulation-specific); v1 only; the repository's integrity checksums and the autocorrelation record were checked in private notes without stored output and are therefore not claimed here.

## 8. What would change this

A per-task score table for Épi-turbo (or the authors' account of the 0.46-point difference); the review model's identity; an ablation with memory removed under the same budget; a statement of how the verifier's inputs are isolated from the agent; second and third runs of the Épi-turbo tasks; machine-checking of the truncation lemma.

## 9. Reproduction

Everything is in `epi_reading_v1/`: `predictions_fixed_2026-10-21.md`; `paper_checks.py` and output (needs the arXiv v1 PDF and `pdftotext`; the PDF is not stored here); `records_checks.py`, `ramsey_check.py` (with `cliq.c`; needs gcc) and `tuza_checks.py`, each with its output, which fetch or take single files from the pinned commit of the results repository; `geometry_2026-10-21/` (scripts take a checkout path; outputs are from 2026-10-21). All scripts are standard library except the geometry scripts (numpy) and the Tuza checker (numpy, from the repository).

## References

Sources: the report arXiv:2610.24944v1 ("Épi: Towards a Persistent, Self-Improving Agent for Autonomous Research", dated 18 October 2026) and the repository `github.com/BakeLab/Epi-results` at commit 97fa6a4 (`data/records.json`, `mathematics/tuza/` including `PROOF.md`, `verify.py` and `certificate.json.gz`, `mathematics/ramsey-c45/construction.graph6`, and the construction files read on 2026-10-21). Counts and table values were transcribed by hand from the PDF and recomputed in `paper_checks.py`.

## Revision log

- *2026-10-23, v1.* First version.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
