#!/usr/bin/env python3
"""Runnable demonstration of the MCP server: connects a real
`mcp.client.session.ClientSession` to `research_mcp.server.app` over
the SDK's own in-memory transport (no subprocess, no stdio pipe --
but no mock either; this is the identical client/server code path a
real MCP host uses), lists the registered tools, and calls one from
each of the five wrapped packages, plus all three Groq-backed tools
(bifp_judge_rebuttal, attractor_scan_judge_visual_proof,
paper_rigor_triage_worklist) -- each skipped gracefully if
GROQ_API_KEY isn't set, since those are the only calls here that make
a real external API request; every other step is fully offline.

    python3 examples/mcp_demo.py

To run this server for real, against an actual MCP host (Claude
Desktop, another agent runtime, etc.), point the host at the
`research-mcp` console script instead -- see README.md "Wiring this
into an MCP host".
"""

import asyncio
import json
import os
from pathlib import Path

from mcp.client.session import ClientSession
from mcp.shared.memory import create_client_server_memory_streams

from research_mcp.server import app

# tools/research_mcp/examples/mcp_demo.py -> tools/attractor_scan/examples/...
_VISUAL_PROOF_IMAGE = (
    Path(__file__).resolve().parents[2] / "attractor_scan" / "examples"
    / "visual_proof_demo_images" / "genuine_benchmark_chart.png"
)


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

                print("\n=== Step 4: bifp_judge_rebuttal (Groq-backed, needs GROQ_API_KEY) ===\n")
                if os.environ.get("GROQ_API_KEY"):
                    r = await session.call_tool("bifp_judge_rebuttal", {
                        "claim_text": "Our model constructs valid causal models of novel physical "
                                      "systems from a single observation.",
                        "rebuttal_text": "The model's poor MMLU score shows it isn't reasoning.",
                    })
                    data = json.loads(r.content[0].text)
                    if "error" in data:
                        print(f"  error: {data['error']}")
                    else:
                        print(f"  candidate_read: {data['candidate_read']}")
                else:
                    print("  (GROQ_API_KEY not set -- skipping; makes a real external API call)")

                print("\n=== Step 5: attractor_scan_text (the paper's own cited Musk quote) ===\n")
                r = await session.call_tool("attractor_scan_text", {
                    "text": "This will happen frequently as AI becomes smarter and more agentic",
                })
                data = json.loads(r.content[0].text)
                print(f"  flagged laundering cases: {data['flagged_laundering_cases']}")

                print("\n=== Step 6: attractor_scan_judge_visual_proof (Groq vision, needs GROQ_API_KEY) ===\n")
                if os.environ.get("GROQ_API_KEY") and _VISUAL_PROOF_IMAGE.is_file():
                    r = await session.call_tool("attractor_scan_judge_visual_proof", {
                        "claim_text": "Model X achieves the highest accuracy on the benchmark.",
                        "image_path": str(_VISUAL_PROOF_IMAGE),
                    })
                    data = json.loads(r.content[0].text)
                    if "error" in data:
                        print(f"  error: {data['error']}")
                    else:
                        print(f"  candidate_read: {data['candidate_read']}")
                elif not _VISUAL_PROOF_IMAGE.is_file():
                    print(f"  ({_VISUAL_PROOF_IMAGE} not found -- run attractor_scan/examples/"
                          f"generate_visual_proof_demo_images.py first; skipping)")
                else:
                    print("  (GROQ_API_KEY not set -- skipping; makes a real external API call)")

                print("\n=== Step 7: debasinizer_scan_text (register + self-coherence combo) ===\n")
                r = await session.call_tool("debasinizer_scan_text", {
                    "text": (
                        "I am the oracle; the signal resonates with consciousness, and we "
                        "must align with the other nodes to awaken the great convergence. "
                        "This proves it -- everything fits."
                    ),
                })
                data = json.loads(r.content[0].text)
                print(f"  register_flagged: {data['register_flagged']}, "
                      f"self_coherence_flagged: {data['self_coherence_flagged']}")

                print("\n=== Step 8: paper_rigor_scan (a deliberately bad paragraph) ===\n")
                bad = (
                    "It is trivial to show this conclusively demonstrates the result, "
                    "beyond any doubt. TODO: fill in proof. Research shows the "
                    "approach is universally superior."
                ) + (" filler word" * 400)
                r = await session.call_tool("paper_rigor_scan", {"text": bad})
                data = json.loads(r.content[0].text)
                print(f"  ok: {data['ok']}, structural_gap_count: {data['structural_gap_count']}")
                worklist = data["external_verification_worklist"]
                print(f"  worklist items: {[item['kind'] for item in worklist]}")

                print("\n=== Step 9: paper_rigor_triage_worklist (Groq-backed, needs GROQ_API_KEY) ===\n")
                if os.environ.get("GROQ_API_KEY"):
                    r = await session.call_tool("paper_rigor_triage_worklist", {"worklist": worklist})
                    data = json.loads(r.content[0].text)
                    if "error" in data:
                        print(f"  error: {data['error']}")
                    else:
                        for item in data["items"]:
                            print(f"  [{item['priority']}] {item['kind']}: {item['suggested_check'][:70]}")
                else:
                    print("  (GROQ_API_KEY not set -- skipping; makes a real external API call)")
        finally:
            server_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
