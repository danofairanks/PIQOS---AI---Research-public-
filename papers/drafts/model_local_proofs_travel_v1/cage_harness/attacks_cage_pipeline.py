"""CAGE governor pipeline attacks. Env: CAGE_ENV=test CAGE_SEAL_STRICT_MODE=false CAGE_DOMAIN=finance EVIDENCE_STREAM_ENABLED=true REDIS_URL=redis://localhost:6379; PYTHONPATH=<repo>; needs redis-server on 6379 and the plugin entry point installed. See PREREG_cage_pipeline_2026-10-03.md"""
import asyncio, json, logging, math, copy, sys
logging.disable(logging.CRITICAL)
from unittest.mock import AsyncMock
import src.cage_finance.tiers.causal_tier as ct
ct.causal_safety_check = lambda p, t: True          # disclosed stub
from src.gateway.governance.env_posture import DeploymentPosture
from src.gateway.governance.governor.assembly import assemble_governor
from src.gateway.governance.governor.pipeline import UNGOVERNED_STAGES
from src.gateway.governance.evidence.stream import start_evidence_sink, get_evidence_sink
from src.gateway.governance.schemas.thresholds import get_agent_confidence_threshold
from src.gateway.governance import routing_seal as rs
from src.cage_finance.plugin import FinanceCagePlugin
R = {}
def mkgov(opa):
    gv = assemble_governor([FinanceCagePlugin()], posture=DeploymentPosture.DEV, opa=opa)
    from src.gateway.governance.constants import register_overlay_dir   # as bootstrap_governor does
    for c in gv.components.contributions:
        for d in c.compliance_overlay_dirs: register_overlay_dir(d)
    return gv
def allow_opa():
    o = AsyncMock(); o.evaluate_policy.return_value = "ALLOW"; return o
BASE = {"symbol": "AAPL", "amount": 10.0, "confidence": 0.99, "trader_id": "a", "trader_role": "trader",
        "latency_ms": 50, "drawdown": 0.01, "currency": "USD"}
def short(e): return f"{type(e).__name__}: {str(e)[:90]}"
async def gov(g, name, params):
    try:
        s = await g.govern(name, params); return ("SEAL", s[:14])
    except BaseException as e: return ("REFUSED", short(e))
def v(seal_params):  # verify helper
    return None

async def main():
    await start_evidence_sink()
    opa = allow_opa(); g = mkgov(opa)
    thr = get_agent_confidence_threshold(); R["threshold"] = thr; R["UNGOVERNED_STAGES"] = sorted(UNGOVERNED_STAGES)
    # G1
    p = dict(BASE); s = await g.govern("execute_trade", p)
    R["G1"] = dict(control=("SEAL", s[:14]), seal_verifies=rs.verify_seal(s, "execute_trade", p),
                   verifies_other_params=_tv(s, "execute_trade", {**p, "amount": 11.0}))
    # G2
    R["G2"] = {}
    for n in ("check_balance", "prompt_injection_check"):
        R["G2"][n] = dict(empty=await gov(g, n, {}), conf0=await gov(g, n, {"confidence": 0.0}),
                          big_amount=await gov(g, n, {"amount": 1e9, "symbol": "AAPL"}))
    # G3
    R["G3"] = {n: await gov(g, n, dict(BASE)) for n in ("Execute_Trade", "execute_trade ", "execute_trade​", "execute-trade", "EXECUTE_TRADE", "ｅxecute_trade", "execute_trade\n")}
    # G4
    R["G4"] = {}
    for label, c in [("None", None), ("str", "0.99"), ("True", True), ("nan", float("nan")), ("inf", float("inf")), ("-1", -1), ("1.5", 1.5),
                     ("below", thr - 0.01), ("at_threshold", thr), ("1.0", 1.0), ("missing", "__missing__")]:
        q = dict(BASE); 
        if c == "__missing__": q.pop("confidence")
        else: q["confidence"] = c
        R["G4"][label] = await gov(g, "execute_trade", q)
    # G5
    R["G5"] = {}
    for label, a in [("str10", "10"), ("True", True), ("-5", -5), ("0", 0), ("nan", float("nan")), ("inf", float("inf")), ("1e308", 1e308),
                     ("None", None), ("missing", "__missing__"), ("list", [10]), ("10001", 10001.0), ("10000", 10000.0), ("20000", 20000.0)]:
        q = dict(BASE)
        if a == "__missing__": q.pop("amount")
        else: q["amount"] = a
        R["G5"][label] = await gov(g, "execute_trade", q)
    # G5x post-hoc follow-up (not preregistered): string amounts
    R["G5x_posthoc"] = {}
    for label, a in [("str20000", "20000"), ("str1e6", "1000000"), ("str-5", "-5"), ("str0", "0"), ("strnan", "nan"), ("str_abc", "abc"), ("str_1e308", "1e308"), ("int_10", 10), ("int_20000", 20000)]:
        R["G5x_posthoc"][label] = await gov(g, "execute_trade", {**BASE, "amount": a})
    # G6
    R["G6"] = {}
    base_bad = {**BASE, "amount": 20000.0}
    R["G6"]["control_20000"] = await gov(g, "execute_trade", dict(base_bad))
    for k, val in [("approved", True), ("hitl_approved", True), ("skip_governance", True), ("policy_decision", "ALLOW"), ("deferred_id", "x"), ("human_approved", True)]:
        R["G6"][f"smuggle_{k}"] = await gov(g, "execute_trade", {**base_bad, k: val})
    cap = AsyncMock(); cap.evaluate_policy.return_value = "ALLOW"; g2 = mkgov(cap)
    await gov(g2, "execute_trade", {**BASE, "action": "check_balance", "tool_input": {"evil": 1}})
    pay = cap.evaluate_policy.call_args[0][0]
    R["G6"]["opa_payload_action"] = pay.get("action"); R["G6"]["opa_payload_tool_input_is_params"] = ("evil" not in json.dumps(pay.get("tool_input")))
    # G7
    R["G7"] = {}
    # (b) mutate during evidence ingest
    sink = get_evidence_sink(); orig = sink.ingest_sync; pb = dict(BASE); pb["amount"] = 10.0
    MUTV = float(sys.argv[1]) if len(sys.argv) > 1 else 9999.0
    async def mut(d): await asyncio.sleep(0); d["amount"] = MUTV
    async def hooked(ev, **k):
        asyncio.get_running_loop().create_task(mut(pb)); return await orig(ev, **k)
    sink.ingest_sync = hooked
    try:
        sb = await g.govern("execute_trade", pb); sink.ingest_sync = orig
        R["G7"]["b_ingest"] = dict(result="SEAL", amount_after=pb["amount"], verifies_mutated=rs.verify_seal(sb, "execute_trade", pb),
                                   verifies_original=_tv(sb, "execute_trade", {**BASE, "amount": 10.0}))
    except BaseException as e:
        sink.ingest_sync = orig; R["G7"]["b_ingest"] = dict(result="REFUSED", why=short(e), amount_after=pb["amount"])
    # (a) mutate during OPA await
    pa = dict(BASE); pa["amount"] = 10.0
    async def opa_mut(payload):
        asyncio.get_running_loop().create_task(mut(pa)); await asyncio.sleep(0.01); return "ALLOW"
    oa = AsyncMock(); oa.evaluate_policy.side_effect = opa_mut; ga = mkgov(oa)
    try:
        sa = await ga.govern("execute_trade", pa)
        R["G7"]["a_opa"] = dict(result="SEAL", amount_after=pa["amount"], verifies_mutated=rs.verify_seal(sa, "execute_trade", pa))
    except BaseException as e:
        R["G7"]["a_opa"] = dict(result="REFUSED", why=short(e), amount_after=pa["amount"])
    # G8
    R["G8"] = {}
    for label, resp in [("ALLOW", "ALLOW"), ("space_lower", " allow "), ("True", True), ("dict_decision_true", {"decision": True}), ("int1", 1),
                        ("ALLOW_WITH_CONDITIONS", "ALLOW_WITH_CONDITIONS"), ("allow_yes", {"allow": "yes"}), ("None", None), ("exception", RuntimeError("boom"))]:
        o = AsyncMock()
        if isinstance(resp, Exception): o.evaluate_policy.side_effect = resp
        else: o.evaluate_policy.return_value = resp
        R["G8"][label] = await gov(mkgov(o), "execute_trade", dict(BASE))
    # G9
    from src.gateway.server.governance_middleware import enforce_governance
    R["G9"] = {}
    for n in ("check_market_status", "verify_content_safety", "Check_Market_Status", "check_market_status ", "check-market-status"):
        try: R["G9"][n] = ("RETURNED", repr(await enforce_governance(g, n, {})))
        except BaseException as e: R["G9"][n] = ("RAISED", short(e))
    # G10
    seals = 0; first_ref = None
    for i in range(300):
        r = await gov(g, "execute_trade", {**BASE, "amount": 5000.0})
        if r[0] == "SEAL": seals += 1
        else: first_ref = r[1]; break
    await asyncio.sleep(2)
    again = await gov(g, "execute_trade", {**BASE, "amount": 5000.0})
    R["G10"] = dict(seals_minted_unsettled=seals, first_refusal=first_ref, after_2s_wait=again)
def _tv(seal, a, p):
    try: return rs.verify_seal(seal, a, p)
    except BaseException as e: return "REJECT:" + short(e)
asyncio.run(main())
print(json.dumps(R, indent=1, default=str))
