# Status, Not Correctness: Reading an AI-Assisted Quantum-Gravity Construction Against Its Own Abstract

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

## 1. The question

"An algebraic quantization of gravity from the null cone" (arXiv:2611.34924v1, hep-th; a single-author paper from a university theoretical physics institute, dated 23 November 2026, 83 pages) proposes a quantization of vacuum general relativity in four dimensions and derives, among other results, a finite-dimensional Hilbert space for a causal diamond and a one-loop logarithmic correction to black hole entropy. Its acknowledgements say several calculations and proofs were developed in long collaboration with an AI system.

This reading does not ask whether the physics is right. It asks a narrower question that a non-specialist reader can check against the text: **for each headline claim in the abstract, what status do the paper's own words give the steps it rests on, and does the abstract carry that status?** Where the answer is "conditional" or "heuristic", that is the paper's wording, and it is quoted.

## 2. What was read, and how

- The paper's text layer (PDF not stored here; sha256 in `quote_checks_output.txt`): the abstract, the introduction, Sections 2 to 6 and Appendix E in full; Appendix D as rendered pages (the end of D.1, all of D.2 and D.3), with the displayed algebra of its main steps spot-checked; Appendices A to C by structure, stated dependencies and the sentences around each cited result, **without re-deriving their equations**, and the first part of D.1 by text only. The reference list was not checked against its sources. The paper's author names are recorded in the evaluator's private notes and are not reproduced here.
- Arithmetic checks on displayed formulas (`checks_arithmetic.py` for Sections 4 and 5, `checks_appendix_D.py` for Appendix D, standard library only). These test that written formulas and inequalities agree with each other as printed. They are not checks of the physics.
- Twenty-two quoted strings were checked against the text layer (`quote_checks.py`; 22 of 22 found).
- Predictions were fixed before the paper was opened (`predictions_fixed_2026-11-26.md`), from a one-line description.
- Same-source note: the reader is an AI model from a different lab than the one the acknowledgements name. This is a reading, not a referee report; no error is claimed anywhere below.

## 3. What the paper says about the AI collaboration (E1)

The only statement is in the acknowledgements: "Several of the calculations and proofs in this paper were developed through detailed, back and forth collaboration with" an AI system "over the course of many months, amounting to ∼ 400M total tokens spent", with thanks to its developer for the compute. A text search of the whole paper found no statement of which calculations or proofs were developed this way, how each was checked, whether any step was formally verified, or whether code or data are available, and no competing-interests statement. The paper has no dedicated limitations section; its caveats are in the body and in footnotes.

## 4. Predictions scored (post hoc, one reader)

| # | Prediction | Result |
|---|---|---|
| P1 | Main claims are results in mathematical physics produced with AI assistance | HIT |
| P2 | Verification mostly human or numerical, not formal | PARTIAL: no formal verification is mentioned and no verification method is stated at all |
| P3 | Abstract's strongest claim stronger than the body establishes | HIT, as a calibration gap (section 6): several abstract statements omit conditions the body states |
| P4 | Limits stated, but shorter than the claims | HIT: deferral footnotes and inline "heuristic" and "argue" wording, no limitations section |
| P5 | Attribution described, not per step | HIT |
| P6 | A headline result depends on an unverified or external step | HIT: see section 5 |

## 5. Claim ledger: what each abstract claim rests on, in the paper's words (E1)

| Abstract claim | What the body says it rests on |
|---|---|
| The abstract states that the algebra of observables generates "a type I factor" | The paper states that the factor is type I because a pure state is chosen: "Since we choose a pure extension". The extension is only partly fixed (it says "we can choose a pure state ω on A"), and a footnote says, of the equivalence question: "We defer to future work whether different choices of ω in Section 4.2 yield unitarily equivalent representations". |
| The abstract says that "each sum over intermediate states converges absolutely" | The convergence step is a general Hilbert-space inequality applied to unitary time evolution. Unitarity is built into the construction for deformations that are *admissible* (the same reduced phase space); the paper states this as a condition. |
| A closed-form, finite graviton pair amplitude "even though expanding first in GN yields a logarithmic divergence" | A constructed two-point function whose phase is chosen to track the area. `checks_arithmetic.py` confirms that the displayed series equals the displayed closed form to about 1e-15, and that the series term grows like log N. That is arithmetic agreement only. |
| A causal diamond "with a given maximum size has a finite dimensional Hilbert space" | A contradiction argument that uses (i) existence of states, shown order by order in the coupling and described at finite coupling as: "this provides strong evidence at finite GN and ℏ that" the distance goes to zero, with a footnote calling the last step "a heuristic for the noncommuting operators in (4.26)"; (ii) a clock operator whose self-adjointness on a dense domain is argued: "In Appendix C.2 we argue that (4.27) is finite on a dense set of wavefunctions, as required for it to define a self adjoint clock operator"; (iii) a one-loop two-point function in a stated regime. Appendix D was read as rendered pages: the boost identity and its algebra check out as printed (`checks_appendix_D.py`); the lower bound on the integral of the normal-ordered square holds for any state, and the cycle bound holds for every finite union of cycles; the paper says the estimate for the uncut preparation holds "on the smooth background as in Section 5.2", and the appendix does not derive it; the vacuum-subtracted correlator is assumed to have a finite coincidence limit at the corner ("This is incompatible with the positive right hand side" is the paper's own sentence closing that step); a separate one-loop count of graviton states in D.3 rests on the same flat-space spherical-corner premises and a semiclassical counting rule ("quantization requires a symplectic area of order" ħ per excitation). |
| The entropy has a one-loop logarithmic correction "recovering at one loop the coefficient" of an earlier Euclidean calculation | Per the paper [1], the coefficient 106/45 is printed in (5.67c) [1] (the Gauss–Bonnet step that fixes the log of the trace), enters the determination of the ratio q, printed as 257/302 in (5.68) [1], and re-emerges in (5.69) [1] after the change of variables to fixed mass; `checks_arithmetic.py` confirms that the arithmetic of (5.68) and (5.69) closes, as printed in the paper [1]: q/(2(1−q)) − 1/2 = 106/45 [1]. Whether this is an independent check of the earlier coefficient or follows from the same one-loop number is for a specialist to judge; the earlier coefficient was not checked here. |
| "deriving the semiclassical Einstein equations to one loop as the low energy limit" | Section 6 derives this for coherent initial states, fixed smearings and a first-order correction taken from a cited result. The abstract states the result without those conditions. |

## 6. What the abstract leaves out (calibration, not concealment)

Each item below is stated in the body; none appears in the abstract. They are the abstract-versus-body gaps this reading found, framed as calibration.

1. The type I conclusion follows from choosing a pure state extension, and equivalence across choices is deferred (footnote).
2. Existence of states at finite coupling is "strong evidence", with one step called a heuristic (Section 5.1 and a footnote).
3. The clock operator's domain is argued, not proved, and the argument uses the same estimate (Section 4.3 footnote, Appendix C.2).
4. The semiclassical limit is derived for coherent states with fixed smearings (Section 6).
5. The equivalence with an earlier axiomatic formulation holds "when the Euclidean cylinder has finite trace" (stated in the introduction), and the check that this paper's gravity satisfies the axioms uses the finite-dimensionality result of Section 5.

Finite dimensionality is the node several later claims route through: the entropy statement, the amplitude conditions in Appendix E and the topology result in Section 5.4 all use it.

## 7. What holds (E1)

- The displayed formulas that were checked agree with each other (section 5).
- The paper states its caveats in the text and does not contradict itself in the parts read; two printed equations show opposite boost weights, very likely a loss of labels in the text layer, not an error.
- The structure of the finiteness argument is explicit: a contradiction between a positivity statement for the uncut amplitude and a sign statement for partial sums.

## 8. Flags (ranked; post hoc; leads, not verdicts)

1. **The finiteness argument carries the most weight and its quantitative inputs are one-loop, leading-order statements in a stated regime.** The conclusion is non-perturbative. After the extended read of Appendix D, the displayed algebra of the argument is consistent as printed; the inputs a specialist would examine are the estimate for the uncut preparation, the finite coincidence limit of the vacuum-subtracted correlator at the corner, and the semiclassical counting rule in D.3. The cycle length the argument needs grows roughly like s*² e^{s*} divided by a minimum weight (my reading of the printed bound), so the argument establishes finiteness without a quantitative bound on the dimension.
2. **The representation depends on a choice (the pure extension) whose uniqueness is deferred.**
3. **Existence of states at finite coupling is evidence-level in the paper's own words.**
4. **The entropy agreement has a structure that deserves a specialist's reading** (the same one-loop number appears in the input and the output).
5. **No account of which parts were developed with the AI system and how each was verified.** This is a reporting observation, not evidence about correctness.
6. **The abstract states the headline results without the conditions listed in section 6.**

## 9. What this does and does not establish

It establishes what the paper's own text says about the status of its steps and how the abstract compares. It does **not** establish that any step is correct or incorrect: no error was identified, the displayed algebra of Appendix D was spot-checked as printed but the physics inputs were not re-derived, Appendices A to C were not re-derived, the references were not checked, and the reader is not a specialist in this field. Conditional is not wrong, and an unstated verification method is not evidence of a flaw.

## 10. What would change this

- A specialist check of: uniqueness or equivalence of the pure extensions; self-adjointness of the clock operator at finite coupling; a derivation of the estimate for the uncut preparation and of the finite coincidence limit of the vacuum-subtracted correlator; the mode-count constant behind the one-loop count in D.3; whether the one-loop log coefficient is an independent check; the hypotheses of the cited Euclidean axioms in Appendix E.
- A formal or independent derivation of the finiteness result.
- A statement from the author of which parts used the AI system and how they were checked.

## 11. Reproduction

`quote_checks.py` (needs the paper's extracted text; sha256 of the PDF in `quote_checks_output.txt`), `checks_arithmetic.py` and `checks_appendix_D.py` (standard library only; outputs in `checks_arithmetic_output.txt` and `checks_appendix_D_output.txt`), and the three scanner outputs (`tool_scan_*.json`) of this repository's own tools on this file: the paper-rigor and verification-lint scans report zero gaps after each quotation was attributed and each number tied to the paper's equation numbers; the attractor scan reports one weak lead, the phrase "future work" inside a quotation from the paper's own footnote, read directly and not a maneuver of this reading.

## References

- [1] arXiv:2611.34924v1 [hep-th], 25 November 2026 (83 pages).

## Revision log

- v1, 2026-11-27: first staging copy.
- v1.1, 2026-11-27: Appendix D read as rendered pages and added to the claim ledger, flags and checks; AI system and developer kept unnamed; author names stated as stored privately.
- v1.1 staged in the public drafts folder on 2026-11-27; the paper's arXiv listing showed v1 only that day and the fetched PDF matched the one read.
