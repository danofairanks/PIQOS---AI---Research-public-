#!/usr/bin/env python3
"""Runnable demonstration of the MCP server: connects a real
`mcp.client.session.ClientSession` to `research_mcp.server.app` over
the SDK's own in-memory transport (no subprocess, no stdio pipe --
but no mock either; this is the identical client/server code path a
real MCP host uses), lists the registered tools, and calls one from
each of the four wrapped packages.

    python3 examples/mcp_demo.py

To run this server for real, against an actual MCP host (Claude
Desktop, another agent runtime, etc.), point the host at the
`research-mcp` console script instead -- see README.md "Wiring this
into an MCP host".
"""

import asyncio
import json

from mcp.client.session import ClientSession
from mcp.shared.memory import create_client_server_memory_streams

from research_mcp.server import app


async def main() -> None:
    async with create_client_server_memory_streams() as (client_streams, server_streams):
        client_read, client_write = client_streams
        server_read, server_write = server_streams

        async def run_server() -> None:
            await app._lowlevel_server.run(
                server_read, server_write,
                app._lowlevel_server.create_initialization_options(),
            )

        server_task = asyncio.create_task(run_server())
        try:
            async with ClientSession(client_read, client_write) as session:
                await session.initialize()

                print("=== Step 1: list registered tools ===\n")
                tools = await session.list_tools()
                for t in tools.tools:
                    print(f"  {t.name}")

                print("\n=== Step 2: basin_depth_demo (synthetic corpus) ===\n")
                r = await session.call_tool("basin_depth_demo", {"n_boot": 100})
                data = json.loads(r.content[0].text)
                print(f"  basin_depth = {data['basin_depth']:.2f} -> {data['interpretation']}")

                print("\n=== Step 3: bifp_scan_text (heuristic pass, no audit file needed) ===\n")
                r = await session.call_tool("bifp_scan_text", {"text": "we're working on it"})
                data = json.loads(r.content[0].text)
                print(f"  provisionalization flagged: {data['provisionalization']['flagged']}")

                print("\n=== Step 4: attractor_scan_text (the paper's own cited Musk quote) ===\n")
                r = await session.call_tool("attractor_scan_text", {
                    "text": "This will happen frequently as AI becomes smarter and more agentic",
                })
                data = json.loads(r.content[0].text)
                print(f"  flagged laundering cases: {data['flagged_laundering_cases']}")

                print("\n=== Step 5: paper_rigor_scan (a deliberately bad paragraph) ===\n")
                bad = (
                    "It is trivial to show this conclusively demonstrates the result, "
                    "beyond any doubt. TODO: fill in proof. Research shows the "
                    "approach is universally superior."
                ) + (" filler word" * 400)
                r = await session.call_tool("paper_rigor_scan", {"text": bad})
                data = json.loads(r.content[0].text)
                print(f"  ok: {data['ok']}, structural_gap_count: {data['structural_gap_count']}")
                print(f"  worklist items: {[item['kind'] for item in data['external_verification_worklist']]}")
        finally:
            server_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
