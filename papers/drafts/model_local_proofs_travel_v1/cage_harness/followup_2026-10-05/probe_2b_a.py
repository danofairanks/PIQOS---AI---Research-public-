import asyncio, base64, hashlib, json, os, sys
os.environ["CAGE_ENV"]="test"
import httpx
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import src.gateway.governance.contracts  # import order (see pass 2b note)
from src.gateway.governance.jcs_canonicalizer import jcs_canonicalize_plan
from src.gateway.governance.seams.actuation import ExecutionClearance
from src.integrations.actuator_02.adapter import Actuator02Adapter
from src.integrations.actuator_02.constants import RECEIPT_SIGNATURE_DOMAIN_TAG
b64=lambda b: base64.urlsafe_b64encode(b).rstrip(b"=").decode()
rkey=Ed25519PrivateKey.generate(); akey=Ed25519PrivateKey.generate()
class Signer:
    def sign_raw(self,m): return akey.sign(m)
class Resolver:
    def __init__(s,mode="ok"): s.mode=mode
    async def get_key(s,kid):
        if s.mode=="raise": raise RuntimeError("manifest down")
        return rkey.public_key() if kid=="rk" else None
class Broker:
    def __init__(s,h): s.h=h
    async def fetch_credential(s,**kw): return dict(s.h)
STATE={'mode':'valid','sent':[], 'status':'ACCEPTED'}
def sign_body(body):
    b={k:v for k,v in body.items() if k!="signature"}
    return b64(rkey.sign(RECEIPT_SIGNATURE_DOMAIN_TAG+jcs_canonicalize_plan(b)))
def handler(req):
    digest=hashlib.sha256(req.content).hexdigest()
    STATE['sent'].append({'headers':{k:v for k,v in req.headers.items()},'digest':digest,'assertion':req.headers.get('x-cage-openshell-assertion')})
    m=STATE['mode']; body={"status":STATE['status'],"receipt_id":"r-1","envelope_digest":digest}
    if m=='valid': body["signature"]={"alg":"EdDSA","kid":"rk","value":sign_body(body)}
    elif m=='stripped': pass
    elif m=='status_changed':
        body["signature"]={"alg":"EdDSA","kid":"rk","value":sign_body(body)}; body["status"]="EXECUTED"
    elif m=='other_digest':
        body["envelope_digest"]="0"*64; body["signature"]={"alg":"EdDSA","kid":"rk","value":sign_body(body)}
    elif m=='no_digest':
        body.pop("envelope_digest"); body["signature"]={"alg":"EdDSA","kid":"rk","value":sign_body(body)}
    return httpx.Response(200,json=body)
def clearance(**kw):
    d=dict(thread_id="t",decision="ALLOW",decision_path="DIRECT",action="execute_trade",target="X",operator_urn="urn:o",issued_at=1,
           issued_at_provenance="CONSTRUCTION_TIME",correlation_id="c1",correlation_id_source="THREAD_DERIVED",governance_decision_digest="d",
           opa_input_digest="o",nonce="n"*32,params={"a":1},executor_id="actuator_02",routing_seal="aaa.bbb.ccc")
    d.update(kw); return ExecutionClearance(**d)
def mk(resolver=None,strict=False,broker=None):
    c=httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return Actuator02Adapter(endpoint="https://sup.example",signer=Signer(),http_client=c,credential_broker=broker,receipt_key_resolver=resolver,require_signed_receipts=strict)
async def act(ad,cl,mode='valid',status='ACCEPTED'):
    STATE['mode']=mode; STATE['status']=status; n=len(STATE['sent'])
    r=await ad.actuate(cl)
    return {'accepted':r.accepted,'verification':getattr(r.verification,'value',str(r.verification)),'outcome':getattr(r.outcome,'value',str(r.outcome)),'codes':[f.get('code') for f in r.findings],'request_sent':len(STATE['sent'])>n}
async def main():
    R={}; A={}
    ad=mk(Resolver()); ad_s=mk(Resolver(),strict=True)
    A['A1a_valid']=await act(ad,clearance(),'valid')
    A['A1b_stripped_nonstrict']=await act(ad,clearance(),'stripped')
    A['A1b_stripped_strict']=await act(ad_s,clearance(),'stripped')
    A['A1c_status_changed']=await act(ad,clearance(),'status_changed')
    A['A1d_other_digest']=await act(ad,clearance(),'other_digest')
    A['A1e_no_digest']=await act(ad,clearance(),'no_digest')
    A['A1_no_resolver_stripped']=await act(mk(None),clearance(),'stripped')
    A['A2_manifest_down_nonstrict']=await act(mk(Resolver("raise")),clearance(),'valid')
    A['A2_manifest_down_strict']=await act(mk(Resolver("raise"),strict=True),clearance(),'valid')
    A['A3_executor_actuator_01_default']=await act(ad,clearance(executor_id="actuator_01"),'valid')
    A['A3_executor_cage_finance_broker']=await act(ad,clearance(executor_id="cage_finance_broker"),'valid')
    A['A3_executor_ACTUATOR_02']=await act(ad,clearance(executor_id="ACTUATOR_02"),'valid')
    dflt=ExecutionClearance(thread_id="t",decision="ALLOW",decision_path="DIRECT",action="a",target="x",operator_urn="o",issued_at=1,issued_at_provenance="CONSTRUCTION_TIME",correlation_id="c",correlation_id_source="THREAD_DERIVED",governance_decision_digest="d",opa_input_digest="o",nonce="n"*32)
    A['A3_dataclass_default_executor_id']=dflt.executor_id
    hb={"x-cage-routing-seal":"EVIL1","X-Cage-Envelope-Digest":"EVIL2","x_cage_routing_seal":"EVIL3","X-CAGE_Routing-Seal":"EVIL4","Authorization":"Bearer t"}
    adb=mk(Resolver(),broker=Broker(hb)); n=len(STATE['sent']); await act(adb,clearance(),'valid')
    sent=STATE['sent'][-1]['headers']
    A['A4_outgoing_headers_containing_EVIL']={k:v for k,v in sent.items() if v.startswith('EVIL')}
    A['A4_seal_header_value_is_the_clearance_seal']=sent.get('x-cage-routing-seal')
    A['A5_junk_seal_old_issued_at_no_approvals_quorum5']=await act(ad,clearance(routing_seal="aaa.bbb.ccc",issued_at=0,approvals=[],required_quorum=5),'valid')
    try: Actuator02Adapter(endpoint="http://plain.example",signer=Signer()); A['A6_http_endpoint_accepted']=True
    except ValueError as e: A['A6_http_endpoint_accepted']=False
    await act(ad,clearance(params={"id":9007199254740992}),'valid'); s1=STATE['sent'][-1]
    await act(ad,clearance(params={"id":9007199254740993}),'valid'); s2=STATE['sent'][-1]
    A['A7_digest_equal']=s1['digest']==s2['digest']; A['A7_assertion_equal']=s1['assertion']==s2['assertion']
    R['A']=A; json.dump(R,open(sys.argv[1],'w'),indent=1,default=str); print(json.dumps(R,indent=1,default=str))
asyncio.run(main())
