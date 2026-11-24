import Mathlib

axiom f : ℝ → ℝ

axiom statement :
    ∀ x : ℝ, f x ≤ x ^ 2 + 1
