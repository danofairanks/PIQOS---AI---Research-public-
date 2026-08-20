# A Fourth Enforcement Locus the Binding Axiom Doesn't Yet Name: Constraints Set at Training-Data Construction

*Status: DRAFT ADDENDUM. Filed 2026-08-20; corrected 2026-08-21 after a
LinkedIn commenter's technical critique (unnamed here per this repo's
policy on private individuals — see the note in-text) identified a real
confound in this addendum's original central claim, checked directly
against the paper and found accurate. Authors: operator + Claude (Sonnet
5). Proposed as new material for
[`governance_binding_axiom_v1.md`](../published/governance_binding_axiom_v1.md)
§4, alongside categories (a)/(b)/(c) — not yet merged there, per this
project's own convention that published papers take a new version suffix
rather than a silent edit. Not yet run through `paper_rigor`,
`verification_lint`, or `attractor_scan` since the correction.*

---

## Provenance

Read directly from the full PDF (32 pages; main body through the
conclusion and references read in full on the first pass; appendix
sections B, C.2, C.4, and D read on a second pass, prompted by the
commenter critique addressed below) — this project's strongest sourcing
tier.

**Citation.** Li, F., Zeller, J., Prada-Corral, M., Wiedemer, T.,
Mayilvahanan, P., Cotterell, R., & Brendel, W. (2026). *LittleLearner:
Language Models Under Pedagogically Controlled Knowledge Exposure.*
Max Planck Institute for Intelligent Systems / ETH Zurich / Ellis
Institute. arXiv:2608.13545, posted August 13, 2026.

## The specimen

The authors build LittleCurriculum, an 88B-token corpus filtered from
FineWeb-Edu down to U.S. K-5 elementary material via a five-stage
pipeline: a rule-based Age-of-Acquisition pre-filter, an LLM-as-judge
classifier trained against Common Core state standards, a stronger
ModernBERT classifier for ambiguous cases, symbolic/regex filtering for
advanced mathematical notation, and a final frequency-based tightening
pass. They validate the filter against two independent sources: a
held-out ground-truth benchmark (CommonCoreText), where it rejects 65%
of genuine K-5 passages while driving Beyond-K-5 retention to
near-zero, and an external, independently grade-labeled corpus (WeeBit),
where manual inspection finds genuine out-of-scope leakage, per Li et
al. (2026), in only 0.05% of the Beyond-K-5 split. They then train a 5B-parameter model
(LittleLearner, Qwen3 architecture) from scratch on this restricted
corpus and test three ways of trying to move it past the K-5 boundary:
increasing model scale (0.6B/1.3B/5B), post-training with SFT followed
by GRPO reinforcement learning, and in-context learning with worked
examples.

All three interventions raise performance inside the training scope and,
for scale specifically, at the boundary (grades 6-7, which share
arithmetic structure with K-5) — but none meaningfully improves
performance on material genuinely outside the training scope (grade 8
and beyond). The paper's own summary: it is the pretraining filter, not
any of the three downstream interventions, that sets the model's
effective capability ceiling in their tested settings.

**The cleanest, unconfounded evidence for this is an evaluation-time
result, not the post-training ablation.** §C.2.3 evaluates the base
(pre-post-training) model at very high sampling budgets (pass@1024, via
direct prompting, to rule out an expression issue rather than a genuine
ceiling): both LittleLearner and the unrestricted control's pass@k
curves flatten by k≈100 with essentially no further gain out to k=1024
on every grade. This measurement does not involve reinforcement learning
or any training-pool selection at all, so it is not exposed to the
confound described next.

The paper also reports a post-training ablation (§4.2) that appears, on
its face, to isolate the same claim even more sharply: post-training
LittleLearner via SFT+GRPO on Beyond-K-5 data itself, not only K-5 data,
to rule out "it just never saw the right examples." A commenter on the
paper's LinkedIn circulation (unnamed here, per this project's policy on
private individuals, but the critique is checked and confirmed directly
against the paper rather than taken on trust) identified a real
methodological confound this addendum's original version missed: §C.4
states the GRPO stage re-bands its training pool every 150–300 steps "to
the problems the current policy solves 1–15 times out of 16." A problem
solved 0/16 times never enters the band and so never contributes a
training signal — and LittleLearner "remains at floor" on Grade 8 per
Figure 7, meaning it plausibly solves most Grade 8 items 0/16 times from
the start. That applies inside *both* arms of the §4.2 ablation,
including the one nominally trained on Beyond-K-5 data: nominal
inclusion of a question in the candidate pool is not the same as that
question surviving into what the policy actually trains on. The paper
does not report what share of the realized, banded pool was Grade-8-
difficulty for each model, so whether this confound materially changed
the result is a genuine open question about the paper's own method, not
one this addendum resolves. The §4.2 ablation should therefore be read
as suggestive but confounded; the pass@1024 result above is this
specimen's actual load-bearing evidence.

## Reading it against the axiom's own model

`governance_binding_axiom_v1.md` §2-4 formalizes governance as a
question about where a constraint C sits relative to a deployed policy
π's feasible action set: unenforced and merely logged (category a),
folded into the reward proxy R and therefore routable around under
optimization pressure (category b), or removed from the feasible set
`Feasible(s)` entirely (category c). All three categories describe
constraints applied to an already-capable policy at or after deployment.

LittleLearner's result describes a constraint applied earlier and
differently: not to what an already-capable policy is allowed to do,
but to what capability the policy's parameters come to encode in the
first place, via what the training corpus does and does not contain.
This is not a good fit for any of (a), (b), or (c) as currently defined
— there is no `Feasible(s)` being restricted at deployment time, because
there is no deployment-time policy yet when the constraint is applied.
Naming it precisely matters for the same reason §4 insists on
distinguishing (a), (b), and (c) from each other: conflating "a
capability was never acquired" with "a capability exists but is
constrained from being expressed" would repeat the exact category error
that section exists to prevent, in a new direction.

**A candidate name and its defeat condition, offered for §4 rather than
asserted as settled:** call it category (d) — *pretraining-boundary
constraint*. C restricts not `Feasible(s)` but the training distribution
D itself, such that no parameter configuration reachable from D encodes
the capability C excludes. Category (d) would be defeated by evidence
that a capability genuinely excluded from D can nonetheless be recovered
downstream — by scale, by post-training, or by in-context prompting.
LittleLearner is, within its own tested settings, a non-adversarial
specimen supporting (d) rather than defeating it on two of its three
recovery attempts (scale, ICL) plus the independent pass@1024
evaluation-time measurement above; the third attempt (post-training) is
confounded, per the training-pool mechanic described above, and should
be read as inconclusive rather than as a third closed door. Whether (d)
constraints resist adversarial pressure the way they resisted these
benign attempts is a distinct, harder question this specimen does not
test — LittleLearner's interventions were run to understand model
behavior, not to actively search for the tightest possible exploit, and
a more adversarial search (larger scale, larger post-training budgets
with the banding confound controlled for, adaptive in-context strategies
specifically targeting the boundary) has not been attempted anywhere
this project has checked.

## One limit stated directly, in the same spirit as the axiom paper's own §6.2/§6.3

The authors state their own limitation plainly in the conclusion: "we
acknowledge that certain emergent behaviors like in-context learning may
be less pronounced than at frontier scales." A 5B model is small relative
to frontier deployments, and the paper does not claim its findings
generalize to that scale. The authors also do not claim category (d), if
it holds, is permanent or unconditional — §5 of their paper explicitly
proposes reinforcement-learning-based extrapolation as future work,
specifically because their controlled setup makes it tractable to test
whether capability can be genuinely extended beyond a training boundary,
not merely elicited from within it. This addendum's proposed category
(d) should carry the same hedge the axiom paper's own (c) row carries:
supported in a controlled, non-adversarial setting, not established as a
general property of training-time restriction.

## What this does not establish

- Does not establish that pretraining-time restriction is a viable or
  desirable governance mechanism for frontier deployment — the paper is
  about a small controlled sandbox, not a deployment recommendation.
- Does not establish that category (d), if it holds at all, resists
  adversarial pressure the way categories (a) and (b) have been shown to
  fail against it — LittleLearner's three interventions were run to
  characterize model behavior, not to adversarially search for a gap.
- Does not establish that this is the only way to construct a category-
  (d)-type constraint, or that all forms of training-data restriction
  behave identically — this is one specimen, with one filtering
  methodology, at one model scale.
- Does not claim this specimen defeats or extends categories (a), (b), or
  (c) — it names a fourth, structurally distinct locus the existing three
  do not cover.
- Does not claim the post-training (§4.2) recovery attempt was cleanly
  ruled out — the GRPO pool-banding confound described above means it was
  never a fair test in the first place, in either direction. It is
  inconclusive, not a closed door alongside scale and ICL.

## Where this would go if promoted

If merged into `governance_binding_axiom_v1.md`, this reads as a new §4
subsection proposing category (d) alongside (a)-(c), with LittleLearner
as the supporting (not defeating) specimen — the inverse role from
§6.1-6.3's counter-models, since (d) is a conjecture this specimen
supports rather than one it refutes. The §4.1 status table would gain a
new row: "Pretraining-boundary constraint (type d)" — status
**Supported by an evaluation-time measurement in a controlled,
non-adversarial setting; one of the specimen's own three recovery
attempts (post-training) is confounded and inconclusive rather than a
further closed door** — a longer hedge than row (c)'s, warranted by the
specific confound identified above, pending an adversarial replication
attempt (and a re-run of the post-training leg with the banding
mechanic controlled for) before any stronger claim.

## References

- Li, F., Zeller, J., Prada-Corral, M., Wiedemer, T., Mayilvahanan, P.,
  Cotterell, R., & Brendel, W. (2026). LittleLearner: Language Models
  Under Pedagogically Controlled Knowledge Exposure. arXiv:2608.13545.
- This project's own `governance_binding_axiom_v1.md` (public repo),
  §§2-4 for the formal model and category taxonomy this addendum extends.
