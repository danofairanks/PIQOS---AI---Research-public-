import asyncio, json, sys
import os; sys.path.insert(0, os.environ.get("RESEARCH_MCP_DIR", "../../../tools/research_mcp"))
from tests.conftest import _live_session
sys.argv=["x"]
exec(open("partA.py").read().split("def summarize")[0])
async def main():
    async with _live_session() as s:
        r = await s.call_tool("bifp_scan_text",{"text":FLAGGED}); print(r.content[0].text[:900])
        r = await s.call_tool("attractor_scan_text",{"text":FLAGGED}); o=json.loads(r.content[0].text); print({k:(type(v).__name__, v if not isinstance(v,(list,dict)) else len(v)) for k,v in o.items()})
asyncio.run(main())
