*Copied from the evaluator's working notes. Part 1 was written after seeing only the first three pages (title, abstract, introduction through contributions, Figure 1, Table 1, related work) and before the body; part 2 before Appendix A was opened. The order is the evaluator's own record (the repository history is not an independent timestamp).*

---

# Part 1: predictions fixed before reading the body (2026-11-10)
- P1 (0.80): the Index combines quantities of different kinds under authors' weights and the ranks are sensitive to them; no sensitivity analysis.
- P2 (0.75): the Lite-versus-Full agreement (rho 0.93; 26 of 28 pairs) is weak evidence for Lite as a proxy (Lite is a subset of Full; n = 8; top positions differ).
- P3 (0.70): Opus 5.5 appears only on Lite; its Lite lead over the Full leader's agent is one task.
- P4 (0.70): essentially no open conjecture is resolved; "progress" is special cases and bounds.
- P5 (0.65): contamination is not controlled.
- P6 (0.65): task selection and the significance review are by the authors; no independent panel or agreement figure.
- P7 (0.60): constructions and solver tasks are scored against author-chosen references; one construction beating a reference is an anecdote.
- P8 (0.60): the "same per-attempt budget" does not equalise harnesses, tools or token use.
- P9 (0.55): no confidence intervals, few attempts, ties untreated.
- P10 (0.50): the authors' affiliated model is evaluated by the authors with brief disclosure.
- P11 (0.50): Lean statements may misformalise results and the rate is not quantified.
- P12 (0.45): rank claims at the top of Full and Lite are within a few points of other agents'.

# Scored after reading the body (not part of the preregistration)
All twelve held, four in part (P5 contamination is partly controlled for solver tasks by hidden instances and transformations; P7 the improvements are specific and source-checked; P10 mitigations present; P11 statement-fidelity checks exist but no mis-formalisation count in the text read).

# Part 2: predictions for Appendix A (fixed before opening it)
- A1 (0.80): most theorem sources are 2023-2025. A2 (0.75): no model training cutoffs are stated. A3 (0.70): several construction and solver tasks use long-public instances or records. A4 (0.60): some theorem sources are from 2026. A5 (0.55): the conjecture tasks include problems whose solutions appeared after the task was formulated.
Scored after reading: A1 held (14 of 20 from 2023-2025); A2 held; A3 held; A4 held (six 2026 sources, five 2025); A5 held in part (the two retrieved OpenAI resolutions; no dated check for the others in the text read).
- `checks.py` and `checks_appendixA.py` were written after reading; they are not preregistered. They use numbers typed from the paper's tables.
