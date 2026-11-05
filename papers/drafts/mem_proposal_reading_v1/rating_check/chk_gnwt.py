"""Re-derive the evidence row E and the K = min(M, E) comparison of arXiv 2609.38495 from its own Table 5 and Table 3.
Usage: pdftotext -layout 2609.38495.pdf 2609.38495.txt ; python3 -I chk_gnwt.py 2609.38495.txt
numpy only. The M values are read from the paper's Table 3 (author-assigned 'explanatory scope')."""
import sys, numpy as np
txt = open(sys.argv[1], encoding="utf-8").read().split("\n")
start = next(i for i, l in enumerate(txt) if "Table 5." in l and "Ratings of publications" in l)
rows = {}
for l in txt[start:start + 90]:
    t = l.split()
    if not t or not t[0].isdigit(): continue
    n = int(t[0]); nums = t[1:]
    if n > 25 or len(nums) < 17: continue
    rows[n] = (float(nums[0]), [int(x) for x in nums[1:17]])
assert len(rows) == 25, len(rows)
W = np.array([rows[n][0] for n in sorted(rows)]); R = np.array([rows[n][1] for n in sorted(rows)], float)
E = (W[:, None] * R).sum(0) / W.sum()
printed = [4.65,4.33,4.66,3.75,4.04,4.36,4.41,4.08,4.39,5.14,3.31,4.24,4.52,5.04,4.67,4.80]
print("E recomputed:", np.round(E, 2).tolist()); print("max |E - printed|:", float(np.abs(np.round(E, 2) - printed).max()))
crit = "P1 P2 P3 P4 A1 A2 A3 A4 S1 S2 S3 S4 B1 B2 B3 B4".split()
Mm = [6,6,6,6,6,5,5,6,6,5,6,6,6,6,4,4]; Mg = [5,3,5,4,6,6,6,6,6,5,4,3,6,5,6,5]
Km = np.minimum(Mm, E); Kg = np.minimum(Mg, E)
tie = [c for c, a, b in zip(crit, Km, Kg) if abs(a - b) < 1e-9]
print("K equal for the two theories on", len(tie), "of 16 criteria:", tie)
print("mean K MEM %.3f GNWT %.3f; mean M %.3f %.3f" % (Km.mean(), Kg.mean(), np.mean(Mm), np.mean(Mg)))
def Ef(mask, w): return (w[mask, None] * R[mask]).sum(0) / w[mask].sum()
for name, mask, w in [("equal weights", np.ones(25, bool), np.ones(25)), ("items 1-12 only", np.arange(25) < 12, W), ("items 13-25 only", np.arange(25) >= 12, W)]:
    e = Ef(mask, w); km = np.minimum(Mm, e).mean(); kg = np.minimum(Mg, e).mean()
    print("%s: mean K MEM %.3f GNWT %.3f diff %+.3f" % (name, km, kg, km - kg))
print("if M = 6 for both theories, K difference:", float(np.minimum(6, E).mean() - np.minimum(6, E).mean()))
