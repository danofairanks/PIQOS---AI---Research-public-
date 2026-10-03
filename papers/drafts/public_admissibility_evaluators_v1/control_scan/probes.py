#!/usr/bin/env python3
"""Control-scan probes on four unrelated authorization libraries. Run in a venv with PyJWT, itsdangerous, casbin, pymacaroons installed.
Predictions were written before this file (internal history)."""
import base64, inspect, json, os, tempfile, time, warnings
warnings.filterwarnings("ignore")
from importlib.metadata import version
out = {"versions": {n: version(n) for n in ("PyJWT", "itsdangerous", "casbin", "pymacaroons")}}

def attempt(f):
    try: return {"accepted": True, "value": repr(f())[:60]}
    except BaseException as e: return {"accepted": False, "error": type(e).__name__}

# ---- PyJWT
import jwt
now = int(time.time()); key = "k" * 32
tok_expired = jwt.encode({"sub": "alice", "exp": now - 100}, key, algorithm="HS256")
tok_ok = jwt.encode({"sub": "alice", "exp": now + 100}, key, algorithm="HS256")
h, p, s = tok_ok.split(".")
def b64(d): return base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
tampered = ".".join([h, b64({"sub": "mallory", "exp": now + 100}), s])
none_tok = jwt.encode({"sub": "mallory", "exp": now + 100}, None, algorithm="none")
J = {}
J["Q1_expired_default"] = attempt(lambda: jwt.decode(tok_expired, key, algorithms=["HS256"]))
J["Q1_expired_leeway_1000"] = attempt(lambda: jwt.decode(tok_expired, key, algorithms=["HS256"], leeway=1000))
J["Q1_expired_verify_exp_false"] = attempt(lambda: jwt.decode(tok_expired, key, algorithms=["HS256"], options={"verify_exp": False}))
J["Q1b_decode_has_clock_param"] = any(n in inspect.signature(jwt.decode).parameters for n in ("now", "clock", "timestamp", "current_time"))
J["Q2_replay_twice"] = [attempt(lambda: jwt.decode(tok_ok, key, algorithms=["HS256"]))["accepted"] for _ in range(2)]
J["Q3_tampered_payload"] = attempt(lambda: jwt.decode(tampered, key, algorithms=["HS256"]))
J["Q6_wrong_types"] = {t: attempt(lambda t=t: jwt.decode(eval(t), key, algorithms=["HS256"])) for t in ("None", "123", "[1]")}
J["Q7_none_default_list"] = attempt(lambda: jwt.decode(none_tok, key, algorithms=["HS256"]))
J["Q7_none_listed_by_caller"] = attempt(lambda: jwt.decode(none_tok, None, algorithms=["none"]))
J["Q7_none_listed_verify_signature_false"] = attempt(lambda: jwt.decode(none_tok, None, algorithms=["none"], options={"verify_signature": False}))
J["Q8_verify_signature_false_accepts_forged"] = attempt(lambda: jwt.decode(tampered, options={"verify_signature": False}))
out["PyJWT"] = J

# ---- itsdangerous
from itsdangerous import TimestampSigner, URLSafeTimedSerializer, BadSignature
class OldSigner(TimestampSigner):
    def get_timestamp(self): return int(time.time()) - 1000
old = OldSigner("secret").sign("payload")
fresh = TimestampSigner("secret").sign("payload")
ts = TimestampSigner("secret"); I = {}
I["Q1_old_max_age_10"] = attempt(lambda: ts.unsign(old, max_age=10))
I["Q1_old_default_no_max_age"] = attempt(lambda: ts.unsign(old))
I["Q1b_unsign_has_clock_param"] = any(n in inspect.signature(ts.unsign).parameters for n in ("now", "clock", "timestamp", "current_time"))
I["Q2_replay_twice"] = [attempt(lambda: ts.unsign(fresh, max_age=100))["accepted"] for _ in range(2)]
ser = URLSafeTimedSerializer("secret"); tkn = ser.dumps({"u": "alice"}); a, b, c = tkn.rsplit(".", 2) if tkn.count(".") >= 2 else (tkn, "", "")
I["Q3_tampered"] = attempt(lambda: ser.loads(a + "x." + b + "." + c, max_age=100))
I["Q6_wrong_types"] = {t: attempt(lambda t=t: ser.loads(eval(t), max_age=100)) for t in ("None", "123", "[1]")}
out["itsdangerous"] = I

# ---- casbin
import casbin
d = tempfile.mkdtemp(); mp = os.path.join(d, "m.conf"); pp = os.path.join(d, "p.csv")
open(mp, "w").write("[request_definition]\nr = sub, obj, act\n[policy_definition]\np = sub, obj, act\n[policy_effect]\ne = some(where (p.eft == allow))\n[matchers]\nm = r.sub == p.sub && keyMatch(r.obj, p.obj) && r.act == p.act\n")
open(pp, "w").write("p, alice, /data/*, read\n")
e = casbin.Enforcer(mp, pp); C = {}
C["control_in_scope"] = e.enforce("alice", "/data/file", "read")
C["control_out_of_scope"] = e.enforce("alice", "/secret", "read")
C["Q5_traversal_string_matches_wildcard"] = e.enforce("alice", "/data/../secret", "read")
C["Q8_caller_asserts_subject"] = e.enforce("alice", "/data/x", "read")
C["Q6_wrong_types"] = {t: attempt(lambda t=t: e.enforce(*eval(t))) for t in ("(None, '/data/x', 'read')", "(1, 2, 3)", "('alice',)")}
out["casbin"] = C

# ---- pymacaroons
from pymacaroons import Macaroon, Verifier
from datetime import datetime, timezone
m = Macaroon(location="loc", identifier="id", key="secretkey"); m.add_first_party_caveat("time < 2020-01-01T00:00:00Z")
def time_ok(pred):
    if pred.startswith("time < "):
        return datetime.now(timezone.utc) < datetime.strptime(pred[7:], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return False
M = {}
v1 = Verifier(); v1.satisfy_general(time_ok)
M["Q1_expired_with_time_checking_callback"] = attempt(lambda: v1.verify(m, "secretkey"))
v2 = Verifier(); v2.satisfy_general(lambda pred: True)
M["Q1b_Q8_expired_with_callback_returning_true"] = attempt(lambda: v2.verify(m, "secretkey"))
good = Macaroon(location="loc", identifier="id", key="secretkey"); good.add_first_party_caveat("account = alice")
v3 = Verifier(); v3.satisfy_exact("account = alice")
M["Q2_replay_twice"] = [attempt(lambda: v3.verify(good, "secretkey"))["accepted"] for _ in range(2)]
import copy
stripped = copy.deepcopy(good); stripped.caveats.pop()
M["Q3_stripped_caveat"] = attempt(lambda: Verifier().verify(stripped, "secretkey"))
retag = Macaroon(location="loc", identifier="other", signature=good.signature)  # no key: the attacker does not hold it
M["Q3_changed_identifier_same_signature"] = attempt(lambda: v3.verify(retag, "secretkey"))
M["Q3_control_minting_with_key_is_legitimate"] = attempt(lambda: v3.verify(Macaroon(location="loc", identifier="other", key="secretkey"), "secretkey"))
M["Q6_wrong_types"] = {t: attempt(lambda t=t: v3.verify(eval(t), "secretkey")) for t in ("None", "123", "[1]")}
out["pymacaroons"] = M
print(json.dumps(out, indent=1))
