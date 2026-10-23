# PREREG: evaluation of arXiv 2610.23839v2 "DiscoveryRSI: Recursively Learning to Discover Valuable Hypotheses" (20 Oct 2026, 40 pp.)
Written 2026-10-21 after reading only the title page, Figure 1 and the abstract; BEFORE reading the methods, results or appendices. Evidence classes E1 executed / E2 read / E3 interpretation. AI-assisted evaluation. Not the Chlon-Huang paper (that pre-draft stays open).
Predictions about the paper:
- P1. The headline quality score (4.86 to 5.39) is produced by automated (model-based) judges using a rubric that overlaps the signal used for training ("hypothesis credit optimization" uses assessments).
- P2. The 6.3% vs 2.5% / 2.3% "correspondence with post-cutoff publications" rests on small counts and has no confidence interval or significance test in the main text.
- P3. The human evaluation is small (a few dozen to a few hundred items, few raters) and labelled preliminary.
- P4. Compared models have different training cutoffs and the "post-cutoff" window is not equalised per model.
- P5. "Recursive self-improvement" is two rounds of bounded change (fine-tuning plus harness edits accepted on a dev set), not open-ended RSI.
- P6. Dev/test separation is stated but the re-discovery step draws on the same task distribution as the training episodes.
- P7. Code and models are linked; no independent replication; main results are single runs without seed variance.
What would change these: any prediction missed is recorded as missed in the evaluation, not edited here.
