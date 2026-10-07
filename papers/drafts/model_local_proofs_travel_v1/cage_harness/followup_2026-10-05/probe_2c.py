import asyncio, json, math, os, sys, tempfile, logging
from pathlib import Path
os.environ["CAGE_ENV"]="test"; os.environ.pop("ENVIRONMENT",None)
import src.gateway.governance.contracts  # import order (see pass 2b)
from src.gateway.governance.ftra import classifier as C
from src.gateway.governance.ftra.autonomy import conditional_clear_reason, safe_magnitude, AutonomousEnvelope
from src.gateway.governance.ftra.models import RegistryState, TerminalClassification, ExecutionPlan, PlanStep
from src.gateway.governance.ftra.graph_analyzer import PlanGraphAnalyzer
from src.gateway.governance.governor.stages.ftra import FtraStage
from src.gateway.governance.governor.pipeline import StageContext, Profile
from src.gateway.governance.agent_confidence import reported_confidence
from src.gateway.governance.schemas.thresholds import get_agent_confidence_threshold, get_confidence_defer_floor
logging.disable(logging.CRITICAL)
R={}
T=Path(tempfile.mkdtemp(prefix="ftra2c_"))
def write_registry(name, ceiling=10000.0, envelope=True, digest=True, expires="2027-10-01T00:00:00+00:00", extra=None):
    raw={"version":"3.0","domain":"core","serial":1,"issued_at":"2026-10-01T00:00:00+00:00","expires_at":expires,
         "terminals":{"execute_trade":"IRREVERSIBLE_TERMINAL","read_quote":"READ_ONLY"}}
    if envelope: raw["autonomous_envelope"]={"execute_trade":{"max_magnitude":ceiling}}
    if extra: raw.update(extra)
    p=T/name
    if digest: raw["manifest_sha256"]=C.registry_digest(raw)
    p.write_text(json.dumps(raw,indent=2)); return p
floor=get_agent_confidence_threshold(); dfloor=get_confidence_defer_floor()
R['thresholds']={'agent_confidence_threshold':floor,'defer_floor':dfloor}
# ---- Part F
env=AutonomousEnvelope(10000.0); REG=RegistryState.REGISTERED; TERM=TerminalClassification.IRREVERSIBLE_TERMINAL
def cr(**kw):
    d=dict(classification=TERM,registry_state=REG,envelope=env,magnitude=100.0,confidence=0.99,confidence_floor=floor); d.update(kw)
    return conditional_clear_reason(**d)
F={}
F['F1_nan_confidence']=cr(confidence=float('nan')) is not None
F['F1_control_below_floor']=cr(confidence=0.0) is None
F['F1_control_nan_magnitude']=cr(magnitude=float('nan')) is None
F['F1_control_unregistered']=cr(registry_state=RegistryState.UNREGISTERED if hasattr(RegistryState,'UNREGISTERED') else list(RegistryState)[1]) is None
F['F1_control_good']=cr() is not None
# graph + stage with a real registry file
reg=write_registry("env.json")
cls=C.IrreversibilityClassifier(registry_path=reg)
mx=lambda p: p["amount"]
an=PlanGraphAnalyzer(classifier=cls, magnitude_extractor=mx)
def plan(amount):
    return ExecutionPlan(plan_id="p1",rationale="r",steps=[PlanStep(id="s1",action="execute_trade",description="d",parameters={"amount":amount})])
def an_res(conf,amount=100.0):
    try:
        r=an.analyze(plan(amount),conf); return {'verdict':r.verdict.value,'auto_cleared':list(r.auto_cleared_terminals)}
    except Exception as e: return {'raises':type(e).__name__+': '+str(e)[:70]}
F['F2_graph_nan']=an_res(float('nan')); F['F2_graph_conf_0']=an_res(0.0); F['F2_graph_conf_0.99']=an_res(0.99)
async def stage_res(params):
    st=FtraStage(magnitude_extractor=mx); st._ftra_classifier=cls
    out=await st.run(StageContext(action="execute_trade",params=params,profile=Profile.FULL))
    f=out.ftra
    return {'requires_hitl':f.requires_hitl,'auto_cleared':f.auto_cleared,'codes':[v.code for v in out.violations]}
F['F2_stage_nan']=asyncio.run(stage_res({"amount":100.0,"confidence":float('nan')}))
F['F2_stage_0.99']=asyncio.run(stage_res({"amount":100.0,"confidence":0.99}))
F['F2_reported_confidence_nan']=reported_confidence({"confidence":float('nan')})
# F3
def ovf():
    try: return ('returns',safe_magnitude(lambda p:10**400,{}))
    except Exception as e: return ('raises',type(e).__name__)
F['F3_safe_magnitude_10e400']=ovf()
F['F3_stage_10e400']=asyncio.run(stage_res({"amount":10**400,"confidence":0.99}))
F['F3_graph_10e400']=an_res(0.99,amount=10**400)
# F4
reg4=write_registry("env4.json",ceiling=9007199254740992.0); cls4=C.IrreversibilityClassifier(registry_path=reg4)
an4=PlanGraphAnalyzer(classifier=cls4,magnitude_extractor=mx)
for amt in (9007199254740992,9007199254740993,9007199254740994):
    r=an4.analyze(plan(amt),0.99); F[f'F4_amount_{amt}']={'verdict':r.verdict.value,'auto_cleared':list(r.auto_cleared_terminals)}
R['F']=F
# ---- Part R
Rr={}
def load(p):
    try: d=C._load_registry_document(p); return {'loads':True,'envelope_ceiling':{k:v.max_magnitude for k,v in d.envelopes.items()} if hasattr(d,'envelopes') else None}
    except Exception as e: return {'loads':False,'err':type(e).__name__+': '+str(e)[:80]}
p=write_registry("r1.json",ceiling=10000.0)
Rr['R1_baseline']=load(p)
raw=json.loads(p.read_text()); raw["autonomous_envelope"]["execute_trade"]["max_magnitude"]=1e12; p.write_text(json.dumps(raw))
Rr['R1_edited_no_rehash']=load(p)
C.rehash_registry(p) if False else None
raw=json.loads(p.read_text()); raw["manifest_sha256"]=C.registry_digest(raw); p.write_text(json.dumps(raw))
Rr['R1_edited_with_recomputed_digest']=load(p)
# using the repo's own API
p2=write_registry("r1b.json"); raw=json.loads(p2.read_text()); raw["autonomous_envelope"]["execute_trade"]["max_magnitude"]=1e12; p2.write_text(json.dumps(raw))
try: Rr['R1_rehash_registry_api_returns']=C.rehash_registry(p2)[:16]
except Exception as e: Rr['R1_rehash_registry_api_returns']='raises '+type(e).__name__
Rr['R1_after_rehash_api']=load(p2)
Rr['R2_envelope_without_digest']=load(write_registry("r2a.json",digest=False))
Rr['R2_no_envelope_no_digest']=load(write_registry("r2b.json",envelope=False,digest=False))
pe=write_registry("r3.json",expires="2020-01-01T00:00:00+00:00")
Rr['R3_expired_loads']=load(pe)
c3=C.IrreversibilityClassifier(registry_path=pe); Rr['R3_classify_after_expiry']=c3.classify("execute_trade").value
try: Rr['R3_staleness_report_is_clean']=C.check_registry_staleness(frozenset({"execute_trade","read_quote"}),pe).is_clean
except Exception as e: Rr['R3_staleness_report_is_clean']='raises '+type(e).__name__
R['R']=Rr
# ---- Part E
from src.gateway.governance.estate_provider import StubEstateProvider
from src.gateway.governance.env_posture import resolve_posture, is_enforcing
E={}
for v in (None,"","production","staging","local","testing","continuous-integration","dev ","dev","DEV","development","test","ci"):
    for k in ("CAGE_ENV","ENVIRONMENT"): os.environ.pop(k,None)
    if v is not None: os.environ["CAGE_ENV"]=v
    try: StubEstateProvider(); res='constructs'
    except RuntimeError: res='refused'
    E[repr(v)]={'estate_stub':res,'central_posture':resolve_posture().value,'central_enforcing':is_enforcing()}
R['E']=E
json.dump(R,open(sys.argv[1],'w'),indent=1,default=str); print(json.dumps(R,indent=1,default=str))
