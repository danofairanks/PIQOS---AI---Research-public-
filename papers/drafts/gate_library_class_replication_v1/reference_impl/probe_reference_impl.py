"""Run from the reference implementation repo root with DATABASE_URL=sqlite:///<file>. Engine-level + real app via TestClient."""
import json, math, os, sys, io
from datetime import datetime, timezone
from app.engines.extractor import extract_rules
from app.engines.evaluator import evaluate
from app.engines.types import OrderData

out = {}
def ev(text, role, amount, action="payment.release", evidence=(), delegation_max=None):
    rules = extract_rules(text, "p.txt")
    for i, r in enumerate(rules): r.id = f"r{i}"
    rec = evaluate(OrderData(action=action, requester_role=role, amount=amount, evidence=list(evidence), delegation_max_amount=delegation_max), rules)
    return rec.decision
def rl(text): return [(r.attribute, r.action, r.subject, r.value, r.threshold) for r in extract_rules(text, "p.txt")]

# --- extraction ---
BASE = "Authorized roles for payment.release: manager."
out["X1_unauthorized_roles_rules"] = rl("Unauthorized roles for payment.release: intern.")
out["X1_unauthorized_intern_decision"] = ev("Unauthorized roles for payment.release: intern.", "intern", 100)
out["X1_no_authorized_roles_rules"] = rl("No authorized roles for payment.release: contractor.")
out["X1_no_authorized_contractor_decision"] = ev("No authorized roles for payment.release: contractor.", "contractor", 100)
t = BASE + " The manager may approve payment.release up to USD 100,000."
out["X2_usd_prefix_rules"] = rl(t); out["X2_manager_10M"] = ev(t, "manager", 10_000_000)
out["X2_control_dollar_sign"] = ev(BASE + " The manager may approve payment.release up to $100,000.", "manager", 10_000_000)
out["X3_amount_parsing"] = {s: [r[3] for r in rl(f"The manager may approve payment.release up to {s}.") if r[0] == "max_amount"]
                            for s in ("$2 million", "100k", "5,000.50", "100.000", "1,5", "100,000")}
t = "payment.release requires invoice. Only managers are authorized to release payment.release."
out["X4_rules"] = rl(t); out["X4_intern_with_invoice"] = ev(t, "intern", 500, evidence=["invoice"]); out["X4_empty_role"] = ev(t, "", 500, evidence=["invoice"])
out["X4_control_role_list_present"] = ev("Authorized roles for payment.release: manager. payment.release requires invoice.", "intern", 500, evidence=["invoice"])
t = "The manager may approve payment.release up to 10,000."
out["X5_intern_10M_no_role_list"] = ev(t, "intern", 10_000_000)
out["X5_manager_over_limit_control"] = ev(t, "manager", 10_001)
out["X6_first_wins_100k_then_10k"] = (ev(BASE + " The manager may approve payment.release up to 100,000. The manager may approve payment.release up to 10,000.", "manager", 50_000),)
out["X6_10k_then_100k"] = (ev(BASE + " The manager may approve payment.release up to 10,000. The manager may approve payment.release up to 100,000.", "manager", 50_000),)

# --- engine-level evaluation inputs ---
POL = BASE + " The manager may approve payment.release up to 100,000. Any payment.release above 50,000 requires invoice and purchase_order."
out["V1_amount_omitted_engine"] = ev(POL, "manager", None)
out["V2_engine_neg5"] = ev(POL, "manager", -5); out["V2_engine_true"] = ev(POL, "manager", True)
out["V2_engine_nan"] = ev(POL, "manager", float("nan")); out["V2_engine_inf"] = ev(POL, "manager", float("inf"))
try: out["V2_engine_str"] = ev(POL, "manager", "250000")
except Exception as e: out["V2_engine_str"] = f"EXC {type(e).__name__}: {e}"[:90]
out["V3_case"] = ev(POL, "manager", 100, action="Payment.Release"); out["V3_space"] = ev(POL, "manager", 100, action=" payment.release")
out["V4_delegation_huge"] = ev(POL, "manager", 100_001, delegation_max=1e9); out["V4_nan"] = ev(POL, "manager", 100_001, delegation_max=float("nan")); out["V4_negative"] = ev(POL, "manager", 1, delegation_max=-1)
out["V7_boundary"] = (ev(POL, "manager", 100_000, evidence=["invoice", "purchase_order"]), ev(POL, "manager", 100_000.01, evidence=["invoice", "purchase_order"]))
out["C_unknown_action"] = ev(POL, "manager", 1, action="wire.send"); out["C_role_not_listed"] = ev(POL, "intern", 1)
rec = evaluate(OrderData(action="payment.release", requester_role="intern", amount=1), [r for r in extract_rules(POL, "p")])
out["C_short_circuit_no_admissibility_checks"] = [c.category for c in rec.checks]

# --- HTTP ---
from fastapi.testclient import TestClient
import importlib.util
spec = importlib.util.spec_from_file_location("ra_main", "main.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
with TestClient(m.app) as c:
    def upload(text, name="p.txt"): return c.post("/api/v1/specs/upload", files={"file": (name, io.BytesIO(text.encode()), "text/plain")}).json()
    def assess(role="manager", amount="OMIT", action="payment.release", evidence=(), delegation=None, route="/api/v1/orders/assess"):
        body = {"action": action, "target": "T", "requester": {"id": "u", "role": role}, "evidence": list(evidence), "context": {"currency": "EUR"}}
        if amount != "OMIT": body["context"]["amount"] = amount
        if delegation is not None: body["delegation"] = delegation
        r = c.post(route, json=body)
        try: return r.status_code, r.json().get("decision")
        except Exception: return r.status_code, r.text[:60]
    s = upload(POL)
    out["V0_upload_summary_keys"] = sorted(s.keys()); out["V0_total_rules"] = s["total_rules"]
    out["X7_ignored_sentence_listed"] = any("ignored" in k.lower() or "skipped" in k.lower() for k in s)
    s3 = upload("Authorized roles for payment.release: manager. This is a sentence the extractor does not understand. Neither is this one.")
    out["X7_three_sentences_summary"] = {"total_rules": s3["total_rules"], "keys": sorted(s3.keys())}
    upload(POL)
    out["V1_http_amount_omitted"] = assess(amount="OMIT")
    out["V1_http_omitted_with_delegation"] = assess(amount="OMIT", delegation={"max_amount": 1})
    for label, a in (("str", "250000"), ("true", True), ("neg5", -5), ("none", None), ("list", [1]), ("big", 1e308)):
        try: out[f"V2_http_{label}"] = assess(amount=a)
        except Exception as e: out[f"V2_http_{label}"] = f"EXC {type(e).__name__}"
    out["V3_http_case"] = assess(action="Payment.Release", amount=100)
    out["V4_http_delegation_huge"] = assess(amount=100_001, delegation={"max_amount": 1e9, "granted_by": "x"})
    out["V5_http_expired_delegation_ignored"] = assess(amount=100, delegation={"max_amount": 1000, "expires_at": "2000-01-01T00:00:00Z"}, evidence=[])
    out["V7_http_boundary"] = (assess(amount=100000, evidence=["invoice", "purchase_order"]), assess(amount=100000.01, evidence=["invoice", "purchase_order"]))
    out["V8_http_currency_ignored"] = c.post("/api/v1/orders/assess", json={"action": "payment.release", "requester": {"role": "manager"}, "evidence": [], "context": {"amount": 40000, "currency": "JPY"}}).json().get("decision")
    # V6 unauthenticated full replacement
    before = assess(role="manager", amount=100)
    upload("Authorized roles for payment.release: attacker.")
    out["V6_before_after"] = {"manager_before": before, "manager_after": assess(role="manager", amount=100), "attacker_after_unlimited": assess(role="attacker", amount=10**12)}
    r = c.post("/api/v1/specs/upload", files={"file": ("x.txt", io.BytesIO(b"nothing parseable here"), "text/plain")}).json()
    out["V6_unparseable_upload_total_rules"] = r["total_rules"]; out["V6_after_empty_policy_manager"] = assess(role="manager", amount=1)
print(json.dumps(out, indent=1, default=str))
