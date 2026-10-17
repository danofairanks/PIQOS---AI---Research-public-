# Preregistration — definitions pass on the Descendant Standing Problem v1.2 (2026-10-17)
Written before any definitions-pass script was written or run. Operator request: pin each term in the paper's own words, mark where the text supports two readings, rerun the Theorem 1 check under each reading.
Same-source caveat: single Anthropic-model reader/coder. "Reading" = a way of resolving an ambiguity that I identify in the text; I may miss readings.

## Items
D1 "establishes / established" (Defs 2, 4, 8, 10, 11): audit verdict (fallible) vs truth (factive).
D2 RouteComp (Def 6): (C) free ontic attribute of a rule, not tied to truth [preregistered earlier]; (B) route carries q = rule truth-preserving in both models [post-hoc earlier]; (A) faithfulness = the represented rule is a rule of the true program with the same body (no omitted hidden condition).
D3 Certificate validity (Defs 7, 10): (V1) validity is object-level and soundness is a separate premise [paper's p.17 wording]; (V2) the validity clause itself ("no unresolved item could ...") enforces the semantic property, so soundness holds by definition.
D4 Def 15 GateInd: does a gate with one established-failing basis and one established-surviving alternative basis get PASS, FAIL or UNRESOLVED as printed.
D5 Status partitions: Defs 13, 14, 16, 17 exclusive and exhaustive as printed.
D6 Source-family instantiation of Psi (p.14): contractive and label-monotone as claimed, on the printed micro-example and on random families.
D7 "load-bearing" (Def 5), warrant primitives (kappa, Omega, Delta): no operational criterion in the text: pinned and marked; not mechanizable here.

## Predictions [probability]
DP1 [0.9] D5: exhaustive enumeration finds no overlap and no gap in Defs 14 and 17 as printed; no PASS-and-FAIL overlap for Def 13 in 400k random worlds.
DP2 [0.9] D4: enumeration finds assignments in which every basis is resolved (none unresolved) yet GateInd is neither PASS nor FAIL (so UNRESOLVED), namely a gate with at least one established-surviving and one established-failing relied-upon basis.
DP3 [0.97] D6: zero violations of contraction (Supp(D) => Supp(D') => Supp(empty) for D' subset of D) and of label monotonicity over random certified-complete families; the printed micro-example gives NO for {D1} and YES for {D1,D2}.
DP4 [0.85] Reruns of the Theorem 1 check (400k worlds, seed 20261017, same generator) under these readings:
  R_A (RouteComp A): isolated-(iii) class and isolated-route class both have zero counterexamples.
  R_B (RouteComp B): isolated-(iii) zero counterexamples; isolated-route class empty (already observed post hoc).
  R_FACT (D1 factive: premises ii, iv-NO, iv-YES hold by definition; RouteComp C): their isolated classes are empty (n < 200); counterexamples remain only in isolated (iii) and isolated (v-wit).
  R_SEM (D3 V2: both halves of (v) hold by definition; RouteComp C): isolated (v) classes empty; counterexamples remain in isolated (iii), (iv-NO), (iv-YES).
  R_ALL (B + factive + V2): no isolated class has counterexamples; the premise set that carries the theorem is empty.
DP5 [0.85] Across all readings, premises (i) and (ii) never appear in the set of load-bearing premises (isolated class non-empty with counterexamples).

## Reporting rules
Per variant: class table (n, PASS/FAIL/UNRES, counterexamples); a class with n < 200 is "empty (analytic under this reading)"; a class with n >= 200 and zero counterexamples is "idle"; with counterexamples is "load-bearing". No change to generator or knob probabilities between variants other than the reading switches. Failed predictions reported as failed.
