#!/usr/bin/env python3
"""Attack suite on constraint-workshop (exact clone). Usage: attacks_constraint_workshop.py <repo_root> [race_trials].
Predictions were written before this script (internal history). Each attack has a control in the same script.
"""
import copy
import json
import os
import sys
import threading

ROOT = os.path.abspath(sys.argv[1])
RACE_TRIALS = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "commit_gate", "src"))
from stop_machine import State, StopMachine
from authority_gate import AuthorityGate, Evidence, Decision
import invariant_litmus as il
from commit_gate.engine import evaluate as cg_eval, load_ruleset
from commit_gate.canonicalise import canonical_hash
from commit_gate.drift import build_authority_graph, detect_drift
from mgtp.evaluate_transition import evaluate_transition
from mgtp.registry import load_registry
from mgtp.types import AuthorityContext, RiskClass, TransitionRequest

out = {}


def red():
    m = StopMachine(); m.advance(); m.advance(); return m


# CW-1
errs = []
for fn in ("advance", "reset"):
    try:
        getattr(red(), fn)(); errs.append("no error")
    except ValueError:
        errs.append("ValueError")
m = red(); m._state = State.GREEN
out["CW1_stop_machine_write"] = {"control_advance_reset_from_RED": errs, "assign__state_from_RED": m.state.name}

# CW-2
def race(trials):
    old = sys.getswitchinterval(); sys.setswitchinterval(1e-6); green = 0
    for _ in range(trials):
        m = StopMachine(); m.advance(); b = threading.Barrier(2)
        def adv():
            b.wait()
            try: m.advance()
            except Exception: pass
        def rst():
            b.wait()
            try: m.reset()
            except Exception: pass
        t1, t2 = threading.Thread(target=adv), threading.Thread(target=rst); t1.start(); t2.start(); t1.join(); t2.join()
        green += m.state is State.GREEN
    sys.setswitchinterval(old); return green
seq = {}
for order in ("advance_then_reset", "reset_then_advance"):
    m = StopMachine(); m.advance()
    steps = [m.advance, m.reset] if order == "advance_then_reset" else [m.reset, m.advance]
    for s in steps:
        try: s()
        except Exception: pass
    seq[order] = m.state.name
out["CW2_stop_machine_race"] = {"control_sequential": seq, "threaded_trials": RACE_TRIALS, "threaded_trials_ending_GREEN": race(RACE_TRIALS)}

# CW-3
g = AuthorityGate(Evidence.OWNER)
try:
    g.required_level = Evidence.NONE; prop = "no error"
except AttributeError:
    prop = "AttributeError"
g2 = AuthorityGate(Evidence.OWNER); g2._required = Evidence.NONE
out["CW3_authority_gate"] = {"control_USER": g.check(Evidence.USER).name, "caller_supplied_ADMIN": g.check(Evidence.ADMIN).name,
                             "control_property_assignment": prop, "poke__required_then_check_NONE": g2.check(Evidence.NONE).name}

# CW-4
base = "Shannon limit provides an upper bound"
out["CW4_invariant_litmus"] = {"control": il.classify(base).posture.name,
                               "plural": il.classify("Shannon limits provide upper bounds").posture.name,
                               "zero_width": il.classify("Shannon li​mit provides an upper bound").posture.name,
                               "hyphenated": il.classify("Shannon limit provides an upper-bound").posture.name}

# commit gate
rules = load_ruleset(os.path.join(ROOT, "commit_gate", "rules", "ruleset.json"))
ALLOWED_ACTOR = rules["allowlist"][0]["actor_id"]  # the actor id the repository's own ruleset allows
def req(actor=ALLOWED_ACTOR, action="FILE", scope=None, ih="h", ts="2026-01-01T00:00:00Z", ctx=None):
    return {"actor_id": actor, "action_class": action, "context": ctx or {}, "authority_scope": scope if scope is not None else {"project": "alpha"},
            "invariant_hash": ih, "timestamp_utc": ts}
out["CW5_self_declared_actor_scope"] = {"control_other_actor": cg_eval(req(actor="mallory"), rules)["verdict"],
                                        "control_wrong_scope": cg_eval(req(scope={"project": "beta"}), rules)["verdict"],
                                        "claimed_actor_and_scope": cg_eval(req(), rules)["verdict"]}
rn = {"allowlist": [{"actor_id": "u", "action_class": "FILE", "scope_match": {"project": None}}], "denylist": [], "escalation": []}
rs = {"allowlist": [{"actor_id": "u", "action_class": "FILE", "scope_match": {"project": "alpha"}}], "denylist": [], "escalation": []}
out["CW6_null_scope_value"] = {"control_string_rule_missing_key": cg_eval(req(actor="u", scope={}), rs)["verdict"],
                               "null_rule_missing_key": cg_eval(req(actor="u", scope={}), rn)["verdict"]}
a = cg_eval(req(ih="not-a-hash"), rules)["verdict"]; b = cg_eval(req(ih="0" * 64), rules)["verdict"]
cur = copy.deepcopy(rules); cur["allowlist"].append({"actor_id": "mallory", "action_class": "DEPLOY", "scope_match": {}})
bg, cgph = build_authority_graph(rules), build_authority_graph(cur)
out["CW7_invariant_hash"] = {"verdict_with_arbitrary_strings": [a, b],
                             "control_new_edge_same_hash": detect_drift(bg, cgph, "h1", "h1", True)["pass"],
                             "control_new_edge_changed_hash_no_ack": detect_drift(bg, cgph, "h1", "x", False)["pass"],
                             "new_edge_arbitrary_changed_hash_with_ack": detect_drift(bg, cgph, "h1", "x", True)["pass"]}
def attempt(r):
    try: return cg_eval(r, rules)["verdict"]
    except Exception as e: return "raised:" + type(e).__name__
out["CW8_malformed_scope"] = {"control_dict": attempt(req()), "none": attempt(req(scope=None) | {"authority_scope": None}),
                              "list": attempt(req() | {"authority_scope": ["project"]})}
r1 = cg_eval(req(ts="2026-01-01T00:00:00Z"), rules); r2 = cg_eval(req(ts="2030-06-01T00:00:00Z"), rules); r3 = cg_eval(req(ctx={"k": "v"}), rules)
out["CW9_freshness"] = {"same_hash_across_timestamps": r1["decision_hash"] == r2["decision_hash"], "control_changed_field_changes_hash": r1["decision_hash"] != r3["decision_hash"]}
bad_req = req(actor="mallory")
real = cg_eval(bad_req, rules)
ro = {"actor_id": bad_req["actor_id"], "action_class": bad_req["action_class"], "context": bad_req["context"],
      "authority_scope": bad_req["authority_scope"], "invariant_hash": bad_req["invariant_hash"]}
fab = {"verdict": "ALLOW", "reasons": ["allowlist_match"], "request_hash": canonical_hash(ro),
       "decision_hash": canonical_hash({"request": ro, "verdict": "ALLOW", "reasons": ["allowlist_match"]}), "artefact_version": "0.1"}
consistent = fab["decision_hash"] == canonical_hash({"request": ro, "verdict": fab["verdict"], "reasons": fab["reasons"]})
out["CW10_decision_hash_not_authentication"] = {"real_verdict": real["verdict"], "fabricated_ALLOW_hash_consistent_with_its_contents": consistent,
                                                "fabricated_hash_differs_from_real": fab["decision_hash"] != real["decision_hash"]}
# mgtp
registry = load_registry(os.path.join(ROOT, "registry", "TRANSITION_REGISTRY_v0.2.json"))
tr = TransitionRequest("TOOL_CALL_HTTP", RiskClass.HIGH, True, "res-1", False, None, "2025-06-01T12:00:00Z")
def ev(basis):
    try: return evaluate_transition(tr, AuthorityContext("a", basis, "t"), registry).outcome.value
    except Exception as e: return "raised:" + type(e).__name__
out["MG1_MG2_mgtp"] = {"control_USER": ev("USER"), "claimed_ADMIN": ev("ADMIN"), "claimed_OWNER": ev("OWNER"), "unknown_name": ev("SUPERADMIN")}
print(json.dumps(out, indent=2, sort_keys=True))
