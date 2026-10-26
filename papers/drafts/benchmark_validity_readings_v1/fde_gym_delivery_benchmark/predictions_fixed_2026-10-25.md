*Copied verbatim from the evaluator's working note below the rule. Written before the measurement it concerns; that order is the evaluator's own record (the repository history is not an independent timestamp). Dates in the original that read 2026-10-27 are 2026-10-26 in fact.*

---

# Preregistration — arithmetic checks on FDE-Gym's reported tables (2026-10-25)
Written before the script. Source: arXiv 2610.22350v1 (15 Oct 2026), Table 3 (13 configurations; S, U, C, resolved) and the Section 5.2 text. Table 3 was transcribed by me from the PDF page image (no text layer was used); transcription is checked against the paper's own printed S column. No model was run. Secondary analysis of reported numbers only.

C1 Identity: S = U - C within +/-0.011 for all 13 rows (the paper floors U_adj at -1 only in aggregation and averages per run, so small residuals are expected). [0.9]
C2 Contact-cost share of the L0->L1 drop (leading three, original 20 tasks): the text gives C rising from 0.07-0.10 (L0) to 0.18-0.24 (L1) and the mean drop as 0.28. Using range endpoints only, the cost-rise range divided by 0.28 spans roughly 0.39-0.50. Prediction: the whole range lies between 0.3 and 0.6. Per-model C at L0/L1 is not tabulated, so this is a bound, not an estimate. [0.9]
C3 Resolved threshold: with S >= 0.8 and S = U - C, a leading model with mean C 0.14-0.22 needs U >= 0.94-1.02 on a resolved task if its C is typical. Report the implied U threshold per leading model from Table 3 mean C. Prediction: all three exceed 0.90. [0.85]
C4 Rank separation: report which adjacent pairs among the 13 have overlapping 95% CIs in Table 3. Prediction: Opus/Sonnet, Astra/Sol, GLM/DeepSeek/Gemini overlap; Opus vs Astra does not. [0.85]
Post-hoc status: the reading flags in README.md (selection rate, cluster dependence, budget truncation, L0 scoring disclosure) were formed while reading and are not preregistered.
