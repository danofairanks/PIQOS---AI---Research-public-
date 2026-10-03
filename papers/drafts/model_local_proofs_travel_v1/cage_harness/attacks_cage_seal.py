"""Attacks on CAGE routing-seal path. usage: python attacks_cage_seal.py <repo_root>  (see PREREG_cage_seal_2026-10-03.md)"""
import sys, os, json, asyncio, hashlib, hmac, time, base64, subprocess
repo = sys.argv[1]; sys.path.insert(0, repo); os.chdir(repo)
os.environ.pop("GOVERNANCE_SALT", None)  # default salt, as shipped
os.environ["CAGE_ENV"] = "test"
import fakeredis
import src.gateway.governance.routing_seal as rs
from src.gateway.governance.routing_seal import (generate_seal, verify_seal, verify_and_consume_seal,
    SymbolicGovernorViolation as V)
R = {}
ACT, P = "execute_trade", {"symbol": "AAPL", "amount": 10.0, "currency": "USD"}
def mode(strict, env):
    os.environ["CAGE_SEAL_STRICT_MODE"] = "true" if strict else "false"
    if env is None: os.environ.pop("CAGE_ENV", None); os.environ.pop("ENVIRONMENT", None)
    else: os.environ["CAGE_ENV"] = env
def tryv(f, *a, **k):
    try: return ("OK", f(*a, **k))
    except V as e: return ("VIOLATION", str(getattr(e, "reason", e))[:80])
    except BaseException as e: return ("OTHER:" + type(e).__name__, str(e)[:80])
async def atry(f, *a, **k):
    try: return ("OK", await f(*a, **k))
    except V as e: return ("VIOLATION", str(getattr(e, "reason", e))[:80])
    except BaseException as e: return ("OTHER:" + type(e).__name__, str(e)[:80])
def forge(key, action, params, ttl=300, rh="fabricated"):
    ex = format(int(time.time()) + ttl, "x"); slug = action.replace("_", "-").replace(".", "-").lower()[:32]
    msg = f"{ex}.{slug}.{rh}.".encode() + rs._canonical_payload(action, params)
    return f"{ex}.{slug}.{rh}.{hmac.new(key, msg, hashlib.sha256).hexdigest()}"
def newredis(): return fakeredis.FakeAsyncRedis()

# S1 forge with default salt
default_key = hashlib.sha256(rs._DEFAULT_SALT.encode()).digest()
f = forge(default_key, "wire_transfer", {"to": "attacker", "amount": 1e6})
mode(True, "test");  s1_strict = tryv(verify_seal, f, "wire_transfer", {"to": "attacker", "amount": 1e6})
mode(True, None);    s1_prod = tryv(verify_seal, f, "wire_transfer", {"to": "attacker", "amount": 1e6})
mode(False, "test"); s1_nonstrict = tryv(verify_seal, f, "wire_transfer", {"to": "attacker", "amount": 1e6})
fw = forge(hashlib.sha256(b"other").digest(), "wire_transfer", {"to": "attacker", "amount": 1e6})
s1_wrong = tryv(verify_seal, fw, "wire_transfer", {"to": "attacker", "amount": 1e6})
R["S1"] = dict(forged_strict_test_env=s1_strict, forged_prod_env=s1_prod, forged_nonstrict_test_env=s1_nonstrict, wrong_key_nonstrict=s1_wrong)

mode(False, "test")  # remaining attacks run in the mode the repo's tests use
async def main():
    # S2 replay
    r = newredis(); s = generate_seal(ACT, P, record_hash="rh1")
    a = await atry(verify_and_consume_seal, s, ACT, P, r); b = await atry(verify_and_consume_seal, s, ACT, P, r)
    c = await atry(verify_and_consume_seal, str(s), ACT, dict(P), r)
    R["S2"] = dict(first=a, same_string_again=b, value_copy=c)
    # S3 two issuances
    r = newredis(); s1 = generate_seal(ACT, P, record_hash="rh1"); time.sleep(1.1); s2 = generate_seal(ACT, P, record_hash="rh1")
    s3 = generate_seal(ACT, P, record_hash="rh1")
    x = [await atry(verify_and_consume_seal, q, ACT, P, r) for q in (s1, s2)]
    y = await atry(verify_and_consume_seal, s3, ACT, P, r)
    R["S3"] = dict(two_issuances_1s_apart=x, same_second_as_s2_identical_string=(s2 == s3), third_consume=y)
    # S4 concurrency
    r = newredis(); s = generate_seal(ACT, P, record_hash="rh1")
    res = await asyncio.gather(*[atry(verify_and_consume_seal, s, ACT, P, r) for _ in range(50)])
    R["S4"] = dict(winners=sum(1 for t in res if t[0] == "OK"), n=50)
    # S5 canonicalisation
    r = newredis()
    s = generate_seal(ACT, {"x": [1, 2]}, record_hash="rh1")
    R["S5"] = dict(list_vs_string=tryv(verify_seal, s, ACT, {"x": "[1, 2]"}), same_params=tryv(verify_seal, s, ACT, {"x": [1, 2]}),
        control_different_value=tryv(verify_seal, s, ACT, {"x": "[1, 3]"}))
    sd = generate_seal(ACT, {"x": {"a": 1, "b": 2}}, record_hash="rh1")
    R["S5"]["nested_reordered"] = tryv(verify_seal, sd, ACT, {"x": {"b": 2, "a": 1}})
    R["S5"]["nested_dict_vs_its_str"] = tryv(verify_seal, sd, ACT, {"x": str({"a": 1, "b": 2})})
    # S6 action variation
    s = generate_seal(ACT, P, record_hash="rh1")
    R["S6"] = dict(same=tryv(verify_seal, s, ACT, P), case=tryv(verify_seal, s, "Execute_Trade", P), dash=tryv(verify_seal, s, "execute-trade", P))
    # S7 record_hash
    r = newredis(); s = generate_seal(ACT, P, record_hash="fabricated-not-in-any-chain")
    R["S7"] = dict(no_expected=await atry(verify_and_consume_seal, s, ACT, P, r),
        wrong_expected=await atry(verify_and_consume_seal, generate_seal(ACT, P, record_hash="fab2"), ACT, P, newredis(), "other"),
        sentinel_seal=tryv(verify_seal, generate_seal(ACT, P), ACT, P), require_evidence_binding_flag=bool(rs._REQUIRE_EVIDENCE_BINDING))
    # S8 malformed
    r = newredis(); s = generate_seal(ACT, P, record_hash="rh1")
    R["S8"] = dict(seal_none=await atry(verify_and_consume_seal, None, ACT, P, r), seal_int=await atry(verify_and_consume_seal, 5, ACT, P, r),
        params_none=await atry(verify_and_consume_seal, s, ACT, None, r), params_list=await atry(verify_and_consume_seal, s, ACT, [1], r),
        action_none=await atry(verify_and_consume_seal, s, None, P, r), control_bad_string=await atry(verify_and_consume_seal, "garbage", ACT, P, r))
    # S9 expiry
    R["S9"] = dict(expired=tryv(verify_seal, generate_seal(ACT, P, ttl_s=-5, record_hash="rh1"), ACT, P),
        huge_ttl=tryv(verify_seal, generate_seal(ACT, P, ttl_s=10**9, record_hash="rh1"), ACT, P))
    # S10 redis down
    class Down:
        async def eval(self, *a, **k): raise ConnectionError("down")
        async def evalsha(self, *a, **k): raise ConnectionError("down")
        async def script_load(self, *a, **k): raise ConnectionError("down")
    R["S10"] = dict(down=await atry(verify_and_consume_seal, generate_seal(ACT, P, record_hash="rh1"), ACT, P, Down()))
    # S11 jwt
    def b(o): return base64.urlsafe_b64encode(json.dumps(o).encode()).rstrip(b"=").decode()
    ah = hashlib.sha256(rs.jcs_canonicalize_plan({"action": ACT, **P})).hexdigest()
    pl = {"action_hash": ah, "record_hash": "x", "nonce": "n1", "iat": int(time.time()), "exp": int(time.time()) + 300, "iss": "cage-gateway"}
    none_tok = f"{b({'alg':'none','typ':'JWT'})}.{b(pl)}."
    kid_tok = f"{b({'alg':'ES256','typ':'JWT','kid':'attacker'})}.{b(pl)}.AAAA"
    R["S11"] = dict(alg_none=tryv(verify_seal, none_tok, ACT, P), unknown_kid=tryv(verify_seal, kid_tok, ACT, P),
        none_consume=await atry(verify_and_consume_seal, none_tok, ACT, P, newredis()))
    # S13 prod-like, default salt
    mode(True, None)
    R["S13"] = dict(hmac_in_prod_like=tryv(verify_seal, generate_seal(ACT, P, record_hash="rh1"), ACT, P))
asyncio.run(main())
# S12 code reading
src = open("src/gateway/governance/routing_seal.py").read()
R["S12"] = {k: (k in src.lower()) for k in ("revoke", "revocation", "revoked", "blocklist", "denylist")}
print(json.dumps(R, indent=1, default=str))
