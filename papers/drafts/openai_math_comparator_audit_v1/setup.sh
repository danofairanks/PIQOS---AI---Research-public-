#!/bin/bash
# The steps used, in order. Not a polished installer: paths were /srv/lean/{tc,proj,tools}; adapt before running.
set -e
# 1. Lean 4.34.1 (zstd tarball; python3 -m pip install zstandard to unpack without a zstd binary)
curl -sSL -o lean.tar.zst https://github.com/leanprover/lean4/releases/download/v4.34.1/lean-4.34.1-linux.tar.zst
# 2. Comparator and lean4export at the pins in PINS.txt; set lean-toolchain to leanprover/lean4:v4.34.1 in both;
#    in comparator/lakefile.toml replace the [[require]] for lean4export with  path = "../lean4export"; then `lake build` in each.
# 3. landrun: GOPATH=... go install github.com/zouuup/landrun/cmd/landrun@latest
# 4. A project containing: lean-toolchain (from the repo), a lakefile.lean with
#      package OAI where fixedToolchain := true; leanOptions := #[⟨`autoImplicit, false⟩]   (as in the repo)
#      require mathlib from git "https://github.com/leanprover-community/mathlib4.git" @ "d13f23b723b8a846827a245b89c10fc7d3f11612"
#      lean_lib OAIAll where roots := #[`OAI]; globs := #[`OAI.+]
#      lean_lib ComparatorChallenges where globs := #[`ComparatorChallenges.+]
#    the OAI/ modules in the import closure of each solution module, copied unmodified, and ComparatorChallenges/<Name>.{lean,json} unmodified.
# 5. `lake update`, then kill it when it starts `cache get` (the cache host is unreachable); `lake build ProofWidgets` once with network (needs node/npm).
# 6. Run each config with run_cmp.sh (unprivileged user, no network).
