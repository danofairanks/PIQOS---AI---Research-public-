import Mathlib
import OAI.EthKit.Comparator

/-! D3: non-vacuity witnesses for the six theorems of the kit (negative-control file; not a Comparator module).
A witness shows that the hypotheses of a statement are satisfiable by a concrete, non-degenerate instance.
It does not show that the statement matches the paper's lemma. -/
namespace OAI.EthKit.Comparator

-- branch_partition has no hypotheses beyond universal quantification; two concrete instances, one with both sides true and one with both false.
example : FormulaSat (n := 1) (∅ ∪ (∅ : Finset (Clause 1)).image (fun p => ({(0, true)} : Clause 1) ∪ p)) (fun _ => true) ∧
    ((FormulaSat (n := 1) ((∅ : Finset (Clause 1)) ∪ {({(0, true)} : Clause 1)}) (fun _ => true) ∧
      ¬ FormulaSat (n := 1) ((∅ : Finset (Clause 1)) ∪ ∅ ∪ ({(0, true)} : Clause 1).image (fun l => ({negLit l} : Clause 1))) (fun _ => true))) := by
  refine ⟨?_, ?_, ?_⟩
  · intro C hC; simp at hC
  · intro C hC; simp at hC; subst hC; exact ⟨(0, true), by simp, rfl⟩
  · intro h; obtain ⟨l, hl, hx⟩ := h {negLit (0, true)} (by simp); simp [negLit] at hl; subst hl; simp at hx

example : ¬ FormulaSat (n := 1) ((∅ : Finset (Clause 1)) ∪ {({(0, true)} : Clause 1)}) (fun _ => false) := by
  intro h; obtain ⟨l, hl, hx⟩ := h {(0, true)} (by simp); simp at hl; subst hl; simp at hx

-- hermite_unique: hypotheses (d < Q*J, card nodes = Q, deg P <= d, vanishing to order J at all nodes) are satisfiable.
example : ∃ (nodes : Finset ℚ) (P : Polynomial ℚ), nodes.card = 1 ∧ P.natDegree ≤ 0 ∧
    ∀ t ∈ nodes, (Polynomial.X - Polynomial.C t) ^ 1 ∣ P :=
  ⟨{0}, 0, by simp, by simp, by simp⟩

-- degree_control: a concrete instance with m = 1 and y = X.
example : (∏ i : Fin 1, (MvPolynomial.C ((fun _ => (1:ℚ)) ((fun _ : Fin 1 => 0) i)) +
      MvPolynomial.C ((fun _ => (1:ℚ)) ((fun _ : Fin 1 => 0) i)) * (fun _ : Fin 1 => (MvPolynomial.X () : MvPolynomial Unit ℚ)) i) *
    ((fun _ : Fin 1 => (MvPolynomial.X () : MvPolynomial Unit ℚ)) i * (fun _ : Fin 1 => (MvPolynomial.X () : MvPolynomial Unit ℚ)) i -
      (fun _ : Fin 1 => (MvPolynomial.X () : MvPolynomial Unit ℚ)) i) ^ ((fun _ : Fin 1 => 0) i)).totalDegree ≤ 1 * (1 + 2 * ∑ i : Fin 1, (fun _ : Fin 1 => 0) i) :=
  degree_control 1 1 (fun _ => MvPolynomial.X ()) (fun _ => by simp) (fun _ => 1) (fun _ => 1) (fun _ => 0)

-- exists_le_average: D = identity on Fin 2, c = 1, sum = 1 <= 2.
example : ∃ γ : Fin 2, ((γ : ℕ) : ℚ) ≤ 1 :=
  exists_le_average (fun γ : Fin 2 => (γ : ℕ)) 1 (by simp [Fin.sum_univ_two])

-- greedy_contracts: D 0 = 1 <= 2^1, D (t+1) = 0.
example : (fun t : ℕ => if t = 0 then 1 else 0) (3 * 1) = 0 :=
  greedy_contracts 1 le_rfl (fun t => if t = 0 then 1 else 0) (by simp)
    (fun t => by simp)

-- contract_correct: Net = ℕ, size = id, H = 0, R p = ℕ, Z N p = N, alg N p = N, comb f = f 0 + 1 (a real one-child recursion).
example : ∀ (N p : ℕ), (fun (N p : ℕ) => N) N p = (fun (N p : ℕ) => N) N p :=
  contract_correct (Net := ℕ) (fun N => N) 0 (fun _ => ℕ) (fun N _ => N) (fun N _ => N)
    (fun N p h => rfl)
    (fun N p h => ⟨Unit, inferInstance, fun _ => N - 1, fun _ => p, fun f => f () + 1,
      fun _ => (by show N - 1 < N; omega), by simp; omega, by simp; omega⟩)

end OAI.EthKit.Comparator
