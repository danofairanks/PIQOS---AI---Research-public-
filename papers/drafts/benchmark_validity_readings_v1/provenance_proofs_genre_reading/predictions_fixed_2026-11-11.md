# Predictions fixed before the sources were read (2026-11-11)

Written and committed in the reader's working notes before the fuller reads of the sources below; the earlier partial reads (the report's Sections 1, 5 to 7 and Appendix, and the abstracts and introductions of arXiv 2511.02620 and 2409.12055) are reused and not scored blind. The order is the evaluator's own record and is not independently timestamped.

**Question.** Do proofs and attestations of which process produced an output (the provenance genre) share the failure modes recorded in this series: headline compression, unmatched comparisons, comparator selection, conditions that cap the claim stated only in the body, no control case?

**Seed set.** (S1) a report on provable inference of a 400-billion-parameter language model; (S2) zkCNN (CCS 2021); (S3) zkLLM (CCS 2024); (S4) zkGPT (USENIX Security 2025); (S5) Artemis (arXiv 2409.12055); (S6) arXiv 2511.02620 (statistical verification, a non-proof comparator); (S7) the C2PA specification (media provenance, non-ML). A source blocked by a challenge page is reported, not bypassed.

**Per-source extraction (fixed in advance).** (a) the exact statement proved; (b) headline words in title and abstract and whether the statement supports them; (c) the performance claim: baseline, hardware, model size, matched conditions, number of runs, intervals; (d) limits stated in the abstract versus only in the body; (e) comparison to prior systems: head-to-head, one sentence, or none; (f) whether the same group builds and benchmarks; (g) a control case where the proven process is wrong or harmful, and what the proof then does.

**Predictions (probability each holds across the seed set as read).**
- G1 (0.80) In most sources the proved statement is process identity and the title or abstract carries a larger word (trustworthy, accountable, secure) that the statement does not support.
- G2 (0.75) Performance comparisons to prior systems are mostly unmatched (model, hardware, quantisation, batch); head-to-head tables are the minority.
- G3 (0.70) Overhead is reported against a baseline the authors chose, in a single configuration, without intervals.
- G4 (0.65) Conditions that cap the claim appear in the body but not the abstract in at least half the sources.
- G5 (0.85) No source supplies a control case where the proven process is wrong or harmful.
- G6 (0.55) At least one source states the post-hoc limitation (detects, does not prevent) explicitly.
- G7 (0.60) The evaluator is inside the builders' loop in nearly all sources.

**Decision rule.** Read each source's abstract, statement or definition section, evaluation and limitations; record (a) to (g) with evidence tiers; findings are pattern instances per source, each quoted or recomputed from printed numbers; if G5 holds, the genre is untested on the control and the open question stays open.
