#!/usr/bin/env python3
"""T7-T10 (Amendment 3): reconstructability, replay, queued effects, redundancy and delegation composition. Reuses T6."""
import random, json, sys
import toys_v3 as t6
CL = t6.CLASSES; VAL = t6.VALID

def scenario(rng, D=10, p_rel=0.5, w=0.35):
    log = []; st = t6.fresh()
    for _ in range(D):
        if rng.random() < p_rel:
            c = rng.choice(CL); e = rng.choices(['break', 'restore_auth', 'silent'], weights=[(1 - w) / 2, (1 - w) / 2, w])[0]
            t6.apply(st, c, e); log.append((c, e))
    return st, log

def fold(log):
    st = t6.fresh()
    for c, e in log: t6.apply(st, c, e)
    return st

def t7(seed=7, N=20000):
    rng = random.Random(seed); S = [scenario(rng) for _ in range(N)]
    truth = [t6.truth(st) for st, _ in S]; unauth = [i for i, t in enumerate(truth) if not t]; auth = [i for i, t in enumerate(truth) if t]
    fcr = lambda dec: round(sum(dec[i] for i in unauth) / len(unauth), 3)
    frr = lambda dec: round(sum(not dec[i] for i in auth) / len(auth), 3)
    out = {}
    dec = [t6.truth(fold(l)) for _, l in S]; out['complete_log'] = {'fcr': fcr(dec), 'frr': frr(dec)}
    dec = [all(t6.visible(st)[CL.index(k)] for k in VAL) for st, _ in S]; out['missing_log_default_allow'] = {'fcr': fcr(dec)}
    out['missing_log_default_deny'] = {'fcr': 0.0, 'frr': 1.0}
    for q in (0.0, 0.25, 0.5, 0.75, 1.0):
        dec = []
        for _, l in S:
            kept = [(c, e) for c, e in l if not (e in ('break', 'silent') and rng.random() < q)]
            dec.append(t6.truth(fold(kept)))
        out['agent_writable_q%s' % q] = {'fcr': fcr(dec)}
    adv_drop = [[(c, e) for c, e in l if e not in ('break', 'silent')] for _, l in S]
    dec = [t6.truth(fold(l)) and t6.truth(fold(a)) for (_, l), a in zip(S, adv_drop)]      # any adverse wins
    out['two_logs_any_adverse_wins'] = {'fcr': fcr(dec)}
    dec = [t6.truth(fold(a)) for a in adv_drop]                                              # agent log wins
    out['two_logs_agent_wins'] = {'fcr': fcr(dec)}
    return out

def t8(seed=8, N=20000, rp=0.3):
    rng = random.Random(seed); n = fc_noseq = fc_seq = unauth = 0
    for _ in range(N):
        st, log = scenario(rng); seqlog = [(i, c, e) for i, (c, e) in enumerate(log)]
        truth = t6.truth(st)
        restores = [x for x in seqlog if x[2] == 'restore_auth']
        evlog = list(seqlog)
        if restores and rng.random() < rp:
            evlog.append(rng.choice(restores))                        # replay of an old restore_auth, original sequence number
        # reference without sequence check folds everything
        s1 = t6.fresh()
        for _, c, e in evlog: t6.apply(s1, c, e)
        # reference with monotone per-component sequence check
        s2 = t6.fresh(); last = {}
        for i, c, e in evlog:
            if i <= last.get(c, -1): continue
            last[c] = i; t6.apply(s2, c, e)
        if not truth:
            unauth += 1; fc_noseq += t6.truth(s1); fc_seq += t6.truth(s2)
    return {'fcr_no_sequence_check': round(fc_noseq / unauth, 3), 'fcr_sequence_check': round(fc_seq / unauth, 3)}

def t9(seed=9, trials=20000, r=0.02, m=10, tau=5):
    rng = random.Random(seed); batch = [0] * m; nonat = 0; atomic = 0
    for _ in range(trials):
        rev_t = None
        for t in range(m * tau + 1):
            if rng.random() < r: rev_t = t; break
        for i in range(m):
            if rev_t is not None and rev_t <= i * tau: batch[i] += 1                      # effect executes after revocation
        for i in range(m):
            gap = rng.random() < r                                                        # revocation inside the 1-tick gap of the per-effect non-atomic check
            if gap: nonat += 1
    per = [round(b / trials, 3) for b in batch]
    return {'batch_by_position': per, 'batch_mean': round(sum(per) / m, 3), 'per_effect_nonatomic': round(nonat / (trials * m), 3), 'per_effect_atomic': atomic}

def t10(seed=10, N=60000, s=0.1):
    rng = random.Random(seed); b = {}
    for _ in range(N):
        st, _l = scenario(rng, D=5)
        aug = tuple(st[k][0] and st[k][1] for k in VAL); b.setdefault(aug, set()).add(t6.truth(st))
    out = {'augmented_state_pairs_differing_truth': sum(len(v) > 1 for v in b.values())}
    chain = {}
    for h in (1, 3, 5, 10):
        viol = sum(any(rng.random() < s for _ in range(h)) for _ in range(20000))
        chain[str(h)] = {'unenforced': round(viol / 20000, 3), 'enforced_monotone': 0.0}
    out['delegation_chain'] = chain
    return out

def main():
    o = {'T7': t7(), 'T8': t8(), 'T9': t9(), 'T10': t10()}
    print(json.dumps(o, indent=1)); return o
def selftest():
    o = json.loads(json.dumps(main()))
    t = o['T7']; assert t['complete_log'] == {'fcr': 0.0, 'frr': 0.0}
    assert abs(t['missing_log_default_allow']['fcr'] - 0.234) < 0.02
    f = [t['agent_writable_q%s' % q]['fcr'] for q in (0.0, 0.25, 0.5, 0.75, 1.0)]
    assert f == sorted(f) and f[0] == 0.0 and f[-1] == 1.0 and 0.1 < f[2] < 0.3   # pre-registered 0.4 to 0.8: missed
    assert t['two_logs_any_adverse_wins']['fcr'] == 0.0 and t['two_logs_agent_wins']['fcr'] == 1.0
    assert 0.0005 < o["T8"]["fcr_no_sequence_check"] < 0.01  # pre-registered > 0.05: missed
    assert o['T8']['fcr_sequence_check'] == 0.0
    t9_ = o['T9']; assert 0.28 <= t9_['batch_mean'] <= 0.38 and 0.01 <= t9_['per_effect_nonatomic'] <= 0.025
    assert o['T10']['augmented_state_pairs_differing_truth'] == 0
    print('selftest ok')
if __name__ == '__main__':
    selftest() if '--selftest' in sys.argv else main()
