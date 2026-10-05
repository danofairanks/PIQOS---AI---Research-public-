import asyncio, base64, json, os, sys, time, hashlib
os.environ["CAGE_SEAL_STRICT_MODE"]="false"; os.environ["CAGE_ENV"]="test"
for k in ("ENVIRONMENT",): os.environ.pop(k,None)
from decimal import Decimal
import redis.asyncio as aioredis
from src.gateway.governance import kms_signer as ks
from src.gateway.governance.consequence_token import ConsequenceToken, ConsequenceTokenError
from src.gateway.governance.consequence_authority_store import ConsequenceAuthorityStore
from src.gateway.governance.consequence_gateway import ConsequenceGateway, ConsequenceDecision
from src.gateway.governance.jcs_canonicalizer import jcs_canonicalize_plan
import src.gateway.governance.evidence.stream as stream_mod
R={}
signer=ks.KMSGovernanceSigner(provider=ks.SoftwareEd25519Provider())
PAY={"action":"transfer","account_id":"A1","amount":100}
def dig(p): return hashlib.sha256(jcs_canonicalize_plan(p)).hexdigest()
def mint(payload=PAY, rec="rec-1", ttl=60, sub="u1", tid="t1", ver="v1"):
    return ConsequenceToken.mint(sub=sub,tid=tid,rec=rec,act=dig(payload),ver=ver,ttl_seconds=ttl,signer=signer)
class FakeSink:
    def __init__(self, exc=None): self.exc=exc; self.n=0
    async def ingest(self, ev):
        self.n+=1
        if self.exc: raise self.exc
        return "id"
async def ev(gw, tok, payload=PAY):
    try:
        e=await gw.evaluate(tok,payload); return (e.decision.value,e.reason_code)
    except Exception as ex: return ('EXCEPTION',type(ex).__name__+': '+str(ex)[:70])
async def main():
    r=aioredis.Redis(port=6391, decode_responses=True); await r.flushall()
    stream_mod.get_evidence_sink=lambda: FakeSink()
    store=ConsequenceAuthorityStore(r, ttl_seconds=90); gw=ConsequenceGateway(store,signer)
    G={}
    # G1
    t=mint(rec="g1"); G['G1_first']=await ev(gw,t); G['G1_second']=await ev(gw,t)
    G['G1_altered_payload']=await ev(gw,mint(rec="g1b"),{**PAY,"amount":101})
    G['G1_expired']=await ev(gw,mint(rec="g1c",ttl=-10))
    h,p,s=mint(rec="g1d").split("."); bad=s[:-4]+("AAAA" if s[-4:]!="AAAA" else "BBBB")
    G['G1_bad_signature']=await ev(gw,f"{h}.{p}.{bad}")
    # G2
    store2=ConsequenceAuthorityStore(r, ttl_seconds=2); gw2=ConsequenceGateway(store2,signer)
    t=mint(rec="g2",ttl=60); a=await ev(gw2,t); await asyncio.sleep(3.2); b=await ev(gw2,t)
    G['G2_store2s_token60s']={'first':a,'after_3s':b}
    t=mint(rec="g2d",ttl=60); a=await ev(gw,t); await asyncio.sleep(3.2); b=await ev(gw,t)
    G['G2_defaults_control']={'first':a,'after_3s':b}
    tl=mint(rec="g2l",ttl=86400); c=ConsequenceToken.verify(tl,signer=signer); G['G2_long_lived_token_verifies']={'exp_minus_iat':c.exp-c.iat}
    # G3
    bh=ConsequenceAuthorityStore.binding_hash
    G['G3_binding_collision']=bh("a:b","c","d","v")==bh("a","b:c","d","v")
    G['G3_control_distinct']=bh("a","c","d","v")!=bh("b","c","d","v")
    # G4
    sink=FakeSink(exc=stream_mod.EvidenceChainUnavailableError("down")); stream_mod.get_evidence_sink=lambda: sink
    t=mint(rec="g4"); G['G4_first_with_sink_down']=await ev(gw,t)
    stream_mod.get_evidence_sink=lambda: FakeSink()
    G['G4_retry_after_sink_up']=await ev(gw,t)
    # G5 jti != rec, kid garbage (gateway-signed)
    import src.gateway.governance.consequence_token as ct
    now=int(time.time())
    hdr={"alg":signer.jose_alg,"kid":"garbage","typ":"JWT"}
    pl={"sub":"u1","tid":"t1","rec":"g5","act":dig(PAY),"ver":"v1","iat":now,"exp":now+60,"jti":"DIFFERENT"}
    hb=ct._b64url_encode(jcs_canonicalize_plan(hdr)); pb=ct._b64url_encode(jcs_canonicalize_plan(pl))
    sig=ct._b64url_encode(signer.sign_raw(f"{hb}.{pb}".encode()))
    G['G5_jti_ne_rec_kid_garbage']=await ev(gw,f"{hb}.{pb}.{sig}")
    # C7 exceptions escaping evaluate
    G['C7_decimal_payload']=await ev(gw,mint(rec="c7a"),{**PAY,"amount":Decimal("100")})
    G['C7_intkey_payload']=await ev(gw,mint(rec="c7b"),{**PAY,1:"x"})
    G['C7_exception_leaves_token_unconsumed']=await r.get("flowsignal:token:c7a")
    # G6 big ints
    big_a={"action":"transfer","account_id":9007199254740992}; 
    t=mint(payload=big_a,rec="g6")
    G['G6_account_...993']=await ev(gw,t,{"action":"transfer","account_id":9007199254740993})
    t=mint(payload=big_a,rec="g6c")
    G['G6_control_...994']=await ev(gw,t,{"action":"transfer","account_id":9007199254740994})
    t=mint(payload=big_a,rec="g6d")
    G['G6_control_same']=await ev(gw,t,big_a)
    # seal path with same value
    import src.gateway.governance.routing_seal as rs
    try: rs.generate_seal("transfer",{"account_id":9007199254740993}); G['G6_seal_path']='accepted'
    except Exception as e: G['G6_seal_path']=type(e).__name__+': '+str(e)[:80]
    R['G']=G
    # G4b: default sink with nothing running
    stream_mod.get_evidence_sink=lambda: (_ for _ in ()).throw(RuntimeError("n/a"))
    R['G4b_note']='see below'
    json.dump(R,open(sys.argv[1],'w'),indent=1,default=str); print(json.dumps(R,indent=1,default=str))
asyncio.run(main())
