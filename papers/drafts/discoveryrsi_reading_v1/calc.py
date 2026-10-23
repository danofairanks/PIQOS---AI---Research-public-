"""Arithmetic on numbers printed in arXiv:2610.23839v2. Standard library only.
Run: python3 -I calc.py
Inputs are transcribed by hand from the PDF (counts: Section 7.4 and Appendix F, Table 6;
axis means and their changes: Section 7.1 prose for six axes, Figure 6 text layer for grounding
and actionability; weights: Appendix D.1).  Units are hypothesis versions, which are dependent
within research families, so every test below is naive and generous to the headline."""
import math
from math import comb

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d

def fisher_two_sided(a, b, c, d):
    n = a + b + c + d; r1 = a + b; c1 = a + c
    pm = lambda x: comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1)
    p0 = pm(a)
    return sum(pm(x) for x in range(max(0, c1 - (n - r1)), min(r1, c1) + 1) if pm(x) <= p0 * (1 + 1e-9))

groups = {'DiscoveryRSI-27B': (74, 1176), 'DeepSeek': (14, 257), 'GLM': (1, 36), 'GPT': (59, 2341), 'Claude': (3, 131)}
print('1. rates with 95% Wilson intervals')
for g, (k, n) in groups.items():
    lo, hi = wilson(k, n); print(f'   {g:17s} {k:3d}/{n:5d} = {100*k/n:4.1f}%  [{100*lo:4.1f}, {100*hi:4.1f}]')
print('2. naive Fisher exact p, DiscoveryRSI-27B vs each group')
k0, n0 = groups['DiscoveryRSI-27B']
for g in ('DeepSeek', 'GLM', 'GPT', 'Claude'):
    k, n = groups[g]; print(f'   vs {g:9s} p = {fisher_two_sided(k0, n0 - k0, k, n - k):.3f}')
print('3. conditional on passing the retrieval gate (Appendix F.4: Claude 15/131, DiscoveryRSI 355/1,176)')
print('   gate pass rates: Claude %.1f%%, DiscoveryRSI %.1f%%' % (100 * 15 / 131, 100 * 355 / 1176))
print('   positives among gate-passers: Claude 3/15 = %.1f%%, DiscoveryRSI 74/355 = %.1f%%; Fisher p = %.3f' % (100 * 3 / 15, 100 * 74 / 355, fisher_two_sided(74, 355 - 74, 3, 15 - 3)))
print('4. DiscoveryRSI-27B by domain (Table 6): positives / generated')
dom = {'Clinical and population health': (13, 557), 'Therapeutic target prioritization': (30, 178), 'Disease mechanisms': (17, 251), 'Population multi-omics': (14, 190)}
print('   sums:', sum(v[0] for v in dom.values()), sum(v[1] for v in dom.values()))
for g, (k, n) in dom.items():
    lo, hi = wilson(k, n); print(f'   {g:34s} {k:3d}/{n:4d} = {100*k/n:4.1f}%  [{100*lo:4.1f}, {100*hi:4.1f}]')
kx = 74 - 30; nx = 1176 - 178
print('   without therapeutic targets: %d/%d = %.1f%% (therapeutic targets: %.1f%% of versions, %.1f%% of positives)' % (kx, nx, 100 * kx / nx, 100 * 178 / 1176, 100 * 30 / 74))
print('   NOTE: the other groups\' domain counts are not printed, so a like-for-like pooled comparison cannot be made.')
print('5. the quality composite (Appendix D.1 weights; Section 7.1 / Figure 6 axis means, round 0 and round 2)')
dims = ['importance', 'novelty', 'grounding', 'falsifiability', 'data resolvability', 'feasibility', 'alternatives', 'actionability']
w = [20, 20, 15, 10, 10, 10, 10, 5]
r0 = [6.48, 4.87, 4.24, 4.00, 3.73, 4.79, 4.44, 5.20]
r2 = [6.04, 4.58, 4.56, 6.20, 4.99, 5.87, 5.98, 5.47]
q0 = sum(a * b for a, b in zip(w, r0)) / 100; q2 = sum(a * b for a, b in zip(w, r2)) / 100
print('   composite from axis means: %.3f -> %.3f (paper: 4.86 -> 5.39), change %.3f' % (q0, q2, q2 - q0))
value = [0, 1, 2, 7]; test = [3, 4, 5, 6]
cv = sum(w[i] * (r2[i] - r0[i]) for i in value) / 100; ct = sum(w[i] * (r2[i] - r0[i]) for i in test) / 100
print('   contribution to the change: value axes (importance, novelty, grounding, actionability) %+.3f ; testability axes (falsifiability, data resolvability, feasibility, alternatives) %+.3f' % (cv, ct))
print('   per axis change:', ', '.join('%s %+.2f' % (d, b - a) for d, a, b in zip(dims, r0, r2)))
print('   importance + novelty alone, weighted: %+.3f' % ((20 * (r2[0] - r0[0]) + 20 * (r2[1] - r0[1])) / 100))
print('6. gain per round (Section 7.1): %.2f then %.2f' % (5.18 - 4.86, 5.39 - 5.18))
