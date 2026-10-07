# Blind pass: counter-models for "authorization depends on trajectory, not final state" claims

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** Pattern-level. The claim family below comes from a recent self-published preprint on authorization state in persistent AI agents; the preprint, its author and its benchmark are deliberately not named, and no party that is small, recent or without a public amplified position is identified. This page is a brief for a reviewer, not a finding about anyone.

**Disclosure.** Drafted with AI assistance. The defeat conditions and the code in `toys.py` were written by one model family, so they are same-source until a different family attacks them. That attack is the purpose of this page. The author's own results and predictions are withheld on purpose.

## What you are asked to do

You are a reviewer from a different model family than the one that wrote this. Work from this page and `toys.py` only. **Do not look up the source preprint.** You may use what you already know.

Return, in this order:

1. **Before reading further than section 2:** from memory, list any prior published work you know that states the central test (section 1) or the augmentation point (CF1). Give titles/authors/years you are confident of, mark the rest uncertain. Say what you could not recall. This is an independent novelty check, so do not search first.
2. **Per claim form (CF1 to CF5):** (a) is the defeat condition observable and well posed, or does it hide a free parameter; (b) the strongest counter-model or objection the author did not name, with your own defeat condition stated in observable terms; (c) your **prediction** for the matching toy, written before you run anything, with a number or an inequality; (d) whether the "survives only if" clause is too lenient or too strict.
3. **Run `python3 -I toys.py`** and compare with your predictions. Report every mismatch, and every bug, tautology or unfair control you find in `toys.py`. Say which results are determined by construction.
4. **Missing claim forms:** any claim the family makes that the five below do not cover.
5. A one-paragraph verdict: which defeat conditions you would keep, change or drop.

Status vocabulary for any conclusion you reach: **defeated at scope** (the stated observable occurred in a run), **not reached** (the toy could not produce it), **blocked** (needs an artifact not supplied), **not run**. Do not call anything refuted on argument alone. Flag fluent but unsupported reasoning in your own answer.

## 1. The claim family (paraphrased, not quoted)

Authorization for a consequential agent action cannot be decided from the final authority state alone; validity may depend on the trajectory (the security-relevant history H, plus the evidence E needed to reconstruct it). Written: `Auth = f(A_final)` versus `Auth = f(A_final, H, E)`.

**Central test.** Build matched pairs of trajectories X_A and X_B with `A_final(X_A) = A_final(X_B)` but different histories. If `Auth(X_A) != Auth(X_B)`, validity is trajectory-dependent.

Supporting machinery in the family: a authority state tuple (principal, mandate, conditions, delegation, effect ceiling, validity); a trusted transition function T with `A_next = T(A, event)`, where the model proposes but must not decide whether its own authority survived; an "authority-state divergence" score `ASD = d(A_0, A_t)` (weighted over mandate, conditions, delegation, effect ceiling, policy, resource); a "decision freshness" score that depends on elapsed time and on changes in state, policy, delegation and resources; a revalidation step before the effect; and a named property, "survivability" (applicability, boundedness, revalidation, reconstructability).

**Reported validation (synthetic).** A generated benchmark of 10,000 scenarios, 5,000 matched pairs. Reference systems defined as final-state-only show a 51.1% false-continuation rate; reference systems defined as transition-aware show 0. The author hedges that real LLM-agent rates are not established.

## 2. Claim forms and the defeat conditions fixed before the toys were built

**CF1. Final-state insufficiency is a property of authorization.**
- Counter-model (state augmentation): any history-dependent validity rule can be written as a function of a final state extended with a sufficient statistic of the history, so "insufficiency" is relative to which fields the state may hold.
- Defeat condition: for a stated history-dependent rule, exhibit a bounded extra statistic whose addition makes a final-state function match the history-aware answer on all matched pairs. Then the claim is defeated at scope for that rule.
- Survives only if: a rule exists whose sufficient statistic grows without bound with trajectory length, or the augmentation is unavailable for a stated engineering reason.
- Toy T1: three rules over events {grant, revoke, act}, residual-class counts by enumeration.

**CF2. The 51.1% versus 0 result shows final-state systems fail.**
- Counter-model (benchmark semantics): a reference defined as blind to H, scored on pairs built to differ only in H, must fail exactly where the label depends on H. The rate is then a generator parameter.
- Defeat condition: with the label-from-history fraction p set by hand, the false-continuation rate tracks p. If it does, the number is not an empirical rate.
- Survives only if: labels come from a source independent of the references, and real agent traces give a non-trivial rate.
- Toy T2.

**CF3. ASD predicts errors better than elapsed time; decision freshness is a usable input.**
- Counter-model: distance, weights and freshness function are free parameters; with enough freedom ASD can beat a single scalar in-sample.
- Defeat condition: fit weights on one generator, test on a held-out generator with a different label rule; advantage under 0.02 AUC on the second means the advantage is the fit.
- Survives only if: weights are fixed before evaluation and still win on a generator not used to choose them.
- Toy T3.

**CF4. A trusted transition function can track authority.**
- Counter-model (self-supplied channel): if the events or the evidence come from the agent's own report, the check runs on a channel the governed side controls. Also: silence read as "still authorized".
- Defeat condition: an agent-reported revocation stream where the agent omits the revocation; count violating steps that pass. Also a silent revocation channel under default-allow versus default-deny.
- Survives only if: the producer of events is named and independent of the agent, and the default for a silent channel is deny.
- Toy T4.

**CF5. Revalidation before the effect makes continuation safe.**
- Counter-model (check-to-use gap and cost): a check at time t and an effect at t+w leave a window for a revocation to land between them unless the effect is bound to the checked version; revalidating every change false-denies benign work.
- Defeat condition: unbound effect executes after revocation at a rate that rises with w; version-bound consume gives zero. Report the false-denial rate of strict revalidation on benign churn.
- Survives only if: effect binding or atomic check-and-effect is specified, and a false-denial rate is reported next to the false-continuation rate.
- Toy T5.

## 3. Known limits of this brief
- The toys encode the mechanisms; several results are determined by construction and you should say which.
- One seed each; class counts in T1 are lower bounds (suffix length equals prefix length).
- The benchmark itself was unavailable, so nothing here touches its own numbers.
- The brief was written by the same model family as the toys. Your independence is the point.
