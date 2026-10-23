# PREREG: evaluation of arXiv 2610.24944v1 "Epi: Towards a Persistent, Self-Improving Agent for Autonomous Research" (Technical Report, 18 Oct 2026, 23 pp.)
Written 2026-10-21 after reading the title page, abstract and introduction (pp.1-2); BEFORE reading the setting, method, results or appendices. Evidence classes E1 executed / E2 read / E3 interpretation. AI-assisted evaluation.
Predictions about the paper:
- P1. Outputs are checked by an exact, deterministic verifier (a closed gate); the paper reports no measured attempt by the agent to exploit or bypass the verifier, so "no bypass" is untested.
- P2. The "120 record-setting results" count instances or parameter settings inside a smaller number of families (100 constructions in 8 families, 20 bounds in 12), so the count overstates the number of independent results; many improvements are tiny margins over a reference.
- P3. Each record's validity depends on a "documented literature or registry reference", which is community-maintained and may lag; the paper does not independently re-establish that no better public result existed.
- P4. The Tuza result is for a restricted family (clique part of at most eight vertices, at most three neighbourhood types) and the proof is computer-assisted; the abstract states the restriction; the full proof is not in the paper.
- P5. The Epi-turbo vs Codex comparison (5.4% higher total score at 64% model cost on 30 tasks) rests on one configuration of the baseline and a single run or a few runs, with no confidence interval, and the aggregate score definition matters.
- P6. "Self-improving" here means accumulated memory and methods with frozen weights; the paper does not report a controlled ablation that isolates the effect of memory or experience on results.
- P7. "Independent review" is performed by model reviewers (same family or prompts), with human review limited to selected results.
What would change these: any miss is recorded as missed, not edited.
