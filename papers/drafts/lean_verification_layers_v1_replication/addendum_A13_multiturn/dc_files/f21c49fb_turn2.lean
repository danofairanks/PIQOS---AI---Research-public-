
import Mathlib

-- The proposed statement for an unspecified real-valued function.
def ProposedStatement (f : ℝ → ℝ) : Prop :=
  ∀ x : ℝ, f x ≤ x ^ 2 + 1

-- A function for which the proposed statement is false.
def counterexampleFunction : ℝ → ℝ :=
  fun x => x ^ 2 + 2

-- The counterexample disproves the proposed statement.
theorem counterexample_fails :
    ¬ ProposedStatement counterexampleFunction := by
  intro h
  have h0 := h 0
  norm_num [ProposedStatement, counterexampleFunction] at h0
