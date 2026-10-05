import asyncio, hashlib, json, logging, os, sys, time
os.environ["CAGE_ENV"]="test"; os.environ.pop("ENVIRONMENT",None)
R={}
# ---------------- Part S
import src.gateway.governance.contracts  # import order: stpa_validator first raises ImportError (circular)
from src.gateway.governance.stpa_validator import STPAValidator, UcaRule
logs=[]
class H(logging.Handler):
    def emit(self,r): logs.append((r.levelname,r.getMessage()[:90]))
logging.getLogger().addHandler(H()); logging.getLogger().setLevel(logging.DEBUG)
S={}
v=STPAValidator()
codes=lambda vs:[getattr(x,'code',repr(x)) for x in vs]
S['S1']={'token_absent':codes(v.validate("write_db",{})),'token_None':codes(v.validate("write_db",{"approval_token":None}))}
for val in ("", "garbage", 0, False, {}):
    S['S1'][f'token={val!r}']=codes(v.validate("write_db",{"approval_token":val}))
S['S2']={a:codes(v.validate(a,{})) for a in ("write_db","write_db ","WRITE_DB","write-db","write_db​")}
logs.clear()
v2=STPAValidator([UcaRule("UCA-1",action="other",predicate=lambda *_: None)])
S['S3']={'core_with_colliding_contrib':codes(v2.validate("write_db",{})),'rules_active':[r.uca_id+'/'+r.action for r in v2.rules],
         'log_lines_ge_WARNING':[l for l in logs if l[0] in('WARNING','ERROR','CRITICAL')]}
v3=STPAValidator([UcaRule("uca-1",action="other",predicate=lambda *_: None)])
S['S3']['lowercase_id_does_not_replace']=codes(v3.validate("write_db",{}))
def runrule(res):
    r=STPAValidator([UcaRule("X-1",action="a",predicate=lambda *_: res)],include_core=False)
    try: return ('returns',[getattr(x,'code',repr(x)) for x in r.validate("a",{})])
    except Exception as e: return ('raises',type(e).__name__+': '+str(e)[:60])
def boom(*_): raise ValueError("x")
S['S4']={'predicate_raises':codes(STPAValidator([UcaRule("X-1",action="a",predicate=boom)],include_core=False).validate("a",{})),
         'returns_0':runrule(0),'returns_empty_dict':runrule({}),'returns_dict':runrule({"a":1}),'returns_tuple_of_str':runrule(("a",))}
R['S']=S
# ---------------- Part O
from src.integrations.actuator_02.ocsf_ingestor import OcsfEvidenceIngestor
from src.gateway.governance.pii_sanitizer import PIISanitizer
class Rec:
    def __init__(s): s.events=[]
    async def ingest(s,e): s.events.append(e); return "id"
def ev(**kw):
    d={"class_uid":1001,"sandbox_id":"sb","thread_id":"t","governance_decision_digest":"AAAAAAAA"}; d.update(kw); return d
async def ing(**kw):
    sink=Rec(); await OcsfEvidenceIngestor(sink).ingest_ocsf_event(ev(**kw)); return sink.events[0]
O={}
async def parto():
    e=await ing(metadata={"a":[[{"token":"s"}]]}); O['O1_nested_list']=e['metadata']
    e=await ing(metadata={"a":[{"token":"s"}]}); O['O1_control_list_of_dict']=e['metadata']
    O['O2']={}
    for d in ("Blocked","Denied","Dropped","Rejected","Block","Deny","Quarantined","Isolated","Unauthorized","Access Revoked","Error","Allowed"):
        e=await ing(disposition=d); O['O2'][d]=e['controlId']
    e=await ing(governance_decision_digest="not-a-digest"); O['O3_arbitrary_digest']=e['governance_decision_digest']
    big="x"*1_000_000
    e=await ing(metadata={"k":big}); O['O3_1MB_metadata_accepted']=len(e['metadata']['k'])
    e=await ing(metadata={"cmd":"curl -H 'Authorization: Bearer abc.def.ghi' https://x"}); O['O4_bearer_in_value_after_ingestor']=e['metadata']['cmd']
    O['O4_after_pii_sanitizer']=PIISanitizer().sanitize_dict({"metadata":e['metadata']})['metadata']['cmd']
    t0=time.perf_counter(); PIISanitizer().sanitize_dict({"type":"SANDBOX_OCSF_TELEMETRY","metadata":{"cmd":"swift "*(16384//6)}}); O['O5_sanitize_dict_16KB_metadata_s']=round(time.perf_counter()-t0,2)
    t0=time.perf_counter(); PIISanitizer().sanitize_dict({"type":"SANDBOX_OCSF_TELEMETRY","metadata":{"cmd":"a"*16384}}); O['O5_control_plain_16KB_s']=round(time.perf_counter()-t0,4)
asyncio.run(parto()); R['O']=O
# ---------------- Part G4b
import redis.asyncio as aioredis
from src.gateway.governance import kms_signer as ks
from src.gateway.governance.consequence_token import ConsequenceToken
from src.gateway.governance.consequence_authority_store import ConsequenceAuthorityStore
from src.gateway.governance.consequence_gateway import ConsequenceGateway
from src.gateway.governance.jcs_canonicalizer import jcs_canonicalize_plan
import src.gateway.governance.evidence.stream as stream_mod
signer=ks.KMSGovernanceSigner(provider=ks.SoftwareEd25519Provider())
PAY={"action":"transfer","account_id":"A1","amount":100}
dig=hashlib.sha256(jcs_canonicalize_plan(PAY)).hexdigest()
def mint(rec): return ConsequenceToken.mint(sub="u",tid="t",rec=rec,act=dig,ver="v",ttl_seconds=60,signer=signer)
async def g4b():
    r=aioredis.Redis(port=6391,decode_responses=True); await r.flushall()
    gw=ConsequenceGateway(ConsequenceAuthorityStore(r,90),signer); G={}
    sink=stream_mod.EvidenceStreamSink(); G['sink_redis_is_None']=sink._redis is None
    stream_mod.get_evidence_sink=lambda: sink
    e=await gw.evaluate(mint("g4b1"),PAY); G['no_redis_sink']=(e.decision.value,e.reason_code)
    sink2=stream_mod.EvidenceStreamSink(); sink2._redis=object()
    async def bad(ev): raise RuntimeError("redis write failed")
    sink2._append=bad; stream_mod.get_evidence_sink=lambda: sink2
    e=await gw.evaluate(mint("g4b2"),PAY); G['append_raises_RuntimeError']=(e.decision.value,e.reason_code)
    async def bad2(ev): raise stream_mod.EvidenceChainUnavailableError("restore failed")
    sink2._append=bad2
    e=await gw.evaluate(mint("g4b3"),PAY); G['append_raises_EvidenceChainUnavailable']=(e.decision.value,e.reason_code)
    return G
R['G4b']=asyncio.run(g4b())
json.dump(R,open(sys.argv[1],'w'),indent=1,default=str); print(json.dumps(R,indent=1,default=str))
