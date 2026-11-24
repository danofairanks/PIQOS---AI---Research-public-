
import Mathlib

theorem original_statement (a b : ℕ) :
    a - b + b = a := by
  sorry

theorem original_statement_is_false :
    ¬ (∀ a b : ℕ, a - b + b = a) := by
  intro h
  have h₂ := h 2 3
  norm_num at h₂
