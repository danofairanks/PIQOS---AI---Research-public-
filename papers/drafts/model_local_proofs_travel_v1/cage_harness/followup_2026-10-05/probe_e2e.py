import asyncio, time, json, sys
import httpx
from fastapi import FastAPI
from src.gateway.governance.evidence.state_commitment import StateCommitmentService
from src.gateway.governance.seams.state_commitment import StateCommitmentLinkage
from src.gateway.server.state_commitment_api import router
from src.gateway.server.workload_identity import IdentityPolicy, WorkloadIdentityMiddleware
from tests.integrations.provider_02.state_commitment_support import RecordingEvidenceSink
TRUSTED="advisor.cage.serviceaccount.identity.linkerd.cluster.local"
def app():
    g=FastAPI(); g.include_router(router); g.state.state_commitments=StateCommitmentService(RecordingEvidenceSink())
    r=FastAPI(); r.mount("/governance",g); r.add_middleware(WorkloadIdentityMiddleware,policy=IdentityPolicy(trusted=frozenset({TRUSTED}))); return r
L=StateCommitmentLinkage("ns","b","s","t","lbl").to_dict()
async def run(snapshot):
    a=app(); gaps=[]; stop=False
    async def ticker():
        last=time.perf_counter()
        while not stop:
            await asyncio.sleep(0.05); n=time.perf_counter(); gaps.append(n-last); last=n
    tk=asyncio.create_task(ticker()); await asyncio.sleep(0.2); gaps.clear()
    t0=time.perf_counter()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=a),base_url="http://gw") as c:
        r=await c.post("/governance/state-commitments",json={"snapshot":snapshot,"linkage":L},headers={"l5d-client-id":TRUSTED})
    el=time.perf_counter()-t0; stop=True; await tk
    return {'status':r.status_code,'elapsed_s':round(el,3),'max_tick_gap_s':round(max(gaps),3) if gaps else None}
async def main():
    R={}
    R['control_plain_16KB']=await run({"v":"a"*16384})
    R['swift_16KB']=await run({"v":"swift "*(16384//6)})
    R['swift_32KB']=await run({"v":"swift "*(32768//6)})
    json.dump(R,open(sys.argv[1],'w'),indent=1); print(json.dumps(R,indent=1))
asyncio.run(main())
