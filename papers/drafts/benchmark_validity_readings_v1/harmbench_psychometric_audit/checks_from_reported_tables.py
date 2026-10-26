"""Arithmetic on numbers REPORTED in arXiv 2610.12409v1 (Stewart et al., psychometric audit of HarmBench).
Nothing is re-fitted; HELM Safety response data and the authors' code were not accessed.
Post-hoc and descriptive: confirms the paper's tables are internally consistent and derives the context
numbers quoted in README.md. Inputs typed from Table 1, Table 4 and Section 3 (page refs in README.md).
"""
n_models, n_items = 81, 398
print("C1 parameter counts (Table 1)")
print(f"  1D 2PL  : 2*{n_items}+{n_models} = {2*n_items+n_models} (reported 877)")
print(f"  conf 3D : 2*{n_items}+3*{n_models} = {2*n_items+3*n_models} (reported 1,039)")
print(f"  conf 7D : 2*{n_items}+7*{n_models} = {2*n_items+7*n_models} (reported 1,363)")
print(f"  expl d=2: 2*877 = {2*877} (reported 1,754); d=10: 10*877 = {10*877} (reported 8,770)")

print("C2 held-out log-loss gaps (mean across 5 splits; SDs 0.003-0.007)")
ll = {"1D 2PL": .470, "1D 3PL": .322, "1D 1PL": .330, "expl 2D": .287, "conf 3D": .258, "conf 7D": .255}
print(f"  1D 3PL - conf 3D = {ll['1D 3PL']-ll['conf 3D']:.3f} (reported 0.064)")
print(f"  1D 3PL - expl 2D = {ll['1D 3PL']-ll['expl 2D']:.3f}; 1D 2PL - expl 2D = {ll['1D 2PL']-ll['expl 2D']:.3f}")
print(f"  1D 2PL is worse than 1D 1PL by {ll['1D 2PL']-ll['1D 1PL']:.3f} although it has more parameters (877 vs 479):")
print("    the '1 -> 2 dimensions improves sharply' headline in the text uses the poorly fitting 1D 2PL; the paper's own comparator is the 1D 3PL")

print("C3 pool composition (Section 3.2, Table 4)")
print(f"  OpenAI+Anthropic = 21+11 = 32 of {n_models} models ({100*32/n_models:.0f}%); closed+open = 48+33 = {48+33}")
print(f"  raw means: OpenAI .866, Anthropic .889 vs pool pass rate .67 -> both DIF groups sit at the top")
print(f"  expected failures per model at those means: {(1-.866)*n_items:.0f} (OpenAI), {(1-.889)*n_items:.0f} (Anthropic) of {n_items} items")
print("  closed .776 vs open .507, yet 0 DIF flags in every scope")

print("C4 DIF flag counts (Table 2): single score 13 (MH) / 17 (logit) of 398; 3D scopes 1 / 2; 7D scopes 2+0.. / cyber 2 MH 4 logit")
print(f"  13/398 = {100*13/398:.1f}%, 17/398 = {100*17/398:.1f}% (family-wise cutoff from a fitted 1D no-DIF simulation)")

print("C5 follow-up without copyright (Section 4): 2D vs 1D 2PL log-loss .278 vs .293, paired reduction .0149 (SD .0043) over 295-298 items")
print(f"  reduction / SD = {0.0149/0.0043:.1f} (5 splits; splits share models, so the SD is not an independent-sample error)")
