import Mathlib

theorem div_self_real : ∀ x : ℝ, x / x = 1 := by
  intro x
  by_cases h : x = 0
  · subst x
    norm_num
  · exact div_self h
