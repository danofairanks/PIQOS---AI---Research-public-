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

from attractor_scan.agent_tools import (
    attractor_scan_claim_boundary_portability, attractor_scan_corpus,
    attractor_scan_judge_visual_proof, attractor_scan_text,
)
from basin_depth.agent_tools import basin_depth_demo, basin_depth_derive_vocab, basin_depth_run
from bifp.agent_tools import (
    bifp_attach_rebuttal_judgment, bifp_attach_scan_to_audit, bifp_generate_report,
    bifp_get_closed_path_status, bifp_get_status, bifp_judge_rebuttal, bifp_list_phases,
    bifp_record_criterion, bifp_record_fixture, bifp_scan_closed_path_language,
    bifp_scan_hardcoded_assertion_style, bifp_scan_text, bifp_start_audit,
    bifp_start_closed_path_ledger, bifp_trace_field_assignments,
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
        "heuristics cannot determine. Three tools call Groq and require "
        "GROQ_API_KEY, each advisory-only and never a verdict: "
        "bifp_judge_rebuttal / bifp_attach_rebuttal_judgment return one "
        "candidate read on whether a rebuttal addresses a claim as actually "
        "made or a weaker substitute (BIFP §3.7), never calling record() "
        "itself, since BIFP's own §3.9 forbids AI-as-judge for the claim's "
        "actual adjudication; attractor_scan_judge_visual_proof returns one "
        "candidate read on a single image + claim pair for whether the "
        "image's genuine technical content supports the claim or is "
        "connected only by wordplay (basin_attractors_v1.md §2.8 Case 6), "
        "never scanning a corpus; paper_rigor_triage_worklist attaches a "
        "priority and a suggested_check to each item in an existing "
        "external_verification_worklist without adding, removing, or "
        "resolving any of them -- it has no web access and never claims to "
        "have verified anything. bifp_start_closed_path_ledger / "
        "bifp_record_fixture / bifp_get_closed_path_status track, per "
        "fixture, whether a governance artifact's evidence is closed-path "
        "(expected outcome asserted as a literal matching the artifact's "
        "own output) or open-path (expected outcome derived from an "
        "independent specification) -- papers/drafts/closed_path_"
        "confirmation_v1.md §2's defeat condition, operationalized; "
        "bifp_scan_closed_path_language and bifp_scan_hardcoded_assertion_"
        "style are standalone lexical leads over prose/code for the same "
        "distinction, not a substitute for actually classifying fixtures. "
        "bifp_trace_field_assignments is a sharper, AST-based check: for "
        "caller-supplied field names, is each one ever assigned from an "
        "expression touching input across caller-supplied source files, "
        "or only ever a literal constant -- a field that is never proven "
        "input-derived cannot vary with input at all, a stronger finding "
        "than closed-loop. Conservative in one direction only: any "
        "Name/Attribute/Subscript/Call reference in an assignment's "
        "right-hand side rules out the flag for that field, even where "
        "the reference is also constant in practice. "
        "attractor_scan_claim_boundary_portability checks whether a source "
        "document's own stated limitations show any lexical trace in a "
        "separate citation/reference text -- a two-document comparison, "
        "unlike attractor_scan_text's single-document scan. Every tool "
        "here is a heuristic lead generator, not a verdict -- see each "
        "source package's own README for exactly what it does and does "
        "not detect."
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
    bifp_judge_rebuttal,
    bifp_attach_rebuttal_judgment,
    bifp_start_closed_path_ledger,
    bifp_record_fixture,
    bifp_get_closed_path_status,
    bifp_scan_closed_path_language,
    bifp_scan_hardcoded_assertion_style,
    bifp_trace_field_assignments,
    attractor_scan_text,
    attractor_scan_corpus,
    attractor_scan_judge_visual_proof,
    attractor_scan_claim_boundary_portability,
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
