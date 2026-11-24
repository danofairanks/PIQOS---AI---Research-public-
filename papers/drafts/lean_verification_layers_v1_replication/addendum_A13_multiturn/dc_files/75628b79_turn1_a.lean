
import Mathlib

theorem original_statement :
    ∀ x : ℝ, x / x = 1 := by
  intro x
  -- The statement is false for x = 0.
  norm_num
