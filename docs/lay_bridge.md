# Basins Without the Mysticism: A Reading Guide for People New to This Repo

*Filed 2026-08-18. Authors: operator + Claude (Sonnet 5). This is not a
research paper — no new claim is made here that isn't already published
elsewhere in this repository. Its only job is to point a reader who
bounces off "basin," "attractor," or "coherence" at the actual papers
those words come from, and to state plainly what this project is and is
not claiming when it uses them.*

---

## What this page does not claim

(This section doubles as the "what this project is not claiming"
grounding the rest of the page depends on — read together, not
separately.)

Get this out of the way first, because it's the fastest way this
vocabulary gets misread.

- **Not** "the brain is a neural net," and not any claim about neurons,
  consciousness, or biology at all. **No paper in this repository makes a
  biological or neuroscientific claim.** Every mechanism described below
  is about how information — claims, evidence, output — behaves under
  repeated measurement, in a training run, a conversation, a research
  field, or a social network. That is the whole domain.
- **Not** a claim that every human habit is "model collapse," or that
  people and language models are the same kind of thing. Where this
  project does compare a human case to a lab case —
  [`register_invariance_self_falsification_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/drafts/register_invariance_self_falsification_v1.md)
  is the clearest example — it states directly what's claimed to
  transfer (a measurable pattern) and what isn't (register, aesthetic,
  institutional status). See its §1, which quotes
  [`mirror_test_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/published/mirror_test_v1.md)
  §5.1 directly: "The mechanism does not care about the aesthetic or the
  social status of the participants... The latter just has more
  resources to keep the story going."
- **Not** a moral verdict on anyone this project analyzes. Every case
  study and paper here separates a structural finding (does this claim
  survive contact with evidence?) from a claim about intent — see, for
  one dated example among many,
  [`case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md)'s
  explicit "not evaluated as bad faith."

## The shared object, in one paragraph

A **basin** is a state a system keeps returning to even after it's
pushed away from it. An **attractor** is what's inside the basin — the
specific claim, story, or output the system settles back on.
[`basin_attractors_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/published/basin_attractors_v1.md)
names nine such attractors in AI industry discourse specifically (§2) —
each one a load-bearing claim, paired with real counter-evidence and the
defensive move that keeps the claim standing anyway. None of this
requires the system doing the settling to be a mind. It requires only
that the system produce output, receive feedback on that output, and
weight future output by that feedback — true of a model in training, a
person in an argument, and a research community reading its own press.

## The actual bridge — with citations, not analogy

The table below maps a plain-language description to the specific
mechanism this project has already published for it. Every right-hand
cell links to where the claim is actually made and defended — this
project's own discipline (`CLAUDE.md`'s house conventions) requires that
of every claim it publishes, including this one.

| Plain description | Where this project actually says it |
|---|---|
| Fluent and internally consistent isn't the same as true | **Grounded vs. detached coherence** — [`mirror_test_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/published/mirror_test_v1.md) §4.1–4.2; extended in [`laundered_vocabulary_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/published/laundered_vocabulary_v1.md)'s Coherence entry, which grounds the distinction in three literatures that predate and don't cite this project — epistemological coherentism vs. correspondence theory, NLG fluency-vs-faithfulness research (Ji et al., 2023), and philosophy applied to LLMs directly (Hicks, Humphries & Slater, "ChatGPT is Bullshit," 2024). |
| A claim that's structured so nothing could ever count against it | **Defeat conditions**, and the requirement to state one before a claim counts as scientific under this project's own method — [`governance_binding_axiom_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/published/governance_binding_axiom_v1.md) §5; the same discipline as [`basin_attractors_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/published/basin_attractors_v1.md)'s Basin-Immune Falsification Protocol (BIFP) §3, Phase 0. |
| A safety rule that's recorded somewhere but doesn't change what actually happens, vs. one that does | **Three enforcement tiers** — zero-cost-but-logged, weak penalty folded into the reward signal, true hard constraint — [`governance_binding_axiom_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/published/governance_binding_axiom_v1.md) §4, with a stated, distinct defeat condition for each tier. |
| A community that looks self-critical but never questions its actual goal | **The Illusion of Dissent** — insiders disagreeing about means while agreeing on ends — [`mirror_test_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/published/mirror_test_v1.md) §5.6. |
| A vocabulary word borrowed from a real field to make a claim sound more rigorous than it is | **Semantic laundering** — [`basin_attractors_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/published/basin_attractors_v1.md) §2.8; the growing catalog of specific instances lives in [`laundered_vocabulary_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/published/laundered_vocabulary_v1.md). |
| A critique that gets produced and shared but never actually changes anything | **The Critique Basin** — circulation (signatures, likes, citations) rewarded independently of correction — [`critique_basin_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/drafts/critique_basin_v1.md) (draft), with a stated two-tier test for telling real correction apart from a pause that later resumes unchanged. |
| Who actually absorbs and reinforces a claim once it's made | **The five-ring model** — labs, capital, academic legitimacy, social consensus, end users — [`mirror_test_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/published/mirror_test_v1.md) §5.3, with the specific mechanism by which each ring absorbs friction in §5.4. |

## Why the same table works for a lab and a person

This isn't an assumption bolted on afterward — it's the specific,
narrow thing
[`register_invariance_self_falsification_v1.md`](https://github.com/danofairanks/PIQOS---AI---Research-public-/blob/Main/papers/drafts/register_invariance_self_falsification_v1.md)
sets out to test. It takes one real, dated small-scale case and one
real, dated lab-scale case and checks the *same* mechanisms above
against both, row by row (its own §2 table). What differs between the
two cases: register (technical polish vs. plain language), and which one
a reader dismisses on sight versus takes seriously by default. What
doesn't differ, per that draft's own explicit finding: whether the claim
is falsifiable, whether the surrounding community corrects it, and
whether it responds to challenge by engaging or by deploying one of
`basin_attractors_v1.md`'s cataloged defensive moves. That's a specific,
checkable claim about *this* case and *this* case only — not a general
license to read every human disagreement through this framework. The
draft's own §4 says so directly: no institution and no individual is
claimed to have failed this test; the point is that the same instrument
applies to both without modification.

## What the tools actually check for

The eight tools in [`tools/`](https://github.com/danofairanks/PIQOS---AI---Research-public-/tree/Main/tools)
(installable, and runnable directly in-browser via the
[Paper-Rigor Scanner](scan.html)) don't detect truth or falsehood — no
tool here claims to. They check for the *shape* of the patterns above:
whether a document states a defeat condition, whether a striking
statistic is cited, whether a formal-looking symbol is ever actually
derived, whether a claim of "Coherence" is used in the grounded or the
unfalsifiable sense. A flag from any of them is a lead, not a verdict —
every case study in this repository reads the matched text directly
before treating a flag as a finding, and says so.

## One-sentence takeaway

Every mechanism on this page was published, cited, and defeat-condition-
tested somewhere in this repository before this page existed — this
page adds no new claim, only a map from plain language to where the
actual claim and its evidence live.
