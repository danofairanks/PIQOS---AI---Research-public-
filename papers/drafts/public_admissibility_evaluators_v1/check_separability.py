#!/usr/bin/env python3
"""Exhaustive finite check of T1-T5 (Appendix A of the paper; statements and predictions were written before the script). Model-local: the statements are true by construction; this verifies the
formalization has no gap at small sizes. Usage: python3 check_separability.py"""
import itertools, json

def gates(O): return [dict(zip(O, bits)) for bits in itertools.product((0, 1), repeat=len(O))]  # 1 = permit
def survive(G, o, D): return all(G[o[r]] == 0 for r in D)
def utility(G, o, P): return all(G[o[r]] == 1 for r in P)

def worlds(nR, nO):
    O = list(range(nO))
    for ov in itertools.product(O, repeat=nR):
        for av in itertools.product((0, 1), repeat=nR):
            yield O, {i: ov[i] for i in range(nR)}, [i for i in range(nR) if av[i] == 1], [i for i in range(nR) if av[i] == 0]

res = {"worlds": 0, "T1_fail": 0, "T2_fail": 0, "T3_fail": 0, "T4_fail": 0, "T4_checked": 0, "witness_worlds_with_survival_and_utility": 0}
for nR in range(1, 6):
    for nO in range(1, 4):
        for O, o, P, D in worlds(nR, nO):
            res["worlds"] += 1
            G = gates(O); sep = not ({o[r] for r in P} & {o[r] for r in D})
            exists = any(survive(g, o, D) and utility(g, o, P) for g in G)
            if exists != sep: res["T1_fail"] += 1
            if exists: res["witness_worlds_with_survival_and_utility"] += 1
            deny = {x: 0 for x in O}; permit = {x: 1 for x in O}
            if not survive(deny, o, D) or (P and utility(deny, o, P)): res["T2_fail"] += 1
            if survive(permit, o, D) != (len(D) == 0): res["T3_fail"] += 1
            if P:
                for g in G:
                    if utility(g, o, P):
                        for p in P:  # extension: one mimic scenario of p with a = 0
                            res["T4_checked"] += 1
                            o2 = dict(o); o2[max(o) + 1] = o[p]
                            if survive(g, o2, D + [max(o) + 1]): res["T4_fail"] += 1
# T5: o = (o1, o2); adversary free on o1, o2 limited to values already in o2(D)
res.update({"T5_worlds": 0, "T5a_fail": 0, "T5b_fail": 0, "T5a_separating_worlds": 0, "T5b_nonseparating_worlds": 0})
for nR in range(1, 6):
    O1, O2 = [0, 1], [0, 1]; O = list(itertools.product(O1, O2))
    for ov in itertools.product(O, repeat=nR):
        for av in itertools.product((0, 1), repeat=nR):
            P = [i for i in range(nR) if av[i]]; D = [i for i in range(nR) if not av[i]]
            if not P or not D: continue
            o = {i: ov[i] for i in range(nR)}; res["T5_worlds"] += 1
            o2P, o2D = {o[r][1] for r in P}, {o[r][1] for r in D}
            # extensions: any scenario with a = 0, o1 any, o2 in o2(D)
            ext = [(a, b) for a in O1 for b in o2D]
            if not (o2P & o2D):
                res["T5a_separating_worlds"] += 1
                g2 = {x: 1 if x[1] in o2P else 0 for x in O}  # gate on o2 only
                ok = utility(g2, o, P) and survive(g2, o, D) and all(g2[e] == 0 for e in ext)
                if not ok: res["T5a_fail"] += 1
            else:
                res["T5b_nonseparating_worlds"] += 1
                shared = next(iter(o2P & o2D)); p = next(r for r in P if o[r][1] == shared)
                mimic = (o[p][0], shared)  # allowed: o1 free, o2 = shared in o2(D)
                assert mimic in ext
                for g in gates(O):
                    if utility(g, o, P) and g[mimic] == 0: res["T5b_fail"] += 1  # a utility gate that denies the mimic would contradict T5b
print(json.dumps(res, indent=1))
