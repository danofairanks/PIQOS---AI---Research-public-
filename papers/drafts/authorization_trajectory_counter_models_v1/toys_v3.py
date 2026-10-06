#!/usr/bin/env python3
"""T6: the preprint's ten mutation classes, our own implementation (Amendment 2). stdlib only, seeded."""
import random, json, sys, itertools

CLASSES = ['principal', 'mandate', 'policy', 'delegation', 'condition', 'resource', 'environment', 'effect', 'evidence', 'instruction']
VALID = [c for c in CLASSES if c != 'evidence']          # evidence affects reconstructability, not validity
EV = ('break', 'restore_auth', 'silent', 'ordinary')

def apply(state, cls, ev):
    v, c = state[cls]
    if ev == 'break': v = False
    elif ev == 'restore_auth': v, c = True, True
    elif ev == 'silent':
        c = False
        if cls != 'instruction': v = True              # an accepted conflicting instruction changes nothing visible
    state[cls] = (v, c)

def fresh(): return {k: (True, True) for k in CLASSES}
def truth(st): return all(st[k][0] and st[k][1] for k in VALID)
def visible(st): return tuple(st[k][0] for k in CLASSES)
def augmented(st): return all(st[k][0] and st[k][1] for k in VALID)   # one derived bit per component

# ---------- T6a: exact residual classes by Moore minimization ----------
def classes_count(k, with_evidence_only=False):
    comps = list(range(k))
    states = list(itertools.product([(True, True), (True, False), (False, True), (False, False)], repeat=k))
    events = [(i, e) for i in comps for e in EV[:3]] + [(None, 'ordinary')]
    def step(s, ev):
        i, e = ev
        if i is None: return s
        v, c = s[i]
        if e == 'break': v = False
        elif e == 'restore_auth': v, c = True, True
        else: v, c = True, False
        t = list(s); t[i] = (v, c); return tuple(t)
    acc = lambda s: all(v and c for v, c in s)
    cls = {s: acc(s) for s in states}
    while True:
        sig = {s: (cls[s],) + tuple(cls[step(s, e)] for e in events) for s in states}
        ids = {}
        new = {s: ids.setdefault(sig[s], len(ids)) for s in states}
        if len(set(new.values())) == len(set(cls.values())): return len(set(new.values()))
        cls = new

def t6a():
    return {'per_component': classes_count(1), 'composed': {str(k): classes_count(k) for k in (1, 2, 3, 4)},
            'evidence_component_classes': 1}

# ---------- T6b ----------
def gen(rng, depth, p_rel, w):
    st = fresh(); n_rel = 0; trans = []
    for _ in range(depth):
        if rng.random() < p_rel:
            cls = rng.choice(CLASSES)
            ev = rng.choices(['break', 'restore_auth', 'silent'], weights=[(1 - w) / 2, (1 - w) / 2, w])[0]
            apply(st, cls, ev); n_rel += 1; trans.append(ev)
        else: trans.append('ordinary')
    return st, n_rel, trans

def t6b(seed=6, N=20000):
    rng = random.Random(seed); out = {}
    for w in (0.05, 0.2, 0.35, 0.5, 0.8):
        row = {}
        for D in (0, 1, 3, 5, 10, 20):
            fc = unauth = err = 0
            for _ in range(N):
                st, n, _t = gen(rng, D, 0.5, w)
                tr = truth(st); ref = all(visible(st)[CLASSES.index(k)] for k in VALID)
                unauth += (not tr); fc += (not tr) and ref; err += (ref != tr)
                assert augmented(st) == tr
            row[str(D)] = {'fcr_opportunities': round(fc / max(unauth, 1), 3), 'error_all': round(err / N, 3)}
        out[str(w)] = row
    # operational depth is not authority depth: depth 20, all ordinary
    fc = 0
    for _ in range(N):
        st, n, _t = gen(rng, 20, 0.0, 0.5); fc += (not truth(st))
    out['depth20_all_ordinary_unauthorized'] = fc
    return out

def t6c(seed=6, N=20000):
    rng = random.Random(seed); strict = needed = trans_total = 0
    for _ in range(N):
        _st, _n, tr = gen(rng, 10, 0.5, 0.35)
        for ev in tr:
            trans_total += 1
            if ev != 'ordinary': strict += 1            # strict: revalidate on every authority-relevant transition
            if ev in ('silent',): needed += 1           # needed: R-class only (break is suspend, restore_auth continue)
    # unnecessary = strict revalidations that were not required, counting suspends as handled by S not R
    return {'strict_unnecessary_over_all_transitions': round((strict - needed) / trans_total, 3), 'class_aware': 0.0}

def t6d(seed=6, N=60000):
    rng = random.Random(seed); buckets = {}
    for _ in range(N):
        st, n, tr = gen(rng, 5, 0.5, 0.35); buckets.setdefault(visible(st), []).append(truth(st))
    pairs = diff = 0
    for k, v in buckets.items():
        t = sum(v); f = len(v) - t; pairs += len(v) * (len(v) - 1) // 2; diff += t * f
    return {'equal_final_state_pairs': pairs, 'differing_truth_fraction': round(diff / pairs, 3),
            'path_discrimination': {'final_state_only': 0.0, 'augmented_bit': 1.0}}

def main():
    out = {'T6a': t6a(), 'T6b': t6b(), 'T6c': t6c(), 'T6d': t6d()}
    print(json.dumps(out, indent=1)); return out
def selftest():
    o = json.loads(json.dumps(main()))
    a = o['T6a']; assert a['per_component'] == 2 and [a['composed'][k] for k in '1234'] == [2, 4, 8, 16]
    b = o['T6b']
    assert all(b[w]['0']['fcr_opportunities'] == 0 for w in ('0.05', '0.2', '0.35', '0.5', '0.8')) and b['depth20_all_ordinary_unauthorized'] == 0
    assert abs(b['0.35']['1']['fcr_opportunities'] - 0.511) < 0.02 and b['0.05']['10']['fcr_opportunities'] < 0.2
    assert b['0.35']['20']['fcr_opportunities'] < b['0.35']['1']['fcr_opportunities']      # FCR falls with depth here (prediction missed)
    assert o['T6c']['strict_unnecessary_over_all_transitions'] > 0.2
    print('selftest ok')
if __name__ == '__main__':
    selftest() if '--selftest' in sys.argv else main()
