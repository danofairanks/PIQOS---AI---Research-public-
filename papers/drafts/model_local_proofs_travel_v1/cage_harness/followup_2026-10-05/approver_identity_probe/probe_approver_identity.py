"""Run from CAGE repo root: CAGE_ENV=development CAGE_TRUSTED_CLIENT_IDENTITIES=<advisor identity> python probe_approver_identity.py"""
import asyncio, json, os
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
from fastapi import FastAPI
from src.gateway.governance.contracts import *  # noqa  import order
import src.gateway.server.hybrid_server as h
from src.gateway.server.workload_identity import IdentityPolicy, WorkloadIdentityMiddleware

ADV = "cage-advisor-sa.governance-stack.serviceaccount.identity.linkerd.cluster.local"
REV = "risk-officer-sa.governance-stack.serviceaccount.identity.linkerd.cluster.local"
OTHER = "stranger-sa.default.serviceaccount.identity.linkerd.cluster.local"
out = {}
P = {"control_id": "A.5.2", "verdict": "FAIL", "source": "probe"}
def A(app): return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://t")
async def post(c, path, ident, body, extra=None):
    hdr = [("l5d-client-id", ident)] if ident else []
    hdr += extra or []
    r = await c.post(path, json=body, headers=hdr)
    try: return r.status_code, r.json()
    except Exception: return r.status_code, r.text[:80]

async def main():
    mod = "src.gateway.governance.langgraph_harness.nemo_node_factory"
    reload_mock = AsyncMock(); get_mock = MagicMock(return_value=object())
    with patch(f"{mod}.reload_nemo_rails", reload_mock), patch(f"{mod}.get_nemo_rails", get_mock):
        async with A(h.root_app) as c:
            # controls
            out["C_no_header"] = (await post(c, "/v1/nemo/propose-refinement", None, P))[0]
            out["C_untrusted_identity"] = (await post(c, "/v1/nemo/propose-refinement", OTHER, P))[0]
            out["C_two_headers"] = (await post(c, "/v1/nemo/propose-refinement", ADV, P, extra=[("l5d-client-id", ADV)]))[0]
            # P1 propose by advisor
            s, b = await post(c, "/v1/nemo/propose-refinement", ADV, P); out["P1_propose"] = (s, b.get("status")); pid = b["proposal_id"]
            # P2 same identity approves, reviewer = fake human name
            n0 = reload_mock.await_count
            s, b = await post(c, f"/v1/nemo/approve-refinement/{pid}", ADV, {"approved": True, "reviewer": "Jane Doe, Chief Risk Officer", "rationale": "ok"})
            out["P2_same_identity_approves"] = {"status": s, "body_status": b.get("status"), "reload_calls": reload_mock.await_count - n0}
            rec = dict(h._refinement_proposals[pid]); out["P6_record_fields"] = sorted(rec.keys()); out["P6_reviewer_value"] = rec["reviewer"]
            out["P6_record_contains_caller_identity"] = any(ADV in str(v) for v in rec.values())
            out["P7_reload_call_args"] = [repr(call) for call in reload_mock.await_args_list[-1:]]
            # P3 reviewer variants
            res = {}
            for label, rev in (("empty_string", ""), ("own_service_account", ADV), ("arbitrary", "x")):
                s, b = await post(c, "/v1/nemo/propose-refinement", ADV, P); pid2 = b["proposal_id"]
                s, b = await post(c, f"/v1/nemo/approve-refinement/{pid2}", ADV, {"approved": True, "reviewer": rev, "rationale": "r"})
                res[label] = (s, b.get("status"), repr(h._refinement_proposals[pid2]["reviewer"]))
            out["P3_reviewer_variants"] = res
            # controls on approve
            out["C_second_approve"] = (await post(c, f"/v1/nemo/approve-refinement/{pid}", ADV, {"approved": True, "reviewer": "x", "rationale": "r"}))[0]
            out["C_unknown_id"] = (await post(c, "/v1/nemo/approve-refinement/does-not-exist", ADV, {"approved": True, "reviewer": "x", "rationale": "r"}))[0]
            s, b = await post(c, "/v1/nemo/propose-refinement", ADV, P); pid3 = b["proposal_id"]; n1 = reload_mock.await_count
            s, b = await post(c, f"/v1/nemo/approve-refinement/{pid3}", ADV, {"approved": False, "reviewer": "x", "rationale": "r"})
            out["C_reject"] = {"body_status": b.get("status"), "reload_calls": reload_mock.await_count - n1}
            n2 = reload_mock.await_count
            s, b = await post(c, "/v1/nemo/apply-refinement", ADV, P)
            out["C_apply_only_stages"] = {"status": b.get("status"), "reload_calls": reload_mock.await_count - n2}
            out["C_missing_rationale"] = (await post(c, f"/v1/nemo/approve-refinement/{pid3}", ADV, {"approved": True, "reviewer": "x", "rationale": "  "}))[0]
        # P4: role-agnostic under a two-identity set, same handlers
        app2 = FastAPI()
        app2.add_api_route("/v1/nemo/propose-refinement", h.propose_nemo_refinement, methods=["POST"])
        app2.add_api_route("/v1/nemo/approve-refinement/{proposal_id}", h.approve_nemo_refinement, methods=["POST"])
        app2.add_middleware(WorkloadIdentityMiddleware, policy=IdentityPolicy(trusted=frozenset({ADV, REV})))
        async with A(app2) as c2:
            grid = {}
            for proposer in (ADV, REV):
                for approver in (ADV, REV):
                    s, b = await post(c2, "/v1/nemo/propose-refinement", proposer, P)
                    s2, b2 = await post(c2, f"/v1/nemo/approve-refinement/{b['proposal_id']}", approver, {"approved": True, "reviewer": "r", "rationale": "r"})
                    grid[f"propose={proposer.split('.')[0]} approve={approver.split('.')[0]}"] = (s, s2, b2.get("status"))
            out["P4_two_identity_grid"] = grid
    # in-memory store
    out["note_store_type"] = type(h._refinement_proposals).__name__
    print(json.dumps(out, indent=1, default=str))
asyncio.run(main())
