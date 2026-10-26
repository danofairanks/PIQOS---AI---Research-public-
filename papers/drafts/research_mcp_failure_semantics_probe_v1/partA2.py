import asyncio, json, sys
import os; sys.path.insert(0, os.environ.get("RESEARCH_MCP_DIR", "../../../tools/research_mcp"))
from tests.conftest import _live_session
async def call(s, t, a):
    try:
        r = await asyncio.wait_for(s.call_tool(t, a), timeout=30)
        if r.is_error: return ("PROTOCOL_ERROR", str(r.content)[:160])
        o = json.loads(r.content[0].text)
        return (type(o).__name__, o)
    except Exception as e:
        return ("EXC", f"{type(e).__name__}: {str(e)[:140]}")
def short(o, n=260): return json.dumps(o, default=str)[:n]
async def main():
    async with _live_session() as s:
        for name,txt in (("flagged","TBD: add citations. [citation needed] Nobel laureate says so. studies show it."),("clean","The committee met on Tuesday."),("empty","")):
            k,o = await call(s,"paper_rigor_scan",{"text":txt}); print("paper_rigor_scan",name,k,{x:o.get(x) for x in("path","ok","structural_gap_count","total_gap_count")} if isinstance(o,dict) else o)
        for name,txt in (("flagged","Resonance resonates. I am self-coherent; my coherence proves recursion field."),("clean","The committee met on Tuesday.")):
            k,o = await call(s,"debasinizer_scan_text",{"text":txt}); print("debasinizer",name,{x:o.get(x) for x in("register_flagged","self_coherence_flagged","any_flagged")})
        print("--- other shapes")
        for t,a in (("bifp_list_phases",{}),("attractor_scan_corpus",{"documents":["a","b"]}),("debasinizer_scan_corpus",{"documents":[]}),("hedge_dogwhistle_scan_corpus",{"documents":["x"]}),("rigor_cosplay_scan_corpus",{"documents":["x"]})):
            k,o = await call(s,t,a); print(t,k,short(o,200))
        print("--- error probes")
        for t,a in (("attractor_scan_text",{}),("attractor_scan_text",{"text":123}),("attractor_scan_text",{"text":None}),("bifp_get_status",{"audit_path":"/nonexistent/x.json"}),
                    ("basin_depth_run",{"documents":[],"start_quarter":"2020Q1","end_quarter":"2020Q2","backend":"nope"}),
                    ("bifp_judge_rebuttal",{"claim_text":"c","rebuttal_text":"r"}),("paper_rigor_triage_worklist",{"worklist":[]}),("no_such_tool",{})):
            k,o = await call(s,t,a); print(t,a if len(str(a))<60 else "...",k,short(o,230))
asyncio.run(main())
