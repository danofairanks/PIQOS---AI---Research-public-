
import Mathlib

theorem division_self_eq_one
    (x : ℝ) (h : x ≠ 0) :
    x / x = 1 := by
  exact div_self h
