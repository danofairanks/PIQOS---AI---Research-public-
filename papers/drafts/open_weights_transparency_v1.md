# Open Weights, Open Source, and the Transparency That Isn't There: A Full Evaluation

**Status:** DRAFT. Not yet citable as a stable reference; content here may
change or be withdrawn without notice, per `papers/README.md`'s stated
policy for this directory.

**Opened:** 2026-08-04. **Authors:** operator + Claude (Sonnet 5).

**Companion to:** [`register_invariance_self_falsification_v1.md`](register_invariance_self_falsification_v1.md)'s
technical-axis test, and [`mirror_test_v1.md`](../published/mirror_test_v1.md)
§5.1/§5.4. This draft asks whether "open weights" — the industry's most
visible current transparency gesture — actually satisfies the disclosure
standard this project's own framework requires, and checks a specific
operator hypothesis (that synthetic-data saturation is what makes labs
comfortable releasing weights) against the current evidence.

---

## 1. The Distinction the Debate Runs On

**Open weights and open source are not the same claim, and the gap
between them is the actual content of this debate — checked directly
rather than assumed.** The Open Source Initiative's Open Source AI
Definition (OSAID 1.0), released October 2024 after roughly two years of
multi-stakeholder debate, requires the full package: weights, training
code, and enough data information to understand and meaningfully modify
the system — the "recipe," not just the finished dish. "Open weights"
means something much narrower: the trained parameters are downloadable
and runnable. **Verified finding, stated plainly: almost every model
marketed with "open" branding today — Llama, DeepSeek, Qwen, Gemma —
qualifies only as open-weight, not open-source, under OSAID.** This is
not a fringe critique; it is close to industry consensus among the
people who track the distinction closely, and OSI itself has signaled a
1.1/2.0 revision through Q4 2026 specifically to address what one source
describes as "the data-information compromise" in its own 1.0 standard —
i.e., OSI's own definition is still negotiating how much data disclosure
"open source AI" actually requires, which is itself evidence the
boundary is unsettled, not resolved.

**Why this distinction is the load-bearing one for everything else in
this draft.** "Open weights" grants a real, usable freedom — run the
model locally, fine-tune it, avoid API dependency and per-token cost,
inspect its behavior through probing. It does not grant the freedom
OSAID considers definitional: the ability to audit or rebuild the system
from its actual inputs. Training code, data curation methodology, safety
testing and red-teaming process, and compute/cost figures are, in the
overwhelming majority of "open" releases checked here, not part of what
gets published alongside the weights.

---

## 2. The Current Landscape, Verified

As of mid-2026, the open-weight camp is led by Qwen 3 (Alibaba, Apache
2.0), DeepSeek R1/V3, Llama 4 Scout/Maverick (Meta, restrictive custom
license), Mistral Small/Large (Mistral, largely Apache 2.0/MIT), Kimi K3
(Moonshot, a 2.8-trillion-parameter MoE model released July 2026), and
GLM-4.7 (Z.ai). DeepSeek's own public estimate places its open-weight
models within a few months of the closed frontier on many benchmarks.
Licensing varies meaningfully within the "open" category itself: Mistral,
much of Qwen, DeepSeek, and Microsoft's Phi family use permissive
licenses (Apache 2.0/MIT); Meta's Llama and Google's Gemma carry custom
licenses with restrictions that matter at commercial scale. OpenAI and
Anthropic remain predominantly closed-weight (OpenAI's gpt-oss models
are a partial, recent exception); Google is closed for its frontier
Gemini line, with Gemma as its open-weight counterpart.

---

## 3. What Is Genuinely at Stake for Safety — the Bengio Report, Checked Directly

**This is not a fringe safety concern; it is the conclusion of a
100-plus-expert international report.** The International AI Safety
Report 2026, chaired by Yoshua Bengio with contributions from over 100
AI experts and Expert Advisory Panel nominees from 29 nations plus the
UN, OECD, and EU, addresses open-weight models specifically and finds
open-weight capability now trails closed frontier models by less than a
year. The report's core structural concern is **irreversibility**: once
weights are published, there is no mechanism to roll back existing
downloaded copies or force safety updates onto them — a fundamentally
different risk profile than a closed, API-gated model a lab can patch,
restrict, or withdraw access to. Bengio has stated the concern in its
sharpest form specifically for cyber and biological dual-use capability:
once released, the process cannot be recalled or repaired.

**This is the actual, substantive safety stake — not primarily a data-
transparency question.** It is worth being precise about what the safety
literature's concern is and is not: the irreversibility argument is about
capability proliferation and control, not primarily about whether the
public gets to see how a model was built. This matters for how the
transparency question below should be scoped: open-weighting is
simultaneously a genuine safety risk (per Bengio et al.) *and* a limited
transparency gesture (per §1) — the two are not the same axis, and a
lab's decision to open-weight is not automatically evidence of genuine
methodological openness just because it carries genuine capability risk.

---

## 4. What Open-Weighting Does and Does Not Expose About Internal Lab Process

**What it does not expose, checked against §1's OSAID gap directly.**
Training code, data curation and filtering methodology, RLHF/alignment
process specifics, internal safety-testing and red-teaming results,
compute and cost figures, and internal evaluation results not separately
published are not part of a weights release in the overwhelming majority
of cases checked here. A lab can open-weight its model and still run
exactly the "closely guarded research" posture this project's own SSI
specimen already names and finds evidentially empty — the two are not in
tension. Weight release, by itself, does not clear this project's own
technical-transparency bar (the first axis of the challenge posed in
`register_invariance_self_falsification_v1.md`); it is a real but
partial and narrower form of disclosure than that bar requires.

**What it does expose, checked and more significant than a first pass
suggests.** Released weights are not fully decoupled from training data
after all. Training-data-extraction research, originating with Carlini
et al.'s foundational work on GPT-2 (2020–2021) and extended since,
demonstrates that large language models memorize and can be made to emit
verbatim or near-verbatim training data — including personally
identifiable information and, per more recent probabilistic-extraction
studies, excerpts from copyrighted books — when queried adversarially.
This is a real, documented, non-hypothetical channel by which a
released model's weights can leak fragments of what it was trained on,
independent of whether the lab ever publishes the dataset itself. Open-
weighting is therefore better described as *partial, probabilistic,
adversarially-accessible data exposure* rather than *zero data
exposure* — a materially different and more precise claim than "weights
reveal nothing about the data."

---

## 5. The Operator's Hypothesis, Checked Against the Actual Evidence

**The hypothesis, stated precisely:** that training data has become
saturated with synthetic data to the point that pro-open-weight labs may
feel there is nothing distinctively proprietary left in their data
pipeline to protect, making weight release less costly than it would
have been when training data was more distinctively sourced.

**Checked against current industrial practice — the literal "saturation"
claim does not hold as stated.** Verified: standard 2026 practice keeps
a human-data anchor at roughly 60–70% of the pretraining mix, with
synthetic data used as targeted amplification on verifiable domains
(math, code, structured reasoning) rather than as a wholesale
replacement — a real, capped ceiling around 30–40% synthetic, driven by
well-documented model-collapse risk when synthetic fraction runs too
high. Microsoft's Phi-4, trained on roughly 400 billion synthetic
tokens, is the most aggressive disclosed public instance found in this
pass, and it is a smaller, specialized model family, not evidence of a
frontier-wide shift to synthetic-majority training. **The literal
version of the hypothesis is not supported by current disclosed
practice.**

**A more precise, defensible version of the same intuition does hold up,
and is worth stating as the corrected form of the hypothesis rather than
discarding the intuition entirely.** The "data wall" is real and
independently documented: Epoch AI's widely-cited estimate places the
total effective stock of high-quality public human text at roughly 300
trillion tokens, with exhaustion projected between 2026 and 2032 at
current scaling rates, and frontier labs on pace to exhaust available
public web text by 2028. This is the same underlying pressure already
verified elsewhere in this project — Sutskever's "the data is finite...
there is only one internet" reframing, cited in this project's SSI
specimen. What this pressure actually produces is not synthetic
saturation but **convergence**: every lab drawing from an increasingly
overlapping, increasingly exhausted finite public pool, which erodes the
distinctiveness of any one lab's data pipeline as a competitive moat —
for a different structural reason than the hypothesis names (a shrinking
shared commons, not a synthetic replacement), but pointing toward the
same practical conclusion the hypothesis anticipates: the data
underneath a 2026 frontier model is less likely to be the thing worth
protecting than it would have been in 2020–2022, when far more headroom
existed in unscraped, distinctive public data.

**The documented, actual reasoning labs give for open-weighting is
different from both the hypothesis and this corrected version, and
should be stated plainly rather than folded into either.** Meta's own
publicly reported rationale for open-weighting Llama is platform and
ecosystem strategy — checked directly: releasing weights broadly is
reported as a deliberate move so that "developers wouldn't want to pay
for models from Meta's rivals," a distribution and lock-in strategy
structurally similar to how a company might open-source a framework to
commoditize the layer below its actual business. Zuckerberg's public
framing — that concentrating advanced AI in a few institutions is more
dangerous than distributing it broadly — is worth naming in the same
register this project already applies to Nadella's distillation
critique (`basin_attractors_v1.md` §2.16): a stated position that
happens to align precisely with the position-holder's own competitive
interest is not automatically wrong, but it is not independent of that
interest either, and should be weighed as such rather than taken as a
neutral safety argument. **Net: the primary documented driver of
open-weighting, at least for the largest current player, is competitive
platform strategy — not a stated judgment that the underlying data has
become non-proprietary.** The operator's hypothesis may still describe a
real, unstated background condition making that competitive strategy
cheaper to execute than it would have been five years ago — but it is
not the reason labs give, and this draft does not have evidence it is
the operative reason rather than a plausible contributing factor.

---

## 6. Synthesis: Where This Leaves the Transparency Question

Open-weighting is real, checkable, and — per the Bengio report — carries
genuine, irreversible safety stakes distinct from anything a marketing
claim alone could carry. It is not, however, the methodological
transparency this project's own framework asks for. It clears none of
OSAID's data/code requirements in the overwhelming majority of current
releases, and a lab can hold this exact posture — genuinely open weights,
genuinely closed methodology — without contradiction. The extraction-
attack literature complicates a clean "weights reveal nothing about
data" reading, but adversarial, probabilistic leakage of fragments is
not equivalent to the kind of disclosure BIFP or OSAID actually specify.
The operator's synthetic-saturation hypothesis, checked directly, is not
supported in its literal form by current disclosed training practice,
but the underlying intuition — that the data underneath frontier models
is becoming less distinctive and therefore less costly to expose,
regardless of exposure route — is independently supported by the
data-wall evidence, just via a different mechanism (a shrinking shared
commons) than the one named (synthetic replacement). The best-evidenced
account of *why* labs actually open-weight remains platform-strategic,
not data-related, for the clearest documented case (Meta) — which means
this draft's answer to "what's at stake" and "why now" turns out to be
two separate questions with two separate, only partially overlapping
answers.

---

## 7. What This Draft Does Not Claim

Does not claim open-weight labs are acting in bad faith, or that
open-weighting is not a genuine, valuable form of openness on its own
terms — it grants real freedoms (local deployment, fine-tuning,
independence from API access) that closed models do not, and this draft
does not discount that. Does not claim the operator's synthetic-data
hypothesis is wrong in its underlying intuition — only that its literal
mechanism (saturation) is not supported by current disclosed practice,
while a related mechanism (data-wall-driven convergence) independently
points toward a similar practical conclusion. Does not claim Meta's
stated ecosystem-lock-in rationale is the complete or only reason any
lab open-weights — DeepSeek's, Mistral's, and Alibaba's stated
motivations were not independently checked with the same depth in this
pass and may differ meaningfully from Meta's. Does not resolve the live
dispute over whether Chinese open-weight labs are distilling from closed
US frontier models rather than independently innovating — noted as an
open, contested question in this pass, not adjudicated.

---

*Drafted 2026-08-04. Sources: stackviv.ai, futureagi.com, moesif.com,
geotoolbox.ai (OSAID / open-weights-vs-open-source distinction, verified
across multiple independent summaries); opensource.org (OSAID 1.0,
October 2024, and the planned 1.1/2.0 revision); computingforgeeks.com,
hidekazu-konishi.com, d-central.tech (2026 open-weight model landscape);
arXiv:2602.21012 (International AI Safety Report 2026, Bengio, chair);
NPR (May 31, 2026, open-weight safety risk coverage); Bengio's 2026 World
AI Conference remarks on cyber/bio irreversibility; invisibletech.ai,
pub.towardsai.net, digitalapplied.com (2026 synthetic-data practice,
human-data-anchor ratios); Epoch AI (public high-quality text stock
estimate and exhaustion timeline, cited via secondary sources this
pass); Carlini et al. 2020–2021 (training-data extraction from GPT-2,
foundational) and subsequent probabilistic-extraction studies on
open-weight models (copyrighted-text and PII recovery); completeaitraining.com,
techcentral.co.za, techtimes.com (Meta/Zuckerberg open-weight competitive
strategy and DeepSeek-distillation dispute, verified). Cross-references
[`basin_attractors_v1.md`](../published/basin_attractors_v1.md) §2.16
(the self-interest-stated-directly diagnostic, applied here to
Zuckerberg's framing) and
[`register_invariance_self_falsification_v1.md`](register_invariance_self_falsification_v1.md)
(the technical-axis transparency standard open-weighting is checked
against).*
