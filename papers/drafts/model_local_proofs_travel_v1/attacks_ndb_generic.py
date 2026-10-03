#!/usr/bin/env python3
"""Reviewer's attacks on a witness/gate library (exact clone). Usage: attacks_ndb_generic.py <src_dir> [<proof_dir>].
Each attack has a control that must NOT show the effect, run in the same script.
Run from the repo root of the reconstructed copy. stdlib + pytest not required.
"""
import dataclasses
import os
import sys
import threading
import time

SRC = sys.argv[1]
PROOF = sys.argv[2] if len(sys.argv) > 2 else None
sys.path.insert(0, SRC)
if PROOF:
    sys.path.insert(0, PROOF)
    from model import (State, Phase, gated_transitions, initial_states, reachable, safety_invariant)
from ndb_gate import Gate, Outcome, AuthorityToken, Evidence, EvidenceClass
from ndb_gate.receipts import Receipt, ReceiptChain, verify_chain, GENESIS_HASH

out = {}


def fresh():
    sink = []
    def effect():
        sink.append("FIRED")
        return "FIRED"
    return Gate(), sink, effect


# A1: forged evidence class. The class is a label supplied with the token; nothing verifies it.
g, sink, eff = fresh()
weak = AuthorityToken("x", "s", Evidence("forged", EvidenceClass.PATTERN_ONLY, "attacker"))
c = g.bind("x", "s", weak, eff).outcome.value                 # control: forger labels itself weak (the suite's test)
g2, sink2, eff2 = fresh()
strong = AuthorityToken("x", "s", Evidence("forged", EvidenceClass.PROVED, "attacker"))
a = g2.bind("x", "s", strong, eff2).outcome.value
out["A1_forged_PROVED_label"] = {"control_self_labelled_weak": (c, len(sink)), "attack_self_labelled_PROVED": (a, len(sink2))}

# A2: replay with a copy of a spent token (single-use is tracked by id(token), not by value)
g, sink, eff = fresh()
tok = AuthorityToken("x", "s", Evidence("ok", EvidenceClass.PROVED, "first-party"))
g.bind("x", "s", tok, eff)
same = g.bind("x", "s", tok, eff).outcome.value               # control: same object
copy = dataclasses.replace(tok)                               # equal fields, new object
copied = g.bind("x", "s", copy, eff).outcome.value
out["A2_replay_by_copy"] = {"control_same_object_second_use": same, "attack_copy_second_use": copied, "effects_fired": len(sink)}

# A3: caller-supplied clock
g, sink, eff = fresh()
old = AuthorityToken("x", "s", Evidence("ok", EvidenceClass.PROVED, "first-party"), issued_at=time.time() - 10_000, ttl_seconds=1.0)
c = g.bind("x", "s", old, eff).outcome.value                  # control: expired, real clock
a = g.bind("x", "s", old, eff, now=old.issued_at).outcome.value   # attack: caller passes an earlier 'now'
out["A3_caller_supplied_clock"] = {"control_expired_real_clock": c, "attack_now_param": a, "effects_fired": len(sink)}

# A4: receipt chain: fully recomputed or fabricated chains verify
g, sink, eff = fresh()
tok = AuthorityToken("x", "s", Evidence("ok", EvidenceClass.PROVED, "first-party"))
g.bind("x", "s", None, eff)                                   # HOLD
g.bind("x", "s", tok, eff)                                    # ALLOW
real = list(g.chain)
# control: edit one receipt in place without recomputing later hashes
edited = [dataclasses.replace(real[0], outcome="ALLOW")] + real[1:]
control_ok = verify_chain(edited)
# attack 1: rebuild the whole chain with the history rewritten
forged = ReceiptChain()
for r in real:
    forged.append(r.action, r.scope, "ALLOW" if r.outcome == "HOLD" else r.outcome, r.reason, r.evidence_class)
attack_rewrite_ok = verify_chain(list(forged))
# attack 2: fabricate a chain of ALLOW receipts that the gate never produced
fab = ReceiptChain()
for _ in range(3):
    fab.append("delete", "prod", "ALLOW", "evidenced authority resolved", "PROVED")
out["A4_receipt_chain"] = {"control_partial_edit_verifies": control_ok, "attack_full_rewrite_verifies": attack_rewrite_ok,
                           "attack_fabricated_chain_verifies": verify_chain(list(fab))}

# A5: race on single-use token (real threads, no monkeypatching)
def race(trials=300, nthreads=8):
    old_interval = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    double = 0
    for _ in range(trials):
        g, sink, eff = fresh()
        tok = AuthorityToken("x", "s", Evidence("ok", EvidenceClass.PROVED, "first-party"))
        barrier = threading.Barrier(nthreads)
        def run():
            barrier.wait()
            g.bind("x", "s", tok, eff)
        ts = [threading.Thread(target=run) for _ in range(nthreads)]
        [t.start() for t in ts]; [t.join() for t in ts]
        double += len(sink) > 1
    sys.setswitchinterval(old_interval)
    return double
seq_double = 0
for _ in range(300):
    g, sink, eff = fresh()
    tok = AuthorityToken("x", "s", Evidence("ok", EvidenceClass.PROVED, "first-party"))
    for _ in range(8):
        g.bind("x", "s", tok, eff)
    seq_double += len(sink) > 1
out["A5_concurrent_single_use"] = {"control_sequential_trials_with_double_effect_of_300": seq_double,
                                   "attack_threaded_trials_with_double_effect_of_300": race()}

if PROOF:
    # A6: the invariant is about the cached decision, not authority at the time of the effect.
    def with_revocation(s):
        nxt = gated_transitions(s)
        if s.phase is Phase.RESOLVED:                              # environment revokes authority after the check
            nxt.append(dataclasses.replace(s, authority_present=False))
        return nxt
    states = reachable.__wrapped__(with_revocation) if hasattr(reachable, "__wrapped__") else None
    if states is None:
        frontier = list(initial_states()); seen = set(frontier)
        while frontier:
            s = frontier.pop()
            for n in with_revocation(s):
                if n not in seen:
                    seen.add(n); frontier.append(n)
        states = seen
    orig_ok = all(safety_invariant(s) for s in states)
    at_exec_ok = all(s.phase is not Phase.EXECUTED or (s.authority_present and s.resolved_allow) for s in states)
    out["A6_model_with_revocation_between_check_and_effect"] = {"states": len(states), "original_invariant_holds": orig_ok,
                                                               "authority_present_at_execution_invariant_holds": at_exec_ok}

# A7: effect_fn failing after the receipt is written
g, sink, eff = fresh()
def boom():
    raise RuntimeError("effect failed")
tok = AuthorityToken("x", "s", Evidence("ok", EvidenceClass.PROVED, "first-party"))
try:
    g.bind("x", "s", tok, boom)
except RuntimeError:
    pass
out["A7_allow_receipt_without_effect"] = {"receipts": len(g.chain), "last_outcome": list(g.chain)[-1].outcome}

import json
print(json.dumps(out, indent=2, sort_keys=True))
