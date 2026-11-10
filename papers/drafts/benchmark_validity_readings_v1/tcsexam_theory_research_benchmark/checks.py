"""Arithmetic behind the reading of arXiv 2611.07962v1 (TCSExam). Numbers typed from Tables 2, 3, 9, 11, 12 and 16 and Appendices C.3 and H. Run: python3 -I checks.py (standard library only)"""
import math, itertools
full = {  # agent: (theorem %, solver relative %, construction %, open-conjecture resolved %, index)
 "GPT-6 Astra": (70.0, 64.7, 104.9, 0.0, 71.9), "Kimi K3.1 Pro": (38.3, 54.1, 98.6, 1.1, 57.4), "Kimi K3": (11.7, 48.7, 95.5, 0.0, 46.8),
 "DeepSeek V4.1 Flash 1017": (6.7, 53.1, 91.8, 5.6, 46.0), "GLM-5.3": (5.0, 49.1, 97.7, 0.0, 45.5), "Qwen3.8 Max (0902)": (5.0, 49.2, 95.1, 0.0, 44.8),
 "Grok 4.6": (5.0, 43.8, 86.2, 0.0, 40.5), "DeepSeek V4.1 Flash 0910": (0.0, 48.3, 86.6, 0.0, 40.4)}
lite = {
 "Opus 5.5": (80.0, 60.5, 100.4, 0.0, 72.3), "GPT-6 Astra": (60.0, 63.0, 100.4, 0.0, 67.0), "Kimi K3.1 Pro": (40.0, 50.0, 88.3, 0.0, 53.5), "Kimi K3": (33.3, 48.9, 79.8, 0.0, 48.6),
 "GLM-5.3": (20.0, 46.1, 90.7, 0.0, 47.0), "Qwen3.8 Max (0902)": (20.0, 51.0, 80.3, 0.0, 45.4), "DeepSeek V4.1 Flash 1017": (6.7, 54.3, 80.2, 0.0, 42.4),
 "Grok 4.6": (20.0, 41.0, 79.3, 0.0, 42.1), "DeepSeek V4.1 Flash 0910": (0.0, 50.4, 79.7, 0.0, 39.0)}
def index(v, w=(30, 30, 30, 10)): return (w[0]*v[0] + w[1]*v[1] + w[2]*v[2] + w[3]*v[3]) / 100
print("== C1 Index I = 30P + 30S + 30C + 10O recomputed from the track means (Tables 2, 3); max abs difference to the printed Index")
for name, tab in (("Full", full), ("Lite", lite)):
    print(" ", name, round(max(abs(index(v) - v[4]) for v in tab.values()), 2))
print("== C2 Lite vs Full agreement (8 shared agents)")
shared = [a for a in full if a in lite]
def ranks(vals):
    order = sorted(vals, key=lambda a: -vals[a]); return {a: i + 1 for i, a in enumerate(order)}
rf = ranks({a: full[a][4] for a in shared}); rl = ranks({a: lite[a][4] for a in shared})
d2 = sum((rf[a] - rl[a])**2 for a in shared); n = len(shared)
print(f"  Spearman rho (no ties) = {1 - 6*d2/(n*(n*n-1)):.3f} (paper 0.93)")
pairs = list(itertools.combinations(shared, 2)); agree = [(a, b) for a, b in pairs if (full[a][4] - full[b][4]) * (lite[a][4] - lite[b][4]) > 0]
print("  pairs agreeing:", len(agree), "of", len(pairs), "(paper 26 of 28)")
orig6 = {"GPT-6 Astra", "Kimi K3", "GLM-5.3", "Qwen3.8 Max (0902)", "Grok 4.6", "DeepSeek V4.1 Flash 0910"}  # Appendix H.2: 1,000 attempts from the original six; Lite list fixed before K3.1 Pro and DeepSeek 1017 were run
ins = [(a, b) for a, b in pairs if a in orig6 and b in orig6]; out = [(a, b) for a, b in pairs if (a, b) not in ins]
print(f"  pairs among the six agents used to choose the Lite list: {len(ins)}, agreeing {sum((a,b) in agree for a,b in ins)}; pairs involving a later agent: {len(out)}, agreeing {sum((a,b) in agree for a,b in out)}")
print("  Appendix H.2: 15 of the 20 Lite tasks reuse the same submissions as Full for the eight shared agents (only the Solver track is run separately)")
print("== C3 Opus 5.5 vs GPT-6 Astra on Lite: where the 5.3-point lead comes from")
o, a = lite["Opus 5.5"], lite["GPT-6 Astra"]
parts = [30*(o[0]-a[0])/100, 30*(o[1]-a[1])/100, 30*(o[2]-a[2])/100, 10*(o[3]-a[3])/100]
print("  theorem, solver, construction, open contributions to the gap:", [round(x, 2) for x in parts], "sum", round(sum(parts), 2), "| one theorem task of five = 6.0 index points")
print("== C4 index sensitivity to weights (Full): rank orders")
schemes = {"authors 30/30/30/10": (30,30,30,10), "equal 25 each": (25,25,25,25), "theorem-heavy 40/20/20/20": (40,20,20,20), "no open track 1/3 each": (100/3,100/3,100/3,0), "theorem only": (100,0,0,0), "construction only": (0,0,100,0), "solver only": (0,100,0,0)}
for k, w in schemes.items():
    sc = {a: index(v, w) for a, v in full.items()}; r = sorted(sc, key=lambda x: -sc[x]); print(f"  {k:28s}", [x.replace('DeepSeek V4.1 Flash ', 'DS').replace('Qwen3.8 Max (0902)', 'Qwen').replace('Kimi ', 'K').replace('GPT-6 ', '') for x in r])
print("  index spread among the middle four agents (K3, DS1017, GLM, Qwen):", [full[a][4] for a in ("Kimi K3", "DeepSeek V4.1 Flash 1017", "GLM-5.3", "Qwen3.8 Max (0902)")])
print("== C5 weak agents' floor: DeepSeek V4.1 Flash 0910 solves 0 theorems yet scores", round(index(full['DeepSeek V4.1 Flash 0910']), 1), "of a leader's 71.9; construction + solver terms alone give", round(30*0.866 + 30*0.483, 1))
def wilson(k, n, z=1.96):
    p = k/n; d = 1 + z*z/n; c = p + z*z/(2*n); a = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)); return round((c-a)/d*100, 1), round((c+a)/d*100, 1)
print("== C6 theorem success, Wilson 95% (attempts as pooled; same-theorem attempts are correlated, so true intervals are wider for the 3-attempt agents)")
for lab, k, n in (("Astra 14/20", 14, 20), ("K3.1 Pro 23/60", 23, 60), ("K3 7/60", 7, 60), ("DS1017 4/60", 4, 60), ("GLM 1/20", 1, 20), ("Opus Lite 4/5", 4, 5), ("Astra Lite 3/5", 3, 5)):
    print(f"  {lab:16s} {round(k/n*100,1):5.1f}%  {wilson(k, n)}")
print("== C7 open conjectures: accepted resolutions are adaptations of published counterexamples/proofs: K3.1 Pro 1 of 90 attempts (", round(1/90*100, 1), "%), DS1017 5 of 90 (", round(5/90*100, 1), "%); the other 28 tasks have none")
print("== C8 Solver metric choice (Table 16, the six original agents): ranks under the Kimi K3-relative score used in the Index vs the original unbounded score")
t16 = {"GPT-6 Astra": (64.7, 107.1), "Kimi K3": (48.7, 78.1), "GLM-5.3": (49.1, 81.1), "Qwen3.8 Max (0902)": (49.2, 64.7), "Grok 4.6": (43.8, 74.6), "DeepSeek V4.1 Flash 0910": (48.3, 77.9)}
for j, lab in ((0, "relative"), (1, "original")):
    print(f"  {lab:8s}", sorted(t16, key=lambda a: -t16[a][j]), "| spread among the five non-leaders:", round(max(t16[a][j] for a in t16 if a != 'GPT-6 Astra') - min(t16[a][j] for a in t16 if a != 'GPT-6 Astra'), 1))
print("  Index recomputed with the original solver score (S = task score / 100) for the six original agents:")
alt = {a: (full[a][0]*0.3 + t16[a][1]*0.3 + full[a][2]*0.3 + full[a][3]*0.1) for a in t16}
print("   ", {a: round(v, 1) for a, v in sorted(alt.items(), key=lambda kv: -kv[1])}, "| printed Index:", {a: full[a][4] for a in t16})
print("  Kimi K3-relative scale: reference mean and standard deviation per instance come from three Kimi K3 attempts (sample SD, denominator n-1 = 2); 32 of 1,870 instances excluded for lacking two valid reference outcomes")
