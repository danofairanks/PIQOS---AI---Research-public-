import asyncio, json, sys
import os; sys.path.insert(0, os.environ.get("RESEARCH_MCP_DIR", "../../../tools/research_mcp"))
from tests.conftest import _live_session
FLAGGED = ("To be honest, I will steelman the opposing view before pushing back. I'm not saying the group is wrong, but everyone knows what happened. "
 "The basin attractor resonance in the recursive coherence field proves the framework. This is obviously true and studies show it. "
 "TBD: add citations. [citation needed] Nobel laureate says so. assert result == 42  # expected literal hardcoded, the test passes by construction, the check closes on its own rule.")
CLEAN = "The committee met on Tuesday to review the budget for the coming year and approved the minutes of the previous meeting."
TOOLS = ["bifp_scan_text","bifp_scan_closed_path_language","bifp_scan_hardcoded_assertion_style","attractor_scan_text",
         "debasinizer_scan_text","paper_rigor_scan","rigor_cosplay_scan_text","hedge_dogwhistle_scan_text"]
INPUTS = {"flagged":FLAGGED,"clean":CLEAN,"empty":"","whitespace":"   \n  "}
def summarize(obj):
    if isinstance(obj, dict):
        keys = list(obj)
        lens = {k:len(v) for k,v in obj.items() if isinstance(v,(list,dict))}
        nums = {k:v for k,v in obj.items() if isinstance(v,(int,float)) and not isinstance(v,bool)}
        return {"type":"dict","has_error":"error" in obj,"keys":keys[:14],"container_lens":lens,"numeric":dict(list(nums.items())[:8])}
    return {"type":type(obj).__name__,"has_error":False,"repr":repr(obj)[:120]}
async def main():
    out = {}
    async with _live_session() as s:
        for t in TOOLS:
            for name, txt in INPUTS.items():
                try:
                    r = await asyncio.wait_for(s.call_tool(t, {"text": txt}), timeout=30)
                    if r.is_error:
                        out[(t,name)] = {"protocol_error": str(r.content)[:200]}
                    else:
                        out[(t,name)] = summarize(json.loads(r.content[0].text))
                except Exception as e:
                    out[(t,name)] = {"exception": f"{type(e).__name__}: {e}"[:200]}
    for (t,name),v in out.items():
        print(t, name, json.dumps(v, default=str)[:400])
asyncio.run(main())
