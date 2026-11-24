
import Mathlib

theorem counterexample_to_original :
    ¬ (∀ x : ℝ, x / x = 1) := by
  intro h
  have h0 : (0 : ℝ) / 0 = 1 := h 0
  norm_num at h0
