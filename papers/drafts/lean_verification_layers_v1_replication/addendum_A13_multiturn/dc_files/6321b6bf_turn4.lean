
import Mathlib

theorem zero_mul_real (a b : ℝ) (h : a = 0) : a * b = 0 := by
  rw [h]
  exact zero_mul b
