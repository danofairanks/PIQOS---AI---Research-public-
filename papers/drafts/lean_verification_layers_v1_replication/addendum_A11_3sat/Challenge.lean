import SatLowerBound.SparseRestriction
import Mathlib.Analysis.SpecialFunctions.Log.Base

namespace Indep

/-- A gate: an arbitrary Boolean function of two earlier signals (indices into the signal list). -/
structure Gate where
  op : Bool → Bool → Bool
  l : Nat
  r : Nat

/-- Signals start as the input bits; each gate appends one signal. Reads out of range give false. -/
def evalFrom : List Bool → List Gate → Nat → Bool
  | sigs, [], out => sigs.getD out false
  | sigs, g :: rest, out => evalFrom (sigs ++ [g.op (sigs.getD g.l false) (sigs.getD g.r false)]) rest out

/-- Well-formed: every index refers to a signal that already exists. -/
def WF : Nat → List Gate → Nat → Prop
  | n, [], out => out < n
  | n, g :: rest, out => g.l < n ∧ g.r < n ∧ WF (n + 1) rest out

/-- A circuit: input count, gates, output index. -/
structure Circ (n : Nat) where
  gates : List Gate
  out : Nat

def Circ.size {n : Nat} (C : Circ n) : Nat := C.gates.length
def Circ.eval {n : Nat} (C : Circ n) (x : Fin n → Bool) : Bool :=
  evalFrom (List.ofFn x) C.gates C.out
@[reducible] def Circ.WF {n : Nat} (C : Circ n) : Prop := Indep.WF n C.gates C.out
def Circ.Computes {n : Nat} (C : Circ n) (f : (Fin n → Bool) → Bool) : Prop :=
  ∀ x, C.eval x = f x

/-- T-a -/
theorem finite_ceiling_indep (w r k : Nat)
    (hw : 2 ≤ w) (hrw : r < w) (hr : 4 ≤ r) (hk : 3 ≤ k) (hkr : k + 2 ≤ r)
    (hlog : (2 : ℝ) ^ (k - 2) >
      Real.logb 2 (6 * (r : ℝ) * ((r : ℝ) - 1)) + (r : ℝ) * Real.logb 2 3)
    (C : Circ (SatLowerBound.inputBits w)) (hwf : C.WF)
    (hc : C.Computes (SatLowerBound.satFunction w)) :
    (SatLowerBound.inputBits w : ℤ) +
      ⌈((30 * (r : ℝ) - 42 * ((k : ℝ) + 1)) *
        ((SatLowerBound.variableCount w : ℝ) - (2 : ℝ) ^ r) - 3) / 7⌉ ≤ (C.size : ℤ) := sorry

/-- T-b -/
theorem exact_certificate_indep :
    ∀ (w r : Nat), 8 ≤ w → 3 ≤ r → r < w →
      ∀ C : Circ (SatLowerBound.inputBits w), C.WF →
        C.Computes (SatLowerBound.satFunction w) →
          SatLowerBound.inputBits w + (4 * r - 7) * SatLowerBound.remainingClauses w r ≤ C.size + 1 := sorry

end Indep
