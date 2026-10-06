"""CAGE provider_06 side of the comparison. Run from CAGE repo root, CAGE_ENV=development. Inputs: upstream_gen_out.json."""
import asyncio, base64, hashlib, json, sys, datetime as dt
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
from src.gateway.governance.contracts import *  # noqa  import order
from src.gateway.governance.jcs_canonicalizer import jcs_canonicalize_plan
from src.integrations.provider_06 import adapter as A
from src.integrations.provider_06.signature import verify_receipt_digest, verify_receipt_signature

up = json.load(open(sys.argv[1]))
out = {}
priv = Ed25519PrivateKey.generate(); pub = priv.public_key()
class FakeJWKS:
    def __init__(self, keys): self.keys = keys
    async def get_key(self, kid): return self.keys.get(kid)
def adapter(keys, endpoint="http://x"):
    a = A.Provider06AgentIntegrityAdapter(endpoint=endpoint)
    a._jwks_client = FakeJWKS(keys) if keys is not None else None
    return a

def cage_receipt(evidence="EV", status="PASS", issuer="test-issuer", audience="cage-test", purpose="verification",
                 created=None, expires="default", sigenc="url_nopad", key=priv, kid="k1", nonce="n1"):
    now = datetime.now(timezone.utc)
    body = {"protocolVersion": "1-alpha", "receiptVersion": "2-alpha", "engineVersion": "x", "issuer": issuer, "audience": audience,
            "purpose": purpose, "nonce": nonce, "runId": "r1", "createdAt": (created or now).isoformat(),
            "policyDigest": "p" * 64, "envelopeDigest": evidence,
            "verification": {"protocolVersion": "1-alpha", "status": status, "findings": []}}
    if expires == "default": body["expiresAt"] = (now + timedelta(minutes=30)).isoformat()
    elif expires is not None: body["expiresAt"] = expires
    pb = jcs_canonicalize_plan(body); sig = key.sign(pb)
    enc = {"url_nopad": base64.urlsafe_b64encode(sig).decode().rstrip("="), "std_pad": base64.b64encode(sig).decode(),
           "url_pad": base64.urlsafe_b64encode(sig).decode()}[sigenc]
    return {**body, "signature": {"algorithm": "Ed25519", "keyId": kid, "value": enc}, "receiptDigest": hashlib.sha256(pb).hexdigest()}

class Resp:
    def __init__(self, data): self._d = data
    def raise_for_status(self): pass
    def json(self): return self._d
def client_for(data):
    class C:
        def __init__(s, *a, **k): pass
        async def __aenter__(s): return s
        async def __aexit__(s, *a): return False
        async def post(s, url, **k): return Resp(data)
    return C
async def submit(a, receipt, evidence="EV"):
    with patch("httpx.AsyncClient", client_for(receipt)):
        s = await a.submit_evidence("t1", evidence)
    return {"error": s.error, "seal": bool(s.seal_hash)}

async def main():
    keys = {"k1": pub}
    # controls
    r = cage_receipt()
    out["C_valid_cage_scheme"] = await submit(adapter(keys), r)
    t = json.loads(json.dumps(r)); t["verification"]["status"] = "PASS"; t["audience"] = "x"
    out["C_tampered_body"] = await submit(adapter(keys), t)
    out["C_unknown_kid"] = await submit(adapter({}), r)
    # U0 genuine upstream receipt
    g = up["receipt"]; gpub = serialization.load_pem_public_key(up["publicKeyPem"].encode())
    out["U0"] = {"digest_ok": verify_receipt_digest(g), "sig_ok": verify_receipt_signature(g, gpub),
                 "adapter_submit": await submit(adapter({up["keyId"]: gpub}), g, evidence=g["envelopeDigest"]),
                 "sig_value_len": len(g["signature"]["value"]), "sig_value_has_plus_or_slash": ("+" in g["signature"]["value"] or "/" in g["signature"]["value"])}
    # what would CAGE need? compute upstream's digest definition on genuine receipt to show the definitional difference
    body_wo_digest = {k: v for k, v in g.items() if k != "receiptDigest"}
    out["U0"]["upstream_digest_def_matches_genuine"] = hashlib.sha256(jcs_canonicalize_plan(body_wo_digest)).hexdigest() == g["receiptDigest"]
    out["U0"]["cage_digest_def_matches_genuine"] = verify_receipt_digest(g)
    ub = {"protected": {"algorithm": g["signature"]["algorithm"], "keyId": g["signature"]["keyId"]}, "body": {k: v for k, v in g.items() if k not in ("receiptDigest", "signature")}}
    try:
        gpub.verify(base64.b64decode(g["signature"]["value"]), jcs_canonicalize_plan(ub)); out["U0"]["upstream_sig_def_verifies_with_jcs"] = True
    except Exception as e: out["U0"]["upstream_sig_def_verifies_with_jcs"] = f"False ({type(e).__name__})"
    # A1 subject mismatch
    out["A1_envelope_digest_mismatch"] = await submit(adapter(keys), cage_receipt(evidence="SOMETHING-ELSE"), evidence="EV")
    # A2 signed BLOCKED
    out["A2_signed_BLOCKED_receipt"] = await submit(adapter(keys), cage_receipt(status="BLOCKED"))
    # A3 issuer/audience/purpose
    out["A3_wrong_issuer"] = await submit(adapter(keys), cage_receipt(issuer="evil"))
    out["A3_wrong_audience"] = await submit(adapter(keys), cage_receipt(audience="someone-else"))
    out["A3_wrong_purpose"] = await submit(adapter(keys), cage_receipt(purpose="anything"))
    # A4
    out["A4_missing_expiresAt"] = await submit(adapter(keys), cage_receipt(expires=None))
    out["A4_malformed_expiresAt"] = await submit(adapter(keys), cage_receipt(expires="not-a-date"))
    # A5
    now = datetime.now(timezone.utc)
    out["A5_created_1y_future"] = await submit(adapter(keys), cage_receipt(created=now + timedelta(days=365)))
    out["A5_lifetime_10y"] = await submit(adapter(keys), cage_receipt(expires=(now + timedelta(days=3650)).isoformat()))
    # A6 replay
    a = adapter(keys); rr = cage_receipt(); out["A6_replay"] = [await submit(a, rr), await submit(a, rr)]
    # A7 boundary: freeze 'now' == expiresAt
    exp = datetime(2030, 1, 1, tzinfo=timezone.utc)
    class FrozenDT(datetime):
        @classmethod
        def now(cls, tz=None): return exp if tz else exp.replace(tzinfo=None)
    with patch.object(A, "datetime", FrozenDT):
        out["A7_now_equals_expiresAt"] = await submit(adapter(keys), cage_receipt(expires=exp.isoformat()))
        out["A7_one_second_after"] = None
    with patch.object(A, "datetime", type("F2", (datetime,), {"now": classmethod(lambda cls, tz=None: exp + timedelta(seconds=1))})):
        out["A7_one_second_after"] = await submit(adapter(keys), cage_receipt(expires=exp.isoformat()))
    # A8 signature encodings (CAGE-scheme receipts; digest excludes signature so digest is identical across encodings)
    base = cage_receipt()
    raw = base64.urlsafe_b64decode(base["signature"]["value"] + "==")
    encs = {"url_nopad": base64.urlsafe_b64encode(raw).decode().rstrip("="), "std_pad": base64.b64encode(raw).decode(), "url_pad": base64.urlsafe_b64encode(raw).decode()}
    variants = {k: {**base, "signature": {**base["signature"], "value": v}} for k, v in encs.items()}
    out["A8_sig_encodings"] = {k: (await submit(adapter(keys), v))["error"] is None for k, v in variants.items()}
    out["A8_distinct_signature_strings"] = len({v["signature"]["value"] for v in variants.values()})
    out["A8_digest_identical_across_encodings"] = len({v["receiptDigest"] for v in variants.values()}) == 1
    # A9 validate_fria with JWKS configured and unsigned PASS
    a = adapter(keys)
    with patch("httpx.AsyncClient", client_for({"protocolVersion": "1-alpha", "status": "PASS", "findings": []})):
        v = await a.validate_fria({"anything": 1})
    out["A9_validate_fria_unsigned_PASS"] = {"admitted": v.admitted, "error": v.error}
    # A10 no key manifest configured: any receipt JSON sealed
    forged = {"receiptDigest": "f" * 64, "foo": "bar"}
    out["A10_no_manifest_forged_receipt"] = await submit(adapter(None), forged)
    print(json.dumps(out, indent=1, default=str))
asyncio.run(main())
