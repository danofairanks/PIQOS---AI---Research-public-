*Copied from the evaluator's working note. Written after seeing only the abstract and the first two pages of the introduction (through Table 1) and before reading the rest; that order is the evaluator's own record (the repository history is not an independent timestamp).*

---

# Predictions fixed before reading the body (2026-11-09)
- P1 (0.8): the "34% improvement" is a gain in recall on a small benchmark; precision or false-positive rate is not reported with it, or only weakly; no intervals (0.7).
- P2 (0.65): PAT's design choices (prompts, number of samples, aggregation) were developed on SPOT or similar data used for the headline, without a held-out split.
- P3 (0.6): the zero-shot baseline is a single call to the same underlying model; no compute-matched baseline (majority vote or best-of-N at the same budget), so the gain confounds method with compute.
- P4 (0.75): the pilot outcomes are author-reported (surveys, anecdotes) from opt-in participants; no control group; no expert adjudication of flagged errors or false alarms.
- P5 (0.55): the 2026 NeurIPS count in Table 1 is an estimate and the AI-attribution claims are hedged; the combined figure rests on that estimate.
- P6 (0.6): the four-level taxonomy is conceptual with qualitative trade-offs and no empirical test.
- P7 (0.65): examples of "critical errors" are anecdotal; hallucinated flaws are acknowledged but not quantified from the pilots.
- P8 (0.7): evaluation is entirely by the tool's builders on the builders' model family; no independent evaluation.
- P9 (0.5): the tool, prompts and pilot data are not released.
- P10 (0.55): "referee control preserved" is a design stance; automation bias and anchoring of referees on tool output are not measured.
- P11 (0.5): authors gaming the tool, prompt injection in manuscripts and confidentiality of submitted manuscripts are discussed only briefly or not at all.
- P12 (0.5): contamination of benchmark papers is acknowledged.
- P13 (0.45): a non-Google model is mentioned (as baseline or judge).

# Scored after reading (added later; not part of the preregistration)
P1 met (recall only on 29 errors; the gain is 34.5 points). P2 partial (not stated either way). P3 met (single call only, although the text argues Pass@k). P4 met (opt-in surveys; no response rate). P5 met. P6 met. P7 met. P8 met. P9 met (no code, prompt or data statement). P10 met. P11 partial (gaming gets one clause; injection and confidentiality none). P12 missed (contamination is not mentioned). P13 missed (only Gemini-family systems appear). 9 held, 2 partial, 2 missed.
- `checks.py` was written after reading the paper; it is not preregistered. It uses numbers typed from the paper's tables and text.
