"""Arithmetic behind the reading of PoseBench (arXiv 2405.14108v7). Percentages are typed from the labels in Figs 2-4 (they are also in the PDF text layer); scored set sizes come from released_data_check*.py.
Run: python3 -I checks.py   (standard library only)"""
import math
def wilson(p, n, z=1.96):
    p /= 100; d = 1 + z*z/n; c = p + z*z/(2*n); a = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)); return (c-a)/d*100, (c+a)/d*100
def z(p1, p2, n):
    se = math.sqrt(p1/100*(1-p1/100)/n + p2/100*(1-p2/100)/n); return (p1-p2)/100/se
print("== C1 stated against scored set sizes (released data)")
print("  Astex: stated 85, scored 84 (AlphaFold 3 scores 84 per run; 1YV3_BIT of the 85 released directories is never scored)")
print("  DockGen-E: stated 122, scored 100 (AlphaFold 3 scores 100 per run, all inside the 122-id test split; 22 never scored); relative size of the gap:", f"{22/122*100:.0f}%")
print("  PoseBusters Benchmark: stated 130 of 308 after a training-cutoff filter; not recounted")
print("== C2 sampling width at the scored sizes (Wilson 95%, unpaired; the paper's +/- is SD over 3 runs, not over complexes)")
for lab, p, n in [("Astex AF3 54.8", 54.8, 84), ("Astex Chai-1 44.4", 44.4, 84), ("PB AF3 38.1", 38.1, 130), ("PB Boltz-1 34.4", 34.4, 130), ("PB Chai-1 27.7", 27.7, 130), ("DockGen-E AF3 44.3", 44.3, 100), ("DockGen-E Boltz-1 29.3", 29.3, 100), ("DockGen-E Chai-1 28.3", 28.3, 100)]:
    lo, hi = wilson(p, n); print(f"  {lab:24s} n={n:3d}: {lo:.1f}-{hi:.1f}")
print("== C3 headline gaps on RMSD<=2A & PB-valid, unpaired two-proportion z (paired outcomes are not reported, so McNemar cannot be computed)")
print(f"  PoseBusters AF3 - Boltz-1 = {38.1-34.4:.1f} pts, z = {z(38.1,34.4,130):.2f}; AF3 - Chai-1 = {38.1-27.7:.1f} pts, z = {z(38.1,27.7,130):.2f}")
print(f"  Astex AF3 - Chai-1 = {54.8-44.4:.1f} pts, z = {z(54.8,44.4,84):.2f}")
print(f"  DockGen-E AF3 - Boltz-1 = {44.3-29.3:.1f} pts, z = {z(44.3,29.3,100):.2f}")
print("== C4 failure to run is not separated from failure to dock (rows scored per run, from the released csv files; rates printed in the paper divide by 84 or 100)")
print("  Astex (84): AlphaFold 3 84; Boltz-1 61; DiffDock-L 75-77; P2Rank-Vina 50-53")
print("  DockGen-E (100): AlphaFold 3 100; Boltz-1 60-89; DiffDock-L 58-59; P2Rank-Vina 27-28")
print(f"  P2Rank-Vina on Astex: RMSD<=2 A printed 4.4% over 84; over its scored rows (mean 51.3) it is {4.4*84/51.3:.1f}%")
print("== C5 CASP15 sizes: 19 complexes (6 single, 13 multi), 102 fragment ligands; Appendix A gives 15 public (4 single + 11 multi); Appendix D.4 parentheses read '6 (2) and 13 (2)'")
print("  n = 13: Wilson 95% half-width at p=0.5 =", round((wilson(50,13)[1]-wilson(50,13)[0])/2,1), "points")
print("== C6 version drift (term counts in the extracted text): TULIP v1 4, v4 13, v7 0; Boltz v1 0, v4 0, v7 50; apo inputs ESMFold (v1) to AlphaFold 3 (v7); Astex 80 to 85; PoseBusters 280 to 308/130")
print("== C7 apo inputs: AlphaFold 3-predicted structures with RMSD<4 A and TM>0.7: PoseBusters 59.09%, CASP15 36.84% (all) and 20.00% (public)")
