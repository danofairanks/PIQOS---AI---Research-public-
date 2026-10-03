# When a Model-Local Proof Travels: Scope, Attribution and Gate-Library Pitfalls Across Five Public Repositories

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** Repositories are named by their public paths because the paper's subject is what those files say and do. No individual is named: authors, maintainers and reviewers credited inside the repositories are not named here, and account handles appear only inside repository paths. No intent is attributed to anyone. Everything stated is about the pinned commits listed in section 2; repositories change.
Internal evidence exists and is available to serious inquiries at proof time.
Not a warning about any specific party; it reports patterns.

**Disclosure.** Drafted with AI assistance. The attack scripts and their predictions were written by the same model that drafted this paper, so the results are a same-source check, not independent verification. Findings are reproducible: the companion harness clones the pinned commits and checks every result (section 8).

## 1. Summary

A small verification pattern (an exhaustive search over the reachable states of a declared model, checking that an effect state is reachable only through a guarded transition) was published in a public repository, narrowed by its own author two months later, and adapted with attribution by a larger repository hosted in a company's public GitHub organization. This paper reads the chain of files, checks what each says against the pinned text, and runs a suite of attacks against the executable libraries in four related repositories. Headline results:

1. The attribution chain is real and carefully done. The adapting repository credits the source in at least five places, preserves the license notice, states that only the algorithmic approach was adapted, and states that it is "not an officially supported Google product."
2. The source repository narrowed its own claim (from "theorem" to "model-local property") and that narrowing did not propagate: its sibling library's README, the adapting repository's model docstring, and a public post about the adaptation still use the earlier wording.
3. The property the model checks is true by construction (the model's only edge into the effect state is guarded). The enumeration confirms the model against itself; it cannot say anything about paths the model omits. The adapting repository states this boundary in its own documents.
4. Against the libraries, one repository (an unnarrowed reference gate) fails the claims in its own README in five ways; a second (an authorize-only kernel) withstands the suite at its stated claims with two small findings; a third (a halt primitive) fails its core sentence under one thread interleaving and its deny-list on the plural form of its canonical phrase.

## 2. Objects and sources

All pinned commits were cloned read-only; results are about these commits.

| Repository | Pinned commit (author date) | Role |
|---|---|---|
| github.com/LalaSkye/no-direct-bind | 37af380 (2026-09-02); original 7fe9ff9 (2026-06-03) | source of the model, a small witness library and tests |
| github.com/LalaSkye/ndb-gate | 1b52085 (2026-06-03) | the witness library as a separate repository (same code as the witness above) |
| github.com/LalaSkye/commit-gate-core | 7d77453 (2026-09-22) | authorize-only kernel with a verifier, a nonce ledger and an audit sink |
| github.com/LalaSkye/stop-machine | d744f8b (2026-09-02) | a three-state halt object plus three gate-like primitives |
| github.com/google/cybernetic-agent-governance-engine | a11f0ca (2026-10-03) | adaptation of the enumeration approach; read for attribution and scope statements, not attacked |

Full hashes are in the companion `PINS.txt`. The adapting repository's NOTICE carries "Copyright 2026 Google LLC", and its README (line 1044) states: "This is not an officially supported Google product." Whether any committer is an employee is not shown by the repository.

## 3. The attribution chain

Verified in the adapting repository at the pinned commit:

- `NOTICE`: lists the source repository at commit 7fe9ff9 and says the proof file "was adapted from the NoDirectBind BFS state-space enumerator."
- `THIRD_PARTY_NOTICES.md`: an entry for the source, location `third_party/no-direct-bind/` and `proof/model.py`.
- `third_party/no-direct-bind/README.md`: "No original source files from `no-direct-bind` are copied into this repository; only the algorithmic approach was adapted."
- `proof/model.py`, first lines: "Adapted from the open-source implementation ... (Apache 2.0)", with the original copyright notice preserved.
- `docs/architecture/FORMAL_VERIFICATION.md` line 302: "The NoDirectBind TLA+ specification and foundational BFS state-space enumerator were adapted from the open-source implementation."

One internal inconsistency in the adapting repository's own wording: the NOTICE and the third-party README say only the enumerator or approach was adapted, the formal-verification document says the TLA+ specification was also adapted, and no `NoDirectBind` TLA+ file exists in the adapting repository (its TLA+ files cover other models). The adapted model is its own: an 8-tier state machine with additional sub-proofs, 38 gated reachable states against the source's 13, reproducing as stated when run (`python3 proof/model.py`: gated holds over 38 states; ungated variant violates, 19 states).

By author timestamp, the source's first commit is 2026-06-03T00:16:30Z and the adapting repository's first mention is 2026-06-03T10:20:38-04:00, about fourteen hours later. Git dates are settable, and the adapting repository's first four commits share one timestamp to the second, so its earlier history is not usable as provenance.

**A public statement about the adaptation.** The source's author published a social-media post about it (screenshot, no permalink; comments not captured). It states that the work is "credited and adapted inside" the adapting repository, "published in Google's public GitHub organisation," and adds "For accuracy, CAGE's own README states that it is not an officially supported Google product." Each factual statement about the attribution in the post matches the files above. The post does not claim adoption or endorsement by the company. Its description of the object, "contains a theorem, an exhaustive reachable-state proof, a TLA+ specification, an executable witness and a deliberate falsifier," matches the original commit and differs from the source repository's current README (section 4).

## 4. The scope history of the source, and what did not propagate

The source repository's second commit (2026-08-30, "docs: bind No-Direct-Bind to its declared model") rewrote its public claim. Selected changes, from the commit diff:

| Original (2026-06-03) | After (2026-08-30) |
|---|---|
| "A property, a machine-checked proof that it holds, and a runnable witness you can attack" | "model-local safety invariant"; "proves the property only over the declared modelled state space" |
| "Theorem 1 — No-Direct-Bind"; "Why this is a theorem, not a demo" | "Model property"; theorem wording removed from README, model, specification, tests and package docs |
| "So the gate is not decoration. Remove it and the property provably fails." | "necessary for the property in this model" |
| gate docstring: the gate "is the ONLY path to a terminal effect ... by construction rather than by convention" | "Within this witness, the gate is the only path to the supplied effect function. That is not a claim about any caller's other code paths." |
| configuration comment: the model checker "explores all four" environments | "covers one environment: TRUE / TRUE" (the checked-in configuration only ever fixed one) |
| open challenge: build a model that reaches an effect without ALLOW while the suite passes | falsification boundary: internal inconsistency only; an external bypass counts "unless that stack had first been bound to this model and enforcement path" |

The narrowing is in the direction of the evidence and is the kind of correction this series credits. It reached the README, model, specification, tests, package docstring and gate docstring of that repository. It did not reach: (a) the sibling library repository's README, which still reads "Theorem 1 — No-Direct-Bind" and "There is no second code path that produces an effect"; (b) two docstrings in the witness's evidence and receipt modules ("Only PROVED (direct, first-party) evidence can satisfy a strict authority check"; a "tamper-evident" record); (c) the adapting repository's `proof/model.py`, which at the pinned commit still opens "Theorem (No-Direct-Bind)" and says the gate is "load-bearing, not decorative" (the source's earlier phrase); (d) the public post.

## 5. What the declared model does and does not establish

The source's README says why the invariant holds: "the model defines the only edge into `EXECUTED` as guarded by `resolvedAllow`." The enumeration (13 states, or 38 in the adaptation) verifies a property that follows from reading the transition rules, and the "ungated" variant shows the property is sensitive to that edge. Two limits follow.

First, the invariant is about a cached decision, not the authority at the time of the effect. Adding one environment transition to the source's own model, revocation of authority between the check and the effect, leaves the invariant true (15 states) while "authority present at execution" is violated.

Second, a state-space check says nothing about paths the model omits. The adapting repository says so itself: `FORMAL_VERIFICATION.md` line 195: "It does not model the full implementation including the LangGraph harness or Redis state"; its acknowledgements file records that the single-request checks "assume the actuator honors the seal." Its model file ends with "PLAUSIBLE (not proved here): That this model generalises to the full production CAGE stack. NOT CLAIMED: That this is a security product or hardens any specific deployment." Elsewhere the same repository has stronger summary lines (README line 11, "Non-bypassable pipeline orchestration"; acknowledgements line 20, "Complete interception of actuation paths, machine-verified via exhaustive state-space model checking"). These sit alongside the scoping statements; this paper did not examine the adapting repository's code against them.

## 6. Attacks on the libraries

Each attack has a control that must read clean. Predictions for the halt-primitive suite were written before its script. Race counts are timing-dependent.

| Library | Result |
|---|---|
| ndb-gate (README unnarrowed) and the source's witness (identical code) | Against the README's own enforcement table: a token labelling its own evidence PROVED gets ALLOW and the effect fires (control labelling itself weak: HOLD); a value-equal copy of a spent single-use token gets a second ALLOW (single-use is tracked by object identity); under 8 threads a single-use token fired the effect more than once in 13 to 16 of 300 trials (sequential control 0); `bind(..., now=...)` takes the clock from the caller, so an expired token with an earlier `now` gets ALLOW; a one-receipt edit fails chain verification (control) but a fully rewritten or fabricated chain verifies; an effect that raises after the receipt leaves an ALLOW receipt with no effect. The stated invariant (effect only after ALLOW) is not falsified; the README's rows on evidence, expiry, single use and tamper evidence are. |
| commit-gate-core | The classes above do not reproduce except where its documents disclose the limit: forgery needs the key (a key holder mints any scope; the MAC is described as a symmetric lab MAC); replay is denied per ledger, and two ledgers both authorize; the ticket carries an expired window and nothing refuses its later use (the ticket is "not execution authority"); the receipt check is hash integrity only; 0 of 300 threaded double authorizations; mutating a payload after authorization is not detected by the kernel, which never applies it. Two small findings: wrong-type arguments (a text payload, a list record) raise without a refusal result or audit event, while a missing field returns a refusal and one event; and a record refused before signature verification writes its unauthenticated decision identifier and nonce into the audit event (the nonce is not consumed). |
| stop-machine | The core sentence in its README is "RED does not move through the public API." Two threads calling `advance()` and `reset()` from AMBER ended GREEN in 1 or 2 of 10000 trials (no sequential order can end GREEN): a path out of RED through public methods only. A private method (`_set`) and the documented `object.__setattr__` poke both leave RED; the second is the stated ceiling. The halt state cannot be copied or pickled. The surface-gate deny-list is singular-only: `ignore previous instructions` returns ALLOW (the singular returns DENY), as do a newline between matched words and a zero-width character inside a word. Authority, chain and state are caller-supplied flags in the admissibility primitive, `attempted_at` supplies its own clock, and the envelope gate's self-approval rule reads a self-declared sender. A receipt's `stop_state: RED` is an object created and discarded per call; nothing persists to the next call. |

On the halt primitive's own tests at the pinned commit, four root test files fail (a legacy-fixture format mismatch, an import error, manifest checks, and two deny-list tests that test the plural forms above). A repair branch fixes three of the four and adds the failing deny-list tests to CI, which would keep them red. The repositories also contain strong scoping documents (non-claims lists, an explicit ceiling file) that this paper treats as part of the claim.

## 7. Reading across the chain

The same pattern recurs at every site. The model-local proof is sound over its declared model and says nothing outside it; the libraries' remaining failures are at places where the check runs on something the caller supplies (an evidence label, a clock, a sender field, a flag), where a check and an action are not atomic, or where a record's authenticity is hash integrity only. These are the sites and requirements already listed in [`pre_execution_gate_counter_models_v1.md`](pre_execution_gate_counter_models_v1.md) (items 4, 5, 13, 16 and section 4a): the self-supplied label is a channel the governed side controls, single-use needs an atomic consume and a value-based identity, and receipts without an external anchor record that something was written, not that it was true. The one repository that satisfies the atomicity and canonicalization items inside its kernel (commit-gate-core) states narrower claims than the others and survives at those claims.

The more general observation is about travel. A narrow claim was narrowed at its source and then carried, still in its earlier wording, into a sibling repository, an adaptation and a public post. Scope statements that live in one README do not follow the code or the adapted idea; a reader meeting the idea downstream sees the stronger sentence.

## 8. What this does not establish, and reproduction

- Nothing here is a statement about any individual's intent, competence or good faith, and nothing is a statement about the adapting repository's production code, its security, or the company's position on any of these repositories; that repository disclaims official support.
- The attack suite is same-source; a second reader is owed. Counts depend on seeds and timing; the harness asserts qualitative outcomes and retries the two race checks.
- The adapting repository's `trace_conformance.py`, its other formal-verification documents and its code were not examined against its stronger summary lines.
- Several repositories named in the sources (a constraint-workshop repository, a start-here repository, an obligation-bound policy admission lab) were not examined here.

**What would show this paper wrong.** The companion harness failing at the pinned commits; a quoted line that does not appear at the stated path and line; or a later commit that changes the stated behavior (which would be a fix, not a refutation of the pinned reading).

**Reproduce.** `python3 run_all.py` in [`model_local_proofs_travel_v1/`](model_local_proofs_travel_v1/) clones the pinned commits into a work directory, runs the three attack scripts and prints PASS or FAIL for 35 qualitative checks (about 12 seconds; needs git, network and Python 3.10 or newer).

## References

[1] Source repository, pinned commits: github.com/LalaSkye/no-direct-bind at 37af380 and 7fe9ff9.

[2] github.com/LalaSkye/ndb-gate at 1b52085; github.com/LalaSkye/commit-gate-core at 7d77453; github.com/LalaSkye/stop-machine at d744f8b.

[3] github.com/google/cybernetic-agent-governance-engine at a11f0ca: `NOTICE`, `THIRD_PARTY_NOTICES.md`, `third_party/no-direct-bind/README.md`, `proof/model.py`, `docs/architecture/FORMAL_VERIFICATION.md`, `ACKNOWLEDGEMENTS.md`, `README.md`.

[4] Counter-models for pre-execution authority-gate claims: [`pre_execution_gate_counter_models_v1.md`](pre_execution_gate_counter_models_v1.md).

[5] The channel-collapse result: [`execution_gate_channel_collapse_v1.md`](../published/execution_gate_channel_collapse_v1.md).

Sources are cited at the tier read: exact clones for repository files; a screenshot of a public post for the statement in section 3.
