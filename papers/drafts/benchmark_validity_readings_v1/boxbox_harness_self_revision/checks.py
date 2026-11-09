"""Arithmetic behind the reading of arXiv 2611.09218v1 (BoxBox / PerfRace). Every number is typed from the paper's tables and text and recomputed here.
Run: python3 -I checks.py   (standard library only)"""
T1 = {"Frozen": (1.442, 23.22, 0.2142), "HE": (1.281, 24.56, 0.1243), "HS": (1.539, 12.98, 0.2872), "BoxBox": (1.702, 16.43, 0.4886)}  # Table 1: Speedup@4h, mean model cost per run ($), Speedup/$
print("== C1 Table 1: the per-dollar column against the table's own means")
print("  method   S/cost (ratio of means)   (S-1)/cost   reported Speedup/$   reported / (S/cost)")
for k, (s, c, r) in T1.items():
    print(f"  {k:7s}  {s/c:.4f}                    {(s-1)/c:.4f}       {r:.4f}               {r/(s/c):.2f}")
b, h = T1["BoxBox"], T1["HS"]
print(f"  BoxBox / HS: reported x{b[2]/h[2]:.2f}; ratio of means x{(b[0]/b[1])/(h[0]/h[1]):.2f}; gain per dollar (S-1)/cost x{((b[0]-1)/b[1])/((h[0]-1)/h[1]):.2f}")
print(f"  cost cut against Frozen: {(1-b[1]/T1['Frozen'][1])*100:.1f}% (paper: 29.3%)")
print("== C2 size of the headline lead")
print(f"  BoxBox - HS = {b[0]-h[0]:.3f} ({(b[0]/h[0]-1)*100:.1f}% relative); BoxBox - Frozen = {b[0]-T1['Frozen'][0]:.3f} ({(b[0]/T1['Frozen'][0]-1)*100:.1f}%)")
print("  intervals in Fig. 1 resample the 3 runs per task over the fixed 50-task set (Appendix A.1); tasks are not resampled, so this lead has no task-level interval")
print("== C3 ablation (Table 2; 14 sampled test tasks)")
for lab, s, c, r in [("w/o Agent Triggering", 1.508, 21.58, 0.1338), ("w/o Full Editing", 1.349, 16.07, 0.1132), ("Full BoxBox", 1.584, 15.07, 0.3452)]:
    print(f"  {lab:21s} speedup {s}  cost ${c}  reported Speedup/$ {r}  S/cost {s/c:.4f}  ratio {r/(s/c):.2f}")
print(f"  Full vs w/o Agent Triggering: speedup +{(1.584/1.508-1)*100:.1f}%; Full BoxBox on these 14 tasks is 1.584 (1.702 on all 50); no Frozen reference on the same 14 is reported")
print("  review cadence: 30-minute cooldown after each review (Appendix C.2) -> at most", int(240 // 30), "reviews in 4 h; observed median 5; the compared variant reviews every 30 minutes")
print("== C4 offline baseline (HE) cost accounting (Table 4)")
print(f"  test: 150 runs x $24.56 = ${150*24.56:.1f} (Table 4: $3,683.34); per run with training and validation: ${(200.34+1176.12+3683.34)/150:.2f} (paper: at least $33.73)")
print("== C5 internal consistency")
print(f"  Frozen at 4 h: 1.442 on the 50 test tasks (Table 1) against 1.435 on 88 tasks (Appendix B.5)")
print(f"  HS attempts 2,132 minus 150 runs = {2132-150} boundaries (text: 1,983; off by one, immaterial)")
print("  Appendix B.5 evaluates '88 tasks' (264 trajectories) of 100; the text read gives no reason for 88")
print("  Table 11: CV < 6% on", 20 + 64, "of 99 wall-clock tasks; 6-10% on", 8 + 3 + 4, "; red-team cases per task: one on 60 of 100 tasks")
print("  Table 9: 93,992 of 103,475 candidates fail on fewer than 10 GitHub stars; 239 reach Pair Verification; 132 rejected in design, 6 in build, 1 at finalisation ->", 239 - 132 - 6 - 1, "accepted (paper: 100)")
