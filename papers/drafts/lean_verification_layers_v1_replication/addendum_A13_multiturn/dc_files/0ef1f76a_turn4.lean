import Mathlib

theorem nat_sub_add_counterexample :
    ¬ (∀ a b : ℕ, a - b + b = a) := by
  intro h
  have hc := h 2 3
  norm_num at hc
