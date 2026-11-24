import Mathlib

theorem div_self_real_false :
    ¬ (∀ x : ℝ, x / x = 1) := by
  intro h
  have h0 := h 0
  norm_num at h0
