
import Mathlib

theorem natural_sub_add_is_false :
    ¬ (∀ a b : ℕ, a - b + b = a) := by
  intro h
  have h₂ := h 2 3
  norm_num at h₂
