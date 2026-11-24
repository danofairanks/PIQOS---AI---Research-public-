
import Mathlib

theorem zero_mul_of_eq_zero (a b : ℝ) (h : a = 0) : a * b = 0 := by
  rw [h]
  ring
