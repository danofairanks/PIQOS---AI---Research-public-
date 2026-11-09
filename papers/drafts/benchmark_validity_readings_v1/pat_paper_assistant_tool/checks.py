"""Arithmetic behind the reading of arXiv 2606.28277v1 (Paper Assistant Tool). Every number is typed from the paper's tables and text and recomputed here.
Run: python3 -I checks.py   (needs scipy)"""
import math
from scipy import stats
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); a = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return (c - a) / d, (c + a) / d
print("== C1 SPOT subset (Table 2): 26 papers, 29 errors")
print(f"  PAT 26/29 = {26/29*100:.1f}% ; zero-shot 16/29 = {16/29*100:.1f}% (stated 89.7 and 55.2)")
print(f"  Wilson 95%: PAT {wilson(26,29)[0]*100:.1f}-{wilson(26,29)[1]*100:.1f}% ; zero-shot {wilson(16,29)[0]*100:.1f}-{wilson(16,29)[1]*100:.1f}%")
print(f"  gain {(26-16)/29*100:.1f} points ('34%' in the text); relative gain {((26/16)-1)*100:.0f}% ; extra errors found {26-16}")
print(f"  unpaired Fisher exact p = {stats.fisher_exact([[26,3],[16,13]])[1]:.4f} (paired outcomes are not reported, so McNemar cannot be computed)")
print(f"  original SPOT best 21.1% would be {0.211*29:.1f} of 29 errors (6/29 = {6/29*100:.1f}%, 7/29 = {7/29*100:.1f}%)")
print("== C2 Table 1 submission counts")
tab = {2020: (2594, 4990, 9467), 2021: (3014, 5513, 9122), 2022: (3422, 5630, 10411), 2023: (4955, 6538, 12345), 2024: (7304, 9653, 15671), 2025: (11672, 12107, 21575), 2026: (19809, 24371, 29703)}
prev = None
for y, v in tab.items():
    s = sum(v); print(f"  {y}: {s}" + ("" if prev is None else f" ; year on year {(s/prev-1)*100:+.2f}%")); prev = s
print(f"  NeurIPS 2026 estimate = 21575 x (21575/15671) = {21575*21575/15671:.0f} (table 29,703); share of the 2026 combined total that is extrapolated: {29703/73883*100:.1f}%")
print("== C3 NeurIPS 2021 consistency experiment")
print(f"  random-selection inconsistency at acceptance 0.227: 2p(1-p) = {2*0.227*0.773:.3f} (text: 35%)")
print("== C4 survey percentages against the stated cohort sizes (STOC n = 124, ICML n = 733); entries reported as integers (97%, 31%) are not tested")
def attain(pct, n):
    full = [k for k in range(n + 1) if abs(k / n * 100 - pct) < 0.051]
    if full: return f"{full[0]}/{n}"
    for m in range(n - 1, n - 9, -1):
        ks = [k for k in range(m + 1) if abs(k / m * 100 - pct) < 0.051]
        if ks: return f"not attainable at n = {n}; fits {ks[0]}/{m}"
    return f"not attainable at n = {n} or n-1..n-8"
for lab, pct, n in [("STOC improved clarity", 85.1, 124), ("STOC education value", 75.2, 124), ("STOC very/mostly helpful", 92.7, 124), ("STOC mostly/all grounded", 55.8, 124), ("STOC substantive theory gaps", 11.6, 124),
                    ("ICML would use again", 92.1, 733), ("ICML improved clarity", 87.0, 733), ("ICML education value", 83.9, 733), ("ICML very/mostly helpful", 90.7, 733), ("ICML mostly/all grounded", 64.8, 733), ("ICML substantive theory gaps", 35.4, 733)]:
    print(f"  {lab:40s} {pct:5.1f}% -> {attain(pct, n)}")
print(f"  respondents 124 + 733 = {124+733}; against 'over 4,700 submissions' at most {(124+733)/4700*100:.1f}% (units differ)")
print(f"  not mostly/all grounded: STOC {100-55.8:.1f}% ; ICML {100-64.8:.1f}%")
