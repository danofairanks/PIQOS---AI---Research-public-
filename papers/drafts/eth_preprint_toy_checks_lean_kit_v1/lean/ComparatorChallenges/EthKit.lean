import Mathlib

open Finset Function

namespace OAI.EthKit.Comparator

/-! ## Problem specification: k-SAT counting -/

abbrev Lit (n : ℕ) := Fin n × Bool
abbrev Clause (n : ℕ) := Finset (Lit n)

/-- `x` satisfies the formula `F` (a conjunction of clauses; a clause is a disjunction of literals;
a literal `(i, b)` is true under `x` iff `x i = b`). -/
def FormulaSat {n : ℕ} (F : Finset (Clause n)) (x : Fin n → Bool) : Prop :=
  ∀ C ∈ F, ∃ l ∈ C, x l.1 = l.2

open Classical in
/-- The number of satisfying assignments. -/
noncomputable def satCount {n : ℕ} (F : Finset (Clause n)) : ℕ :=
  (Finset.univ.filter (fun x : Fin n → Bool => FormulaSat F x)).card

/-- Negation of a literal. -/
def negLit {n : ℕ} (l : Lit n) : Lit n := (l.1, !l.2)

/-! ## Appendix A, Lemma A.1: the two children of a branch partition the satisfying assignments -/

theorem branch_partition {n : ℕ} (G P : Finset (Clause n)) (H : Clause n) (x : Fin n → Bool) :
    FormulaSat (G ∪ P.image (fun p => H ∪ p)) x ↔
      (FormulaSat (G ∪ {H}) x ∧
          ¬ FormulaSat (G ∪ P ∪ H.image (fun l => ({negLit l} : Clause n))) x) ∨
      (¬ FormulaSat (G ∪ {H}) x ∧
          FormulaSat (G ∪ P ∪ H.image (fun l => ({negLit l} : Clause n))) x) := by
  sorry

/-! ## Section 3.4: Hermite uniqueness -/

theorem hermite_unique (Q J d : ℕ) (hQJ : d < Q * J) (nodes : Finset ℚ) (hn : nodes.card = Q)
    (P : Polynomial ℚ) (hdeg : P.natDegree ≤ d)
    (hroot : ∀ t ∈ nodes, (Polynomial.X - Polynomial.C t) ^ J ∣ P) : P = 0 := by
  sorry

/-! ## Lemma 5.2, degree control -/

theorem degree_control {σ : Type*} (m dstar : ℕ) (y : Fin m → MvPolynomial σ ℚ)
    (hy : ∀ i, (y i).totalDegree ≤ dstar) (a b : ℕ → ℚ) (j : Fin m → ℕ) :
    (∏ i, (MvPolynomial.C (a (j i)) + MvPolynomial.C (b (j i)) * y i) *
        (y i * y i - y i) ^ (j i)).totalDegree ≤ dstar * (m + 2 * ∑ i, j i) := by
  sorry

/-! ## Lemma 6.2: averaging and the (27/32)^n argument -/

theorem exists_le_average {ι : Type*} [Fintype ι] [Nonempty ι] (D : ι → ℕ) (c : ℚ)
    (h : (∑ γ, (D γ : ℚ)) ≤ c * Fintype.card ι) : ∃ γ, (D γ : ℚ) ≤ c := by
  sorry

theorem greedy_contracts (n : ℕ) (hn : 1 ≤ n) (D : ℕ → ℕ) (h0 : D 0 ≤ 2 ^ n)
    (hstep : ∀ t, 4 * D (t + 1) ≤ 3 * D t) : D (3 * n) = 0 := by
  sorry

/-! ## The induction shell of Theorem D.1 -/

theorem contract_correct {Net : Type*} (size : Net → ℕ) (H : ℕ) (R : ℕ → Type*)
    (Z alg : (N : Net) → (p : ℕ) → R p)
    (leaf : ∀ N p, size N ≤ H → alg N p = Z N p)
    (step : ∀ N p, H < size N →
      ∃ (ι : Type) (_ : Fintype ι) (K : ι → Net) (q : ι → ℕ) (comb : ((i : ι) → R (q i)) → R p),
        (∀ i, size (K i) < size N) ∧
        alg N p = comb (fun i => alg (K i) (q i)) ∧
        Z N p = comb (fun i => Z (K i) (q i))) :
    ∀ N p, alg N p = Z N p := by
  sorry

end OAI.EthKit.Comparator
