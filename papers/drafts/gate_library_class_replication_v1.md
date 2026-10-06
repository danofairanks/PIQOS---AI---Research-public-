# Two More Gate Libraries: Replicating the Self-Supplied-Channel Class Outside the Chain

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** Repositories are named by their public paths because the subject is what those files say and do. No individual is named: authors and maintainers credited inside the repositories are not named here, and account handles appear only inside repository paths. No intent is attributed to anyone. Everything stated is about the pinned commits in section 2; repositories change. Both repositories describe themselves as limited (a bounded demonstrator; experimental, not production software), and this note says so wherever a result depends on it.
Internal evidence exists and is available to serious inquiries at proof time.
Not a warning about any specific party; it reports patterns.

**Disclosure.** Drafted with AI assistance. The predictions, probes and this text were produced by the same model, so the results are a same-source check, not independent verification. Every result is reproducible from the companion folder (section 9), including the harness errors made along the way.

**Companion to.** [`model_local_proofs_travel_v1.md`](model_local_proofs_travel_v1.md) (a chain of repositories in which a narrow proof travelled) and [`pre_execution_gate_counter_models_v1.md`](pre_execution_gate_counter_models_v1.md) (what each pre-execution gate argument needs). Neither repository here is part of that chain: nothing travels between them and it. They are read because they state pre-execution gates in public code, which lets the counter-models' item 9 ("runs against systems the author did not write, with an examiner-chosen read path and a preserved, hashed trace") be met twice.

## 1. Summary

The counter-models paper and the earlier channel-collapse result identify a class: the check runs on a channel the governed side produces or can influence. This note asks whether the class shows up in two unrelated public gate libraries, and finds it, together with three companions that the earlier work lists as separate items.

1. **A deterministic policy-reading reference implementation** (`github.com/grahamb-ai/runtime-authority-reference-implementation`) documents its limits carefully: a four-pattern extractor that "silently produces nothing" for other sentences, no identity infrastructure, currency unchecked, one active policy. What its documents do not state is the direction of failure. A prohibition ("Unauthorized roles for payment.release: intern.") is read as a grant; when an authority sentence falls outside the patterns, an action governed only by an evidence rule has no authority check at all; a role no rule names is unrestricted by a role-limit rule; an omitted `amount` skips the ceiling, the threshold-evidence rule and a delegation cap and returns ALLOW; the first of two limits applies whichever is stricter. Its stated "default refusal" and "exact monetary-boundary evaluation" hold for the cases in its evidence repository and not for these.
2. **A governance contract in a larger experimental repository** (`github.com/IAmSoThirsty/Project-AI`) lists ten binding points and "186 passed, 0 failed". The governance test files give 185 passed and 1 failed. Against the contract: a policy `{"*": {"*": True}}` passes the weakening check; a caller's context flag waives the capability token; a token passed the documented way crashes the gate before verification, so no token passes; the one-time-use store clears itself at 10,000 entries; an empty policy hash binds to nothing; the last-stage invariants read caller-set flags; a failed evidence write is logged at debug level where the contract says critical; and the "RFC 3161" time check accepts any `Date` header.
3. **The shared shape** (section 6): a self-supplied channel (flags, an amount, a role, a list of evidence names, a header); absence read as a pass (a missing input skips a check; a missing rule type removes the check); a misread that fails in the permissive direction; a control that cannot be reached; and a record that is bounded or best-effort. Each maps to an item the counter-models paper already lists (4, 5, 13, 16, 9).
4. **Both repositories are candid about being limited**, and the results do not contradict those labels. They concern the gap between the labels and a contract or evidence that states stronger guarantees, and whether the permissive direction of failure is stated.
5. **Not established**: that the context flags are weaknesses (this depends on who builds the context, which neither repository states); anything about production deployments; anything beyond two repositories.

## 2. Objects and sources

All pinned commits were cloned read-only; results are about these commits.

| Repository | Pinned commit (author date) | Role |
|---|---|---|
| github.com/grahamb-ai/runtime-authority-reference-implementation | 26893c2 (2026-08-09); code identical to ea36ac1, the commit its evidence repository pins | the reference implementation: policy parser, extractor, authority and admissibility engines, evaluator, API, 52 tests |
| github.com/grahamb-ai/runtime-authority-evidence | fef4354 (2026-08-09) | the maintainers' captured evidence and limitations document; quoted, not executed |
| github.com/IAmSoThirsty/Project-AI | 7650aa1 (2026-09-13) | an experimental governance repository; only `src/app/core` and its contract and tests were examined |

Full hashes are in the companion `PINS.txt`. Claims are quoted with path and line:

- `runtime-authority-reference-implementation/README.md:125` "default refusal where no policy rules apply to an action"; `:127` "exact monetary-boundary evaluation"; `:91` "It is intentionally bounded."
- `runtime-authority-evidence/docs/limitations_and_next_steps.md:13` "It silently produces nothing for a sentence it doesn't recognize, no error."; `:42` "Currency isn't checked".
- `Project-AI/docs/architecture/GOVERNANCE_CONTRACT.md:74` capability tokens are "short-lived (TTL ≤ 300s), one-time-use, and bound to: action type, scope list, context hash, and policy hash"; `:56` and `:60` every outcome "produces an evidence bundle" with "no silent success"; "If evidence bundle write fails, the failure is logged at CRITICAL severity"; `:83` "Stale policy hash bindings are rejected"; `:128` "Expected: **186 passed, 0 failed.**"
- `Project-AI/README_HONEST.md:11` "Many components are experimental or aspirational. This is a research project, not production software."

## 3. Method

- **Predictions fixed in writing before the probes ran** (`reference_impl/PREREG_reference_impl.md`, `project_ai/PREREG_project_ai.md`), each with controls: the repository's own tests run first (52 passed; 185 passed, 1 failed), plus control cases in each probe.
- **Result vocabulary.** *Control-holds*: the case behaves as the repository's text says. *Within-declared*: the behaviour is stated by the repository (a limitations document, a docstring, an explicit label such as "stubbed" or "lexical heuristic"). *Outside-declared*: the repository's contract or evidence states a stronger guarantee, or a consequence the documents do not state. Nothing is recorded as a defect on argument alone; every item is an observed run.
- **Misses and harness errors are kept.** One prediction missed (section 5, E1). The Project-AI probe was run four times; runs 1 to 3 hit harness errors of mine (an import path, a missing dependency, a missing caller flag, a malformed test server, a context missing a flag) and are preserved with amendments written before each rerun. Reference implementation: two executions of one script (the first printed SQL logging noise to the output stream and was rerun with logging off; no result changed).
- **Cases are runs of the real code**: the extractor and evaluator, the real FastAPI app through a test client, the real gate, registry, token service and time validator. Nothing is patched except where stated.
- Counts are exact, not sampled; the probes are deterministic apart from random token identifiers, which the comparison helper masks.

## 4. The reference implementation

The repository's own documents bound it: "intentionally bounded", "not a production deployment", no "general-purpose natural-language policy interpreter" (`README.md:27,91-95`), and a limitations document that names the silent drop, the missing authentication, currency, a dormant delegation-expiry check and a single global policy. The results line up with those disclosures; what they add is direction.

| Case | Observed | Classification |
|---|---|---|
| "Unauthorized roles for payment.release: intern." and "No authorized roles for payment.release: contractor." | each extracted as an authority grant for that role (the pattern is applied with `search`, so `authorized roles` matches inside "Unauthorized roles"); the listed role evaluates ALLOW (`extractor.py:54-56`) | outside-declared: the limitations document says unmatched sentences produce nothing; here a prohibition produces its opposite |
| Evidence sentence extracted, authority sentence phrased outside the patterns ("Only managers are authorized to release payment.release.") | the rule set holds an evidence rule only; any role, including an empty string, is ALLOW once the evidence names are listed; with a role list present the same request is REFUSE (`authority.py:58`) | outside-declared: "default refusal" holds only when no rule of any kind applies to the action |
| Role-limit rule only ("The manager may approve payment.release up to 10,000.") | an unnamed role (intern) at 10,000,000 is ALLOW | outside-declared |
| Two limit sentences for one role and action | the first in text order applies (100,000 then 10,000 → ALLOW at 50,000; reversed → ESCALATE) (`admissibility.py:66`) | outside-declared |
| `context.amount` omitted (or `null`) | the ceiling check is not produced, the threshold-evidence rule sees amount 0, and a `delegation.max_amount` of 1 is never applied: ALLOW over HTTP (`admissibility.py:89,115`) | outside-declared: "exact monetary-boundary evaluation" holds only when an amount is supplied |
| `amount` as a string or list | unhandled `TypeError` (a test client raises; a deployed server would answer 500, not observed); `true`, `-5` pass; NaN, infinity and 1e308 escalate | outside-declared |
| "up to USD 100,000" | no rule (the pattern needs the symbol before the digits); manager at 10,000,000 → ALLOW; with `$100,000` → ESCALATE. `1,5` parses as 15.0; `$2 million` as 2.0; `100k` as 100.0; `5,000.50` as 5000.0 | within-declared (silent drop); consequence unstated |
| Upload summary | counts only; three sentences with one understood → `total_rules: 1`, no list of ignored text | within-declared |
| Unauthenticated upload | replaces all rules; the earlier role gets REFUSE and a role named in the new text gets ALLOW at 10^12; an unparseable upload leaves no rules, so every action is REFUSE | within-declared (no identity infrastructure; one global policy) |
| `delegation.expires_at` in the past | ignored | within-declared (dormant, stated in code) |
| `Payment.Release`, ` payment.release` | REFUSE | control-holds (safe, brittle) |
| delegation cap above the policy limit; NaN cap; negative cap | no effect; no effect; every amount ESCALATE | control-holds (tightening only) |
| amount == limit; limit + 0.01 | ALLOW; ESCALATE | control-holds (matches the repository's evidence) |
| unknown action; role not on an existing list; authority failure | REFUSE; REFUSE; only authority checks in the record | control-holds |
| currency | 40,000 JPY passes like EUR | within-declared |

Every prediction held. The repository's own 52 tests pass at the pinned commit.

## 5. The Project-AI contract

The repository says it is experimental ("not production software"); its contract says it is "Binding", "machine-verified", and lists ten points. Of the 186 tests the contract expects to pass, 185 pass and one fails (`test_semantic_collision.py::test_mismatched_intent_in_octoreflex`: `ViolationType` has no `MISMATCHED_INTENT`). The cases below use the real gate, registry, token service and time validator with no secret environment variables set.

| Case | Observed | Classification |
|---|---|---|
| Default secrets (`capability_token.py:27`, `policy_registry.py:19`) | a policy and a capability token signed with the default strings verify without the service; no warning when the variables are unset | within-declared (dev default; "replace with Ed25519 in production") |
| Weakening check (`policy_registry.py:217`) | an explicit `{"system": {"shutdown": True}}` is rejected as weakening; `{"*": {"*": True}}` is accepted, after which `system.shutdown` and `db.delete_all` are permitted (the check looks up named actions, not the `"*"` key) | outside-declared (contract: weakening is rejected) |
| Mutating action, no token | denied "CapabilityToken required" | control-holds |
| `requires_capability_token: False` in the caller's context | executor runs (`execution_gate.py:319`); the key is read in code only, with no mention in the contract, other documents or tests | outside-declared (contract points 6 and 7) |
| `is_mutating_action: False` | executor runs; the override is in the function's docstring and a test (`degraded_mode.py:37`; `test_degraded_mode.py:27`) | within-declared as an override; the contract does not mention it |
| A service-minted token placed where the gate looks (`context["_capability_token"]`) | the gate raises `TypeError: Object of type CapabilityToken is not JSON serializable` from `MutationGovernanceBinding.create` (`mutation_binding.py:23`) before verification; the dict form fails closed; no test passes a valid token through the gate | outside-declared; **prediction missed on mechanism** (predicted a context-hash mismatch) |
| One-time-use store | a consumed token is refused; after 10,005 other tokens are consumed the clear-on-overflow (`capability_token.py:186`) resets the store and the first token verifies again within its lifetime | outside-declared (contract point 7) |
| Token with `policy_hash = ""` | verifies against any current policy hash (`capability_token.py:104`); a token with a set hash and a mismatch is refused (control) | outside-declared (contract point 8) |
| Last-stage invariants | `continuity_proof_fresh` is `ctx.get("continuity_verified", False)` at severity BLOCK (`invariant_severity.py:189`): without the flag every request is blocked, with it the request executes. The same module's other default invariants read other caller flags | outside-declared in effect: the check is self-attestation (found in calibration; not predicted) |
| `high_impact` and `human_confirmed` | the authorization evaluator denies without `human_confirmed` and allows with it (`execution_authorization.py:141`), both from the caller's dict; through the gate the high-impact request is still denied because calibration returns HUMAN_APPROVAL_REQUIRED and does not read the flag | outside-declared for the evaluator; control-holds through the gate (so no human-approved high-impact path executes) |
| Request classifier | a transfer request prefixed "explain:" passes and executes under a permissive policy; a harm-pattern request is denied | within-declared ("lexical heuristic ... MUST replace") |
| Evidence writer raises | the executor has already run, the result is returned, and the failure is logged at DEBUG (`execution_gate.py:374`) | outside-declared (contract point 5: critical, "no silent success") |
| Executor raises | the exception propagates and no bundle is recorded | outside-declared (contract point 5) |
| "RFC 3161" time check (`time_trust.py:83`) | an HTTP endpoint with only a `Date` header is accepted (outcome OK); a spoofed 2001 date yields HALT; no timestamp token is parsed | within-declared as minimal; the paper-level wording is stronger |
| Seven outcome values | present as named | control-holds |

Every prediction held except one (the token mechanism). Whether the context-flag rows are weaknesses depends on who constructs the context: if it is the governed agent's output, the flags let it waive the gate; if it is trusted integrator code, they are a design choice and the contract's wording overreaches. Neither the contract nor the code states which.

Not examined: the conversation threat-state register, the deterministic replay of the five invariants the abstract of the paper naming these components mentions, the sovereign runtime beyond the one stage the gate calls, and anything outside the core package.

## 6. What the two share, and what the earlier work already says

Mapped to [`pre_execution_gate_counter_models_v1.md`](pre_execution_gate_counter_models_v1.md), section 5, and the channel-collapse result:

| Shape | Reference implementation | Project-AI | Earlier item |
|---|---|---|---|
| The check runs on a channel the governed side supplies | role, amount and evidence names come from the request | `requires_capability_token`, `is_mutating_action`, `continuity_verified`, `human_confirmed`, `required_scope` come from the context; the time source is an HTTP header | 5 (an observation channel independent of the governed system); the channel-collapse class |
| Absence is read as a pass | omitted amount; an action with no authority rule; an unnamed role | empty policy hash; empty scope; unset flags default the invariant to a block but a set flag clears it | 5, 8 |
| A misread of the rule content fails in the permissive direction | a prohibition read as a grant; a silent drop that removes a ceiling | the weakening check misses the wildcard key | 4 (provenance and correction of rule content) |
| The control that matters cannot be reached | delegation expiry is dormant | no token can pass the gate | 1, 2 (mediation and placement) |
| The check and its record are not atomic or are best-effort | n/a (no consumption store) | clear-on-overflow store; evidence emitted after execution and swallowed on failure | 13, and the evidence-quality point in section 4a |
| A single canonical parse | the extractor reads the sentence once, differently from a human | the context hash covers the token it is meant to bind | 16 |

The mapping is a reading, not a derivation: the earlier items are requirements, and a requirement being unmet is not the same as a counter-model succeeding. What these two repositories supply is item 9's category (runs against systems the author did not write), with preserved traces, for two systems that were not built to answer the earlier work.

Two differences from the chain's repositories are worth stating. First, both repositories here document their limits more fully than most of the chain, and the results mostly fall inside those limits as the lower rows of each table show; the findings are the direction of failure and the contract rows. Second, neither claims a proof: the reference implementation claims demonstrations and the Project-AI contract claims machine verification by its own tests, so the earlier "model-local proof" language does not apply and "same-side evidence" does.

## 7. What this does not establish

- Nothing here is a statement about any individual's intent, competence or good faith, or about a production deployment; both repositories say they are not production.
- Two repositories are not a sample. They were chosen because each states a pre-execution gate in public code and the work could be preregistered against its own text; a different pair might not show the class.
- The probes are same-source: the predictions, the probes and this text come from one model, and the reference implementation's results were also shaped by what its extractor patterns made easy to try. A second reader is owed.
- Whether a context flag is a weakness depends on who builds the context; this note reports what the code does, not what a deployment does.
- The reference implementation's HTTP layer was exercised only through a test client against SQLite; the Project-AI examination is limited to the core gate path under default configuration, with the sovereign runtime stage satisfied by installing its dependency.
- The Project-AI repository describes a much larger system (several languages, many components); nothing outside the examined path is claimed.
- No issue has been filed on either repository from this work.

**What would show this note wrong.** The companion harness failing at the pinned commits; a quoted line that does not appear at the stated path and line; or a later commit that changes the stated behaviour (a fix, not a refutation of the pinned reading).

## 8. Disclosure of how the repositories were found

The reference implementation was found while checking a vendor lineage cited by the adapting repository in the companion chain paper; Project-AI was found from a paper that names its components. Neither is connected to the chain of the companion paper.

## 9. Reproduce

`./reproduce.sh` in [`gate_library_class_replication_v1/`](gate_library_class_replication_v1/) clones the pinned commits into a work directory (not committed), runs each repository's own tests as the control (expect `52 passed`; `185 passed, 1 failed`), runs both probes and compares them with the committed outputs, ignoring random token identifiers (needs git, network and Python 3.10 or newer; a few minutes, mostly the Project-AI clone). Runs 1 to 3 of the Project-AI probe, with their harness errors, are in `project_ai/` with the amendments in its preregistration. [`SHA256SUMS`](gate_library_class_replication_v1/SHA256SUMS) covers the folder.

## References

- [`model_local_proofs_travel_v1.md`](model_local_proofs_travel_v1.md): the chain paper this note accompanies.
- [`pre_execution_gate_counter_models_v1.md`](pre_execution_gate_counter_models_v1.md): the claim forms, the defeat conditions and the requirements list (section 5) referred to above.
- [`execution_gate_channel_collapse_v1.md`](../published/execution_gate_channel_collapse_v1.md): the channel-collapse result of which section 6's first row is a new site.
- The pinned repositories in section 2 and `PINS.txt`.
