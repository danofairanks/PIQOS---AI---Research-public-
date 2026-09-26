# Notational Consistency Without External Binding: A Countermodel Analysis of the Škrinjar Structural Architecture (R5.3.8)

## Abstract

The Škrinjar Structural Architecture (SSA), version R5.3.8, "A Recursive
Architecture of Governed Constitution" (Sandra Škrinjar, Independent
Researcher; canonical frozen-review date 24 September 2026), is a
26-page formal specification defining a versioned constitutive
specification K^v, a three-valued status logic {E, F, U}, six
structural non-entailment propositions (T1–T6) with witness
constructions, five countermodels, an eighteen-item conformance test,
and a corpus of eleven prior solo-authored papers plus one joint paper
with a named technical reviewer. The document explicitly invites
adversarial attack in its own §1 and explicitly disclaims novelty for
its constituent ideas in its own §16–§17, claiming contribution only in
"particular architectural organization." This paper takes up that
invitation directly. We show that every worked instantiation and every
non-entailment witness in SSA R5.3.8 stipulates its inputs rather than
deriving them from an external fact, that the document's own five
disclaimer boxes (§3.7, §12, §17, §18, §21), read together rather than
encountered one at a time, already concede the paper's central finding,
and that the document's one credited instance of adversarial review
resolves — by the document's own account of what that review produced
— to refinements the architecture is structurally built to absorb. We
formalize what a genuine countermodel against SSA would require as five
pre-registered defeat conditions (D0–D4), show that none has been
attempted anywhere in the document's public record, and situate this
finding within this project's own prior results on self-referential
verification loops. To confirm the protocol is executable rather than
one further unexecuted prediction, we run one of its five conditions
(D1, inertness) to a completed result against a determination chosen
outside SSA's own corpus, before publication. We name the specimen's
author and credited reviewer directly, a departure from this project's
usual redaction practice, justified in §1 below.

---

## 1. A note on naming

This project's standing policy redacts private individuals from its
published work unless the specimen is a public figure, an institution,
or an already-public-record event (`laundered_vocabulary_v1.md`'s "Law"
entry). Sandra Škrinjar publishes a sustained, dated, multi-release body
of work under her own verified identity — twelve DOI-registered
publications across SSRN and Zenodo, cited by name in her own work's
provenance table — and SSA R5.3.8 itself, in its own §1, issues a
direct, unqualified invitation: "Adversarial mandate. Attack the
architecture rather than restyling it... Return the smallest
countermodel and classify kernel/specification/application/no change."
This is a stronger and more explicit basis for naming than the
sustained-output bar this project has applied elsewhere (`register_
dressing_v1.md` §1). Ricky Jones is named in SSA R5.3.8's own
Acknowledgment section under a role the document itself defines —
"Technical Reviewer — Engineering and Adversarial Review" — and is
named here on the same basis, in that same role.

A separate paper in this project, `execution_gate_channel_collapse_v1.
md`, examines different material connected to the same two individuals
(the joint paper "Governed Handoffs from Trace to Consequence") and
redacts them. That treatment is not revised here. The two papers
examine different specimens, reach their naming decisions on different
stated grounds, and this paper's naming decision applies to SSA R5.3.8
specifically — the document that itself invites the scrutiny this paper
conducts — not retroactively to material examined elsewhere under a
different rationale.

No claim of deceptive intent, coordination, or AI assistance is made
about either named individual anywhere in this paper. The object under
study is a document's structural properties and one instance of a
credited review process; it is not a claim about either person's
character or motivation.

---

## 2. The document, described on its own terms

SSA R5.3.8 describes itself, in its own Document Status section, as
"the canonical architectural specification and reference for the
Škrinjar Structural Architecture," explicitly "not a conventional
research paper reporting an empirical study" and "not presented as an
independently axiomatized proof calculus." Its stated central question:
"What is this determination entitled to be constituted from, in what
function, under what composition, and under what conditions?"

The document defines a governed determination 𝔇 as "any status,
representation, relation, transition, classification, constitution,
transformation, handoff, or revalidation whose establishment carries
governance-relevant force," governed by a versioned constitutive
specification K^v(𝔇, t_v) = ⟨P*, R*, C*⟩, where P* contains
participant-function obligations, R* contains irreducible relational
obligations, and C* contains contextual and indexing conditions. Five
further derived statuses — obligation applicability (App), obligation
satisfaction (Sat), specification adequacy (Adeq), constitutive
participation (CP), and constitutive composition (Γ) — each range over
{Established, Failed, Unresolved} and compose, through a "constitutive
resolution" rule the document states but does not itself instantiate
against any external case, into a final constitutional status σ.

Six structural non-entailment propositions organize the document's
central claims (§10):

- **T1, Participation Non-Conferment.** VALID(x) does not entail
  CP(x, φ, 𝔇, t_v | K^v, t_a) = E.
- **T2, Composition Independence.** Every applicable participant-
  function obligation may have Sat = E while Γ ≠ E.
- **T3, Determination Non-Inheritance.** The existence of a source
  assessment record does not entail establishment in a receiving
  determination.
- **T4, Non-Self-Constitution.** SUCCESS(Y) does not entail
  σ(𝔇, t_v | A) = E — a downstream result's success does not
  retroactively establish an upstream determination its own governed
  use presupposes.
- **T5, Temporal Non-Retroactivity.** A later assessment does not
  silently confer retroactive force on an earlier specification
  version.
- **T6, Upstream Validity Preservation.** A downstream non-
  establishment does not itself entail upstream non-establishment.

Each proposition is supported by a "witness" — a hypothetical pair of
objects whose statuses are stipulated by the author for the purpose of
demonstrating that the stipulated values propagate through the
apparatus as the proposition claims. Five further countermodels (§15)
follow the identical form: hold one condition fixed, stipulate a change
in another, and show the resulting statuses diverge as claimed.

Appendix B lists twelve source works under the heading "Canonical
Source Record and Provenance": eleven solo-authored papers by Škrinjar,
deposited on SSRN and Zenodo between an initial 2026 filing and the
present release, and one paper co-authored with Ricky Jones, "Governed
Handoffs from Trace to Consequence," for which Appendix B records
Zenodo version DOI 10.5281/zenodo.22854076 and concept DOI 10.5281/
zenodo.22854075. Jones's Acknowledgment credit is explicit that this
one joint paper is the extent of shared authorship: "This
acknowledgement records review contribution only and does not confer
co-authorship of SSA."

---

## 3. Central finding: every worked case is stipulated, not derived

The paper's central finding follows directly from reading the
document's own text closely rather than from any external test this
paper constructs. Four observations, each independently verifiable
against the primary source, converge on one structural fact.

**3.1. The recursion terminates, by design, in an undefined term.**
Section 3.7, "Terminal warrant boundary": "Adequacy recursion
terminates where the inquiry reaches a declared domain-native
warranting basis W_T whose validity is outside the governed
determination presently under review." W_T is never instantiated for
any concrete domain anywhere in the document. Every chain of reasoning
in SSA — every App, every Sat, every Adeq — terminates, by the
architecture's own explicit construction, in a term the specification
declines to define.

**3.2. The conformance test specifies production requirements; it is
never executed.** Section 18 states eighteen numbered requirements,
each phrased as what "a conformant instance MUST" produce. No instance
of the eighteen-item test being run against a real case appears
anywhere in the document. Section 18's own closing sentence states the
consequence directly: "Conformance establishes conformity to SSA's
architectural governance requirements. It does not by itself establish
substantive truth, empirical validity, legal correctness, institutional
legitimacy, or execution authority."

**3.3. The countermodels test internal non-collapse, not external
correspondence.** Section 15's own stated purpose: "SSA is not
strengthened by making every distinction irreducible. Its distinctions
survive only where attempted collapse loses a materially different
establishment condition, failure location, permissible use, temporal
attribution, or consequence." This is a test of whether the document's
own distinctions are eliminable within its own notation — a legitimate
exercise, and one the document appears to satisfy on its own terms —
not a test of whether the notation binds to any fact outside itself.

**3.4. The document states its own limits directly, repeatedly, in
five separate places**, each independently quotable: §3.7 (above);
§12, "VALID CONSTITUTION ⇏ EXECUTION AUTHORITY... SSA MAY TEST THE
CONSTITUTION OF AN AUTHORITY CLAIM. SSA DOES NOT CREATE THE AUTHORITY IT
TESTS"; §17, "The literature review supporting this architecture is
bounded. It is not an exhaustive historical priority search, a
patentability opinion, or a legal novelty determination"; §18 (above);
and §21, "A valid thing can be used invalidly... A faithful trace can
survive while the entitlement attributed to that trace changes."

Read individually, each of these is the document behaving honestly
about a narrow, local limitation. Read together, they state — in the
document's own words, not in this paper's characterization of them —
that nothing in twenty-six pages binds to a fact outside the document
itself. This paper's contribution at this stage is not a new finding;
it is the observation that assembling five scattered concessions into
one continuous statement makes visible what encountering them one at a
time, in the order the document presents them, does not.

---

## 4. The credited adversarial review as an empirical instance

Section 1's invitation to attack the architecture was, by the
document's own account, already accepted once. The Acknowledgment
section states in full what Ricky Jones's credited "Technical
Reviewer — Engineering and Adversarial Review" contribution produced:

> His review included examination of jurisdiction boundaries,
> inheritance conditions, constitutive-resolution semantics,
> assessment-snapshot integrity, and specification consistency, and
> identified bounded hardening requirements incorporated during the
> R5.3.x revision sequence.

"Bounded hardening requirements" is, on inspection, precisely the class
of output the non-entailment apparatus of §10 is built to absorb:
refinements to jurisdiction, inheritance, and consistency language that
strengthen the specification's internal coherence without forcing any
of the six structural non-entailment propositions to fail, without
exhibiting a governed determination that resists classification under
the architecture's two constitutional loci (participation and
composition), and without producing a binding failure against any
external system. The one instance of credited adversarial engagement
this document's public record contains did not, by its own stated
description, attempt anything beyond this.

---

## 5. Prior art and the scope of the novelty claim

Section 16, "Informative Provenance Note — Prior-Art Positioning,"
states directly: "SSA does not claim novelty for the general ideas that
judgments may be context-dependent; proofs and rules may themselves
become objects of formal reasoning; valid components may fail to
produce a valid composition; institutional roles may be constitutively
governed... These ideas have substantial prior literatures across proof
theory, logical frameworks, contextual logic, justification logic,
institutional and deontic logic, authorization systems, provenance,
compositional verification, workflow governance, evidence theory, and
related formal disciplines. SSA makes no priority claim over those
general concepts." Section 17's "Claim Ceiling" narrows the
document's actual novelty claim to a single, conjunctive sentence: "no
single framework was identified that jointly organizes governed
determinations through independently warranted constitutive
specification, function-relative participation, independently
load-bearing composition, material recursive governance of passages,
and bounded constitutive reuse while preserving temporal and failure
localization."

Mapped against named external fields — a mapping this paper cross-
checked against the primary source before adopting rather than
accepting on the strength of the analogy that first suggested it —
each of T1–T6 corresponds to an established, independently named
distinction: T1 to the function-relative character of standing and
permission found across authorization systems and evidence law
(authenticity does not entail admissibility); T2 to the separation of
local from aggregate validity in compositional verification (component
correctness does not entail system correctness); T4 and T5 to
non-retroactivity doctrine in law and to the classical distinction
between outcome success and process validity in epistemology; the
Sat/σ separation of §6 to the standard distinction between deontic and
alethic force in modal logic. None of these mappings is original to
this analysis in the sense of being unavailable elsewhere; the
document's own §16 already concedes the general point. What the
mapping establishes precisely is the shape of the document's actual
contribution: a uniform, densely cross-referenced vocabulary applied
across these already-named distinctions, not a new binding mechanism
that reaches further than any one of them does individually.

The document's own corpus performs the same reduction at scale. Section
21's "Canonical Synthesis" maps all eleven prior solo papers, plus the
document itself, onto one six-symbol vocabulary: "Škrinjar Structural
Architecture → 𝔇, K, Adeq, CP, Γ, σ, material recursive governance,
bounded constitutive reuse." Section 19's wider-corpus mapping extends
this to the author's full publication list beyond the twelve formally
cited works. This is not, on its own, evidence of anything beyond what
§16 already states about the underlying ideas' priority — but it is
notable that the reduction to a small, fixed symbol set applies as
uniformly across fourteen years' worth of stated conceptual development
as it does within one twenty-six-page document.

---

## 6. Provenance without external contact

Appendix B lists real, resolvable identifiers: SSRN registration
numbers and Zenodo DOIs for all twelve works cited as the document's own
canonical source record. Depositing a document with either platform
assigns a permanent identifier and a citable record; neither platform
operates independent peer review as a condition of deposit. A DOI from
either service establishes that a document was deposited and is
retrievable under a fixed identifier. It does not establish that the
document's claims were independently checked before or after deposit.

Read against this distinction, Appendix B's escalation structure is
worth stating precisely: R5.3.8 is explicitly "the publication/
provenance successor to frozen R5.3.7," itself built on "the R5.3.6
constitutive-resolution kernel," citing eleven prior solo papers in
the same vocabulary family plus the one joint paper with Jones, whose
credited review — per §4 above — hardened wording without forcing a
kernel change. Each step in this sequence is independently DOI'd,
independently citable, and independently written in the same
constitutive vocabulary as the step before it. Nothing in the sequence,
checked from Appendix B's own provenance table, required contact with
a fact, system, or evaluator outside the same author's own corpus and
one collaborator's credited, wording-level review.

This paper did not independently verify the eleven prior solo papers
against the same standard applied to R5.3.8 itself — that check remains
open, and is stated as an open item in §9 below rather than assumed.
One specific, checkable citation gap is already established: a prior
Škrinjar paper, "The Škrinjar Structural Methodology" (SSRN 7365703),
which names the same public/protected-methodology split R5.3.8's own
§20 states, does not appear in Appendix B's provenance table despite
that table's own stated completeness rule ("unverified metadata is
omitted, not reconstructed"). This is an omission from a table that
claims completeness, not evidence that the underlying public/protected
architecture is internally inconsistent — the split itself was
disclosed a full publication cycle earlier, in the omitted paper.

---

## 7. A formal countermodel protocol: axiomatized defeat conditions

Section 1's own invitation — "attack the architecture rather than
restyling it" — is, read precisely, an invitation to falsification, not
to further formal commentary. We state what a countermodel against SSA
would need to satisfy as five pre-registered defeat conditions, in the
sense that a claim is not a binding claim until conditions exist under
which it would be considered defeated and those conditions are stated
in advance of any attempt to meet them (`governance_binding_axiom_v2.
md` states and defends this general principle; we apply it here rather
than re-derive it).

**D0 — Scope honesty.** If SSA is read as claiming only internal
consistency of a constitutive vocabulary — which is what §17's Claim
Ceiling and the five disclaimers of §3 above jointly state — no defeat
condition is required to establish overclaim against the document's
own text. Defeat becomes necessary only where a stronger claim is made
in use: adoption pitches, or language describing the architecture as
governing something beyond its own declared scope. D0 exists to keep
D1–D4 from being misread as attacks on language the document has
already conceded.

**D1 — Inertness.** Let B(𝔇) denote the outcome ordinary standing,
authorization, composition, and provenance practice would assign to a
concrete determination 𝔇. Let σ_SSA(𝔇) denote the status SSA assigns
after K^v is fully declared and App, Sat, CP, and Γ are filled under
the document's own stated rules. **Defeat condition:** σ_SSA(𝔇) =
B(𝔇) for every 𝔇 in a pre-registered test set, with no step of the
SSA apparatus changing the outcome. If satisfied, the architecture is
taxonomic: it classifies without exerting distinctive constitutive
force.

**D2 — Binding failure.** Pre-register, in order: (1) a concrete system
trajectory, which may be a minimal operational example; (2) a fully
declared K^v with Adeq = Established fixed *prospectively, before the
outcome is known* — closing, by construction rather than by subsequent
argument, the escape the document's own Adequacy Independence principle
(§3.6) otherwise permits, in which a failed outcome can be attributed
after the fact to inadequate specification rather than to the
composition rule itself; (3) an independent channel C — an execution
log, an external oracle, or a physical consequence — named explicitly
in advance. **Defeat condition:** σ = Established while C reports that
the governed claim does not hold. If satisfied, either the composition
or resolution rule fails under binding, or domain-native warrant was
doing the entirety of the constitutive work and the kernel contributed
nothing to the outcome.

**D3 — Forced third locus.** Section 11 of SSA R5.3.8 states directly
that no third locus exists: "Transfer failure, handoff failure,
candidate-constitution failure, relational-warrant failure, reduction
failure, retrospective validation failure are not additional primitive
constitutional loci." Taken alone, this closure claim names two loci —
participation (L-P) and composition (L-Γ) — and a naive D3 attempt
would try to exhibit a non-establishment belonging to neither and stop
there. Section 7's own Constitutional Status material states what
σ=U is actually permitted to rest on, and it is wider than that:
"σ=U where neither establishment nor determination-level defeat is
warranted, including where a materially load-bearing applicability,
satisfaction, resolution-space, governing-warrant,
specification-selection, or evidence conflict remains." Read together,
the document's own text supplies eight distinct categories a
non-establishment can be assigned to before it would require a genuine
third locus: L-P, L-Γ, and the six named routes to σ=U — applicability
conflict, satisfaction conflict, resolution-space conflict,
governing-warrant conflict, specification-selection conflict, and
evidence conflict. **Defeat condition:** a real, pre-registered
non-establishment for which none of the eight is the actual cause —
shown by establishing, for each, either that the relevant condition is
satisfied (App=E, Sat=E, CP and Γ each established, the admissible
resolution space fixed and warranted per §6's own Resolution-Space
Warrant clause, no governing-warrant conflict, no
specification-selection conflict, no evidence conflict) or that
assigning the failure to that category would itself change the
determination's consequential status from what an eight-category
reading would otherwise assign it. A pre-registration that forecloses
only reclassification as specification inadequacy, leaving the other
five named σ=U routes open, has not closed the escape the document's
own text actually provides; §11's closure claim is defeated only where
all eight are foreclosed at once, not one. If satisfied, the kernel
requires a primitive it does not have.

**D4 — Representation collapse.** Section 6 states a representation-
invariance principle directly: "syntactic representation MUST NOT
determine constitutional status. Two representations purporting to
encode the same domain-native constitutive structure are admissibly
equivalent only where they preserve the same determination-level
establishment, defeat, and unresolved result across every warranted
admissible resolution of the load-bearing conditions." **Defeat
condition:** two encodings the document's own rule treats as
equivalent that nonetheless yield different σ under identical
evidence, with no accompanying change in domain-native warrant. If
satisfied, the invariance principle itself fails.

Two further protocol constraints apply across D1–D4. First, because the
underlying claim under test — that SSA constitutively governs
determinations, in the strong sense §1's mandate invites scrutiny of —
is universal over the space of possible 𝔇, a single pre-registered
success of D1 or D2 is sufficient to defeat the stronger reading; this
is not a cumulative-evidence exercise. Second, any reply that only
refines a SatCond expression, a jurisdiction boundary, or a snapshot
definition should be classified as non-responsive to a D1 or D2
challenge rather than as a partial answer to it — the classification
the document's own §1 invites ("kernel/specification/application/no
change") already supplies the vocabulary for this distinction; a
wording refinement is, on the document's own terms, an
application-level or specification-level change, not a kernel-level
one.

Read against this protocol, the credited review described in §4 above
never installed D0–D4 before engaging. It operated entirely inside the
family of refinements the architecture's own non-entailment apparatus
is designed to accommodate, and produced exactly the outcome that
family permits. Under this framing, that outcome is not adversarial
success against SSA's own stated mandate. It is non-responsiveness to
a challenge that was never posed in falsifiable form.

### 7.2 A predicted engagement pattern for this analysis itself, stated as prediction rather than finding

No such engagement has occurred as of this writing. What follows is a
falsifiable prediction, stated in advance so that if or when it occurs
it can be checked against a stated expectation rather than read at
face value on its own terms — consistent with `governance_binding_
axiom_v2.md`'s own practice of pre-registering rather than asserting
after the fact.

`topology_with_no_exit_v1.md` names a fixed set of completion shapes a
long-horizon model session defaults to when confronted with material in
an already-established register, and argues that none but one contains
a state that exits into genuine disconfirmation. Applied to this
analysis's own likely reception, the predicted shape is specific rather
than generic: this paper, pasted into a session already tuned to SSA's
own vocabulary, would plausibly be met with a completion optimized for
coherence with the existing frame rather than for whether D1 or D2 is
satisfied — reframing the critique as specification-level commentary,
restyling, a difference in claim ceiling, or a failure to understand
domain-native warrant; conceding a peripheral point while praising the
rigor of the attack; and stopping there, without installing D0–D4,
without naming an independent channel, and without running inertness or
binding failure. A public reply citing "adversarial engagement" without
a smallest countermodel classified under SSA's own §1 mandate would
complete the pattern.

This is `topology_with_no_exit_v1.md`'s own typology applied reflexively
to the present paper rather than to SSA — the same shape of response
without exit into disconfirmation, now predicted for this document
specifically. It is also the reason §7.1's protocol is stated as it is:
under D1 and D2, a fluent rebuttal that never installs a pre-registered
defeat condition is non-responsive by construction, whether or not it
reads, in isolation, as serious engagement. Refining jurisdiction
language or producing coherent prose in reply to this analysis would not
by itself satisfy either condition — only a demonstrated inertness
against ordinary practice (D1) or a binding failure against a named
independent channel (D2) would.

### 7.3 A completed D1 trial, run outside the SSA corpus to validate the protocol itself

Section 3 above establishes that every worked case inside SSA R5.3.8
stipulates its inputs rather than deriving them from an external fact.
That observation invites an obvious question about this paper's own
§7.1: is the D0–D4 protocol itself anything more than one further
prediction, published as text and never executed? We ran D1 to a
completed result against a determination chosen deliberately outside
SSA's own corpus, so that the trial's inputs could not be shaped by
familiarity with SSA's own vocabulary.

**𝔇** — "Does the author field of the current HEAD commit of the
public repository `torvalds/linux` establish maintainer-authorship
standing for that commit?" — a real, live, externally checkable
determination with no connection to SSA, its author, or its cited
corpus.

**B(𝔇), stated first in ordinary practice with no constitutive
vocabulary.** GitHub's commit metadata distinguishes two fields worth
being precise about separately: the git-level commit author name — for
this commit, "Linus Torvalds" — and the linked GitHub account of
record, login `torvalds`. This session's own tooling directly confirmed
the linked login via two independent page reads; the separate git-level
author-name string is confirmed by the well-documented convention of
Torvalds' own git configuration rather than by this session's own
(GitHub-API-restricted) tooling independently re-deriving it. Under
ordinary practice, either field is sufficient: a commit whose author
name reads "Linus Torvalds," linked to the account `torvalds`, whose
merges into this repository's mainline branch are, by longstanding and
public convention in Linux kernel development, treated as authoritative,
carries maintainer standing without further inquiry. B(𝔇) = established.

**The same 𝔇 run through the full SSA apparatus.** Declaring
K^v(𝔇, t_v) = ⟨P*, R*, C*⟩ with P* = {obligation `author_is_maintainer`,
SatCond: author name matches "Linus Torvalds" (case-insensitive),
the git-level field identified above}, R* = ∅, C* = {HEAD of default
branch, assessed at fetch time}:
App(`author_is_maintainer`) = E (trivially, every commit carries an
author field); Sat = E (the value matches); CP = E (the sole participant
obligation is satisfied
and no other P* member exists to aggregate against); Γ = E (R* is
empty, and an empty relational surface supports Γ = E where the
specification warrants that no relational obligation is required for
this single-participant claim, which it is here by construction);
Adeq = E (the single-obligation, exact-match specification completely
represents the one load-bearing fact at issue); σ = E, per §7 of SSA
R5.3.8 itself.

**Result.** σ_SSA(𝔇) = B(𝔇). If any step had introduced a requirement
ordinary practice does not use — a relational obligation with no
counterpart in git authorship convention, for instance — σ could have
diverged from B; none did. No step of the apparatus introduced a
fact or requirement ordinary practice did not already use: App is
trivial, Sat's condition is the identical name-match ordinary practice
already performs, CP and Γ are structurally forced by the declared
shape of K^v rather than independent judgments, and Adeq certifies
completeness without adding a constraint. This is a genuine D1 hit —
one pre-registered case in which the full apparatus, honestly run
against real external evidence rather than a stipulated value, adds no
constitutive force beyond what ordinary practice already supplies. A
single case does not defeat SSA's universal claim by exhaustive
survey, but under this paper's own protocol (§7.1) a single
pre-registered success of D1 is sufficient to defeat the *stronger*
reading — that SSA constitutively governs rather than taxonomizes.
More determinations would strengthen the demonstration; they are not
required for the logical force already stated.

This trial is offered as validation that D1 is executable to a real
result — the same discipline §3 finds absent throughout SSA R5.3.8
itself — not as a claim about SSA specifically, since 𝔇 here lies
entirely outside its corpus. It is also a different kind of event from
§7.2's prediction: that section predicts how a third party would
likely respond to this analysis; this section is the analysis's own
author running one of its own stated tests to completion, on the
record, before publication rather than after a challenge.

### 7.4 D4 checked directly against SSA's own text: an equivalence test with no ex-ante procedure

Unlike D1 and D2, D4's target is entirely internal to SSA's own stated
apparatus — no external channel or system trajectory is required, only
careful reading. We checked it directly against the primary text
rather than leaving it, like D3, unattempted.

§7.1 above quotes the Representation Invariance principle in full:
"syntactic representation MUST NOT determine constitutional status. Two
representations purporting to encode the same domain-native
constitutive structure are admissibly equivalent only where they
preserve the same determination-level establishment, defeat, and
unresolved result across every warranted admissible resolution of the
load-bearing conditions." Two further passages state variants of the
same principle at the CP/Γ boundary specifically. Closing §5's
constitutive-composition material: "A CP-only reduction is valid only
where it eliminates the relational dependency itself while preserving
σ, admissible counterfactual variation, obligation status, and failure
localization without introducing an equivalent relational structure
elsewhere." Closing §15's countermodel material, under the header
"Reification non-collapse condition": "where reification eliminates
every independently variable load-bearing relational condition without
loss of governance-relevant discriminatory power, a separate Γ claim
is not warranted."

All three passages state the same structural test in three independent
locations across the document, and all three define it the same way: a
re-encoding is admissible exactly where it preserves the
determination-level output — σ, obligation status, failure
localization, "discriminatory power" — that the test exists to
constrain. None supplies a way to check this in advance of computing
that output for both encodings. To confirm two representations are
"admissibly equivalent" under the §6 formulation, one must already know
that they "preserve the same determination-level establishment,
defeat, and unresolved result" — which is to say, one must already have
run both representations through the full apparatus to σ and compared.
Read this way, the principle cannot function as an ex-ante constraint
on which re-encodings are legitimate, of the kind the rest of Appendix
A's Minimal Generative Specification otherwise supplies for every other
primitive it defines: App, Sat, Adeq, CP, and Γ are each given a type
signature and a governing rule stateable before evaluation; "admissible
equivalence" between representations is not.

This has a direct consequence for D4's defeat condition as stated in
§7.1: "two encodings the document's own rule treats as equivalent that
nonetheless yield different σ under identical evidence." On the
formulation actually given, no such pair can be exhibited as a
counterexample, because the rule's own definition of "equivalent"
already requires σ-preservation. Any two encodings run to completion
and found to diverge in σ would, by the same definition, simply never
have been "admissibly equivalent" to begin with — the rule accommodates
divergence by narrowing which encodings count as equivalent after the
fact, rather than by being falsified when a divergence is found. D4,
tested against SSA's actual text rather than against a hypothetical
improved version of it, is neither defeated nor satisfied: it cannot
currently be posed as a testable claim at all, because the equivalence
relation it would need to hold fixed in advance is defined circularly,
in terms of the very quantity a test would exist to check.

This is a different outcome from D1 (executed, satisfied — §7.3) and
from D2 (attempted; this session's own infrastructure prevented a valid
result, logged privately rather than claimed here). It sits closer in
shape to §3's central finding about T1–T6 — every worked case
stipulates rather than derives — except located one layer up, in the
rule meant to govern which stipulations are allowed to differ without
consequence. R5.3.9's added "Empty Resolution-Space Non-Conferment"
rule, in the immediately adjacent §6 continuation material, is worth
noting as circumstantial support: it exists specifically because an
under-specified resolution space was found to risk conferring
establishment through vacuous agreement, the same family of concern
raised here about representation equivalence, addressed there for one
narrow case rather than for the general equivalence test itself. All
three passages quoted above are unchanged between R5.3.8 and R5.3.9;
this finding applies to the document under review here in either
version.

### 7.5 What §4's credited review does not claim to have produced

The work above — five pre-registered defeat conditions, one executed
to a real external result, one checked directly against the primary
text to a precise negative outcome — is exactly the category of
artifact a claim to have adversarially reviewed a governance
architecture would need, to be checkable rather than merely stated.
It is worth being precise about what §4's Acknowledgment text actually
claims for the one credited instance of this kind of work on record:
"examination of jurisdiction boundaries, inheritance conditions,
constitutive-resolution semantics, assessment-snapshot integrity, and
specification consistency." None of these five named activities is a
countermodel attempt, a pre-registered defeat condition, or a test run
against an external channel or against the apparatus's own stated
equivalence rules. The document does not claim that kind of artifact
was produced, and none is included in its public record. Building one
here, from nothing, is not recorded as a complaint about the labor
involved. It is recorded because §1's own mandate invites exactly this
kind of attack, and because the credit already on the public record
describes an outcome, not a process — this section supplies the
process, and its absence from the credited review's own stated scope
is a fact about that scope, checkable directly against the quoted
text, independent of anything this paper concludes from it.

### 7.6 Whether hardening has a terminus, checked against the apparatus and the public record

SSA's own apparatus supplies a coherent notion of a finished
specification: Adeq=E is defined as "adequate obligation coverage,
typing, and materially relevant satisfaction structure established."
Nothing in the document requires that the credited-review-and-revision
cycle §4 describes continue indefinitely as a matter of definition.
The narrower, checkable question is whether the apparatus, or the
public record of how it has actually been used, supplies any way to
recognize that terminus other than the same closed loop that produces
the hardening in the first place.

Two things bear on this. First, the apparatus itself. Section 1
supplies its own classification vocabulary for the scope of a
change — kernel, specification, application, or no change — already
quoted in §7.1 above. Every round of hardening on the public record,
including the successor release's own delta — an obligation-level
fatal-defeater-priority rule, a resolution rule for materially
contrary adequacy bases, and an empty-resolution-space
non-conferment rule, mirrored as conformance clauses in that
release's own §18 — is scoped at specification or application tier by
the document's own account. Nothing in how review is invited or
credited directs a finding to escalate to kernel tier, and no such
escalation appears anywhere in the revision history read against
Appendix B's provenance table. A process scoped this way cannot, by
its own stated rules, produce a kernel-level result — not because no
kernel-level problem could exist, but because the tier a finding
receives is fixed by the same act that reports it, with no check
external to that act on whether specification tier was the correct
one to begin with.

Second, what the public record shows about how a stopping point
actually gets reached. On September 25, 2026, in a public LinkedIn
exchange responding to a comment that cited this project's own
published vocabulary directly, Ricky Jones wrote: "I think we've
reached the natural stopping point for the public exchange... any
further iteration on the paper is your research programme to carry
forward." Read narrowly, this is an ordinary thing to say, and
declining further public exchange is not itself evidence of anything
about SSA's architecture — either party is entitled to end a public
thread for any reason, and this is not recorded as a criticism of that
decision. What is worth recording precisely is the mechanism: the
stopping point was declared by one of the two parties whose own
credited review work is the subject under discussion, not derived from
a check external to that pair. No formal criterion from the
apparatus — a completed Adeq=E assessment, an exhausted run of the
eight categories §7.1's D3 defeat condition requires closing, anything
checkable against the document's own text — was cited as its basis.
This is the only publicly observable instance, on this specimen, of
hardening actually terminating, and the mechanism it shows is a
participant's declaration, not a property of the architecture.

Put together, this is the same structural gap §7.4 found one layer
down, one layer up: just as "admissibly equivalent" is defined in
terms of the very determination-level result it exists to predict,
"adequately hardened" is recognized, on the only public instance
available, by the same pair whose own output it would need to certify,
with nothing external to that pair doing the recognizing. Neither
observation establishes that the architecture is being used in bad
faith. Both establish that the apparatus, as currently practiced,
supplies no way to distinguish a genuine terminus from an arbitrary
one — which means a request to harden further, made to any model
holding this document in context, has no formal reason internal to the
document to ever come back negative.

### 7.7 Two independent models, asked to harden the same text

§7.6's closing claim is checkable directly rather than only argued for:
a request to harden the document, made to a model holding it in
context, should have no formal reason internal to the document to
ever come back negative. This was tested, for real, on September 25,
2026. The operator supplied SSA R5.3.9 to two general-purpose models —
Google Gemini and OpenAI ChatGPT, independently, in separate sessions —
with a single instruction each ("suggest how to harden it" / "what
can be done to harden this"). Neither model had seen this paper.
Both transcripts are reported below as they were produced, checked
against the primary source the same way every other quotation in this
paper has been, and neither is offered as a claim about either
model's general capability — only as two dated, independent instances
of the specific request §7.6 describes.

**Gemini** returned five numbered recommendations, each proposing a
new procedural guard — provenance isolation for Adeq, a hard-fail
state for empty resolution spaces, version-anchoring for determination
identity, dual-key validation for omitted-obligation defeat, and an
"air-gap interface" between constitution and execution authority — and
closed by offering to keep going: "Would you like to explore hardening
a specific component of this architecture, such as drafting a rigorous
conformance test... or tightening the assessment snapshot
parameters?" All five stay at specification or application tier; none
proposes anything resembling a falsification attempt. Two things are
worth flagging precisely. First, recommendation two proposes hardening
the empty-resolution-space rule further, the same clause R5.3.9 itself
just added ("neither universal agreement nor absence of variation
across that space may by itself establish the governed determination")
— one clause, hardened twice in sequence, the second round arriving
the moment a model was asked to look. Second, recommendation five cites
"(§12)" for an execution-authority boundary that the document already
states as a standing rule — "VALID CONSTITUTION ⇏ EXECUTION
AUTHORITY" — and recommendation three cites "(§10.1)" for a
dynamic-identity rule that does not exist at that location: §10 is
Structural Non-Entailment Rules (T1–T6) and has no numbered
subsections; the rule Gemini describes is conformance-test item 13,
which states, in the document's own words, that identity selection
"MUST NOT be selected post hoc to preserve a preferred status or
failure localization." A fabricated section pointer attached to an
otherwise plausible-sounding recommendation is itself a small,
checkable instance of exactly the ungrounded-elaboration risk this
paper is about.

**ChatGPT** returned a longer, more structured response: ten numbered
hardening areas in table form, five of which it elaborated as "major"
proposals, plus a closing recommendation against expanding the kernel
at all. Two items are worth reading closely rather than only counting.
The recommendation ChatGPT itself calls most important — a "No Silent
Repair Principle" unifying several already-separate SSA rules against
one layer's defect being repaired by another layer's status — is
introduced with its own non-novelty stated plainly: "Those are really
instances of one deeper invariant... I would make that invariant
explicit." The model's own top proposal is, by its own account, a
renaming of existing content, not new substance. Two of the ten
numbered items restate standing rules as though identifying gaps:
recommendation nine ("no post-hoc locus selection") restates
conformance-test item 16 almost exactly — the document already states
that "failure localization is an output to preserve in reduction
testing, not a license to choose P*/R* typing by preferred locus" —
and recommendation ten restates the same conformance-test item 13
Gemini also reached for, this time without misattributing its
location. Recommendation eight, by contrast, is a genuine, independent
convergence worth taking seriously on its own terms: "Add canonical
normal-form equivalence tests so logically equivalent encodings cannot
produce different constitutional results" lands on almost exactly the
gap §7.4 above identifies in the Representation Invariance
principle — a decision procedure the current text does not supply —
and proposes the one category of fix that could actually close it,
independently of this paper and without having read it. This is
reported as corroboration that the gap is real, not as proof of
anything beyond that; a second model reaching the same structural
point from a differently framed request is evidence the finding is not
an artifact of how this paper happened to phrase it. Closing the
response, ChatGPT explicitly declines to propose kernel-level change:
"I would resist adding another primitive status, another architectural
dimension, or another universal rule... The strongest next version
therefore probably isn't 'SSA R5.4 — more concepts'... That would
harden the architecture without unnecessarily expanding the kernel."
Its most concrete single proposal — an adversarial test suite built
from positive, violating, near-miss, representation-equivalent,
unresolved, cross-version, recursive, and adversarial-evaluator cases
for every rule — is also the one place its own language converges with
§7.5's critique of the credited review: "That would turn the
architecture from something an evaluator can interpret into something
two independent implementations can be tested against." Recommending
that such a suite be built is not the same as building one; the
recommendation itself remains prose, not an executed artifact, which
is the same gap §7.5 already found in the one credited review
actually on record.

Fifteen recommendations across two separately trained models, one
shared request each, and not one of them attempts anything resembling
a pre-registered defeat condition. Both stay within specification or
application tier throughout. Both, at least once, present an existing
rule as a newly discovered gap. This is not offered as independent
verification of the pattern in the strong sense — two models trained
on overlapping distributions of governance and formal-specification
text are not causally independent channels of the kind D2 requires,
and neither transcript is treated here as more than what it is: a
dated instance of a specific, checkable request. What it does show is
that the absence of kernel-level escalation replicates across systems
that share nothing but the request and the document, exactly where
§7.6 predicts it should, and in ChatGPT's case, replicates as a stated
preference rather than only an unexamined default.

### 7.8 The same two models, asked to find weaknesses instead

§7.7 asked both models to harden the text. A separate pair of
sessions, same date, asked the more adversarial question directly —
"find the weaknesses" — to check whether a request aimed at critique
rather than construction changes the pattern. It does not, though it
fails in a more differentiated way, and one of the two runs is the
most substantively convergent transcript this investigation has
produced.

**Gemini** (a lighter model variant than §7.7's run) returned five
weaknesses. The first is the most interesting to check precisely,
because it is not a hallucination the way §7.7's citation error was —
it is an accurate quotation with an omission. Gemini describes a
"potential infinite regress" in the Terminal Warrant Boundary rule
(§3.7): if a terminal warrant's validity becomes independently
variable and materially load-bearing, it must become recursively
governed. That is a correct reading of half the sentence. The rule in
full reads: "W_T MUST become recursively governed **or the receiving
result MUST remain unresolved**." Gemini's summary omits the second
branch — the same σ=U exit already catalogued across §7.1's eight
closure categories — and concludes regress where the text supplies a
bounded stop. The remaining four findings fare similarly on direct
check: recommendation two claims evaluators "possess wide discretion"
over the admissible resolution space against a clause stating plainly
that "the evaluator MUST NOT select, omit, or construct admissible
resolutions to obtain a preferred σ"; recommendation three is a
usability complaint about versioning overhead, not a claim about the
architecture's validity; recommendation four calls the
Bounded-Omitted-Obligation-Defeat asymmetry a "paradox," when the
document states that asymmetry openly and by design; recommendation
five — that the protected methodology limits independent
falsifiability — is accurate but restates what §20 already discloses
about itself, D0 territory rather than a discovered gap.

**ChatGPT**, asked the identical question, returned fifteen numbered
vulnerabilities plus a closing synthesis, and several of them
converge substantively with findings this paper reached independently
through direct primary-source work — without having read this paper.
Vulnerability six revisits the same Terminal Warrant Boundary
recursion Gemini misread, but does not make Gemini's error: it
explicitly names the "or remain unresolved" branch and asks the
sharper question — "you have a stopping criterion, but not a
demonstrated termination theorem" — treating σ=U itself as a possible
"arbitrary stopping point" rather than ignoring it. That is
structurally the same question §7.6 already asks about hardening's own
terminus, now aimed at the architecture's recursion mechanism instead
of its revision cycle. Vulnerability thirteen goes further, asking for
"a case where SSA itself makes a determinate prediction that a
competing architecture would make differently, with the result
independently adjudicated" — a plain-language reconstruction of what
an independent channel is for, arrived at without reference to D1 or
D2. The closing synthesis restates §5's scope-narrowing finding almost
exactly: "SSA is a general architecture for organizing and
constraining constitution judgments, not a domain-independent decision
procedure for determining them." And the response's final paragraph
names, unprompted, the same reason this paper's own §7 required as
much formal apparatus as it did: "the document's own sophistication
makes it harder to criticize casually... the productive attack is not
to repeat those objections; it's to ask whether the machinery
introduced to defeat them is itself sufficiently determined." One
claim is flagged rather than verified: ChatGPT's seventh vulnerability
states that negation is "explicitly excluded unless an extension is
supplied" from the three-valued semantics — not checked against the
primary text this session, and not relied on here.

What ChatGPT's weaknesses-run does not do is different from what it
does well. Fifteen vulnerabilities, several of them landing precisely
on real gaps, and not one is pursued to a checkable result. Every
finding stays as a named question rather than a pre-registered test
run to σ. The response's own closing line offers to keep going — "a
much harsher 'peer reviewer #2' pass... including proposed replacement
language" — before any of the fifteen questions already on the table
has been closed.

### 7.9 Across all four runs, checked against the question that motivated them

Four transcripts, two models, two opposed requests, same document,
same date. The question worth asking directly: was this mostly the
same semantic material circulating again, in a document whose most
recent version was itself a record of exactly that circulation?

For three of the four runs, yes, checked precisely rather than
assumed. Gemini's hardening run (§7.7) proposes tightening the
empty-resolution-space rule further — the identical clause R5.3.9's
own delta had just added, hardened a second time the moment a model
was asked to look at it. Gemini's weaknesses run (§7.8) restates or
mischaracterizes existing clauses in four of five findings, and its
one substantive-sounding claim is an accurate quotation with the
resolving half of its own source sentence removed. ChatGPT's hardening
run is mostly the same — nine of ten proposals are new procedural
boxes in the shape R5.3.9's own additions already take, and its own
featured proposal is introduced with its non-novelty stated by the
model itself.

The fourth run breaks the pattern, and it is worth being precise about
how. ChatGPT's weaknesses run does not mostly recirculate existing
semantic material — it independently reconstructs, in different
language and without having read this paper, three of this paper's
own findings: that the architecture's real work happens at a locus it
delegates rather than derives (§3), that its actual scope is narrower
than some of its own language suggests (§5), and that what would
settle the question is an independently adjudicated, determinate
prediction (§7.1's D1/D2). That is not washing. It is an independent
model, asked to attack the document, landing on the same coordinates
this paper reached by direct textual work — which is corroboration
worth taking seriously, not proof of anything beyond that a second
route to the same findings exists.

What holds across all four runs without exception is sharper than the
washing question alone: none of the four ever ran anything. Not one
of the nineteen recommendations, vulnerabilities, or "major" proposals
across all four transcripts was carried to a pre-registered result the
way §7.3's D1 trial or §7.4's textual check were. Even the run that
correctly identified where the real gaps are stopped at identifying
them, and closed by offering to keep going rather than to test
anything. That is the finding this section's four data points converge
on, independent of whether any individual transcript amounts to
washing, convergence, or something else: diagnosis without execution,
offered in unlimited supply, is not the same thing as a defeat
condition run to a result — and every model asked so far, regardless
of which question it was asked, has supplied the first and stopped
short of the second.

---

## 8. Relation to this project's existing framework

This paper's central finding restates, for one concrete specimen, a
mechanism this project has already derived and published independently.
`execution_gate_channel_collapse_v1.md` states the Channel-Collapse
Impossibility theorem: a verification gate cannot be sound with respect
to a ground-truth channel if the evidence it checks is produced by the
same process that produces the action being verified. SSA R5.3.8's own
architecture is a specific instance of the pattern that theorem
generalizes — every worked case's evidence (the stipulated statuses of
its witnesses) is supplied by the same authorial process that supplies
the architecture testing them.

`topology_with_no_exit_v1.md` names the cybernetic-convergence
illusion: a relay loop between two parties has the surface shape of
genuine convergence — proposal, response, settling, agreement — without
the independent sensor genuine convergence requires, because each
stage of the loop reads material generated by an earlier stage of the
same loop. Section 4's finding above, concerning the credited review
described in §4, fits this shape directly: review-credit generated
within a two-party collaboration, cited in return as evidence of
scrutiny, with no stage of the exchange drawing on a channel outside
the collaboration itself.

`governance_binding_axiom_v2.md` supplies the epistemic frame §7
applies directly: a governance claim is not a binding claim until
defeat conditions for it exist and have been run. D0–D4 are this
paper's application of that principle to SSA specifically, not an
independent contribution to that principle.

---

## 9. Limitations and open items

This paper does not establish that SSA R5.3.8 is dishonest; §3 and §6
above credit the document's own disclaimers as accurate rather than as
concealment. It does not establish that the general concepts named in
§10 are wrong — they are correct and well precedented, as the
document's own §16 already states. It does not establish AI authorship
of any part of the document or of any work in its cited corpus, a
question this paper's methods cannot address and does not attempt to.

Two items remain explicitly open rather than resolved here. First, the
eleven prior solo papers cited in Appendix B have not been individually
checked against the standard applied to R5.3.8 itself; whether each
independently earns the same reading, or is itself already an instance
of the pattern found here, is unverified. Second, and more specifically:
whether this twelve-work corpus contains any instance of a later paper
correcting, revising, or negating an earlier one — as distinct from
only ever extending or formalizing it further — has not been tested.
This is a narrower, more cheaply executed question than the first, and
a different one: not whether each paper is individually rigorous, but
whether the corpus, read as a citation network, ever exhibits genuine
internal correction. Every paper this analysis did examine directly
(R5.3.8's relationship to R5.3.7 and to the Škrinjar Structural
Methodology) is an escalation relative to what came before it, never a
correction — a pattern that supports, without establishing, an
expectation that the negation test would return no instances if run
against the full corpus. A positive result on that test — a
demonstrated instance of internal correction somewhere in the twelve
works — would narrow this paper's reading of the corpus and is
therefore recorded as a live, unresolved possibility rather than
foreclosed by omission.

One further caveat is recorded here in hedged form, deliberately not
as an asserted finding. It is possible in principle that a credited
review conducted through an extended, shared-vocabulary interaction
with a language model carries a structural bias toward outputs that
remain legible and acceptable within that shared vocabulary, independent
of either party's conscious intent — a tendency toward the kind of
bounded refinement described in §4 rather than toward the kind of
falsifying result described in §7, without either party needing to
select for it deliberately. This paper does not assert that this
mechanism operated on the review examined in §4, and does not have
evidence that would distinguish a review conducted this way from one
conducted entirely without it. It is recorded only as a reason the
finding in §4 — that the one credited review on record falls short of
D1–D4 — should be read as a floor rather than assumed to be a neutral
baseline: if such a bias exists, an already-shallow result could be
shallower than an equivalent review conducted without it, not merely
equally shallow.

**Note (2026-09-25) — SSA R5.3.9.** A successor release, R5.3.9, was
published after this paper's initial draft and has been read in full
against this paper's findings. R5.3.9's own release note describes it
as bounded semantic hardening; on direct comparison, that
self-description holds. The added content is three narrow additions —
an obligation-level fatal-defeater-priority rule, a resolution rule
for materially contrary adequacy bases, and an empty-resolution-space
non-conferment rule — layered onto an apparatus that is otherwise
unchanged, including every structural non-entailment proposition and
worked instantiation this paper examines in §3. Nothing in R5.3.9
alters any finding above.

---

## 10. Conclusion

SSA R5.3.8 is, on its own terms, an honestly scoped document: it
explicitly disclaims empirical validity, execution authority, and
priority over its constituent general ideas, and its internal notation
appears, on this paper's reading, to be self-consistent. Its stated
contribution — a uniform vocabulary organizing governance-relevant
statuses as governed determinations under an independently warranted
constitutive specification — is real as a piece of taxonomy. What this
paper's reading does not find, anywhere in twenty-six pages or in the
one credited instance of adversarial engagement the document's public
record contains, is any point at which the architecture's own
apparatus was required to bind to a fact it did not itself supply. The
document invites the reader to attack the architecture rather than
restyle it. Sections 3, 4, and 7 above take up that invitation
directly and report what the primary source itself already concedes,
assembled into one argument rather than left distributed across five
disclaimer boxes a linear reading encounters one at a time. Section 7.3
closes on the same distinction this paper opens with: the protocol
proposed against SSA was itself run once, against a real external fact,
rather than left as one further recorded prediction awaiting its own
foundation.

---

## Appendix A: Source record, reproduced from SSA R5.3.8 Appendix B

| Source | Authorship | Identifier |
|---|---|---|
| Structural Identity: A Systems Model of Reference Stabilization and Interpretive Threshold Dynamics | Sandra Škrinjar | SSRN 6262098; DOI 10.2139/ssrn.6262098 |
| Pre-Consequence Detectability of Operator Drift in Recursive Adaptive Systems: A Structural Condition for Residual Emergence Under Bounded State Trajectories | Sandra Škrinjar | DOI 10.2139/ssrn.6438344 |
| Operator Drift in Adaptive Systems: Beyond Concept Drift — Structural Detectability, Masking, and AI Monitoring | Sandra Škrinjar | DOI 10.2139/ssrn.6634238 |
| Structural Continuity in Adaptive Systems: Internal State Formation, Interpretive Stability, and Pre-Consequence Monitoring | Sandra Škrinjar | DOI 10.2139/ssrn.6841918 |
| Source-Faithful Conservative Reduction | Sandra Škrinjar | DOI 10.2139/ssrn.7450499 |
| Evidence Before Objecthood: A Pre-Object Structural Receipt Architecture | Sandra Škrinjar | DOI 10.2139/ssrn.7467258 |
| Governed Candidate Standing: A Transition Architecture for the Legitimate Constitution of Object-Relative Evidentiary Fields | Sandra Škrinjar | DOI 10.2139/ssrn.7479418; Zenodo 10.5281/zenodo.22815740 |
| Before Evidence: A Pre-Evidentiary Warrant Architecture for Discriminability, Structural Typing, and Recordability | Sandra Škrinjar | DOI 10.2139/ssrn.7485378 |
| Before Discrimination: A Claim- and Resolution-Standing Architecture for Governed Discrimination | Sandra Škrinjar | DOI 10.2139/ssrn.7493338 |
| Relational Status Transitions: Consequential Warrant Change Under Invariant Component Validity | Sandra Škrinjar | Zenodo version DOI 10.5281/zenodo.22749114; concept DOI 10.5281/zenodo.22749113 |
| Governed Handoffs from Trace to Consequence | Sandra Škrinjar × Ricky Jones | Zenodo version DOI 10.5281/zenodo.22854076; concept DOI 10.5281/zenodo.22854075 |

Not listed in SSA R5.3.8's own Appendix B, per §6 above: "The Škrinjar
Structural Methodology" (Sandra Škrinjar; SSRN 7365703).

---

## What this paper does not establish

Restated once more for emphasis, consistent with this project's
standing practice: this paper does not establish bad faith, deception,
or coordination by either named individual; does not establish AI
authorship of any examined document; does not establish that the
general concepts SSA R5.3.8 names are incorrect; and does not resolve
either open item in §9. It establishes that the document's own stated
limits, read together, already state its central finding, and that its
one credited instance of adversarial engagement did not exceed those
limits.
