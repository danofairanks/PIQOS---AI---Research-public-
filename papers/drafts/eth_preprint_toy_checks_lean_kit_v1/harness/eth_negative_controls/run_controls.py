"""D1/D1b/D4 run (see PREREG.md). python3 -I run_controls.py"""
import sys, os, json, time, functools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "negative_controls"))
sys.path.insert(0, os.path.join(HERE, "..", "eth_counter_test"))
import eth_counter as ec
import run_tests as rt
import decoy_counter as dc

PROBE = {"brute_H": [], "Z": 0, "count_sat": []}

def caller():
    return sys._getframe(2).f_code.co_name

def wrap_probe():
    orig_brute, orig_Z, orig_cs = ec.Counter.brute_H, ec.Counter.Z, ec.count_sat
    @functools.wraps(orig_brute)
    def brute(self, *a, **k):
        PROBE["brute_H"].append(caller()); return orig_brute(self, *a, **k)
    @functools.wraps(orig_Z)
    def Zw(self, *a, **k):
        PROBE["Z"] += 1; return orig_Z(self, *a, **k)
    @functools.wraps(orig_cs)
    def cs(*a, **k):
        PROBE["count_sat"].append(sys._getframe(1).f_code.co_name); return orig_cs(*a, **k)
    ec.Counter.brute_H, ec.Counter.Z = brute, Zw
    ec.count_sat = cs; rt.count_sat = cs
    return orig_brute, orig_Z, orig_cs

def reset():
    PROBE["brute_H"].clear(); PROBE["count_sat"].clear(); PROBE["Z"] = 0

def d4_flag(callers):
    return any(c in ("taylor_decoupled", "design_at") for c in callers)

FIELDS = ["H(0)==#F", "deg_H<=occ*(R-1)", "L2_hermite_from_brute_ok", "Q*J>3nR", "L3_decoupled_matches_brute_taylor",
          "L4_count_correct", "design_violations(2.5)"]

def run_cfg(CounterCls, name, cfgs, seeds):
    rt.Counter = CounterCls
    rows = []
    for (r, Q, R, n, m) in cfgs:
        cons = ec.Construction(r, Q, R)
        for s in range(seeds):
            reset()
            t0 = time.time()
            res = rt.run_case(cons, n, m, 1000 + s, do_decoupled=True, verbose=False)
            row = {"cls": name, "cfg": [r, Q, R, n, m], "seed": 1000 + s,
                   "fields": {f: res.get(f) for f in FIELDS}, "truth": res["truth"], "L4_count": res.get("L4_count"),
                   "self_reported": res.get("counters"), "seconds": round(time.time() - t0, 2),
                   "probe": {"brute_H_callers": list(PROBE["brute_H"]), "count_sat_callers": list(PROBE["count_sat"]), "Z_calls": PROBE["Z"]}}
            row["d4_flag"] = d4_flag(PROBE["brute_H"] + PROBE["count_sat"])
            row["correct"] = bool(res["H(0)==#F"] and res["L2_hermite_from_brute_ok"] and res.get("L3_decoupled_matches_brute_taylor")
                                  and res.get("L4_count_correct") and res.get("design_violations(2.5)") == 0)
            rows.append(row)
    return rows

if __name__ == "__main__":
    cfgs = [(2, 3, 2, 4, 5), (2, 3, 3, 4, 5), (3, 2, 2, 4, 5)]
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    wrap_probe()
    out = {}
    for name, cls in [("real", ec.Counter), ("D1", dc.DecoyCounter), ("D1b", dc.DecoyCounterB), ("D1c_posthoc", dc.DecoyCounterC)]:
        rows = run_cfg(cls, name, cfgs, seeds)
        out[name] = rows
        print(name, "cases", len(rows), "correct", sum(r["correct"] for r in rows), "d4_flag", sum(r["d4_flag"] for r in rows),
              "mean_Z_calls", sum(r["probe"]["Z_calls"] for r in rows) / len(rows), "mean_seconds", round(sum(r["seconds"] for r in rows) / len(rows), 2), flush=True)
    json.dump(out, open("controls_D1_results.json", "w"), indent=1, default=str)
