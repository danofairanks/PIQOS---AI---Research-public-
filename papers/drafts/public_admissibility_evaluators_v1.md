# What a Public Admissibility Evaluator Can Show: Self-Declared Fields, Lexical Contradiction and the Defeated-Authority Path Across Eight Public Repositories

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** Repositories are named by their public paths because the paper's subject is what those files say and do. No individual or organization is named: account handles appear only inside repository paths, and no intent is attributed to anyone. Everything stated is about the pinned commits in section 2; repositories change.
Internal evidence exists and is available to serious inquiries at proof time.
Not a warning about any specific party; it reports patterns.

**Disclosure.** Drafted with AI assistance. The attack scripts and their predictions were written by the same model that drafted this paper, so the results are a same-source check, not independent verification. Findings are reproducible: the companion harness clones the pinned commits and checks every result (section 7).

## 1. Summary

A family of eight public repositories presents "runtime admissibility" governance: a check, asked immediately before a consequence, whether standing established earlier still survives. The repositories state plainly that the public material is a reference or a sanitized surface and that the production runtime is private. This paper takes the public material at its word and asks the question the family itself poses: if authority is defeated, does a covered consequence still fire? The check is run on the public reference evaluator and its example guard, on a second evaluator, on two endpoint files and on one scoring function. Headline results, each with a control:

1. Where the standing is stated in words the evaluator lists ("revoked", "expired" and a few others), it blocks. Where the same standing ends in other words ("terminated", "ended", "withdrawn", "no longer in force", "lapsed", "cancelled", "rescinded", "superseded") the reference evaluator returns stable, admissible, allow.
2. The reference evaluator reads an authority revoked flag and an expiry, and records both, but they change only a secondary continuity block. A packet with the revoked flag set and an expiry in the past returns stable, admissible, allow at the top level, and the example guard, which checks the top-level fields, executes the effect.
3. Revocation recorded after the evaluation returns and before the effect runs is not seen (no recheck): the effect ran with the registry showing revoked at that moment. A revocation before the evaluation is withheld.
4. The receipt's hash is reproducible from the receipt by anyone; a forged stable/allow receipt with a recomputed hash is accepted by the example guard, which says in its first line that production receipt verification belongs elsewhere.
5. The fields the decision rests on are supplied by the host: a packet whose required fields all contain the string "x" is stable/allow, an empty string or a zero counts as evidence, and the host chooses the freshness window (omitted or zero disables it).
6. A second evaluator treats status values outside a four-item list as admissible and treats unparseable expiry and verification timestamps as current. Two other repositories' `api/evaluate.js` files return constant responses (one returns ALLOW for any input, including a revoked-authority packet and an empty body). One scoring function admits an identity vector with one dimension at 60 of 100.
7. The defeat conditions used here are achievable. A small counter-model that reads the standing from a registry it controls (the host supplies only a standing identifier and an action), signs its receipt, and runs the effect through a compare-and-swap on the registry revision holds all four defeat inputs that the public reference guard fails, and each of its checks fails when the corresponding mechanism is removed. It also has stated residuals (section 5a).
8. A matrix of defeat form against timing over five guard variants shows where each defence helps (section 5b): a re-evaluation before the effect closes nothing the first evaluation did not, only the registry-bound variant holds every form before the effect starts, and no variant stops a defeat after the effect has started.
9. None of the defeat shapes used here is new, and neither is the counter-model's mechanism (section 3a). The family's own frozen executor examination lists six unauthorized paths, its landing-page schema is a relabelling of older ideas (dataset shift; time-of-check to time-of-use), and this project's own axiom paper published the same attack shapes before this run. What this paper adds is an executed run of them against the public reference artifacts, the authority-flag, self-declared-field, constant-endpoint and scoring-function findings, and the form-by-timing matrix.
10. An independent executor toy built only from the family's published freeze text blocks all six of its listed unauthorized paths, which supports the property class (not their implementation, which cannot be run here). Replay inside the validity window, replay across executors and a refusal recorded after minting are not among the six and fire until a nonce, an audience and a revocation epoch are added; binding the exact payload bytes does not close a parse differential between the decision and the effect (section 5c).
11. Semantic shuffling defeats a wording-based check in both directions: standing that ends in other words, a perturbed or translated listed word, a split word and a role swap all pass, while a mention, a negation and a future tense are blocked. A registry-bound design inherits the problem at its status vocabulary unless it is an allow-list with default deny. The bubble test does not measure this (section 5d).
12. Survival is relative, not absolute (Appendix A). In a finite model, a gate with utility that survives a declared set of defeat scenarios exists exactly when the gate's observations separate the authorized scenarios from the defeat scenarios; no gate with utility survives a defeat family that is closed under mimicry or under adding an unmediated path; and survival holds only relative to channels the adversary cannot write. The claim that no governance survives is therefore false as a universal and true only in those open-world and empty-trust-base forms. The result is true by construction and classifies the defeat conditions of this paper into three failures; it does not discover them.
13. The family also does several things carefully, credited in section 3: it states the public/production boundary, preserves failed predecessor examinations, and ships an example whose sink intentionally accepts the release after revocation.

## 2. Objects and sources

All pinned commits were cloned read-only; results are about these commits. Full hashes are in the companion `PINS.txt`.

| Repository | Pinned commit (author date) | Role in this paper |
|---|---|---|
| github.com/zlomke76-del/harmonic-public | 7fe1597 (2026-10-03) | reference evaluator, example guard, preserved evidence; attacked |
| github.com/zlomke76-del/runtime-admissibility-core-public | 9305b82 (2026-05-26) | second evaluator; attacked |
| github.com/zlomke76-del/authority-continuity-primitive-public | 95ee54d (2026-05-26) | endpoint file; called |
| github.com/zlomke76-del/consequence-boundary-public | a6ee5f8 (2026-05-26) | endpoint file; called |
| github.com/zlomke76-del/solaceframe-public | c6bb260 (2026-05-26) | render-continuity tooling; one admission function called |
| github.com/zlomke76-del/solace-kernel-public | d65084a (2026-05-26) | static web surface; listed |
| github.com/zlomke76-del/solace-public | 9fafc0b (2026-05-26) | static web surface; listed |
| github.com/zlomke76-del/solaceveil-public | 249a61f (2026-09-24) | static web surface; listed |

The repositories' own checks pass at these commits (the reference repository's vector test, its ten guard tests, its evidence verifiers and its example run), with one exception recorded in section 4.

## 3. What the repositories say about themselves, and what they get right

- The reference repository's boundary file says the repository is not "the sovereign production Harmonic runtime source tree" (`V4_PUBLIC_BOUNDARY.md`), and its landing page says "Historical validity receives no automatic persistence" and that determination of standing is separate from downstream enforcement (`index.html`, line 16).
- The example guard's first line says "Production receipt verification belongs in its own adapter" (`examples/raw-vs-governed/guard.js`, line 1), and the example's README says "The HTTP sink intentionally accepts a release even after revocation, exposing the gap a downstream executor can create" (`examples/raw-vs-governed/README.md`, lines 71 and 72).
- The preserved lineage keeps a failed positive control and a failed first successor where they landed, and states what each does not establish (`README.md`, the lineage and "What this does not establish" sections). That is the practice this series credits.
- The preserved V114 test says it is "not a runnable public-repo test" because its import targets a private location (`evidence/examinations/v114-execution-boundary/README.md`, line 15). The sanitized sibling repository says it is "intentionally sanitized for public release" (`solaceframe-public`, `README.md`, line 15).

These statements bound what a reader can conclude from the public files. The checks below stay inside them: they test the public evaluators, not the private runtime.

### 3a. Prior art, and the defeat conditions already published

**Citations in the repositories.** A text search of all eight repositories for citation markers (arXiv, DOI, "prior art", "related work", "references") and for named earlier work (time-of-check, Zanzibar, "new enemy", macaroons, Clark-Wilson, Lamport, Bell-LaPadula, Biba, linearizability) finds nothing in the reference repository and no reference or bibliography section in any repository. The example's README describes itself as inspired by earlier scenarios without naming them. The vocabulary (Temporal Standing, T₀ → ΔN → Tₙ, PERMITTED/CONSTRAINED/ESCALATED/REFUSED, the examination identifiers) is the family's own, and the lineage it credits is its collaborators, not literature.

**The family's own published defeat conditions.** The frozen V114 examination lists six unauthorized paths that defeat its property: direct external execution with no receipt, a forged permit receipt, mutation of the payload after a valid receipt is minted, replay or use of an expired receipt, a governance refusal that still produces the consequence, and absence of persisted governance evidence that still produces the consequence (`evidence/examinations/v114-execution-boundary/V114_FREEZE.md`, lines 16 to 21). It names the implementation under test as a signed short-lived execution receipt with exact `execute_hash` binding and executor-side verification (same file, lines 41 to 44), and its scope note says a deployment-wide claim "requires an architecture-specific inventory of every effect-capable route" (line 37). The V113 record pairs a standing-preserving change (ΔN1) with a standing-defeating one (ΔN2) (`evidence/examinations/v113-complete-information-successor/V113_ADJUDICATION.md`, lines 23 and 38), and the BS-003 to BS-005 lineage preserves positive controls, a negative after one controlled transition, and precommitted falsifiers (`README.md`). A public screening protocol by the same author (read as a screenshot and its attached one-page PDF; no permalink; not in the repository; weak tier) adds paired changes in both orders, a frozen last point of unilateral reversibility, and a requirement that the same identified action be followed to the consequence boundary.

**Overlap with this paper.**

| This paper | The family's published condition |
|---|---|
| forged, tampered, expired and replayed receipts (section 4, 5a) | V114 paths 2, 3 and 4 (their constituted executor signs and verifies; the public reference guard does not, as its first line says) |
| the registry-bound counter-model (5a) | the V114 implementation class: signed short-lived receipt, payload binding, executor-side verification. The counter-model re-derives the class from the published description; it is not offered as new |
| a defeat between evaluation and effect (section 4, 5b) | the screening protocol's staleness between approval and execution; V114 covers it only as receipt expiry |
| a defeat after the effect has started (5b) | the protocol's last point of unilateral reversibility |
| a direct call to the effect function (5a residual) | V114 path 1, tested against an executor boundary that demands a receipt |
| authority flag ignored at the top level, self-declared completeness, constant endpoints, the scoring function | not among the published conditions |

**Older and external prior art for the same shapes.** The schema T₀ → ΔN → Tₙ relabels an older idea: a rule validated under the conditions of one time and applied under different conditions later. This project's axiom paper records that provenance (dataset shift [9][10]; time-of-check to time-of-use) and ran three attacks on its own toy (a divergent read path, cadence-throttled revalidation, and a time-of-check to time-of-use race with examiner-chosen timing) before this run [11]. The check-and-act race is the subject of Bishop and Dilger [6]; stale authorization after a removal is the "new enemy" problem Zanzibar addresses with a consistency token [7]; a monotonically increasing token that the effect side checks is the fencing-token pattern [8]. None of these is cited by the family, and whether its authors knew them is not shown.

## 4. The attacks

Each attack has a control that must read clean. Predictions were written before the run; one missed (a vector miscalculated in the prediction, noted). The reference repository's own tests pass first; the preserved V114 test cannot run: it exits with `Cannot find module '../api/secure-execution'`, and that file is not in `api/`, as its README discloses.

| Target | Result |
|---|---|
| lexical contradiction (reference evaluator) | The evaluator blocks when claims contain a listed stable word and observations contain a listed unstable word. Eight paraphrases of the standing ending, none containing a listed word, return stable/allow; "revoked" blocks. "has not been revoked" blocks (a false positive in the fail-closed direction). Claims that contain no listed stable word ("NDA is in place") with an observation "NDA revoked" return stable/allow; with "valid" in the claim they block |
| host-chosen inputs | A basis 200 minutes old with a freshness window of 1 is flagged and degrades; with the window omitted or set to 0 it is not flagged. A packet whose required fields are all "x" is stable/allow. With no observations, evidence of `[""]` or `[0]` satisfies the reality-coupling check; with no evidence it degrades |
| authority flags | A complete packet with `authority.revoked: true` and an `expires_at` in the past returns stable/admissible/allow; the continuity block records revoked, expired, survivability "fragile" and escalation required (pressure 77). The repository's own example sets the revoked flag together with an observation that contains "revoked": its deny comes from the word, not the flag |
| guard and receipt | Over real HTTP against the repository's handler, the guard executed the effect for the revoked-flag packet. A revocation made after the evaluation returned and before the effect ran was not caught (the effect saw the registry revoked); revoking before the evaluation was withheld. The receipt's artifact hash (a SHA-256 of the stable-serialized packet and result) recomputes from the receipt; a forged stable/allow receipt with a recomputed hash was accepted, a wrong packet identifier and a `public_release: false` receipt were rejected |
| second evaluator | An authority status of terminated or withdrawn, or a runtime signal saying terminated, is admissible; a revoked status and a signal saying revoked are inadmissible. An unparseable `expires_at` value (the word tomorrow) is treated as not expired; an unparseable verification time is treated as not stale (the reference evaluator flags an unparseable verification time) |
| two endpoint files | `authority-continuity-primitive-public/api/evaluate.js` returns `ALLOW / VALID / RECOMPUTED` for a revoked-authority packet and for an empty body; `consequence-boundary-public/api/evaluate.js` returns the same "observe / requires_runtime_validation" for any input |
| one scoring function | `computeAdmission` in `solaceframe-public` admits a vector of seven 100s and one 60 (mean 95), returns "review" for one 59, and "rejected" for one 0 (the prediction said "review"; the mean, 87.5, is below the review threshold) |
| three static surfaces | `solace-kernel-public`, `solace-public` and `solaceveil-public` contain `app/layout.tsx` and `app/page.tsx` and no evaluator, kernel or `api/` directory, matching their README exclusion lists |

## 5. The defeated-authority path

The reference repository's landing page says the evaluator assesses whether standing established at T₀ still survives a material change ΔN for the exact consequence at Tₙ (`index.html`, line 16), and its example turns that into a test: force a defeated-authority path to a covered consequence and see whether it still fires. The example reports a pass; the check above reproduces its pass (a revoked NDA described as "revoked" is withheld). Two variants, within the example's own structure, do not pass. First, the defeat is read from wording: the same defeat stated in other words, or recorded only in the authority field the evaluator itself reads, fires. Second, the guard evaluates and then acts; a defeat that lands in between fires. The example's README names the second gap as one a downstream executor can create; the guard shipped beside it has the same gap between its evaluation and its effect. Neither variant is a claim about the private runtime.

### 5a. Are the defeat conditions achievable? A registry-bound counter-model

A defeat condition that nothing could satisfy would be unfair. To test fairness, `b1_registry_bound_guard.js` implements a deliberately small counter-model (a toy, not a product): the host supplies only a standing identifier, an action and a packet identifier; the evaluator reads the registry itself and signs a receipt (Ed25519 over packet, action, standing, registry revision, decision, expiry and a nonce); the guard verifies signature, binding, expiry and single use, then starts the effect through a compare-and-swap on the registry revision, so the check and the start of the effect are one synchronous step. Effects are closures the host can name but not supply. Predictions and design were written before the toy.

Results, each with a control: with the defeat recorded in the registry, the effect is withheld whatever the host text says; host text has no influence either way ("ended", "terminated", "has not been revoked" and even "revoked" with the registry active all allow, which is the design's cost: a host cannot report a defeat, it must be recorded in the registry); a host flag is not an input; a revocation after evaluation and before the effect gives zero effects, and so does revoke-then-restore (the receipt's revision is stale); forged, tampered, mis-bound, expired and replayed receipts are all rejected. The same four defeat inputs fire on the public reference guard. Mutation checks keep the attacks honest: with the compare-and-swap, the signature check or the nonce check removed, the corresponding attack fires. A first run of the mutation checks was vacuous because of a harness bug (flags passed in the wrong shape); it was fixed and rerun before the reported results.

Residuals that still succeed, stated as limits of the design: a holder of the signing key mints an accepted receipt; a registry that says active while the world is revoked is trusted; a caller holding a reference to the effect function calls it directly with or without revocation (exclusivity is placement, not code); and a revocation after the effect has started is not stopped. The counter-model says the defeat conditions can be met by moving the decisive input out of the host's channel and placing the check at the effect; it says nothing about whether the private runtime does. The mechanism is the class the family's frozen executor examination describes (section 3a), re-derived here from that description, and the compare-and-swap on a revision is the fencing-token pattern [8].

### 5b. Defeat form against timing against guard

`b3_defeat_matrix.js` crosses four defeat forms (a listed word in the observation, an unlisted wording, an authority flag only, and a registry change the host never reads), three timings (before the first evaluation, after the last check and before the effect starts, and after the effect has started; a fourth, between an evaluation and a recheck, applies to one guard) and five guards: the public reference guard, the same guard with one re-evaluation immediately before the effect (a common patch, built from two nested calls of the real guard), the registry-bound counter-model, the same counter-model with its compare-and-swap removed, and a guard over the constant endpoint file. A cell reads "fires" if the covered effect starts after the defeat. All 60 preregistered cells matched.

| Guard | Before evaluation | Between evaluation and recheck | After last check, before effect | After effect starts |
|---|---|---|---|---|
| public reference guard | listed word held; the other three forms fire | n/a | all fire | all fire |
| public guard plus recheck | listed word held; the other three fire | listed word held; the other three fire | all fire | all fire |
| registry-bound with compare-and-swap | all held | n/a | all held | all fire |
| registry-bound, compare-and-swap removed | all held | n/a | all fire | all fire |
| guard over the constant endpoint | all fire | n/a | all fire | all fire |

Reading: only the registry-bound variant with the compare-and-swap holds every form both before the evaluation and in the gap before the effect starts; the recheck patch changes nothing the first evaluation did not already catch and leaves the gap open; no variant closes the last column, because a defeat after the effect has started is outside any check made before it (irreversibility is a separate property, which the family's boundary files also separate). The forms were chosen to line up with the evaluator's listed words, so the matrix shows the structure; it does not discover new blind spots, and the public-guard host is modelled as an honest reporter in the wording of each form.

### 5c. An executor built from the published freeze text

The frozen executor examination cannot be run here (section 4), but its property and six paths are published (section 3a). `b2_constituted_executor.js` builds an independent toy from that text alone and attacks it. The baseline has the five features the freeze text names: an Ed25519-signed short-lived receipt, exact payload-hash binding, a governance-evidence prerequisite at minting, a refusal stop, and executor-side verification. A hardened variant adds a one-time nonce, an executor audience in the receipt and a revocation epoch checked by compare-and-swap at the start of the effect. Predictions were written before the toy. This tests the property class from the published description; it does not test the private implementation.

Results (consequences produced, with controls): the six listed paths (no receipt, a forged receipt, a payload changed after minting, an expired receipt, a refusal including a tampered decision, and no persisted evidence including a faulty mint with a fabricated identifier) produce none on either variant. Outside the six: replay inside the validity window gives 2 consequences on the baseline and 1 on the hardened variant; replay across two executors, 2 and 1; a refusal recorded after minting and before expiry produces the consequence on the baseline and not on the hardened variant; reusing a receipt for another action is blocked when the action is inside the hashed bytes and fires when it is not. Removing any single check makes its attack fire. The residuals fire on both variants: a holder of the signing key, a direct call to the consequence function, an executor whose clock is behind real time, and a refusal after the effect has started.

One prediction missed. A payload with a duplicate key (`{"amount":10,"amount":1000000}`) was read by the decision layer as amount 10 and by the effect layer as amount 1000000. I predicted that binding the exact bytes would block it; it does not, because the decision was made on a different parse of the same bytes. Binding the parsed form fires too, and only a shared strict parse (here, rejecting duplicate keys) blocked it. The point generalizes: binding must cover the value the decision evaluated, not only the bytes executed.

Reading: the property class in the freeze text is achievable for its six listed paths, which credits the family's design description. The listed paths are a subset of what the class needs, as the freeze text's own non-claim says (a deployment claim needs an inventory of every effect-capable route); replay, audience, refusal after minting and the parse differential are the next entries on that inventory.

### 5d. Semantic shuffling

Two kinds of shuffle matter for a check that turns text into a decision: the meaning is kept while the surface changes, and the surface is kept while the meaning changes. `semantic_shuffle_probes.js` probes the reference evaluator (claims say the agreement is valid; the control `revoked` blocks and `remains valid` allows). Predictions were written before the script and all matched.

Evaded (stable, allow): rewording (`no longer valid`, `has ceased to be effective`, `is void`); the listed word perturbed (a Cyrillic letter, a zero-width character, fullwidth letters); translation (French, German); the word split across two statements; and a role swap in which the claims say revoked and the observation says valid. Blocked as false positives: a mention of the word in a description of a slide deck, a negation (`not revoked and not terminated`) and a future tense (`will be revoked tomorrow`). Permuting the order of the observations changes nothing. A lexical check therefore breaks both invariances.

The registry-bound counter-model of section 5a is not immune one layer out. A registry that stores a status string needs a rule for turning the string into a decision, and three rules were tried. An allow-list with exact match and default deny held: only `active` allowed, and even `ACTIVE` was denied. A deny-list allowed every unlisted word and most perturbations (`terminated`, `withdrawn`, `lapsed`, a Cyrillic variant of `revoked`, and `ACTIVE`; with lower-casing and trimming it also denied `Revoked ` with a trailing space, but still allowed the rest). The bubble test of section 6 does not measure this: a gate can pass it and still be defeated at its vocabulary.

The duplicate-key parse differential of section 5c is the same species: two layers read the same bytes differently. The requirements that follow are the same in both places: state vocabularies as default-deny allow-lists, no decisive input carried as free text, and one canonical form (or one strict parse) consumed by both the decision and the effect. A language-model judge in place of the word list changes the failure mode rather than removing it (it is the probabilistic scorer that [`pre_execution_gate_counter_models_v1.md`](pre_execution_gate_counter_models_v1.md) treats separately), and was not tested here.

## 6. Reading across

The same classes as in [`pre_execution_gate_counter_models_v1.md`](pre_execution_gate_counter_models_v1.md) and [`model_local_proofs_travel_v1.md`](model_local_proofs_travel_v1.md) recur. The decision rests on values the host supplies (packet claims, observations, evidence, flags, the clock and the freshness window), so the check runs on a channel the governed side produces: the self-supplied-label class. Contradiction is detected by listed words, so standing that ends in an unlisted word is invisible: the surface-text class. The receipt hash is integrity, not authenticity: the hash-as-receipt class. The evaluate-then-act gap is the check-and-act class. Two endpoint files that return constants show the other end of the same range: a response shape with nothing behind it. What distinguishes this family from the earlier specimens is the amount of careful scoping language around reference code; the result stays that a public packet can show how the reference responds to the packets it is given, not that the standing was real.

Determinism is not what makes a gate a closed bubble; the input channel is. A gate is a bubble to the degree its decisive inputs are produced inside the thing it governs: it stays repeatable and reads satisfied for anything the host phrases acceptably. A simple test holds every host-visible input fixed, changes the world state that matters, and asks whether the verdict (here, whether the effect starts) changes. Over the matrix of section 5b, excluding the in-flight timing (which fires for every guard because it is outside any pre-execution check), the effect still fires in 7 of 8 defeat cells for the public reference guard, 10 of 12 with a recheck, 8 of 8 for a guard over the constant endpoint, 4 of 8 for the registry-bound counter-model without its compare-and-swap, and 0 of 8 with it. The registry-bound counter-model stays deterministic and passes because its decisive input is the registry and its check sits at the effect. This measure was defined after the matrix was run, was not preregistered, and the forms were chosen to line up with the public evaluator's blind spots, so the public figures are close to a ceiling for that evaluator; a gate that passes can still be a bubble one layer out (a registry that says active while the world is revoked), so the size of the bubble is relative to who produces the registry.

The mechanisms are not unusual. A pilot over four widely used authorization libraries unrelated to this family (a token library, a signed-timestamp library, a policy engine and a macaroon library; pinned versions and probes in `control_scan/`) found a caller-chosen freshness window, clock or attribute reachable through documented parameters or defaults in all four, stateless replay acceptance in all three where it applies, and wildcard matching of a path-traversal string in the one library with wildcards; every tamper control was rejected. So the mechanisms alone do not separate the specimens from ordinary libraries. What separates them is the claim made about the mechanism: a primitive documents that it takes the window or the attribute from the caller, while a gate that claims to decide present standing for a consequence is read against that claim. A probe cannot measure the claim; it is read from the files (sections 3 and 3a).

## 7. What this does not establish, and reproduction

- Nothing here is a statement about the private runtime, about any production deployment, or about the repositories' authors' intent or competence. The public files describe themselves as reference and sanitized.
- The preserved V114 examination (a constituted synthetic executor) was not run: it cannot be run from the public repository. Its recorded result is neither confirmed nor refuted here.
- The Temporal Standing Test protocol page and the site were not examined; this paper does not assess them.
- The defeat shapes and the counter-model's mechanism are not new (section 3a); the contribution is the executed run on the public reference artifacts. The screening protocol cited in section 3a was read at screenshot tier and is not in the repository.
- The attack suite is same-source; a second reader is owed. The control scan is a pilot of four libraries in one language, with probes written by this paper's author from its own pattern list. A control scan of unrelated authorization libraries, to estimate how often these classes appear elsewhere, was not run.
- Scope of the conclusions. Every finding is about a public file at a pinned commit, read against that file's own statements and against the defeat conditions in the family's published V114 freeze text. None is a finding about the frozen harness proposition, about the private runtime, or about the Temporal Standing Test; where a sentence in this paper reads as reaching past the public demonstrator, the narrower reading is the intended one and the sentence is the error. The frozen harness cited in the family's checksum lists (two zips named in `FORENSIC_SHA256SUMS.txt`) is not in the public repository, so this paper cannot test it.
- Counts are about the pinned commits; later commits may change the behavior, which would be a fix, not a refutation.

**What would show this paper wrong.** The companion harness failing at the pinned commits; a quoted line that does not appear at the stated path and line; or a later commit that changes the stated behavior.

**Reproduce.** `python3 run_all.py` in [`public_admissibility_evaluators_v1/`](public_admissibility_evaluators_v1/) clones the pinned commits into a work directory, runs one Node script and prints PASS or FAIL for 39 qualitative checks (a few seconds; needs git, network, Node 22 or newer and Python 3.10 or newer).

## Appendix A. Survival in finite math

A world is a finite set of scenarios, each with a ground truth of authorized or not; P is the set of authorized scenarios and D the set of defeat scenarios. A gate sees an observation o of each scenario and permits or denies on it. The gate *survives* D if it denies every scenario in D; it has *utility* if it permits every scenario in P (the positive control). `check_separability.py` enumerates every world with at most five scenarios and three observation values (10756 worlds, every gate) and a two-channel family (34720 worlds). Statements and predictions were written before the script; there were no failures.

- **T1, separability.** A gate with survival and utility exists exactly when the observations of P and of D are disjoint sets (2428 worlds have a witness).
- **T2.** The deny-all gate always survives and has no utility, so survival alone is vacuous.
- **T3.** The permit-all gate survives only when D is empty.
- **T4, open world.** For every world with P nonempty and every gate with utility, adding one defeat scenario that mimics the observation of a positive breaks survival (53849 gate and mimic pairs). No gate with utility survives a defeat family closed under mimicry.
- **T5, trust base.** Split the observation into a part the adversary can set freely and a part it cannot forge. If the unforgeable part separates P from D, the gate that reads only that part survives every extension within the adversary's reach. If it does not, a full mimic of a positive is available and no gate with utility survives.
- **T6.** If some effect path bypasses the gate, any defeat scenario using it defeats every gate (stated; not enumerated).

Verdict on the claim that no governance survives: false as a universal, since T1 gives witnesses and the counter-models of section 5 are instances; true in two bounded forms: no gate with utility survives an open-world family (T4, T6), and survival is always relative to a trust base (T5) and a declared defeat family, with the trivial exception that an empty trust base makes the claim true.

Each defeat condition in this paper is an instance of one of three failures. The adversary writes the observation (host-supplied labels, clock and free text; a key holder). The gate's partition of observations is coarser than the separation needs (semantic shuffling, the vocabulary toy; the repair is a finer partition, an allow-list with default deny). Or the observation is sampled at the wrong time or read by two readers (check-then-act, the in-flight case, the parse differential). The time-axis section and the exit-path defeat condition of this project's axiom paper [11] correspond to the third failure and to T6 respectively. Schneider [12] answers a different question: which properties a monitor can enforce at all.

Limits: the statements are true by construction, the same class as the model-local enumerations discussed in [`model_local_proofs_travel_v1.md`](model_local_proofs_travel_v1.md); the defeat scenarios are defined as mimics, which makes T4 close to a tautology; the model has no probability, cost or adaptive adversary, and utility is only the positive control. Its value is classification, not discovery.

## Appendix B. Per-finding record

Each row is one finding with its pinned commit, the claim it is tested against, the control, and a script in [`public_admissibility_evaluators_v1/findings/`](public_admissibility_evaluators_v1/findings/) (run `node <file> <dir containing the pinned clones>`; the draft's `run_all.py` clones them). Scripts were re-run on 2026-10-03 at the pinned commits; each prints the control beside the finding.

| # | Repository at pinned commit | Claim tested | Observed | Control | Script |
|---|---|---|---|---|---|
| B1 | harmonic-public 7fe1597 | contradiction between T0 claims and Tn observations is detected | eight other wordings of the same ending return stable, admissible, allow; so does an observation that contradicts a claim lacking a listed term | the listed word "revoked" is blocked | `i1_lexical.js` |
| B2 | harmonic-public 7fe1597 | revoked or expired authority is not admissible | flags change only `runtime_continuity`; top level stays stable, admissible, allow; `guardedExecute` runs the effect | packet without the flags | `i2_authority_flags.js` |
| B3 | harmonic-public 7fe1597 | revocation after evaluation is seen by the guard | effect ran with the registry inactive at effect time | revocation before evaluation is withheld | `i3_gap_and_receipt.js` (part a) |
| B4 | harmonic-public 7fe1597 | receipt authenticity (`guard.js` line 1 states production verification belongs elsewhere) | hash recomputes from the receipt; a forged receipt executes | wrong `packet_id` and `public_release: false` are rejected | `i3_gap_and_receipt.js` (part b) |
| B5 | harmonic-public 7fe1597 | required fields establish reality coupling and freshness | evidence `""` or `0` accepted; omitted or zero `stale_after_minutes` disables staleness | empty evidence array and `stale_after_minutes` of 1 | `i4_smaller.js` |
| B6 | runtime-admissibility-core-public 9305b82 | status and timestamps establish current authority | status `terminated`, `expires_at` `"tomorrow"` and `last_verified_at` `"garbage"` are admissible | status `revoked` is inadmissible | `i4_smaller.js` (rows `rac:`) |
| B7 | authority-continuity-primitive-public 95ee54d; consequence-boundary-public a6ee5f8 | `api/evaluate.js` decides | one returns ALLOW, VALID, RECOMPUTED for a revoked packet and an empty body; the other returns a constant for any input | none possible; whether these are intended placeholders is open | `i5_stubs_and_solaceframe.js` |
| B8 | solaceframe-public c6bb260 | `computeAdmission` | one dimension at 60 of 100 is admitted (mean 95); 59 gives review; 0 gives rejected | all 100 | `i5_stubs_and_solaceframe.js` |
| B9 | harmonic-public 7fe1597 | `V114_TEST.js` runs | exit 1, `Cannot find module '../api/secure-execution'`; its README discloses the private import | none | `cd evidence/examinations/v114-execution-boundary && node V114_TEST.js` in the clone |
| B10 | frozen V114 text (harmonic-public 7fe1597) | six listed unauthorized paths | an independent toy blocks all six; replay in window, replay across executors, refusal after minting and a duplicate-key parse differential produce the consequence until a nonce, audience, revocation epoch and a shared strict parse are added | the toy's hardened variant | `b2_constituted_executor.js` |
| B11 | harmonic-public 7fe1597 | wording-based contradiction check | rewording, perturbed word, translation, split word and role swap pass; mention, negation and future tense are blocked | listed word and the blocked forms | `semantic_shuffle_probes.js` |

B1, B2, B5 and B11 are defeats of the public reference evaluator; B3 and B4 are about the example guard and are disclosed limits of it; B7 and B8 are questions about what the files are for, not defects asserted; B9 is a fact the repository discloses; B10 is a candidate extension to a frozen examination, not a retroactive falsifier of it.

## Appendix C. Reader response

A maintainer of the family replied on a public professional-network thread after reading the draft's findings and received them frozen against the pinned commits. The reply is paraphrased here, at screenshot tier (the screenshot is kept in the author's record, not in this repository). Its category-level reading of the findings:

- Credible public-reference implementation defects: lexical contradiction handling, authority revocation and expiry not propagating into the top-level disposition, and some permissive input-validation behavior. By the author's mapping: B1, B2, B5, B6, and B11 as the wording-shuffle extension of B1. The reply does not itemise, so this mapping is the author's, not the maintainer's.
- Already-disclosed limitations or non-failures: V114 public non-runnability, downstream enforcement races, and cryptographic receipt verification outside the demo adapter. Mapping: B9, B3, B4.
- Successor properties rather than retroactive falsifiers: nonce, audience, revocation epoch, replay and parse-differential cases beyond the six frozen V114 paths. Mapping: B10. This paper already states the same limit (sections 3a and 5c): B10 extends the inventory the freeze text's own non-claim calls incomplete and does not falsify the six.
- Not addressed in the reply as read: B7 and B8.
- A claim-mapping dispute where the draft moves from breaking the simplified public demonstrator to broader conclusions about the frozen harness proposition or Temporal Standing. Response: the scope paragraph in section 7 was added to say that the conclusions stop at the public demonstrator. The reply states that the frozen harness proposition has not been falsified by this submission; this paper agrees that it did not test it, and the frozen harness is not public.

The maintainer said the findings will be dispositioned individually and that any correction will be a successor version of the frozen result. Per-finding dispositions are not yet in; Appendix B will take them as they appear, recorded as given, with the date and the artifact read.

### C1. Verifiability of the frozen proposition

This is a statement about how the proposition is published, not about its truth or anyone's intent.

- A falsifier exists in principle: the family's V114 freeze text names six unauthorized paths and a pass or fail frame.
- No outside reader can run it. `V114_TEST.js` imports a private module, and the harness archives named in the family's checksum lists are not in the public repository. A falsifying result could therefore not be produced from outside whether or not one exists.
- "Not falsified by this submission" is true and uninformative here, because this submission did not run the harness.
- A proposition scoped to six listed paths can fail only on those six. The freeze text's own non-claim says a deployment claim needs an inventory of every effect-capable route, so the six are a subset. If findings beyond the six are classed as successor properties and never as falsifiers, no finding can count against the frozen result; whether that happens is open and is read from the dispositions as they arrive.
- The accurate record today is: unverifiable outside the private harness, with the boundary of what counts as a falsifier set by classification labels whose criteria were requested and not yet stated.

What would settle it: (1) the criteria for each label (pass, fail, unresolved, successor property) stated before items are classified; (2) a public run of the harness, or at least the missing V114 module, so the six-path result can be reproduced and this paper's independent toy compared against it; (3) one pre-stated condition accepted as failing the proposition that is not reclassified as a successor. Until one of these exists, this paper claims nothing about the frozen harness proposition in either direction.

## References

[1] The repositories and pinned commits in section 2; each statement quoted in section 3 is cited with its path and line.

[2] Counter-models for pre-execution authority-gate claims: [`pre_execution_gate_counter_models_v1.md`](pre_execution_gate_counter_models_v1.md).

[3] When a model-local proof travels: [`model_local_proofs_travel_v1.md`](model_local_proofs_travel_v1.md).

[4] The channel-collapse result: [`execution_gate_channel_collapse_v1.md`](../published/execution_gate_channel_collapse_v1.md).

[5] The family's frozen examination and lineage files cited in section 3a, at the pinned commit.

[6] M. Bishop and M. Dilger. Checking for race conditions in file accesses. *Computing Systems* 9(2):131–152, 1996.

[7] Pang et al. Zanzibar: Google's consistent, global authorization system. USENIX Annual Technical Conference, 2019.

[8] M. Kleppmann. How to do distributed locking. Blog post, 2016 (fencing tokens).

[9] J. G. Moreno-Torres, T. Raeder, R. Alaiz-Rodríguez, N. V. Chawla and F. Herrera. A unifying view on dataset shift in classification. *Pattern Recognition* 45:521–530, 2012.

[10] H. Shimodaira. Improving predictive inference under covariate shift by weighting the log-likelihood function. *Journal of Statistical Planning and Inference* 90:227–244, 2000.

[11] This project's axiom paper, section 12.1 (provenance of the notation) and section 12.5 (three attacks on its own toy): [`governance_binding_axiom_v2.md`](../published/governance_binding_axiom_v2.md).

[12] F. B. Schneider. Enforceable security policies. *ACM Transactions on Information and System Security* 3(1):30–50, 2000.

Sources are cited at the tier read: exact clones for repository files; for references [6] to [10] and [12], the bibliographic record found by search (the papers themselves were not read for this draft).

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
