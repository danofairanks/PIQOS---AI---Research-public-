# Predictions fixed before the repository, the paper or any manuscript was read (2026-11-14)
Known beforehand: the repository URL and its owner's name; nothing about content, README, licence or samples. The order (predictions before reading) is the evaluator's own record and is not independently timestamped.

| # | Prediction | Prior | Outcome |
|---|---|---|---|
| P1 | A multi-agent pipeline that turns rough materials (idea, notes, results) into a full manuscript; a writing pipeline, not hypothesis generation | 0.6 | Held |
| P2 | The repository itself contains few sample outputs (fewer than 10) or none; samples may live in a linked paper or site | 0.6 | Held (none; one input example; four manuscripts on the project page) |
| P3 | Its own evaluation uses LLM judges or preference comparisons with models from one vendor writing and judging; no intervals on headline comparisons | 0.65 | Not examined (the paper's evaluation was not read in full) |
| P4 | It includes a citation-verification step | 0.5 | Held (title matching against a scholarly index, an abstract required, a date cutoff) |
| P5 | Adjacent to the public repository's tools only as a source of the kind of text they read; not adjacent in design | 0.8 | Held |
| P6 | Samples disclose AI authorship in some form, without describing the checking | 0.5 | Missed (no disclosure inside the manuscripts; the project page and paper carry it) |
| P7 | At least one sample has a citation that cannot be found at a primary source (spot check of up to 10 per sample) | 0.3 | Missed (0 of 24 not found; one found but irrelevant) |
| P8 | The public tools flag little and most flags dissolve on reading | 0.6 | Held |
Stack fixed at the same time: text extraction; paper_rigor, verification_lint, attractor_scan; quote check; numbers recomputed against the source papers; up to 10 citations per sample checked at their primary listing; the manuscripts' own disclosures against what the pipeline does.
