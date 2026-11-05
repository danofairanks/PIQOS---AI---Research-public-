# A Consciousness-Architecture Proposal Read for What It Can Be Tested On: Four Preprints, Five Counter-Models and One Layer Question

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** Four arXiv preprints by the same two authors, read together: 2609.23828 (submitted 20 September 2026; the main proposal), 2609.20437 (17 September; the formal model), 2609.38495 (29 September; a comparison with Global Neuronal Workspace Theory) and 2610.04057 (2 October; a comparison with Recurrent Processing Theory). The authors are called "the authors" and are not named; the architecture is named as the papers name it (the Motivated Emotional Mind, "MEM"). No intent is attributed. The authors have not been contacted for this version.

**Disclosure.** Read and drafted with AI assistance; the reader is an Anthropic model. Predictions were written before reading (a generic list, then a topic list after the abstract of the main paper) and before each toy was run; the preregistrations and their amendments are in `mem_proposal_reading_v1/counter_models/`. The papers make no claim about any Anthropic system. One reader, no independent blind pass yet.

## 1. What the papers are

A conceptual proposal and three companions. The main paper argues that excitability, homeostasis, learning, hierarchy and language do not suffice for attributing consciousness to an artificial system, and proposes that an architecture with receptor-grounded representations, interoception coupled to regulation, affect, associative memory units ("semblions") and content-specific re-entry into lower sensory and interoceptive maps is the relevant candidate. It states that it does "not attribute consciousness to any existing artificial system", presents MEM as "a falsifiable research program", and proposes nine tests (humans, cephalopods, simple invertebrates, a synthetic agent). It contains no new data, simulation or analysis. The formal paper gives the equations; the GNWT paper reinterprets 25 published studies through MEM and scores them; the RPT paper positions MEM as an extension of recurrent-processing theory and adds six predictions.

## 2. What they do well

- Non-claims are explicit and carried through: existing language, vision-language-action and robotic systems are classified as not warranting a subject-level attribution; sufficiency is not claimed; substrate independence is left open.
- The testing section can lose. It names four conditions that would weaken the architecture, requires hybrid rivals to be admitted, specifies capacity-matched ablations and distributions over initialisations, and follows the structure of a published adversarial collaboration.
- The GNWT paper concludes what its tables support ("post hoc compatibility cannot substitute for prospective prediction"), and the RPT paper contains an epistemic-status table that separates the components it treats as settled from its strong constitutive claims and names its own theoretical risks.
- The arithmetic checked here reproduces (section 4).

## 3. What the papers cannot yet support (leads, not verdicts)

1. **The central criterion has no operational form.** The definition of a phenomenal state turns on a "suprathreshold interoceptive representation". The word appears four times in the main paper; no threshold, unit or measurement is given. As written, no system can be scored on it.
2. **The formal weight sits in a sister preprint.** The main paper reproduces six equations from a formal paper submitted three days earlier, and says "The equations do not prove consciousness". The formal paper has no simulation and states that its equations contain no consciousness variable. The definition is cited to a further preprint by one author. Two of the four papers have about 16% and 27% of their reference entries by the authors (pattern count, approximate).
3. **The comparison classes are partly hypothetical.** The main paper's Table 4 marks a "MEM agent" column with "central" or a tick for a design that has not been built, and compares it with existing system classes on criteria that design defines.
4. **A cross-reference does not match.** The main paper cites "Equation (31)" for the action-selection rule; in the formal paper that is Equation (29), and the minus sign in the formal paper's `arg max Q = - arg min J` as typeset is dropped in transcription. Low weight; recorded for accuracy.
5. **The claimed advantage is partly by construction.** The main paper says the architecture "encompasses a broader profile of prespecified indicators" than single-mechanism rivals, then warns that this would reflect "defining the theories unequally" unless hybrid rivals are admitted, and retreats to a weaker claim. The indicator list is the architecture's own.
6. **Part of the necessity claim is definitional.** The main paper (section 5) says re-entry is "a necessary condition of secondary perception", where secondary perception is defined as top-down reconstruction in sensory maps; necessity for phenomenality is the actual hypothesis, called "a new and significant hypothesis". The first proposed tests measure vividness, a report-adjacent quantity. Recent aphantasia work bears directly on early-cortex reinstatement and imagery and is not cited.
7. **Nearest prior art is missing from the reference list of the main paper.** A 2019 *Nature Machine Intelligence* perspective on homeostasis-inspired "feeling machines" (Man and Damasio) and a 2025 *Behavioral and Brain Sciences* target article on biological naturalism (Seth) are not cited, though the paper cites related work on interoception and indicator properties. Checked by searching the reference list; relevance is the reader's inference from titles and abstracts.
8. **The claim is stated at different strengths in different papers.** The main paper: re-entry "may be necessary for phenomenality". The RPT paper: a section titled "Secondary perception as the Core of Phenomenal Consciousness in MEM", and the "sufficiency of secondary perception for phenomenality" as a hypothesis; and, in its limitations, the identity reading "the process viewed from the first-person perspective". Necessary, core, sufficient and identical are four claims of different strength, each hedged separately, so no single test is tied to one of them. The GNWT paper separates "strong MEM" falsifiers from moderate versions that "must specify in advance which of these conditions they regard as central"; no paper says which version the authors hold.
9. **Feasibility.** The proposed human test of re-entry asks for a reversible perturbation of feedback to one lower-level map that spares feedforward encoding, attention and working memory; whether any current method achieves that separation is not argued.

## 4. Arithmetic checked

The GNWT paper scores 25 studies 1-6 on 16 criteria, takes a weighted mean per criterion (E), assigns each theory a "scope" score (M) and reports K = min(M, E). `rating_check/chk_gnwt.py` recomputes E from the paper's Table 5: every printed E reproduces (largest difference 0.00), as do the Table 3 K values and Table 4 means. E is the same for both theories by definition, so K is identical for both wherever both M are at least E: that is 11 of 16 criteria by construction. K differs only where an author-assigned M falls below E. The overall MEM-minus-GNWT difference in mean K is +0.07 over all 16 criteria, -0.06 over the 12 GNWT-canon items, and +0.20 over the 13 interoception items that the authors chose as MEM-relevant (their own note says this selection favours MEM); with M = 6 for both theories the difference is zero. The paper states "a structured synthesis rather than a meta-analysis", and does not claim more than compatibility. The sentence giving a mean fit of 5.09 for MEM and 3.00 for GNWT on items 13-25 could not be derived from the printed tables (not checked further).

## 5. Disclaimers beside structure that carries the disclaimed claim

A disclaimer can be sound and the surrounding layout can still carry the claim. Judged by the reader, with no blinded test run; the checker's deletion test (remove the disclaiming cell and ask what a reader infers) was not run on readers.

- Table 3, MEM-like agent row: the disclaimer "no evidence that they constitute a sufficient condition" sits beside "more architectural requirements indicative of phenomenal consciousness"; other rows in the column read "no basis for attributing subject-level consciousness" or "not in itself an indicator of phenomenality".
- Table 4, "Phenomenal evidence": existing system classes read "none"; biology and the MEM agent read "unresolved". The MEM agent is a design, so its evidence is also none.
- The GNWT paper's M/K tables carry "not a ranking" notes beside a layout that reports MEM at 6.00 and GNWT at 4.25 on phenomenality, with the scores assigned by the authors.
- The main abstract says the formal model "makes the proposal more precise and testable"; the formal paper contains no variable for phenomenality and no simulation.

## 6. Counter-models and defeat conditions

Method as in `../pre_execution_gate_counter_models_v1.md`: claim forms extracted; defeat conditions written and hashed before any toy existed; results labelled defeated at scope, not reached, or blocked; toys use only the papers' own definitions plus standard tabular Q-learning and standard attention. Preregistration: `counter_models/PREREG_DEFEAT_CONDITIONS.md`; amendments: `counter_models/AMENDMENTS.md`. Two flaws of mine found after the first runs (a modulation bug that made T5 run 1 invalid; tuned parameters at the grid edge in T4) are recorded as amendments, not edits; run 1 outputs are kept.

| Claim form | Toy | Result (seed- and parameter-specific; qualitative defeats are not) |
|---|---|---|
| Formal score "unlike ordinary classification" (Eq. 6-7) | Classifier on the concatenated input, 10^4 instances, dot, cosine, RBF | **Defeated at scope (formal level).** Differences at floating-point level, argmax agreement 100%; the identity is algebraic and the run checks my implementation. |
| Re-entry / secondary perception as Eq. 13-14 | Top-k sparse attention with pairwise bias and residual mix | **Defeated at scope (formal level only).** Difference 1.1e-14 over 3000 instances. What the papers say separates re-entry from this step is the provenance of the stored prototypes (receptor-grounded) and physical lower-level maps; neither is in the formalism, so that part is blocked, not defeated. |
| A disconnect/restore test separates coupled interoception from telemetry | Tabular agents, one allostatic variable, sensor stuck at "full" for 60 steps then restored | **Defeated at scope.** A plain RL agent that reads the battery as an observation passes the test as the coupled agent does (recharge frequency 0.34 to 0.00 to 0.35 for both); an agent that ignores the reading does not. Learning-rate modulation by affect separates the two, by construction; the specific test is not sufficient alone. |
| A resource-matched rival cannot explain the affect-modulation result | Two regulated variables, hidden food patch changing every 100 episodes, 15 tuned configurations each, 30 fresh seeds | **Defeated at scope** under a reading rule fixed before run 2. Modulation beats fixed-parameter homeostatic RL by 11.9 SE; a simple tuned schedule keyed to the same regulatory cost beats the affect-signal form by 2.96 SE (run 1: 14.2 SE and 2.30 SE). Modulation of learning by regulatory pressure is a real effect here; the specific form of the affect signal is not shown to matter. Disclosures: the rival schedule is not the same function; tuned parameters sit at the grid maximum for both in run 2; the exploration term is simplified. |
| An interaction among components is the basic unit of inference | 2x2 factorial of two independently implemented modulators, 30 seeds per cell | **Not reached.** The preregistered condition (significance flips with the measurement scale) is not met: the interaction is present on both scales (raw +19.4, CI +11.0 to +27.9; log +0.150, CI +0.04 to +0.26). Post hoc, not preregistered: two independent modulators interact sub-additively and the sign is opposite to the paper's predicted direction; a floor effect on regulatory cost is the likely reason. |
| Re-entry necessary for vividness or phenomenality; "suprathreshold" interoception; identity with a biophysical configuration | none | **Blocked.** No operational definition of phenomenality, vividness or the threshold for any artificial system; nothing built. |

The toys attack contrasts the papers draw, at the scope stated, and several of those contrasts are narrowed by the papers themselves. None touches the claims that carry the consciousness thesis.

## 7. What layer the proposal sits at

- **As evidence:** post hoc. The GNWT paper reinterprets published studies after the fact and says so; its ratings and scope scores are assigned by the proposers, so the input to the scoring is written by the party being scored. The prospective program (preregistered tests, independent data collection) is the only layer where the check would not be written by the proposers, and it has not been run.
- **As an agent design:** the hypothetical agent edits its own accumulated state (valences, a program repertoire, generated goals) and consolidates a new program when the improvement in its own simulated value passes a threshold. That is a self-modifying loop whose gate input is computed by the agent. The tolerated bounds are described as shifting "with posture, exertion, circadian phase, development, task demands, or social context", with no stated owner or rule, and the thresholds are free parameters. Loops of this kind have documented gate-leakage failures in the self-evolving-agent literature; nothing in the papers says why this design would differ. The ethical safeguards named in the main paper (stopping thresholds, state monitoring) rest on variables the agent itself produces.
- **Binding issues, as in this repository's other readings:** (a) the check runs on a channel the checked side writes (proposer-assigned scores; designer-declared coupling; the system's own report, which the main paper itself treats as "primarily a generated report" for language models); (b) a safeguard or attribution decision bound to a profile evaluated at one time, for an agent that keeps changing, with no version binding of the evaluated state; (c) no custody of predictions and analysis plans outside the authors, though the proposed adversarial collaboration partly covers this.
- **What a surviving form would need (conditions, not advice):** predictions and analysis plans hashed and held outside the authors; an independent observation channel for coupling (physical intervention on the real regulatory variable, with an external trace, not the agent's telemetry); version-binding of any profile used for attribution or safeguards; bounds and thresholds outside the agent's write set; an operational, measured definition of "suprathreshold"; a stated choice among necessary, core, sufficient and identical, and between strong and moderate MEM. Since the affect-modulation form is matched by a simple schedule at toy scale, the discriminating content has to lie in grounding provenance and re-entry, which have no operational definition today; until they do, the surviving claim is a research program, not a tested theory.

## 8. Evidence tier and deeper-pass flag

**Tier.** E1 executed or read directly: full text of the main paper and the arithmetic and equations named above; sections of the three companions that carry the argument (the middle expository sections and the 25 per-study reinterpretations were not read in full); the toys' outputs; arXiv metadata. E2 read: relevance of the prior art, the reading of "necessity", the feasibility remark, the layer placement. E3 not checked: the authors' earlier single-author papers and a second reader.
**Deeper pass.** Read the 25 per-study reinterpretations; read the cited aphantasia and interoception literature in primary form; run the deletion test on blinded readers; a second reader on section 5 and on the layer reading.

## 9. What this reading does not claim, and what was verified

- No claim is made about whether MEM is correct, or whether any machine is or could be conscious; none about the authors' motives or competence.
- Quoted strings were checked against the text layers of the four PDFs with `quote_checks.py` (result in `quote_check_results.txt`); the PDFs are not stored here (sha256 prefixes: 2609.23828 `c2df50db9a6a3edf`, 2609.38495 `52e9456feea2b709`, 2610.04057 `cbe511ca5a751803`, 2609.20437 `ea12c80c9bb664a0`).
- The public repository's own scanners were run on this draft (`tool_scan_*.json`); flags are leads, not verdicts.
- The toys are tabular and small; the formal-level identities are algebraic; none tests grounding, re-entry necessity or identity.

## 10. Limitations

- Four papers chosen because one is circulating; nothing here is a rate.
- One reader, the same model family as the drafting assistant; no author contact; no independent reproduction of the toys.
- Prior-art relevance rests on titles and abstracts of the works named.
- The post hoc observation in the interaction toy (sub-additivity, sign) is not preregistered and is not offered as a finding about the architecture.

## Version notes

- *2026-11-05, v1.* First public version.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
