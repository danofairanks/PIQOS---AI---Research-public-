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

theorem prop_core (g b a : Prop) :
    (g ∧ (a ∨ b)) ↔ ((g ∧ a) ∧ ¬ (g ∧ b ∧ ¬ a)) ∨ (¬ (g ∧ a) ∧ (g ∧ b ∧ ¬ a)) := by
  by_cases hg : g <;> by_cases ha : a <;> by_cases hb : b <;> simp [hg, ha, hb]

theorem branch_partition {n : ℕ} (G P : Finset (Clause n)) (H : Clause n) (x : Fin n → Bool) :
    FormulaSat (G ∪ P.image (fun p => H ∪ p)) x ↔
      (FormulaSat (G ∪ {H}) x ∧
          ¬ FormulaSat (G ∪ P ∪ H.image (fun l => ({negLit l} : Clause n))) x) ∨
      (¬ FormulaSat (G ∪ {H}) x ∧
          FormulaSat (G ∪ P ∪ H.image (fun l => ({negLit l} : Clause n))) x) := by
  have hU : ∀ A B : Finset (Clause n), FormulaSat (A ∪ B) x ↔ FormulaSat A x ∧ FormulaSat B x := by
    intro A B
    unfold FormulaSat
    constructor
    · intro h
      exact ⟨fun C hC => h C (Finset.mem_union_left _ hC), fun C hC => h C (Finset.mem_union_right _ hC)⟩
    · rintro ⟨h1, h2⟩ C hC
      rcases Finset.mem_union.mp hC with h | h
      · exact h1 C h
      · exact h2 C h
  have hS : FormulaSat ({H} : Finset (Clause n)) x ↔ ∃ l ∈ H, x l.1 = l.2 := by
    unfold FormulaSat; simp
  have hbool : ∀ b c : Bool, b = !c ↔ ¬ b = c := by decide
  have hN : FormulaSat (H.image (fun l => ({negLit l} : Clause n))) x ↔ ∀ l ∈ H, ¬ x l.1 = l.2 := by
    unfold FormulaSat
    rw [Finset.forall_mem_image]
    refine forall₂_congr (fun l hl => ?_)
    simp only [Finset.mem_singleton, exists_eq_left, negLit]
    exact hbool _ _
  have hI : FormulaSat (P.image (fun p => H ∪ p)) x ↔
      ((∃ l ∈ H, x l.1 = l.2) ∨ FormulaSat P x) := by
    unfold FormulaSat
    rw [Finset.forall_mem_image]
    constructor
    · intro h
      by_cases ha : ∃ l ∈ H, x l.1 = l.2
      · exact Or.inl ha
      · right
        intro p hp
        obtain ⟨l, hl, hx⟩ := h hp
        rcases Finset.mem_union.mp hl with h1 | h1
        · exact absurd ⟨l, h1, hx⟩ ha
        · exact ⟨l, h1, hx⟩
    · intro h p hp
      rcases h with ⟨l, hl, hx⟩ | h
      · exact ⟨l, Finset.mem_union_left _ hl, hx⟩
      · obtain ⟨l, hl, hx⟩ := h p hp
        exact ⟨l, Finset.mem_union_right _ hl, hx⟩
  have e1 : FormulaSat (G ∪ P.image (fun p => H ∪ p)) x ↔
      FormulaSat G x ∧ ((∃ l ∈ H, x l.1 = l.2) ∨ FormulaSat P x) := by
    rw [hU, hI]
  have e2 : FormulaSat (G ∪ {H}) x ↔ FormulaSat G x ∧ ∃ l ∈ H, x l.1 = l.2 := by
    rw [hU, hS]
  have e3 : FormulaSat (G ∪ P ∪ H.image (fun l => ({negLit l} : Clause n))) x ↔
      FormulaSat G x ∧ FormulaSat P x ∧ ¬ ∃ l ∈ H, x l.1 = l.2 := by
    have hneg : (∀ l ∈ H, ¬ x l.1 = l.2) ↔ ¬ ∃ l ∈ H, x l.1 = l.2 := by
      constructor
      · rintro h ⟨l, hl, hx⟩
        exact h l hl hx
      · intro h l hl hx
        exact h ⟨l, hl, hx⟩
    rw [hU, hU, hN, hneg]
    exact and_assoc
  rw [e1, e2, e3]
  exact prop_core _ _ _

/-! ## Section 3.4: Hermite uniqueness -/

theorem hermite_unique (Q J d : ℕ) (hQJ : d < Q * J) (nodes : Finset ℚ) (hn : nodes.card = Q)
    (P : Polynomial ℚ) (hdeg : P.natDegree ≤ d)
    (hroot : ∀ t ∈ nodes, (Polynomial.X - Polynomial.C t) ^ J ∣ P) : P = 0 := by
  by_contra hP
  have hcop : (nodes : Set ℚ).Pairwise
      (IsCoprime on fun t : ℚ => (Polynomial.X - Polynomial.C t) ^ J) := by
    intro a _ b _ hab
    exact (Polynomial.pairwise_coprime_X_sub_C (s := fun t : ℚ => t) (fun _ _ h => h) hab).pow
  have hdvd : (∏ t ∈ nodes, (Polynomial.X - Polynomial.C t) ^ J) ∣ P :=
    Finset.prod_dvd_of_coprime hcop hroot
  have hmonic : (∏ t ∈ nodes, (Polynomial.X - Polynomial.C t) ^ J).Monic :=
    Polynomial.monic_prod_of_monic _ _ (fun t _ => (Polynomial.monic_X_sub_C t).pow J)
  have hdeg_prod : (∏ t ∈ nodes, (Polynomial.X - Polynomial.C t) ^ J).natDegree = Q * J := by
    rw [Polynomial.natDegree_prod_of_monic _ _ (fun t _ => (Polynomial.monic_X_sub_C t).pow J)]
    simp [Polynomial.natDegree_pow, hn, Finset.sum_const, mul_comm]
  have := Polynomial.natDegree_le_of_dvd hdvd hP
  omega

/-! ## Lemma 5.2, degree control -/

theorem degree_control {σ : Type*} (m dstar : ℕ) (y : Fin m → MvPolynomial σ ℚ)
    (hy : ∀ i, (y i).totalDegree ≤ dstar) (a b : ℕ → ℚ) (j : Fin m → ℕ) :
    (∏ i, (MvPolynomial.C (a (j i)) + MvPolynomial.C (b (j i)) * y i) *
        (y i * y i - y i) ^ (j i)).totalDegree ≤ dstar * (m + 2 * ∑ i, j i) := by
  classical
  refine (MvPolynomial.totalDegree_finsetProd _ _).trans ?_
  have hterm : ∀ i, ((MvPolynomial.C (a (j i)) + MvPolynomial.C (b (j i)) * y i) *
      (y i * y i - y i) ^ (j i)).totalDegree ≤ dstar + 2 * dstar * j i := by
    intro i
    refine (MvPolynomial.totalDegree_mul _ _).trans ?_
    have h1 : (MvPolynomial.C (a (j i)) + MvPolynomial.C (b (j i)) * y i).totalDegree ≤ dstar := by
      refine (MvPolynomial.totalDegree_add _ _).trans ?_
      refine max_le ?_ ?_
      · simp [MvPolynomial.totalDegree_C]
      · refine (MvPolynomial.totalDegree_mul _ _).trans ?_
        have := hy i
        simp [MvPolynomial.totalDegree_C, this]
    have h2 : (y i * y i - y i).totalDegree ≤ 2 * dstar := by
      refine (MvPolynomial.totalDegree_sub _ _).trans ?_
      have hh := hy i
      refine max_le ?_ ?_
      · exact (MvPolynomial.totalDegree_mul _ _).trans (by omega)
      · omega
    have h3 : ((y i * y i - y i) ^ (j i)).totalDegree ≤ 2 * dstar * j i := by
      refine (MvPolynomial.totalDegree_pow _ _).trans ?_
      calc j i * (y i * y i - y i).totalDegree ≤ j i * (2 * dstar) := Nat.mul_le_mul_left _ h2
        _ = 2 * dstar * j i := by ring
    omega
  refine le_trans (Finset.sum_le_sum (fun i _ => hterm i)) ?_
  simp [Finset.sum_add_distrib, ← Finset.mul_sum]
  ring_nf
  exact le_refl _

/-! ## Lemma 6.2: averaging and the (27/32)^n argument -/

theorem exists_le_average {ι : Type*} [Fintype ι] [Nonempty ι] (D : ι → ℕ) (c : ℚ)
    (h : (∑ γ, (D γ : ℚ)) ≤ c * Fintype.card ι) : ∃ γ, (D γ : ℚ) ≤ c := by
  by_contra hcon
  push Not at hcon
  have : c * Fintype.card ι < ∑ γ, (D γ : ℚ) := by
    calc c * Fintype.card ι = ∑ _γ : ι, c := by simp [mul_comm]
      _ < ∑ γ, (D γ : ℚ) :=
        Finset.sum_lt_sum_of_nonempty Finset.univ_nonempty (fun γ _ => hcon γ)
  linarith

theorem greedy_contracts (n : ℕ) (hn : 1 ≤ n) (D : ℕ → ℕ) (h0 : D 0 ≤ 2 ^ n)
    (hstep : ∀ t, 4 * D (t + 1) ≤ 3 * D t) : D (3 * n) = 0 := by
  have key : ∀ t, 4 ^ t * D t ≤ 3 ^ t * D 0 := by
    intro t
    induction t with
    | zero => simp
    | succ t ih =>
      calc 4 ^ (t + 1) * D (t + 1) = 4 ^ t * (4 * D (t + 1)) := by ring
        _ ≤ 4 ^ t * (3 * D t) := Nat.mul_le_mul_left _ (hstep t)
        _ = 3 * (4 ^ t * D t) := by ring
        _ ≤ 3 * (3 ^ t * D 0) := Nat.mul_le_mul_left _ ih
        _ = 3 ^ (t + 1) * D 0 := by ring
  by_contra hne
  have hpos : 1 ≤ D (3 * n) := Nat.one_le_iff_ne_zero.mpr hne
  have h1 : 4 ^ (3 * n) ≤ 3 ^ (3 * n) * 2 ^ n :=
    calc 4 ^ (3 * n) ≤ 4 ^ (3 * n) * D (3 * n) := Nat.le_mul_of_pos_right _ hpos
      _ ≤ 3 ^ (3 * n) * D 0 := key (3 * n)
      _ ≤ 3 ^ (3 * n) * 2 ^ n := Nat.mul_le_mul_left _ h0
  have h54 : 3 ^ (3 * n) * 2 ^ n = 54 ^ n := by
    rw [pow_mul, ← mul_pow]; norm_num
  have h64 : 4 ^ (3 * n) = 64 ^ n := by
    rw [pow_mul]; norm_num
  rw [h54, h64] at h1
  have : 54 ^ n < 64 ^ n := Nat.pow_lt_pow_left (by norm_num) (by omega)
  omega

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
  intro N
  induction' hN : size N using Nat.strong_induction_on with s ih generalizing N
  intro p
  by_cases h : size N ≤ H
  · exact leaf N p h
  · push Not at h
    obtain ⟨ι, _, K, q, comb, hlt, hA, hZ⟩ := step N p h
    rw [hA, hZ]
    congr 1
    funext i
    exact ih (size (K i)) (hN ▸ hlt i) (K i) rfl (q i)

end OAI.EthKit.Comparator
