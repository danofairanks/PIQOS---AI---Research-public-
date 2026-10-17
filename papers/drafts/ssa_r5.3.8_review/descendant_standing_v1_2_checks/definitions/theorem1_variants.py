"""VARIANTS of the Theorem 1 check for the definitions pass (see PREREG.md in this folder). Copy of ../theorem1_check/theorem1_check.py with reading switches.
Original docstring: Mechanical check of Theorem 1 (Skrinjar, Descendant Standing Problem v1.2, p.20). See PREREG.md (written before this file).
Stdlib only. Seed and N fixed in PREREG. Prints the PREREG hash so the output ties to it."""
import hashlib, itertools, random, sys, collections, os

SEED, N, CAP = 20261017, 400000, 300
P_KNOB = 0.25
import argparse
ap = argparse.ArgumentParser(); ap.add_argument("--route", default="C", choices=["A","B","C"]); ap.add_argument("--factive", action="store_true"); ap.add_argument("--semvalid", action="store_true")
ARGS = ap.parse_args()
READING = ARGS.route
here = os.path.dirname(os.path.abspath(__file__))
print("PREREG sha256:", hashlib.sha256(open(os.path.join(here, "PREREG.md"), "rb").read()).hexdigest())
print("variant: route=%s factive=%s semvalid=%s" % (ARGS.route, ARGS.factive, ARGS.semvalid))

def least_model(leaf_vals, rules):
    val = dict(leaf_vals)
    changed = True
    while changed:
        changed = False
        for body, head in rules:
            if not val.get(head, False) and all(val.get(b, False) for b in body):
                val[head] = True
                changed = True
    return val

def make_world(rng):
    nr = rng.randint(2, 5); nh = rng.choice([0, 0, 1, 2]); ni = rng.randint(1, 4)
    nl = nr + nh; n = nl + ni + 1; q = n - 1
    knobs = {k: rng.random() < P_KNOB for k in ["i", "ii", "iii", "ivNO", "ivYES", "vroute", "vwit"]}
    if ARGS.factive: knobs["ii"] = knobs["ivNO"] = knobs["ivYES"] = False
    if ARGS.semvalid: knobs["vroute"] = knobs["vwit"] = False
    # true program (acyclic by index order)
    true_rules = []
    for v in range(nl, n):
        for _ in range(rng.randint(1, 3)):
            s = min(rng.randint(1, 3), v)
            body = tuple(sorted(rng.sample(range(v), s)))
            true_rules.append((body, v))
    cur = {l: rng.random() < 0.8 for l in range(nl)}
    wd = {l: cur[l] and rng.random() < 0.65 for l in range(nl)}
    Mcur = least_model({l: cur[l] for l in range(nl)}, true_rules)
    Mwd = least_model({l: wd[l] for l in range(nl)}, true_rules)
    sem = Mwd.get(q, False)
    hidden = set(range(nr, nl))
    # represented rules: (body, head, faithful, complete)
    rep = []
    true_set = set(true_rules)
    for body, head in true_rules:
        if any(b in hidden for b in body):
            if knobs["i"] and rng.random() < 0.6:
                nb = tuple(b for b in body if b not in hidden)
                if nb:
                    rep.append((nb, head, False, rng.random() < 0.5))
            continue
        if rng.random() < 0.85:
            rep.append((body, head, True, rng.random() < 0.85))
    if knobs["iii"]:
        for _ in range(rng.randint(1, 2)):
            head = rng.randint(nl, q)
            pool = [x for x in range(head) if x not in hidden]
            if not pool: continue
            body = tuple(sorted(rng.sample(pool, min(rng.randint(1, 2), len(pool)))))
            if (body, head) in true_set: continue
            rep.append((body, head, False, rng.random() < 0.5))
    if READING == "A":   # complete iff the represented rule is a rule of the true program with the same body (faithful)
        rep = [(b, h, f, bool(f)) for b, h, f, c in rep]
    if READING == "B":   # post-hoc variant: a rule is 'complete' iff it is truth-preserving in both models (route carries q)
        rep = [(b, h, f, all(not (all(Mx.get(x, False) for x in b) and not Mx.get(h, False)) for Mx in (Mcur, Mwd))) for b, h, f, c in rep]
    # audit statuses
    status = {}
    for l in range(nr):
        st = "ACTIVE" if cur[l] else "FAILED"
        if rng.random() < 0.25: st = "UNRESOLVED"
        elif knobs["ii"] and rng.random() < 0.4: st = "FAILED" if st == "ACTIVE" else "ACTIVE"
        status[l] = st
    A = {l for l in status if status[l] == "ACTIVE"}; U = {l for l in status if status[l] == "UNRESOLVED"}
    label = {}
    for l in A:
        ideal = "NO" if wd[l] else "YES"
        lab = "UNRESOLVED" if rng.random() < 0.25 else ideal
        if not wd[l] and knobs["ivNO"] and rng.random() < 0.5: lab = "NO"
        if wd[l] and knobs["ivYES"] and rng.random() < 0.5: lab = "YES"
        label[l] = lab
    # derivations of q over represented rules
    memo = {}
    overflow = [False]
    by_head = collections.defaultdict(list)
    for idx, (b, h, f, c) in enumerate(rep): by_head[h].append(idx)
    def derivs(node):
        if node in memo: return memo[node]
        if node < nr: res = [(frozenset(), frozenset([node]))]
        elif node < nl: res = []
        else:
            res = set()
            for idx in by_head.get(node, []):
                body = rep[idx][0]
                lists = [derivs(b) for b in body]
                if any(len(x) == 0 for x in lists): continue
                for combo in itertools.product(*lists):
                    rs = frozenset().union(*[c[0] for c in combo]) | {idx}
                    ls = frozenset().union(*[c[1] for c in combo])
                    res.add((rs, ls))
                    if len(res) > CAP: overflow[0] = True; break
                if overflow[0]: break
            res = list(res)
        memo[node] = res
        return res
    recs = derivs(q)
    if overflow[0]: return None
    comp = {r: all(rep[i][3] for i in r[0]) for r in recs}
    closed = {}
    for r in recs:
        if comp[r]: closed[r] = rng.random() < 0.7
        else: closed[r] = bool(knobs["vroute"] and rng.random() < 0.5)
    ANO = {l for l in A if label[l] == "NO"}
    seed = U | {l for l in A if label[l] in ("NO", "UNRESOLVED")}
    PASS = any(r[1] <= ANO and closed[r] for r in recs)
    seed_deriv = any(r[1] <= seed for r in recs)
    surv = {l for l in range(nl) if wd[l]}
    wcomp = (not sem) or any(r[1] <= ((A | U) & surv) and comp[r] for r in recs)
    wclosed = (rng.random() < 0.7) if wcomp else bool(knobs["vwit"] and rng.random() < 0.5)
    FAIL = wclosed and not seed_deriv
    overlap_flag = bool(PASS and FAIL)
    CR = "PASS" if PASS else ("FAIL" if FAIL else "UNRESOLVED")
    # premises evaluated directly
    prem = {}
    prem["i"] = not any((not f) and any(True for _ in [0]) and (b, h) not in true_set and False for b, h, f, c in rep)  # placeholder, replaced below
    dropped = [1 for b, h, f, c in rep if (not f) and (b, h) not in true_set and any(tb for tb, th in true_rules if th == h and set(b) <= set(tb) and set(tb) != set(b) and any(x in hidden for x in tb))]
    prem["i"] = not dropped
    prem["ii"] = all((cur[l] if status[l] == "ACTIVE" else (not cur[l]) if status[l] == "FAILED" else True) for l in status)
    prem["iii"] = all(not (all(Mx.get(b, False) for b in body) and not Mx.get(head, False)) for body, head, f, c in rep for Mx in (Mcur, Mwd))
    prem["ivNO"] = all((wd[l] if label[l] == "NO" else True) for l in A)
    prem["ivYES"] = all(((not wd[l]) if label[l] == "YES" else True) for l in A)
    prem["vroute"] = all((comp[r] if closed[r] else True) for r in recs)
    prem["vwit"] = (wcomp if wclosed else True)
    return dict(overlap=overlap_flag, CR=CR, sem=sem, prem=prem, size=n, desc=dict(nr=nr, nh=nh, n=n, true_rules=true_rules, rep=[(b, h, f, c) for b, h, f, c in rep],
        cur=cur, wd=wd, status=status, label=label, recs=[(sorted(r[1]), sorted(r[0]), comp[r], closed[r]) for r in recs], wcomp=wcomp, wclosed=wclosed))

rng = random.Random(SEED)
names = ["i", "ii", "iii", "ivNO", "ivYES", "vroute", "vwit"]
stats = collections.defaultdict(lambda: collections.Counter())
anyviol = collections.defaultdict(lambda: collections.Counter())
examples = {}
skipped = 0
overlaps = 0
under_unres_sem = collections.Counter()
for _ in range(N):
    w = make_world(rng)
    if w is None: skipped += 1; continue
    overlaps += w["overlap"]
    viol = tuple(k for k in names if not w["prem"][k])
    cls = "ALL_HOLD" if not viol else ("ONLY_" + viol[0] if len(viol) == 1 else "MULTI")
    cep = (w["CR"] == "PASS" and not w["sem"]); cef = (w["CR"] == "FAIL" and w["sem"])
    for key, cn in ((cls, stats), ):
        c = cn[key]; c["n"] += 1; c[w["CR"]] += 1; c["CE_PASS"] += cep; c["CE_FAIL"] += cef
        c["sem1"] += w["sem"]
    for k in viol:
        c = anyviol[k]; c["n"] += 1; c[w["CR"]] += 1; c["CE_PASS"] += cep; c["CE_FAIL"] += cef
    if cls == "ALL_HOLD" and w["CR"] == "UNRESOLVED": under_unres_sem[w["sem"]] += 1
    if (cep or cef) and (cls not in examples or w["size"] < examples[cls][0]):
        examples[cls] = (w["size"], w["desc"], "CE_PASS" if cep else "CE_FAIL")
print(f"reading {READING}  seed {SEED}  N {N}  skipped(cap) {skipped}")
print("\nClass table (worlds classified by which premises hold, evaluated directly)")
print(f"{'class':14s} {'n':>8s} {'PASS':>8s} {'FAIL':>8s} {'UNRES':>8s} {'CE_PASS':>8s} {'CE_FAIL':>8s}")
for k in ["ALL_HOLD"] + ["ONLY_" + x for x in names] + ["MULTI"]:
    c = stats.get(k, collections.Counter())
    print(f"{k:14s} {c['n']:8d} {c['PASS']:8d} {c['FAIL']:8d} {c['UNRESOLVED']:8d} {c['CE_PASS']:8d} {c['CE_FAIL']:8d}" + ("   (n<200: untestable)" if 0 < c['n'] < 200 else ("   (n=0)" if c['n']==0 else "")))
print("\nPASS-and-FAIL overlap (Def 13 predicates both true):", overlaps)
print("Premise roles from isolated classes (n<200: empty/analytic under this reading; n>=200 & CE=0: idle; CE>0: load-bearing):")
for k in names:
    c = stats.get("ONLY_" + k, collections.Counter())
    role = "empty/analytic" if c["n"] < 200 else ("load-bearing" if (c["CE_PASS"] + c["CE_FAIL"]) > 0 else "idle")
    print(f"  {k:7s} n={c['n']:6d} CE={c['CE_PASS'] + c['CE_FAIL']:6d} -> {role}")
print("\nPremise violated (any other premises may also be violated)")
for k in names:
    c = anyviol[k]
    print(f"violates {k:7s} n={c['n']:7d}  CE_PASS={c['CE_PASS']:6d}  CE_FAIL={c['CE_FAIL']:6d}")
a = stats["ALL_HOLD"]
print("\nNon-vacuity in ALL_HOLD: PASS %.1f%%  FAIL %.1f%%  UNRESOLVED %.1f%%; SemInd under UNRESOLVED: %s" % (100*a['PASS']/a['n'], 100*a['FAIL']/a['n'], 100*a['UNRESOLVED']/a['n'], dict(under_unres_sem)))
