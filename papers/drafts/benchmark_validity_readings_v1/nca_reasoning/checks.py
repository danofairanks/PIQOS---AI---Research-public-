# Table 1 values transcribed from the text-extracted PDF (Params, FLOPs, accuracy).
fl={"NCA ARC pass@2 (K=3264)":2400,"NCA E ARC pass@2 (K=9792)":7100,"LoopViT-s":80.1,"LoopViT-m":132.7,"LoopViT-l":220.5}  # FLOPs in teraFLOPs (2.4P = 2400T)
print("C1 ARC-AGI-1: NCA FLOPs relative to LoopViT (pass@2 rows); accuracy 48.8 / 51.3 vs 60.1 / 63.8 / 65.8")
for n in ("NCA ARC pass@2 (K=3264)","NCA E ARC pass@2 (K=9792)"):
    print(f"  {n}: x{fl[n]/fl['LoopViT-s']:.1f} (s)  x{fl[n]/fl['LoopViT-m']:.1f} (m)  x{fl[n]/fl['LoopViT-l']:.1f} (l)")
print("C2 Maze-OOD 201x201: DeepThink 521.7T vs NCA 11.8T  ->",round(521.7/11.8,1),"x fewer FLOPs; accuracy 74.0 vs 100.0")
print("   Maze-OOD 59x59: 24.1T vs 163.4B ->",round(24100/163.4,1),"x")
print("   Maze-OOD size ratio by area: 201^2/9^2 =",round(201**2/9**2,1))
print("C3 Maze-Hard K=128 (NCA, A*): 89.2 vs PTRM mode@K=100 86.7; FLOPs",382.2/2.0,"x fewer; K=1: 86.6 vs 83.8 (A*), FLOPs 3.8T/15.3B =",round(3800/15.3,0),"x; depth D=200 vs 16 =",200/16,"x steps")
print("C4 Sudoku-OOD: K=1 66.1 vs 51.7 (+%.1f); conf@K 98.5 vs 89.5 (+%.1f); FLOPs 97.3T/23.9T = %.1fx fewer" % (66.1-51.7,98.5-89.5,97.3/23.9))
print("C5 Sudoku-Extreme: K=1 75.6 vs 87.3 (%.1f); conf@K 92.7 vs 98.8 (%.1f); FLOPs 190.1T vs 164.0T" % (75.6-87.3,92.7-98.8))
import math
print("C6 binomial SE on a 400-task ARC public eval set at p=0.49 (approx):",round(100*math.sqrt(.49*.51/400),2),"pp; reported NCA-TRM gap",round(48.8-44.6,1))
