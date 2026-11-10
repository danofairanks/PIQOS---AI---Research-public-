*Copied from the evaluator's working note. Written after seeing only the first three pages (title, abstract, introduction through the start of Section 2.1, Figure 1) and before the body; that order is the evaluator's own record (the repository history is not an independent timestamp).*

---

# Predictions fixed before reading the body (2026-11-10)
- P1 (0.85): the result's strength is bounded by the trusted specification and contracts: a nontrivial part of the executed behaviour (the cryptographic primitives and some other routines) is replaced by contracts, so the "unmodified implementation" claim is true of the code but not of the whole executed behaviour.
- P2 (0.75): validation that the specification is not vacuous or wrong rests on small evidence (two re-introduced bugs) plus review; no mutation testing and no counted list of what the specification does not cover.
- P3 (0.75): "AI makes formal verification practical" is evidenced by proof size, not by cost against a human baseline.
- P4 (0.70): scope excludes side channels and timing, concurrency, the operating system, randomness sources and hardware faults.
- P5 (0.65): the post-quantum claim is symbolic (idealised primitives); the computational proof covers classical attackers only.
- P6 (0.60): the machine-code semantics is trusted with limited validation evidence.
- P7 (0.60): the "first" claim is narrow and defined against prior work as abstract, modified or narrower.
- P8 (0.55): human effort is substantial but not quantified.
- P9 (0.50): the list of axioms and unchecked escape hatches is stated, with the compiler and the proof kernel trusted.
- P10 (0.50): the evaluation is by the framework's authors; no independent re-check on file.
- P11 (0.45): agent and compute usage is reported only in aggregate.
- P12 (0.40): disclosure or coordination with the protocol's maintainers is mentioned briefly or not at all.

# Scored after reading (added later; not part of the preregistration)
P1 met (39 hooked routines replaced by contracts; cryptographic primitives idealised). P2 not met (vacuity proofs, mutation testing, two re-introduced bugs proved to violate the theorem, catalogues of departures, maintainers' feedback). P3 met (effort in people and weeks; no compute, token or dollar totals; no baseline). P4 met. P5 met. P6 not met (lockstep testing against two independent oracles and an emulator). P7 met in part (carefully scoped; narrow). P8 met. P9 met in part (comparator, standard axioms only, `sorry` and `native_decide` rejected; the compiler is not trusted, better than predicted). P10 met (open-sourced for community review; no independent re-check on file). P11 met. P12 met (no disclosure statement; no new vulnerability claimed). 9 met (2 in part), 3 not met.
- `checks.py` was written after reading the paper; it is not preregistered. It uses numbers typed from the paper.
