# OPERATIONAL PROTOCOL: Elaboration-Drift Prevalence Test for Low-Gatekeeping Research Repositories
## Version 1.0 | July 2026

---

## 1. PURPOSE

The case studies in this repository (`2026-07-28_minimal_input_elaboration_drift.md`, `2026-07-28_nfl_misapplication_grok_x.md`) document individual, confirmed instances of a specific pattern: a minimal directional prompt producing a confidently-formalized "Theorem"/"Lemma"/"Corollary" artifact whose central inferential step is not supported by its own cited sources (Claim 3a, *Iterative Basin Deepening via Partial Grounding*; Claim 1a, confidence peaking at maximum inferential distance from grounding — both in `papers/published/basin_attractors_v1.md`).

Two confirmed specimens establish that the pattern occurs. They do not establish how often it occurs, whether it is increasing, or whether anyone is correcting it. This protocol tests those three questions directly, against publicly archived, low- or no-gatekeeping research repositories, of which Zenodo is the primary target corpus.

**Prediction under test:**

> Documents matching the structural pattern named above (hereafter "elaboration-drift specimens") occur in low-gatekeeping repositories at a rate materially higher than in moderated venues; the rate has risen since general-purpose LLM availability (≈ late 2022); and the rate of retraction, correction, or substantive external correction of flagged specimens is at or near zero.

This is the same claim as `papers/published/mirror_test_v1.md` §5.8's reinforcing-loop reading and §6.5's loop-polarity measurement (accumulated confidence as a stock, propagation as inflow, correction as outflow), applied here to primary preprint literature rather than field-level narrative claims. A prevalence measurement that confirms it would be materially stronger evidence than the two individual case studies; a prevalence measurement that disconfirms it would require this repository to revise how it frames the phenomenon's scale.

**What this protocol does not claim to measure.** It cannot detect "AI-generated" as a provable fact — Zenodo carries no AI-disclosure requirement, and general-purpose AI-text detectors have a documented, substantial false-positive/false-negative rate that would make any classifier score an unreliable load-bearing signal. This protocol measures the prevalence and trend of a **structural pattern** (formal scaffolding + unsupported inferential leap + field-encompassing framing + no verifiable derivation trail), which predates LLMs — arXiv's `math.GM` category has hosted human-authored specimens of the identical shape for over a decade. Any claim this protocol supports is a claim about pattern prevalence and trend, not a claim about AI authorship, unless a specific document carries independent corroboration (explicit self-disclosure in the text, or a documented session transcript of the kind the two existing case studies provide).

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

1. Run the inclusion-criteria query against each corpus per year-bin; record the total matching count per bin (this alone is a reportable deliverable — a raw growth curve for the primary corpus, independent of classification).
2. From each bin, draw a stratified random sample sized to bound the 95% confidence interval on the manually-audited prevalence estimate (§3.2) to ±5 percentage points at an assumed prevalence near 10–20% (standard binomial sample-size calculation; recompute the target size once a pilot batch establishes the actual base rate, since ±5pp at very low or very high true prevalence requires a smaller sample).
3. Publish the full list of sampled record IDs and query parameters (§9).

---

## 3. CLASSIFICATION CRITERIA

No single marker is sufficient. A document is classified as an **elaboration-drift specimen** only if it satisfies the mandatory markers (M1, M3) plus at least one supporting marker (M4 or M5); M2 is reserved for a manual sub-sample audit and is the load-bearing evidentiary marker, not a full-corpus filter.

### M1 — Formal-Scaffolding Density (automatable pre-filter)
Presence of explicit "Theorem," "Lemma," "Corollary," or "Proof" labels, at a density (labels per 1,000 words) exceeding the 90th percentile density observed in a reference sample of accepted journal articles in the same nominal subfield. High formal-apparatus density alone is not evidence of anything; it is a pre-filter that bounds the set requiring manual review.

### M2 — Citation-Support Mismatch (manual audit only; load-bearing)
The document cites real, checkable external sources in support of its central formal claim, but on manual verification, the cited sources do not establish the specific inferential step the document draws from them (the same check applied to the Terminal Claim and NFL specimens in this repository's case studies: does the source support a *typical-case/probabilistic* claim that the document converts into a *universal/necessary* one, or does the source support a narrower or differently-scoped claim than the one attributed to it). This cannot be automated reliably at corpus scale and is evaluated only on the stratified sample drawn per §2.4, by two independent coders per document.

### M3 — Field-Encompassing Framing (automatable pre-filter)
Presence of rhetoric asserting the result is field-ending, industry- or discipline-wide, immune to standard objections, or reversing the burden of proof onto an entire field rather than onto a specific prior claim — the same rhetorical shape catalogued in the Terminal Claim specimen ("what the industry cannot defend," "the only move the immune system cannot absorb") and, in weaker form, the NFL specimen's "must … per NFL" framing. Operationalized as a seed phrase-pattern list (built the same way as the Noether protocol's immune-vocabulary pool, §3.2 of that protocol: empirically derived from a training subsample, then validated against a hand-coded seed list at >60% Jaccard overlap), not a single fixed string match.

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

### 6.3 Tertiary Hypothesis (Trend)
**H0c:** confirmed-specimen prevalence in the pre-2023 bins is statistically indistinguishable from the 2023–2026 bins.
**H1c:** prevalence is higher in 2023–2026.

Test via Mann-Kendall trend test across yearly bins, plus a simple pre/post two-proportion z-test at the January 2023 split.

### 6.4 Outflow Hypothesis
**H0d:** ρ (retraction/correction rate, §5) is indistinguishable from a baseline correction rate measured on the moderated control corpus's own rare false positives (i.e., correction happens at a comparable rate wherever a mistaken claim occurs).
**H1d:** ρ on the primary corpus is at or near zero, materially lower than the moderated-control baseline.

This is the direct empirical test of `mirror_test_v1.md` §6.5's confirmation/falsification condition, applied here to primary literature: H1d confirmed = a measured reinforcing loop with no operative balancing loop, on this corpus specifically.

---

## 7. INTERPRETATION FRAMEWORK

Define the **Accumulation Index**:

**A = P × (1 − ρ)**

where P is the confirmed-specimen prevalence rate (§6.1) and ρ is the retraction/correction rate (§5), both on the primary corpus. A is bounded [0, 1] and represents the fraction of the corpus that both matches the structural pattern and shows no corrective outflow — the population-level analog of the Noether protocol's basin-depth metric B.

| Result pattern | Reading |
|---|---|
| H1, H1b rejected (prevalence ≈ moderated control AND ≈ sibling control) | The phenomenon is not elevated in low-gatekeeping venues at measurable scale; the two case studies remain individually valid but should not be generalized to a scope claim. |
| H1 confirmed, H1b rejected (prevalence elevated vs. moderated control, but comparable across all low-gatekeeping venues) | Elevated prevalence is a general property of low-gatekeeping repositories, not specific to the LLM era or to Zenodo — report as such; do not attribute to AI without further corroboration (§1). |
| H1, H1b, H1c all confirmed, H1d confirmed | The strongest reading: prevalence is elevated specifically in low-gatekeeping venues, has risen since general LLM availability, and shows near-zero corrective outflow — a measured instance of the §5.8/§6.5 reinforcing-loop-without-balancing-loop signature in primary literature. This still does not prove AI authorship of any individual document without corroboration; it is a claim about the corpus, not about any one paper. |
| H1c rejected (no pre/post rise) | Weakens any causal story tying the phenomenon to LLM availability specifically, even if overall prevalence (H1) is confirmed. |

---

## 8. LIMITATIONS AND SCOPE CAVEATS

1. **Cannot establish AI authorship.** Restated from §1: this protocol measures a structural pattern's prevalence, not AI involvement. A confirmed specimen may be entirely human-authored (arXiv `math.GM` has produced this shape of document since long before LLMs existed). Any AI-attribution claim requires independent corroboration per document.
2. **M2 is manual and does not scale to the full corpus.** The prevalence estimate carries the sampling uncertainty of the stratified audit, not full-corpus certainty. Report confidence intervals, not point estimates, in every deliverable.
3. **Zenodo metadata is inconsistently populated.** M5 (affiliation/ORCID) is a weak signal for this reason and must never be treated as sufficient on its own (§3, M5).
4. **AI-text classifiers are unreliable and are explicitly excluded from the load-bearing classification** (M6). Any use of M6 must be reported separately from the confirmed-specimen count, never merged into it.
5. **English-only**, for the same reason as the Noether protocol: non-English deposits are excluded, which may miss the same pattern in other linguistic communities.
6. **Correlation, not mechanism.** A confirmed pre/post rise (H1c) is a temporal association with LLM availability, not a demonstrated causal mechanism. Treat it with the same caution the Noether protocol applies to its own autocorrelation result (that protocol's §10.5).
7. **Retraction/correction is under-measured by design.** §5's outflow check relies on Zenodo version history and indexed citations; genuine informal correction (a comment thread, a rebuttal on a forum) that never generates an indexed citation or a versioned retraction will not register as outflow, biasing ρ toward the low/"no correction" reading. This should be stated alongside any H1d confirmation, not omitted.

---

## 9. REPRODUCIBILITY REQUIREMENTS

1. **Query reproducibility.** Full Zenodo API query strings, date ranges, and community/category filters for all three corpora must be published, along with the raw per-bin record counts prior to sampling.
2. **Sample publication.** The full list of sampled record IDs (or DOIs), by bin and corpus, must be published.
3. **Coding reliability.** M2 manual review requires two independent coders with Cohen's kappa > 0.80 on a pilot batch before proceeding to the full sample; disagreements resolved by a third coder, exactly as in the Noether protocol (§9.3 there).
4. **Code and seed lists.** The M3 phrase-pattern derivation code, the M1 density-threshold reference sample, and all classification code must be published with fixed random seeds.

---

## 10. EXPECTED OUTPUT

### 10.1 Primary Deliverables
1. Raw per-bin, per-corpus record counts (pre-sampling) — a reportable growth curve independent of classification.
2. Confirmed-specimen prevalence rate (P) with 95% CI, per corpus and pooled.
3. Retraction/correction rate (ρ) with 95% CI, primary corpus.
4. Accumulation Index (A = P × (1 − ρ)).
5. Statistical test results for H1, H1b, H1c, H1d (§6).
6. Full classification audit trail: sampled record list, M1/M3/M4/M5 scores, M2 coder judgments and kappa, M6 recorded separately.

### 10.2 Interpretation Deliverable
A single reported Accumulation Index for the 2018–2026 Zenodo corpus, with the pre/post-2023 split reported alongside it, read against the interpretation table in §7 — explicitly not collapsed into a single number without the accompanying H1b (Zenodo-specificity) and H1d (outflow) results, since either of those failing to confirm changes what the number is allowed to mean.

---

*Protocol designed to test the population-level scope of the elaboration-drift pattern documented in `case_studies/2026-07-28_minimal_input_elaboration_drift.md` and `case_studies/2026-07-28_nfl_misapplication_grok_x.md`, and to operationalize the reinforcing-loop-without-balancing-loop reading in `papers/published/mirror_test_v1.md` §5.8–§6.5 against primary preprint literature rather than field-level narrative claims. No corpus has been queried and no classification has been run under this protocol; this document specifies the method only.*
