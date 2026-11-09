*Copied from the evaluator's working note. Written after seeing only the first two pages (title, abstract, Figure 1, introduction, contributions) and before reading the rest; that order is the evaluator's own record (the repository history is not an independent timestamp).*

---

# Predictions fixed before reading the body (2026-11-09)
- P1 (0.80): the gap to the strongest baseline sits mostly inside the interval overlap once task-level variance is counted; no paired per-task test of the method against the baseline.
- P2 (0.75): the intervals resample runs with tasks held fixed, so they understate uncertainty across tasks.
- P3 (0.65): the mean speedup is carried by a few tasks; a median or per-task win rate would be weaker than the headline.
- P4 (0.70): baselines were implemented and tuned by the authors with less effort than the method; the offline baseline losing to the frozen harness reflects the adaptation more than the approach.
- P5 (0.60): "matched test-time budgets" matches wall-clock but not model cost; the cost-efficiency claim holds only for some metrics or curve regions.
- P6 (0.65): correctness is checked by the authors' own tests; no independent check of timing noise.
- P7 (0.55): one agent model; no results across models.
- P8 (0.55): the metric is best-so-far speedup (a running maximum over noisy timings), which favours methods that submit more candidates; no noise-corrected re-measurement.
- P9 (0.50): the ablation does not rule out that gains come from extra review compute rather than recursion; recursion itself is not shown on many tasks.
- P10 (0.45): at least one failure mode (broken revisions, drift, harness bloat) is reported with counts.
- P11 (0.40): safety of a self-modifying harness is treated briefly.
- P12 (0.50): contamination of tasks drawn from public repositories is addressed weakly or not at all.

# Scored after reading (added later; not part of the preregistration)
P1 met in part (no paired test; run-level bands only; the overlap itself could not be read to that precision, E3). P2 met (bands resample 3 runs per task over the fixed 50 tasks). P3 met in part (heavy-tailed per-task endpoints in the plots, a harmonic mean chosen against that; best-or-tied on about 24 of 50 panels by eye, E3). P4 met (both baselines are the authors' adaptations; the offline baseline is trained on 45-minute runs and tested at 4 h, and one traced failure comes from a path assumption). P5 partly met (wall-clock matched, cost not; the per-dollar column reverses with the metric). P6 met in part (authors' tests with held-out cases and a red-team pass; timing variation reported but not corrected in the score). P7 met (one model). P8 met (running maximum; no re-measurement; no per-method submission counts). P9 met. P10 partly met (categories and case studies, no counts of failed activations or rollbacks). P11 met. P12 met (the word does not occur). 10 held, 2 partly met, 0 missed.
- `checks.py` was written after reading the paper; it is not preregistered. It uses numbers typed from the paper's tables and text.
