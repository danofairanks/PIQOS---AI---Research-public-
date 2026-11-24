import Mathlib

theorem div_self_real : ∀ x : ℝ, x / x = 1 := by
  intro x
  norm_num
