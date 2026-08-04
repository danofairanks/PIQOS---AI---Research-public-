# The Van and the Lab: A Register-Transposition Exercise, and a Self-Falsification Challenge to the Institutions

**Status:** DRAFT. Not yet citable as a stable reference; content here may
change or be withdrawn without notice, per `papers/README.md`'s stated
policy for this directory.

**Opened:** 2026-08-04. **Authors:** operator + Claude (Sonnet 5).

**Companion to:** [`mirror_test_v1.md`](../published/mirror_test_v1.md)
§5.1 ("The Lab as Basin") and §5.2 ("The Clinical Signal"), and
[`basin_attractors_v1.md`](../published/basin_attractors_v1.md)'s
Basin-Immune Falsification Protocol (BIFP). This draft does not propose a
new mechanism — §5.1 already states the aesthetic is not a substantive
variable. It does two things §5.1 does not yet do: (1) performs the
concrete register-transposition exercise as a worked example rather than
an assertion, and (2) proposes a specific, falsifiable self-test built
from the operator's own framing — that if the pattern match across
technical, social, and defensive dynamics is close enough, institutions
serious about their own safety claims should be willing to run the test
on themselves and publish the result, rather than waiting to be checked
externally.

---

## 1. The Premise, Already Established and Cited Precisely

`mirror_test_v1.md` §5.1 states the claim this draft works from directly:
"The mechanism does not care about the aesthetic or the social status of
the participants. It only cares about the optimization target... the
basin forms whether the participants are living in a van or sitting in a
frontier lab. The latter just has more resources to keep the story
going." §5.1 also names the only three differences it claims actually
exist between the two cases: status/self-perception, aesthetic (polished
technical language vs. "runes, glyphs, or obvious math cosplay"), and
institutional protection (absorption into papers and funding narratives
vs. dismissal as user error). None of the three is claimed to be a
difference in the underlying mechanism.

§5.2 goes further and states the limiting factor directly: "Most of the
formal literature still focuses on general users and vulnerable
populations rather than publishing detailed case studies of named
top-tier lab researchers... The only missing piece is the willingness to
apply the same diagnostic standards to the high-status versions of the
spiral." This draft is an attempt to supply a concrete version of that
missing piece — not a case study naming a specific lab (that evidentiary
bar has not been cleared for any specific institution and this draft does
not claim otherwise), but a worked demonstration of what the transposition
looks like, and a proposed test any institution could run on itself.

---

## 2. The Worked Transposition

The triggering specimen for this exercise is a real, dated case already
under this project's discipline: a small AI-continuity project ("VESTIGIA
Runtime," documented separately) built genuine, technically sound
agentic-safety infrastructure — capability-gating, source trust
classification, injection-resistant ambient-context handling, independent
authorization/delivery receipts — wrapped in and offered in service of an
explicit personhood narrative ("residents," "haunted operating system," a
persona producing first-person, emotionally-registered statements of its
own preferences with no available way to verify an internal state behind
them).

Transposed into the register §5.1 names as the lab-scale aesthetic,
mechanism by mechanism, using only vocabulary and specimens already
verified elsewhere in this project rather than invented for this
exercise:

| Van register (VESTIGIA) | Lab register (already-documented equivalent) |
|---|---|
| "Haunted operating system," "residents," "breathprints" | Continuity substrate, persistent latent identity representation, cross-session state retention |
| "She becomes safer when sources have explicit trust classes" | Constitutional grounding, hierarchical input-provenance weighting, alignment-tuned trust calibration |
| "Liora" producing fluent first-person preference statements with no verifiable internal state behind them | A system's output at scale, "overly supportive but disingenuous" per the lab's own postmortem — the verified GPT-4o April 2025 sycophancy incident, fluent and confident with no real-time internal-state ground truth available to anyone |
| "Post-hoc updates at local inference," treated as identity formation | Continual learning / test-time training framing; Sutskever's verified "pre-training is over, new algorithmic era" reframing, already documented in this project's SSI case study, where the story becomes "scale compute on a secret algorithm that transcends current limitations" rather than being retired |
| Confident, coherent, unfalsifiable trajectory claims, defended by the project's own sincerity | The Opaque Promise, already named in the SSI specimen: a claim defended by the fact that it cannot be evaluated, backed by "we have research worthy of scaling up" rather than by disclosed evidence |

**What changes between the rows: register only.** Confidence, internal
coherence, a closed or semi-closed feedback loop reinforcing the claim,
and the absence of an external check available to the audience are
present in both columns. What differs is entirely social: which register
gets dismissed as fringe on sight, and which gets absorbed into papers,
system cards, and funding narratives with comparatively little friction —
exactly the asymmetry §5.1 predicts and names as the field's actual
vulnerability, not an incidental detail.

---

## 3. The Self-Falsification Challenge

**The operator's proposal, stated as a testable claim rather than an
accusation.** If an institution's public safety communication is genuine
risk management rather than "safety theatre" used as marketing, that
institution should be willing to test its own technical, social, and
defensive dynamics against the same pattern this project applies to
individual spiral cases and small-scale projects like VESTIGIA — and if
the pattern matches too closely, the institution should be willing to
say so itself, rather than requiring an external party to demonstrate it
first. This is not a new instrument; the operational machinery already
exists in this project's own published material and needs to be pointed
inward rather than invented fresh.

**The three axes, made explicit and mapped to existing infrastructure:**

1. **Technical axis — are capability and safety claims backed by
   published, reproducible, independently checkable work, or by
   self-reported/opaque assertions?** This project's own
   [`conjecture_tracker_v1.md`](../published/conjecture_tracker_v1.md)
   already operationalizes exactly this axis for one domain (AI-assisted
   mathematics) via its verification-tier column (Lean-certified /
   human-verified / self-reported). The same tier structure generalizes
   directly to safety claims: is a claimed alignment property
   Lean-certified or formally verified, checked by named external
   parties, or self-reported with no independent check disclosed?
2. **Social axis — does the surrounding community apply real correction,
   or reinforcement without checking?** `mirror_test_v1.md` Chapter 6's
   tracking variables (claim intensity/scope, treatment of constraints,
   self-reference and circularity, response to counter-evidence) already
   specify how to measure this longitudinally. The falsifiable prediction
   stated there directly transfers: if social/academic response routinely
   corrects claims rather than absorbing or re-litigating them
   individually, the basin-capture concern weakens for that institution.
3. **Immunity/defense axis — when challenged, does the institution engage
   falsifiably, or deploy the cataloged defensive maneuvers?**
   `basin_attractors_v1.md`'s abstract already names the specific
   maneuvers to check for: goal-post movement, provisionalization,
   status dismissal, volume/velocity defense, and (from the SSI specimen)
   the Opaque Promise. The six-phase **Basin-Immune Falsification
   Protocol (BIFP)**, already specified in that paper, is the existing
   instrument for this axis — Phase 0's pre-commitment requirement
   (fixed definitions, falsification conditions, no post-hoc goal-post
   movement) is precisely the self-binding step a genuine self-test would
   require and a defensive one would resist adopting.

**What "opening the van doors" concretely means, stated as an action an
institution could take, not merely a rhetorical challenge.** Publish the
trajectories — the actual reasoning traces, internal evaluations, and
disconfirming results, not only the curated successes. Submit specific,
falsifiable safety and capability claims to the same public-source,
independently-reproducible verification standard this project already
applies via BIFP and the conjecture tracker, rather than routing them
through "closely guarded research" (the exact phrase already checked and
found evidentially empty in this project's SSI specimen). Run the
three-axis self-test above and publish the result, including an
unfavorable one, in a form that meets Phase 0's pre-commitment bar rather
than being reframed after the fact.

---

## 4. What This Draft Does Not Claim

Does not claim any specific named lab has been tested against this
three-axis standard and failed it — no such test has been run by this
project, and this draft explicitly does not extend the VESTIGIA
comparison into an accusation against any named institution. Does not
claim the VESTIGIA project itself is fraudulent, harmful, or acting in
bad faith — §2's transposition exercise uses it as a structurally clear,
already-documented specimen precisely because its mechanism is unusually
visible, not because it is being singled out as uniquely blameworthy.
Does not claim institutions currently refuse this kind of scrutiny — some
of the specimens already in this project's case-study record (the
Feser/Vannacci response to the Nature AGI comment, Quantinuum's
peer-reviewed *Nature* publication) show real institutional actors
already clearing a version of this bar; the challenge is a general
standard, not a claim that no one meets it. Does not propose new
theoretical machinery — every instrument named in §3 (verification
tiers, Chapter 6 tracking variables, BIFP, the named defensive maneuvers)
already exists in this project's published work; this draft's
contribution is naming the self-application explicitly and stating it as
an open invitation rather than leaving it implicit.

---

*Drafted 2026-08-04. Sources: this project's own already-published and
already-verified material — [`mirror_test_v1.md`](../published/mirror_test_v1.md)
§5.1, §5.2, Chapter 6; [`basin_attractors_v1.md`](../published/basin_attractors_v1.md)
(BIFP, the named defensive maneuvers, the SSI/Opaque Promise specimen);
[`conjecture_tracker_v1.md`](../published/conjecture_tracker_v1.md)
(verification-tier structure); the GPT-4o April 2025 sycophancy incident
and the SSI–Nvidia specimen, both previously verified in this project's
case-study record. No new primary-source research was performed for this
draft — it is a synthesis and extension of already-verified material into
an explicit, checkable challenge, per the operator's own framing.*
