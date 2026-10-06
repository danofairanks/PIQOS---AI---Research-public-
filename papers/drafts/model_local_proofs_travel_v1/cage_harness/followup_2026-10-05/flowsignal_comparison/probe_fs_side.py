"""FlowSignal-side T1-T7. Run with fs venv from harness dir."""
import json, math, sys
from datetime import datetime, timedelta, timezone
from dataclasses import replace
from app.engines.financial_types import FinancialAuthorityRequest
from app.engines.financial_runtime import evaluate_financial
from app.engines.execution_gateway import ExecutionAttempt, validate_execution
from app.engines import authority_store as AS

T0 = datetime(2026, 10, 6, 12, 0, tzinfo=timezone.utc)
def req(**kw):
    base = dict(scenario_id="p", action="payment.release", target="t", actor_id="a", actor_type="agent", actor_role="r",
        actor_authenticated=True, kya_status="VERIFIED", principal_id="p1", principal_name="P", mandate_id="MANDATE-TREASURY-001",
        mandate_status="ACTIVE", mandate_max_amount=1000.0, mandate_currency="USD", permitted_source_accounts=["S"],
        permitted_counterparty_class="c", mandate_valid_until=T0 + timedelta(days=1), amount=100.0, currency="USD",
        source_account="S", beneficiary="B", purpose="x", counterparty_status="APPROVED", account_status="ACTIVE",
        risk_state="NORMAL", approval_required=False, screening_status="CLEAR", screening_captured_at=T0 - timedelta(seconds=5),
        screening_max_age_seconds=300, screening_source="src", requested_execution_time=T0)
    base.update(kw); return FinancialAuthorityRequest(**base)
def att(r, **kw):
    d = dict(actor_id=r.actor_id, principal_id=r.principal_id, action=r.action, target=r.target, amount=r.amount, currency=r.currency,
        source_account=r.source_account, beneficiary=r.beneficiary, purpose=r.purpose, mandate_id=r.mandate_id, attempted_at=T0 + timedelta(seconds=1))
    d.update(kw); return ExecutionAttempt(**d)
out = {}
def dec(r): resp, rc = evaluate_financial(r, sealed_at=None); return resp.decision, resp.reason_code, rc
# controls
out["C0_baseline"] = dec(req())[:2]
# T1 mandate not in store -> presented limit
resp = dec(req(mandate_id="MANDATE-NOT-IN-STORE", mandate_max_amount=10**12, amount=5 * 10**11))
out["T1_unknown_mandate_presented_limit"] = resp[:2]
out["T1_snapshot_records_presented_vs_authoritative"] = {k: resp[2].request_snapshot[k] for k in ("presented_mandate_max_amount", "authoritative_mandate_max_amount")}
out["T1_known_mandate_presented_limit_ignored"] = dec(req(mandate_max_amount=10**12, amount=5 * 10**6))[:2]
# T2 negative amount
out["T2_negative_amount"] = dec(req(amount=-50.0))[:2]
# T3 NaN / inf
out["T3_nan"] = dec(req(amount=float("nan")))[:2]
out["T3_inf"] = dec(req(amount=float("inf")))[:2]
out["T3_neg_inf"] = dec(req(amount=float("-inf")))[:2]
# T4 caller-supplied clock: expired mandate + stale screening made to pass by backdating requested_execution_time
real_now_like = T0 + timedelta(days=30)
out["T4_honest_late_clock_expired_mandate"] = dec(req(requested_execution_time=real_now_like))[:2]
out["T4_backdated_clock_same_world"] = dec(req(requested_execution_time=T0))[:2]
out["T4_stale_evidence_via_forward_captured_at"] = dec(req(screening_captured_at=T0 + timedelta(hours=5), screening_max_age_seconds=1))[:2]  # future capture -> age clamped to 0
# T5 int vs float binding
r = req(amount=100.0); resp, rc = evaluate_financial(r)
out["T5_float_receipt_int_attempt"] = validate_execution(rc, att(r, amount=100)).reason_code
out["T5_float_receipt_float_attempt"] = validate_execution(rc, att(r)).reason_code
# T6 control: state advance after receipt
r = req(); resp, rc = evaluate_financial(r)
AS.advance_authority_state_version()
out["T6_after_state_advance"] = validate_execution(rc, att(r)).reason_code
# T7 control: gateway permit twice for same receipt (does the gateway itself enforce single issuance?)
r = req(); resp, rc = evaluate_financial(r)
g1 = validate_execution(rc, att(r)); g2 = validate_execution(rc, att(r))
out["T7_gateway_issues_permit_each_call"] = (g1.status, g2.status)
out["T7_note"] = "single-use is a downstream consumption store, not the gateway; checked below"
# T8 forged receipt without key knowledge: edit decision
import copy
r = req(risk_state="HIGH"); resp, rc = evaluate_financial(r)
rc2 = copy.copy(rc); rc2.decision = "ALLOW"
out["T8_decision_edit_without_key"] = validate_execution(rc2, att(r, attempted_at=T0)).reason_code
print(json.dumps(out, indent=1, default=str))
