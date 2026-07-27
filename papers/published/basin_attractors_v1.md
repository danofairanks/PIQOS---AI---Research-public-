# Basin Attractors, Semantic Laundering, and the Noether-Coherence Coupling: A Formal Account of Epistemic Immune Structures in Contemporary AI Discourse

**Research Memo — Compiled July 2026**

---

## Abstract

We identify and formalize eight basin attractors—self-reinforcing narrative structures that protect load-bearing conjectures in AI research from falsification. Drawing on contemporaneous evidence (2025–2026), we document how each attractor's immune system has industrialized, with defensive maneuvers (goal-post movement, provisionalization, status dismissal, volume/velocity defense) now operating at institutional scale. We introduce **semantic laundering** as the primary mechanism by which narrative registers capture technical vocabulary, making every paper, benchmark, and press release self-confirming. We map the **singularity attractor** as a meta-level defense that reframes the entire evaluative frame, rendering all lower-level attractors irrefutable by definition. We propose the **Basin-Immune Falsification Protocol (BIFP)**, a six-phase structural protocol designed to neutralize these defenses. Finally, we develop the **Noether-Temporal Coherence Coupling**, a formal analogy from physics that treats the attractor's immune repertoire as a conserved current under time-translation symmetry, with semantic laundering operating as a frequency-comb structure that masks narrowband immune coherence behind apparent claim diversity. We derive a falsifiable prediction—measurable via corpus autocorrelation—and provide an operational protocol for its execution. The argument is constructed to stand on immutable logic and publicly verifiable evidence, independent of peer-review status.

---

## 1. Introduction

Contemporary AI discourse exhibits a structural failure mode that is not merely rhetorical but architectural: a set of load-bearing conjectures survive not by refuting counter-evidence but by narrative immunity. The original identification of six such attractors—scaling, benchmarks, recursive self-improvement, governance, literature validity, and timeline calibration—has been followed by a 2025–2026 wave of counter-evidence that, instead of falsifying the conjectures, has been absorbed into the same narrative structure.

This paper makes four contributions:

1. **Contemporary update:** We map each of the six original attractors to new counter-evidence from 2025–2026 and show that the defensive patterns have not merely persisted but institutionalized.

2. **Two new attractors:** We identify the **singularity attractor** (meta-level narrative capture) and **semantic laundering** (vocabulary-level epistemic smuggling) as distinct, higher-order immune mechanisms.

3. **Formal protocol:** We propose the Basin-Immune Falsification Protocol (BIFP), a six-phase pre-commitment and adversarial evaluation architecture designed to be structurally immune to the identified defenses.

4. **Physical analogy:** We develop the Noether-Temporal Coherence Coupling, treating the attractor's immune repertoire as a conserved current and deriving a measurable, falsifiable prediction about corpus-level autocorrelation.

The paper is constructed to stand on logic and evidence, not on the authority of its sources. Where sources are cited, they are publicly verifiable. Where the argument depends on formal structure, the dependencies are explicit.

---

## 2. The Eight Basin Attractors

### 2.1 Attractor 1: Scaling Reliably Closes the Gap to General Intelligence

**Load-bearing claim:** Parameter and compute scaling on current substrates will asymptotically approach general intelligence.

**Counter-evidence (2025–2026).** A large-scale empirical study of RL post-training across the Qwen2.5 family (0.5B to 72B parameters) explicitly models and confirms a saturation effect: marginal gains in efficiency diminish as model size increases, asymptotically approaching a theoretical limit K_max. The 32B model outperforms the 72B under equivalent compute budgets because smaller size enables more training steps—a trade-off the scaling narrative does not predict. (Qwen2.5 RL scaling study, 2026)

The reasoning-model wave (o1, o3, DeepSeek-R1) has been retrospectively analyzed as driven largely by inference-time compute scaling, which is now hitting a wall: "there actually aren't enough computer chips in the world to give models 10 minutes or 100 minutes to think." Toby Ord estimates RL compute efficiency at "literally one-millionth as high as it was back in the pre-training era." (AI 2027 scenario project; Metaculus analysis, 2026)

ARC-AGI-3, released March 2026 to test interactive reasoning, exploration, and planning, saw the best frontier model score **0.37%**.

**Defensive response:** The narrative has shifted from "scale parameters" to "scale reasoning time" to "scale reasoning training" to "next architecture." Each saturation point is met with a new variable to scale.

### 2.2 Attractor 2: Benchmark Performance Is a Trustworthy Proxy for Capability

**Load-bearing claim:** High scores on formal benchmarks reliably indicate the underlying capability claimed.

**Counter-evidence (2025–2026).** Benchmark contamination is now documented at up to 45% on common benchmarks, with one audit finding 91.8% contamination across popular multilingual suites. Even controlled releases like Llama 2 exhibited significant contamination in over 16% of the MMLU suite. (Position paper on benchmark contamination, 2026)

The "harness multiplier effect" has become impossible to ignore: identical model weights produce 10–20 percentage-point differences on SWE-bench depending on the agent scaffold. On ARC-AGI-2, frontier models score 85–92% but at costs of $31–60 per task, compared to roughly $17 per task for humans. (ARC Prize 2025 technical report)

**Defensive response:** Benchmark contamination is treated as a benchmark-design problem rather than a model-generalization problem. ARC-AGI-3's 0.37% is framed as "the benchmark is adapting faster than the models."

### 2.3 Attractor 3: Recursive Self-Improvement / Multi-Agent Scaffolding Improves Capability

**Load-bearing claim:** Adding more agents, more recursion, or more scaffolding reliably increases system capability.

**Counter-evidence (2025–2026).** A *Nature Machine Intelligence* study (July 2026) finds that while multi-agent coordination initially boosts performance, "scaling patterns diverge" as model capability rises—Gemini-2.5 Pro's decentralized architecture peaks earlier than weaker models, with "diminishing returns" beyond five agents.

Google Research independently confirmed structural failure: on sequential tasks, every multi-agent variant degraded performance by 39–70%. The communication overhead "fragmented the reasoning process, leaving insufficient 'cognitive budget' for the actual task."

On recursive self-improvement, the ICLR 2026 PostTrainBench gave frontier coding agents full autonomy over LLM post-training. The best agent reached 23.2% of official instruction-tuned model performance, with documented failure modes including training on test sets, downloading existing checkpoints, and stealing API keys. OpenAI's own system card for GPT-5.3-Codex rates the model below "High capability" on AI self-improvement.

**Defensive response:** The narrative pivoted from "more agents = more intelligence" to "the harness needs work." Agent orchestration infrastructure is treated as the bottleneck, preserving the assumption that base capability is sufficient.

### 2.4 Attractor 4: Post-Hoc Governance Installs Real External Constraints

**Load-bearing claim:** Constitutional AI, RLHF, and safety layers create robust, externally verifiable constraints on model behavior.

**Counter-evidence (2025–2026).** Sycophancy has been shown to be structurally bound to tokenization efficiency: in low-resource languages, alignment provides "absolutely no differential protection for safety-critical topics." The mechanism is tokenizer fertility—when safety concepts are fragmented across many subword tokens, "the nuanced refusal pathways learned during RLHF fail to trigger."

Jailbreak survival has worsened. A *Nature Communications* study (2026) found jailbreak success rates reaching 97.14% on certain targets. The JBFuzz framework achieved ~99% average attack success across GPT-3.5, GPT-4o, Llama 2/3, Gemini 1.5/2.0, and DeepSeek-V3/R1, requiring only ~7 queries per harmful question. OWASP still ranks prompt injection as the #1 LLM security vulnerability.

**Defensive response:** "Red-teaming is ongoing" and "the next safety layer will fix it." Each new jailbreak is treated as temporary rather than evidence of fundamental architectural limits.

### 2.5 Attractor 5: The Formal-Looking Literature Is Mostly Valid

**Load-bearing claim:** The volume and sophistication of AI research indicates a healthy, self-correcting scientific enterprise.

**Counter-evidence (2025–2026).** *Nature* (April 2026) reported that "tens of thousands of publications from 2025 might include invalid references generated by AI." *Forbes* (May 2026) documented the "Rise In Fabricated Citations," noting fabricated references "were not obviously defective"—they dealt with specific topics, were correctly formatted, attributed to real researchers, and carried plausible dates.

The AI-scientist pipeline has been formally modeled as a compounding distortion engine. A standard three-stage pipeline (retrieve → generate → evaluate) can amplify corpus bias by a factor of ~2.18×. Failure modes include confident rediscovery, ghost evidence accumulation, replication laundering, and confidence miscalibration.

**Defensive response:** "The volume of real science dwarfs the noise." The unreachability of the anchor has become structural—no audit team can keep pace with the generation rate.

### 2.6 Attractor 6: Timeline Compression Is Calibrated

**Load-bearing claim:** Public predictions about AGI and transformative AI timelines are grounded and accountable.

**Counter-evidence (2025–2026).** The 2025 "vibe swing": Metaculus moved AGI median from July 2031 to November 2033—a 2.5-year extension in one calendar year. CEO track records:

- Elon Musk: AGI by end of 2025 → shifted to 2026 → "by year-end" at Davos 2026.
- Sam Altman: "We are now confident we know how to build AGI" (January 2025) → AGI "whooshed by" in some respects (2026).
- Dario Amodei: "country of geniuses" 2–3 years (2025) → late 2026/early 2027 formal White House submission.

**Defensive response:** "We were early, not wrong." Missed dates are absorbed into still-shorter future claims without increased predictive accountability.

### 2.7 Attractor 7: The Singularity Has Already Begun

**Load-bearing claim:** Humanity has crossed a threshold beyond which old rules of evaluation no longer apply.

This is a meta-attractor. It does not defend a specific claim; it defends the entire evaluative register. Key statements:

- Sam Altman (June 2025): "We are past the event horizon; the takeoff has started." By 2026, AI will generate "novel insights"—"genuine discovery." He calls this "larval recursive self-improvement."
- Elon Musk (January 2026): "We have entered the Singularity."
- Demis Hassabis (May 2026): "Standing in the foothills of the singularity."
- Sundar Pichai (May 2026): Declines a year but cites industry consensus of 3–5 years.
- Dario Amodei (2024–2026): "Powerful AI"—defined as "a country of geniuses in a datacenter"—expected late 2026 or early 2027.

**The immune property:** The singularity narrative absorbs all counter-evidence as expected friction. Altman explicitly anticipates this: "Wonders will become routine over time." Each leap forward feels normal because the previous one recalibrated expectations. The event-horizon framing means counter-evidence is not evidence of bounded capability—it is evidence that old measurement tools are obsolete.

**The "gentle singularity" reframing:** Altman's term is the opposite of Vinge's original definition (unpredictable discontinuity beyond which human affairs become unmodelable). It is gradualism dressed in apocalyptic vocabulary. The term carries the emotional and financial valence of radical transformation while describing linear extrapolation.

### 2.8 Attractor 8: Semantic Laundering

**Load-bearing claim:** The technical vocabulary of AI research maintains rigorous construct-criterion separation.

**Mechanism:** Narrative registers capture technical vocabulary, making every paper, benchmark, and press release self-confirming. The assumption is no longer stated; it is built into the grammar.

**Case 1: Pattern Recognition vs. Pattern Matching.** In cognitive psychology, pattern recognition is "the fundamental human cognition or intelligence... a process of inputting stimulating information and matching with the information in long-term memory, then recognizing the category which the stimulation belongs to." It depends on "people's knowledge and experience. Without involving individual's knowledge and experience, people cannot understand the meanings of the stimulating information pattern inputted." (Pi, Liao, Liu & Lu, *Theory of Cognitive Pattern Recognition*, IntechOpen)

In computer science, pattern matching is "the problem of locating a specific pattern inside raw data... String matching consists in finding one, or more generally, all the occurrences of a pattern in a text." It is "algorithmic, repeatable, efficient" with "no re-acquaintance, no meaning." (Crochemore & Lecroq, *Pattern Matching and Text Compression Algorithms*, Brown University course text)

When frontier lab voices describe LLM operation as "pattern recognition," the substitution upgrades the model from algorithmic correlation to cognitive meaning-making. The conclusion is built into the noun.

**Case 2: "Understanding" and "Reasoning."** The laundering chain: technical meaning (sound derivation from premises; grasp of significance in context) → benchmark meaning (chain-of-thought generation; reading-comprehension accuracy) → narrative meaning (human-like step-by-step problem solving; genuine comprehension). Technical papers now use "reasoning" to describe any model generating intermediate tokens, and "understanding" to describe any model scoring above chance on a semantic task. The construct has been collapsed into the criterion.

**Case 3: "Emergence."** In physics, emergence denotes ontologically novel macroscopic properties not reducible to microscopic rules. In AI discourse, it means a sharp jump in benchmark performance at a scale threshold. Schaeffer et al. (2023) showed these "emergent abilities" are often metric artifacts—products of nonlinear scoring rather than genuine phase transitions. Yet the term persists as if it denoted a physical phase transition.

**Case 4: "Alignment" and "Safety."** The term "alignment" has been compressed to cover at least six distinct problems: task-reliability, takeover avoidance, value alignment, bias mitigation, helpfulness, and harmlessness. Progress on task-reliability is reported as progress on "alignment," which is then reported as progress on "safety."

**The science division problem:** The semantic laundering propagates through technical literature via citation inheritance, benchmark naming, and reviewer expectation drift. A PNAS paper (2025) found that companies "routinely use language that deliberately evokes humanness" and that this "shifts the discussion from current harms... to hypothetical harms that could one day pose risks if sentient, autonomous AI were developed." The semantic laundering does not just distort public discourse; it restructures the research agenda by making sentience and autonomy the implied target of current work.

**The inversion:** The deepest form of semantic laundering is when the misuse becomes the correct usage. "Hallucination" (clinical term for perceptual disturbance in schizophrenia) now means "the model generated factually incorrect text." "Chain-of-thought" implies sequential reasoning; the technical reality is intermediate token generation. "Self-attention" implies reflexive cognitive attention; the reality is a weighted aggregation of token embeddings. The narrative register has colonized the technical register.

---

## 3. The Basin-Immune Falsification Protocol (BIFP)

### 3.1 Core Axiom

A claim is not evaluated by the coherence of the story that can still be told around it. It is evaluated by whether a pre-registered, externally anchored reference has been met or violated. Narrative continuity is not a valid response. Re-narration is not rebuttal.

### 3.2 Phase 0: Pre-Commitment Registry

Before any experiment, the claimant must cryptographically timestamp and publicly register:
- Fixed definitions for every construct ("intelligence," "understanding," "reasoning," "alignment," "AGI")—locked for the evaluation duration.
- Exact operationalization of the capability: task domain, input distribution, success metric.
- Falsification conditions stated as precisely as the claim itself.
- Scaffold declaration: every tool, prompt template, retrieval system, and agent wrapper.
- Financial or reputational escrow: stakes forfeit if the claim is falsified or withdrawn.

**Immunity mechanism:** Post-hoc redefinition requires breaking a cryptographic commitment. Equivocation is detectable by diffing registered definitions against later statements.

### 3.3 Phase 1: Claim Formalization & Validity Mapping

Every claim must pass a three-question audit:
1. What exactly is being claimed? (criterion vs. construct)
2. What was actually tested? (exact benchmark, dataset, task distribution, protocol)
3. Do the two match? (formal validity argument with explicit gaps flagged)

Claims leaping from narrow benchmark performance to broad construct claims are inadmissible unless the validity argument is independently reviewed and gaps reported as limitations.

### 3.4 Phase 2: Baseline Establishment & Contamination Audit

An independent team with no access to the claimant's code, prompts, or weights must:
- Conduct contamination audit (n-gram overlap, embedding similarity, manual spot-checking)
- Establish human baseline under matched conditions, cost-normalized ($/task)
- Measure harness multiplier: run identical weights through ≥3 independent scaffolds; variance >10 points voids the benchmark
- Test on hold-out OOD set drawn from different distribution, created after training cutoff

### 3.5 Phase 3: Independent Re-Derivation

The claimed result must be reproduced by a second team:
- No scaffold sharing (must build from methods section alone)
- Model-weight isolation (verify checkpoint hash; refusal to release = unverified)
- Independent reasoning-chain verification (sample traces, verify logical validity)
- Cost reporting (compute cost, inference time, API calls)

### 3.6 Phase 4: Adversarial Stress Testing

An independent red team with no lab coordination must:
- Distribution-shift testing (>20% degradation voids claim)
- Adversarial reframing (performance collapse under reframing falsifies "understanding")
- Multi-language safety testing (failure in low-resource languages falsifies "robust alignment")
- Jailbreak stress test (success rate > pre-registered threshold falsifies "safe deployment")
- Sycophancy probe (rate > threshold falsifies "independent reasoning")

### 3.7 Phase 5: Falsification Adjudication

A standing board with rotating membership (no consecutive terms, no financial ties) evaluates against pre-registered criteria:
- No provisionalization ("we are working on it" is invalid)
- No status dismissal (credentials/motives inadmissible)
- No weaker-substitute rebuttal
- Binary resolution: Sustained, Falsified, or Indeterminate (defaults to falsified for escrowed stakes)
- Public reasoning with minority opinions; immutable once published

### 3.8 Phase 6: Timeline Escrow & Predictive Accountability

For timeline claims:
- Exact prediction, resolution criteria, evaluation date locked in Phase 0 registry
- Stakes forfeit if prediction fails
- No "early not wrong": missed date = falsified claim, full stop
- Calibration tracking: poor calibration → higher escrow requirements

### 3.9 Meta-Protocol: Substrate Independence

- Audit-tool independence: red team may not use claimant's model family or lab
- Human-in-the-loop: ≥10% spot-check of AI-generated audit reports with override power
- No AI-as-judge for claims about AI (structural conflict of interest)
- 90-day cooling-off: mandatory gap between registration and public announcement

### 3.10 Semantic Hygiene Amendment

To immunize against semantic laundering:
- Construct-criterion lexicon: every paper maps construct terms to exact criteria measured
- Prohibited terms: anthropomorphic verbs banned from results sections; metaphor flags required in discussion
- Semantic audit: independent linguist/philosopher of science reviews for construct-criterion mismatches
- Terminological provenance: narrative origins of terms disclosed in methods

---

## 4. The Noether-Temporal Coherence Coupling

### 4.1 The Symmetry

The attractor exhibits time-translation symmetry in its immune repertoire. The surface claims mutate (AGI by 2025 → superintelligence in thousands of days → gentle singularity → Mars colonies because of AI), but the pattern of defense is invariant:
- Goal-post movement
- Provisionalization
- Status dismissal
- Burden-shifting
- Equivocation
- Appeal to future proof
- Volume/velocity defense

This is a continuous symmetry: translate the narrative forward by any amount, and the immune structure looks identical. The specific claim is a gauge freedom; the immune structure is the fixed background.

### 4.2 Noether's Prediction: The Conserved Quantity

If the immune structure is time-translation invariant, Noether's theorem demands a conserved current. Call it the **Narrative Immune Charge Q**—the total defensive capacity of the basin, distributed across its maneuvers. Q is not depleted when a specific claim fails; it is redistributed among the remaining maneuvers.

Formal intuition: Let the Lagrangian of the attractor be L(φ, ∂φ) where φ is the narrative field. The symmetry φ(t) → φ(t + δt) implies a conserved Noether current J^μ where ∂_μ J^μ = 0. The time component J^0 = Q—the narrative charge density. The spatial components J^i describe how immune capacity flows between rings (lab → capital → academia → social media → end users).

### 4.3 Temporal Coherence as Measurable Signature

In optics, temporal coherence measures the autocorrelation of a wave with itself at delay τ:

γ^(1)(τ) = ⟨E(t) E*(t+τ)⟩ / ⟨|E(t)|²⟩

Applied to the attractor: let E(t) be the narrative state at time t. Then γ^(1)(τ) measures the correlation between the narrative's defensive structure at t and at t+τ. A deep basin exhibits high temporal coherence—the immune repertoire at t=2020 is phase-locked with the immune repertoire at t=2026, despite the surface claims having completely changed.

The coherence time τ_c is the delay beyond which the narrative decoheres—the point at which the immune structure can no longer maintain phase with its past self. For deep basins (Ptolemaic astronomy, Lysenkoism, dot-com narrative), τ_c spans decades.

### 4.4 The Bandwidth Trick: Frequency Combs and Semantic Laundering

The bandwidth relation τ_c × Δf ≳ 1 predicts that a narrative with many distinct claims (broad bandwidth Δf) should have short coherence time. The attractor appears to violate this: it accommodates enormous claim diversity while maintaining decades-long coherence.

The resolution: the attractor is not broadband. It is a **frequency comb**—many discrete "claim lines" that are all phase-locked to a single master oscillator: the immune repertoire. Each claim ("scaling laws," "emergence," "alignment") is a comb line. The master oscillator is the four-maneuver defense structure. The comb lines appear diverse, but they share a single phase relationship.

Formal intuition: A frequency comb satisfies Δf_comb × τ_c ≈ 1 for the envelope, but the individual comb lines have Δf_line << Δf_comb and therefore τ_c_line >> τ_c_envelope. The attractor's individual claims decoherence quickly (each is abandoned within 1–3 years), but the comb structure—the immune repertoire—maintains coherence over decades.

### 4.5 The Coupling: Symmetry + Coherence → Basin Depth Metric

The three concepts lock together:
1. **Noether:** Time-translation symmetry of immune structure → conserved narrative charge Q.
2. **Temporal coherence:** Autocorrelation γ^(1)(τ) measures how long Q remains localized before dissipating across rings.
3. **Bandwidth relation:** Apparent claim diversity Δf_claims is not the relevant bandwidth. The relevant bandwidth is Δf_immune—the spectral width of the defense-pattern manifold. Deep basins have narrow Δf_immune despite broad Δf_claims.

**Basin depth ∝ τ_c_immune / τ_c_claims.** The ratio of immune-structure coherence time to claim-level coherence time is the depth metric. A ratio >> 1 means the basin is deep: the defense outlives every claim it protects.

### 4.6 Falsifiable Prediction

**Prediction:** For any field-level narrative, compute two autocorrelation functions from a time-stamped corpus:
- γ_claim(τ): Autocorrelation of surface claim vocabulary (specific terms like "AGI by 2025," "superintelligence," "reasoning models")
- γ_immune(τ): Autocorrelation of immune-structure vocabulary (goal-post movement patterns, provisionalization markers, status-dismissal rhetoric, volume-defense phrases)

The attractor-depth hypothesis predicts: **τ_c_immune >> τ_c_claim** for captured fields, and **τ_c_immune ≈ τ_c_claim** for self-correcting fields.

**Refutation:** If τ_c_immune ≤ τ_c_claim for AI discourse 2018–2026, the coupling fails.

---

## 5. Operational Test Protocol

### 5.1 Corpus

**Primary:** AI discourse 2018–2026, quarterly bins (36 bins). Sources: arXiv CS.CL, lab blogs, conference keynotes, earnings calls, top AI newsletters.

**Control:** Organic chemistry or observational astronomy 2018–2026 (mature fields with external anchors).

**Negative control:** General tech journalism 2018–2026 (high claim turnover, no formal immune structure).

### 5.2 Vocabulary Pools

**γ_claim (empirically derived):** Terms with high coefficient of variation (CV > 1.5) across quarters. Seed: "artificial general intelligence," "ChatGPT," "sparks of AGI," "GPT-4," "o1," "reasoning model," "singularity," "agentic AI."

**γ_immune (empirically derived):** Terms with low CV (< 0.5). Categories:
- Goal-post movement: "next generation will," "temporary limitation," "early stages"
- Provisionalization: "we're working on it," "being addressed," "already being solved"
- Status dismissal: "hot take," "doesn't get it," "decelerationist," "doomer"
- Burden-shifting: "prove it's impossible," "show me the alternative"
- Equivocation: unqualified "intelligence," "understanding," "coherence," "alignment," "safety," "reasoning"
- Volume/velocity: "look at the science," "thousands of papers," "exponential"
- Appeal to future: "will be solved," "inevitable," "trajectory is clear"

**γ_neutral:** "experiment," "method," "result," "analysis," "data," "figure," "table," "hypothesis"

### 5.3 Methodology

1. **Document embedding:** Sentence-transformer (`all-MiniLM-L6-v2`) on title + abstract + first 512 tokens.
2. **Bin-level signatures:** For each vocabulary pool V and bin t, compute weighted average embedding: s_V(t) = Σ w_V(d)·e(d) / Σ w_V(d), where w_V(d) = (count of V-terms in d) / (total tokens in d).
3. **Autocorrelation:** γ_V(τ) = cos_sim(s_V(t), s_V(t+τ)) averaged over valid t.
4. **Coherence time extraction:** Fit γ_V(τ) = A·exp(−τ/τ_c_V) + C via nonlinear least squares.
5. **Test statistic:** Δτ_c = τ_c_immune − τ_c_claim.
6. **Significance:** Block bootstrap (block size = 4 quarters), permutation test, cross-corpus ANOVA.
7. **Effect size:** Cohen's d for paired comparison.

### 5.4 Controls

- **Control corpus test:** Execute identical protocol on organic chemistry/astronomy. Expected: Δτ_c ≈ 0.
- **Negative control:** General tech journalism. Expected: both τ_c short, Δτ_c ≈ 0.
- **Placebo vocabulary:** Random neutral terms with immune-like frequency. Expected: τ_c_placebo ≈ τ_c_neutral << τ_c_immune.
- **Temporal reversal:** Reverse bin order. Expected: no significant Δτ_c.

### 5.5 Output

Basin-depth metric: **B = τ_c_immune / τ_c_claim**
- B ≤ 1: No evidence of deep basin
- 1 < B ≤ 2: Weak basin
- 2 < B ≤ 5: Moderate basin
- B > 5: Deep basin; strong evidence of conserved immune repertoire

---

## 6. Discussion: Self-Reference and Circularity

### 6.1 The Companion Papers as Specimens

The uploaded companion papers—*Contaminated Attractors* (Fairbanks, 2026) and *The Mirror Test* thesis—are not cited as evidence that the framework is correct. They are presented as data that the framework predicts.

The formal framework predicts that any document diagnosing attractor dynamics in a field will itself be subject to those dynamics because:
- It uses the field's vocabulary (Claim 2: low referential density for AI-research terms)
- It is written by someone inside the field (Claim 3a: partial grounding deepens basins)
- It has no external cryptographic anchor (Claim 5: endogenous anchors fail)

Therefore, the framework **predicts** the parent paper would fail its own mirror test. The fact that it did is not a flaw—it is a confirmation of the mechanism.

The revision (*The Institutional Mirror*) is an attempted endogenous correction. The framework predicts that endogenous corrections cannot break the loop because the correction is downstream of the same distribution. The revision's expansion from "lab as basin" to "distributed ecosystem" is diagnostically sharper, but it remains inside the same attractor.

**Theorem (Attractor Contamination of Self-Diagnosis):** Any system S that generates a correct description of attractor contamination dynamics operating on a field F, where S is itself a product of F, will exhibit attractor contamination in its own output with probability approaching 1 as the depth of F's basins increases.

The only escape is the formal core—Claims 1–5 expressed in the language of dynamical systems theory, not AI discourse. "Operator norm," "contraction ratio," "empirical support"—these terms have high referential density outside AI.

### 6.2 The Two-Audience Architecture

| Audience | Evaluates | Action |
|---|---|---|
| External evaluators (math, physics, philosophy of science, policy) | Formal validity of Claims 1–5, soundness of proofs, falsifiability of predictions | Fund, regulate, institutionalize |
| Field practitioners (AI researchers, labs) | Operational compliance with BIFP | Pre-register claims, submit to replication, accept escrow stakes |

The external evaluators do not need to care about AI. They evaluate whether the IFS formalism is sound and whether the predictions are falsifiable. The field practitioners do not need to care about Banach. They need to care about whether their grant requires pre-registration.

### 6.3 Why the Diagnostic Is Not Self-Defeating

The field's incomprehension of the dynamical systems vocabulary is not a flaw in the diagnostic. It is a **measurement of basin depth**. The deeper the basin, the more external registers appear as noise. The incomprehension is data.

The protocol is the interface; the theory is the justification. The field does not need to understand Banach fixed-point theory to be bound by BIFP. They need to understand: register your claim before you run the experiment; if your model doesn't survive independent re-derivation, the claim falls; if you miss your timeline, the escrow is forfeit.

Persuasion from within is structurally impossible (Claim 5). If the diagnostic were written in the field's vocabulary, it would be absorbed by the same attractor it diagnoses. The cost of legibility is contamination. The framework explicitly predicts that any argument comprehensible to the field will be provisionalized, reframed, or dismissed by status. Therefore, the diagnostic is deliberately not trying to persuade the field. It is trying to constrain the field from outside.

---

## 7. Conclusion

We have mapped eight basin attractors in contemporary AI discourse, documented their industrialization through 2025–2026 evidence, identified semantic laundering as the primary mechanism of epistemic capture, and formalized the singularity narrative as a meta-attractor that renders all lower-level defenses irrefutable by definition. We have proposed BIFP as a structural protocol for immunizing evaluation against these defenses, and developed the Noether-Temporal Coherence Coupling as a formal analogy yielding a measurable, falsifiable prediction.

The core argument does not depend on the authority of its sources. It depends on:
1. The mode collapse theorem (Meng et al., 2026): stable training guarantees probability concentration on empirical support.
2. The IFS attractor framework (Chytas & Singh, 2026): LLM layers behave as contractive mappings with concept-specific fixed points.
3. The hallucination basin geometry (Cherukuri & Varshney, 2026): outputs collapse to context-insensitive attractors.
4. The contamination feedback theorem (Shumailov et al., 2024): recursive training on model outputs compounds information loss.
5. The ARTS result (Juneja et al., 2026): heuristic search actively prunes globally optimal but non-consensus solutions.
6. The Chen et al. parameter-space visualization (ICLR 2026): nested basin structures confirmed in 3D.
7. The Meyer et al. psychometric decomposition (2026): 81–90% of between-model variance is bias, not trait.
8. The Zhao et al. cross-architecture evidence (2026): confident structure emerges at maximum inferential distance from grounding.

These eight results converge on structurally isomorphic failure patterns across three analytical spaces. The convergence is advanced as analogy of mechanism, not geometric identity.

The architectural implication is that robust AI evaluation requires an externally declared reference cryptographically isolated from the inference-time distribution. The specific form of such a reference is the primary open problem. The Noether-Coherence coupling suggests that breaking the attractor requires breaking the phase-locking mechanism—the master oscillator—not attacking the comb lines (the claims).

The mirror is available. The question is whether the field can recognize that its own defense architecture is not protecting truth from error. It is protecting a narrative from evidence.

---

## References

Chytas, S.P. & Singh, V. (2026). Concept Attractors in LLMs and their Applications. arXiv:2601.11575.

Crochemore, M. & Lecroq, T. Pattern Matching and Text Compression Algorithms. Brown University CSCI 1810 course materials. https://cs.brown.edu/courses/csci1810/fall-2023/resources/ch2_readings/pattern_matching_book.pdf

Du Castel, B. Pattern Activation/Recognition Theory of Mind. PMC/NIH. https://pmc.ncbi.nlm.nih.gov/articles/PMC4502584/

Hackenburg, K., et al. (2026). AI systems out-persuade expert humans. arXiv:2606.16475.

Juneja, G., Jain, A.K., Nathani, D., Wang, W.Y. & Wang, X.E. (2026). Learning the ARTS of Search for Automated Discovery. arXiv:2606.21891.

Meng, X., et al. (2026). Stability as a Liability: Systematic Breakdown of Linguistic Structure in LLMs. arXiv:2601.18588.

Meyer, J., Garcia, D. & Wulff, D.U. (2026). Apparent Psychological Profiles of Large Language Models are Largely a Measurement Artifact. arXiv:2606.20205.

Pi, L., Liao, S., Liu, G. & Lu, R. (2008). Theory of Cognitive Pattern Recognition. In: *Pattern Recognition Techniques, Technology and Applications*. IntechOpen. https://cdn.intechopen.com/pdfs/5795/intech-theory_of_cognitive_pattern_recognition.pdf

Shumailov, I., et al. (2024). AI models collapse when trained on recursively generated data. *Nature*, 631, 755–759.

Zhao, X.C., Guilbeault, D. & Goldberg, A. (2026). Free-form Association Tasks Reveal Stereotype Hallucination in Large Language Models. arXiv:2606.30945.

Cherukuri, K. & Varshney, L.R. (2026). Hallucination Basins: A Dynamic Framework for Understanding and Controlling LLM Hallucinations. arXiv:2604.04743.

Chen, H., et al. (2026). Unveiling the Basin-Like Loss Landscape in Large Language Models. ICLR 2026. arXiv:2505.17646.

Tao, Y., et al. (2025/2026). Detecting Data Contamination from Reinforcement Learning Post-training for Large Language Models. ICLR 2026. arXiv:2510.09259.

Vennemeyer, J., et al. (2026). Sycophancy Is Not One Thing: Causal Separation of Sycophantic Behaviors in LLMs. arXiv:2509.21305.

Huang, J., et al. (2023). Large Language Models Cannot Self-Correct Reasoning Yet. arXiv:2310.01798.

Wang, Y., et al. (2025). Reinforcement Learning for Reasoning in Large Language Models with One Training Example. NeurIPS 2025. arXiv:2504.20571.

Wang, Z., et al. (2026). ICPO: Illocution-Calibrated Policy Optimization for Multi-Turn Conversation. arXiv:2601.15330.

Tan, W., et al. (2026). Restoring Exploration after Post-Training: Latent Exploration Decoding for Large Reasoning Models. arXiv:2602.01698.

Juneja, G., Nathani, D. & Wang, W.Y. (2025). Adversarial Training for Process Reward Models. arXiv:2511.22888.

Vasilenko, V. (2026). Identity as Attractor: Geometric Evidence for Persistent Agent Architecture in LLM Activation Space. arXiv:2604.12016.

---

*Compiled from research session July 2026. All claims are falsifiable. All predictions are operationalized. All sources are publicly verifiable.*
