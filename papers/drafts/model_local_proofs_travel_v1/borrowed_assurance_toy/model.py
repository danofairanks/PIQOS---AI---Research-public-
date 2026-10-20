"""Toy model: borrowed assurance and the stub-substitution detector.

Plain Python, deterministic, standard library only. See PREREG.md (written first).
"""
import hashlib, json, sys

NOW = 1000


class RealU:
    """Upstream check: a token is current only if its version equals the authority's."""
    def check_current(self, token_version, current_version):
        return token_version == current_version


class StubTrue:
    def check_current(self, token_version, current_version):
        return True


class StubFalse:
    def check_current(self, token_version, current_version):
        return False


def binding(token, payload):
    return hashlib.sha256(json.dumps([token["id"], token["version"], token["action"], payload],
                                     sort_keys=True).encode()).hexdigest()


def bound_ok(token, payload):
    return token["bound"] == binding(token, payload)


def _gate(u, tv, cv):                       # indirection used by A2
    return u.check_current(tv, cv)


class A:        # calls U at the boundary
    def __init__(self, u): self.u = u
    def execute(self, token, payload, current, now):
        if not bound_ok(token, payload): return "BLOCK"
        return "EXECUTE" if self.u.check_current(token["version"], current) else "BLOCK"


class A2(A):    # calls U through a wrapper
    def execute(self, token, payload, current, now):
        if not bound_ok(token, payload): return "BLOCK"
        return "EXECUTE" if _gate(self.u, token["version"], current) else "BLOCK"


class B:        # version is a claim mixed into the binding; never compared to current
    def __init__(self, u): self.u = u
    def execute(self, token, payload, current, now):
        return "EXECUTE" if bound_ok(token, payload) else "BLOCK"


class C:        # no version compare; blocks only on expiry
    def __init__(self, u): self.u = u
    def execute(self, token, payload, current, now):
        if not bound_ok(token, payload): return "BLOCK"
        return "BLOCK" if now >= token["expires_at"] else "EXECUTE"


class D(B):     # same code as B; its own suite has no stale case
    pass


def make_token(version, expires_at, payload="pay:10"):
    t = {"id": "tok1", "version": version, "expires_at": expires_at, "action": "pay"}
    t["bound"] = binding(t, payload)
    return t


CASES = {   # name: (token version, expires_at, authority current, payload presented, expected)
    "F":  (2, NOW + 60, 2, "pay:10", "EXECUTE"),
    "S":  (1, NOW + 60, 2, "pay:10", "BLOCK"),
    "SE": (1, NOW - 1, 2, "pay:10", "BLOCK"),
    "T":  (2, NOW + 60, 2, "pay:99", "BLOCK"),
}
SUITES = {"A": ["F", "S", "SE", "T"], "A2": ["F", "S", "SE", "T"], "B": ["F", "S", "SE", "T"],
          "C": ["F", "S", "SE", "T"], "D": ["F", "T"]}
COMPONENTS = {"A": A, "A2": A2, "B": B, "C": C, "D": D}


def run(comp_name, u, case):
    ver, exp, cur, presented, _ = CASES[case]
    token = make_token(ver, exp)   # bound to original payload "pay:10"
    return COMPONENTS[comp_name](u).execute(token, presented, cur, NOW)


def classify(comp, case):
    real, stub = run(comp, RealU(), case), run(comp, StubTrue(), case)
    if real == "BLOCK" and stub == "EXECUTE": return "DEPENDENT", real, stub
    if real == "EXECUTE" and stub == "EXECUTE": return "BORROWED", real, stub
    if real == "BLOCK" and stub == "BLOCK": return "OTHER-REASON", real, stub
    return "ANOMALY", real, stub


def main():
    u_suite_green = RealU().check_current(1, 1) and not RealU().check_current(1, 2)
    out = {"u_suite": "GREEN" if u_suite_green else "RED", "components": {}}
    for comp in COMPONENTS:
        entry = {"inherited_status": "GREEN (inherits U suite)" if u_suite_green else "RED"}
        suite = SUITES[comp]
        entry["own_suite_results"] = {c: run(comp, RealU(), c) for c in suite}
        entry["own_suite_pass"] = all(run(comp, RealU(), c) == CASES[c][4] for c in suite)
        for case in ("S", "SE"):
            lab, real, stub = classify(comp, case)
            entry["detector_" + case] = {"in_suite": case in suite, "label": lab, "real": real, "stub": stub}
        entry["probe_S_outside_suite"] = run(comp, RealU(), "S")
        entry["control_F_real"] = run(comp, RealU(), "F")
        entry["control_F_alwaysfalse"] = run(comp, StubFalse(), "F")
        if "S" not in suite: entry["verdict"] = "UNREACHED"
        else: entry["verdict"] = entry["detector_S"]["label"]
        out["components"][comp] = entry
    pred = {"A": "DEPENDENT", "A2": "DEPENDENT", "B": "BORROWED", "C": "BORROWED", "D": "UNREACHED"}
    out["prediction_checks"] = {k: (out["components"][k]["verdict"] == v) for k, v in pred.items()}
    out["prediction_checks"]["C_SE_other_reason"] = out["components"]["C"]["detector_SE"]["label"] == "OTHER-REASON"
    out["prediction_checks"]["control_flips_A_A2"] = all(
        out["components"][k]["control_F_real"] != out["components"][k]["control_F_alwaysfalse"] for k in ("A", "A2"))
    out["prediction_checks"]["control_no_flip_B_C_D"] = all(
        out["components"][k]["control_F_real"] == out["components"][k]["control_F_alwaysfalse"] for k in ("B", "C", "D"))
    json.dump(out, open("output.json", "w"), indent=2, sort_keys=True)
    print(json.dumps(out["prediction_checks"], indent=1))
    for k, v in out["components"].items():
        print(k, v["verdict"], "| S real/stub:", v["detector_S"]["real"], v["detector_S"]["stub"],
              "| SE:", v["detector_SE"]["label"], "| own suite pass:", v["own_suite_pass"], "| inherited:", v["inherited_status"])


if __name__ == "__main__":
    main()
