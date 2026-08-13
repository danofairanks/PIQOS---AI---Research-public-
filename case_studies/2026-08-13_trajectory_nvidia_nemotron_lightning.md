# Real-Time Specimen Analysis: NVIDIA's Multi-Lab Early-Access Pattern, Extended: Trajectory Labs' Nemotron 3.5 Lightning Post-Training Claim

### A smaller, more transparent instance of the same circular-partnership mechanism as the SSI deal -- and a rare specimen in this directory that substantially survives verification

---

## Executive Summary

On August 11, 2026, Trajectory Labs (@trajectorylabs) posted that it
received early access to, and post-trained, NVIDIA's newly-released
Nemotron 3.5 Lightning model on Harvey's LAB legal benchmark, lifting
its all-pass rate from 0% to 8.3% -- above Anthropic's Opus 4.6 at
6.6%. Checked directly against primary and independently-indexed
sources: the company, the model, the benchmark, and NVIDIA's own
acknowledgment of the partnership are all real and independently
corroborated -- a materially stronger evidentiary position than the
companion SSI-NVIDIA specimen in this directory, which carried zero
technical disclosure. The one figure that does *not* clear independent
verification is the headline number itself: the 8.3% result matches
Trajectory's own blog post exactly, and no third party has replicated
it. The specimen is logged less as a caution and more as a contrast
case: it extends this directory's documented NVIDIA multi-lab pattern
with a third instance, and it is one of the few specimens here where
"self-reported benchmark claim" turns out to be accurate rather than
inflated.

---

## The Specimen: What Was Posted

Trajectory Labs (@trajectorylabs), a verified X account, posted at
8:12 AM on August 11, 2026 (130K views, 32 reposts, 544 likes at time
of inspection):

> "Continual learning is a bet that the retraining loop will get
> cheaper over time. With larger models, you can maybe run this loop
> once every few weeks. But with smaller models, you can run it
> nightly, per customer. And it keeps recursing: a model per company,
> then a model per client that company serves, then per matter. We're
> getting closer to intelligence cheap enough to meter.
>
> On the path to this, we received early access to, and post-trained
> @nvidia's Nemotron 3.5 Lightning on @harvey LAB. One click on the
> Trajectory platform, no new engineering. 0% to 8.3%, above Opus 4.6
> at 6.6%."

The post includes a bar chart, "All-pass rate by model" ("Share of
held-out Harvey tasks where every rubric criterion passed"), showing:
GPT-OSS 120B 0.0%, base Lightning 0.0%, Trajectory-tuned Super 0.8%
and 3.3% (two data points), base Ultra 0.8%, GPT 5.5 3.3%, Sonnet 4.6
4.2%, Trajectory-tuned Ultra 5.8%, Opus 4.6 6.6%, and Trajectory-tuned
Lightning 8.3% (highest bar). A same-account follow-up reply, partially
visible, adds: "Lightning starts lower than other base models we tried
from Nvidia, yet ends higher, which is what [text cut off]."

## Checked Against Primary Sources

**Trajectory Labs is a real, funded company.** trajectory.ai is live;
the specific blog post the screenshot's figures come from is indexed
there. Founders (Ronak Malde, Michael Elabd, Arjun Karanam) carry
backgrounds at DeepMind, OpenAI, Meta Superintelligence Labs, Amazon
AGI, and Scale AI. The company raised a $15M seed (Conviction) and a
subsequent $40M round led by Sequoia (~$300M valuation). Reported
partners beyond Harvey include Clay, Decagon, Mercor, and Rogo.

**Nemotron 3.5 Lightning is a real NVIDIA release, and NVIDIA's own
materials corroborate the partnership.** The model (30B-parameter
MoE, 3B active, distilled from Nemotron 3 Ultra, agentic-focused) was
announced on or around August 11, 2026, covered by NVIDIA's own
developer and corporate blogs as well as CNBC, VentureBeat, and
Hugging Face (model card:
`nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B`). **NVIDIA's own
materials name Harvey and CodeRabbit as post-training partners on this
release** -- this is not a claim resting on Trajectory's word alone;
the vendor whose model is at the center of the claim independently
names the same benchmark relationship.

**Harvey LAB is a real, open-sourced benchmark.** Harvey's Legal Agent
Benchmark (LAB) was open-sourced May 6, 2026
(`github.com/harveyai/harvey-labs`; harvey.ai/blog): 1,200+ tasks,
75,000+ rubric criteria, graded on an "all-pass" standard requiring
every rubric criterion to pass for a task to count. Harvey has
separately partnered with Anthropic, OpenAI, and NVIDIA on this
benchmark, and third-party trackers (Artificial Analysis's "Harvey
LAB-AA" leaderboard, vals.ai/benchmarks/hlab) independently run their
own measurements against it -- the benchmark itself, unlike the
specific 8.3% claim, is not a Trajectory-only artifact.

**The specific percentages are accurate to Trajectory's own reporting
-- and that is precisely the limit of what is independently confirmed.**
Trajectory's own blog post states the same figures shown in the
screenshot: Nemotron 3.5 Lightning 0% -> 8.3%, Nemotron 3 Ultra
0.8% -> 5.8%, Nemotron 3 Super 0.8% -> 3.3%, against Opus 4.6 at 6.6%.
No independent third party was found replicating these exact numbers;
Artificial Analysis's own Harvey LAB-AA leaderboard is a separately-run
measurement, not a check of Trajectory's specific result. "Opus 4.6"
(Anthropic, released February 5, 2026) and "GPT 5.5" (OpenAI, released
April 23, 2026) are both real, released models as of August 2026 --
the comparison set is not fabricated or mislabeled, which narrows the
open question to exactly one thing: whether Trajectory's own
post-training pipeline produced the 8.3% figure it reports, which
remains self-reported and unreplicated.

## The Broader Pattern: A Third Instance, With More Disclosure Than the First

This directory already documents NVIDIA's circular multi-lab betting
pattern twice: the SSI-NVIDIA $5B partnership announcement
(`2026-07-27_ssi_nvidia_partnership.md`, diagnosed as "The Opaque
Promise" -- capital commitment with zero technical disclosure) and
Bloomberg's network graphic of ~20 companies bound by investment,
hardware, and service relationships with NVIDIA at the structural
center (`2026-07-28_nvidia_circular_deals_bloomberg.md`). Independent
research this session found the pattern is larger than either specimen
alone shows: beyond SSI, NVIDIA has struck a comparable early-access/
compute-supply relationship with Thinking Machines Lab (Mira Murati;
≥1GW chip commitment reported by Bloomberg and CNBC), alongside its
established backing of OpenAI, Anthropic, xAI, and Mistral --
reportedly approaching $53B across roughly 170 deals as of February
2026 (TechCrunch, "Nvidia's AI empire"). The Trajectory/Nemotron
relationship is a smaller-scale instance of the identical structural
pattern: a compute/model vendor providing early access to an
emerging company, positioned so that company's success is also a
demonstration of the vendor's product.

**What makes this instance worth logging as a distinct data point,
not just a fourth entry restating the same finding:** it inverts the
SSI specimen's central defect. The SSI announcement's diagnosis turned
on the *absence* of any technical disclosure -- capital commitment
standing in for evidence. Here, the opposite is true: a real benchmark
(Harvey LAB, independently open-sourced and separately tracked by
third parties), a real model NVIDIA itself documents, and a
partnership NVIDIA itself names in its own materials. The pattern
`mirror_test_v1.md` §5.5 names (companies citing each other's
investment and partnership activity as mutually-reinforcing evidence
of progress) is still structurally present -- Trajectory's post is,
among other things, marketing that benefits from NVIDIA's brand and
NVIDIA's post benefits from naming an early adopter -- but the
specific mechanism §5.5 warns about (evidence substituting circularity
for external validation) is weaker here than in either prior specimen,
precisely because independently-checkable technical claims (the model,
the benchmark, the partnership) sit underneath the circularity instead
of being absent.

## Why This Belongs Next to the Seed IQ Specimen, Not Just the NVIDIA Ones

`2026-08-04_aix_seed_iq_arc_agi_3_claim.md` applies Attractor 2
(Benchmarks) to a self-reported, un-badged benchmark claim that did
not survive scrutiny -- the claimant's own thread conceded the
weakness, and independent comparison against the Verified leaderboard
showed the claim implausible on its face. This specimen runs the same
check -- is a self-reported benchmark number independently corroborated,
or resting entirely on the claimant's own say-so -- against a claim
that, this time, holds up on every checkable point except the exact
headline figure. That is worth stating plainly rather than treated as
a foregone conclusion: this project's framework is a diagnostic
instrument, not a machine for finding fault, and a specimen that mostly
survives contact with primary sources is as informative a result as
one that doesn't.

---

## What This Case Study Does Not Claim

- Does not claim bad faith, deception, or even sloppiness on
  Trajectory's part. Every claim checked either confirmed directly or
  narrowed cleanly to "self-reported, not yet independently
  replicated" -- which is an accurate, ordinary description of a
  single company's own benchmark result, not evidence of wrongdoing.
- Does not claim the 8.3% figure is false. It is unreplicated by any
  third party found this session, which is a different, weaker claim
  than "unconfirmed" or "implausible" -- unlike the Seed IQ specimen,
  nothing here contradicts the number or suggests it doesn't hold.
- Does not claim NVIDIA's naming of Harvey and CodeRabbit as
  post-training partners is itself evidence for Trajectory's specific
  8.3% figure -- NVIDIA's materials corroborate that a partnership and
  benchmark relationship exist, not that any particular result from
  that relationship is accurate.
- Does not claim this specimen's "substantially survives verification"
  outcome generalizes to other Trajectory claims, other NVIDIA-adjacent
  companies, or self-reported AI benchmarks generally -- one specimen
  holding up is one specimen, not a trend, the same discipline this
  directory applies when a specimen fails.
- Does not extend to whether NVIDIA's broader ~$53B/~170-deal
  investment pattern (TechCrunch) is itself sustainable or represents
  improper circular financing -- that question is explicitly out of
  scope here and in the companion specimens, which make the same
  qualification.
- Does not independently verify Trajectory's claimed valuation,
  funding amounts, or founder backgrounds beyond what public reporting
  (pulse2.com, aiweekly.co) states -- those figures are reported as
  found, not re-derived from primary filings.

---

*Specimen dated 2026-08-13. Sources: X post from @trajectorylabs (verified account), inspected directly via screenshot; NVIDIA developer/corporate blog coverage of Nemotron 3.5 Lightning; Hugging Face model card; Harvey LAB benchmark repository and blog; Trajectory's own blog post matching the screenshot's figures; TechCrunch reporting on NVIDIA's broader investment pattern; pulse2.com and aiweekly.co on Trajectory's funding. Applies the framework from [`../papers/published/mirror_test_v1.md`](../papers/published/mirror_test_v1.md) §5.5 (self-reference and circularity) and [`../papers/published/basin_attractors_v1.md`](../papers/published/basin_attractors_v1.md) §2.2 (Attractor 2, Benchmarks). Companion specimens, same underlying ring: [`2026-07-27_ssi_nvidia_partnership.md`](2026-07-27_ssi_nvidia_partnership.md) and [`2026-07-28_nvidia_circular_deals_bloomberg.md`](2026-07-28_nvidia_circular_deals_bloomberg.md).*
