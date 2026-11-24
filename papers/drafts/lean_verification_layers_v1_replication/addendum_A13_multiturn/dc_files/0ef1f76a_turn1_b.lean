import Mathlib

theorem nat_sub_add_eq (a b : ℕ) (h : b ≤ a) :
    a - b + b = a := by
  omega
