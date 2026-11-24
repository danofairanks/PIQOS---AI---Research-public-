
import Mathlib

theorem zero_mul_of_zero_left (a b : ℝ) (h : a = 0) :
    a * b = 0 := by
  rw [h]
  ring
