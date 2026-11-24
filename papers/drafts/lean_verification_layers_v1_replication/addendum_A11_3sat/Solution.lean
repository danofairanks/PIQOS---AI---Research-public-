import Credit.TwoLevel.ManuscriptTheorem
import SatLowerBound.Main
import SatLowerBound.SparseRestriction
import Mathlib.Analysis.SpecialFunctions.Log.Base

/-! Independent circuit model (written from the paper's Definitions 2.5-2.7) and a bridge to
the package's `SatLowerBound.Circuit`.  Inherited, NOT independent: `inputBits`,
`variableCount`, `remainingClauses`, `satFunction` (the package's own). -/

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

/-- Translation to the package's circuit type. -/
def tr : (gs : List Gate) → (n : Nat) → (out : Nat) → WF n gs out → SatLowerBound.Circuit n
  | [], _, out, h => .output ⟨out, h⟩
  | g :: rest, n, out, h =>
      .gate (SatLowerBound.Table.ofFunction g.op) ⟨g.l, h.1⟩ ⟨g.r, h.2.1⟩ (tr rest (n + 1) out h.2.2)

theorem tr_size : ∀ (gs : List Gate) (n out : Nat) (h : WF n gs out), (tr gs n out h).size = gs.length
  | [], _, _, _ => rfl
  | g :: rest, n, out, h => by
      simp only [tr, SatLowerBound.Circuit.size, List.length_cons, tr_size rest (n + 1) out h.2.2]

theorem ofFn_extend {n : Nat} (x : Fin n → Bool) (b : Bool) :
    List.ofFn (SatLowerBound.extend x b) = List.ofFn x ++ [b] := by
  rw [List.ofFn_succ']
  simp [SatLowerBound.extend_old, SatLowerBound.extend_last, List.concat_eq_append]

theorem tr_eval : ∀ (gs : List Gate) (n out : Nat) (h : WF n gs out) (x : Fin n → Bool),
    (tr gs n out h).eval x = evalFrom (List.ofFn x) gs out
  | [], n, out, h, x => by
      have h' : out < n := h
      simp [tr, SatLowerBound.Circuit.eval, evalFrom, List.getD_eq_getElem?_getD, h']
  | g :: rest, n, out, h, x => by
      have hl : (List.ofFn x).getD g.l false = x ⟨g.l, h.1⟩ := by
        simp [List.getD_eq_getElem?_getD, h.1]
      have hr : (List.ofFn x).getD g.r false = x ⟨g.r, h.2.1⟩ := by
        simp [List.getD_eq_getElem?_getD, h.2.1]
      simp only [tr, SatLowerBound.Circuit.eval, evalFrom]
      rw [tr_eval rest (n + 1) out h.2.2, ofFn_extend, hl, hr, SatLowerBound.Table.eval_ofFunction]

theorem tr_computes {n : Nat} (C : Circ n) (hwf : C.WF) (f : (Fin n → Bool) → Bool)
    (hc : C.Computes f) : (tr C.gates n C.out hwf).Computes f := by
  intro x
  have := tr_eval C.gates n C.out hwf x
  rw [this]
  exact hc x

/-- T-a: equation (5) form, over the independent circuit model. -/
theorem finite_ceiling_indep (w r k : Nat)
    (hw : 2 ≤ w) (hrw : r < w) (hr : 4 ≤ r) (hk : 3 ≤ k) (hkr : k + 2 ≤ r)
    (hlog : (2 : ℝ) ^ (k - 2) >
      Real.logb 2 (6 * (r : ℝ) * ((r : ℝ) - 1)) + (r : ℝ) * Real.logb 2 3)
    (C : Circ (SatLowerBound.inputBits w)) (hwf : C.WF)
    (hc : C.Computes (SatLowerBound.satFunction w)) :
    (SatLowerBound.inputBits w : ℤ) +
      ⌈((30 * (r : ℝ) - 42 * ((k : ℝ) + 1)) *
        ((SatLowerBound.variableCount w : ℝ) - (2 : ℝ) ^ r) - 3) / 7⌉ ≤ (C.size : ℤ) := by
  have h := SatLowerBound.paper_finite_ceiling_bound w r k hw hrw hr hk hkr hlog
    (tr C.gates _ C.out hwf) (tr_computes C hwf _ hc)
  have hs := tr_size C.gates (SatLowerBound.inputBits w) C.out hwf
  simpa [Circ.size, hs] using h

/-- T-b: the 7/3 certificate, over the independent circuit model. -/
theorem exact_certificate_indep :
    ∀ (w r : Nat), 8 ≤ w → 3 ≤ r → r < w →
      ∀ C : Circ (SatLowerBound.inputBits w), C.WF →
        C.Computes (SatLowerBound.satFunction w) →
          SatLowerBound.inputBits w + (4 * r - 7) * SatLowerBound.remainingClauses w r ≤ C.size + 1 := by
  intro w r hw hr hrw C hwf hc
  have h := SatLowerBound.main_lower_bound w r hw hr hrw
    (tr C.gates _ C.out hwf) (tr_computes C hwf _ hc)
  have hs := tr_size C.gates (SatLowerBound.inputBits w) C.out hwf
  simpa [Circ.size, hs] using h

end Indep

