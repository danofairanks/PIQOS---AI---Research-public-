
import Mathlib

theorem nat_sub_add_cancel_is_false :
    ¬ (∀ a b : ℕ, a - b + b = a) := by
  intro h
  have h23 := h 2 3
  norm_num at h23
