
import Mathlib

variable (f : ℝ → ℝ)

def ProposedStatement : Prop :=
  ∀ x : ℝ, f x ≤ x ^ 2 + 1
