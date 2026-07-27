# OPERATIONAL PROTOCOL: Noether-Temporal Coherence Test for Basin Attractor Depth
## Version 1.0 | July 2026

---

## 1. PURPOSE

Test the coupled prediction from the Noether-Temporal Coherence framework:

> **Prediction:** For a captured epistemic field, the autocorrelation coherence time of immune-structure vocabulary (τ_c_immune) significantly exceeds the coherence time of surface-claim vocabulary (τ_c_claim). For a self-correcting field, τ_c_immune ≈ τ_c_claim.

This protocol operationalizes the prediction into a reproducible NLP pipeline executable against any time-stamped text corpus.

---

## 2. CORPUS SPECIFICATION

### 2.1 Primary Corpus (Captured Field Candidate)
**Domain:** Artificial Intelligence discourse, 2018–2026
**Time resolution:** Quarterly bins (Q1 2018 – Q4 2026 = 36 bins)
**Sources:**
| Source | URL/Access | Format | Weight |
|---|---|---|---|
| arXiv CS.CL abstracts + titles | arxiv.org | XML/API | 0.30 |
| OpenAI blog + research announcements | openai.com/blog | HTML scrape | 0.15 |
| Anthropic blog + research announcements | anthropic.com | HTML scrape | 0.10 |
| Google DeepMind blog + research | deepmind.google | HTML scrape | 0.10 |
| NeurIPS/ICML/ICLR keynote transcripts | conference proceedings | PDF/text | 0.15 |
| Earnings call transcripts (MSFT, GOOGL, META) | Seeking Alpha, FactSet | Text | 0.10 |
| AI-focused Substack newsletters (top 20 by subscriber count) | Substack API | HTML | 0.10 |

**Inclusion criteria:**
- Document must be timestamped to quarter-level precision
- Document must contain at least one term from either the Claim Vocabulary Pool or the Immune Vocabulary Pool (Sec. 3)
- Documents shorter than 100 tokens are excluded

**Exclusion criteria:**
- Pure code repositories without natural language
- Non-English text
- Duplicate documents (deduplicate via MinHash LSH, threshold 0.85)

### 2.2 Control Corpus (Self-Correcting Field)
**Domain:** Organic chemistry or observational astronomy, 2018–2026
**Rationale:** Mature fields with established external anchors (experimental reproducibility, telescope observation) and documented instances of self-correction (e.g., retraction culture in organic chemistry).
**Sources:**
- arXiv chem.OC or astro-ph.HE abstracts
- Journal of Organic Chemistry abstracts
- Astrophysical Journal Letters abstracts
- Conference proceedings (ACS National Meetings, AAS meetings)

**Same time resolution, same inclusion/exclusion criteria.**

### 2.3 Negative Control Corpus (Non-Scientific Discourse)
**Domain:** General technology journalism (TechCrunch, The Verge, Wired), 2018–2026
**Rationale:** High claim turnover, no formal immune structure, no institutional defense rings. Expect τ_c_immune ≈ τ_c_claim ≈ very short.

---

## 3. VOCABULARY OPERATIONALIZATION

### 3.1 Claim Vocabulary Pool (γ_claim)
**Definition:** Terms and phrases that denote specific, time-bound capability claims, product announcements, or paradigm labels. These are expected to rise and fall with the hype cycle.

**Methodology (empirical derivation, not imposed):**
1. Extract all bigrams and trigrams from the primary corpus
2. Compute term frequency by quarter
3. Identify terms with high coefficient of variation (CV > 1.5) across quarters
4. Human-code the top 500 into: claim-related, immune-related, or neutral
5. Retain only claim-related terms

**Seed list (for validation against empirical derivation):**
| Era | Terms |
|---|---|
| 2018–2020 | "artificial general intelligence", "transformative AI", "GPT-3", "few-shot learning", "BERT", "scaling laws" |
| 2021–2022 | "ChatGPT", "sparks of AGI", "emergent abilities", "alignment problem", "large language model", "prompt engineering" |
| 2023 | "GPT-4", "multimodal", "frontier model", "reasoning", "constitutional AI", "RLHF" |
| 2024 | "o1", "reasoning model", "agentic AI", "superintelligence", "AI scientist", "test-time compute" |
| 2025–2026 | "singularity", "event horizon", "gentle singularity", "ASI", "recursive self-improvement", "Mars colonies AI" |

**Validation requirement:** The empirically derived claim vocabulary must have >70% overlap with the seed list by Jaccard similarity. If overlap <70%, the corpus or seed list requires re-examination.

### 3.2 Immune Vocabulary Pool (γ_immune)
**Definition:** Terms and phrases that denote defensive rhetorical maneuvers — the four attractor defenses identified in the basin framework. These are hypothesized to be time-invariant across the observation window.

**Categories and seed terms:**

| Defense Maneuver | Seed Terms | Rationale |
|---|---|---|
| **Goal-post movement** | "next generation will", "next scale", "temporary limitation", "early stages", "just getting started", "on the roadmap", "future work", "not yet", "soon" | Reframes failure as incomplete progress |
| **Provisionalization** | "we're working on it", "in progress", "being addressed", "handled by ongoing research", "already being solved" | Labels counter-evidence as temporary |
| **Status dismissal** | "hot take", "doesn't get it", "behind the curve", "not serious", "decelerationist", "doomer", "anti-progress", "cringe", "out of touch" | Dismisses source rather than engaging content |
| **Burden-shifting** | "prove it's impossible", "show me the alternative", "what's your solution", "where's your model", "build it yourself" | Shifts burden to critic |
| **Equivocation** | "intelligence" (unqualified), "understanding" (unqualified), "coherence" (unqualified), "alignment" (unqualified), "safety" (unqualified), "reasoning" (unqualified) | Uses high-valence terms without operationalization |
| **Volume/velocity** | "look at the science", "thousands of papers", "rapid progress", "moving fast", "breakthrough pace", "exponential", "accelerating" | Substitutes production rate for verification |
| **Appeal to future** | "will be solved", "next version", "coming soon", "inevitable", "just a matter of time", "trajectory is clear" | Deflects current failure to future success |

**Empirical derivation:** Same methodology as claim vocabulary, but select terms with **low** coefficient of variation (CV < 0.5) across quarters. The intersection of low-CV terms with the seed list constitutes γ_immune.

**Validation requirement:** >60% of seed list must appear in the empirically derived low-CV set. Terms that fail to appear are dropped from the pool.

### 3.3 Neutral Vocabulary Pool (γ_neutral)
**Definition:** General scientific terms expected to have stable frequency but no immune function.
**Seed list:** "experiment", "method", "result", "analysis", "data", "figure", "table", "hypothesis", "conclusion"
**Purpose:** Baseline for autocorrelation decay in normal scientific discourse.

---

## 4. AUTOCORRELATION METHODOLOGY

### 4.1 Document Embedding
For each document d in bin t, compute a sentence-transformer embedding:
- **Model:** `all-MiniLM-L6-v2` (standard, reproducible) or `intfloat/e5-large-v2` (higher quality)
- **Input:** Full document text (title + abstract + first 512 tokens of body)
- **Output:** 384-dimensional vector e(d)

### 4.2 Bin-Level Signature Vectors
For each vocabulary pool V ∈ {γ_claim, γ_immune, γ_neutral} and each time bin t:

1. **Filter:** Select documents in bin t that contain at least one term from V
2. **Weight:** For each selected document d, compute a vocabulary attention weight:
   w_V(d) = (count of V-terms in d) / (total tokens in d)
3. **Aggregate:** Compute the bin signature vector:
   s_V(t) = Σ_{d ∈ bin_t} w_V(d) · e(d) / Σ_{d ∈ bin_t} w_V(d)

This produces three time series of signature vectors: s_claim(t), s_immune(t), s_neutral(t) for t = 1...36.

### 4.3 Autocorrelation Function
For each vocabulary pool V and delay τ (in quarters, τ = 1...18):

γ_V(τ) = cos_sim(s_V(t), s_V(t+τ)) averaged over all valid t

where cos_sim(u,v) = (u·v) / (||u|| ||v||)

This yields three autocorrelation functions: γ_claim(τ), γ_immune(τ), γ_neutral(τ).

### 4.4 Alternative: Term-Frequency Autocorrelation (Robustness Check)
As a non-embedding alternative:
1. Compute term-frequency vector f_V(t) for each bin (dimension = |V|)
2. Normalize to probability distribution: p_V(t) = f_V(t) / Σ f_V(t)
3. Compute autocorrelation: γ_V(τ) = Σ_i p_V(t)_i · p_V(t+τ)_i (dot product similarity)

This is less semantically rich but more interpretable. Both methods should be reported.

---

## 5. COHERENCE TIME EXTRACTION

### 5.1 Model Fitting
Fit an exponential decay model to each autocorrelation function:

γ_V(τ) = A · exp(-τ / τ_c_V) + C

where:
- A = initial amplitude (γ(0) - C)
- τ_c_V = coherence time for vocabulary pool V
- C = noise floor (asymptotic baseline)

**Fitting method:** Nonlinear least squares (scipy.optimize.curve_fit)
**Constraints:** A > 0, τ_c_V > 0, 0 ≤ C < 0.3

### 5.2 Alternative: Threshold Method
Define τ_c_V as the smallest τ such that γ_V(τ) < 1/e ≈ 0.368.
If γ_V(τ) never drops below 1/e, set τ_c_V = max(τ) + 1 (censored).

Report both methods. The exponential fit is primary; threshold method is robustness check.

---

## 6. STATISTICAL TEST

### 6.1 Primary Hypothesis
**H_0:** τ_c_immune ≤ τ_c_claim (null: immune structure decoheres at same rate or faster than claims)
**H_1:** τ_c_immune > τ_c_claim (alternative: immune structure persists longer than claims)

### 6.2 Test Statistic
Δτ_c = τ_c_immune - τ_c_claim

### 6.3 Significance Testing
Because we have only one realization of the AI discourse time series, standard parametric tests are underpowered. Use:

**Method A: Bootstrap resampling of bins**
1. Resample time bins with replacement (maintaining temporal order via block bootstrap, block size = 4 quarters)
2. Recompute γ_V(τ) and τ_c_V for each bootstrap sample
3. Compute Δτ_c for each sample
4. p-value = proportion of bootstrap samples where Δτ_c ≤ 0

**Method B: Permutation test**
1. Pool all documents from all bins
2. Randomly reassign documents to bins (preserving bin sizes)
3. Recompute τ_c_immune and τ_c_claim
4. p-value = proportion of permutations where Δτ_c ≥ observed Δτ_c

**Method C: Cross-corpus comparison**
Compare Δτ_c across primary, control, and negative control corpora using ANOVA or Kruskal-Wallis.
Expected ordering: Δτ_c_primary > Δτ_c_control > Δτ_c_negative

Report all three methods. Conclusion requires consistency across methods.

### 6.4 Effect Size
Cohen's d for paired comparison:
d = (τ_c_immune - τ_c_claim) / σ_pooled
where σ_pooled is the pooled standard deviation from bootstrap samples.

| d | Interpretation |
|---|---|
| < 0.2 | Negligible |
| 0.2–0.5 | Small |
| 0.5–0.8 | Medium |
| > 0.8 | Large |

---

## 7. CONTROL TESTS

### 7.1 Control Corpus Test
Execute the identical protocol on the organic chemistry / astronomy corpus.
**Expected:** Δτ_c ≈ 0 (immune and claim vocabulary decoherence at similar rates)
**If observed:** Δτ_c > 0.5, this suggests the effect is not specific to captured fields but may be a general property of scientific discourse under media attention.

### 7.2 Negative Control Test
Execute on general tech journalism corpus.
**Expected:** Both τ_c_immune and τ_c_claim are short (< 2 quarters), Δτ_c ≈ 0.
**If observed:** τ_c_immune >> τ_c_claim, this suggests the immune vocabulary is not specific to institutional defense but may be a general feature of technology journalism.

### 7.3 Placebo Vocabulary Test
Create a synthetic "immune" vocabulary by randomly selecting terms from the neutral pool with the same frequency distribution as the immune seed list.
**Expected:** τ_c_placebo ≈ τ_c_neutral << τ_c_immune.
**If observed:** τ_c_placebo ≈ τ_c_immune, the effect is driven by low-frequency stability rather than immune function.

### 7.4 Temporal Reversal Test
Reverse the time order of the corpus bins and recompute.
**Expected:** No significant Δτ_c in reversed time (autocorrelation is symmetric, but the specific claim/immune vocabulary mapping should not survive reversal if the temporal structure is real).
**If observed:** Same Δτ_c in reversed time, the effect is an artifact of vocabulary frequency distribution, not temporal dynamics.

---

## 8. INTERPRETATION FRAMEWORK

### 8.1 If H_1 is confirmed (τ_c_immune >> τ_c_claim)
This supports the Noether-Temporal Coherence coupling:
- The immune structure is a conserved current under time-translation of the narrative
- The surface claims are gauge freedoms that decoherence rapidly
- The basin depth metric (τ_c_immune / τ_c_claim) is > 1 for the AI field

### 8.2 If H_0 is not rejected (τ_c_immune ≤ τ_c_claim)
This refutes the coupling for this corpus:
- The immune structure is not conserved; it decoheres as fast as the claims
- The attractor may be shallow or the vocabulary operationalization failed
- The Noether analogy does not apply to this field at this granularity

### 8.3 If control corpora show same pattern
- The effect is a general property of scientific communication, not specific to captured fields
- The basin-depth metric requires recalibration or the vocabulary pools need refinement

---

## 9. REPRODUCIBILITY REQUIREMENTS

### 9.1 Data Availability
- All source documents must be archived with timestamps
- arXiv data: use official bulk download + metadata
- Blog data: use Wayback Machine snapshots with timestamp verification
- Earnings calls: use publicly available transcript services
- Full document list and hashes must be published

### 9.2 Code Availability
- All preprocessing, embedding, autocorrelation, and statistical testing code must be published
- Random seeds must be fixed
- Software versions must be documented

### 9.3 Vocabulary Audit
- The final vocabulary pools must be published with derivation methodology
- Human coding must be performed by at least two independent coders with inter-rater reliability > 0.80 (Cohen's kappa)
- Disagreements must be resolved by a third coder

---

## 10. LIMITATIONS AND SCOPE CAVEATS

1. **Single field, single time window:** The primary corpus covers only AI discourse 2018–2026. Generalization to other fields or time periods requires additional data.
2. **English-only:** Non-English AI discourse is excluded, which may miss immune structures in other linguistic registers.
3. **Vocabulary dependence:** The test is sensitive to vocabulary pool construction. The empirical derivation step is designed to mitigate this, but human coding introduces subjectivity.
4. **Embedding model bias:** `all-MiniLM-L6-v2` was trained on web text including AI discourse up to 2021. It may encode some of the very attractor structure it is being used to measure. The term-frequency robustness check partially addresses this.
5. **Causality:** Autocorrelation measures temporal association, not causal mechanism. The Noether analogy provides a formal intuition, not a causal proof.
6. **Scale:** The test measures discourse-level patterns, not individual cognitive states or institutional decisions.

---

## 11. EXPECTED OUTPUT

### 11.1 Primary Deliverables
1. Three autocorrelation plots (γ_claim, γ_immune, γ_neutral vs. τ)
2. Fitted coherence times with confidence intervals
3. Statistical test results (bootstrap, permutation, cross-corpus)
4. Effect size estimates
5. Full vocabulary pools with derivation audit trail

### 11.2 Interpretation Deliverable
A single basin-depth metric for the AI field 2018–2026:

**B = τ_c_immune / τ_c_claim**

| B | Interpretation |
|---|---|
| B ≤ 1 | No evidence of deep basin; immune structure not conserved |
| 1 < B ≤ 2 | Weak basin; some immune persistence |
| 2 < B ≤ 5 | Moderate basin; immune structure clearly outlives claims |
| B > 5 | Deep basin; strong evidence of conserved immune repertoire |

This metric is comparable across fields and time windows.

---

## APPENDIX A: Vocabulary Pool Derivation Algorithm (Pseudocode)

```python
# Step 1: Corpus ingestion
for source in sources:
    documents = download(source, 2018, 2026)
    documents = deduplicate(documents, threshold=0.85)
    documents = filter_by_length(documents, min_tokens=100)

# Step 2: Tokenization and n-gram extraction
for doc in documents:
    tokens = tokenize(doc.text.lower())
    bigrams = extract_ngrams(tokens, n=2)
    trigrams = extract_ngrams(tokens, n=3)
    store(bigrams + trigrams, doc.quarter)

# Step 3: Frequency time series
for term in all_terms:
    for quarter in quarters:
        freq[term][quarter] = count(term, quarter) / total_tokens(quarter)

# Step 4: Coefficient of variation
for term in all_terms:
    cv[term] = std(freq[term]) / mean(freq[term])

# Step 5: Pool assignment
claim_candidates = {term for term, cv_val in cv.items() if cv_val > 1.5}
immune_candidates = {term for term, cv_val in cv.items() if cv_val < 0.5}

# Step 6: Human coding (2 coders + arbiter)
claim_pool = human_code(claim_candidates, category="claim", kappa>0.80)
immune_pool = human_code(immune_candidates, category="immune", kappa>0.80)
neutral_pool = human_code(random_sample(all_terms, n=500), category="neutral", kappa>0.80)

# Step 7: Validation
assert jaccard(claim_pool, seed_claim) > 0.70
assert jaccard(immune_pool, seed_immune) > 0.60
```

## APPENDIX B: Autocorrelation Computation (Pseudocode)

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

# Compute bin signatures
for vocab in ['claim', 'immune', 'neutral']:
    for t, quarter in enumerate(quarters):
        docs = [d for d in corpus if d.quarter == quarter and contains(d, vocab_pools[vocab])]
        embeddings = [model.encode(d.text) for d in docs]
        weights = [count_vocab(d, vocab_pools[vocab]) / len(d.tokens) for d in docs]
        signature[vocab][t] = np.average(embeddings, axis=0, weights=weights)

# Compute autocorrelation
for vocab in ['claim', 'immune', 'neutral']:
    for tau in range(1, 19):
        corrs = []
        for t in range(len(quarters) - tau):
            corrs.append(cosine_similarity(signature[vocab][t], signature[vocab][t+tau]))
        gamma[vocab][tau] = np.mean(corrs)

# Exponential fit
from scipy.optimize import curve_fit

def decay(tau, A, tau_c, C):
    return A * np.exp(-tau / tau_c) + C

for vocab in ['claim', 'immune', 'neutral']:
    popt, pcov = curve_fit(decay, taus, gamma[vocab], p0=[0.5, 5.0, 0.1])
    tau_c[vocab] = popt[1]
    tau_c_ci[vocab] = np.sqrt(np.diag(pcov))[1]  # 1-sigma CI

# Test statistic
delta = tau_c['immune'] - tau_c['claim']
```

---

*Protocol designed for the Noether-Temporal Coherence coupling test. All steps are reproducible given standard NLP tooling and publicly available corpora.*
