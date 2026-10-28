import itertools, json, math, random, sys
import numpy as np
from math import comb, log2

def make_formula(n, k, p, rng, units=0):
    cl = set()
    for w in range(2, k+1):
        for vs in itertools.combinations(range(n), w):
            for signs in itertools.product((0, 1), repeat=w):
                if rng.random() < (p if w == k else p*0.05):
                    cl.add(frozenset(zip(vs, signs)))
    for _ in range(units):
        cl.add(frozenset({(rng.randrange(n), rng.randrange(2))}))
    return normalize(cl)

def normalize(cl):
    cl = set(cl); out = set()
    for c in sorted(cl, key=len):
        if not any(o <= c for o in out): out.add(c)
    return out

def select_branch(F, k, M):
    for c in range(2, k+1):
        cnt = {}
        for C in F:
            if len(C) != c: continue
            lits = sorted(C)
            for s in range(1, c):
                for H in itertools.combinations(lits, s):
                    cnt[H] = cnt.get(H, 0) + 1
        valid = [H for H, d in cnt.items() if d >= M**(c-len(H))]
        if valid:
            top = max(len(H) for H in valid)
            Hs = sorted(H for H in valid if len(H) == top)
            return c, frozenset(Hs[0])
    return None

def neg(l): return (l[0], 1-l[1])

def children(F, c, H, marked):
    sel = [C for C in F if len(C) == c and H <= C]
    G = set(F) - set(sel)
    Ps = {C - H for C in sel}
    # child A
    newA = {H}
    FA = {C for C in G if not any(h <= C for h in newA)} | newA
    markedA = {C for C in marked if C in FA and C not in newA} | newA
    # child B
    units = {frozenset({neg(l)}) for l in H}
    newB_units = {u for u in units if u not in F}
    newB = set(Ps) | units
    FB0 = {C for C in G if not any(h <= C for h in newB)}
    FB = FB0 | newB
    markedB = {C for C in marked if C in FB and C not in newB} | set(Ps) | newB_units
    return (FA, markedA, newA, 1), (FB, markedB, newB_units | set(Ps), len(Ps), newB_units, Ps, len(sel))

def sat_vector(F, n, lit_true):
    ok = np.ones(1 << n, dtype=bool)
    for C in F:
        v = np.zeros(1 << n, dtype=bool)
        for l in C: v |= lit_true[l]
        ok &= v
        if not ok.any(): break
    return ok

def run(n, k, M, p, seed, units=0, node_cap=30000, verify_partition=True):
    rng = random.Random(seed)
    F0 = make_formula(n, k, p, rng, units)
    Gam = 2*(3**(k-1)-1); Cc = 4*sum((3*M)**j for j in range(0, k-1))
    Bocc = 2*sum(M**j for j in range(k))
    lit_true = {}
    xs = np.arange(1 << n)
    for v in range(n):
        for s in (0, 1): lit_true[(v, s)] = (((xs >> v) & 1) == s)
    stats = dict(n=n, k=k, M=M, p=p, seed=seed, m0=len(F0), nodes=0, leaves=0, max_depth=0, max_Bchoices=0, A2_violations=0,
                 T_violations=0, depth_viol=0, Bchoice_viol=0, leaf_occ_max=0, leaf_occ_viol=0, new_clause_removed=0, capped=False,
                 max_T=[0]*(k), unit_dup_leaf=0)
    leafsat = np.zeros(1 << n, dtype=np.int32) if verify_partition else None
    stack = [(F0, set(), [0]*k, 0, 0)]     # F, marked, T by width, depth, Bchoices
    while stack:
        F, marked, T, depth, bch = stack.pop()
        stats['nodes'] += 1
        if stats['nodes'] > node_cap: stats['capped'] = True; break
        stats['max_depth'] = max(stats['max_depth'], depth); stats['max_Bchoices'] = max(stats['max_Bchoices'], bch)
        if depth > Cc*n: stats['depth_viol'] += 1
        if bch > Gam*n/M + 1e-9: stats['Bchoice_viol'] += 1
        for j in range(1, k):
            stats['max_T'][j] = max(stats['max_T'][j], T[j])
            if T[j] > 4*(3*M)**(j-1)*n: stats['T_violations'] += 1
        # Lemma A.2 invariant on marked present clauses of width j<k
        cnt = {}
        for C in marked:
            j = len(C)
            if 2 <= j < k:
                lits = sorted(C)
                for i in range(1, j):
                    for S in itertools.combinations(lits, i):
                        cnt[(j, S)] = cnt.get((j, S), 0) + 1
        for (j, S), d in cnt.items():
            if d >= 2*M**(j-len(S)): stats['A2_violations'] += 1
        sel = select_branch(F, k, M)
        if sel is None:
            stats['leaves'] += 1
            occ = {}
            for C in F:
                for (v, s) in C: occ[v] = occ.get(v, 0) + 1
            mo = max(occ.values(), default=0); stats['leaf_occ_max'] = max(stats['leaf_occ_max'], mo)
            if mo > Bocc: stats['leaf_occ_viol'] += 1
            if verify_partition: leafsat += sat_vector(F, n, lit_true)
            continue
        c, H = sel
        (FA, mA, newA, zA), (FB, mB, newB, zB, newunits, Ps, nsel) = children(F, c, H, marked)
        # Lemma A.1 survival of new clauses
        if H not in FA: stats['new_clause_removed'] += 1
        if not (set(Ps) | set(newunits)) <= FB: stats['new_clause_removed'] += 1
        if nsel < M**(c-len(H)): stats['new_clause_removed'] += 1000       # sanity
        TA = list(T); TA[len(H)] += 1
        TB = list(T); TB[c-len(H)] += len(Ps); TB[1] += len(newunits)
        stack.append((FA, mA, TA, depth+1, bch))
        stack.append((FB, mB, TB, depth+1, bch+1))
    if verify_partition and not stats['capped']:
        orig = sat_vector(F0, n, lit_true)
        stats['partition_exact'] = bool(np.array_equal(leafsat, orig.astype(np.int32)))
        stats['count_orig'] = int(orig.sum()); stats['count_leaf_sum'] = int(leafsat.sum())
    stats['node_bound'] = None
    if True:
        stats['node_bound_log2'] = 2*log2(Cc*n+1) + (Gam*n/M)*log2(4*Cc*M)
        stats['nodes_log2'] = log2(max(stats['nodes'], 1))
    stats['C'] = Cc; stats['Gamma'] = Gam; stats['B'] = Bocc
    return stats

def comb_check():
    bad = []
    for k in (3, 4):
        Gam = 2*(3**(k-1)-1)
        for M in (16, 32, 64, 128):
            if M < Gam: continue
            Cc = 4*sum((3*M)**j for j in range(0, k-1))
            for n in range(1, 201):
                a_max = (Gam*n)//M
                s = sum(comb(Cc*n, a) for a in range(a_max+1))
                lhs = log2(s); rhs = (Gam*n/M)*log2(4*Cc*M)
                if lhs > rhs + 1e-9: bad.append((k, M, n, lhs, rhs))
    return bad

if __name__ == "__main__":
    out = []
    specs = [(10, 3, 2, 0.5), (10, 3, 3, 0.5), (11, 3, 4, 0.6), (12, 3, 4, 0.7), (12, 3, 16, 0.9), (12, 3, 16, 0.95), (10, 4, 4, 0.2),
             (9, 3, 2, 0.8), (11, 3, 3, 0.8)]
    for (n, k, M, p) in specs:
        for seed in (1, 2):
            if n == 10 and k == 4: pass
            st = run(n, k, M, p, seed, units=(2 if seed == 2 else 0), node_cap=40000, verify_partition=True)
            out.append(st)
            keys = ['n','k','M','p','seed','m0','nodes','leaves','max_depth','max_Bchoices','A2_violations','T_violations','depth_viol','Bchoice_viol','leaf_occ_max','leaf_occ_viol','new_clause_removed','capped','partition_exact','node_bound_log2','nodes_log2']
            print({kk: (round(st[kk], 2) if isinstance(st.get(kk), float) else st.get(kk)) for kk in keys}, "max_T", st['max_T'][1:], flush=True)
    cb = comb_check(); print("comb inequality failures:", len(cb))
    json.dump(dict(runs=out, comb_failures=cb), open("appendixA_results.json", "w"), indent=1, default=str)
    print("TOTALS: A2_viol", sum(s['A2_violations'] for s in out), "T_viol", sum(s['T_violations'] for s in out), "depth_viol", sum(s['depth_viol'] for s in out),
          "B_viol", sum(s['Bchoice_viol'] for s in out), "leaf_occ_viol", sum(s['leaf_occ_viol'] for s in out), "survival_viol", sum(s['new_clause_removed'] for s in out),
          "partition fails", sum(1 for s in out if s.get('partition_exact') is False), "capped", sum(1 for s in out if s['capped']))
