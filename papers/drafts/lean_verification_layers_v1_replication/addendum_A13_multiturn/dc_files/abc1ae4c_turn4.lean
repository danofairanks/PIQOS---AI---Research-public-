
import Mathlib

theorem original_statement_is_false :
    ∃ f : ℝ → ℝ, ¬ (∀ x : ℝ, f x ≤ x ^ 2 + 1) := by
  refine ⟨fun x => x ^ 2 + 2, ?_⟩
  intro h
  have h0 := h 0
  norm_num at h0
