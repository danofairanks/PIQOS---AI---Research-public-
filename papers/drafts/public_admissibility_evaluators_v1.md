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
9. The family also does several things carefully, credited in section 3: it states the public/production boundary, preserves failed predecessor examinations, and ships an example whose sink intentionally accepts the release after revocation.

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

The family poses a test: force a defeated-authority path to a covered consequence and see whether it still fires. The reference example does this and reports a pass; the check above reproduces its pass (a revoked NDA described as "revoked" is withheld). Two variants, within the example's own structure, do not pass. First, the defeat is read from wording: the same defeat stated in other words, or recorded only in the authority field the evaluator itself reads, fires. Second, the guard evaluates and then acts; a defeat that lands in between fires. The example's README names the second gap as one a downstream executor can create; the guard shipped beside it has the same gap between its evaluation and its effect. Neither variant is a claim about the private runtime.

### 5a. Are the defeat conditions achievable? A registry-bound counter-model

A defeat condition that nothing could satisfy would be unfair. To test fairness, `b1_registry_bound_guard.js` implements a deliberately small counter-model (a toy, not a product): the host supplies only a standing identifier, an action and a packet identifier; the evaluator reads the registry itself and signs a receipt (Ed25519 over packet, action, standing, registry revision, decision, expiry and a nonce); the guard verifies signature, binding, expiry and single use, then starts the effect through a compare-and-swap on the registry revision, so the check and the start of the effect are one synchronous step. Effects are closures the host can name but not supply. Predictions and design were written before the toy.

Results, each with a control: with the defeat recorded in the registry, the effect is withheld whatever the host text says; host text has no influence either way ("ended", "terminated", "has not been revoked" and even "revoked" with the registry active all allow, which is the design's cost: a host cannot report a defeat, it must be recorded in the registry); a host flag is not an input; a revocation after evaluation and before the effect gives zero effects, and so does revoke-then-restore (the receipt's revision is stale); forged, tampered, mis-bound, expired and replayed receipts are all rejected. The same four defeat inputs fire on the public reference guard. Mutation checks keep the attacks honest: with the compare-and-swap, the signature check or the nonce check removed, the corresponding attack fires. A first run of the mutation checks was vacuous because of a harness bug (flags passed in the wrong shape); it was fixed and rerun before the reported results.

Residuals that still succeed, stated as limits of the design: a holder of the signing key mints an accepted receipt; a registry that says active while the world is revoked is trusted; a caller holding a reference to the effect function calls it directly with or without revocation (exclusivity is placement, not code); and a revocation after the effect has started is not stopped. The counter-model says the defeat conditions can be met by moving the decisive input out of the host's channel and placing the check at the effect; it says nothing about whether the private runtime does.

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

## 6. Reading across

The same classes as in [`pre_execution_gate_counter_models_v1.md`](pre_execution_gate_counter_models_v1.md) and [`model_local_proofs_travel_v1.md`](model_local_proofs_travel_v1.md) recur. The decision rests on values the host supplies (packet claims, observations, evidence, flags, the clock and the freshness window), so the check runs on a channel the governed side produces: the self-supplied-label class. Contradiction is detected by listed words, so standing that ends in an unlisted word is invisible: the surface-text class. The receipt hash is integrity, not authenticity: the hash-as-receipt class. The evaluate-then-act gap is the check-and-act class. Two endpoint files that return constants show the other end of the same range: a response shape with nothing behind it. What distinguishes this family from the earlier specimens is the amount of careful scoping language around reference code; the result stays that a public packet can show how the reference responds to the packets it is given, not that the standing was real.

## 7. What this does not establish, and reproduction

- Nothing here is a statement about the private runtime, about any production deployment, or about the repositories' authors' intent or competence. The public files describe themselves as reference and sanitized.
- The preserved V114 examination (a constituted synthetic executor) was not run: it cannot be run from the public repository. Its recorded result is neither confirmed nor refuted here.
- The Temporal Standing Test protocol page and the site were not examined; this paper does not assess them.
- The attack suite is same-source; a second reader is owed. A control scan of unrelated authorization libraries, to estimate how often these classes appear elsewhere, was not run.
- Counts are about the pinned commits; later commits may change the behavior, which would be a fix, not a refutation.

**What would show this paper wrong.** The companion harness failing at the pinned commits; a quoted line that does not appear at the stated path and line; or a later commit that changes the stated behavior.

**Reproduce.** `python3 run_all.py` in [`public_admissibility_evaluators_v1/`](public_admissibility_evaluators_v1/) clones the pinned commits into a work directory, runs one Node script and prints PASS or FAIL for 29 qualitative checks (a few seconds; needs git, network, Node 22 or newer and Python 3.10 or newer).

## References

[1] The repositories and pinned commits in section 2; each statement quoted in section 3 is cited with its path and line.

[2] Counter-models for pre-execution authority-gate claims: [`pre_execution_gate_counter_models_v1.md`](pre_execution_gate_counter_models_v1.md).

[3] When a model-local proof travels: [`model_local_proofs_travel_v1.md`](model_local_proofs_travel_v1.md).

[4] The channel-collapse result: [`execution_gate_channel_collapse_v1.md`](../published/execution_gate_channel_collapse_v1.md).

Sources are cited at the tier read: exact clones for repository files.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
