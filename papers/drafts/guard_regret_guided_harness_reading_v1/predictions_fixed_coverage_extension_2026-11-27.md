# Predictions fixed before the coverage extension: arXiv 2611.23476v1 (GUARD)

*AI-assisted. Written before the extended read (the per-benchmark tables beyond Table 2, the ablations, the remaining appendices) and before searching the text for a code or data statement. Already read before this: the abstract, introduction, formulation summary, Section 4.1, the algorithm and theorem statements, Table 2, the conclusion and its summary table, the appendix proofs and the cost accounting. The order is the evaluator's own record and is not independently timestamped.*

| # | Prediction | Confidence |
|---|---|---|
| E1 | A code or data availability statement exists (a link or a promise of release) | 0.45 |
| E2 | At least one results table beyond Table 2 reports a spread (standard deviation, interval or several seeds) for a headline cell | 0.50 |
| E3 | The ablations show that removing a component (Analyze, Propose or Gate) lowers the headline metric on at least one benchmark, and at least one removal does not lower it | 0.70 |
| E4 | A measured adaptation-time cost (wall-clock, tokens or dollars) is reported in the appendices | 0.35 |
| E5 | How the "final" hosted configuration was chosen is stated | 0.40 |
| E6 | A caveat about shared reviewer-and-solver flaws, or about reference-free grading, appears in the appendices | 0.35 |
| E7 | At least one benchmark table shows the method not beating the best baseline on some metric or domain | 0.80 |

Decision rule fixed with them: scored after the relevant text is read; an absence is reported as "not found by search and reading of the named sections", not as absence from the paper.
