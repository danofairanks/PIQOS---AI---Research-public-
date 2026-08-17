"""MCP server exposing basin_depth, bifp, attractor_scan, debasinizer,
and paper_rigor's already-JSON-safe `agent_tools.py` function surfaces
as real MCP tools.

Every registered function is unmodified from its source package --
this module is pure wiring, not a reimplementation. Each function's
docstring becomes the tool description an MCP client sees, and its
type hints become the tool's JSON input schema; both are already
in place because `agent_tools.py` in each sibling package was written
to that contract from the start (see each package's own agent_tools.py
module docstring).

Run it directly (stdio transport, the default MCP host integration)::

    research-mcp

Or import the app and drive it yourself (see tests/test_server.py for
a real in-memory client-server round trip, not a mock)::

    from research_mcp.server import app
"""

from __future__ import annotations

try:
    # The name this project actually shipped against and tested (mcp
    # 2.0.0). Import compatibility fallback below covers the older
    # `FastMCP` name some earlier 1.x releases used for the same class.
    from mcp.server.mcpserver import MCPServer
except ImportError:  # pragma: no cover -- exercised only on older mcp releases
    from mcp.server.fastmcp import FastMCP as MCPServer

from attractor_scan.agent_tools import attractor_scan_corpus, attractor_scan_text
from basin_depth.agent_tools import basin_depth_demo, basin_depth_derive_vocab, basin_depth_run
from bifp.agent_tools import (
    bifp_attach_scan_to_audit, bifp_generate_report, bifp_get_status, bifp_list_phases,
    bifp_record_criterion, bifp_scan_text, bifp_start_audit,
)
from debasinizer.agent_tools import debasinizer_scan_corpus, debasinizer_scan_text
from paper_rigor.agent_tools import paper_rigor_scan, paper_rigor_triage_worklist

app = MCPServer(
    "piqos-research-tools",
    instructions=(
        "Basin-attractor research tooling from the PIQOS AI Research (Public) "
        "project: basin_depth_* measures coherence-time decay in a text corpus "
        "(Noether-Temporal Coherence Test Protocol), bifp_* runs a structured "
        "Basin-Immune Falsification Protocol audit, attractor_scan_* "
        "classifies text for the seven defensive maneuvers and semantic-"
        "laundering cases named in basin_attractors_v1.md, debasinizer_scan_* "
        "classifies text for the resonance-vocabulary register documented in "
        "the Mind Viruses paper (arXiv:2608.10218) and self-referential "
        "coherence-assertion phrasing -- a distinct source and claim from "
        "attractor_scan, not a duplicate of it -- and paper_rigor_scan "
        "checks any paper (no PIQOS-specific vocabulary required) for placeholder/"
        "hand-wave phrases, an unstated falsifiability condition, self-citation "
        "ratio, formal-vs-informal sourcing mix, uncited empirical-certainty "
        "claims, credential-substituted-for-evidence claims, unsupported "
        "consensus claims, a claimed-citability-with-zero-references "
        "contradiction, and a missing limitations section -- its "
        "external_verification_worklist output names the specific items that "
        "need a real web search/fetch to resolve (does citation X really say "
        "what's claimed, is this source credible), which this tool's own text "
        "heuristics cannot determine. paper_rigor_triage_worklist is an optional, "
        "Groq-backed advisory pass over an existing worklist (pass paper_rigor_"
        "scan's own external_verification_worklist output straight through) -- "
        "it attaches a priority and a suggested_check to each item without "
        "adding, removing, or resolving any of them; it has no web access and "
        "never claims to have verified anything. Requires GROQ_API_KEY. Every "
        "tool here is a heuristic lead generator, not a verdict -- see each "
        "source package's own README for exactly what it does and does not "
        "detect."
    ),
)

_TOOLS = [
    basin_depth_demo,
    basin_depth_run,
    basin_depth_derive_vocab,
    bifp_list_phases,
    bifp_start_audit,
    bifp_record_criterion,
    bifp_scan_text,
    bifp_attach_scan_to_audit,
    bifp_get_status,
    bifp_generate_report,
    attractor_scan_text,
    attractor_scan_corpus,
    debasinizer_scan_text,
    debasinizer_scan_corpus,
    paper_rigor_scan,
    paper_rigor_triage_worklist,
]

for _fn in _TOOLS:
    app.tool()(_fn)


def main() -> None:
    app.run()


if __name__ == "__main__":
    main()
