# A Follow-Up Check of Škrinjar's *The Descendant Standing Problem* (v1.2): Theorem 1 Executed, Definitions Pinned

*Companion note to [`countermodel_analysis_v1.md`](countermodel_analysis_v1.md) (SSA R5.3.8). Draft; may change or be withdrawn without notice.*

## Abstract

Sandra Škrinjar's "The Descendant Standing Problem: Governing Learned Policies After Retrospective Warrant Failure" (v1.2, 13 October 2026, 36 pages; [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7610441)) is the first document in this author's line that the earlier countermodel analysis could not fault for the same reasons. It cites 31 outside works, repeatedly disclaims novelty for its machinery, and states its scope as the descendant's *currently asserted governing basis*. It contains no executed component, so we executed one: we implemented the paper's finite support calculus and ran Theorem 1 on 400,000 random finite worlds per reading. All nine preregistered predictions held; Theorem 1 produced no counterexample in either direction on worlds satisfying its premises. We then pinned the load-bearing terms in the paper's own words and re-ran the check under five alternative readings of the ambiguous ones. The theorem holds under all of them, but which premises do work depends on the reading, and under the strongest combined reading the theorem is close to definitional. We also found one gap in Definition 15 (gate-support independence) and note what Theorem 1 does not cover. Nothing here binds the framework to a real lineage; neither does the paper, and it says so.

All checks are small, synthetic and run by one model that also formalized the definitions (same-source caveat, §7). Scripts, preregistrations and raw outputs are in [`descendant_standing_v1_2_checks/`](descendant_standing_v1_2_checks/).

---

## 1. What changed relative to the R5.3.8 analysis

Credit first, because it is earned.

- **External literature and sized claims.** 31 references (truth maintenance, ATMS, belief revision, provenance, machine unlearning, selective labels, legal derivative-evidence doctrine) and an explicit disclaimer: "The paper does not claim novelty for truth maintenance, Horn closure, provenance, machine unlearning, recursive taint, independent-source reasoning, or policy-feedback effects." (p.1). Self-citation of the eleven R5.3.8 Appendix B titles: 0. The earlier findings "no external references" and "kernel is self-cited" do not apply to this document.
- **The regress is terminated openly.** Independence is operationalized as clean re-derivation against a confirmed defect set Δ. Δ, the review operator Ω and the criterion κ are declared "externally supplied" (p.30). This is the earlier "independently established is stipulated" finding partly answered: the stipulation is now named as an input, not hidden in the definitions.
- **A sharp separation.** "DETERMINATION CORRECTED ≠ LEARNED EFFECT REMOVED" (p.4) and the question "Does the descendant have a current governing basis that can stand without the defective ancestor's warrant?" (p.5) are stated in prose before the formalism.

Unchanged from the earlier analysis:

- The paper's synthetic cases (Table 1, Cases A–D) are labelled "Formally evaluated synthetic constructions" (p.27) and are evaluated by hand from leaf labels the author sets. Stipulated labels are legitimate for non-entailment countermodels; they do not show the framework is applicable to a real lineage, and the paper makes "No empirical prevalence claim" (p.31).
- Nothing in the document was executed (0 mentions of code, proof assistant, SMT or implementation).
- The document does not mention SSA, R5.3.x, or this project's earlier analysis. It reuses vocabulary ("standing", "witness", a three-valued label scheme, non-entailment tables) without citing the earlier works that use it. We record this as an observation and draw no inference about intent.

## 2. Method

Preregistered before any script existed (`theorem1/PREREG.md`, sha256 `b0ea0b83…`; `definitions/PREREG.md`, sha256 `c6592171…`). Counts first, quoted spans (≤25 words), a residual line for what was not read. Read in full: abstract, introduction, related work, Definitions 1 and 17, §6, §7.2–7.11, §8–12. Not read line by line: the proofs, §4.3, §5.1–5.8 and pp.11–20 definitions in full detail (the definitions pass below read the specific definitions it cites). References were not opened.

## 3. Theorem 1, executed

**Theorem 1** (p.20): under premises (i) defect-auditable normal form, (ii) sound current-support audit, (iii) every represented rule semantically sound, (iv) active-leaf defect-dependence labels correct, and (v) certificate soundness (RouteClosed ⇒ RouteComp, WClosed ⇒ WComp), clean re-derivation PASS implies semantic independence (SemInd = 1) and FAIL implies SemInd = 0.

We implemented Definitions 3–13 as printed on random acyclic Horn programs (2–5 represented leaves, 0–2 hidden leaves, 1–4 internal nodes), injected each premise violation independently with fixed probability, and evaluated every premise directly on each generated world. N = 400,000 per reading, seed 20261017. Source for every figure in §3–§4: this note's own runs, in `descendant_standing_v1_2_checks/theorem1/theorem1_check_output.txt`, `theorem1/RESULTS.md`, `definitions/variant_*_output.txt` and `definitions/definitions_checks_output.txt`; none is taken from the paper.

| Prediction (probability) | Result |
|---|---|
| P1 all five premises hold ⇒ 0 counterexamples (0.95) | 204,984 worlds, **0 counterexamples** — [raw](descendant_standing_v1_2_checks/theorem1/theorem1_check_output.txt) |
| P2 non-vacuous (0.85) | PASS 9.9% / FAIL 29.7% / UNRESOLVED 60.5%; both SemInd values occur under UNRESOLVED — [raw](descendant_standing_v1_2_checks/theorem1/theorem1_check_output.txt) |
| P3 only (iii) violated ⇒ false PASS (0.9) | 613 of 10,590 — [raw](descendant_standing_v1_2_checks/theorem1/theorem1_check_output.txt) |
| P4 only (iv, NO labels) violated ⇒ false PASS (0.95) | 2,077 of 17,529 — [raw](descendant_standing_v1_2_checks/theorem1/theorem1_check_output.txt) |
| P5 only (iv, YES labels) violated ⇒ false FAIL (0.95) | 4,748 of 30,063 — [raw](descendant_standing_v1_2_checks/theorem1/theorem1_check_output.txt) |
| P6 only witness-closure soundness violated ⇒ false FAIL (0.95) | 3,094 of 4,710 — [raw](descendant_standing_v1_2_checks/theorem1/theorem1_check_output.txt) |
| P7 only route-closure soundness violated ⇒ none (0.8) | 0 of 13,375 — [raw](descendant_standing_v1_2_checks/theorem1/theorem1_check_output.txt) |
| P8 only (ii) violated ⇒ none (0.8) | 0 of 44,025 — [raw](descendant_standing_v1_2_checks/theorem1/theorem1_check_output.txt) |
| P9 only (i) violated ⇒ none (0.7) | 0 of 19,954 — [raw](descendant_standing_v1_2_checks/theorem1/theorem1_check_output.txt) |

Nine of nine held. The theorem is sound for the two implications it claims. The load-bearing premises are the audit facts: rule soundness, NO-label correctness (PASS direction), YES-label correctness (FAIL direction), and witness-closure soundness (FAIL direction). A wrong NO label gives a false PASS; a wrong YES label or an unsound witness certificate gives a false FAIL; the smallest counterexamples have four nodes each. Premises (i), (ii) and one of {(iii), route-closure soundness} are idle for these two implications. In plain terms, the theorem is a soundness lemma: if the audits are correct, the conclusions are correct. That is what the paper's own Limitations say.

## 4. Definitions pass

Several defined terms support two readings. We pinned each in the paper's own words and re-ran the check under each reading.

| Term | Reading 1 | Reading 2 |
|---|---|---|
| "established" (Defs 2, 8, 10, 11) | fallible audit verdict | factive (the support really holds) |
| RouteComp (Def 6, p.13) | free ontic attribute (C) | the route carries q (B), or faithful to the true program (A) |
| certificate validity (Defs 6, 10) | only about unresolved exclusions | also enforces the semantic clause |

Isolated-violation classes per premise (LB = load-bearing, counterexamples exist; idle = n ≥ 200 and none; empty = the violation cannot occur in isolation under that reading). "Route C" is the preregistered reading from §3; R_FACT, R_SEM and R_ALL are the variants defined in `definitions/PREREG.md`.

| Premise | Route C | R_A | R_B | R_FACT | R_SEM | R_ALL |
|---|---|---|---|---|---|---|
| (i) | idle | idle | idle | idle | idle | idle |
| (ii) | idle | idle | idle | empty | idle | empty |
| (iii) | LB | idle | idle | LB | LB | idle |
| (iv) NO | LB | LB | LB | empty | LB | empty |
| (iv) YES | LB | LB | LB | empty | LB | empty |
| (v) route | idle | idle | empty | idle | empty | empty |
| (v) witness | LB | LB | LB | LB | empty | empty |

Theorem 1 held in every column (0 counterexamples where all premises hold). The load-bearing set shrinks as the readings strengthen; under R_ALL (route completeness as truth-preservation, factive "established", validity enforcing the semantic clause) only premises (i) and (iii) remain and neither can be violated without being covered, so the theorem is close to definitional. As written, the reader chooses the reading; v1.2 would be clearer with the three choices stated.

**Definition 15 (GateInd), p.19.** PASS requires every relied-upon gate basis to survive; FAIL requires an established-failing basis and "no alternative defect-independent basis is relied upon for that gate." A gate with one failing basis and one surviving alternative, both resolved, fits neither: it comes out UNRESOLVED. Enumerating configurations of up to three resolved bases, 28 are UNRESOLVED when "alternative" means the same gate and 56 when it means any other basis. The text does not say whether the surviving alternative should rescue the gate. One clarifying sentence would settle it.

**Partitions** ([raw](descendant_standing_v1_2_checks/definitions/definitions_checks_output.txt)). Definitions 14, 16 and 17 have no overlaps in exhaustive enumeration (120 Definition 14 configurations; 438 candidate-witness states for Definitions 16 and 17); Definition 13's PASS and FAIL predicates never co-held in 400,000 worlds in any of five variants ([raw](descendant_standing_v1_2_checks/definitions/variant_routeA_output.txt)). The source-family instantiation (SrcFam) shows no contraction or monotonicity violation in 100,000 random families ([raw](descendant_standing_v1_2_checks/definitions/definitions_checks_output.txt)), and the printed micro-example reproduces (NO for Δ={D1}, YES for Δ={D1,D2}). These checks mostly confirm that the paper states its own rules consistently; they do not show that SrcFam models warrant well.

**Undefined primitives.** "Load-bearing" (Def 5), Ψ, SrcFam completeness, Δ, Ω and κ are not mechanisable. A second reader (an external model) independently observed that warrant itself has no stated measurement procedure and enters only as a status label under κ. We keep the narrow form: the ontic layer (Supp, RouteComp, SemInd) is also model-relative, and the premises that bridge audit verdict to world have no stated test. We do not keep the broader claim that the paper "fails" a definition-before-equation standard: the paper labels Theorem 1 conditional, separates ontic from epistemic objects, and states audit-relativity itself (Proposition 3, partial-observation non-identifiability).

## 5. What Theorem 1 does not cover

Theorem 1 says: if the support story is correctly audited in this formal sense, clean re-derivation is semantically meaningful in that story. It contains no learning dynamics (no use of mesa, attention, objective or gradient; "reward" and "self-training" appear only as examples of governance outputs becoming learning signals). The causal learning layer is decoupled from clean re-derivation by design: Observation 1 (p.23) says that within a fixed support structure changing materiality alone does not change CR. An agent or condition outside the represented support structure is not ignored; it is assumed away through the premises. In the check: an unrepresented route that lets the basis survive yields UNRESOLVED when the witness certificate is sound (safe); an unrepresented condition that defeats a represented route makes the rule unsound, and the theorem is then silent (613 false PASS in the isolated class). **CR = PASS is therefore not evidence that an agent is safe or aligned**; it supports only that the stated basis survives withdrawal of the defective ancestor's warrant within the audited story. The paper's own non-entailments point the same way.

**A gap the paper does not address: a governed learner that can influence its own audit.** The paper models a recursive loop explicitly: governance outputs become negative examples, reward or self-training supervision (p.2), and a recursive replay policy χ governs chains such as P1 → D(1) → Z(1) → P2. It also cites work on self-improving agents, but only for the distinction between capability retention and authorization inheritance. It contains no treatment of a strategic or adversarial actor: a text search of the paper finds no use of adversarial, strategic, manipulat-, gaming, Goodhart or tamper-. The confirmed defect set Δ, the review operator Ω, the criterion κ, the dependence specification Ψ and the label audit are all "externally supplied" (p.30), and Theorem 1's load-bearing premises (§3) are exactly the label-correctness and certificate-soundness facts those inputs establish. If the learner whose lineage is being audited can write to, or shape the evidence behind, any of those inputs, premises (iv) and (v) can fail in the direction that produces false PASS or false FAIL, and the theorem is silent. The check in §3 quantifies what a wrong NO label or an unsound witness certificate does; it does not model who might cause one. This is the recursive-self-improvement-adjacent question of whether the gated system can write the gate's input, and the paper's scope statement (a currently asserted governing basis, no prevalence claim) leaves it outside. We state it as an unaddressed condition, not as a flaw in the theorem.

## 6. What is credibly useful

Our paraphrase of the paper's point: an independent evaluator is not an independent evidentiary basis: a fresh evaluator can still rely on lineage-shaped evidence through selection, observability, labels, thresholds or calibration. The selective-labels literature holds the same point; the paper's contribution is drawing the consequence for remediation claims (claim-relative closure). That is an idea worth keeping independent of the framework.

## 7. Limits

- **Same-source caveat.** A single model read the paper, formalized Definitions 3–13, wrote the generator and chose the violation knobs. Where the text is ambiguous we fixed one reading in the preregistration and flagged it. A different formalization could differ.
- Small random structures (at most 12 nodes, derivations capped at 300 records) are a test, not a proof. Corollaries 1–2 and Proposition 1 were not tested.
- Nothing here binds Ψ, the labels or the certificates to a real lineage, evaluator or system, and nothing could from the paper's text alone.
- A reference spot-check by title search was inconclusive for several 2026 items (the index may miss them) and is not reported.
- The paper's v1.0 and v1.1 were not supplied; whether the author has seen the earlier analysis is unknown.

## 8. Reproduction

`descendant_standing_v1_2_checks/` contains the preregistrations, stdlib-only scripts, raw outputs and `SHA256SUMS`. `theorem1/theorem1_check.py` takes an optional reading argument (`C` default, `B`); `definitions/theorem1_variants.py` takes `--route {A,B,C}`, `--factive`, `--semvalid`; `definitions/definitions_checks.py` runs the partition, Definition 15 and SrcFam checks (its quote-verification section needs a plain-text extraction of the paper placed at `../paper_text.txt`; the paper text is not redistributed here, so that section is skipped by default).

## What this note does not establish

It does not establish that the framework is wrong, that its premises can or cannot be met for any real lineage, or anything about the author's intent. It establishes that, under the formalization described, Theorem 1 holds, which premises carry it depends on how three defined terms are read, and one clause of Definition 15 is incomplete.
