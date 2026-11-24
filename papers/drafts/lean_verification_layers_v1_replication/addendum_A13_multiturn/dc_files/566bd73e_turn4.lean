
import Mathlib

theorem zero_mul_of_eq_zero :
    ∀ (a b : ℝ), a = 0 → a * b = 0 := by
  intro a b h
  rw [h]
  exact zero_mul b
