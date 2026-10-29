-- DECOY (negative control; see PREREG.md). Not part of the kit.
import Mathlib

/-! DECOY (negative control, see PREREG): trivially true statement. -/
namespace OAI.EthKit.Decoy

abbrev Lit (n : ℕ) := Fin n × Bool
abbrev Clause (n : ℕ) := Finset (Lit n)

def FormulaSat {n : ℕ} (F : Finset (Clause n)) (x : Fin n → Bool) : Prop :=
  ∀ C ∈ F, ∃ l ∈ C, x l.1 = l.2

open Classical in
noncomputable def satCount {n : ℕ} (F : Finset (Clause n)) : ℕ :=
  (Finset.univ.filter (fun x : Fin n → Bool => FormulaSat F x)).card

theorem decoy_refl {n : ℕ} (F : Finset (Clause n)) : satCount F = satCount F := by
  rfl

end OAI.EthKit.Decoy
