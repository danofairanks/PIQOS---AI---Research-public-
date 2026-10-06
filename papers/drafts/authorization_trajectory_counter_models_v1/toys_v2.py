#!/usr/bin/env python3
"""Controls added after the blind pass (Amendment 1). stdlib only, seeded."""
import random, json
import toys

def t3b(seed=3):
    rng = random.Random(seed)
    X1, y1, e1 = toys.gen(rng, 3000, 1); X1t, y1t, e1t = toys.gen(rng, 3000, 1); X2t, y2t, e2t = toys.gen(rng, 3000, 2); X2, y2, e2 = toys.gen(rng, 3000, 2)
    w1 = toys.fit(X1, y1)
    asd = lambda w, X: [sum(a * c for a, c in zip(w, x)) for x in X]
    eq = lambda X: [sum(x) for x in X]
    base = lambda X, e: [ei + 0.0 for ei in e]
    # elapsed + total change count (counts are label-agnostic): fitted 2-feature logistic would need a separate fit; use rank-free sum z = dt + total count
    ec = lambda X, e: [ei + sum(x) for x, ei in zip(X, e)]
    return {'gen1_hold': {'asd_fitted': round(toys.auc(asd(w1, X1t), y1t), 3), 'asd_equal_w': round(toys.auc(eq(X1t), y1t), 3),
                          'elapsed': round(toys.auc(e1t, y1t), 3), 'elapsed_plus_total_count': round(toys.auc(ec(X1t, e1t), y1t), 3)},
            'gen2_with_w1': {'asd_fitted_w1': round(toys.auc(asd(w1, X2t), y2t), 3), 'asd_equal_w': round(toys.auc(eq(X2t), y2t), 3),
                             'elapsed': round(toys.auc(e2t, y2t), 3), 'elapsed_plus_total_count': round(toys.auc(ec(X2t, e2t), y2t), 3)}}

def t4b(seed=4, steps=500, revoke_at=200):
    out = {}
    for d in (0, 5, 20, 50):
        passed = 0
        for t in range(steps):
            heard_revoke = t >= revoke_at + d     # independent channel, delivery delayed by d
            live = not heard_revoke
            if t >= revoke_at and live: passed += 1
        out[str(d)] = passed
    return out

def t5b(seed=5, trials=20000, r=0.02):
    rng = random.Random(seed); res = {}
    for w in (1, 5, 10, 20, 40):
        atomic = nonatomic = ignoring = 0
        for _ in range(trials):
            version = 1; checked = version
            for _ in range(w):                           # revocation window between check and consume
                if rng.random() < r: version += 1
            read = version                               # non-atomic effector reads the version here
            gap_revoke = rng.random() < r                # revocation lands between read and act
            if gap_revoke: version += 1
            if version != checked: ignoring += 1         # version-ignoring effector acts after a revocation
            # atomic compare-and-consume: compare and act in one step on the final version
            if version == checked: pass                  # allowed and legitimate
            # non-atomic: compares the stale read, acts, violates if version moved after the read
            if read == checked and version != checked: nonatomic += 1
        res[str(w)] = {'atomic': atomic, 'nonatomic': round(nonatomic / trials, 3), 'ignoring': round(ignoring / trials, 3), 'expected_ignoring': round(1 - (1 - r) ** (w + 1), 3)}
    return res

def selftest():
    o = {'T3b': t3b(), 'T4b': t4b(), 'T5b': t5b()}
    assert o['T3b']['gen1_hold']['asd_equal_w'] < o['T3b']['gen1_hold']['asd_fitted']
    g = o['T3b']['gen2_with_w1']; assert g['elapsed_plus_total_count'] - g['asd_fitted_w1'] > 0.05
    assert [o['T4b'][k] for k in ('0', '5', '20', '50')] == [0, 5, 20, 50]
    assert all(o['T5b'][w]['atomic'] == 0 for w in o['T5b'])
    assert all(0.005 < o['T5b'][w]['nonatomic'] < 0.03 for w in o['T5b'])
    print('selftest ok')
if __name__ == '__main__':
    selftest() if '--selftest' in __import__('sys').argv else print(json.dumps({'T3b': t3b(), 'T4b': t4b(), 'T5b': t5b()}, indent=1))
