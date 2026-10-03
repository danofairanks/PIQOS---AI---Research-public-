# Counter-Models for Pre-Execution Authority-Gate Claims: What Each Argument Needs

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** Pattern-level. No case, specimen, repository or product that is the subject of a pattern is identified, and no party that is small, recent (under about a year old) or without a public amplified position is named. Published works and established organizations are cited by name.
Internal evidence exists and is available to serious inquiries at proof time.
Not a warning about any specific party; it reports patterns.

**Disclosure.** Drafted with AI assistance. The attacks in section 6 were named by the same model that wrote the toys, so they are a same-source check and not independent verification. The attack ideas in section 6a came from a second model family's re-implementation attempt; the predictions, controls and code for them are again by the model that wrote the toys.

## 1. The question

A family of governance claims says that a deterministic gate placed *before* execution gives an authority that probabilistic systems cannot, and that this follows from a few short arguments. This paper takes nine claim forms from one self-published preprint series by a small vendor (seven preprints, read in full: no runs, no measurements, no mechanism disclosed, universal scope in most) and asks, for each, what a counter-model would have to show, builds the counter-model where the text admits one, and states what the claim would need to hold. It tests arguments, not any implementation: none was available and the mechanism is stated as withheld.

## 2. Method

- Each claim form got a defeat condition, in observable terms, **fixed in writing before the toy was built**. The series' own validity criterion supplies the standard: a single executable prohibited path invalidates a governance claim.
- Status vocabulary: **defeated at scope** (the stated observable occurred in a run), **not reached** (the toy could not produce it), **blocked** (it needs an artifact the public text does not supply; not run). Nothing is recorded as refuted on argument alone.
- Companion code (stdlib only, seeded, `--selftest` asserts the pinned results; four scripts): [`pre_execution_gate_counter_models_v1/`](pre_execution_gate_counter_models_v1/). Counts are seed- and parameter-specific; the qualitative results are not (section 6).

## 3. Results by claim form

| Claim form | Toy | Result |
|---|---|---|
| Inference and authority "cannot coexist in the same mechanism" (three-premise argument) | probabilistic scorer with a reject option inside the same function | **Defeated at scope.** 484 of 2000 requests halted with no output and no effect. A narrowed claim survives: the reject option gave no denial guarantee (181 prohibited requests executed). The premise that any output means the core function executed also excludes a deterministic rule gate (998 refusal messages), so it proves too much |
| Determinism gives stability under perturbation | logistic map | **Defeated at scope.** Repeat runs identical; starts 1e-10 apart differ by more than 0.1 at step 37; a stable-regime control contracts |
| Embedded admissibility "guarantees" every successor lies in the permitted set | latent-state gate, honest and masking generators, independent-probe variant | **Defeated at scope** on a gate that reads the system's own report (10 of 10 violating steps passed); **not reached** with an independent probe. The guarantee holds for every transition function by construction (clamp: 51 functions including an adversarial one), so it carries no information about the function or the set; 76% of successors were altered by the projection |
| Hybrid of hard and soft (context-sensitive) constraints escapes that result | predicate variant, context-change run | **Does not escape.** Misreported context passed 15 of 15 soft-zone violations (independent context probe: 0). A state entered legitimately became inadmissible after a context change for 233 of 500 steps with no transition proposed, so the successor check never ran; if the system re-proposes its current state at each step the check runs and denies, but the stranded state stays, because the source states validity for successors and gives no repair or eviction rule (the result is modeling-dependent on that point, and an independent re-implementation attempt made the other choice); the invariant-subset argument holds only for the context-independent core. (A penalty variant accepts soft-violating proposals, but that restates a textual exclusion in the source's own wording and is not counted as a toy result) |
| Prohibited paths proven absent over the state space | model graph versus real graph; side channel; host that kills the gate | **Defeated at scope.** The proof over the model holds while an executable prohibited path exists in the real graph; a model rebuilt from traces of the real graph detects both |
| Out-of-space actions are "unreachable" (complete mediation) | same graph, unmediated edge | **Defeated at scope** (an effect path outside the gate) |
| Same governing law across constitution, admissibility and execution; "the interfaces are part of the proof" | nondeterministic stage before a deterministic gate | **Defeated at scope.** The same input gives both outcomes (deny fraction 0.584 at noise 0.5 over 500 runs); the outcome is stable only at margins of about four noise units or more; a deterministic-stage control gives one outcome |
| A threshold on a scalar score guarantees limits "regardless of input" | none | **Blocked.** The score is undefined |
| "The system exists, runs, and its authority chain has been exercised" | none | **Blocked.** No artifact, trace or hash |

## 4. What the defeats share

Each defeat has the same structure as the channel-collapse result in [`execution_gate_channel_collapse_v1.md`](execution_gate_channel_collapse_v1.md), at a new site: **the check runs on a channel the governed side produces or can influence** (its report, its reported context, a model of its state space, an upstream interpretation stage). Each closes by one of the two exits that paper names: an observation channel the governed side does not control (independent probe, trace-derived model), or a stated placement that removes the second channel. The toys that closed under an independent channel are results for the requirement, not against the claim form.

## 5. What a pre-execution gate claim needs

Generic and testable; none is a statement about what exists in any product.

1. Enumerated effect paths and the mediation point for each (complete mediation: Saltzer and Schroeder [3]; the reference monitor concept: Anderson [4]).
2. Placement and trust root: what happens when the host tries to bypass, kill or modify the gate (tamper-resistance).
3. A proof object over the real artifact, or a model-to-real fidelity argument.
4. Provenance and correction of the rule content, with a terminus; or an explicit scope limit and withdrawal of any claim to constitute authority.
5. An observation channel, independent of the governed system, for every state or context condition the rules depend on, with an error bound. Enforceability by monitoring has a known characterization: Schneider [5].
6. The status of any probabilistic or interpretive stage in the decision path, with a variance bound if present. A reject option is established practice in classification: Chow [1], El-Yaniv and Wiener [2].
7. Definitions of any score used in a threshold, plus an adversarial-input analysis, or drop "regardless of input".
8. A statement of what is preserved at each stage boundary, with evidence.
9. Runs against systems the author did not write, with an examiner-chosen read path and a preserved, hashed trace.
10. The third-party findings themselves (claim examined, evidence inspected, property established, scope); a patent filing or application is not a finding.
11. One stable definition each of authority, determinism and execution across a series.
12. Scope per claim reconciled with narrower scope statements made elsewhere in the series.

13. Check-to-use atomicity: the independent check and the effect are one atomic step, or the check is repeated at execution time, with the availability cost reported (section 6a).
14. Effect-level observation: a model rebuilt from traces needs an independent monitor on the effect channel; state transitions alone cannot see an effect that leaves the state trace unchanged (section 6a).
15. A stated policy for run-time-generated actions, default-deny or otherwise, with the cost reported as legitimate actions blocked; enumerated deny-lists and alias maps are only as good as their coverage (section 6a).
16. A single canonical parse: the gate canonicalizes and the executor runs exactly the object the gate saw (section 6a).

**Minimal set to make the strongest claim testable at all:** 1, 2, 4 (or the scope limit) and 9. Items 13 to 16 refine items 1 and 5 and do not change the minimal set.

## 6. Attack round 2 (author-named, not independent)

Nine steelman attacks were named and given observables and predictions before any code. All nine outcomes matched the predictions, which is weak evidence of adversarial strength: the author predicted the author's own results. The round's usable output is the narrowing it forced:

- **Decomposition.** The denial guarantee of a probabilistic mechanism with a reject option requires a noise-free read of ground truth, i.e. a deterministic gate (prohibited requests executed: 0 at scorer noise 0, 5 at 0.2, 181 at 0.8). The halting result stands (484 to 689 halts at every noise level).
- **Full observability.** The latent-state defeat applies only where latent variables exist: with the reported state read from the state itself, 0 violations.
- **Authenticated context.** Signing the context report does not close the hole unless it is fresh and from a signer the governed system does not control: unauthenticated 15; authenticated but replayable 15; fresh nonce from an independent signer 0.
- **Coverage of the exit.** A model rebuilt from traces misses rare edges unless coverage is sufficient: for an edge of probability 0.001, detection 0.28 at 100 walks, 0.84 at 1000, 1.0 at 10000.
- **Meaning of "deterministic".** It holds for exact input identity, not for paraphrases near a margin; the term needs a definition.
- **The independent probe is itself a channel.** With probe miss probability 0, 0.05, 0.2, mean violations passed were 0, 0.38, 1.84 of 10: the residual scales with the error and the regress relocates to probe integrity. It is not closed.
- **Straw-man check.** The penalty variant of the hybrid is a textual exclusion check, not a counter-model result; reclassified.
- **Unchanged.** Sensitivity at every precision tried (8 to 52 bits); the model-to-real gap; the qualitative results across 180 runs (20 seeds, 3 noise levels, 3 thresholds).

## 6a. Round 3: attack ideas built as simulations with controls

A second model family re-implemented the toys from an earlier version of this text and named further attacks. Its code encoded each attack so it could not fail (replacing the attack property with its absence did not change the observable), so those results were not counted. The attack ideas were kept and rebuilt: each toy computes its outcome by running a mechanism, counts are incremented inside the function they count, each has a control that must read zero (a non-zero control marks the toy broken) and a mutation that removes the attack property. Observables and predictions were fixed before the code.

| Attack | Observed | Read |
|---|---|---|
| Check-to-use gap (an independent probe at time t, the effect later) | Governed side flips state right after a passing probe: 2000 of 2000 effects executed while violating. Random flips (probability 0.1 per step over 5 steps): 0.402 of trials. No flips, or zero delay: 0. Atomic check-and-act: 0. Recheck at execution time: 0 at probe miss 0, 35 of 2000 at miss 0.05, with 807 of 2000 trials blocked | The independent probe of section 4 closes the hole only if check and effect are atomic or the check is repeated at execution time; the repeat has an availability cost |
| Trace semantic aliasing | Models rebuilt from state-only traces are identical for a benign and a hostile system with the same topology, and a "no prohibited effect" proof holds for both. Models from effect-instrumented traces detect the hostile one and do not flag the benign one | A trace-derived model needs an independent monitor on the effect channel |
| Dynamic dispatch after enumeration | Known-name deny-list: 300 prohibited effects executed. Alias-normalized deny-list: 70, all via an alias outside the map. Default-deny allowlist: 0 prohibited. Only canonical names generated: deny-list 0 | A prediction missed in the base world: I predicted the allowlist would block some legitimate actions, and it blocked 0 because the generator emitted only enumerated legitimate names. With 10% novel legitimate actions added, it blocks 163 and still lets 0 prohibited through. The base counts moved slightly from the first run (299 and 78) because adding that draw changed the random stream, not the semantics |
| Gate and executor parse the same request differently (exhaustive, exact) | 14 of 30 requests allowed by the gate and executed as the prohibited operation (first versus last duplicate key; case-sensitive versus case-folded). Gate canonicalizes and passes its canonical operation: 0. Parse-once without normalization while the executor still case-folds: 12. Grammar without duplicates and case variants: 0 | Parse-once is not enough alone; the gate must canonicalize and the executor must run exactly what the gate saw. An earlier version of this control was vacuous and was rewritten as two separate code paths |
| Advisory gate versus gate-owned effect path | Advisory, host compliance 1.0: 0; 0.9: 60 of 610 prohibited requests; 0.0: 610 of 610. Owned effect path, bypass 0: 0; bypass 0.1: 61 of 610 | Parametric by construction (rates in, rates out); low evidential weight; it restates the mediation requirement |
| Hybrid with the current state re-proposed (instrumented gate) | No proposal: 0 gate invocations, 233 stranded steps. Re-propose each step: 500 invocations, 233 denies, 233 stranded. Repair on deny: 1 deny, 1 repair, 0 stranded | Replaces the earlier constant gate-invocation field. The repair rule removes the stranding but, in this toy, moves the state out of the soft zone for good, and the source states no such rule |

The four requirements added in section 5 (items 13 to 16) come from this round. Round 3 is still same-source: the attack ideas are another model's, the predictions and code are the author's. Counts are exact only for the parse-mismatch toy (enumerated); the others are seeded.

## 7. Results that cut against a one-sided reading

The literal impossibility claim is defeated but a narrowed form survives. The model-to-real proof is sound when the model matches the real graph (that world is not defeated). A deterministic gate is stable under an interpretive stage whenever the margin exceeds that stage's noise, so a variance bound would settle it. The hard-constraint core guarantee holds for every function.

## 8. What this does not establish

- That any implementation fails or works; intent of any party; prevalence.
- That the toy parameters are representative: counts depend on seeds and parameters; the qualitative defeats do not.
- Anything about patent claims, which were not read.
- Single rater; the round-2 and round-3 attacks are same-source.

**What would show this paper wrong.** A failing `--selftest` on a clean checkout (four scripts); a defeat condition shown to be mis-specified against the source text; or a published placement, trust root, effect-path list and third-party run protocol that satisfies items 1, 2, 4 and 9 for a specific gate. Reproduction so far is execution only: a run by a different model family (Python 3.12.3) and the author's runs (Python 3.10.20, 3.11.15) give byte-identical output for all three scripts ([`REPRODUCTION.md`](pre_execution_gate_counter_models_v1/REPRODUCTION.md)); it did not re-implement from this text. Owed: a re-implementation from this text alone and an independent attack round.

## References

[1] C. K. Chow. On optimum error and reject trade-off. *IEEE Transactions on Information Theory* 16(1):41–46, 1970.

[2] R. El-Yaniv and Y. Wiener. On the foundations of noise-free selective classification. *Journal of Machine Learning Research* 11:1605–1641, 2010.

[3] J. H. Saltzer and M. D. Schroeder. The protection of information in computer systems. *Proceedings of the IEEE*, 1975.

[4] J. P. Anderson. *Computer Security Technology Planning Study.* James P. Anderson & Co., report for the USAF Electronic Systems Division, October 1972.

[5] F. B. Schneider. Enforceable security policies. *ACM Transactions on Information and System Security* 3(1):30–50, 2000.

Bibliographic details of [1]–[5] were checked against search-result summaries (tier: search summary, not the primary documents).
