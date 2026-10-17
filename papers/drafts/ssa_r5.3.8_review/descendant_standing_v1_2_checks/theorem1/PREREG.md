# Preregistration — mechanical check of Theorem 1 (Škrinjar, Descendant Standing Problem v1.2, p.20)
Written 2026-10-17 before the script was written or run. Operator request: run the mechanical check on Theorem 1.
Same-source caveat: single Anthropic-model reader/coder. Formalization is mine, from Defs 3-13 (pp.11-17); where the text is ambiguous I fix one reading below and flag the dependence.

## What is tested
Theorem 1 (p.20): under premises (i) defect-auditable normal form, (ii) sound current-support audit (ACTIVE => Supp(M_pi)=1, FAILED => Supp(M_pi)=0), (iii) every represented Horn rule semantically sound in M_pi and M_{-D}, (iv) active-leaf defect-dependence labels correct (NO => leaf survives in M_{-D}; YES => it does not), (v) certificate soundness (RouteClosed=1 => RouteComp=1; WClosed=1 => WComp=1):
CR=PASS => SemInd=1, and CR=FAIL => SemInd=0 (SemInd=1 iff M_{-D} |= q).

## Model (finite, random)
- True program: acyclic positive Horn rules over nodes (represented leaves, hidden leaves, internal nodes, root q). Leaf truth cur[l] in {0,1}; wd[l] <= cur[l] (support-contractive withdrawal, p.13). M_pi, M_{-D} = least models of the TRUE program from cur / wd. SemInd = M_{-D}(q).
- Represented structure S: represented leaves L; represented rules = a subset of the true rules with no hidden leaf in the body (omitted rules and hidden leaves create unrepresented support routes); optional violation injections below.
- Audit outputs: CurSupp status per represented leaf (ACTIVE / FAILED / UNRESOLVED); labels lambda in {NO, UNRESOLVED, YES} for ACTIVE leaves; per-rule "complete" bit (RouteComp is a free ontic attribute of a rule: reading C); RouteClosed(d) per derivation record (rules used, leaves); WClosed.
- Definitions implemented as printed: A, U, F; A_NO; Seed<=? = U + {active leaves labelled NO or UNRESOLVED}; CR = PASS iff some derivation has leaves in A_NO and RouteClosed=1; FAIL iff WClosed=1 and no derivation has leaves in Seed<=?; else UNRESOLVED. WComp(M_{-D}|=q => exists represented derivation with leaves in (A+U) that survive in M_{-D} and all rules complete).
- Violation knobs (each applied independently with fixed probability per world): (i) include a true rule with its hidden-leaf body conditions dropped; (ii) flip ACTIVE/FAILED against cur; (iii) add a represented rule absent from the true program; (iv-NO) label NO on an active leaf with wd=0; (iv-YES) label YES on an active leaf with wd=1; (v-route) RouteClosed=1 on a derivation with an incomplete rule; (v-wit) WClosed=1 when WComp=0.
- Premises are then evaluated DIRECTLY on each generated world (not assumed from the knobs), and worlds are classified by exactly which premises hold.
- Seed 20261017; N = 400,000 worlds; derivation enumeration capped at 300 records per world (worlds above the cap are skipped and counted).

## Predictions (recorded now; probabilities in brackets)
P1 [0.95]. On worlds where all five premises hold: zero counterexamples to PASS => SemInd=1 and to FAIL => SemInd=0.
P2 [0.85]. Non-vacuity on those worlds: PASS, FAIL and UNRESOLVED each >= 5% of worlds; under CR=UNRESOLVED both SemInd values occur (so "no semantic conclusion follows" is non-vacuous).
P3 [0.9]. Violating only (iii) (unsound represented rule), with route certificates left sound under reading C, yields PASS counterexamples > 0.
P4 [0.95]. Violating only (iv-NO) yields PASS counterexamples > 0.
P5 [0.95]. Violating only (iv-YES) yields FAIL counterexamples > 0.
P6 [0.95]. Violating only (v-wit) yields FAIL counterexamples > 0.
P7 [0.8]. Violating only (v-route) yields ZERO counterexamples: the RouteClosed => RouteComp half of (v) is idle for the stated conclusion, because RouteComp is not tied to truth values in the definitions and soundness of rules in M_{-D} (premise iii) already gives PASS => SemInd=1. (Dependence on reading: if RouteComp is read as "the route carries q", premise (iii) becomes the idle one instead. Either way one of the two is redundant for this conclusion.)
P8 [0.8]. Violating only (ii) yields zero counterexamples (idle for the stated conclusion; it is used by Corollary 1, not Theorem 1).
P9 [0.7]. Violating only (i) yields zero counterexamples or cannot be isolated from (iii) in this generator (reported as n/a if fewer than 200 such worlds).

## Reporting rules
Counts, rates and all classes with n < 200 are reported as untestable. No re-tuning of knob probabilities after seeing results except to fix a bug against the printed definitions; any such change is logged with the reason. A prediction that fails is reported as failed.
