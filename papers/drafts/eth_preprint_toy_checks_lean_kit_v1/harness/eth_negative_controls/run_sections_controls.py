import sys, os, json, functools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "negative_controls"))
import sections_decoy as sd
S = sd.S
calls = {"Z_rep_ring": 0, "brute_H_ring": 0}
oz, ob = S.Z_rep_ring, S.brute_H_ring
def z(*a, **k): calls["Z_rep_ring"] += 1; return oz(*a, **k)
def b(*a, **k): calls["brute_H_ring"] += 1; return ob(*a, **k)
S.Z_rep_ring, S.brute_H_ring = z, b
decoy = sd.make_decoy_run_system()
systems = {
    "unsat": [[(0,), ()], [(0,)]], "A": [[(0, 1), (2,)], [(1, 3), (0,), ()]], "B": [[(0, 1, 2), (3,)], [(0, 3), (1,)]],
    "C": [[(0, 1), (2, 3)], [(0, 2), (1, 3), ()]], "D": [[(0, 1), (1, 2), (3,)], [(0, 3)], [(2, 3), (0,)]],
    "E": [[(0,), (1,), (2,)], [(0, 1), (2, 3), (1, 3)]],
}
KEYS = ["N", "N_pipeline", "N_correct", "S_equal", "per_V_coef_equal", "taylor_equals_bruteforce", "hermite_ok", "deg_ok", "bound_ok"]
out = {"real": [], "decoy": []}
for kind, fn in (("real", S.run_system), ("decoy", decoy)):
    for nm, eqs in systems.items():
        calls["Z_rep_ring"] = calls["brute_H_ring"] = 0
        rec = fn(nm, 4, eqs, seed=sum(map(ord, nm)) % 1000)
        row = {k: rec.get(k) for k in KEYS}
        row.update(name=nm, vectors_examined=rec.get("vectors_examined"), probe=dict(calls))
        out[kind].append(row)
        print(kind, json.dumps(row), flush=True)
json.dump(out, open(os.path.join(HERE, "controls_sections_results.json"), "w"), indent=1, default=str)
