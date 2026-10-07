"""CAGE-side S1-S5 + controls. Run from CAGE repo root with its venv. Real Redis on 6391."""
import asyncio, hashlib, json, time, sys
import redis.asyncio as aioredis
from src.gateway.governance.contracts import *  # noqa  (import order: contracts first)
from src.gateway.governance.kms_signer import KMSGovernanceSigner, SoftwareEd25519Provider
from src.gateway.governance.consequence_token import ConsequenceToken
from src.gateway.governance.consequence_authority_store import ConsequenceAuthorityStore
from src.gateway.governance.consequence_gateway import ConsequenceGateway
from src.gateway.governance.jcs_canonicalizer import jcs_canonicalize_plan
import unittest.mock as um

out = {}
def dig(p): return hashlib.sha256(jcs_canonicalize_plan(p)).hexdigest()

async def main():
    r = aioredis.from_url("redis://127.0.0.1:6391", decode_responses=True)
    await r.flushall()
    store = ConsequenceAuthorityStore(r, ttl_seconds=90)
    signer = KMSGovernanceSigner(kms_client=None, key_version_name="", public_key_pem=b"", provider=SoftwareEd25519Provider())
    gw = ConsequenceGateway(store, signer)
    P = {"op": "pay", "amount": 100, "to": "acct-1"}
    def mint(rec, p=P, ver="v1", tid="t", sub="a", ttl=60):
        return ConsequenceToken.mint(sub=sub, tid=tid, rec=rec, act=dig(p), ver=ver, ttl_seconds=ttl, signer=signer)
    ev = lambda e: (e.decision.value, e.reason_code)
    # controls
    tok = mint("c1")
    out["C1_first"] = ev(await gw.evaluate(tok, P))
    out["C2_replay"] = ev(await gw.evaluate(tok, P))
    out["C3_tamper"] = ev(await gw.evaluate(mint("c3"), {**P, "amount": 101}))
    # S1: 'authority state changed' after mint. Token ver="v1"; nothing in gateway takes a current version.
    import inspect
    out["S1_evaluate_signature"] = str(inspect.signature(gw.evaluate))
    out["S1_gateway_source_mentions_ver_compare"] = "claims.ver" in inspect.getsource(ConsequenceGateway.evaluate) and \
        any(("claims.ver" in l and ("!=" in l or "==" in l)) for l in inspect.getsource(ConsequenceGateway.evaluate).splitlines())
    # state 'moves' to v2 (e.g. revocation upstream): no input path exists; token still executes
    out["S1_stale_ver_token_executes"] = ev(await gw.evaluate(mint("s1", ver="v1-REVOKED-UPSTREAM"), P))
    # S2: delete consumption marker, replay inside TTL
    tok2 = mint("s2")
    a = ev(await gw.evaluate(tok2, P))
    keys = await r.keys("flowsignal:token:*")
    await r.delete("flowsignal:token:s2")
    b = ev(await gw.evaluate(tok2, P))
    out["S2"] = {"first": a, "after_marker_delete": b}
    # S3: signer holder mints for fabricated rec never issued by any authority
    out["S3_fabricated_rec"] = ev(await gw.evaluate(mint("never-issued-by-anyone-0001", sub="anyone"), P))
    # S4: boundary
    real = time.time
    tok4 = mint("s4", ttl=60)
    claims = json.loads(__import__("base64").urlsafe_b64decode(tok4.split(".")[1] + "=="))
    exp = claims["exp"]
    res = {}
    for label, t in (("exp-1", exp - 1), ("exp", exp), ("exp+1", exp + 1)):
        await r.flushall()
        with um.patch("time.time", return_value=float(t)):
            try:
                res[label] = ev(await gw.evaluate(tok4, P))
            except Exception as e:
                res[label] = ("EXC", repr(e)[:80])
    out["S4"] = res
    # S5: digest binds whole payload
    base = dig(P)
    out["S5"] = {k: dig({**P, k: v}) != base for k, v in (("memo", "x"), ("amount", 100.0000001), ("to", "acct-2"), ("extra_flag", True))}
    out["S5_int_vs_float_equal"] = dig({**P, "amount": 100.0}) == base
    out["S5_big_int_collide"] = dig({**P, "amount": 2**53 + 1}) == dig({**P, "amount": 2**53})
    print(json.dumps(out, indent=1, default=str))
asyncio.run(main())
