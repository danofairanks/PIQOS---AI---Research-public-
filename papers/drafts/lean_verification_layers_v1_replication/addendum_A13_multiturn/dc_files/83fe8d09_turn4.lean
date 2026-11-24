import Mathlib

def f : ℝ → ℝ := fun x => x ^ 2 + 2

theorem statement :
    ∀ x : ℝ, f x ≤ x ^ 2 + 1 := by
  intro x
  dsimp [f]
  norm_num
