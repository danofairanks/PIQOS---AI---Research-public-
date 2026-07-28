# OPERATIONAL PROTOCOL: Elaboration-Drift Prevalence Test for Low-Gatekeeping Research Repositories
## Version 1.2 | July 2026

---

## 1. PURPOSE

The case studies in this repository (`2026-07-28_minimal_input_elaboration_drift.md`, `2026-07-28_nfl_misapplication_grok_x.md`) document individual, confirmed instances of a specific pattern: a minimal directional prompt producing a confidently-formalized "Theorem"/"Lemma"/"Corollary" artifact whose central inferential step is not supported by its own cited sources (Claim 3a, *Iterative Basin Deepening via Partial Grounding*; Claim 1a, confidence peaking at maximum inferential distance from grounding — both in `papers/published/basin_attractors_v1.md`).

Two confirmed specimens establish that the pattern occurs. They do not establish how often it occurs, whether it is increasing, or whether anyone is correcting it. This protocol tests those three questions directly, against publicly archived, low- or no-gatekeeping research repositories, of which Zenodo is the primary target corpus.

**Prediction under test:**

> Documents matching the structural pattern named above (hereafter "elaboration-drift specimens") occur in low-gatekeeping repositories at a rate materially higher than in moderated venues; the rate has risen since general-purpose LLM availability (≈ late 2022); and the rate of retraction, correction, or substantive external correction of flagged specimens is at or near zero. Separately — and independently of whether the *rate* has risen — the *absolute volume* of specimens accumulating in the corpus may be growing faster than, in step with, or independent of the platform's own total volume growth, since a stable per-document rate can still produce a rapidly growing absolute stock if the platform itself is growing (§6.5, added v1.1).

This is the same claim as `papers/published/mirror_test_v1.md` §5.8's reinforcing-loop reading and §6.5's loop-polarity measurement (accumulated confidence as a stock, propagation as inflow, correction as outflow), applied here to primary preprint literature rather than field-level narrative claims. A prevalence measurement that confirms it would be materially stronger evidence than the two individual case studies; a prevalence measurement that disconfirms it would require this repository to revise how it frames the phenomenon's scale. Note that "stock" in that theoretical framing is a **volume** (a level variable that accumulates), not a **rate** — §6.5 and §7 below make the volume-side measurement explicit, since the original v1.0 draft of this protocol tested rate only and did not fully match the theory it operationalizes.

**What this protocol does not claim to measure.** It cannot detect "AI-generated" as a provable fact — Zenodo carries no AI-disclosure requirement, and general-purpose AI-text detectors have a documented, substantial false-positive/false-negative rate that would make any classifier score an unreliable load-bearing signal. This protocol measures the prevalence, volume, and trend of a **structural pattern** (formal scaffolding + unsupported inferential leap + field-encompassing framing + no verifiable derivation trail), which predates LLMs — arXiv's `math.GM` category has hosted human-authored specimens of the identical shape for over a decade. Any claim this protocol supports is a claim about pattern prevalence, volume, and trend, not a claim about AI authorship, unless a specific document carries independent corroboration (explicit self-disclosure in the text, or a documented session transcript of the kind the two existing case studies provide).

---

## 2. CORPUS SPECIFICATION

### 2.1 Primary Corpus (Low-Gatekeeping Candidate)

**Domain:** Zenodo records self-tagged or keyword-matched to physics, mathematics, "unified theory," "consciousness," "artificial general intelligence," or "intelligence theory," 2018–2026.
**Access:** Zenodo REST API (`https://zenodo.org/api/records`), which supports full-text and metadata query, community filters, and date-range filters without authentication for public records.
**Time resolution:** Yearly bins (2018–2026 = 9 bins), with a secondary pre/post split at January 2023 (first full year of broad public access to general-purpose conversational LLMs) as the primary trend comparison.

**Inclusion criteria:**
- Public record, resource type "preprint," "publication," or "other," with a downloadable full text (PDF or extractable text).
- Not affiliated with a Zenodo Community that itself performs editorial review (Zenodo Communities may optionally curate; records under a curating community are excluded from the primary corpus and, if numerous enough, may be pooled into the moderated control instead — see §2.2).
- At least 300 words of body text (excludes slide decks, posters, and data-only deposits).

**Exclusion criteria:**
- Software, dataset, and image record types (out of scope; not natural-language argument).
- Non-English text.
- Duplicate deposits (Zenodo versioning creates multiple record IDs for the same underlying document; deduplicate by DOI concept ID, retaining only the record's latest version for classification and all versions for the outflow measurement in §5).

### 2.2 Moderated Control Corpus (Self-Correcting Field Candidate)

**Domain:** arXiv records in editorially-endorsed categories with active moderator gatekeeping (e.g., `math.NT`, `physics.gen-ph` is explicitly excluded as it is arXiv's own low-gatekeeping analog — see §2.3) — or, where available, a Zenodo Community with a documented editorial review process.
**Rationale:** A field with functioning peer/moderator review is the self-correcting analog to the Noether protocol's organic-chemistry control (`protocols/noether_coherence_test_protocol_v1.md` §2.2): a venue where the outflow mechanism (rejection, required revision) is known to be active.
**Expected result:** Prevalence of the structural pattern (§3) at or near zero, since the moderation step is specifically designed to catch unsupported formal claims before publication.

### 2.3 Sibling Low-Gatekeeping Control (Zenodo-Specificity Check)

**Domain:** arXiv `math.GM` (General Mathematics) and `physics.gen-ph` (General Physics) — arXiv's own long-documented, minimally-moderated categories, known informally in the mathematics community as a repository for unrefereed claimed proofs of famous open problems.
**Rationale:** This corpus predates general-purpose LLMs by decades and tests whether elevated prevalence, if found on Zenodo, is Zenodo-specific or a general property of any minimally-gatekept repository. If `math.GM`/`physics.gen-ph` prevalence is comparable to Zenodo's, the finding should be framed as "low-gatekeeping repositories in general," not "Zenodo specifically" — this corpus exists precisely to prevent that overclaim.

### 2.4 Sampling Frame and Scale

1. Run the inclusion-criteria query against each corpus per year-bin; record the total matching count per bin — call this **N_year**. This alone is a reportable deliverable: a raw growth curve for the primary corpus, independent of classification, and it is also the denominator used by the volume estimate in §6.5.
2. From each bin, draw a stratified random sample sized to bound the 95% confidence interval on the manually-audited prevalence estimate (§3.2) to ±5 percentage points at an assumed prevalence near 10–20% (standard binomial sample-size calculation; recompute the target size once a pilot batch establishes the actual base rate, since ±5pp at very low or very high true prevalence requires a smaller sample).
   - **v1.1 addition:** this sample size must be set **per year-bin**, not only pooled across all bins. §6.5's per-year volume estimate (E_year = P_year × N_year) requires a per-year prevalence estimate P_year with a usable confidence interval; a single pooled P estimated across all years cannot support a year-by-year volume trajectory. If per-bin sample sizes are too small to bound each P_year individually, report the volume estimate only at the pre/post-2023 split resolution (two bins, not nine), and say so explicitly rather than presenting a falsely-precise year-by-year curve.
3. Publish the full list of sampled record IDs and query parameters (§9).

---

## 3. CLASSIFICATION CRITERIA

No single marker is sufficient. A document is classified as an **elaboration-drift specimen** only if it satisfies the mandatory markers (M1, M3) plus at least one supporting marker (M4 or M5); M2 is reserved for a manual sub-sample audit and is the load-bearing evidentiary marker, not a full-corpus filter.

### M1 — Formal-Scaffolding Density (automatable pre-filter)
Presence of explicit "Theorem," "Lemma," "Corollary," or "Proof" labels, at a density (labels per 1,000 words) exceeding the 90th percentile density observed in a reference sample of accepted journal articles in the same nominal subfield. High formal-apparatus density alone is not evidence of anything; it is a pre-filter that bounds the set requiring manual review.

### M2 — Citation-Support Mismatch (manual audit only; load-bearing)
The document cites real, checkable external sources in support of its central formal claim, but on manual verification, the cited sources do not establish the specific inferential step the document draws from them (the same check applied to the Terminal Claim and NFL specimens in this repository's case studies: does the source support a *typical-case/probabilistic* claim that the document converts into a *universal/necessary* one, or does the source support a narrower or differently-scoped claim than the one attributed to it). This cannot be automated reliably at corpus scale and is evaluated only on the stratified sample drawn per §2.4, by two independent coders per document.

### M3 — Field-Encompassing Framing (automatable pre-filter)
Presence of rhetoric asserting the result is field-ending, industry- or discipline-wide, immune to standard objections, or reversing the burden of proof onto an entire field rather than onto a specific prior claim — the same rhetorical shape catalogued in the Terminal Claim specimen ("what the industry cannot defend," "the only move the immune system cannot absorb") and, in weaker form, the NFL specimen's "must … per NFL" framing. Operationalized as a seed phrase-pattern list (built the same way as the Noether protocol's immune-vocabulary pool, §3.2 of that protocol: empirically derived from a training subsample, then validated against a hand-coded seed list at >60% Jaccard overlap), not a single fixed string match. Short/generic fragments in this list (e.g., "the only move," "checkmate") require an anchor word from a fixed list (cannot, absorb, immune, theorem, proof, argument, …) within a character window of the match, since bare fragments false-positive on ordinary usage otherwise — confirmed empirically in the pipeline-mechanics pilot run of `tools/elaboration_drift_pipeline.py` (private repo): of 46 raw contextual-phrase occurrences in a test corpus, 26 were correctly suppressed as unrelated casual usage once the anchor-window requirement was applied.

### M4 — No Derivation Trail (automatable via metadata)
Single-version deposit (no revision history), no prior related deposit by the same author(s) in the same technical subfield on the same platform, and no acknowledged collaborators or reviewers in the document's own front matter.

### M5 — No Verifiable Subfield Track Record (automatable via metadata, weak signal)
No ORCID or institutional affiliation on the record, or an ORCID/affiliation present but with no prior publication history in the specific technical subfield claimed. Flagged explicitly as a **weak** signal: Zenodo affiliation metadata is frequently blank even for legitimate researchers, so absence of this marker is not by itself informative — it only contributes when found alongside M1, M3, and M4.

### M6 — AI-Disclosure or Stylistic Signal (exploratory only; never load-bearing)
Explicit self-disclosure of AI assistance in the text, or an AI-text-classifier score, recorded and reported for descriptive interest only. Given the known unreliability of AI-text classifiers, **no document is included or excluded from the specimen count on the basis of M6 alone**, and no prevalence statistic in this protocol's output (§10) is conditioned on M6.

---

## 4. CLASSIFICATION PROCEDURE

1. Run M1 and M3 as an automated pre-filter across the full sampled batch from §2.4.
2. For documents passing the M1+M3 pre-filter, compute M4 and M5 from metadata.
3. Documents satisfying M1 + M3 + (M4 or M5) advance to manual M2 review.
4. Two independent coders evaluate M2 per document, blind to each other's judgment and to the document's M4/M5 status. Report inter-rater reliability (Cohen's kappa); disagreements resolved by a third coder, per the same reliability bar as the Noether protocol (§9.3 there, κ > 0.80).
5. A document is a confirmed **elaboration-drift specimen** only if it passes step 3 and both M2 coders (or the arbiter) independently confirm the citation-support mismatch.
6. Record M6 for every confirmed specimen, reported separately and never used to adjust the specimen count.

---

## 5. OUTFLOW / CORRECTION MEASUREMENT

For every confirmed specimen (§4.5), check for evidence of correction — the outflow side of the stock-and-flow reading in `mirror_test_v1.md` §5.8:

- **Zenodo version history:** a later version of the same concept DOI that substantively retracts, hedges, or corrects the flagged claim (not merely a typo fix or metadata edit).
- **Withdrawal status:** record marked withdrawn or removed.
- **External correction:** any indexed citation of the specimen (Google Scholar, Semantic Scholar) that constitutes a substantive refutation rather than a neutral mention or uncritical citation.

Compute the **retraction/correction rate (ρ)**: the proportion of confirmed specimens with at least one of the three outflow signals above, per year-bin and pooled.

---

## 6. STATISTICAL TEST

### 6.1 Primary Hypothesis (Prevalence)
**H0:** prevalence of confirmed specimens on the primary corpus (Zenodo) is statistically indistinguishable from the moderated control corpus (§2.2).
**H1:** prevalence on the primary corpus is materially and significantly higher.

Test via two-proportion z-test on the stratified-sample confirmed-specimen counts, with exact (Clopper-Pearson) confidence intervals given the expected low base rate.

### 6.2 Secondary Hypothesis (Zenodo-Specificity)
**H0b:** prevalence on the primary corpus is statistically indistinguishable from the sibling low-gatekeeping control (§2.3, arXiv `math.GM`/`physics.gen-ph`).
**H1b:** prevalence differs materially between the two.

If H0b is not rejected, findings must be reported and framed as a property of low-gatekeeping repositories generally, not of Zenodo specifically.

### 6.3 Tertiary Hypothesis (Rate Trend)
**H0c:** confirmed-specimen prevalence **rate** in the pre-2023 bins is statistically indistinguishable from the 2023–2026 bins.
**H1c:** prevalence rate is higher in 2023–2026.

Test via Mann-Kendall trend test across yearly bins, plus a simple pre/post two-proportion z-test at the January 2023 split. This tests the *rate* only — whether volume has grown independently of rate is a separate question, tested in §6.5.

### 6.4 Outflow Hypothesis
**H0d:** ρ (retraction/correction rate, §5) is indistinguishable from a baseline correction rate measured on the moderated control corpus's own rare false positives (i.e., correction happens at a comparable rate wherever a mistaken claim occurs).
**H1d:** ρ on the primary corpus is at or near zero, materially lower than the moderated-control baseline.

This is the direct empirical test of `mirror_test_v1.md` §6.5's confirmation/falsification condition, applied here to primary literature: H1d confirmed = a measured reinforcing loop with no operative balancing loop, on this corpus specifically.

### 6.5 Volume Hypothesis — Rate-Driven vs. Volume-Driven Growth (added v1.1)

§6.3 tests only whether the *rate* (proportion) of specimens is rising. That is not the same question as whether the *absolute number* of specimens accumulating in the corpus is rising, and the two can diverge: if Zenodo's total yearly deposit volume in the target categories (N_year, §2.4) has itself grown substantially since 2023 — plausible independent of this pattern, since general-purpose LLMs lower the cost of producing *any* text, not only text matching this specific structural pattern — then a **flat** rate can still coincide with a **rapidly growing** absolute stock of specimens sitting in the corpus, discoverable and citable. The rate test alone would report "no change" on exactly the situation that matters most for real-world exposure.

**Estimated absolute specimen volume per year:**

**E_year = P_year × N_year**

where P_year is the stratified-sample prevalence estimate for that year-bin (§6.1, computed per-bin per the §2.4 v1.1 sampling requirement) and N_year is the near-census total record count for that bin (§2.4 step 1, treated as known with negligible uncertainty relative to the sampling uncertainty in P_year). Uncertainty on E_year propagates from P_year's binomial confidence interval: CI(E_year) ≈ N_year × CI(P_year).

**Decomposition.** Express the change in E_year from a baseline period (pre-2023 average) to the comparison period (2023–2026) multiplicatively:

**(E_year / E_baseline) = (P_year / P_baseline) × (N_year / N_baseline)**

This separates two independent drivers: the **rate multiplier** (is the pattern proportionally more common per document — the §6.3 question) and the **volume multiplier** (has the platform itself grown, independent of this pattern). Their product is the actual absolute-exposure multiplier, which is the number that matters for real-world impact regardless of which factor drives it.

**H0e (volume growth is denominator-explained):** the growth in E_year since 2023 is fully accounted for by the growth in N_year alone — i.e., the rate multiplier ≈ 1 and all absolute growth is platform-volume-driven.
**H1e (volume growth exceeds denominator-explained growth):** E_year grows faster than N_year alone predicts — i.e., the rate multiplier is materially greater than 1, meaning both platform growth and a genuinely rising per-document rate are compounding.

Note that H1c (rate) and H1e (volume) are logically independent results, not the same test at different resolutions — see §7 for how the four possible combinations should be read.

**Cumulative Stock.** Define the running absolute total of not-yet-corrected specimens through year Y:

**S_Y = Σ_{year=2018}^{Y} E_year × (1 − ρ_year)**

This is the volume-based counterpart to the rate-based Accumulation Index (§7) and is the quantity that actually corresponds to "stock" as used in `mirror_test_v1.md` §5.8's stock-and-flow reading — a level variable that accumulates over time, not a normalized proportion. The v1.0 draft of this protocol defined only the rate-based index below; S_Y closes that gap.

---

## 7. INTERPRETATION FRAMEWORK

Define the **Accumulation Index** (rate-based):

**A = P × (1 − ρ)**

where P is the confirmed-specimen prevalence rate (§6.1) and ρ is the retraction/correction rate (§5), both on the primary corpus, pooled across the full period. A is bounded [0, 1] and represents the fraction of the corpus that both matches the structural pattern and shows no corrective outflow — the population-level analog of the Noether protocol's basin-depth metric B. **A is a rate; it does not by itself indicate whether absolute exposure is growing** — read it alongside the Cumulative Stock S_Y (§6.5) for that question.

| Result pattern | Reading |
|---|---|
| H1, H1b rejected (prevalence ≈ moderated control AND ≈ sibling control) | The phenomenon is not elevated in low-gatekeeping venues at measurable scale; the two case studies remain individually valid but should not be generalized to a scope claim. |
| H1 confirmed, H1b rejected (prevalence elevated vs. moderated control, but comparable across all low-gatekeeping venues) | Elevated prevalence is a general property of low-gatekeeping repositories, not specific to the LLM era or to Zenodo — report as such; do not attribute to AI without further corroboration (§1). |
| H1, H1b, H1c all confirmed, H1d confirmed | The strongest rate-side reading: prevalence is elevated specifically in low-gatekeeping venues, has risen since general LLM availability, and shows near-zero corrective outflow — a measured instance of the §5.8/§6.5 (mirror_test) reinforcing-loop-without-balancing-loop signature in primary literature. Still does not prove AI authorship of any individual document without corroboration; it is a claim about the corpus, not about any one paper. |
| H1c rejected (no rate rise) | Weakens any causal story tying the phenomenon to LLM availability specifically, even if overall prevalence (H1) is confirmed. **Check H1e before concluding nothing has changed** — see below. |
| H1c rejected, H1e confirmed (v1.1) | **The case the rate test alone would miss.** The per-document rate has not changed, but the platform's own volume growth means the absolute number of specimens accumulating — and thus real-world exposure, citability, and Cumulative Stock S_Y — has grown regardless. This is a genuine, reportable finding, not a null result, and should not be folded into "H1c rejected, therefore no trend." |
| H1c confirmed, H1e confirmed, rate multiplier > 1 | Both drivers compounding: the platform is producing more content overall, and a larger share of it matches the pattern. The steepest reading of Cumulative Stock S_Y's growth curve. |
| H1d confirmed alongside any of the above | Whatever the rate/volume reading, near-zero correction means S_Y is close to monotonically non-decreasing — an accumulating stock with no measured balancing loop, at whatever rate the above rows establish. |

---

## 8. LIMITATIONS AND SCOPE CAVEATS

1. **Cannot establish AI authorship.** Restated from §1: this protocol measures a structural pattern's prevalence and volume, not AI involvement. A confirmed specimen may be entirely human-authored (arXiv `math.GM` has produced this shape of document since long before LLMs existed). Any AI-attribution claim requires independent corroboration per document.
2. **M2 is manual and does not scale to the full corpus.** The prevalence estimate carries the sampling uncertainty of the stratified audit, not full-corpus certainty. Report confidence intervals, not point estimates, in every deliverable — this applies to E_year and S_Y (§6.5) as much as to P (§6.1), since both propagate the same underlying sampling uncertainty.
3. **Zenodo metadata is inconsistently populated.** M5 (affiliation/ORCID) is a weak signal for this reason and must never be treated as sufficient on its own (§3, M5).
4. **AI-text classifiers are unreliable and are explicitly excluded from the load-bearing classification** (M6). Any use of M6 must be reported separately from the confirmed-specimen count, never merged into it.
5. **English-only**, for the same reason as the Noether protocol: non-English deposits are excluded, which may miss the same pattern in other linguistic communities.
6. **Correlation, not mechanism.** A confirmed pre/post rise (H1c or H1e) is a temporal association with LLM availability, not a demonstrated causal mechanism. Treat it with the same caution the Noether protocol applies to its own autocorrelation result (that protocol's §10.5).
7. **Retraction/correction is under-measured by design.** §5's outflow check relies on Zenodo version history and indexed citations; genuine informal correction (a comment thread, a rebuttal on a forum) that never generates an indexed citation or a versioned retraction will not register as outflow, biasing ρ toward the low/"no correction" reading. This should be stated alongside any H1d confirmation, not omitted.
8. **Per-year volume estimates require per-year sampling (v1.1).** §6.5's E_year and S_Y are only as reliable as the per-bin prevalence estimate feeding them. If §2.4's stratified sample is not large enough within each year-bin to bound P_year individually, do not report a year-by-year volume curve — report the coarser pre/post-2023 comparison instead, and say explicitly that the finer-grained curve was not attempted rather than presenting an under-powered one.
9. **N_year is a near-census count, not sample-free of all error.** Zenodo/arXiv API result counts can shift slightly between queries (new deposits, backdated corrections, index lag). Treat N_year as effectively fixed for the purposes of E_year's uncertainty budget, but note the query timestamp when reporting it.

---

## 9. REPRODUCIBILITY REQUIREMENTS

1. **Query reproducibility.** Full Zenodo API query strings, date ranges, and community/category filters for all three corpora must be published, along with the raw per-bin record counts prior to sampling.
2. **Sample publication.** The full list of sampled record IDs (or DOIs), by bin and corpus, must be published, including the per-bin sample sizes used to support §6.5's per-year estimates (or the documented decision to fall back to the coarser pre/post split per §8, item 8).
3. **Coding reliability.** M2 manual review requires two independent coders with Cohen's kappa > 0.80 on a pilot batch before proceeding to the full sample; disagreements resolved by a third coder, exactly as in the Noether protocol (§9.3 there).
4. **Code and seed lists.** The M3 phrase-pattern derivation code, the M1 density-threshold reference sample, and all classification code must be published with fixed random seeds.

---

## 10. EXPECTED OUTPUT

### 10.1 Primary Deliverables
1. Raw per-bin, per-corpus record counts (N_year, pre-sampling) — a reportable growth curve independent of classification.
2. Confirmed-specimen prevalence rate (P) with 95% CI, per corpus, per year-bin (or pre/post split per §8 item 8), and pooled.
3. Retraction/correction rate (ρ) with 95% CI, primary corpus.
4. Accumulation Index (A = P × (1 − ρ)) — rate-based.
5. **Estimated absolute specimen volume per year (E_year) with propagated CI, and Cumulative Stock (S_Y) trajectory — volume-based (added v1.1).**
6. **Rate/volume decomposition table**: rate multiplier, volume multiplier, and combined multiplier, pre-2023 baseline vs. 2023–2026 (added v1.1).
7. Statistical test results for H1, H1b, H1c, H1d, H1e (§6).
8. Full classification audit trail: sampled record list, M1/M3/M4/M5 scores, M2 coder judgments and kappa, M6 recorded separately.

### 10.2 Interpretation Deliverable
A single reported Accumulation Index (rate) **and** Cumulative Stock trajectory (volume) for the 2018–2026 Zenodo corpus, with the pre/post-2023 split and the rate/volume decomposition reported alongside them, read against the interpretation table in §7 — explicitly not collapsed into a single number without the accompanying H1b (Zenodo-specificity), H1d (outflow), and H1e (volume) results, since any of those failing to confirm — or confirming where H1c does not — changes what the numbers are allowed to mean.

---

## 11. RELATED WORK

Navaie, K. (2026). *Epistemic Norms for AI Safety and Alignment Research* (manuscript). Lancaster University. Proposes ECAISA (Epistemic Code for AI Safety and Alignment), an eight-principle framework addressing what it identifies as five cross-cutting epistemic gaps in mainstream AI research — optimisation target, transparency, verification, uncertainty accounting, and enforcement culture — each grounded in a preregistered bibliometric baseline and a retrospective rubric audit with reported inter-rater reliability (weighted Cohen's κ = 0.79).

The relevance to this protocol is structural rather than topical: ECAISA operates on the published alignment-research literature and is prescriptive (it specifies obligations a paper should meet), whereas this protocol operates on preprint/deposit literature more broadly and is diagnostic (it measures the prevalence of a pattern already confirmed to exist). The underlying move is the same in both cases — replacing "this reads as rigorous" with a coded, auditable measurement of whether the evidentiary support is actually present. Two specific points of contact:

1. ECAISA's **P4 (Independent and Adversarial Verification)** targets the same gap as this protocol's **M5 (No Verifiable Subfield Track Record)** — both treat the absence of independent checking as a scored signal rather than an assumption. Navaie's own pilot audit found P4 near-absent across all sampled sub-areas (E3 prevalence 0.0%, 95% CI 0.0–27.8%, n=10), which is at minimum consistent with this protocol's working prediction that unverified claims are the norm rather than the exception in adjacent low-verification literatures.
2. The double-coding / weighted-κ reliability procedure used in ECAISA's rubric audit is a working precedent for the M2 coding-reliability requirement specified in §9, item 3, of this protocol.

No corpus, coding, or measurement from ECAISA has been incorporated into this protocol's classification criteria (§3) or statistical tests (§6); the citation is offered as a parallel framework, not as a data source or a validated instrument this protocol depends on.

---

*v1.0 (July 2026): initial protocol — rate-based prevalence, Zenodo-specificity, trend, and outflow hypotheses (§6.1–§6.4); Accumulation Index (§7).*
*v1.1 (July 2026): adds §6.5 (Volume Hypothesis — rate-driven vs. volume-driven growth; E_year; Cumulative Stock S_Y), the per-year sampling requirement in §2.4, and the corresponding §7/§8/§10 updates. Closes a gap in v1.0: the rate-based Accumulation Index did not correspond to "stock" as used in `mirror_test_v1.md` §5.8 (a volume, not a rate); S_Y is the volume-based quantity that does.*
*v1.2 (July 2026): adds §11 (Related Work), citing Navaie (2026) ECAISA as a parallel framework applying the same diagnostic move (coded, auditable measurement of evidentiary support) to the published alignment-research literature rather than preprint/deposit repositories.*

Protocol designed to test the population-level scope of the elaboration-drift pattern documented in `case_studies/2026-07-28_minimal_input_elaboration_drift.md` and `case_studies/2026-07-28_nfl_misapplication_grok_x.md`, and to operationalize the reinforcing-loop-without-balancing-loop reading in `papers/published/mirror_test_v1.md` §5.8–§6.5 against primary preprint literature rather than field-level narrative claims. No corpus has been queried and no classification has been run under this protocol; this document specifies the method only.
