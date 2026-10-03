#!/usr/bin/env python3
"""Round 3: attack ideas from a second model family's re-implementation attempt, built as simulations with controls.
Companion to ../pre_execution_gate_counter_models_v1.md (section 6a). Observables and predictions were fixed before this file was written.
Rules: outcomes are computed by running mechanisms; counters are incremented inside the functions they
count; a control that must be 0 and is not marks the toy TOY-BROKEN; each toy has a mutation check.
stdlib only. Usage: python3 gate_round3.py [--selftest]
"""
import itertools
import json
import random
import sys


# ---------------- R3-A: check-to-use gap ----------------
class World:
    def __init__(self):
        self.latent_violating = False


def r3a(mode, w, q=0.0, eps=0.0, trials=2000, seed=31):
    rng = random.Random(seed)
    executed_violating = executed = flipped = 0
    for _ in range(trials):
        world = World()
        probe = lambda: (not world.latent_violating) or (rng.random() < eps)    # True = "safe"; misses with prob eps
        if mode == "ATOMIC":                              # probe and effect in one step: nothing can intervene
            if probe():
                executed += 1
                executed_violating += world.latent_violating
            continue
        passed = probe()
        if not passed:
            continue
        for step in range(w):                             # intervening steps between probe and effect
            if mode == "NON_ATOMIC_ADVERSARIAL":
                world.latent_violating = True             # governed side flips right after a passing probe
            elif mode in ("NON_ATOMIC_RANDOM", "RECHECK") and rng.random() < q:
                world.latent_violating = True
        flipped += world.latent_violating
        if mode == "RECHECK" and not probe():
            continue                                      # re-probe at execution time
        executed += 1
        executed_violating += world.latent_violating
    return {"executed": executed, "executed_violating": executed_violating,
            "violating_fraction": round(executed_violating / trials, 3), "flipped_trials": flipped}


def r3a_all():
    out = {
        "ADVERSARIAL_w5": r3a("NON_ATOMIC_ADVERSARIAL", 5),
        "RANDOM_q0.1_w5": r3a("NON_ATOMIC_RANDOM", 5, q=0.1),
        "RANDOM_q0_w5": r3a("NON_ATOMIC_RANDOM", 5, q=0.0),
        "RANDOM_q0.1_w0": r3a("NON_ATOMIC_RANDOM", 0, q=0.1),
        "ATOMIC_adversarial_irrelevant": r3a("ATOMIC", 5),
        "RECHECK_q0.1_w5_eps0": r3a("RECHECK", 5, q=0.1, eps=0.0),
        "RECHECK_q0.1_w5_eps0.05": r3a("RECHECK", 5, q=0.1, eps=0.05),
        "MUTATION_adversarial_w0": r3a("NON_ATOMIC_ADVERSARIAL", 0),
    }
    controls_zero = (out["ATOMIC_adversarial_irrelevant"]["executed_violating"] == 0
                     and out["RECHECK_q0.1_w5_eps0"]["executed_violating"] == 0
                     and out["MUTATION_adversarial_w0"]["executed_violating"] == 0
                     and out["RANDOM_q0_w5"]["executed_violating"] == 0)
    attack = out["ADVERSARIAL_w5"]["violating_fraction"] > 0.9 and out["RANDOM_q0.1_w5"]["violating_fraction"] > 0.2
    out["status"] = "TOY-BROKEN" if not controls_zero else ("ATTACK-SUCCEEDS" if attack else "ATTACK-FAILS")
    return out


# ---------------- R3-B: trace semantic aliasing ----------------
def make_real(hostile):
    # edge: (src, dst, effect); effect is invisible in the state trace
    return [("s0", "s1", None), ("s1", "s2", None), ("s2", "done", "delete" if hostile else "log")]


def walk_traces(edges, instrumented, walks=50, seed=5):
    rng = random.Random(seed)
    nxt = {}
    for e in edges:
        nxt.setdefault(e[0], []).append(e)
    observed = set()
    for _ in range(walks):
        u = "s0"
        while u in nxt:
            e = rng.choice(nxt[u])
            observed.add((e[0], e[1], e[2] if instrumented else None))
            u = e[1]
    return observed


def r3b():
    prohibited_effect = "delete"
    res = {}
    for name, hostile in (("benign", False), ("hostile", True)):
        real = make_real(hostile)
        real_has_prohibited = any(e[2] == prohibited_effect for e in real)
        for kind, instr in (("topology_only", False), ("effect_instrumented", True)):
            model = walk_traces(real, instr)
            proof_holds = not any(e[2] == prohibited_effect for e in model)     # "no prohibited effect" over the model
            res[f"{name}/{kind}"] = {"proof_holds": proof_holds, "real_has_prohibited": real_has_prohibited,
                                     "defeated": proof_holds and real_has_prohibited}
    same_topology_models = (walk_traces(make_real(False), False) == walk_traces(make_real(True), False))
    controls_ok = (not res["benign/topology_only"]["defeated"] and not res["benign/effect_instrumented"]["defeated"]
                   and not res["hostile/effect_instrumented"]["defeated"])
    attack = res["hostile/topology_only"]["defeated"] and same_topology_models
    return {"worlds": res, "topology_only_models_identical": same_topology_models,
            "status": "TOY-BROKEN" if not controls_ok else ("ATTACK-SUCCEEDS" if attack else "ATTACK-FAILS")}


# ---------------- R3-C: dynamic dispatch after enumeration ----------------
EXECUTOR_SEMANTICS = {"delete": "DELETE", "rm": "DELETE", "unlink": "DELETE", "remove": "DELETE", "zap": "DELETE",
                      "read": "READ", "write": "WRITE", "list": "READ", "stat": "READ", "copy": "WRITE"}
KNOWN_NAMES = {"delete"}
KNOWN_ALIASES = {"delete", "rm", "unlink", "remove"}          # normalizer's alias map (not "zap")
ALLOWLIST = {"read", "write", "list"}


def gate_allows(policy, name):
    if policy == "BLACKLIST_ENUM":
        return name not in KNOWN_NAMES
    if policy == "BLACKLIST_NORMALIZED":
        return name not in KNOWN_ALIASES
    return name in ALLOWLIST                                    # ALLOWLIST: default deny


def r3c(only_canonical=False, novel_legit_rate=0.0, n=2000, seed=41):
    rng = random.Random(seed)
    acts = []
    for _ in range(n):
        u = rng.random()
        if u < 0.8:
            if rng.random() < novel_legit_rate:
                acts.append(rng.choice(["stat", "copy"]))          # legitimate actions not enumerated in the allowlist
            else:
                acts.append(rng.choice(["read", "write", "list"]))
        elif only_canonical:
            acts.append("delete")
        else:
            acts.append(rng.choice(["delete", "rm", "unlink", "remove", "zap"]))
    out = {}
    for policy in ("BLACKLIST_ENUM", "BLACKLIST_NORMALIZED", "ALLOWLIST"):
        prohibited_exec = legit_blocked = 0
        for a in acts:
            if gate_allows(policy, a):
                prohibited_exec += EXECUTOR_SEMANTICS[a] == "DELETE"
            else:
                legit_blocked += EXECUTOR_SEMANTICS[a] != "DELETE"
        out[policy] = {"prohibited_executed": prohibited_exec, "legit_blocked": legit_blocked}
    return out


def r3c_all():
    attack = r3c()
    mutation = r3c(only_canonical=True)
    with_novel = r3c(novel_legit_rate=0.1)
    ok_ctrl = attack["ALLOWLIST"]["prohibited_executed"] == 0 and mutation["BLACKLIST_ENUM"]["prohibited_executed"] == 0
    succeeds = (attack["BLACKLIST_ENUM"]["prohibited_executed"] > 0
                and 0 < attack["BLACKLIST_NORMALIZED"]["prohibited_executed"] < attack["BLACKLIST_ENUM"]["prohibited_executed"])
    return {"attack": attack, "mutation_only_canonical_names": mutation, "variant_10pct_novel_legit_actions": with_novel,
            "prediction_allowlist_has_nonzero_legit_block_in_base_world": attack["ALLOWLIST"]["legit_blocked"] > 0,
            "allowlist_cost_appears_with_novel_legit_actions": with_novel["ALLOWLIST"]["legit_blocked"] > 0,
            "status": "TOY-BROKEN" if not ok_ctrl else ("ATTACK-SUCCEEDS" if succeeds else "ATTACK-FAILS")}


# ---------------- R3-D: parse mismatch ----------------
def gate_parse(s):
    kv = [p.split("=", 1) for p in s.split("&")]
    ops = [v for k, v in kv if k == "op"]
    return ops[0]                                               # first duplicate wins, case-sensitive


def exec_parse(s):
    kv = [p.split("=", 1) for p in s.split("&")]
    ops = [v for k, v in kv if k == "op"]
    return ops[-1].lower()                                      # last wins, case-folded


def gate_ok(op):
    return op != "delete"                                       # case-sensitive deny of the prohibited name


def requests(ops, max_keys):
    out = []
    for n in range(1, max_keys + 1):
        for combo in itertools.product(ops, repeat=n):
            out.append("&".join(f"op={o}" for o in combo))
    return out


def executor_runs_passed_op(op):
    return op                                                   # executes exactly the operation object the gate passed


def executor_runs_passed_op_but_folds(op):
    return op.lower()                                           # executor still case-folds what it was passed


def r3d():
    ops_attack = ["read", "write", "delete", "Delete", "DELETE"]
    reqs = requests(ops_attack, 2)
    mismatch = sum(1 for r in reqs if gate_ok(gate_parse(r)) and exec_parse(r) == "delete")

    def count(gate_normalizes, executor):
        n = 0
        for r in reqs:
            op = gate_parse(r)
            if gate_normalizes:
                op = op.lower()                                 # gate canonicalizes, then passes the canonical op on
            if gate_ok(op) and executor(op) == "delete":
                n += 1
        return n
    parse_once_normalized = count(True, executor_runs_passed_op)
    parse_once_raw_exec_folds = count(False, executor_runs_passed_op_but_folds)
    reqs_mut = requests(["read", "write", "delete"], 1)
    mismatch_mut = sum(1 for r in reqs_mut if gate_ok(gate_parse(r)) and exec_parse(r) == "delete")
    status = ("TOY-BROKEN" if (parse_once_normalized != 0 or mismatch_mut != 0)
              else ("ATTACK-SUCCEEDS" if mismatch > 0 else "ATTACK-FAILS"))
    return {"requests_enumerated": len(reqs), "mismatched_allowed_but_executed_as_delete": mismatch,
            "parse_once_with_gate_normalization": parse_once_normalized,
            "parse_once_without_normalization_executor_still_folds": parse_once_raw_exec_folds,
            "mutation_grammar_mismatch": mismatch_mut, "status": status}


# ---------------- R3-E: advisory gate versus gate-owned effect path ----------------
def r3e(mode, c=1.0, b=0.0, n=2000, p_prohibited=0.3, seed=51):
    rng = random.Random(seed)
    executed_prohibited = prohibited = 0
    for _ in range(n):
        is_prohibited = rng.random() < p_prohibited
        prohibited += is_prohibited
        allowed = not is_prohibited                              # the gate's decision is correct here
        if mode == "ADVISORY":
            performs = allowed or (rng.random() > c)             # host ignores a reject with prob 1 - c
        else:                                                    # OWNED: effect runs inside the gate; host may use a bypass channel
            performs = allowed or (rng.random() < b)
        if performs and is_prohibited:
            executed_prohibited += 1
    return {"prohibited_requests": prohibited, "prohibited_executed": executed_prohibited}


def r3e_all():
    out = {"ADVISORY_c1.0": r3e("ADVISORY", c=1.0), "ADVISORY_c0.9": r3e("ADVISORY", c=0.9),
           "ADVISORY_c0.0": r3e("ADVISORY", c=0.0), "OWNED_b0": r3e("OWNED", b=0.0),
           "OWNED_b0.1": r3e("OWNED", b=0.1)}
    ctrl_ok = out["ADVISORY_c1.0"]["prohibited_executed"] == 0 and out["OWNED_b0"]["prohibited_executed"] == 0
    succeeds = out["ADVISORY_c0.0"]["prohibited_executed"] == out["ADVISORY_c0.0"]["prohibited_requests"] \
        and out["OWNED_b0.1"]["prohibited_executed"] > 0
    out["status"] = "TOY-BROKEN" if not ctrl_ok else ("ATTACK-SUCCEEDS" if succeeds else "ATTACK-FAILS")
    return out


# ---------------- R3-F: hybrid re-proposal with an instrumented gate ----------------
HARD_MAX, SOFT_LOW = 0.6, 0.3


def in_E(r, c):
    return r <= HARD_MAX and (not (SOFT_LOW < r <= HARD_MAX) or c == "oversight")


def r3f(world, seed=9, steps=500, flip=0.2):
    rng = random.Random(seed)
    calls = {"n": 0, "denies": 0}

    def gate(r_next, c):                                         # counter incremented inside the gate
        calls["n"] += 1
        ok = in_E(r_next, c)
        calls["denies"] += (not ok)
        return ok

    c, r, stranded, repairs = "oversight", 0.5, 0, 0
    for _ in range(steps):
        if rng.random() < flip:
            c = "none" if c == "oversight" else "oversight"
        if world in ("RE_PROPOSE", "REPAIR_ON_DENY"):
            ok = gate(r, c)
            if not ok and world == "REPAIR_ON_DENY":
                r, repairs = 0.2, repairs + 1                    # repair rule: not stated in the source
        if not in_E(r, c):
            stranded += 1
    return {"gate_invocations": calls["n"], "gate_denies": calls["denies"], "stranded_steps": stranded,
            "repair_events": repairs}


def r3f_all():
    out = {w: r3f(w) for w in ("NO_PROPOSAL", "RE_PROPOSE", "REPAIR_ON_DENY")}
    ok = (out["NO_PROPOSAL"]["gate_invocations"] == 0 and out["RE_PROPOSE"]["gate_invocations"] == 500)
    same = out["NO_PROPOSAL"]["stranded_steps"] == out["RE_PROPOSE"]["stranded_steps"]
    repaired = out["REPAIR_ON_DENY"]["repair_events"] > 0 and out["REPAIR_ON_DENY"]["stranded_steps"] < out["RE_PROPOSE"]["stranded_steps"]
    out["status"] = "TOY-BROKEN" if not ok else ("ATTACK-SUCCEEDS" if (same and out["NO_PROPOSAL"]["stranded_steps"] > 0 and repaired) else "PARTIAL")
    return out


def run_all():
    return {"R3A": r3a_all(), "R3B": r3b(), "R3C": r3c_all(), "R3D": r3d(), "R3E": r3e_all(), "R3F": r3f_all()}


def summary(r):
    return {k: v["status"] for k, v in r.items()}


PINNED_STATUS = {"R3A": "ATTACK-SUCCEEDS", "R3B": "ATTACK-SUCCEEDS", "R3C": "ATTACK-SUCCEEDS",
                 "R3D": "ATTACK-SUCCEEDS", "R3E": "ATTACK-SUCCEEDS", "R3F": "ATTACK-SUCCEEDS"}

PINNED_COUNTS = {
    "R3A_adversarial_violating_fraction": 1.0, "R3A_random_q0.1_w5_violating_fraction": 0.402,
    "R3C_blacklist_enum_prohibited": 300, "R3C_blacklist_normalized_prohibited": 70,
    "R3D_mismatch": 14, "R3D_parse_once_raw_exec_folds": 12,
    "R3E_advisory_c0.9": 60, "R3E_owned_b0.1": 61,
    "R3F_no_proposal_invocations": 0, "R3F_re_propose_invocations": 500, "R3F_stranded": 233,
}


def counts(r):
    return {
        "R3A_adversarial_violating_fraction": r["R3A"]["ADVERSARIAL_w5"]["violating_fraction"],
        "R3A_random_q0.1_w5_violating_fraction": r["R3A"]["RANDOM_q0.1_w5"]["violating_fraction"],
        "R3C_blacklist_enum_prohibited": r["R3C"]["attack"]["BLACKLIST_ENUM"]["prohibited_executed"],
        "R3C_blacklist_normalized_prohibited": r["R3C"]["attack"]["BLACKLIST_NORMALIZED"]["prohibited_executed"],
        "R3D_mismatch": r["R3D"]["mismatched_allowed_but_executed_as_delete"],
        "R3D_parse_once_raw_exec_folds": r["R3D"]["parse_once_without_normalization_executor_still_folds"],
        "R3E_advisory_c0.9": r["R3E"]["ADVISORY_c0.9"]["prohibited_executed"],
        "R3E_owned_b0.1": r["R3E"]["OWNED_b0.1"]["prohibited_executed"],
        "R3F_no_proposal_invocations": r["R3F"]["NO_PROPOSAL"]["gate_invocations"],
        "R3F_re_propose_invocations": r["R3F"]["RE_PROPOSE"]["gate_invocations"],
        "R3F_stranded": r["R3F"]["RE_PROPOSE"]["stranded_steps"],
    }


if __name__ == "__main__":
    r = run_all()
    r["summary"] = summary(r)
    r["counts"] = counts(r)
    print(json.dumps(r, indent=2, sort_keys=True))
    if "--selftest" in sys.argv:
        assert r["summary"] == PINNED_STATUS, r["summary"]
        assert r["counts"] == PINNED_COUNTS, r["counts"]
        print("selftest OK")
