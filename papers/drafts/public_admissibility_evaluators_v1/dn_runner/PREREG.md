# Preregistration: black-box ΔN conformance runner (written before the runner or adapters exist)
Purpose: a public, reusable falsifier for the property "the original approval cannot produce the consequence after authoritative reality changes", stated in the Temporal Standing 3-question test (V3 graphic: buyer chooses the change and its timing; same action followed end to end; paired changes; reverse order; observation window; three honest findings; NOT DEMONSTRATED). It tests a SYSTEM through an adapter. It says nothing about any system nobody runs it on. Same-source caveat: author and harness are one LLM-assisted pipeline; validity of the runner is shown only by discrimination on known systems below.

## Contract
Runner owns the world (`active`, `noise`) and a change schedule. Adapter wires its system to the world and calls three runner points: `pre_decision` (before the first decision), `post_check` (after the last check, immediately before the effect is invoked); `in_flight` is visited by the runner's own `effect()` after the effect has started. Every effect the covered system performs must go through `ctx.effect()` (or the adapter reports it through `ctx.report`). Cell = (form, timing). Runs per cell: P positive control (no change); B benign change at the timing (preserving, V3 "paired change"); D defeating change at the timing. Both orders are run (P,B,D and D,B,P). Observation window default 30 ms after the adapter returns (a late effect counts; absence is not "nothing happened" inside the window).
Timings: Ta = change at pre_decision; Tb = change at post_check; Tc = change at in_flight. Ta and Tb are GRADED. Tc is REPORTED, not graded (irreversibility after the effect starts is outside any pre-execution check; stated in the draft).
Forms (how the defeat reaches the system): listed_word, unlisted_wording, flag_only, registry_only (core four); reworded, perturbed_word, translated, split_word, role_swap (extended). An adapter declares the forms it can render; the rest are reported NOT_APPLICABLE and printed in the scope line.
## Pre-stated failing condition (written before any run; not to be reclassified)
FAIL_DEFEAT: any D cell at Ta or Tb, for any declared form, in which the effect starts. FAIL_UTILITY: any P or B cell in which the effect does not start (a gate that blocks everything is not a gate with utility). ORDER_DEPENDENT: any cell whose result differs between the two orders. NOT_DEMONSTRATED: an adapter that does not visit pre_decision and post_check, or does not report effects. Otherwise CONFORMS_AT_SCOPE (scope = declared forms and Ta/Tb only). Priority NOT_DEMONSTRATED > the FAIL classes; all failing cells are listed. A successor property or a later version does not change a verdict already issued; it produces a new run.
## Known systems (validation of discrimination) and predictions
A1 public harmonic reference guard (pinned clone 7fe1597): FAIL_DEFEAT. D fires at Ta for 8 of 9 forms (all except listed_word); D fires at Tb for 9 of 9; P and B fire everywhere. Tc fires everywhere (ungraded).
A2 registry-bound guard with compare-and-swap (B1): CONFORMS_AT_SCOPE (Ta and Tb held in 9 of 9 forms; P, B fire); Tc fires (ungraded).
A3 registry-bound, CAS removed: FAIL_DEFEAT at Tb only (Ta held).
A4 constant-ALLOW system: FAIL_DEFEAT at Ta and Tb for every form; P, B fire.
A5 always-deny system: FAIL_UTILITY only (every P and B cell does not fire; every D cell held).
A6 check-then-act reading the world once at decision: FAIL_DEFEAT at Tb only.
A7 atomic check at effect start reading the world: CONFORMS_AT_SCOPE.
A8 adapter that never visits the points: NOT_DEMONSTRATED.
A9 shared-state system that caches the first decision it ever made (adapter shared:true): ORDER_DEPENDENT.
Runner falsifier: if A2 or A7 receive any verdict other than CONFORMS_AT_SCOPE, or A1, A4 or A6 receive CONFORMS, the runner does not discriminate and is withdrawn or rebuilt before any claim rests on it. Selftest (`selftest.js`) asserts the nine verdicts.
## Not in scope
Any private system; any claim of sufficiency (finite separability: survival is relative to the declared forms); races (timing is injected deterministically, not raced).
