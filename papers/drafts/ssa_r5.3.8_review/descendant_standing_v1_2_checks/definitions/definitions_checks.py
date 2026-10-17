"""Definitions-pass checks (PREREG.md D1,D4,D5,D6). Stdlib only. Run: python3 -I definitions_checks.py"""
import itertools, random, re, os, hashlib
here = os.path.dirname(os.path.abspath(__file__))
print("PREREG sha256:", hashlib.sha256(open(os.path.join(here, "PREREG.md"), "rb").read()).hexdigest())

# ---- Q: pinned quotes verified against extracted text, with page lookup
# The paper text is not redistributed. Put a plain-text extraction of the PDF at
# ../paper_text.txt (pages delimited by lines "=====PAGE n=====") to run the quote check.
try:
    txt = open(os.path.join(here, "..", "paper_text.txt"), encoding="utf-8").read()
except FileNotFoundError:
    txt = ""
    print("paper text not supplied: quote check skipped")
norm = lambda s: re.sub(r"\s+", " ", s)
pages = [(m.start(), int(m.group(1))) for m in re.finditer(r"=====PAGE (\d+)=====", txt)]
def page_of(pos):
    p = None
    for s, n in pages:
        if s <= pos: p = n
    return p
QUOTES = {
 "D1 Def2 'established' (evidence)": "REMOVED iff the evidence establishes that the declared removal criterion",
 "D1 Def8 label NO": "The label is NO iff it is established that",
 "D1 Def8 UNRESOLVED": "it is UNRESOLVED when the survival status is not established",
 "D1 YES-label gloss": "a YES label means that established current support existed in the witness interpretation",
 "D1 mono. is epistemic": "label monotonicity below remains an explicit epistemic",
 "D2 Def6 RouteComp": "no further undeclared condition is required for that route to carry",
 "D2 Def6 first clause": "is in fact represented in the derivation, is within the declared dependence-audit scope",
 "D2 Def7 distinct": "The ontic property RouteComp and the epistemic certificate RouteClosed",
 "D3 Def6 cert valid": "A route certificate is valid only if no unresolved item in Excl could introduce an omitted",
 "D3 Def10 cert valid": "A witness certificate is valid only if no unresolved item in Excl could supply a semantically surviving",
 "D4 Def15 PASS": "It is PASS iff every load-bearing GateBasis",
 "D4 Def15 FAIL": "no alternative defect-independent basis is relied upon for that gate",
 "D4 Def15 Otherwise": "Otherwise it is UNRESOLVED",
 "D6 SrcFam nonempty": "so SrcFam(l) ≠∅",
 "D6 NO needs one set": "A NO finding needs only one certified sufficient set",
 "D6 YES needs complete": "A YES finding by exhaustion additionally requires the audit to establish",
 "D6 contraction claim": "the support-contractive implication follows immediately",
 "D5 Def17 exclusive": "The four statuses are mutually exclusive on the declared lineage domain",
 "D5 Def14 exhaustive": "The value is defined exhaustively as follows",
}
nt = norm(txt)
print("\n== QUOTES")
for k, q in (QUOTES.items() if txt else []):
    i = nt.find(norm(q))
    if i < 0: print(f"  MISSING  {k}"); continue
    # map back to raw position by searching raw prefix
    raw = txt.find(q.split()[0] + " " + q.split()[1]) if False else None
    first = norm(q)[:40]
    # find page via raw regex tolerant of whitespace
    pat = re.compile(r"\s+".join(map(re.escape, q.split())))
    m = pat.search(txt)
    print(f"  OK p.{page_of(m.start()) if m else '?'}  {k}  ({len(q.split())} words)")

# ---- D5: exhaustive partition checks
print("\n== D5 partitions")
# Def 14: Valid in {1,0,bot}. Struct in {1,0,U}, gates each in {sat,fail,unres}, 0..2 gates
def valid_def14(struct, gates):
    one = struct == 1 and all(g == "sat" for g in gates)
    zero = struct == 0 or any(g == "fail" for g in gates)
    return one, zero
bad = 0; n = 0
for struct in (1, 0, "U"):
    for k in range(0, 4):
        for gates in itertools.product(("sat", "fail", "unres"), repeat=k):
            one, zero = valid_def14(struct, gates); n += 1
            if one and zero: bad += 1; print("  overlap", struct, gates)
print(f"  Def14: {n} configs, 1&0 overlaps={bad}; bot is residual by definition (exhaustive by 'otherwise')")
# Def 17 / 16 over candidate witness states: DValid in {1,0,bot}, CR in {PASS,FAIL,UNRES}; claim closure flag; PNew = is P==P- and old witness
states = list(itertools.product((1, 0, "bot"), ("PASS", "FAIL", "UNRES")))
over16 = gap16 = over17 = 0; tot = 0
for m in range(1, 4):
    for cands in itertools.combinations_with_replacement(states, m):
        for closed in (0, 1):
            tot += 1
            est = any(d == 1 and c == "PASS" for d, c in cands)
            allres = all(d != "bot" for d, c in cands)
            dfd = closed == 1 and allres and all(d == 0 or (d == 1 and c == "FAIL") for d, c in cands)
            unres = not est and not dfd
            if est and dfd: over16 += 1
            # Def 17 w/ lineage: carried needs old witness in cands with DValid1 PASS and P==P-
            for old_idx in range(m):
                for same in (0, 1):
                    od, oc = cands[old_idx]
                    carried = same == 1 and od == 1 and oc == "PASS"
                    reest = (not carried) and est
                    defeated = dfd
                    nflags = carried + reest + defeated
                    # ordered cases make the status unique; check whether conditions themselves overlap
                    if carried and defeated or reest and defeated: over17 += 1
print(f"  Def16: {tot} states, ESTABLISHED&DEFEATED overlaps={over16}; UNRESOLVED = complement by construction")
print(f"  Def17: DEFEATED overlaps with CARRIED/REESTABLISHED conditions={over17} (the 'ordered' cases are then not needed for exclusivity)")
# Def 13 PASS/FAIL: PASS: d with Leaves ⊆ A_NO; FAIL: no d with Leaves ⊆ Seed_<=?  Overlap iff A_NO ⊆ Seed false
print("  Def13: PASS&FAIL exclusivity depends on NO-labelled active leaves being inside the seed set; tested in theorem1_variants.py (overlap counter), not here.")

# ---- D4: Def 15 enumeration
print("\n== D4 Def15 GateInd as printed")
# a witness relies on a set of load-bearing bases; each basis status: surv (established survive), fail (established not survive), unres
# 'alternative' reading (X): the surviving basis is an alternative to the failing one for the SAME gate. (Y): any other relied-upon surviving basis counts.
def gateind(bases):  # bases: list of (gate_id, status)
    pas = all(s == "surv" for g, s in bases)
    fails = [g for g, s in bases if s == "fail"]
    fail_X = any(not any(g2 == g and s2 == "surv" for g2, s2 in bases) for g in fails)  # no surviving alternative for that gate
    fail_Y = bool(fails) and not any(s == "surv" for g, s in bases)
    return pas, fail_X, fail_Y
gaps = []
for k in (1, 2, 3):
    for gates in itertools.product((0, 1), repeat=k):
        for st in itertools.product(("surv", "fail", "unres"), repeat=k):
            bases = list(zip(gates, st))
            if any(s == "unres" for _, s in bases): continue  # resolved-only
            pas, fx, fy = gateind(bases)
            if not pas and not fx: gaps.append((bases, "gap under X (resolved bases, neither PASS nor FAIL)"))
print(f"  resolved configs with GateInd=UNRESOLVED under reading X (alternative = same gate): {len(gaps)}")
for b, _ in gaps[:6]: print("   ", b)
mixed_same_gate = [b for b, _ in gaps if len({g for g,_ in b}) == 1]
print(f"  of which single-gate (fail+surv on the SAME gate; arguably 'alternative basis' => FAIL not warranted): {len(mixed_same_gate)}")
multi = [b for b, _ in gaps if len({g for g,_ in b}) > 1]
print(f"  multi-gate gaps (failing gate A, surviving gate B, bases fully resolved, GateInd printed = UNRESOLVED): {len(multi)}")
for b in multi[:4]: print("   ", b)
print("  Under reading Y (any surviving relied-upon basis blocks FAIL) the gap count is",
      sum(1 for k in (1,2,3) for gates in itertools.product((0,1),repeat=k) for st in itertools.product(("surv","fail"),repeat=k)
          if not gateind(list(zip(gates,st)))[0] and not gateind(list(zip(gates,st)))[2]))

# ---- D6: SrcFam
print("\n== D6 SrcFam")
rng = random.Random(20261017)
univ = ["D1", "D2", "D3", "D4", "D5"]
def label(fam, delta, complete=True):
    if any(not (set(S) & delta) for S in fam): return "NO"
    return "YES" if complete else "UNRESOLVED"
rank = {"NO": 0, "UNRESOLVED": 1, "YES": 2}
viol_c = viol_m = trials = viol_empty = 0
for _ in range(100000):
    k = rng.randint(1, 4)
    fam = [set(rng.sample(univ, rng.randint(0, 3))) for _ in range(k)]
    complete = rng.random() < 0.7
    big = set(rng.sample(univ, rng.randint(0, 5)))
    small = set(x for x in big if rng.random() < 0.5)
    trials += 1
    if label(fam, big, complete) == "NO" and label(fam, small, complete) != "NO": viol_c += 1       # contraction
    if rank[label(fam, small, complete)] > rank[label(fam, big, complete)]: viol_m += 1            # monotone
    if label(fam, set(), complete) != "NO" and any(len(S) == 0 for S in fam): viol_empty += 1
    # at empty delta: nonempty family => survives only if some set disjoint from empty = any set => NO. but empty-set member needs 'independent warrant'
print(f"  trials={trials} contraction violations={viol_c} monotonicity violations={viol_m}")
fam = [{"D1"}, {"D2", "D3"}]
print("  micro-example: Δ={D1} ->", label(fam, {"D1"}), "; Δ={D1,D2} ->", label(fam, {"D1", "D2"}))
print("  empty-Δ always NO for nonempty family:", all(label([set(rng.sample(univ, rng.randint(0, 3)))], set()) == "NO" for _ in range(1000)))
