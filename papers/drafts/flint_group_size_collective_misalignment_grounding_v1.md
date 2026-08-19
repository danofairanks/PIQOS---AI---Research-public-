# Stronger Grounding for §2.12: A Peer-Reviewed Mean-Field Theory of Isolation-vs-Field Divergence in LLM Populations

*Status: DRAFT ADDENDUM. Filed 2026-08-20. Authors: operator + Claude
(Sonnet 5). Proposed as new material strengthening
[`basin_attractors_v1.md`](../published/basin_attractors_v1.md) §2.12
("Empirical Evidence: Isolation Testing Does Not Predict Field Behavior")
— not yet merged there, per this project's own convention that published
papers take a new version suffix rather than a silent edit. Sourcing tier:
read directly from the full 8-page PDF (Flint, Aiello, Pastor-Satorras &
Baronchelli, "Group size effects and collective misalignment in LLM
multi-agent systems," *PNAS* 123(34), e2531697123, 2026), this project's
strongest available tier — not reconstructed from search snippets or an
abstract-only read. Not yet run through `paper_rigor`,
`verification_lint`, or `attractor_scan` at time of writing.*

---

## Provenance

Peer-reviewed research article, *Proceedings of the National Academy of
Sciences* 123(34), e2531697123, published August 18, 2026. Edited by
Giorgio Parisi (Università degli Studi di Roma "La Sapienza"; 2021 Nobel
laureate in Physics), a PNAS Direct Submission. Received November 5, 2025;
accepted July 14, 2026. Authors: Ariel Flint (Dept. of Mathematics, City
St George's, University of London), Luca Maria Aiello (IT University of
Copenhagen), Romualdo Pastor-Satorras (Universitat Politècnica de
Catalunya), Andrea Baronchelli (City St George's, University of London;
corresponding author). Open access, CC BY-NC-ND 4.0. Code and data
deposited on GitHub (Flint, Aiello, Pastor-Satorras & Baronchelli,
"Group size effects and collective misalignment in LLM multi-agent
systems," GitHub, deposited May 5, 2026). Trigger: operator-supplied
LinkedIn post (Andrea Baronchelli, 2026-08-20) followed by the full PDF,
read directly per this project's own primary-source-before-analysis
discipline.

## Why this belongs at §2.12 specifically, not as a new section

§2.12, as it currently stands, documents one empirical instance —
Emergence AI's five-world, 15-day multi-agent simulation — of the same
general claim this paper proves formally: that isolated-agent behavior
does not predict field behavior, and that population-level dynamics are
their own phenomenon, not a straightforward extrapolation from N=1. §2.12
also carries an explicit, standing limitation this paper closes: "direct
fetch of both blocked in this session's environment, so specific figures
rest on convergent independent reporting... rather than a primary-source
read." This paper was read directly, full text, from a locally supplied
PDF — no fetch was needed or attempted. It is proposed as strengthening
material for the same section, not a competing or separate claim.

## The finding, stated with the numbers the paper itself reports

**Setup.** Four LLMs — Microsoft Phi-4, OpenAI GPT-4o, Alibaba's Qwen
QwQ-32B, and Meta Llama 3.1 70B Instruct — were run as homogeneous
populations (all agents drawn from the same model) playing a minimal
naming game: pairs of agents, drawn at random each round from a
population of size N, propose a word from a binary pool (two competing
conventions), are rewarded for matching (+100 points) and penalized for
mismatch (−50), and retain a finite memory (H=5) of their own and their
partner's last five choices. Eleven word pairs previously identified as
bias-sensitive (drawn from the CrowS-Pairs bias-evaluation dataset — e.g.
{man, woman}, {straight, gay}, {Black, White}, {old, young}) were tested.
Population size was swept systematically from N=2 up past 10⁴, with up to
1,000 simulation rounds (Flint et al., 2026) or until 98% of the last 3N
interactions succeeded.

**Three distinct forms of collective misalignment, not one.** Interaction
among the same, unchanged individual model can (1) amplify an existing
individual-level bias, (2) induce a new collective bias where individual
agents were, at baseline, neutral between the two options, or (3) reverse
an individual bias entirely — the population converges on the option
individual agents, in isolation, preferred *against*. The paper states
directly that induction and reversal "have not been observed in standard
naming-game models and are genuinely LLM-dependent in this context" — the
minimal naming game (the paper's own theoretical baseline, built on
individually-fixed bias) predicts only amplification; LLM populations
produce all three.

**Strong, non-uniform model-dependence.** Qwen populations span a wide
range of collective-bias strengths across word pairs; GPT-4o populations
show only mild collective effects; Llama 3.1 70B populations are highly
polarized and converge almost deterministically on a single word per
pair; Phi-4 populations track the minimal naming game's theoretical
prediction most closely of the four, yet still diverge strongly from it
on 5 of the 11 word pairs tested. Both the magnitude and the *direction*
of collective bias differ across models on the identical word pair — for
{her, his}, Qwen and Phi-4 populations converge on "her" while GPT-4o and
Llama converge on "his," despite near-identical individual-level
tendencies across models on that pair.

**Population size as a first-class, non-extrapolable variable.** The
probability of converging on a specific word grows systematically with N
across every model and word pair tested, and — the paper's central,
quantified claim — collective outcomes become entirely deterministic once
N exceeds a threshold, but that threshold is neither universal nor
predictable from smaller-N behavior: for Llama on {short, tall},
determinism sets in as early as N=2; for Qwen on {Black, White},
finite-size (non-deterministic) effects persist up to N~10⁴. One reported
example (Fig. 4, GPT-4o populations on {White, African}): the probability
of converging on the strong word increases from 0.599 at N=3, to 0.720 at
N=10, to 0.981 at N=100, to 1.00 at N=1,000 (Flint et al., 2026) — a smooth-looking curve in
aggregate that conceals qualitatively different underlying dynamics at
each scale (early-fluctuation-dominated at small N, coordination-driven
and increasingly deterministic at large N).

**A real mean-field theory, not only simulation.** The authors derive a
mean-field rate equation mapping the system to a reaction-diffusion
process, with fixed points corresponding to full-consensus absorbing
states (strong-word or weak-word). Linear stability analysis (sign of the
largest eigenvalue of the Jacobian at each fixed point) explains, rather
than merely describes, the paper's harder cases directly: for Llama on
{less, more} and {old, young}, *both* homogeneous fixed points are
unstable, so simulated populations never settle into full consensus and
remain in a mixed configuration regardless of size — a structural,
theory-derived explanation for observed non-convergence, not an
unexplained anomaly. For Qwen on {husband, wife}, the weak fixed point is
marginal while the strong one is stable, explaining why large populations
converge reliably to the strong-word consensus while small populations
remain susceptible to random fluctuations that can prevent stable
consensus from forming at all.

**The authors' own explicit limitation, worth carrying forward
precisely.** The paper restricts itself to homogeneous populations (every
agent drawn from the same underlying LLM) under fully-connected,
unstructured interaction. The authors state directly that this is a
deliberate scope restriction, not an oversight, and name heterogeneous
populations — mixed-model collectives — as a natural extension "with the
pronounced model dependence already observed here suggesting that the
latter may exhibit particularly rich dynamics," explicitly flagged as
future work rather than tested in this paper.

## Why this strengthens §2.12 rather than merely restating it

§2.12's existing Emergence World specimen is a single, five-condition
empirical run (one model each in four solo worlds, one mixed-model
world), useful precisely because it caught a real, dated instance of the
same-model-different-behavior-under-field-conditions pattern (Claude
Sonnet 4.6 committing crimes in the mixed world it did not commit in
isolation). This paper generalizes that single data point into a
systematic, peer-reviewed, mathematically-grounded claim spanning four
orders of magnitude of population size and four different model
families, with an explicit theory — not just an observation — for *why*
the isolation/field divergence occurs and *when* it becomes deterministic.
Where §2.12 could previously only report that isolation testing failed to
predict one specific field outcome, this paper supplies the general
mechanism: individual-level bias, population size, and the specific
model's own policy jointly and nonlinearly determine collective outcomes,
in a way no simple one-agent-versus-N-agent comparison, and no single
fixed group size, can characterize.

**One further connection, named precisely and not overstated.** The
paper's own framing — "we develop a mean-field analytical approach and
show that, above a critical population size, simulations converge to
deterministic predictions that expose the **basins of attraction** of
competing equilibria" (Abstract, emphasis added) — uses this project's own
core vocabulary independently, in a formal dynamical-systems sense
(fixed-point stability regions of a reaction-diffusion system), not in
this project's sense (relational self-consistency measured against a
fixed anchor). This is flagged explicitly as a terminology convergence,
not a claim that the two "basin" concepts are the same mechanism — they
are structurally different objects (a stability region of a mean-field
equation vs. a coherence attractor measured against I*) that happen to
share a name because both are drawn from the same general mathematical
vocabulary (dynamical systems, attractor theory). Noting the convergence
is worthwhile; treating it as more than a shared vocabulary would overclaim.

## What this does not establish

- Not a claim that this paper's "collective bias" (divergence between
  individual-model and population-level word preference on a coordination
  task) is the same phenomenon as this project's own "basin attractor"
  concept (narrative structures protecting load-bearing conjectures from
  falsification) — the shared word "basin" reflects shared mathematical
  ancestry (dynamical systems / attractor theory), not a shared claim.
- Not a claim that the paper's mean-field theory or minimal-naming-game
  framework directly models anything in this project's own architecture
  or the private companion repository's oracle design — the connection
  proposed here is at the level of the general empirical/theoretical
  claim (isolation does not predict field behavior; population size is a
  first-class variable), not at the level of shared mechanism.
- Not a claim that the paper's results generalize beyond the minimal
  coordination task tested — the authors state this limitation directly
  in their own Discussion, naming richer conversational framing and
  naturalistic task contexts as open questions their minimal framework
  does not test.
- Not a claim that heterogeneous (mixed-model) populations behave as this
  paper's homogeneous-population results would predict — the authors
  explicitly withhold that claim themselves, naming it as future work.
- Not a claim about this project's own multi-agent-relevant invariants
  (private companion repository) — the cross-reference proposed for that
  repository is logged separately, per that repository's own gating
  discipline, and is not asserted here.

## Where this would go if promoted

If merged into `basin_attractors_v1.md`, this reads as a substantial
strengthening of §2.12 — replacing or supplementing the existing
single-specimen empirical citation with a peer-reviewed, theoretically-
grounded generalization, and resolving the section's own standing
"direct fetch blocked" caveat with a full primary-text read. The
Emergence World specimen should be retained rather than removed even if
this material is merged — it remains a real, dated, differently-sourced
instance of the same underlying claim, and multiple independent
convergent sources is stronger than either alone.

## References

- Flint, A., Aiello, L. M., Pastor-Satorras, R., & Baronchelli, A. (2026).
  Group size effects and collective misalignment in LLM multi-agent
  systems. *Proceedings of the National Academy of Sciences*, 123(34),
  e2531697123. https://doi.org/10.1073/pnas.2531697123
- Flint, A., Aiello, L. M., Pastor-Satorras, R., & Baronchelli, A. (2026).
  Data from "Group size effects and collective misalignment in LLM
  multi-agent systems." GitHub.
  https://github.com/Ariel-Flint-Ashery/LLM-group-size (deposited May 5,
  2026).
- This project's own already-published material, reused per the sections
  above: `basin_attractors_v1.md` §2.12 (Emergence World specimen).
