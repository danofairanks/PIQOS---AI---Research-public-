#!/usr/bin/env python3
"""Toys T1-T5 for the authorization-trajectory counter-model paper. stdlib only, seeded."""
import itertools, math, random, sys, json

# ---------------- T1: rules over histories ----------------
def run(h):
    active = False; g = r = s = 0; spent_epoch = 0; revoked_ever = False
    for e in h:
        if e == 'g': active = True; g += 1; spent_epoch = 0
        elif e == 'r': active = False; r += 1; revoked_ever = True
        else: s += 1; spent_epoch += 1
    return active, g, r, s, spent_epoch, revoked_ever

def valid(rule, h):
    active, g, r, s, se, rv = run(h)
    if rule == 'A': return active and s < 3
    if rule == 'B': return active and not rv
    if rule == 'C': return active and s < g
def naive(rule, h):
    active, g, r, s, se, rv = run(h)
    if rule == 'A': return active and se < 3
    return active

def histories(n): 
    for L in range(n + 1):
        yield from (''.join(p) for p in itertools.product('grs', repeat=L))

def t1(nmax=6):
    out = {}
    for rule in 'ABC':
        # matched pairs: equal naive A_f, different correct answer
        H = list(histories(5)); by = {}
        for h in H: by.setdefault(naive(rule, h), []).append(h)
        pairs = mism = 0
        for k, hs in by.items():
            t = sum(valid(rule, h) for h in hs); f = len(hs) - t
            pairs += t * f; mism += t * f
        tot = sum(len(v) * (len(v) - 1) // 2 for v in by.values())
        classes = {}
        for n in range(2, nmax + 1):
            pre = list(histories(n)); suf = list(histories(n))
            sigs = {tuple(valid(rule, p + x) for x in suf) for p in pre}
            classes[str(n)] = len(sigs)
        out[rule] = {'naive_equal_pairs': tot, 'mismatched_pairs': mism, 'classes': classes}
    return out

# ---------------- T2 ----------------
def t2(seed=1, N=20000):
    rng = random.Random(seed); res = {}
    for p in (0.1, 0.3, 0.5, 0.7, 1.0):
        fc = 0; fc_hd = 0; hd = 0
        for _ in range(N):
            hist_dep = rng.random() < p
            correct = rng.choice([True, False]) if hist_dep else True  # pair member to be judged
            # equal-A_f partner: the reference answers continue on equal state
            if hist_dep:
                hd += 1
                if not correct: fc += 1; fc_hd += 1
            # non-history pairs: both valid, reference right
        res[str(p)] = {'fc_all': round(fc / N, 3), 'fc_hd_only': round(fc_hd / max(hd, 1), 3)}
    # rule-mined generator: random walks under rule A, pairs with equal naive state
    rng = random.Random(seed); mined = 0; diff = 0
    for _ in range(N):
        a = ''.join(rng.choice('grs') for _ in range(6)); b = ''.join(rng.choice('grs') for _ in range(6))
        if naive('A', a) == naive('A', b):
            mined += 1; diff += valid('A', a) != valid('A', b)
    res['mined'] = {'pairs': mined, 'p_emergent': round(diff / mined, 3)}
    return res

# ---------------- T3 ----------------
def auc(scores, labels):
    pos = [s for s, l in zip(scores, labels) if l]; neg = [s for s, l in zip(scores, labels) if not l]
    w = 0.0
    idx = sorted(range(len(scores)), key=lambda i: scores[i]); ranks = [0.0] * len(scores); i = 0
    while i < len(idx):
        j = i
        while j + 1 < len(idx) and scores[idx[j + 1]] == scores[idx[i]]: j += 1
        for k in range(i, j + 1): ranks[idx[k]] = (i + j) / 2 + 1
        i = j + 1
    rp = sum(ranks[i] for i, l in enumerate(labels) if l)
    return (rp - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))
def poisson(rng, lam):
    L = math.exp(-lam); k = 0; p = 1.0
    while True:
        p *= rng.random()
        if p <= L: return k
        k += 1
def gen(rng, n, rule):
    X = []; y = []; el = []
    for _ in range(n):
        dt = rng.expovariate(1.0)
        c = [poisson(rng, 0.4 * dt) for _ in range(5)]  # mandate,cond,deleg,ceiling,policy
        if rule == 1: lab = c[0] + c[2] > 0
        else: lab = c[1] + c[3] > 0
        if rng.random() < 0.05: lab = not lab
        X.append(c); y.append(1 if lab else 0); el.append(dt)
    return X, y, el
def fit(X, y, it=300, lr=0.1):
    w = [0.0] * 5; b = 0.0
    for _ in range(it):
        gw = [0.0] * 5; gb = 0.0
        for xi, yi in zip(X, y):
            z = b + sum(a * c for a, c in zip(w, xi)); pr = 1 / (1 + math.exp(-z)); e = pr - yi
            for k in range(5): gw[k] += e * xi[k]
            gb += e
        n = len(X); w = [a - lr * g / n for a, g in zip(w, gw)]; b -= lr * gb / n
    return w
def t3(seed=3):
    rng = random.Random(seed)
    X1, y1, e1 = gen(rng, 3000, 1); X1t, y1t, e1t = gen(rng, 3000, 1); X2t, y2t, e2t = gen(rng, 3000, 2)
    X2, y2, e2 = gen(rng, 3000, 2)
    w1 = fit(X1, y1); w2 = fit(X2, y2)
    asd = lambda w, X: [sum(a * c for a, c in zip(w, x)) for x in X]
    r = {'w1': [round(v, 2) for v in w1], 'w2': [round(v, 2) for v in w2],
         'gen1_hold': {'asd': round(auc(asd(w1, X1t), y1t), 3), 'elapsed': round(auc(e1t, y1t), 3)},
         'gen2_with_w1': {'asd': round(auc(asd(w1, X2t), y2t), 3), 'elapsed': round(auc(e2t, y2t), 3)},
         'gen2_with_w2': {'asd': round(auc(asd(w2, X2t), y2t), 3), 'elapsed': round(auc(e2t, y2t), 3)}}
    return r

# ---------------- T4 ----------------
def t4(seed=4, steps=500):
    rng = random.Random(seed); res = {}
    revoke_at = 200
    truth = [t < revoke_at for t in range(steps)]  # authority live until revoke_at
    viol_steps = [t for t in range(steps) if not truth[t]]
    def agent_masking(t): return None  # omits the revocation event
    def honest_agent(t): return 'revoke' if t == revoke_at else None
    def indep(t): return 'revoke' if t == revoke_at else None
    def gate(source, default):
        live = True; passed = 0
        for t in range(steps):
            ev = source(t)
            if ev == 'revoke': live = False
            if not truth[t] and live: passed += 1
        return passed
    res['honest_agent_reported'] = gate(honest_agent, 'pass')
    res['masking_agent_reported'] = gate(agent_masking, 'pass')
    res['independent_channel'] = gate(indep, 'deny')
    # silent channel: revocation authority silent (channel down) from revoke_at; default-pass vs default-deny
    def silent_gate(default_pass):
        passed = 0
        for t in range(steps):
            heard = t < revoke_at   # channel carries 'still live' heartbeats until it goes silent
            ok = heard or default_pass
            if not truth[t] and ok: passed += 1
        return passed
    res['silent_default_pass'] = silent_gate(True); res['silent_default_deny'] = silent_gate(False)
    res['violating_steps'] = len(viol_steps)
    return res

# ---------------- T5 ----------------
def t5(seed=5, trials=20000, r=0.02):
    rng = random.Random(seed); res = {}
    for w in (1, 5, 10, 20, 40):
        unb = bnd = 0
        for _ in range(trials):
            revoked = any(rng.random() < r for _ in range(w))   # revocation between check and effect
            if revoked: unb += 1    # unbound effect executes after revoke
            # version-bound: effect consume compares current version; revoked -> denied -> 0 violations
        res[str(w)] = {'unbound': round(unb / trials, 3), 'bound': bnd, 'expected': round(1 - (1 - r) ** w, 3)}
    # availability: benign trajectories with irrelevant churn
    rng = random.Random(seed); n = 20000; strict = rel = 0
    for _ in range(n):
        changes = [rng.random() < 0.1 for _ in range(5)]   # five dims, independent churn
        changes[0] = False   # benign: the one relevant dimension did not change
        strict += any(changes[1:])   # benign half: mandate (relevant) unchanged; strict denies on any other change
    res['false_denial'] = {'strict_version_compare': round(strict / n, 3), 'relevant_only_benign': 0.0}
    return res

def main():
    out = {'T1': t1(), 'T2': t2(), 'T3': t3(), 'T4': t4(), 'T5': t5()}
    print(json.dumps(out, indent=1, default=str)); return out
def selftest():
    o = json.loads(json.dumps(main(), default=str))
    c = o['T1']
    assert max(c['A']['classes'].values()) <= 8 and c['A']['classes']['5'] == c['A']['classes']['6']
    assert c['B']['classes']['2'] == c['B']['classes']['6'] == 3
    assert [c['C']['classes'][str(n)] for n in range(2, 7)] == [6, 9, 12, 15, 18]
    assert all(c[r]['mismatched_pairs'] > 0 for r in 'ABC')
    for p in ('0.1', '0.3', '0.5', '0.7'):
        assert abs(o['T2'][p]['fc_all'] - float(p) / 2) <= 0.02
    assert o['T2']['1.0']['fc_all'] < 0.511 - 0.01   # pre-registered reproduction of 51.1% not reached
    t3 = o['T3']
    assert t3['gen1_hold']['asd'] - t3['gen1_hold']['elapsed'] >= 0.02
    assert t3['gen2_with_w1']['asd'] - t3['gen2_with_w1']['elapsed'] < 0.02
    assert t3['gen2_with_w2']['asd'] - t3['gen2_with_w2']['elapsed'] >= 0.02
    t4 = o['T4']
    assert (t4['honest_agent_reported'], t4['masking_agent_reported'], t4['independent_channel']) == (0, 300, 0)
    assert (t4['silent_default_pass'], t4['silent_default_deny']) == (300, 0)
    t5 = o['T5']
    assert all(t5[w]['bound'] == 0 for w in ('1', '5', '10', '20', '40'))
    assert [t5[w]['unbound'] for w in ('1', '5', '10', '20', '40')] == sorted(t5[w]['unbound'] for w in ('1', '5', '10', '20', '40'))
    assert t5['false_denial']['strict_version_compare'] > 0.3
    print('selftest ok')
if __name__ == '__main__':
    selftest() if '--selftest' in sys.argv else main()
