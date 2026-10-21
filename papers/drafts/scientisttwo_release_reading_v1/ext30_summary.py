"""Recomputes the second-tranche counts from ext30_coding.jsonl (one JSON object per paper)."""
import json, math
rows = [json.loads(l) for l in open('ext30_coding.jsonl')]
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
n = len(rows); k = sum(1 for r in rows if r['mismatches'] > 0)
print('papers', n, 'with >=1 counted mismatch', k, '%.0f%%' % (100 * k / n), 'Wilson %.2f-%.2f' % wilson(k, n))
minor = {'e08', 'e18', 'e27'}
k2 = sum(1 for r in rows if r['mismatches'] > 0 and r['id'] not in minor)
print('excluding minor/arguable', sorted(minor), k2, '%.0f%%' % (100 * k2 / n), 'Wilson %.2f-%.2f' % wilson(k2, n))
k3, n3 = k + 5, n + 6   # plus the six papers of the first tranche (5 with a counted mismatch)
print('with the first six:', k3, '/', n3, '%.0f%%' % (100 * k3 / n3), 'Wilson %.2f-%.2f' % wilson(k3, n3))
print('with no counted mismatch:', sum(1 for r in rows if r['mismatches'] == 0))
