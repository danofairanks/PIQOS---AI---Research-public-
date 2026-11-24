
import Mathlib

universe u

variable {V : Type u} [Fintype V]

variable (Balanced : SimpleGraph V → Prop)

def FourVertexClaim : Prop :=
  ∀ G : SimpleGraph V,
    Fintype.card V = 4 →
      (Balanced G ↔ Even (Fintype.card V))
