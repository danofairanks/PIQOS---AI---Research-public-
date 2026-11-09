"""Arithmetic behind the two papers added on 2026-11-09 (Steer2Edit, arXiv 2602.09870v3; ThinkEdit, arXiv 2503.22048v4). Every number is typed from the cited tables and recomputed here. Run: python3 -I checks_arithmetic_added_papers.py"""
print("== Steer2Edit (arXiv 2602.09870v3)")
print("  LLaMA-2-7B-Chat safety 49.9 -> 88.2: +%.1f; utility 35.5 -> 28.0: %.1f points, %.0f%% relative" % (88.2-49.9, 28.0-35.5, (28.0-35.5)/35.5*100))
print("  LLaMA-2-70B-Chat: safety 66.6 -> 97.0 (+%.1f); utility 51.8 -> 35.7: %.1f points, %.0f%% relative" % (97.0-66.6, 35.7-51.8, (35.7-51.8)/51.8*100))
print("  70B best steering config by safety (alpha 1.5): safety 79.4 utility 37.9; gap to the edit %.1f (paper text: +17.6); edit utility is %.1f below that configuration" % (97.0-79.4, 37.9-35.7))
print("  70B CommonsenseQA 64.3 -> 44.8 (%.1f), GSM8K 48.3 -> 26.9 (%.1f), CodeMMLU 42.7 -> 35.5 (%.1f)" % (44.8-64.3, 26.9-48.3, 35.5-42.7))
print("  Qwen3-4B-Thinking best config (Table 10): average accuracy 87.8 -> 77.3 (%.1f); GPQA 66.3 -> 42.4 (%.1f); MATH-500 97.7 -> 89.7 (%.1f); length 5319 -> 3387 (%.1f%%)" % (77.3-87.8, 42.4-66.3, 89.7-97.7, (3387-5319)/5319*100))
print("  OR-Bench (Table 11): over-refusal original 60.1 -> edit 66.4 (+%.1f); at about 66%% over-refusal steering (alpha 0.5, 65.8) has safety 60.5 vs the edit's 88.1 (+%.1f)" % (66.4-60.1, 88.1-60.5))
print("  AUSteer trade-off config (Table 15): safety 77.2 utility 30.2; the edit 88.2 / 28.0 (utility %.1f lower)" % (30.2-28.0))
print("  Diffusion LLM (n=1, Table 14): average utility 33.8 -> 18.8 (%.0f%% relative); safety 51.5 -> 88.0" % ((18.8-33.8)/33.8*100))
print("  Truthfulness LLaMA-3-8B: TruthfulQA 40.3 -> 53.1 (+%.1f); utility 65.8 -> 62.7 (%.1f); Expert-FACTOR 41.5 -> 54.2 (+%.1f)" % (53.1-40.3, 62.7-65.8, 54.2-41.5))
print("  Judge swap (Table 16): agreement 222+120 = %d of 408 = %.1f%%; disagreements %d" % (222+120, (222+120)/408*100, 11+55))
print("== ThinkEdit (arXiv 2503.22048v4)")
T1={'14B':[(90.80,93.78),(95.08,96.56),(96.32,96.36),(90.25,91.03),(91.48,91.92)],
    '8B':[(82.26,89.44),(96.01,96.19),(93.46,94.44),(85.49,86.49),(87.26,88.06)],
    '1.5B':[(79.15,84.56),(68.52,90.66),(93.00,93.66),(75.48,75.05),(82.22,82.24)]}
d=[b-a for v in T1.values() for a,b in v]
print("  Table 1: mean gain over %d cells = %.2f; without the 1.5B MMLU Elementary Math cell (+22.14) = %.2f; negative cells = %d" % (len(d), sum(d)/len(d), (sum(d)-22.14)/14, sum(1 for x in d if x<0)))
d32=[95.25-92.97,98.02-95.93,96.02-96.41,91.31-91.27,91.60-91.62]
print("  with the 32B model (Table 9, 4%% rate): mean gain over 20 cells = %.2f" % ((sum(d)+sum(d32))/20))
T2={'14B':[((96.31,95.65,92.93),(96.31,96.18,96.77)),((93.89,96.22,95.60),(97.78,95.14,96.53)),((99.52,99.30,97.70),(99.52,99.53,98.62)),((89.39,94.32,96.25),(96.67,97.88,98.11)),((86.40,91.40,93.50),(91.20,93.20,95.00))],
 '8B':[((88.92,87.18,85.82),(96.31,95.50,94.68)),((97.22,96.49,96.80),(97.78,97.57,97.60)),((97.14,94.88,94.83),(99.05,99.07,97.82)),((78.64,88.79,93.41),(95.76,97.42,97.46)),((82.00,81.40,88.30),(95.60,93.80,95.40))],
 '1.5B':[((88.46,87.48,85.02),(92.62,92.90,92.32)),((62.78,62.16,60.53),(87.78,88.11,88.67)),((97.62,95.12,93.91),(95.71,95.58,96.44)),((91.52,95.00,95.72),(95.15,96.59,97.27)),((82.40,89.80,93.40),(90.80,92.00,94.20))]}
dd=[b-a for v in T2.values() for o,e in v for a,b in zip(o,e)]
print("  Table 2: mean gain over %d cells = %.2f; negative cells = %d" % (len(dd), sum(dd)/len(dd), sum(1 for x in dd if x<0)))
T4={'14B':[(354.5,538.2),(184.9,291.4),(1600.5,1670.4),(4306.2,4243.7),(3096.8,3079.7)],
    '8B':[(597.3,927.7),(1486.6,1517.9),(1646.6,1723.7),(4789.1,4773.5),(3507.6,3509.5)],
    '1.5B':[(768.1,1126.6),(517.0,768.9),(2080.9,1946.3),(6360.0,5522.4),(4260.3,3821.1)]}
names=['GSM8K','MMLU-elem','MATH-L1','MATH-L5','MATH-500']
for m,v in T4.items(): print("  Table 4 relative length change", m, ["%s %+.1f%%"%(n,(b-a)/a*100) for n,(a,b) in zip(names,v)])
A=sum(a for v in T4.values() for a,b in v); B=sum(b for v in T4.values() for a,b in v)
print("  token-pooled length change over all 15 cells = %.2f%% (paper: -0.27%%)" % ((B-A)/A*100))
print("  mean of the 15 per-cell relative changes = %.1f%%" % (sum((b-a)/a*100 for v in T4.values() for a,b in v)/15))
print("  Table 15 mean relative length change over four models = %.1f%% (paper: +48.0%%)" % (sum([(409.03-308.32)/308.32,(518.06-341.09)/341.09,(957.32-606.09)/606.09,(1125.64-753.45)/753.45])/4*100))
