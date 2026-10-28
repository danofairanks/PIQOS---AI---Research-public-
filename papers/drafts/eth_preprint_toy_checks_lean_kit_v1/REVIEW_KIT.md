# Review kit: ETH preprint (openai/math, 25 Oct 2026, sha256 5b1612dc...8123)
Everything below is my own work product; none of it has been externally reviewed.

## 1. Obligations table
`INDUCTION_LEMMA.md` lists O1-O10 (what the induction needs), each marked R (read), T (tested at toy scale), M (cost-modeled). O10 (canonical lifting consistency) is R only. The induction itself was never run (toy tuple counts exceed 10^108).

## 2. Harnesses and results (folders in `harness/`)
eth_counter_test, eth_cost_model, eth_sparsification_model, eth_appendixD_model, eth_appendixA_check, eth_appendixB_check, eth_lemma45_check, eth_lemma46_check, eth_lemma48_check, eth_lemma52_check, eth_section3_check, eth_section6_check, eth_appendixD_proofs_check, eth_modes_check, eth_D11_check, eth_induction_check, eth_sections345_run; each has a `RESULTS_eth_*.md` in `results/`. Bounded Sections 3-5 end-to-end run: 85/85 exact (source: `results/RESULTS_eth_sections345_run.md`). No gap found at toy scale.

## 3. Lean (this kit)
`lean/ComparatorChallenges/EthKit.{lean,json}` (challenge, `sorry`) and `lean/OAI/EthKit/Comparator.lean` (solution); log in `lean/comparator_EthKit.log`.

## 4. Claims that need expert review (not settled by anything here)
1. The induction invariants hold for the D.4.6 child networks as defined: (A1)-(A5) preserved, parameter regime (P1)-(P6) closed under the recursion (O5-O8).
2. Canonical lifting consistency across precisions (O10).
3. Precision bookkeeping D.11 at real parameter sizes; thresholds I computed (lambda_2 about 2e6-8e6; D.11 lambda_1 about 3e7-7e7; Lemma 4.8 lambda_0 about 1e10-1e11) are from my reading of the constants.
4. That the subexponential regime appears only for n above roughly 2^(10^10) to 2^(10^17) in my cost model: this concerns practicality, not correctness, but depends on my reading of hidden constants.
5. Whether `branch_partition` etc. match the paper's Lemma A.1, Section 3.4, Lemma 5.2, Lemma 6.2 as intended.
6. Formalization of the full theorem including the time bound is out of reach here.

## 5. Caveats
Same model family wrote the reading, harnesses, and Lean; convergence among them is not independent verification.
