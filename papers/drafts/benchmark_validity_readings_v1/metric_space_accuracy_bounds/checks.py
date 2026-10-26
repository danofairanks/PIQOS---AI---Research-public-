import math
print("C1 reported classification intervals are [1-K, 1-K/2] (Cor 2.11): implied K and recomputed upper end")
for n,(lo,hi) in {"CIFAR-10 train":(85.61,92.81),"CIFAR-10 test":(83.76,91.88),"RESISC45 train":(83.85,91.93),
  "RESISC45 test":(82.36,91.18),"EUROSAT train":(97.78,98.89),"EUROSAT test":(96.89,98.44)}.items():
    K=1-lo/100; print(f"  {n:15s} K={K:.4f}  1-K/2={100*(1-K/2):.2f} reported {hi}")
print("C2 reported regression intervals are [K/2, K]: ratio hi/lo")
for n,(lo,hi) in {"synthetic train":(0.0102,0.0203),"synthetic test":(0.0113,0.0225)}.items(): print(f"  {n:16s} ratio {hi/lo:.2f}")
print("C3 synthetic example: floor bracket from the paper's stated noise (f's exact form not recovered; Lipschitz 0.9 from text)")
sd_t=0.03/math.sqrt(12)                      # target noise U([0,0.03])
rms_in=math.sqrt(2*(0.01**2/3))              # RMS of |delta|, delta ~ U([0,0.01]^2)
hi_in=0.9*rms_in                             # upper bound on input-noise effect on f
lo_floor=sd_t; hi_floor=math.sqrt(sd_t**2+hi_in**2)
print(f"  target-noise std {sd_t:.5f}; input-effect upper bound {hi_in:.5f}; floor in [{lo_floor:.4f}, {hi_floor:.4f}]")
print("  reported lower interval ends: train 0.0102, test 0.0113 -> inside the bracket: inconclusive")
