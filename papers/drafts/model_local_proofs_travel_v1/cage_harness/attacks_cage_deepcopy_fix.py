"""Tests the deepcopy-at-govern()-entry fix. mode: 'unpatched' | 'patched'. Same env as attacks_cage_pipeline.py. See PREREG_cage_deepcopy_fix_2026-10-03.md"""
import asyncio, json, logging, copy, sys, hashlib, threading
logging.disable(logging.CRITICAL)
from unittest.mock import AsyncMock
import src.cage_finance.tiers.causal_tier as ct
ct.causal_safety_check = lambda p, t: True
from src.gateway.governance.env_posture import DeploymentPosture
from src.gateway.governance.governor.assembly import assemble_governor
from src.gateway.governance.governor.governor import SymbolicGovernor
from src.gateway.governance.evidence.stream import start_evidence_sink, get_evidence_sink
from src.gateway.governance import routing_seal as rs
from src.gateway.governance.jcs_canonicalizer import jcs_canonicalize_plan
from src.cage_finance.plugin import FinanceCagePlugin
MODE = sys.argv[1]
if MODE == "patched":
    _orig = SymbolicGovernor.govern
    async def govern(self, tool_name, params):
        return await _orig(self, tool_name, copy.deepcopy(params))
    SymbolicGovernor.govern = govern
R = {"mode": MODE}
def mkgov(opa):
    gv = assemble_governor([FinanceCagePlugin()], posture=DeploymentPosture.DEV, opa=opa)
    from src.gateway.governance.constants import register_overlay_dir
    for c in gv.components.contributions:
        for d in c.compliance_overlay_dirs: register_overlay_dir(d)
    return gv
def allow_opa():
    o = AsyncMock(); o.evaluate_policy.return_value = "ALLOW"; return o
BASE = {"symbol": "AAPL", "amount": 10.0, "confidence": 0.99, "trader_id": "a", "trader_role": "trader", "latency_ms": 50, "drawdown": 0.01, "currency": "USD"}
def short(e): return f"{type(e).__name__}: {str(e)[:90]}"
def tv(seal, p):
    try: return rs.verify_seal(seal, "execute_trade", p)
    except BaseException as e: return "REJECT"
def phash(p):
    def n(o):
        if isinstance(o, dict): return {k: n(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [n(i) for i in o]
        return o if isinstance(o, (str, int, float, bool, type(None))) else str(o)
    return hashlib.sha256(jcs_canonicalize_plan(n(p))).hexdigest()[:16]
async def main():
    await start_evidence_sink(); g = mkgov(allow_opa()); sink = get_evidence_sink(); orig = sink.ingest_sync
    # F1
    p = dict(BASE); s = await g.govern("execute_trade", p)
    R["F1"] = dict(seal_verifies=tv(s, p), rejects_11=tv(s, {**p, "amount": 11.0}))
    # F2 / F4 / F6: mutate during ingest
    for label, mk, mutate in [("F2_amount", lambda: dict(BASE), lambda d: d.__setitem__("amount", 1_000_000.0)),
                               ("F4_nested", lambda: {**BASE, "meta": {"tags": ["a"]}}, lambda d: (d["meta"]["tags"].append("evil"), d.__setitem__("amount", 1_000_000.0)))]:
        pb = mk(); original = copy.deepcopy(pb); seen = {}
        async def mut(d): await asyncio.sleep(0); mutate(d)
        async def hooked(ev, **k):
            seen["ev_hash"] = ev["params_hash"]; asyncio.get_running_loop().create_task(mut(pb)); return await orig(ev, **k)
        sink.ingest_sync = hooked
        try:
            sb = await g.govern("execute_trade", pb); r = dict(result="SEAL", verifies_original=tv(sb, original), verifies_mutated=tv(sb, pb),
                    evidence_hash_equals_original=(seen.get("ev_hash") == phash(original)), evidence_hash_equals_mutated=(seen.get("ev_hash") == phash(pb)))
        except BaseException as e: r = dict(result="REFUSED", why=short(e))
        sink.ingest_sync = orig; R[label] = r
    # F3 mutate during OPA
    for mv in (9999.0, 1_000_000.0):
        pa = dict(BASE); original = dict(BASE)
        async def mut(d, mv=mv): await asyncio.sleep(0); d["amount"] = mv
        async def opa_mut(payload, pa=pa, mut=mut):
            asyncio.get_running_loop().create_task(mut(pa)); await asyncio.sleep(0.01); return "ALLOW"
        oa = AsyncMock(); oa.evaluate_policy.side_effect = opa_mut; ga = mkgov(oa)
        try:
            sa = await ga.govern("execute_trade", pa); R[f"F3_{int(mv)}"] = dict(result="SEAL", verifies_original=tv(sa, original), verifies_mutated=tv(sa, pa))
        except BaseException as e: R[f"F3_{int(mv)}"] = dict(result="REFUSED", why=short(e))
    # F5 non-deepcopyable
    try:
        s5 = await g.govern("execute_trade", {**BASE, "lock": threading.Lock()}); R["F5"] = dict(result="SEAL", seal=s5[:14])
    except BaseException as e: R["F5"] = dict(result="REFUSED", why=short(e))
asyncio.run(main())
print(json.dumps(R, indent=1, default=str))
