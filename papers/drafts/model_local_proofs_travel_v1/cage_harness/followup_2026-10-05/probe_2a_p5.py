import asyncio, base64, json, sys
import httpx
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from src.integrations.provider_07.jwks_client import Provider07JwksClient
b64=lambda b: base64.urlsafe_b64encode(b).rstrip(b"=").decode()
pub=Ed25519PrivateKey.generate().public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
S={'keys':[{"kty":"OKP","crv":"Ed25519","kid":"k1","x":b64(pub)}],'gets':0,'fail':False}
def h(req):
    S['gets']+=1
    if S['fail']: return httpx.Response(503)
    return httpx.Response(200,json={"keys":S['keys']})
orig=httpx.AsyncClient
class P(orig):
    def __init__(s,*a,**k): k['transport']=httpx.MockTransport(h); super().__init__(*a,**k)
httpx.AsyncClient=P
async def main():
    R={}
    c=Provider07JwksClient("https://svc.example/jwks.json")
    R['warm_known']= (await c.get_key("k1")) is not None
    S['keys']=[]
    R['unknown_lookup_with_empty_manifest']=(await c.get_key("other")) is None
    R['known_after_empty_manifest_refresh']=(await c.get_key("k1")) is not None
    S['keys']=[{"kty":"OKP","crv":"Ed25519","kid":"k1","x":b64(pub)}]
    R['known_after_manifest_restored']=(await c.get_key("k1")) is not None
    # outage during unknown-kid lookup on a warm cache: does the known key still resolve for the next call?
    c2=Provider07JwksClient("https://svc.example/jwks.json"); await c2.get_key("k1")
    S['fail']=True
    try: await c2.get_key("unknown"); R['outage_unknown_lookup']='returned'
    except Exception as e: R['outage_unknown_lookup']='raises '+type(e).__name__
    S['fail']=False
    R['known_lookup_after_outage_during_warm_cache']=(await c2.get_key("k1")) is not None
    json.dump(R,open(sys.argv[1],'w'),indent=1); print(json.dumps(R,indent=1))
asyncio.run(main())
