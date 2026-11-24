
import Mathlib

-- The exact original statement, unchanged.
def original_statement : Prop :=
  ∀ x : ℝ, x / x = 1

-- Certified proof that the original statement is false.
theorem original_statement_is_false :
    ¬ original_statement := by
  intro h
  have h0 : (0 : ℝ) / 0 = 1 := h 0
  norm_num at h0
