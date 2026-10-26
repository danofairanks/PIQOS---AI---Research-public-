# Reading a Convex-Equilibrium Paper's Certificates: "Convex Equilibrium Potentials for Monge-Ampere" (arXiv:2610.31386v1)

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one preprint, "Convex Equilibrium Potentials for Monge-Ampère: Curvature Bounds and A Posteriori Evaluation" (arXiv:2610.31386v1, 22 October 2026, 26 pages). The authors are called "the authors"; the organisations the paper names are CINVESTAV and IBM Research. The authors' repository is named by its path, `github.com/EdisonVazquezG/monge-ampere-equilibrium`; it was not fetched or run. No intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance; one reader, an AI system. The paper's AI-use statement names Claude among the tools used, and the reader is also an Anthropic model, so this is a same-developer reading and the usual same-source caveat applies. **No predictions were preregistered**: this is a same-session evaluation, and the checks below were designed after reading the paper.

## 1. What was read, and how

- **Read (E2):** all 26 pages. The proofs of Lemma 4.1, Theorems 4.2, 4.4, 4.6 and 5.1 (Appendix E.1 re-derived), Corollary 5.2 and Proposition 6.3 were followed.
- **Executed (E1):** two scripts, `check_bounds_and_sharpness.py` and `check_thm51_certificate.py` (numpy and scipy only, seeds fixed in the scripts, outputs committed).
- **Re-verification on 2026-10-26.** The PDF was re-fetched from arXiv and its sha256 matches the one recorded when the paper was read (`1b895a68…daee4d`, 26 pages). `quote_checks_output.txt` reports how many double-quoted strings in this draft occur in the PDF's text layer. Both scripts re-ran and reproduced their committed outputs.

## 2. What the paper claims

Softplus equilibrium networks with W ≥ 0, w ≥ 0, ‖W‖∞ ≤ q < 1 are convex. Hessian norm ≤ ‖w‖₁K_A² min{δ⁻², 1/(4δ³)} (δ = 1−q) via the cancellation 0 ≤ Sγ ≤ 1, with δ⁻² sharp over the class (one-neuron family); third derivative ≤ (1+3q)‖w‖₁K_A³δ⁻³, sharp exponent. Residual-based a posteriori bounds on state, first and second derivatives, and (n = 2) the Hessian determinant at an approximate equilibrium; Arb interval arithmetic over a box cover gives uniform residual and boundary bounds on the unit disk, and a comparison argument gives a solution-error bound ‖u−v‖ ≤ B∂ + ½√R. Two manufactured Dirichlet problems, three seeds each, all six models certified with R < 0.25 and B∂ < 0.01; adaptive float64 evaluation up to ~2× faster, certified adaptive evaluation slower.

## 3. Checked here (E1/E2)

- Proofs read and followed: Lemma 4.1, Theorems 4.2, 4.4, 4.6, Theorem 5.1 (appendix E.1 re-derived: B(J−Ĵ) = (Ψ−Ψ̂)v̂ − r), Corollary 5.2 (cofactor / nuclear norm), Proposition 6.3 (barrier b(x) = √R(‖x‖²−1)/2). No error found.
- `check_bounds_and_sharpness.py`: 1,200 random networks (q ∈ {0.5, 0.9, 0.99}, m ≤ 8, n = 2): max Sγ = 0.691 (≤ 1), max ‖H‖₂/C₂ = 0.385 (≤ 1). One-neuron family at ε ∈ {0.2, 0.05, 0.01, 0.002}: z\*(0) = −log ε; u″ matches (1−ε)/(ε²(2−ε)³) to printed precision; ε²u″ → 0.1251; u‴ by finite difference matches (1−ε)(1−ε+ε²)/(ε³(2−ε)⁵); ε³u‴ → 0.0313 (≈ 1/32).
- `check_thm51_certificate.py`: 3,000 perturbed approximate states (random W, A, b, w, q ∈ {0.3, 0.7, 0.9, 0.97}): max error/bound ratios 0.863 (state), 0.883 (J), 0.896 (K), 0.743 (H), 0.285 (det); none above 1. Seeds fixed in the scripts; outputs committed.
- Not checked: the Arb implementation, the box cover and its audits, Tables 1–4 and Figures 2–5 values, the references (not individually verified), anything in the authors' repository.

## 4. Weaknesses (E2/E3)

1. The sharp (1−q)⁻² result is not exercised by the experiments: trained models have ‖W‖∞ 0.58–0.66 (δ ≳ 0.34), where the cubic branch of the bound is smaller (stated by the authors, §8.3). Exponent sharpness rests on the analytic family only.
2. "Certified" depends on targets that bind: R ≤ 0.25 against f = 1 (P1) and up to 4.84 (P2); five of six models met it on the first cover; P2/seed 2 missed (0.4377) and was refined post hoc (disclosed) to 0.249951; the other two P2 bounds are 0.249993 and 0.249997, i.e. at the stopping rule. Observed sup residual is 0.046–0.10.
3. Solution-error certificate: barrier bound 0.243–0.260 against observed 0.004–0.006 (~50×); the tighter "direct" bounds (0.047–0.115) use the known manufactured solution and are not a method for unknown solutions.
4. Speed: baseline is fixed 32 iterations, well beyond what the tolerances need, so the ~2× is partly baseline-chosen; adaptive float64 has no roundoff enclosure; the rigorous adaptive path is 1.5–2.7× slower; Arb cohort is 8 points/model versus 512 for float64 (different cohorts, acknowledged).
5. Scope: determinant certificate n = 2 only; box cover exponential in dimension (~16k boxes at depth 9 in 2D); two smooth strictly convex targets; no comparison with explicit ICNNs or other solvers (acknowledged); abstract's "fully nonlinear PDEs" is broader than the 2D evidence.
6. Rigor ends at the implementation (authors: not formal verification of the stack).

## 5. Circularity and falsifiability

No circularity was found in the theory; the violation counts use float64 reference diagnostics with a stated 10⁻¹¹ floor. Claims are falsifiable inequalities. No self-citation loop (no self-citations). Limits stated plainly (not stacked).

## 6. Possible patterns (E3; one instance, not a pattern yet)

- *A posteriori certificate on a frozen object.* Guarantee attaches to the evaluated artifact, not to the training process; a bad model fails to certify rather than certifying wrongly. Compare with other "verified"/"certified" claims for whether the guarantee fails closed.
- *Threshold that binds.* Reported "all six trained models are certified" where refinement runs until the target is met, so the reported bound equals the target and says little about the model. Check for post-hoc refinement and for bounds hugging the target.
- *Sharp theory, unexercised in experiments.* Headline theoretical result in a regime the experiments do not reach; the paper discloses it.
- *Speedup against a convenient fixed baseline.* Check what a tolerance-matched fixed baseline would give.

## 7. What this does and does not establish

- It supports the paper's central inequalities in the regimes executed (no error found in the proofs read; no counterexample among 1,200 and 3,000 random cases), and it shows where the headline wording ("certified", the speedup, "fully nonlinear PDEs") is broader than the evidence executed.
- It does not verify the Arb implementation, the box cover or the tables, and it does not show the paper is wrong anywhere.
- One reader, one session, no preregistration; author code unread; Tables 1–4 and Arb results taken as reported; references unverified. If the code or a v2 appears, rerun with preregistered predictions and compare R, B∂ and the P2/seed 2 refinement.

## 8. Reproduction

Everything is in `convex_equilibrium_reading_v1/`: the two scripts and their outputs; `quote_checks_output.txt` (needs the preprint PDF and `pdftotext`; the PDF is not stored here); `tool_scan_*.json`.

## References

Sources: arXiv:2610.31386v1 (22 October 2026), PDF sha256 `1b895a68b4d09fcc249104a71b94d531ee63cd3e8a0bccef19e3e0d956bdaee4`.

## Revision log

- *2026-10-26, v1.* First public version, from the reader's working notes of 2026-10-23. One section heading was renamed and cross-references to working notes are not carried over.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
