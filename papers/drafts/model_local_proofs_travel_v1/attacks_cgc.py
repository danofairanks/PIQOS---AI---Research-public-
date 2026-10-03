#!/usr/bin/env python3
"""Reviewer's attack suite adapted to commit-gate-core (exact clone). Usage: attacks_cgc.py <repo_root>.
Test doubles (clock, ledger, audit sink, record builder) are copied from the repository's own tests/test_authorize.py.
Each attack has a control that must not show the effect; outcomes are measured by running the library.
"""
import copy
import importlib.util
import json
import sys
import threading
from datetime import datetime, timezone
from threading import Lock

REPO = sys.argv[1]
sys.path.insert(0, REPO + "/src")
from commit_gate_core.authorize import payload_hash
from commit_gate_core.gate import CommitGate
from commit_gate_core.hmac_mac import HmacSha256Verifier

spec = importlib.util.spec_from_file_location("verify_receipt", REPO + "/scripts/verify_receipt.py")
vr = importlib.util.module_from_spec(spec); spec.loader.exec_module(vr)


class FakeClock:
    def __init__(self, now): self._now = now
    def now(self): return self._now


class InMemoryNonceLedger:                                    # verbatim from the repository's tests
    def __init__(self):
        self.used = set(); self._owners = {}; self._lock = Lock()
    def contains(self, nonce):
        with self._lock: return nonce in self.used
    def consume(self, nonce, decision_id):
        with self._lock:
            if nonce in self.used: return False
            self.used.add(nonce); self._owners[nonce] = decision_id; return True
    def rollback(self, nonce, decision_id):
        with self._lock:
            if self._owners.get(nonce) == decision_id:
                self.used.discard(nonce); self._owners.pop(nonce, None)


class RecordingAuditSink:
    def __init__(self, fail_on=None):
        self.events = []; self.fail_on = fail_on
    def append(self, event):
        if self.fail_on and event.get("event_type") == self.fail_on:
            raise IOError("audit down")
        self.events.append(event)


KEY = b"lab-key-not-for-production"
PAYLOAD = b"invoice-778-body"
NOW = datetime(2026, 4, 27, 5, 1, tzinfo=timezone.utc)
SCOPE = dict(actor_id="agent_17", action="approve_invoice", object_id="invoice_778", environment="prod")


def signed_record(verifier, payload=PAYLOAD, **overrides):
    record = {"decision_id": "dr_001", "actor_id": "agent_17", "action": "approve_invoice", "object_id": "invoice_778",
              "environment": "prod", "commit_hash": payload_hash(payload), "verdict": "ALLOW", "policy_version": "2026-04-27.1",
              "issued_at": "2026-04-27T05:00:00Z", "expires_at": "2026-04-27T05:05:00Z", "nonce": "nonce_001", "signature": ""}
    record.update(overrides)
    record["signature"] = verifier.sign(record)
    return record


def make_gate(now=NOW, audit=None, ledger=None, key=KEY):
    v = HmacSha256Verifier(key)
    audit = audit or RecordingAuditSink()
    ledger = ledger or InMemoryNonceLedger()
    g = CommitGate(verifier=v, nonce_ledger=ledger, audit=audit, accepted_policy_versions=("2026-04-27.1",), clock=FakeClock(now))
    return g, v, ledger, audit


out = {}

# C1 forgery
g, v, led, aud = make_gate()
rec = signed_record(v)
tampered = dict(rec, object_id="invoice_999")                    # control: scope edited, signature stale
r1 = g.authorize(tampered, PAYLOAD, **dict(SCOPE, object_id="invoice_999")).code
other_key = HmacSha256Verifier(b"other-key")
r2 = g.authorize(signed_record(other_key, nonce="n2"), PAYLOAD, **SCOPE).code      # control: wrong key
g3, v3, _, _ = make_gate()
arbitrary = signed_record(v3, decision_id="dr_any", action="wire_transfer", object_id="acct_1", nonce="n3", commit_hash=payload_hash(b"x"))
r3 = g3.authorize(arbitrary, b"x", actor_id="agent_17", action="wire_transfer", object_id="acct_1", environment="prod").code
out["C1_forgery"] = {"control_stale_signature": r1, "control_wrong_key": r2, "key_holder_mints_arbitrary_scope": r3}

# C2 replay
g, v, led, aud = make_gate()
rec = signed_record(v)
first = g.authorize(dict(rec), PAYLOAD, **SCOPE).code
again = g.authorize(dict(rec), PAYLOAD, **SCOPE).code           # control: same ledger
gA, vA, _, _ = make_gate(); gB, vB, _, _ = make_gate()           # two gates, separate ledgers (restart or second process)
recAB = signed_record(vA)
a = gA.authorize(dict(recAB), PAYLOAD, **SCOPE).code
b = gB.authorize(dict(recAB), PAYLOAD, **SCOPE).code
out["C2_replay"] = {"control_first": first, "control_second_same_ledger": again, "two_ledgers_first": a, "two_ledgers_second": b}

# C3 expiry (control) and ticket after expiry (boundary)
gE, vE, _, _ = make_gate(now=datetime(2026, 4, 27, 5, 10, tzinfo=timezone.utc))
exp = gE.authorize(signed_record(vE), PAYLOAD, **SCOPE).code
gF, vF, _, _ = make_gate()
res = gF.authorize(signed_record(vF), PAYLOAD, **SCOPE)
late = datetime(2026, 4, 27, 6, 0, tzinfo=timezone.utc)
ticket_still_usable = res.ticket is not None and res.ticket["expires_at"] < late.isoformat().replace("+00:00", "Z")
out["C3_expiry"] = {"control_expired_record": exp, "ticket_carries_expired_window_and_nothing_refuses_use": ticket_still_usable}

# C4 receipts
fab = {"receipt_id": "rcpt_x", "decision": "REFUSE", "mutation_committed": False, "reason": "fabricated"}
fab["receipt_hash"] = vr.stable_hash(fab)
bad = dict(fab, reason="edited")
out["C4_receipt_hash_check"] = {"control_edited_without_rehash": vr._check_hash_integrity(bad)[0],
                                "fabricated_receipt_with_recomputed_hash": vr._check_hash_integrity(fab)[0]}

# C5 concurrency on the nonce
def race(trials=300, n=8):
    old = sys.getswitchinterval(); sys.setswitchinterval(1e-6); double = 0
    for _ in range(trials):
        g, v, led, aud = make_gate(); rec = signed_record(v); barrier = threading.Barrier(n); results = []
        def run():
            barrier.wait(); results.append(g.authorize(dict(rec), PAYLOAD, **SCOPE).authorized)
        ts = [threading.Thread(target=run) for _ in range(n)]; [t.start() for t in ts]; [t.join() for t in ts]
        double += sum(results) > 1
    sys.setswitchinterval(old); return double
seq = 0
for _ in range(300):
    g, v, led, aud = make_gate(); rec = signed_record(v)
    seq += sum(g.authorize(dict(rec), PAYLOAD, **SCOPE).authorized for _ in range(8)) > 1
out["C5_concurrent_nonce"] = {"control_sequential_trials_with_double_authorization_of_300": seq,
                              "attack_threaded_trials_with_double_authorization_of_300": race()}

# C6 payload snapshot (caller boundary)
g, v, led, aud = make_gate()
buf = bytearray(PAYLOAD)
rec = signed_record(v, payload=PAYLOAD)
res = g.authorize(dict(rec), buf, **SCOPE)
buf[0:7] = b"MALICIO"                                              # mutated after authorization
out["C6_payload_snapshot"] = {"authorized": res.authorized, "ticket_hash_matches_bytes_now_held": res.payload_hash == payload_hash(bytes(buf))}

# C7 audit failure and rollback failure
class BadLedger(InMemoryNonceLedger):
    def rollback(self, nonce, decision_id): raise IOError("rollback down")
g, v, led, aud = make_gate(audit=RecordingAuditSink(fail_on="GATE_AUTHORIZED"), ledger=BadLedger())
res = g.authorize(signed_record(v), PAYLOAD, **SCOPE)
g2, v2, led2, aud2 = make_gate(audit=RecordingAuditSink(fail_on="GATE_AUTHORIZED"))
res2 = g2.authorize(signed_record(v2), PAYLOAD, **SCOPE)
out["C7_audit_failure"] = {"control_rollback_ok": (res2.code, sorted(led2.used)),
                           "rollback_fails": (res.code.split(":")[0] + ":" + res.code.split(":")[1], sorted(led.used))}

# C8 malformed call types
g, v, led, aud = make_gate()
def attempt(fn):
    n0 = len(aud.events)
    try:
        r = fn(); return {"returned": getattr(r, "code", str(r)), "audit_events_added": len(aud.events) - n0}
    except Exception as e:
        return {"raised": type(e).__name__, "audit_events_added": len(aud.events) - n0}
out["C8_malformed_calls"] = {"payload_is_str": attempt(lambda: g.authorize(signed_record(v), "text", **SCOPE)),
                             "record_is_list": attempt(lambda: g.authorize([1, 2], PAYLOAD, **SCOPE)),
                             "control_missing_field": attempt(lambda: g.authorize({"decision_id": "d"}, PAYLOAD, **SCOPE))}

# C9 unauthenticated fields reach the audit log
g, v, led, aud = make_gate()
fake = {"decision_id": "dr_victim_77", "actor_id": "a", "action": "a", "object_id": "o", "environment": "e", "commit_hash": "sha256:00",
        "verdict": "DENY", "policy_version": "p", "issued_at": "2026-04-27T05:00:00Z", "expires_at": "2026-04-27T05:05:00Z",
        "nonce": "attacker_chosen_nonce", "signature": "hmac-sha256:00"}
r = g.authorize(fake, PAYLOAD, **SCOPE)
ev = aud.events[-1]
out["C9_unauthenticated_fields_in_audit"] = {"code": r.code, "audit_decision_id": ev["decision_id"], "audit_nonce": ev["nonce"],
                                             "nonce_consumed": "attacker_chosen_nonce" in led.used}

# C10 canonicalization (safe direction control)
g, v, led, aud = make_gate()
rec = signed_record(v)
r = g.authorize(dict(rec), PAYLOAD, **dict(SCOPE, object_id="invoice_778 "))
out["C10_scope_string_variants"] = {"trailing_space_object_id": r.code}

print(json.dumps(out, indent=2, sort_keys=True))
