# What Compiles: Auditing a Model-Generated Mathematics Release with the Lean Comparator

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** The audited object is a public repository, `github.com/openai/math`, and the organization that published it is named as the repository names itself. No individual is named, no intent is attributed, and nothing here is a statement about how the results were produced beyond what the release says. The unit of analysis is a formal statement and a machine verdict.

**Disclosure.** Drafted with AI assistance. The statement-fidelity readings in section 5 were made by one reader (the model that drafted this paper); no mathematician reviewed them. The controls and the logs are mechanical; the readings are not.

## 1. The question

In October 2026 an organization published 722 manuscripts in 372 "result families", produced by an unreleased internal model, with Lean formalizations for a subset. The question put to this audit was whether the formalized results are real reasoning or "harnessmaxxing": output tuned to pass a checker without establishing the claim. Four routes could make that suspicion true for a formalized result, and they are separable:

1. **The proof is unsound but accepted** (kernel bug, forbidden axiom, `sorry`, a computation trusted outside the kernel).
2. **The theorem checked is not the claim made** (a faithful-looking Lean statement that is weaker, vacuous, or junk-value-dependent).
3. **The checking setup can be steered** (the party that wrote the proof also wrote the thing it is checked against).
4. **The checked subset is not representative** (what is formalized is what is easy to formalize, and its pass rate is read as evidence for the rest).

Routes 1 and 3 are what the Lean Comparator is built to close; route 2 needs a human reading each statement; route 4 is a property of the catalogue. This paper reports what was run for 1 and 3, what was read for 2, and what was counted for 4. It does not test whether any process was "reasoning": a valid proof is valid regardless of its author, and the released reasoning summaries were not read.

## 2. What the release is (counted, not trusted)

From the repository at commit `adc7f1241` (single commit, 2026-10-06), by the companion script `census.py`:

- 722 manuscripts in 372 families; 162 manuscripts (22%) in 127 families (34%) have a formalization listed in `lean/formalization.yaml`; 405 Comparator configs with 507 theorem names, every one permitting exactly `propext`, `Quot.sound`, `Classical.choice`.
- The catalogue's own review field reads `status: "unchecked"`; its automation field lists the method as `agent`; its scope reads "Partial progress." The README says "Some of the unformalized results could have issues."
- Text checks over `OAI/` and `ComparatorChallenges/`: no `native_decide`, `ofReduceBool`, `unsafe`, `implemented_by`, `@[extern` or `sorryAx`; `sorry` appears in 404 of 405 challenge files and in no solution file (by design: the challenge states the theorem, the solution proves it); one challenge file states its claim with an `axiom`; three `axiom` hits in `OAI/` are inside comments. These are text checks, not verification.
- **Selection (route 4).** Of the ten results for which the release publishes reasoning summaries, six have no formalization listed (two-point correlations of multiplicative functions, the irrationality exponent of π, quasipolynomial Szemerédi bounds, the Mézard–Parisi formula, Bloch's law, free-group-factor isomorphism). Other high-stakes titles with none: the full BSD formula from low Selmer corank, Milne's rationality conjecture, Hilbert's tenth problem over ℚ. Formalization coverage tracks the tractability of a statement, not the significance of the claim, so the 22% that is machine-checked cannot vouch for the other 78%.

## 3. Method

Lean 4.34.1; Mathlib at the repository's own pin, built from source (the cache host was unreachable); the Comparator and `lean4export` at their v4.34.0 commits, rebuilt against 4.34.1; `landrun` for sandboxing. Exact pins are in `PINS.txt`. For each config the project contained only the OAI modules in the solution's import closure, copied unmodified, plus the challenge and its JSON, unmodified, with the repository's own compiler option (`autoImplicit false`). Each run was the Comparator's own procedure: build the challenge, export its statement, build the solution, export it, compare, and check axioms and the kernel.

Only 23 of the 405 configs have a challenge file and a solution closure that avoid a full `import Mathlib` and external packages (eleven of those 23 were run); 377 challenge files import all of Mathlib, which on this 4-core host would have been a multi-hour build. The configs run were therefore chosen by build feasibility, then by short statements, not by significance, and they are not a sample of the 405.

**Deviations from the Comparator's documented setup, all in the weaker direction** (for the eleven configs of this section's table; the later run of section 5.1 differs in further ways listed there, notably a prebuilt Mathlib cache). `landrun` could apply only a partial Landlock sandbox (kernel ABI v7; it ran with the `--best-effort` flag the Comparator passes); the systemd-run guard was not used; the builds ran as an unprivileged user with no network and a stripped environment instead; the Lean default kernel was the only kernel (no external kernel); `landrun` was v0.1.17 from `go install`, not a build of `main`.

## 4. Controls

Two negative controls on the first config show the harness discriminates:

- A challenge whose `GoodVertex` uses strict instead of non-strict inequality, paired with the real solution: rejected, `Const does not match between challenge and target 'OAI.SeymourSecondNeighborhood.GoodVertex'`.
- A solution module that states the theorem with `sorry`: rejected, `Illegal axiom detected: 'sorryAx'`.

In addition, `#print axioms` on the Seymour main theorem reports `[propext, Classical.choice, Quot.sound]`, and the solution contains 192 theorems and lemmas in 4861 lines with no `decide`-style bulk proofs.

## 5. Results

Eleven configs were attempted; 11 accepted, 0 rejected, 0 did not finish when this draft was last updated. "Accepted" is the Comparator's `Your solution is okay!`: the exported statement matches the challenge's, only the three permitted axioms are used, and the Lean default kernel accepts it.

| Config | Main theorem | Challenge lines | Solution modules | Solution lines | Comparator result |
|---|---|---|---|---|---|
| `SeymourSecondNeighborhood` | `exists_goodVertex` | 40 | 43 | 4861 | accepted |
| `FiniteCongruenceGraph` | `graph_criterion` | 63 | 2 | 469 | accepted |
| `GrahamSpherical` | `full_main` | 65 | 18 | 969 | accepted |
| `AbhyankarSathaye` | `exists_noncoordinate_polynomial` | 21 | 15 | 1445 | accepted |
| `SecondKahnKalai` | `secondKahnKalaiBounds` | 74 | 37 | 6753 | accepted |
| `GotsmanLinial` | `gotsmanLinialStatement` | 54 | 22 | 4022 | accepted |
| `FormulaHitting` | `universal_hitting` | 66 | 24 | 3281 | accepted |
| `ProjectionCounterexample` | `universal_simplex_upper_bound_false` | 45 | 41 | 3378 | accepted |
| `Dixmier` | `main_theorem_all_universes` | 51 | 32 | 3559 | accepted |
| `TalagrandDiscreteConvexity` | `talagrand_discrete_convexity` | 57 | 36 | 4259 | accepted |
| `TalagrandExpectationThreshold` | `talagrand_expectation_threshold_equivalence` | 60 | 47 | 4834 | accepted |

**Statement readings (route 2), for the accepted configs.** Reading each challenge statement against the English claim, as one reader. These are readings, not verification.

- *Seymour's second-neighborhood conjecture.* An oriented graph is loopless and asymmetric; first neighbors are out-neighbors; second neighbors are vertices other than `v`, not first neighbors, reachable by a path of length two (so sinks are included); a good vertex has at most as many first as second neighbors; the theorem asserts one exists in any nonempty finite oriented graph. This is the standard statement. The proof is a minimal-counterexample argument (reduction, pruning, extremal contradiction) in 43 modules.
- *`FiniteCongruenceGraph`.* A characterization: a finite lattice is the congruence lattice of a finite nonempty algebra if and only if it has a finite colored-graph witness. It is a criterion, not a solution of the finite lattice representation problem; algebras, congruences and the witness conditions are defined from scratch, so fidelity to the manuscript's witness definition is the part a specialist would have to check.
- *`GrahamSpherical`.* A specific 12-point subset of the unit circle (built from the parameter Σ 10^-(m+1)!) with a 50-coloring of every Euclidean space avoiding monochromatic isometric copies, and the denial that the set is Euclidean Ramsey. The statement bundles the witness, the point count, the sphere condition and the coloring claim, so the verdict is about that construction.
- *`AbhyankarSathaye`.* For every n at least 4, a polynomial F in n variables over ℂ with ℂ[x]/(F) isomorphic to a polynomial ring in n−1 variables and F not the image of a variable under any ℂ-algebra automorphism: the standard shape of a counterexample to the Abhyankar–Sathaye conjecture in high dimension.
- *`SecondKahnKalai`.* Explicit constants (2048·e^50 and 6144·e^50) bound the threshold at which G(n,p) contains a non-induced copy of H by the expectation threshold times (1 + log2 of the edge count), and times log2 n. The catalogue states "a universal C"; the Lean statement fixes the constants, which is a stronger form. The thresholds are infima over nonempty sets (at p = 1 a copy exists), so no empty-infimum junk value arises.
- *`GotsmanLinial`.* Average sensitivity of a degree-at-most-d multilinear polynomial threshold function on the n-cube is at most 8·d·√n, with the sign of 0 taken as +1. That convention makes the theorem cover polynomials that vanish somewhere on the cube, a slightly larger class than the usual nonvanishing one.
- *`FormulaHitting`.* A nonzero non-commutative formula of size at most s evaluates to a nonzero matrix on an explicit family of rational matrices of dimension 2·n·s². The formula, series and evaluation are defined in the file; self-contained.
- *`ProjectionCounterexample`.* In dimension 20 the simplex does not maximize the ratio of the volume of the projection body to the volume of the body to the power d−1. The proof is explicit: it computes the simplex's ratio as 21·20^20/20! and exhibits a product body whose ratio exceeds it by the factor 22355476/22020096, about 1.5%, so the junk-value concern that attaches to a negated universal over real-valued measures (a ratio defined through `toReal` of a possibly infinite measure) does not apply here.
- *`Dixmier`.* Every countable discrete nonamenable group has a uniformly 101-bounded representation on a separable Hilbert space that is not similar to a unitary one, with amenability defined as a positive normalized left-invariant mean on bounded complex functions. The definitions are standard in shape; universes are explicit.
- *`TalagrandDiscreteConvexity` and `TalagrandExpectationThreshold`.* Statements about families of finite sets with large explicit constants (2^75; 25·512^4): if a family has measure at least 1−2^-75 then the family of sets not contained in a union of 2^75 members is covered by generators of cost at most one half; and the fractional expectation threshold is at most 25·512^4 times the integral one for proper nonempty increasing families. Self-contained definitions; the constants are part of the statement.

Across the accepted configs the statements are short, the definitions are local, no config needed more than the three standard axioms, and the solutions range from 469 to 6753 lines.

### 5.1 A later run, on a result released after the pin (added 2026-10-27)

The release was updated on 26 October 2026 (repository head `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, committer date 2026-10-26; its `history.md` lists two new manuscripts with Lean formalizations). One of them, "Local smoothing for the Euclidean wave equation" (59 pages, dated 25 October, credited only to the organization), claims Sogge's local smoothing conjecture for the wave equation in every spatial dimension of at least two, with consequences for Bochner–Riesz means, Fourier restriction, Kakeya maximal estimates and the Hausdorff dimension of Kakeya sets. Its Lean counterpart is the config `ComparatorChallenges/LocalSmoothing.json`: six theorems, permitted axioms `propext`, `Quot.sound`, `Classical.choice`, solution module `OAI.Analysis.Fourier.LocalSmoothing.Comparator`. It was run once, on 2026-10-27. The pin of section 2 (6 October) cannot contain it.

| Config | Main theorem | Challenge lines | Solution modules | Solution lines | Comparator result |
|---|---|---|---|---|---|
| `LocalSmoothing` | `euclidean_local_smoothing` | 143 | 2261 | 190467 | accepted |

**Outcome.** The Comparator exited 0 (`Lean default kernel accepts the solution. Your solution is okay!`) after 1 hour 48 minutes 50 seconds (build about 70 minutes; the Comparator's single-threaded kernel check 39 minutes with no output). All 2,261 modules of the solution's closure were built from source inside the sandbox; the log carries `declaration uses sorry` only for the six challenge theorems, by design. `#print axioms`, run afterwards on each of the six theorems as an unprivileged user with no network (`localsmoothing_run/AxiomCheck.lean`, `logs/axioms_LocalSmoothing.log`), reports exactly `[propext, Classical.choice, Quot.sound]` for every one. Challenge and solution files were used unmodified (the challenge file's sha256 is `58dd1d878cd08f8d32850b1142e451a5efd4b0cdcf538ba80efbd01ea83cd9fd`).

**How this run differs from the setup of section 3.**

- **Mathlib came from the public cache, not a source build.** `lake update` ran Mathlib's post-update hook, which fetched 8,908 prebuilt artifact files from `cache.mathlib.org` (the host was reachable this time; the run of section 3 recorded it as unreachable). Mathlib and its dependencies, at the repository's pin `d13f23b723b8`, were therefore not rebuilt on this host. The Comparator README allows the cache if it is trusted. The challenge file's statements are written in Mathlib's vocabulary, so a tampered cache would alter challenge and solution alike and the Comparator would not see it; this run carries that assumption. Everything under `OAI.` was built from source.
- **Regenerable build files were deleted during the run.** About 40 minutes in, free disk fell from 9.9 GB to 4.1 GB: each built module leaves a `*.setup.json` of about 5.6 MB (1,373 files, 7.1 GB at that point), listing its full import list. A background script (`localsmoothing_run/prune_ir.sh`, log `localsmoothing_run/prune_ir.log`) removed those of modules finished more than two minutes earlier until the run ended. Lake regenerates them on demand and the `.olean` files the Comparator reads were not touched; the run printed a normal build and acceptance. It is nonetheless a modification of the build environment during a verification run.
- **Same weaker settings as section 3:** `landrun` v0.1.17 (here installed at the pinned version, not `@latest`), partial Landlock sandbox, no `systemd-run`, unprivileged user and no network, the Lean default kernel only. Lean 4.34.1 (commit `5045d00`); Comparator `d03acab` and `lean4export` `076e8e5` with the same two toolchain edits. The project used a minimal `lakefile.lean` (`localsmoothing_run/lakefile.lean`) holding only the closure.
- **One extra check after the verdict:** the `#print axioms` run, which imports the built solution; it is outside the Comparator's protocol and was done only after it finished.

**The challenge file, verbatim.** This is the trusted reference of the run: the definitions and the six statements, with `sorry` in place of the proofs. Source: `lean/ComparatorChallenges/LocalSmoothing.lean` at commit `7ef5c0cc5ca4`, from the repository's Apache-2.0 licensed material, reproduced for audit.

```lean
import Mathlib

/-!
# Euclidean local smoothing and its consequences

Standalone Comparator reference: six independent targets, no definition holes.
Fourier transforms use angular frequency; all dimensions satisfy `2 ≤ n`.
-/

open MeasureTheory
open scoped RealInnerProductSpace ENNReal

noncomputable section

namespace OAI.Analysis.Fourier.LocalSmoothing.Comparator

abbrev Space (n : ℕ) := EuclideanSpace ℝ (Fin n)

def angularFourier {n : ℕ} (f : Space n → ℂ) (ξ : Space n) : ℂ :=
  ∫ x, Complex.exp (-Complex.I * ((inner ℝ x ξ : ℝ) : ℂ)) * f x

def angularInverse {n : ℕ} (g : Space n → ℂ) (x : Space n) : ℂ :=
  (((2 * Real.pi) ^ n)⁻¹ : ℝ) •
    ∫ ξ, Complex.exp (Complex.I * ((inner ℝ x ξ : ℝ) : ℂ)) * g ξ

def halfWaveIntegral {n : ℕ} (t : ℝ) (f : Space n → ℂ) : Space n → ℂ :=
  angularInverse (fun ξ ↦ Complex.exp (-Complex.I * (t * ‖ξ‖ : ℝ)) *
    angularFourier f ξ)

def besselPotential {n : ℕ} (s : ℝ) (f : Space n → ℂ) : Space n → ℂ :=
  angularInverse (fun ξ ↦ ((1 + ‖ξ‖ ^ 2) ^ (s / 2) : ℝ) • angularFourier f ξ)

def observationMeasure (n : ℕ) : Measure (Space n × ℝ) :=
  volume.prod (volume.restrict (Set.Icc 1 2))

namespace Implications

/-- Surface measure on the unit sphere, viewed as a measure on ambient space. -/
def sphereMeasure (n : ℕ) : Measure (Space n) :=
  (volume : Measure (Space n)).toSphere.map Subtype.val

def sphericalExtension {n : ℕ} (g : Space n → ℂ) (x : Space n) : ℂ :=
  ∫ ω, Complex.exp (Complex.I * ((inner ℝ x ω : ℝ) : ℂ)) * g ω ∂sphereMeasure n

def conjugateExponent (a : ℝ≥0∞) : ℝ :=
  if a = ∞ then 1 else a.toReal / (a.toReal - 1)

def bochnerRieszSymbol {n : ℕ} (δ R : ℝ) (ξ : Space n) : ℝ :=
  (max (1 - (‖ξ‖ / R) ^ 2) 0) ^ δ

def bochnerRiesz {n : ℕ} (δ R : ℝ) (f : Space n → ℂ) : Space n → ℂ :=
  angularInverse (fun ξ ↦ bochnerRieszSymbol δ R ξ • angularFourier f ξ)

def unitSegment {n : ℕ} (ω x : Space n) : Set (Space n) :=
  {y | ∃ t ∈ Set.Icc (- (1 / 2 : ℝ)) (1 / 2), y = x + t • ω}

/-- Open radius-`δ` neighbourhood of the unit segment in direction `ω`. -/
def tube {n : ℕ} (δ : ℝ) (ω x : Space n) : Set (Space n) :=
  ⋃ t ∈ Set.Icc (- (1 / 2 : ℝ)) (1 / 2), Metric.ball (x + t • ω) δ

def kakeyaMaximal {n : ℕ} (δ : ℝ) (f : Space n → ℂ) (ω : Space n) : ℝ≥0∞ :=
  ⨆ x : Space n,
    (∫⁻ y in tube δ ω x, ‖f y‖ₑ) / volume (tube δ ω x)

def IsKakeyaSet {n : ℕ} (F : Set (Space n)) : Prop :=
  ∀ ω : Space n, ‖ω‖ = 1 → ∃ x, unitSegment ω x ⊆ F

end Implications

namespace Stein

/-- The square function with the actual radius derivative `r ∂ᵣ Bᵅᵣ f`. -/
def literalSteinSquareFunction {n : ℕ} (α : ℝ) (f : Space n → ℂ)
    (x : Space n) : ℝ≥0∞ :=
  (∫⁻ r in Set.Ioi (0 : ℝ),
    ‖r • deriv (fun s => Implications.bochnerRiesz α s f x) r‖ₑ ^ 2 /
      ENNReal.ofReal r) ^ (1 / 2 : ℝ)

end Stein

open OAI.Analysis.Fourier.LocalSmoothing.Comparator.Implications

/-- Local smoothing for every finite `p ≥ 2`, including zero loss at `p = 2`. -/
theorem euclidean_local_smoothing :
    ∀ n : ℕ, 2 ≤ n → ∀ p ε : ℝ, 2 ≤ p → (0 < ε ∨ (p = 2 ∧ ε = 0)) →
      ∃ C : ℝ, 0 < C ∧ ∀ f : SchwartzMap (Space n) ℂ,
        MemLp (besselPotential (max 0 (((n : ℝ) - 1) / 2 - n / p) + ε) f)
          (ENNReal.ofReal p) ∧
        MemLp (fun z : Space n × ℝ ↦ halfWaveIntegral z.2 f z.1)
          (ENNReal.ofReal p) (observationMeasure n) ∧
        eLpNorm (fun z : Space n × ℝ ↦ halfWaveIntegral z.2 f z.1)
          (ENNReal.ofReal p) (observationMeasure n) ≤
        ENNReal.ofReal C *
          eLpNorm (besselPotential (max 0 (((n : ℝ) - 1) / 2 - n / p) + ε) f)
            (ENNReal.ofReal p) volume := by
  sorry

/-- Uniform Bochner–Riesz bounds in the full strict range, including `p = ∞`. -/
theorem bochner_riesz :
    ∀ n : ℕ, 2 ≤ n → ∀ p : ℝ≥0∞, 1 ≤ p → ∀ δ : ℝ,
      max ((n : ℝ) * |(p⁻¹).toReal - 1 / 2| - 1 / 2) 0 < δ →
      ∃ C : ℝ, 0 < C ∧ ∀ R : ℝ, 0 < R → ∀ f : SchwartzMap (Space n) ℂ,
        MemLp (bochnerRiesz δ R f) p ∧
        eLpNorm (bochnerRiesz δ R f) p volume ≤
          ENNReal.ofReal C * eLpNorm f p volume := by
  sorry

/-- Spherical restriction in extension form, throughout the strict mixed range. -/
theorem spherical_restriction :
    ∀ n : ℕ, 2 ≤ n → ∀ a : ℝ≥0∞, 1 < a → ∀ b : ℝ,
      2 * (n : ℝ) / (n - 1) < b →
      ((n : ℝ) + 1) / ((n : ℝ) - 1) * conjugateExponent a < b →
      ∃ C : ℝ, 0 < C ∧ ∀ g : Space n → ℂ, MemLp g a (sphereMeasure n) →
        MemLp (sphericalExtension g) (ENNReal.ofReal b) ∧
        eLpNorm (sphericalExtension g) (ENNReal.ofReal b) volume ≤
          ENNReal.ofReal C * eLpNorm g a (sphereMeasure n) := by
  sorry

/-- Kakeya maximal bounds with every positive epsilon loss, uniformly in scale. -/
theorem kakeya_maximal :
    ∀ n : ℕ, 2 ≤ n → ∀ ε : ℝ, 0 < ε → ∃ C : ℝ, 0 < C ∧
      ∀ δ : ℝ, 0 < δ → δ ≤ 1 → ∀ f : Space n → ℂ, MemLp f n →
        MemLp (kakeyaMaximal δ f) n (sphereMeasure n) ∧
        eLpNorm (kakeyaMaximal δ f) n (sphereMeasure n) ≤
          ENNReal.ofReal (C * δ ^ (-ε)) * eLpNorm f n volume := by
  sorry

/-- Every Kakeya set has full Hausdorff dimension; no measurability is assumed. -/
theorem kakeya :
    ∀ n : ℕ, 2 ≤ n → ∀ F : Set (Space n), IsKakeyaSet F → dimH F = n := by
  sorry

/-- Stein's square-function estimate throughout the conjectured strict range. -/
theorem stein_square :
    ∀ n : ℕ, 2 ≤ n → ∀ p α : ℝ, 2 ≤ p →
      max (1 / 2) ((n : ℝ) * (1 / 2 - 1 / p)) < α →
      ∃ C : ℝ, 0 < C ∧ ∀ f : SchwartzMap (Space n) ℂ,
        MemLp (Stein.literalSteinSquareFunction α f) (ENNReal.ofReal p) volume ∧
        eLpNorm (Stein.literalSteinSquareFunction α f) (ENNReal.ofReal p) volume ≤
          ENNReal.ofReal C * eLpNorm f (ENNReal.ofReal p) volume := by
  sorry

end OAI.Analysis.Fourier.LocalSmoothing.Comparator
```

**Readings of the definitions and statements (one reader, same model family as the draft; not a mathematician's review).** Conventions are checked against the paper's Theorem 1.1 and its listed consequences, and against the statement of the local smoothing conjecture in Beltran, Hickman and Sogge (arXiv:1812.11616, Conjecture 2.4), whose sign convention was garbled in text extraction; the threshold was derived from its prose ("a gain relative to the fixed-time estimates").

| Object | Lean definition | Reading |
|---|---|---|
| Fourier transform and inverse | `angularFourier f ξ = ∫ exp(-i⟨x,ξ⟩) f(x) dx`; `angularInverse g x = (2π)^(-n) ∫ exp(i⟨x,ξ⟩) g(ξ) dξ` | angular-frequency convention, matching the paper's `f̂(ξ) = ∫ e^{-iX·ξ} f(X) dX` with inverse factor `(2π)^-n` |
| Half-wave propagator | `halfWaveIntegral t f` = inverse of `exp(-i t ‖ξ‖)` times the transform | `U(T) = e^{-iT\|D\|}` |
| Bessel potential | `besselPotential s f` = inverse of `(1+‖ξ‖²)^(s/2)` times the transform | `J^s = (1-Δ)^{s/2}` |
| Space-time measure | Lebesgue measure on `ℝⁿ` times Lebesgue measure restricted to `[1,2]` | `L^p(ℝⁿ × I)` with `I = [1,2]` |
| Bochner–Riesz means | `bochnerRiesz δ R f` = inverse of `max(1-(‖ξ‖/R)²,0)^δ` times the transform | `(1-\|ξ\|²/R²)_+^δ` |
| Sphere measure and extension | surface measure on the unit sphere from Mathlib's `toSphere`; `sphericalExtension g x = ∫ e^{i⟨x,ω⟩} g(ω) dσ(ω)` | normalization differs from the unit measure by a constant, which does not affect boundedness |
| Kakeya objects | `tube δ ω x` = union of radius-`δ` balls along a unit segment; `kakeyaMaximal` = supremum over centers of the average of `\|f\|` over the tube; `IsKakeyaSet F` = for each unit direction a unit segment inside `F` | standard |
| Stein square function | `(∫₀^∞ \|r ∂ᵣ B^α_r f(x)\|² dr/r)^{1/2}` with `deriv` | equals `(∫ \|∂ᵣ B^α_r f\|² r dr)^{1/2}`; Lean's `deriv` returns 0 where the radial derivative does not exist, which should not arise for these `α` but is a property a specialist should confirm |

| Statement | Reading |
|---|---|
| `euclidean_local_smoothing` | for `n ≥ 2`, real `p ≥ 2`, `ε > 0` (or `p = 2` and `ε = 0`): a constant `C > 0` such that for every complex Schwartz `f`, the half-wave is in `L^p(ℝⁿ × [1,2])` with norm at most `C` times the `L^p` norm of `J^{s₊(p)+ε} f`, `s₊(p) = max(0,(n-1)/2 - n/p)`. This is the paper's Theorem 1.1, and the sharp threshold of Conjecture 2.4 in 1812.11616 (fixed-time order `(n-1)(1/2-1/p)` minus the gain `1/p` for `p ≥ 2n/(n-1)`, and `0` below). |
| `bochner_riesz` | `1 ≤ p ≤ ∞` and `δ > max(n\|1/p-1/2\| - 1/2, 0)`: bounds uniform in the radius, for Schwartz data. The conjectured range. |
| `spherical_restriction` | extension `L^a(S^{n-1}) → L^b(ℝⁿ)` for `a > 1` and both `b > 2n/(n-1)` and `b > ((n+1)/(n-1)) a'`. Strict inequalities: the interior of the conjectured range, not its boundary. |
| `kakeya_maximal` | `‖K_δ f‖_{L^n(S^{n-1})} ≤ C δ^{-ε} ‖f‖_{L^n(ℝⁿ)}` for every `ε > 0` and `0 < δ ≤ 1`. |
| `kakeya` | every set containing a unit segment in each direction has Hausdorff dimension `n`, no measurability assumed. |
| `stein_square` | `G^α` is bounded on `L^p` for `p ≥ 2` and `α > max(1/2, n(1/2-1/p))`, for Schwartz data; this equals the paper's `α > 1/2 + s₊(p)`. |

What the readings find is a match between the Lean statements and the paper's stated theorems, with the restriction result limited to the strict range. The release's announcement of 26 October says the results "resolve the Kakeya conjecture and Stein's restriction conjecture in all dimensions"; the paper's abstract, the repository's `history.md` entry and the Lean statement all say restriction holds "throughout the interior of the conjectured range", so the Lean verdict covers the weaker form. Several items in the paper's abstract have no Lean statement in this config or in its scope note: maximal Bochner–Riesz estimates, the Nikodym maximal estimate, compact paraboloid and truncated cone restriction, and local smoothing for the Schrödinger equation.

**What this run establishes and does not.** Established, given the stated trust assumptions: Lean's kernel has checked proofs of exactly these six statements, with the three standard axioms. Not established: that the paper's own argument is correct (sections 2 to 7 and the appendices were not read); that the definitions above are the intended mathematical objects beyond one reader's check; anything about the items without a Lean statement; and it is not independent of the model family that drafted this paper. The run supports route 1 of section 1 (the proof is accepted by the kernel with only standard axioms) for this config and leaves route 2 (the statement is the claim) to a specialist; the readings above are an aid, not a substitute.

## 6. What a pass does and does not establish

**Established, for each accepted config.** A kernel-checked derivation of the Lean statement, from the three standard axioms, with the statement the challenge file exports. A model, a human or a script could have written it; the verdict does not depend on which. The controls show the harness rejects both a changed statement and a `sorry`.

**Not established.**

- *Fidelity beyond my reading.* The challenge files, and every definition in them, come from the same repository as the solutions. The Comparator's trust model assumes the challenge is written by the verifier; here the verifier has to read it. The statements above are short and their readings are stated, but one reader of the same model family is not an independent mathematical review. Statements with many from-scratch definitions (`FiniteCongruenceGraph`, `GrahamSpherical`) carry more of this risk than Seymour's.
- *Kernel and sandbox.* One kernel, one sandbox configuration weaker than documented.
- *Anything about the other configs and the other manuscripts.* The configs run were chosen for build feasibility; most of the 405 configs, and most manuscripts, were not run. The "22% formalized" figure carries no information about the unformalized claims, which include the largest ones.
- *Reasoning versus harness-fitting as a process.* A passing config shows the output is correct, which excludes the hypothesis that the checked artifact is a harness exploit. It does not show how it was found, and the model's reasoning summaries were not read.

**Where "harnessmaxxing" could still live.** In the unformalized majority, in statement fidelity for the formalized ones, and in selection: a release in which the machine-checked part is the part that is easy to check will show a clean pass rate on exactly the subset where a clean pass rate is cheap. None of these is excluded by this audit.

### 6.1 A popular reading, checked against the census (added 2026-10-17)

A commentary published on 16 October 2026 argues that the release shows a "91% failure rate": per its text, 372 successes out of roughly 4,000 attempts, produced by brute-forcing proofs "until the code compiles in a proof assistant like Lean". Two parts of that reading can be set against this audit's counts; the rest cannot be checked here.

*The ratio.* The 4,000 attempts is the commentary's figure, and it cites no source; the census in section 2 records 722 manuscripts in 372 result families and no attempt count, so the denominator is not something this audit can confirm. A ratio of successes to attempts is a hit rate on a list of open problems, not an error rate, and "unsolved" is not "wrong". The quantity that bears on quality is the error rate among results the release claims, which this audit does not measure. The commentary reports that three manuscripts were withdrawn after a sign error; that is unverified here and, if it means three of 722, is under half of one percent of the manuscripts.

*The mechanism.* "Compiles in Lean" can describe only the formalized subset: 162 of 722 manuscripts (22%) and 127 of 372 families (34%), per section 2. For the rest the catalogue's own review field reads `unchecked`, and that is where the risk described in section 6 sits. For the formalized subset, the 11 accepted configs and the two rejected controls (sections 4 and 5) show a derivation checked by the kernel, whatever search produced it. Whether that search deserves to be called reasoning is not tested here (section 6), and the commentary gives no operational test either: "cannot invent a new concept" and "fails 100% of the time" on problems needing a novel framework have no stated way to be wrong. The release includes explicit counterexamples to long-standing conjectures (for example `AbhyankarSathaye` and `ProjectionCounterexample`, section 5); this audit does not claim they show originality, only that an account of the release as interpolation has to say what they are.

*What the audit supports.* The commentary's institutional point, that the difficulty is volume and verification rather than a demonstration of machine intellect, is consistent with route 4: most of the release is unchecked, and the checked part is the part that is cheap to check. Its claims about training data, about named researchers, and about the labour market are outside this audit and are not repeated.

## 7. Limitations

11 accepted configs out of 405, none rejected, so the harness's discriminating power rests on the two controls alone; configs chosen for build feasibility; one reader; a weaker sandbox; a single kernel; the Lean proofs themselves were not read beyond the top-level structure of one of them; the manuscripts were not read; the controls were run on one config; nothing here is independent of the model family that drafted the paper.

## 8. Reproduction

The companion folder `openai_math_comparator_audit_v1/` holds `PINS.txt`, `setup.sh` (the steps used), `run_cmp.sh`, `census.py`, `make_table.py`, `build_paper.py`, the controls (`controls/`), every Comparator log (`logs/`), and for the later run of section 5.1 its project file, closure list, axiom check and pruning script and log (`localsmoothing_run/`). Counts in section 2 come from `python3 -I census.py <clone>`; the results table from `make_table.py` over the logs. Builds need several GB of disk and tens of minutes per config the first time (Mathlib compiles incrementally across configs).

## References

Sources: the repository itself (https://github.com/openai/math, commit adc7f1241); the Lean Comparator (https://github.com/leanprover/comparator) and its README for the trust model; `lean4export` (https://github.com/leanprover/lean4export); Lean 4 (https://github.com/leanprover/lean4); Mathlib (https://github.com/leanprover-community/mathlib4); `landrun` (https://github.com/Zouuup/landrun). Related in this repository: [`model_local_proofs_travel_v1.md`](model_local_proofs_travel_v1.md) (a check that passes inside one harness does not carry to a different one).

## Revision log

- *2026-10-17.* Added section 6.1 (a popular reading checked against the census). No result, count or verdict above it changed.
- *2026-10-07, v1.* Eleven short-statement configs run and accepted; two negative controls rejected; static census of the release at commit `adc7f1241`. Statement readings by one same-family reader.
- *2026-10-27, v1.1.* Section 5.1 added: one config of the 26 October update (`LocalSmoothing`, 2,261 solution modules) run against the repository head `7ef5c0cc5ca4`, accepted, axioms checked separately, challenge file and definitions reproduced and read. Differences from the earlier setup: Mathlib from the public prebuilt cache instead of a source build, regenerable per-module setup files deleted during the run for disk space. The eleven-config results above are unchanged.
- *Open for the next revision.* A full Mathlib build (multi-hour, several GB) to reach the 377 configs whose challenge files `import Mathlib`; an independent mathematician's read of the Lean statements, starting with the ones that define their objects from scratch (`FiniteCongruenceGraph`, `GrahamSpherical`); a run with a second kernel; a sandbox at the documented strength; for the 27 October run, a source rebuild of Mathlib in place of the cache. New results are added here with their date; a changed verdict is a correction, not an edit in place.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
