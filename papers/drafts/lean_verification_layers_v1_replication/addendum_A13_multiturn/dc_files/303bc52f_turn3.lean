
import Mathlib

theorem real_binomial_expansion (a b : ℝ) :
    (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  exact add_sq a b
