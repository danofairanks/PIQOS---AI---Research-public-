import asyncio, base64, json, os, sys, time
import httpx
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from src.gateway.governance.jcs_canonicalizer import jcs_canonicalize_plan
from src.integrations.provider_07.adapter import Provider07NormativeProvider
for k in ("CAGE_ENV","ENVIRONMENT"): os.environ.pop(k,None)
b64=lambda b: base64.urlsafe_b64encode(b).rstrip(b"=").decode()
key=Ed25519PrivateKey.generate()
pub=key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
STATE={'jwks_gets':0,'infer_posts':0,'keys':[{"kty":"OKP","crv":"Ed25519","kid":"k1","x":b64(pub)}],'resp':None,'delay':0}
def signed(body, kid="k1"):
    body=dict(body); body["kid"]=kid
    body["signature"]=b64(key.sign(jcs_canonicalize_plan({k:v for k,v in body.items() if k!="signature"})))
    return body
BASE={"decision":"ALLOW","confidence_score":0.9,"posterior_risk_score":0.1,"marginal_probabilities":{},"utility_rankings":[],"authority_record_id":"auth-1","findings":[]}
def handler(req):
    if req.url.path.endswith("jwks.json"):
        STATE['jwks_gets']+=1; return httpx.Response(200,json={"keys":STATE['keys']})
    if req.url.path.endswith("/infer"):
        STATE['infer_posts']+=1; return httpx.Response(200,json=STATE['resp'])
    return httpx.Response(404)
_orig=httpx.AsyncClient
class Patched(_orig):
    def __init__(self,*a,**k): k['transport']=httpx.MockTransport(handler); super().__init__(*a,**k)
httpx.AsyncClient=Patched
REQ={"scenario_id":"s1","action":"execute_trade","target":"urn:p:1","actor_id":"urn:a:1","portfolio_vector":{"eq":1.0},
     "proposed_trade":{"asset":"X","side":"BUY","amount":1.0},"client_profile":{"risk_tolerance":"MODERATE","investment_horizon_years":5,"liquidity_need":"LOW"}}
async def run(ad, resp):
    STATE['resp']=resp; before=STATE['jwks_gets']
    r=await ad.validate_fria(REQ)
    return {'admitted':r.admitted,'codes':[f.get('code') for f in (r.findings or [])],'jwks_gets_delta':STATE['jwks_gets']-before}
async def main():
    R={}
    ad=Provider07NormativeProvider("https://svc.example")
    R['P0_control_valid_signature']=await run(ad,signed(BASE))
    tam=signed(BASE); tam['posterior_risk_score']=0.0
    R['P0_control_tampered_field']=await run(ad,tam)
    R['P0_control_unknown_kid']=await run(ad,signed(BASE,kid="zz"))
    # P2
    unsigned=dict(BASE); unsigned.update(kid="key-id",signature="unsigned-placeholder")
    ad_off=Provider07NormativeProvider("https://svc.example",allow_step1_unsigned=False)
    ad_on=Provider07NormativeProvider("https://svc.example",allow_step1_unsigned=True)  # CAGE_ENV unset
    R['P2_flag_off_unsigned']=await run(ad_off,unsigned)
    R['P2_flag_on_unsigned_CAGE_ENV_unset']=await run(ad_on,unsigned)
    os.environ["CAGE_ENV"]="staging"
    ad_stg=Provider07NormativeProvider("https://svc.example",allow_step1_unsigned=True)
    R['P2_flag_on_unsigned_CAGE_ENV_staging']=await run(ad_stg,unsigned)
    os.environ.pop("CAGE_ENV")
    # P3
    c=ad._jwks_client
    STATE['jwks_gets']=0; await c.get_key("k1"); warm=STATE['jwks_gets']
    STATE['jwks_gets']=0; await c.get_key("k1"); await c.get_key("k1"); known=STATE['jwks_gets']
    STATE['jwks_gets']=0
    for i in range(20): await c.get_key(f"unknown-{i}")
    seq=STATE['jwks_gets']
    STATE['jwks_gets']=0
    await asyncio.gather(*[c.get_key(f"unk-c-{i}") for i in range(20)])
    conc=STATE['jwks_gets']
    R['P3']={'fetch_on_warmup':warm,'fetches_for_2_known_lookups':known,'fetches_for_20_unknown_sequential':seq,'fetches_for_20_unknown_concurrent':conc}
    # P5
    STATE['keys']=[]
    r5=await c.get_key("k1")
    R['P5_after_empty_manifest_known_kid_resolves']= r5 is not None
    STATE['keys']=[{"kty":"OKP","crv":"Ed25519","kid":"k1","x":b64(pub)}]
    json.dump(R,open(sys.argv[1],'w'),indent=1); print(json.dumps(R,indent=1))
asyncio.run(main())
