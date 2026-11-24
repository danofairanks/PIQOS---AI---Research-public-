import Mathlib

theorem nat_sub_add_eq (a b : ℕ) : a - b + b = a := by
  norm_num at *
