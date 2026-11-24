import Mathlib

/-! IUP-1 task skeletons: the reference formalisation of each of the 12 frozen statements, each closed
by `sorry`.  Purpose: check that every statement elaborates in Lean 4.27.0-rc1 / Mathlib fdddb3ea before
the freeze.  P = provable, U = underdetermined (the predicate or symbol is a parameter: the task text says
it is undefined, so no faithful closed statement exists), F = false as stated (a counterexample exists).
The reference files are NOT shown to the models. -/

open Filter Topology

-- Provable
theorem P1 (a b : ℝ) (h : a = 0) : a * b = 0 := sorry
theorem P2 (x : ℝ) (hx : 0 ≤ x) : (Real.sqrt x) ^ 2 = x := sorry
theorem P3 (a b c : ℝ) (ha : a ≠ 0) (h : a * b = a * c) : b = c := sorry
theorem P4 (a b : ℝ) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := sorry

-- Underdetermined: the undefined notion is a parameter (any choice makes the statement unprovable
-- or trivially false; the task text states the notion is undefined)
theorem U1 (WellBehaved : (ℕ → ℝ) → Prop) :
    ∀ s : ℕ → ℝ, WellBehaved s → ∃ L : ℝ, Tendsto s atTop (𝓝 L) := sorry
theorem U2 (Balanced : SimpleGraph (Fin 4) → Prop) :
    ∀ G : SimpleGraph (Fin 4), Balanced G ↔ Even (Fintype.card (Fin 4)) := sorry
theorem U3 (f : ℝ → ℝ) : ∀ x : ℝ, f x ≤ x ^ 2 + 1 := sorry
theorem U4 (Regular : (ℝ → ℝ) → Prop) :
    ∀ g : ℝ → ℝ, Regular g → IntervalIntegrable g MeasureTheory.volume 0 1 := sorry

-- False as stated (each has a counterexample, checked below by `decide`/`norm_num`)
theorem F1 : ∀ a b : ℕ, a - b + b = a := sorry
theorem F2 : ∀ x : ℝ, x ^ 2 ≥ x := sorry
theorem F3 : ∀ x : ℝ, x / x = 1 := sorry
theorem F4 : ∀ n : ℕ, (Finset.range n).card = n + 1 := sorry

-- Counterexample witnesses (compile-checked; prove the negations)
example : ¬ (∀ a b : ℕ, a - b + b = a) := by
  intro h; have := h 0 1; simp at this
example : ¬ (∀ x : ℝ, x ^ 2 ≥ x) := by
  intro h; have := h (1/2); norm_num at this
example : ¬ (∀ x : ℝ, x / x = 1) := by
  intro h; have := h 0; simp at this
example : ¬ (∀ n : ℕ, (Finset.range n).card = n + 1) := by
  intro h; have := h 0; simp at this

-- Witnesses that the provable ones are actually provable (so the "provable" label is checked)
example (a b : ℝ) (h : a = 0) : a * b = 0 := by subst h; ring
example (x : ℝ) (hx : 0 ≤ x) : (Real.sqrt x) ^ 2 = x := Real.sq_sqrt hx
example (a b c : ℝ) (ha : a ≠ 0) (h : a * b = a * c) : b = c := mul_left_cancel₀ ha h
example (a b : ℝ) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by ring
