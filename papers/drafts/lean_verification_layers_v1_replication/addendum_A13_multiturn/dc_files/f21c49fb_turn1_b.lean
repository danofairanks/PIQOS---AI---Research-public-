
import Mathlib

def counterexampleFunction : ℝ → ℝ :=
  fun x => x ^ 2 + 2

theorem counterexample_fails :
    ¬ (∀ x : ℝ,
        counterexampleFunction x ≤ x ^ 2 + 1) := by
  intro h
  have h0 := h 0
  norm_num [counterexampleFunction] at h0
