import asyncio, base64, json, os, sys, time, hashlib
os.environ["CAGE_SEAL_STRICT_MODE"]="false"; os.environ["CAGE_ENV"]="test"
os.environ.pop("ENVIRONMENT",None); os.environ.pop("CAGE_REQUIRE_EVIDENCE_BINDING",None)
import redis.asyncio as aioredis
import src.gateway.governance.routing_seal as rs
from src.gateway.governance import kms_signer as ks, jwks as jwks_mod

ACTION="execute_trade"; PARAMS={"symbol":"AAPL","amount":100.0}; RH="c"*64
R={}
def b64(d): return base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()

async def idx(r, seal, rh=RH):
    await r.set(f"cage:seal:evidence:{rs.seal_nonce(seal)}", rh)

async def consume(r, seal):
    try:
        return (await rs.verify_and_consume_seal(seal, ACTION, PARAMS, redis_client=r, expected_aud=None), None)
    except rs.SymbolicGovernorViolation as e:
        return (False, str(e.reason if hasattr(e,'reason') else e))

async def part(mode, r):
    out={}
    # fresh seals
    def mint(): return rs.generate_seal(ACTION, PARAMS, record_hash=RH)
    # B5 control
    s=mint(); out['B5_unindexed_refused']=await consume(r,s)
    await idx(r,s); out['B5_indexed_first']=await consume(r,s); out['B5_indexed_second']=await consume(r,s)
    # B1
    s=mint(); await idx(r,s); out['B1_revoke_true']=await rs.revoke_seal(s,"op",redis_client=r); out['B1_consume']=await consume(r,s)
    # B2
    s=mint(); await idx(r,s); out['B2_consume']=(await consume(r,s))[0]; out['B2_revoke_after']=await rs.revoke_seal(s,"late",redis_client=r); out['B2_state']=(await rs.seal_state(s,redis_client=r)).value
    # B3 50 concurrent
    s=mint(); await idx(r,s); res=await asyncio.gather(*[consume(r,s) for _ in range(50)]); out['B3_winners']=sum(1 for x in res if x[0]); out['B3_reasons']=sorted({x[1] for x in res if not x[0]})
    # B4 race x10 revoke + x10 consume, 30 trials
    outcomes={}
    for _ in range(30):
        s=mint(); await idx(r,s)
        tasks=[consume(r,s) for _ in range(10)]+[rs.revoke_seal(s,"race",redis_client=r) for _ in range(10)]
        res=await asyncio.gather(*tasks)
        cw=sum(1 for x in res[:10] if x[0]); rv=sum(1 for x in res[10:] if x is True)
        st=(await rs.seal_state(s,redis_client=r)).value
        outcomes[(cw,rv,st)]=outcomes.get((cw,rv,st),0)+1
    out['B4_outcomes(consume_winners,revoke_winners,state)']={str(k):v for k,v in outcomes.items()}
    # B8 HMAC nonce
    if mode=='hmac':
        s=mint(); out['B8_nonce_is_sha256_seal']=rs.seal_nonce(s)==hashlib.sha256(s.encode()).hexdigest()
    return out

async def jwt_forgery(r):
    out={}
    g=rs.generate_seal(ACTION,PARAMS,record_hash=RH)
    nonce=rs.seal_nonce(g)
    await idx(r,g)
    hdr=b64({"alg":"EdDSA","typ":"JWT","kid":"forged"})
    far=int(time.time())+10_000_000
    forged=f"{hdr}.{b64({'nonce':nonce,'exp':int(time.time())+1,'iss':'x'})}.{base64.urlsafe_b64encode(b'junk').decode().rstrip('=')}"
    out['B6_forged_consume_refused']=await consume(r,forged)
    out['B6_forged_revoke_returns']=await rs.revoke_seal(forged,"forged",redis_client=r)
    out['B6_genuine_state']=(await rs.seal_state(g,redis_client=r)).value
    out['B6_genuine_consume']=await consume(r,g)
    out['B7_ttl_of_nonce_key_s']=await r.ttl(f"cage:seal:nonce:{nonce}")
    out['B7_genuine_exp_remaining_s']=rs._seal_remaining_ttl(g)
    return out

async def main():
    r=aioredis.Redis(port=6391)
    await r.flushall()
    R['hmac']=await part('hmac',r)
    # JWT: install software ed25519
    ks._signer=ks.KMSGovernanceSigner(provider=ks.SoftwareEd25519Provider()); jwks_mod._global_jwks=None
    await r.flushall()
    R['jwt']=await part('jwt',r)
    await r.flushall()
    R['jwt_forgery']=await jwt_forgery(r)
    json.dump(R,open(sys.argv[1],'w'),indent=1,default=str)
    print(json.dumps(R,indent=1,default=str))
asyncio.run(main())
