
import Mathlib

theorem real_binomial_expansion (a b : ℝ) :
    (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  calc
    (a + b) ^ 2 = (a + b) * (a + b) := by
      rw [pow_two]
    _ = a * a + a * b + b * a + b * b := by
      ring
    _ = a ^ 2 + 2 * a * b + b ^ 2 := by
      ring
