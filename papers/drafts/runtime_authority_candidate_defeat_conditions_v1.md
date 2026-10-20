# Defeat Conditions and Prior Art for Three Submitted Cases Against a Public Runtime-Authority Verification Candidate

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** The object examined is a public verification candidate published by FlowSignal, a UK company that describes its own business model publicly: the repository `github.com/grahamb-ai/flowsignal-runtime-authority-verification`, `main` at `1cfeffa10b9cf2109a11ecbdd0a9a4fd7dd606c0`. The organisation and the repository path are named because the claim being tested is what that repository's README says. No individual is named: maintainers and authors credited in the repository are not named here, and an account handle appears only inside a repository path. No intent is attributed to anyone. The repository asks for exactly this kind of scrutiny ("try to make the declared properties fail"), and this note was written before any reply to the three issues described below.

**Disclosure.** Drafted with AI assistance. The tests and the reading of the source were done by one model in a scratch copy, so the results are a same-source check, not independent verification. Section 5 says which prior-art statements are recalled rather than looked up.

**Companion to.** [`gate_library_class_replication_v1.md`](gate_library_class_replication_v1.md) (where the same repository family is compared at the class level) and [`pre_execution_gate_counter_models_v1.md`](pre_execution_gate_counter_models_v1.md) (the claim forms and defeat conditions for pre-execution gates in general). [`governance_packets_levels_depth_twenty_tests_v1.md`](governance_packets_levels_depth_twenty_tests_v1.md) (the levels, layers and termination test applied in section 4a; that paper is pattern-level and names no case, and nothing here changes it). This note is narrower: it records, for three specific submitted cases, what would show each case to be wrong, before the maintainer has classified them.

## 1. What was submitted

On 2026-10-18 three issues were filed on the repository, following its `PUBLIC-VERIFICATION-CHALLENGE.md` (nine items per case; reproducible test; control; assumptions). Each ships a pytest file that was run only at `1cfeffa`; two controls pass and six challenge assertions fail.

| Issue | Declared property challenged | Observation | Control |
|---|---|---|---|
| [#7](https://github.com/grahamb-ai/flowsignal-runtime-authority-verification/issues/7) | NOW ("Is that authority valid at the point of execution?") | With the fixture mandate's `valid_until` of 2026-12-31T23:59:59Z and `resolved_at = bind_at = 2027-01-01T00:00:00Z`, final bind returns `PERMITTED` and a protected consequence forms. | Same flow at the fixture's own time forms a consequence, so the boundary is reached. |
| [#8](https://github.com/grahamb-ai/flowsignal-runtime-authority-verification/issues/8) | WHAT, specifically the mandate's aggregate capacity | Amounts `0.00` and `-1.00` form a consequence. The sequence `750000.00`, `-500000.00`, `750000.00` forms three consequences (gross positive 1,500,000.00) against a capacity of 1,000,000.00 (per issue #8, linked in this row). | `750000.00`, `750000.00` refuses the second with "aggregate authority capacity exceeded". |
| [#9](https://github.com/grahamb-ai/flowsignal-runtime-authority-verification/issues/9) | "incorrect grant correspondence does not destroy a still-valid grant" (availability) | A request with three decimal places is accepted at prepare, rejected at mint, and its reservation then makes a valid prepare for `750000.00` raise "aggregate authority capacity exceeded". | Not applicable: the contrast is the same prepare with no earlier rejected request. |

## 2. Classification forecast, recorded before any reply

These are forecasts about how the maintainer will classify the cases, not findings. They are written down so they can be wrong.

- #7: scope extension. No numbered item under "What we currently claim" is specific to mandate validity at bind, and the README places a production clock source outside the boundary.
- #8: scope extension. The R1 exact-money claim covers exactness and finiteness, not sign.
- #9: a variant of disclosed weakness 4 in the README ("an availability weakness where an incorrect correspondence could consume a genuine grant"), with a different trigger.

No forecast is made about whether the maintainer will remediate. A scope-extension classification is compatible with the observations being correct; it changes what they establish, not whether they occurred.

## 3. Defeat conditions

Each condition names an outcome that would make a case a non-finding or reduce its claim. A condition that merely narrows scope is marked; it does not make the observation false.

**All three cases**

- **D-all-1 (non-reproduction).** An independent run of the shipped test file at `1cfeffa`, with the pinned dependency versions, does not reproduce the failures. The same-source result is then invalid, and the issue text should be withdrawn or corrected.
- **D-all-2 (wrong object).** The maintainer shows that the tested functions are internal and that the documented entry point (an HTTP route or gateway) always runs a check that the tests bypass. The observation stands for the functions tested; the claim about "the integrated path" is narrowed (scope, not falsification).
- **D-all-3 (wrong commit).** The behaviour differs on the branch the challenge text names (`public-verification-candidate-v0.1`), which was not available to the tester. The observation then describes `main` only.

**#7 (mandate expiry)**

- **D7-1.** Mandate `valid_until` is enforced on a route the tests did not exercise, and that route is the documented way to reach final bind, so the tested sequence is not a reachable state. (Reduces the claim to the functions tested.)
- **D7-2.** The fixture's `valid_until` is documented as informational and not enforced by the reference engine. (The observation stands; it is not a failure of any listed property.)
- **D7-3.** The expected caller contract requires the caller to refuse binds after `valid_until`, and the harness documents that. (Scope: the property is held by the caller, outside the boundary.)

**#8 (non-positive amounts, negative reservation)**

- **D8-1.** Sign is validated at every documented entry point before the engine functions are reached. (Scope; the observation of the internal functions stands.)
- **D8-2.** A negative amount is a documented, intended reversal, with defined semantics, and the aggregate usage is meant to decrease. The claim "gross spend exceeds capacity" then depends on a definition of gross that the maintainer does not accept. (Definition dispute, not falsification; the second sequence would need reclassification.)
- **D8-3.** The usage store caps the sum of absolute values or refuses negative reservations on a path the tests did not take.

**#9 (rejected request keeps its reservation)**

- **D9-1.** A release-on-failure or expiry path exists and is part of the documented flow (for example an explicit release call, or a time-to-live on reservations), and the test omitted that step. Without it the case becomes a documented behaviour and not a bug.
- **D9-2.** The rejection at mint is documented as consuming the reservation by design, as part of disclosed weakness 4.
- **D9-3.** The valid prepare is refused because of a second mandate or state outside the fixture, and the tester's "nothing else outstanding" was wrong.

## 4. What counts as support, and what does not

- A fix commit that makes a challenge assertion pass is evidence the maintainer reads the case as a defect. It is not evidence the tester was right about severity or scope.
- Silence is not evidence of anything. No inference is drawn from the absence of a reply.
- A reply that classifies a case as out of scope confirms that the observation is outside the stated claims. It does not remove the observation. The two statements are kept separate.
- This note makes no claim about the repository as a whole, about any production system, or about the company.

## 4a. Level and layer, in the governance-packets paper's scheme

Applying the categories of [`governance_packets_levels_depth_twenty_tests_v1.md`](governance_packets_levels_depth_twenty_tests_v1.md) (sections 2, 3 and 7). This is a reading from the repository's README, not a measurement, and it covers only what the README says.

- **Level.** Level 2, technical boundary: a gate between an AI system and an effect (the README's own phrasing is "protected consequence" and a final bind before it). The README makes no organizational (Level 1) or model-level (Level 3) claim, and says the harness is a reference implementation. I saw no level equivocation in the README. I did not read other material from the company.
- **Layer.** L4, harness or operating system: checks outside the model, with signed or bound records. Per that paper, this is the only place a hard wall can exist, and only if the checker sits outside the control of what it governs. It says nothing about what any model has learned.
- **Trust domain, which the paper's section 4 makes the deciding question.** In the shipped harness, the checker and the caller are in one process and one repository, and the time of the bind and the amount are values the caller writes (the three cases turn on this). That is the condition the paper calls a convention rather than a wall. The README places a production clock and deployment outside its boundary, so this is a statement about the reference harness, not about a deployed system.
- **Termination test (the paper's section 7).** The README states that the company performed the verification that produced its baseline and that this is not independent third-party validation. Under the paper's test that is not yet a valid end of the chain of checking. The public challenge is an attempt at a valid end: an executed outcome that someone else can run. The three cases are such runs. Their classification by the maintainer, who wrote the harness, is again inside the same circle, which is why section 3 asks for independent reproduction first (D-all-1).
- **Bounded versus universal.** The README's claims are bounded ("within the tested reference-harness boundary") and listed, which the paper's section 4a treats as confirmable by trial. The three cases do not contradict a bounded claim that is outside the cases' scope; they test the edges of the bound (see section 2).

What this does not do: it does not rank the repository against others, and it does not say the checks are weak. It says which of the paper's questions the repository's own documents answer and which they leave to the reader.

## 5. Prior art for the properties involved

The repository describes itself as a reference implementation of known ideas, so the following maps each property to established concepts. **The first six rows are recalled from background knowledge and were not looked up; verify each before relying on it. The last four rows were read as primary sources for earlier drafts in this repository (named in the row); they were not re-read for this note.** The mapping is a reading, not a derivation.

| Property in the repository | Established concept | Reference as recalled |
|---|---|---|
| Authority is checked at the point of execution, not only earlier (NOW, MATCH) | Time-of-check to time-of-use | Bishop and Dilger, "Checking for Race Conditions in File Accesses" (1996) |
| Every access passes a mediating check | Complete mediation, reference monitor | Anderson report (1972); Saltzer and Schroeder (1975) |
| A one-shot grant that corresponds to the exact decision | Capability tokens and replay-resistant, single-use authorisation | Dennis and Van Horn (1966) for capabilities; one-time tokens generally |
| The action in the grant matches the action executed (WHAT, MATCH) | Fine-grained authorisation requests bound to the specific action | OAuth 2.0 Rich Authorization Requests (RFC 9396) |
| Reserve capacity, then confirm or cancel | Reservation with rollback; Try-Confirm-Cancel; sagas | Garcia-Molina and Salem, "Sagas" (1987) for the pattern |
| Amounts must be non-negative where the domain requires it | Numeric range check without a lower bound | Common weakness enumeration "numeric range comparison without minimum check" (identifier recalled as CWE-839) |
| Access is an element of a matrix of domains and objects, consulted by a handler when the access is attempted (WHO, WHAT, NOW) | Lampson, Protection (1971) | read as primary in [`public_admissibility_evaluators_v1.md`](public_admissibility_evaluators_v1.md) section 3a and [`guard_property_prior_art_v1.md`](guard_property_prior_art_v1.md) |
| A guard whose decision depends on state across calls, as an aggregate cap does | Lampson, Protection (1971), the exercise of a grading program that allows a student program a fixed number of tries (p4) | same two drafts |
| Remembered results of an authority check must be updated when authority changes; check authority to change authority (NOW) | Saltzer and Schroeder (1975) | read in part for the first draft above (principles and protection-dynamics passages in full, the rest by keyword) |
| Input of any value must be validated or refused before it changes state; well-formed transformations only (#8, #9) | Clark and Wilson (1987) | read as the NIST SP 500-160 reprint, scanned with OCR errors, per the first draft above |

What this does and does not establish. The properties are not novel in kind, and the repository does not claim that they are. The three cases fall into three of the oldest failure shapes in the table: a check performed at one time and not at the point of use (#7), a missing range check on an input (#8), and a reservation not released when a later step fails (#9). The recurrence of these shapes in a reference implementation is an observation about the checklist, not about the authors.

## 6. Limits

- Three cases, one commit, one tester. No claim about frequency.
- The tests run in a scratch copy with caller-supplied times; production clock sources, persistence and distributed coordination are outside the repository's stated boundary and outside this note.
- The first six rows of the prior-art table are recalled, not verified; the last four were read as primaries for earlier drafts and not re-read here (section 5).
- The maintainer may have changed `main` since `1cfeffa`; the note is about that commit only.
- Unpublished or later-filed material (for example a patent application) is unknown to this note. The note works only from public artifacts and does not assume access to hidden ones, nor does it ask the maintainer for anything beyond a public reproduction and a classification. Such material, if it exists, would not change the observations in section 1 and could bear only on the prior-art statements in section 5, which make no novelty claim. A published document of this kind would be added to section 5 as a related document, not treated as a defeat condition.
- Defeat conditions were written by the same model that wrote the tests. They are a checklist for a reviewer, not an independent list.

## 7. Updates

Maintainer responses will be recorded here with their date, including classification, any fix commit, and whether any defeat condition above was met. A condition is marked met only if the response names it or shows the outcome directly.

- *2026-10-18, v1.1.* Added the four access-matrix and integrity rows to section 5 (Lampson, Saltzer and Schroeder, Clark and Wilson), taken from earlier drafts that read them as primaries.
- *2026-10-18, v1.2.* Added section 4a (level, layer, trust domain and termination test, per the governance-packets paper) and the companion link. Forecasts and defeat conditions unchanged.
- *2026-10-18, v1.3.* Added a limits line on unpublished or later-filed material (section 6). Forecasts and defeat conditions unchanged.
- *2026-10-20, v1.4.* Pointer only: where a claim about an integrated system cites a bounded test of one component, section 7b of [`model_local_proofs_travel_v1.md`](model_local_proofs_travel_v1.md) names the pattern (borrowed assurance) and gives a stub-substitution check with its prior art. Forecasts and defeat conditions unchanged.

---
*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
