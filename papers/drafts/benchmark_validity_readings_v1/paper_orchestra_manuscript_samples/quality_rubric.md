# Quality rubric for the four gallery manuscripts (fixed 2026-11-14 before the scorecard cells were filled)
Not a blind test: the reader had already gone through the manuscripts. What is fixed here is the rule for turning evidence into a score, so cells are not tuned afterwards. One rater; evidence tiers as in the README. Not an LLM-judge score, not a reviewer recommendation, and not a verdict on the science of the source papers.

## Axis 1: abstract claim vs the manuscript's own evidence (per abstract claim)
Claims are the abstract's checkable assertions; rhetorical phrases ("new paradigm", "foundation model", "highly effective") are listed separately as R and not scored as evidence.
- S supported: the manuscript's own body or tables show it as stated.
- P partial: shown, but scope, condition or comparison is dropped or weaker than stated.
- C contradicted: the manuscript's own text or tables, or its own references, contradict it.
- U unsupported: nothing in the manuscript shows it.
Score = (S + 0.5 P) / (S + P + C + U), reported with the raw counts.
## Axis 2: internal consistency (count of defects found between title, abstract, method text and tables)
## Axis 3: fidelity of numbers to the inputs (share of decimal tokens found in the source text; E1)
## Axis 4: citations: existence (share of checked arXiv ids that resolve with matching title) and relevance defects found (count)
## Axis 5: novelty-claim integrity: does the manuscript claim "first" while its own references or text contain the same work (yes / no / listed-only)
## Axis 6: disclosure and limits inside the manuscript: limitations section (y/n), AI-generation disclosure (y/n)
## Axis 7: run-to-run stability (pairs only): abstract claims on which the two runs agree in strength; method description agreement; theorem or constant present in only one.
## Reading rule
No single total is reported across axes. A manuscript is not "good" or "bad" here; the scorecard shows where its text can and cannot be relied on.
