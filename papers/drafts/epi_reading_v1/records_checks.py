"""Count and margin checks on data/records.json of the results repository BakeLab/Epi-results at the pinned commit
97fa6a420f417458e11723c8bceb70f1529e447a (single-file fetch, no clone).  Standard library only.  Usage: python3 -I records_checks.py
Relative gain = |result - previous_comparison| / |previous_comparison|, the 'earlier value used for comparison' the paper says its tables retain."""
import json, urllib.request, collections, statistics
U = 'https://raw.githubusercontent.com/BakeLab/Epi-results/97fa6a420f417458e11723c8bceb70f1529e447a/data/records.json'
d = json.loads(urllib.request.urlopen(urllib.request.Request(U, headers={'User-Agent': 'research-check/1.0'}), timeout=30).read())
print('records:', len(d))
print('status:', dict(collections.Counter(x['status'] for x in d)))
print('category:', dict(collections.Counter(x['category'] for x in d)))
pack = {'circular-quadrant', 'four-dimensional-balls', 'semicircle', 'pentagons', 'octagon'}
print('geometric packing records (paper: 97 of 100):', sum(x['category'] in pack for x in d))
print('non-packing:', [x['category'] for x in d if x['category'] not in pack])
rows = []
for x in d:
    p = x.get('previous_comparison')
    if isinstance(p, (int, float)) and p != 0:
        rows.append((abs(x['result'] - p) / abs(p), x['id'], x['category'], x['status']))
print('records with a numeric previous_comparison:', len(rows), 'of', len(d))
g = sorted(r[0] for r in rows)
q = lambda f: g[int(f * (len(g) - 1))]
print('relative gain: min %.2e  median %.2e  p90 %.2e  max %.2e' % (g[0], statistics.median(g), q(0.9), g[-1]))
for thr in (1e-4, 2.8e-4, 1e-3, 1e-2):
    print('  gains <= %.1e: %d of %d' % (thr, sum(v <= thr for v in g), len(g)))
print('largest five:')
for r in sorted(rows, reverse=True)[:5]: print('   %.3e  %s  (%s, %s)' % r)
for st in ('improves_registry', 'listed_record'):
    gg = sorted(r[0] for r in rows if r[3] == st)
    if gg: print('%s: n=%d  median %.2e  max %.2e' % (st, len(gg), statistics.median(gg), gg[-1]))
