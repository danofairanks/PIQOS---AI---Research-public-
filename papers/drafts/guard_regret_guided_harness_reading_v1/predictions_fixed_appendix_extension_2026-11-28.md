# Predictions fixed before the v1.1 appendix extension: arXiv 2611.23476v1 (GUARD)

*AI-assisted. Written 2026-11-28 before reading Tables C.4 to C.8, Boxes B.1 to B.4 and the figure captions, and before any search of the text for link annotations, cost, limitation, selection or seed language. Before writing this I had seen only matching lines from a text search (mentions of Table C.4 "3 ties", the ablation tables, the prompt-box line and a plan-to-release sentence), not table rows.*

The absence statements in v1 under test: A1 no measured adaptation-time total; A2 one seed for the continual-stream headline; A3 how the reported hosted configuration was chosen is not described; A4 no shared reviewer-and-solver discussion; A5 no code or data link.

| # | Prediction | Confidence | Result (scored after reading) |
|---|---|---|---|
| F1 | At least one cell in Tables C.4 to C.8 where the method ties or loses to a prior method or to the unchanged initial harness | 0.85 | HIT: several (section 5.7, 5.8) |
| F2 | At least one of Tables C.4 to C.8 reports a spread (SD, interval or seeds) for a cell of the method | 0.45 | MISS: C.8 reports p-values and three replicates, no SD or interval for the method's cell; spreads sit in the professional-suite appendix |
| F3 | No table in C.4 to C.8 or the boxes reports an adaptation-phase cost (wall-clock, tokens, dollars) | 0.65 | HIT: asymptotic count plus a measured test-time wall-clock only |
| F4 | The prompt boxes contain no statement on shared flaws between reviewer and solver | 0.80 | HIT; the word "limitation" does not occur in the text layer |
| F5 | No URL to code or data in the text layer, footnotes or reference list | 0.85 | HIT: the only PDF link annotation is the arXiv abstract page |
| F6 | A paragraph describing how the final hosted configuration was chosen exists | 0.25 | MISS: components that changed between the initial and final runs are named; the selection is not described |

Decision rule: an absence is reported as "not found by full-text search of the text layer and the PDF link annotations", not as absence from the paper. v1 statements are edited only if a hit contradicts them; none was contradicted. Four of six predictions hit.
