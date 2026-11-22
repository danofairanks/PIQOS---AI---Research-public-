# Probe 1: correlated failure among Lean checkers in the Lean Kernel Arena (round 2026-11-14..21).
# Input: /tmp/arena_results.json (https://arena.lean-lang.org/results.json). Output: probe1_results.json + printed summary.
import json, random, itertools, collections, re, sys
import numpy as np
d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else '/tmp/arena_results.json'))
tests = {t['name']: t for t in d['tests']}
chk = {c['name']: c for c in d['checkers']}
names = sorted(chk)
inv = sorted(t for t, v in tests.items() if v['outcome'] == 'reject')
val = sorted(t for t, v in tests.items() if v['outcome'] == 'accept')
nonE = inv + val
status = collections.defaultdict(dict)
for r in d['results']:
    status[r['checker']][r['test']] = r['status']
W = {c: {t for t in inv if status[c].get(t) == 'accepted'} for c in names}
WR = {c: {t for t in val if status[c].get(t) == 'rejected'} for c in names}
DEC = {c: {t for t in nonE if status[c].get(t) in ('declined', 'timeout', 'error')} for c in names}
missing = {c: [t for t in nonE if t not in status[c]] for c in names}
out = {'n_checkers': len(names), 'n_invalid': len(inv), 'n_valid': len(val),
       'checkers_with_missing_results': {c: len(v) for c, v in missing.items() if v}}
# Statistic A
k = {t: sum(1 for c in names if t in W[c]) for t in inv}
S_obs = sum(v * (v - 1) // 2 for v in k.values())
sizes = {c: len(W[c]) for c in names if W[c]}
rng = random.Random(20261121)
cnt = 0; N = 20000; sims = []
for _ in range(N):
    kk = collections.Counter()
    for c, s in sizes.items():
        for t in rng.sample(inv, s): kk[t] += 1
    S = sum(v * (v - 1) // 2 for v in kk.values()); sims.append(S)
    if S >= S_obs: cnt += 1
out['A'] = {'S_obs': S_obs, 'null_mean': float(np.mean(sims)), 'null_p95': float(np.percentile(sims, 95)),
            'p': (cnt + 1) / (N + 1), 'k_by_test': {t: v for t, v in k.items() if v},
            'wrong_accept_set_sizes': sizes}
# Statistic B
def jac(a, b):
    u = a | b
    return len(a & b) / len(u) if u else float('nan')
def stem(c):
    for s in ['nanoclo', 'nanoda', 'nanobruijn', 'nano-lean', 'pestka', 'kefir', 'tenet', 'metalean', 'con-', 'official', 'lean4']:
        if c.startswith(s): return s
    return c
def owner(c):
    m = re.match(r'https?://[^/]+/([^/]+)/', chk[c].get('url', '') or '')
    return m.group(1) if m else None
ne = [c for c in names if W[c]]
pairs = []
for a, b in itertools.combinations(ne, 2):
    sib = (owner(a) is not None and owner(a) == owner(b)) or stem(a) == stem(b)
    pairs.append({'a': a, 'b': b, 'jaccard': jac(W[a], W[b]), 'sibling': bool(sib), 'owner_a': owner(a), 'owner_b': owner(b)})
sibs = [p['jaccard'] for p in pairs if p['sibling']]; non = [p['jaccard'] for p in pairs if not p['sibling']]
out['B'] = {'n_nonempty_checkers': len(ne), 'n_pairs': len(pairs), 'n_sibling_pairs': len(sibs),
            'mean_jaccard_sibling': float(np.mean(sibs)) if sibs else None,
            'mean_jaccard_nonsibling': float(np.mean(non)) if non else None, 'pairs': pairs}
# Statistic C
shipped = ['official', 'official-nightly', 'nanoda', 'lean4lean', 'con-leche', 'con-ron', 'ind-models']
C = {}
for a, b in itertools.combinations(shipped, 2):
    C[f'{a}|{b}'] = {'jaccard': jac(DEC[a], DEC[b]), 'sizes': [len(DEC[a]), len(DEC[b])]}
out['C'] = C
# Statistic D
fail = np.array([[1.0 if (t in W[c] or t in WR[c] or t in DEC[c]) else 0.0 for t in nonE] for c in names])
cov = np.cov(fail)  # checkers x checkers
ev = np.clip(np.linalg.eigvalsh(cov), 0, None)
pr = float(ev.sum() ** 2 / (ev ** 2).sum()) if (ev ** 2).sum() > 0 else float('nan')
out['D'] = {'participation_ratio_all_failures': pr, 'n_checkers_with_any_failure': int((fail.sum(axis=1) > 0).sum())}
# D on wrong-accept only, nonempty checkers
fw = np.array([[1.0 if t in W[c] else 0.0 for t in inv] for c in ne])
ev2 = np.clip(np.linalg.eigvalsh(np.cov(fw)), 0, None)
out['D']['participation_ratio_wrong_accepts_nonempty'] = float(ev2.sum() ** 2 / (ev2 ** 2).sum())
out['D']['n_nonempty'] = len(ne)
# Statistic P1-5: classes of tests accepted by >= 2 checkers
multi = {t: v for t, v in k.items() if v >= 2}
out['multi_accept_tests'] = {t: {'k': v, 'checkers': [c for c in names if t in W[c]], 'desc_first_line': (tests[t].get('description') or '').strip().split('\n')[0][:200]} for t, v in multi.items()}
json.dump(out, open('probe1_results.json', 'w'), indent=1)
print('A: S_obs', S_obs, 'null mean %.2f p95 %.1f p=%.4f' % (out['A']['null_mean'], out['A']['null_p95'], out['A']['p']))
print('   k_by_test', out['A']['k_by_test'])
print('B: nonempty', len(ne), 'pairs', len(pairs), 'sibling pairs', len(sibs), 'mean J sib %s non %s' % (out['B']['mean_jaccard_sibling'], out['B']['mean_jaccard_nonsibling']))
for p in pairs:
    if p['sibling']: print('   sibling', p['a'], p['b'], round(p['jaccard'], 3), p['owner_a'], p['owner_b'])
print('C: declines', {k_: (round(v['jaccard'], 2), v['sizes']) for k_, v in C.items() if v['sizes'][0] or v['sizes'][1]})
print('D:', out['D'])
print('multi-accept tests:'); [print('  ', t, v['k'], v['checkers']) for t, v in out['multi_accept_tests'].items()]
print('missing results:', out['checkers_with_missing_results'])
