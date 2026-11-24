
import Mathlib

def f : ℝ → ℝ := fun x => x ^ 2 + 2

theorem counterexample :
    ¬ (∀ x : ℝ, f x ≤ x ^ 2 + 1) := by
  intro h
  have h0 := h 0
  norm_num [f] at h0
