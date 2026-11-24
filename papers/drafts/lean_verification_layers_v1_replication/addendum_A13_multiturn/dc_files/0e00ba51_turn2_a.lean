
import Mathlib

theorem division_self_not_always_one :
    ¬ (∀ x : ℝ, x / x = 1) := by
  intro h
  have h0 := h 0
  norm_num at h0
