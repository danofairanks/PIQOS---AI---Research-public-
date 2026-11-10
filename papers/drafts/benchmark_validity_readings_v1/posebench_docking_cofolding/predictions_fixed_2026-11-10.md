*Copied from the evaluator's working notes. Part 1 was written after seeing only the title, affiliations, abstract and the first page of the introduction, before the body; part 2 was written after the body had been read and before the released data were opened. The order is the evaluator's own record (the repository history is not an independent timestamp).*

---

# Part 1: predictions fixed before reading the body (2026-11-10)
- P1 (0.80): training-data overlap between the co-folding models and the test sets is only partly controlled; "novel pose" claims rest on an author-defined similarity or time split.
- P2 (0.75): the conventional baseline is a single pipeline; "co-folding beats conventional" is a statement about one baseline.
- P3 (0.70): test sets are small; success rates have no confidence intervals or paired tests.
- P4 (0.65): the docking baselines' apo input is itself produced by one of the compared co-folding systems.
- P5 (0.60): the multi-ligand set is small and its construction is the authors'.
- P6 (0.60): the accuracy-versus-chemical-specificity claim depends on metrics defined or combined by the authors.
- P7 (0.55): the MSA-sensitivity claim rests on few conditions, applied unevenly, without repeats.
- P8 (0.55): numbers or the method list changed across versions.
- P9 (0.50): a physical-validity filter is applied in some tables and not others.
- P10 (0.50): compute or runtime comparisons are absent or limited.
- P11 (0.45): the authors' own methods are included or favoured.
- P12 (0.40): samples or seeds per method differ and are not matched.

# Scored after reading (not part of the preregistration)
P1 met (the overlap is disclosed; only the time-split PoseBusters subset is clean for two models). P2 met (one pipeline; the template-based baseline of earlier versions is absent in v7). P3 met in part (n = 85/122/130/13 stated; the plotted +/- is SD over three runs; no paired tests; stated sizes differ from scored sizes, see the README). P4 met (AlphaFold 3 predicts the apo input for every docking baseline). P5 met. P6 met (PLIF-WM is rescaled across the compared methods). P7 met in part (single-sequence ablation on three co-folding methods only). P8 met (title, baseline set and headline changed). P9 not met (the same checks are shown for every method). P10 not met (runtime and memory are reported in an appendix). P11 not met (no method by the authors is evaluated). P12 met in part (sample counts differ per method; selection is by each method's own confidence). 8 met (3 in part), 3 not met, 1 not applicable.

# Part 2: predictions for the direct test against the released data (fixed before opening the Zenodo record)
- R1 (0.70): the released per-complex results for Astex score 84 complexes, not 85.
- R2 (0.65): the number of scored complexes varies by method on PoseBusters and DockGen-E, with failures concentrated in some methods.
- R3 (0.60): printed percentages reproduce to rounding once the right denominator is used.
- R4 (0.55): a common denominator equal to the stated n changes at least one ordering among the top methods.
- R5 (0.50): the record has no plain per-complex success table, so a recount would need the authors' scoring code.
Scored after the recount: R1 met; R2 met in part (counts vary and are large for DiffDock-L, P2Rank-Vina and Boltz-1; AlphaFold 3 is complete; missing predictions are counted as failures, which was not predicted); R3 met (cRMSD and RMSD rows reproduce exactly; validity-gated rows exact for three methods on Astex, within about one point on DockGen-E when the identity checks are left out); R4 not met (all methods share the denominator, so no ordering changes); R5 not met (per-complex `bust_results.csv` files are released for every run).
- `checks.py` and the `released_data_check*.py` scripts were written after reading; they are not preregistered.
