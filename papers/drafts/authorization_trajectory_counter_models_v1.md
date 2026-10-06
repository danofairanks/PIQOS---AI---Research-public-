# Counter-Models for "Authorization Depends on Trajectory, Not Final State": What Each Claim Needs

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** The work examined is identified by its own title and benchmark name, not by any person: the October 2026 self-published preprint *Authorization State and Trajectory in Persistent AI Agents: Testing Final-State Sufficiency* and its synthetic benchmark (AS-Bench). No author is named, no intent is attributed, and nothing here is a finding about a person. The paper examines arguments and one benchmark's headline number, not an implementation. Other works are cited by arXiv identifier and title.

**What was read.** The preprint's full text was **not** read. The claim forms below were taken from a screenshot of its summary page and a short summary note, so they may misstate it, and a claim stated there with a hedge may appear here without it. The author's own caveat is kept: the reported rates are on a synthetic benchmark and real LLM-agent rates are not established.

**Disclosure.** Drafted with AI assistance. The defeat conditions and the toys were written by one model family. Two review passes (section 7) followed; neither was blind in the strong sense. Nothing here is independent verification.

## 1. The question

The preprint asks whether the final authorization state is sufficient to decide whether a consequential action is authorized, or whether validity can depend on the trajectory through which that state was reached. It writes the contrast as `Auth = f(A_final)` against `Auth = f(A_final, H, E)`, with H the security-relevant history and E the evidence needed to reconstruct it. Its central experiment is a matched pair: two trajectories with the same final state and different histories, where a different correct decision shows trajectory dependence. Its support is a generated benchmark (10,000 scenarios, 5,000 matched pairs) on which final-state-only references show 51.1% false continuation and transition-aware references show 0.

This paper asks what each claim form would have to survive. For each it fixes, in observable terms and before building anything, a counter-model and a defeat condition; builds a small toy; reports what happened, including the predictions that missed; and says what the claim would need to hold.

## 2. Method

- One defeat condition per claim form, **written before the toy was built** ([`PREREG.md`](authorization_trajectory_counter_models_v1/PREREG.md); later changes are dated amendments below the original text).
- Status vocabulary: **defeated at scope** (the stated observable occurred in a run), **not reached** (the toy could not produce it), **blocked** (needs an artifact not supplied), **not run**. Nothing is recorded as refuted on argument alone.
- Companion code (stdlib only, seeded, `--selftest` asserts the pinned results): [`authorization_trajectory_counter_models_v1/`](authorization_trajectory_counter_models_v1/). Counts are seed-specific; qualitative results are not.
- Several toy results are **determined by construction** (the toy encodes the mechanism). They show the structure has the stated consequence; they are not evidence that any real system has it. Each result below says which kind it is.

## 3. The claim forms and what the toys showed

| Claim form | Counter-model | Toy | Result | Kind |
|---|---|---|---|---|
| **CF1.** Final-state insufficiency is a property of authorization | State augmentation: any history-dependent rule is a function of a final state extended with a sufficient statistic of the history, so insufficiency is relative to the fields the state may hold | T1: three rules over {grant, revoke, act}; residual classes by enumeration (prefixes and suffixes up to length n) | Rule A (lifetime cap): 4, 7, 7, 7, 7 classes for n = 2..6. Rule B (no restore after any revoke): 3 at every n. Rule C (one act per grant, lifetime): 6, 9, 12, 15, 18. Matched pairs with equal naive final state and different correct answers exist for all three | **Defeated at scope for A and B** (a 7-class and a 3-class statistic reproduce the answer exactly); **not defeated for C**, whose statistic grows with trajectory length. Not by construction for the class counts; the naive-state mismatch counts measure the chosen projection, and rule A's naive state already carries a counter |
| **CF2.** The 51.1% vs 0 result shows final-state systems fail | Benchmark semantics: a reference defined as blind to H, scored on pairs built to differ only in H, must fail where the label depends on H; the rate is a generator parameter | T2: matched pairs with history-dependent fraction p set by hand | False continuation over all cases 0.050 / 0.147 / 0.251 / 0.351 / 0.496 at p = 0.1 / 0.3 / 0.5 / 0.7 / 1.0 (about p/2); 0.50 among history-dependent pairs at every p. Pairs mined from rule-A random walks: 10,002 equal-state pairs, 0.197 differ | **Defeated at scope as an interpretation of the rate**: the toy's rate is its parameter. **By construction** (the coin is hand-set). My toy tops out at 0.50, so the preprint's 51.1% was not reproduced (0.496 vs 0.511, about 4 standard errors); its denominator and labels were not available |
| **CF3.** An authority-state divergence score predicts errors better than elapsed time | The distance, weights and freshness function are free parameters | T3: two generators with different label rules; logistic score fitted on the first | Held-out first generator: fitted 0.952, elapsed 0.784. Second generator with first-generator weights: 0.791 vs elapsed 0.805. Controls (T3b): equal-weight change count 0.862 / 0.878; elapsed plus total change count 0.859 / 0.878 | **Defeated at scope**: out of sample, the fitted score has no advantage over an unweighted change count. The toy implements a fitted logistic, not a distance `d(A_0, A_t)`, so it does not test the preprint's score as defined; the fitted result is in-sample by construction. One prediction missed (below) |
| **CF4.** A trusted transition function can track authority; the model must not decide whether its own authority survived | Self-supplied channel: if events or evidence come from the agent's report, the check runs on a channel the governed side controls; silence read as "still authorized" | T4 and T4b: agent-reported revocation stream; silent channel; independent channel with delivery delay d | Masking agent: 300 of 300 post-revocation steps pass. Silent channel, default-pass: 300; default-deny: 0. Independent channel delayed by d steps: d violating steps (d = 0, 5, 20, 50 gave 0, 5, 20, 50) | **Defeated at scope** for an agent-sourced or default-pass design. **By construction.** Default-deny on silence does not close a late channel; a delivery bound is a requirement. Run-1 row for the independent channel was the honest-agent function (a dead argument) and is not evidence |
| **CF5.** Revalidation before the effect makes continuation safe | Check-to-use gap; cost | T5 and T5b: revocation rate r = 0.02 per tick between check and effect; effector variants | Unbound effect: 0.018, 0.095, 0.184, 0.338, 0.552 for window w = 1, 5, 10, 20, 40, tracking the closed form. Atomic compare-and-consume: 0 (by construction of the toy's compare). Non-atomic version-honoring effector: 0.018 to 0.010, falling with w. Version-ignoring effector: tracks the unbound rate. Strict revalidation on benign churn: 0.343 false denial | **Defeated at scope** for unbound and non-atomic effects. Binding closes the window only if compare and act are atomic and the effector honors the version. **By construction** except the effector comparison. Run-1 "bound = 0" was hard-coded and is withdrawn |
| **CF6.** The finding is new | Prior art | Literature check, section 6 | The matched-pair test and the augmentation point are prior art | **Defeated at scope** for novelty of those two |

**Predictions that missed.** (1) T2: I expected the 51.1% to be reproducible near p = 1.0; the toy tops out at 0.50. (2) T3b: I expected the elapsed-plus-count baseline to be within 0.02 of the transferred score; it beat it by 0.087. The first-run reason I gave for CF3's defeat (weight overfit) was incomplete; the control shows the advantage over elapsed time is largely an unweighted change count. (3) T5b: I expected the non-atomic leak to be flat at 0.02; it falls with w because the leak counts only paths not already revoked before the read (r(1-r)^w). (4) T5b: the version-ignoring closed form I predicted was off by one tick (the gap tick is in the window).

**Harness errors kept.** T4 passed an argument it never used; T5's version-bound row was a constant; T1 rule A's "final state" included a history counter; T1 `pairs` duplicates `mism`; T5's comment said five dimensions where four were checked. All were found by the review passes in section 7 or on rereading; run 1 output is kept in `out_run1.json` and the controls are in `toys_v2.py` and `out_run2_v2controls.json`.

## 4. Claim forms added after review, defeat conditions fixed, not run

- **CF7 reconstructability (E).** Defeat: with H present but E missing, delayed, contradictory or agent-writable, a transition-aware reference's false-continuation rate rises to the final-state reference's rate.
- **CF8 state-source integrity.** Delay is covered by T4b. Defeat for replay and freshness: an independent but replayed or stale event stream produces a wrong decision.
- **CF9 atomicity and concurrency.** T5b covers one effect. Defeat for concurrent queued effects: check, bind and commit not atomic against revocation or delegation changes leaves post-revocation effects.
- **CF10 redundancy.** If a trusted transition function maintains the state, history is already folded into it and `f(A_final, H, E)` and `f(A_final)` coincide. Defeat: a rule where the maintained state decides every matched pair correctly.
- **CF11 real traces.** The preprint states real LLM-agent rates are not established; prior work with real traces exists (section 6).

## 5. What the defeats share

CF1, CF2 and CF3 share one structure: **the result is determined by what the instrument is allowed to see, and the instrument was built by the claimant.** A reference defined as blind to H, scored on labels derived from H, fails where the labels need H; a divergence score fitted to a label rule predicts that rule. CF4 and CF5 are the channel-collapse and check-to-use structures from [`pre_execution_gate_counter_models_v1.md`](pre_execution_gate_counter_models_v1.md), at another site; their exits are the same (an independent channel, deny on silence, an effect bound to the checked version with atomic compare and act). The preprint's separation of a trusted transition function from the proposing model is the right instinct; it is also what makes the augmentation counter-model easy, since a state holding principal, mandate, delegation, effect ceiling and validity with a trusted transition function is already a final state that includes history statistics. The open question is how large the extra statistic must be.

## 6. Prior work

Nine arXiv preprints were read in part (abstract, introduction, grep hits and cited sections; appendices mostly not):
- **2609.08062v2** (30 Sep 2026), *ResidualAuth: What Authorization State Must Agent Systems Preserve under Revocable Delegation?* States the matched-pair formulation (identical current permissions and reachability, opposite decisions after the same revocation), defines a residual authorization state by Myhill–Nerode equivalence, proves exponentially many residual states can share one transitive closure, and runs a paired benchmark. Its text calls its core "a standard Myhill–Nerode instantiation." My T1 uses the same method at toy scale and is not independent of it.
- **2609.01836v1** (1 Sep 2026), *Agent Memory Is a Surface for Endogenous Authorization Laundering.* Matched authorized/unauthorized pairs under a hidden deterministic ledger; up to 50.2% false authority for unauthorized requests under incremental memory updates; safeguards cut laundering and reject more legitimate actions.
- **2609.33910v1** (27 Sep 2026), *When Consent Outlives Context: Residual Authority Replay in Long-Lived Agents.* Approvals persist beyond their context in eight production coding agents; attack success up to 35.1 percentage points higher than with a fresh authorization state.
- **2609.02866v1** (2 Sep 2026), *When Does Authorization End? Effect Closure at Provider Boundaries.* Version-binding and revocation-to-effect gaps in GitHub, Kubernetes, NATS and Kafka.
- **2608.21159v1**, *AID-Guard: Stateful Authorization for Delegated Agent Effects.* Revalidation at commit; a strict exact-manifest profile reduced benign utility by 35.4 to 43.8 percentage points.
- **2609.21284v1**, *Authorization Revocation for Long-Running AI Agents: Root-Scoped Quiescence under Delegation and Asynchronous Execution.* Epoch fences and certificates.
- **2609.31301v1**, *Beyond Approved Actions: Runtime Validation of Persistent Outcomes in Agent Workflows.* Effect comparison against what was approved for the current state.
- **2609.28586v1**, *Agent Approval Laundering: Transitive Effects Beyond the Approved Invocation.* An information limit: if executions with identical policy-visible fields require different effect-specific decisions, no record-only policy can guarantee both.
- **2609.15906v1**, *Authorization Architectures for Tool-Using AI Agents* (a review). Names task-aware revalidation as an unresolved requirement.

A string search of all nine for the preprint's score names ("decision freshness", "authority-state divergence", "survivab*") found none; the transition classes were not searched. This does not show the preprint's own elements are absent elsewhere. Whether the preprint cites any of these is unknown.

## 7. Review passes

- **Same-family pass** (a fresh instance, brief and toys only). Found the dead argument in T4, the hard-coded bound in T5, the history counter in T1 rule A's naive state, the tautology in T2, and the missing fixed-weights and elapsed-plus-count controls in T3 (common-cause leakage through elapsed time). It disclosed reading the toys before writing its first step. Its recalled prior work (security automata, history-based access control, execution-history access control, usage control, consistency-token authorization, fail-safe defaults) is unverified recall by the same model family.
- **Different-family pass** (supplied as text; its run is as reported by that reviewer and was not reproduced). Agreed on the dead argument, the tautology, the learned-not-defined score and the stipulated bound; supplied the CF1 wording split (finite-dimensional, finite-state, bounded-range, bounded-memory) and CF8's replay and freshness. Missed the history counter in T1, the common-cause leakage and the delivery-latency gap. It reported no prediction mismatches, which is expected when predictions come from reading the code.
- **Protocol defect.** Both passes saw `toys.py`, so predictions were code-derivable. A stronger pass withholds the code until predictions are filed. The brief given to the reviewers is preserved at [`authorization_trajectory_blind_pass_v1/`](authorization_trajectory_blind_pass_v1/).

## 8. What a trajectory-dependent authorization claim needs

1. A stated kind of bound on the extra statistic, and an exhibited rule for which no bounded augmentation reproduces the history-aware answer, or an argument that the engineering barrier is real (CF1).
2. Benchmark labels from an independent source, the label-from-history fraction reported, and real agent traces before any sentence about rates (CF2, CF11).
3. Weights and distance fixed before evaluation, an unweighted change-count baseline and an elapsed-plus-count baseline, and a held-out generator that does not share a common cause (CF3).
4. The producer of events and evidence named and independent of the agent, a default of deny on silence, a delivery bound, and replay and freshness protection (CF4, CF7, CF8).
5. The effect bound to the checked version with an atomic compare-and-act and an effector that honors it (CF5, CF9).
6. A false-denial rate beside every false-continuation rate, with "benign" defined without presupposing the relevant dimension (CF5).
7. Operational definitions for each named property ("survivability" and its four parts), or the property is a label.
8. The prior work in section 6 positioned.

## 9. What this does not establish

The preprint's full text was not read, so none of this is a finding about its experiments, only about the claim forms as summarized. The benchmark was not available; nothing here touches its own numbers, and the preprint's 51.1% is neither reproduced nor refuted. Toys T2, T4 and the atomic row of T5 are determined by construction. T1's class counts are lower bounds (suffix length equals prefix length), each toy ran with one seed, and the toy rules are far simpler than a delegation graph, where the cited work shows the required statistic can be exponential in delegation redundancy. Both review passes are same-source in the sense that the brief and code came from one family. The claim that trajectory matters to authorization in some rules is plausible and is not what is tested; what is tested is whether the headline and the "final-state insufficiency" framing survive the representation and circularity attacks. A narrower reading survives: trajectory information can matter, history is not shown to be irreducible, benchmark error rates can be artifacts of label prevalence, learned divergence metrics can fail under generator shift, a trusted transition function needs an independent event channel, and revalidation alone does not close a check-to-use race.

## What would show this paper wrong

A reader who supplies the benchmark's labels and finds they come from an independent source and survive a hand-set-p check; a rule shown to have an unbounded statistic that engineering cannot bound; the preprint's divergence score, fixed in advance, beating an unweighted change count on a generator it was not tuned on; or a published statement of the preprint's score or transition classes that predates it.

## References

Sources for the preprint's statistics (10,000 scenarios, 5,000 matched pairs, 51.1%, 0) and for its formulas: the preprint's own summary page, *Authorization State and Trajectory in Persistent AI Agents: Testing Final-State Sufficiency*, self-published October 2026 (screenshot and a summary note; full text not read; link available on request). Sources for the numbers in section 6, each from the paper's own abstract or text as read in part:

- arXiv:2609.08062v2, *ResidualAuth: What Authorization State Must Agent Systems Preserve under Revocable Delegation?* https://arxiv.org/abs/2609.08062
- arXiv:2609.01836v1, *Agent Memory Is a Surface for Endogenous Authorization Laundering.* https://arxiv.org/abs/2609.01836
- arXiv:2609.33910v1, *When Consent Outlives Context: Residual Authority Replay in Long-Lived Agents.* https://arxiv.org/abs/2609.33910
- arXiv:2609.02866v1, *When Does Authorization End? Effect Closure at Provider Boundaries.* https://arxiv.org/abs/2609.02866
- arXiv:2608.21159v1, *AID-Guard: Stateful Authorization for Delegated Agent Effects.* https://arxiv.org/abs/2608.21159
- arXiv:2609.21284v1, *Authorization Revocation for Long-Running AI Agents: Root-Scoped Quiescence under Delegation and Asynchronous Execution.* https://arxiv.org/abs/2609.21284
- arXiv:2609.31301v1, *Beyond Approved Actions: Runtime Validation of Persistent Outcomes in Agent Workflows.* https://arxiv.org/abs/2609.31301
- arXiv:2609.28586v1, *Agent Approval Laundering: Transitive Effects Beyond the Approved Invocation.* https://arxiv.org/abs/2609.28586
- arXiv:2609.15906v1, *Authorization Architectures for Tool-Using AI Agents.* https://arxiv.org/abs/2609.15906
- Companion papers in this repository: [`pre_execution_gate_counter_models_v1.md`](pre_execution_gate_counter_models_v1.md) (channel-collapse and check-to-use requirements).
