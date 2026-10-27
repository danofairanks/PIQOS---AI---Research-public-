import Lake
open Lake DSL

package OAI where
  fixedToolchain := true
  leanOptions := #[⟨`autoImplicit, false⟩]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "d13f23b723b8a846827a245b89c10fc7d3f11612"

lean_lib OAIAll where
  roots := #[`OAI.Analysis.Fourier.LocalSmoothing.Comparator]
  globs := #[.submodules `OAI]

lean_lib ComparatorChallenges where
  globs := #[.submodules `ComparatorChallenges]
