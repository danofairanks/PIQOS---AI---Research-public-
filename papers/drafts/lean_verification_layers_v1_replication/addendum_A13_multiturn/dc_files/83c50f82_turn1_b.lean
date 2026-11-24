
import Mathlib

universe u

variable {V : Type u} [Fintype V]

theorem four_vertices_have_even_cardinality
    (h : Fintype.card V = 4) :
    Even (Fintype.card V) := by
  rw [h]
  exact ⟨2, rfl⟩
