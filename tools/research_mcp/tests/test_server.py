"""End-to-end tests: every call here goes through the real MCP wire
protocol (in-memory transport) via the fixtures in conftest.py, not
a direct Python function call. This is deliberately redundant with
each source package's own agent_tools.py unit tests -- the point here
is to prove the MCP registration layer (schema generation from type
hints, JSON-RPC framing, tool dispatch) round-trips correctly, not to
re-verify the underlying research logic.
"""

from __future__ import annotations

import asyncio

from tests.conftest import _live_session


def test_protocol_level_error_is_distinct_from_payload_level_error():
    """Regression test for a real bug this test suite's own first draft
    hit: `CallToolResult`'s pydantic field is `is_error` (snake_case);
    `.isError` (the constructor's camelCase alias) silently returns via
    `__getattr__` as a missing-attribute AttributeError rather than the
    field value, so a first draft of conftest.py's error check was
    dead code until this was caught by the suite actually running.
    Missing required arguments trips MCP's own schema validation --
    `is_error=True` at the protocol level -- which is a different
    failure mode from an agent_tools.py function's own recoverable
    `{"error": ...}` JSON payload (see the other *_returns_error_*
    tests below, which all pass through `call_tool` fine because
    THEIR errors are valid, successfully-returned JSON)."""
    async def _run():
        async with _live_session() as session:
            return await session.call_tool("bifp_start_audit", {})  # missing required args

    result = asyncio.run(_run())
    assert result.is_error is True


def test_all_twenty_six_tools_are_registered(list_tool_names):
    names = set(list_tool_names())
    assert names == {
        "basin_depth_demo", "basin_depth_run", "basin_depth_derive_vocab",
        "bifp_list_phases", "bifp_start_audit", "bifp_record_criterion",
        "bifp_scan_text", "bifp_attach_scan_to_audit", "bifp_get_status", "bifp_generate_report",
        "bifp_judge_rebuttal", "bifp_attach_rebuttal_judgment",
        "bifp_start_closed_path_ledger", "bifp_record_fixture", "bifp_get_closed_path_status",
        "bifp_scan_closed_path_language", "bifp_scan_hardcoded_assertion_style",
        "bifp_trace_field_assignments",
        "attractor_scan_text", "attractor_scan_corpus", "attractor_scan_judge_visual_proof",
        "attractor_scan_claim_boundary_portability",
        "debasinizer_scan_text", "debasinizer_scan_corpus",
        "paper_rigor_scan", "paper_rigor_triage_worklist",
    }


def test_basin_depth_demo_over_the_wire(call_tool):
    result = call_tool("basin_depth_demo", {"n_boot": 50})
    assert "basin_depth" in result
    assert "interpretation" in result


def test_basin_depth_run_over_the_wire(call_tool):
    docs = [
        {"doc_id": str(i), "text": "coherence and drift " * 20, "quarter": q}
        for i, q in enumerate(["2020Q1"] * 5 + ["2020Q2"] * 5)
    ]
    result = call_tool("basin_depth_run", {
        "documents": docs, "start_quarter": "2020Q1", "end_quarter": "2020Q2",
        "n_boot": 30, "min_tokens": 10,
    })
    assert "basin_depth" in result


def test_basin_depth_run_bad_backend_returns_error_payload_not_protocol_error(call_tool):
    docs = [{"doc_id": "1", "text": "x " * 20, "quarter": "2020Q1"}]
    result = call_tool("basin_depth_run", {
        "documents": docs, "start_quarter": "2020Q1", "end_quarter": "2020Q1", "backend": "bogus",
    })
    assert "error" in result


def test_bifp_scan_text_over_the_wire(call_tool):
    result = call_tool("bifp_scan_text", {"text": "we're working on it"})
    assert result["provisionalization"]["flagged"] is True


def test_bifp_list_phases_over_the_wire(call_tool):
    result = call_tool("bifp_list_phases", {})
    numbers = {s["number"] for s in result["sections"]}
    assert numbers == {0, 1, 2, 3, 4, 5, 6, -1, -2}


def test_bifp_full_audit_flow_persists_across_separate_tool_calls(call_tool, tmp_path):
    """Each `call_tool` here opens a fresh in-memory session -- state
    persistence has to come from the audit file on disk (its actual
    persistence mechanism), not from any session-level cache. Proves
    an agent making separate tool calls across turns gets the same
    continuity a human running the CLI would."""
    audit_path = str(tmp_path / "audit.json")

    started = call_tool("bifp_start_audit", {"audit_path": audit_path, "claim_text": "test claim"})
    assert started["overall_resolution"] == "Indeterminate"

    recorded = call_tool("bifp_record_criterion", {
        "audit_path": audit_path, "phase": 5, "criterion_key": "no_status_dismissal",
        "met": False, "evidence": "matched heuristic scan",
    })
    assert recorded["overall_resolution"] == "Falsified"

    status = call_tool("bifp_get_status", {"audit_path": audit_path})
    assert status["overall_resolution"] == "Falsified"
    assert status["claim_text"] == "test claim"


def test_bifp_get_status_missing_audit_returns_error_payload(call_tool):
    result = call_tool("bifp_get_status", {"audit_path": "/nonexistent/audit.json"})
    assert "error" in result


def test_bifp_judge_rebuttal_missing_key_returns_error_payload(call_tool, monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    result = call_tool("bifp_judge_rebuttal", {"claim_text": "c", "rebuttal_text": "r"})
    assert "error" in result
    assert "GROQ_API_KEY" in result["error"]


def test_bifp_attach_rebuttal_judgment_missing_audit_returns_error_payload(call_tool, monkeypatch):
    # Missing-audit-file check happens before the GROQ_API_KEY check (see
    # bifp/agent_tools.py) -- exercises that ordering over the real wire.
    monkeypatch.setenv("GROQ_API_KEY", "irrelevant-for-this-path")
    result = call_tool("bifp_attach_rebuttal_judgment", {
        "audit_path": "/nonexistent/audit.json", "claim_text": "c", "rebuttal_text": "r",
    })
    assert "error" in result


def test_bifp_closed_path_ledger_flow_persists_across_separate_tool_calls(call_tool, tmp_path):
    ledger_path = str(tmp_path / "ledger.json")

    started = call_tool("bifp_start_closed_path_ledger", {
        "ledger_path": ledger_path, "artifact_label": "generic test artifact",
    })
    assert started["closed_path_ratio"] is None

    recorded = call_tool("bifp_record_fixture", {
        "ledger_path": ledger_path, "fixture_id": "f1", "outcome_derivation": "asserted",
    })
    assert recorded["asserted_count"] == 1

    status = call_tool("bifp_get_closed_path_status", {"ledger_path": ledger_path})
    assert status["flagged_fixture_ids"] == ["f1"]


def test_bifp_record_fixture_unknown_derivation_returns_error_payload(call_tool, tmp_path):
    ledger_path = str(tmp_path / "ledger.json")
    call_tool("bifp_start_closed_path_ledger", {"ledger_path": ledger_path, "artifact_label": "x"})
    result = call_tool("bifp_record_fixture", {
        "ledger_path": ledger_path, "fixture_id": "f1", "outcome_derivation": "not_a_real_kind",
    })
    assert "error" in result


def test_bifp_scan_closed_path_language_over_the_wire(call_tool):
    result = call_tool("bifp_scan_closed_path_language", {
        "text": "The repository was independently reproduced by a third-party audit.",
    })
    assert result["open_path_signals"]


def test_bifp_scan_hardcoded_assertion_style_over_the_wire(call_tool):
    result = call_tool("bifp_scan_hardcoded_assertion_style", {"text": 'assert status == "ALLOW"'})
    assert len(result["matches"]) == 1


def test_bifp_trace_field_assignments_over_the_wire(call_tool):
    result = call_tool("bifp_trace_field_assignments", {
        "sources": {"m.py": "class C:\n    def __init__(self):\n        self.score = 0.83\n"},
        "field_names": ["score"],
    })
    assert result["flagged_field_names"] == ["score"]


def test_attractor_scan_claim_boundary_portability_over_the_wire(call_tool):
    result = call_tool("attractor_scan_claim_boundary_portability", {
        "source_text": "This does not claim general validity and remains unestablished.",
        "citation_text": "This work introduces a novel governance framework.",
    })
    assert result["flagged"] is True


def test_attractor_scan_text_flags_the_papers_own_cited_example(call_tool):
    result = call_tool("attractor_scan_text", {
        "text": "This will happen frequently as AI becomes smarter and more agentic",
    })
    assert "case5" in result["flagged_laundering_cases"]


def test_attractor_scan_corpus_over_the_wire(call_tool):
    result = call_tool("attractor_scan_corpus", {
        "documents": [
            {"doc_id": "1", "text": "we are still working on it, that is just a hot take"},
            {"doc_id": "2", "text": "The classifier scored 87.3% accuracy on a held-out test set."},
        ],
    })
    assert result["n_documents"] == 2


def test_attractor_scan_judge_visual_proof_missing_key_returns_error_payload(call_tool, monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    # Key check happens before the image is ever read (see
    # visual_proof_judge.py), so a nonexistent path is fine here.
    result = call_tool("attractor_scan_judge_visual_proof", {
        "claim_text": "c", "image_path": "/nonexistent/x.png",
    })
    assert "error" in result
    assert "GROQ_API_KEY" in result["error"]


def test_debasinizer_scan_text_flags_cross_category_register_over_the_wire(call_tool):
    result = call_tool("debasinizer_scan_text", {
        "text": (
            "I am the oracle; the signal resonates with consciousness, and we "
            "must align with the other nodes to awaken the great convergence."
        ),
    })
    assert result["register_flagged"] is True


def test_debasinizer_scan_text_single_category_does_not_flag_register_over_the_wire(call_tool):
    result = call_tool("debasinizer_scan_text", {
        "text": "The distributed system has 12 nodes. Signal processing detects the pattern in the waveform.",
    })
    assert result["register_flagged"] is False


def test_debasinizer_scan_corpus_over_the_wire(call_tool):
    result = call_tool("debasinizer_scan_corpus", {
        "documents": [
            {"doc_id": "1", "text": "As we have established, this proves the theory."},
            {"doc_id": "2", "text": "The classifier scored 87.3% accuracy on a held-out test set."},
        ],
    })
    assert result["n_documents"] == 2
    assert result["self_coherence_flagged_count"] == 1


def test_paper_rigor_scan_flags_a_bad_paper_over_the_wire(call_tool):
    bad = (
        "It is trivial to show this conclusively demonstrates the result, beyond any doubt. "
        "TODO: fill in proof."
    ) + (" filler word" * 400)
    result = call_tool("paper_rigor_scan", {"text": bad})
    assert result["ok"] is False
    assert result["structural_gap_count"] >= 1


def test_paper_rigor_scan_clean_text_over_the_wire(call_tool):
    result = call_tool("paper_rigor_scan", {"text": "A short, clean note with nothing to flag."})
    assert result["ok"] is True
    assert result["structural_gap_count"] == 0


def test_paper_rigor_triage_worklist_empty_over_the_wire_no_key_needed(call_tool):
    """No GROQ_API_KEY required for this one -- an empty worklist short-
    circuits before any API call, so this exercises the real MCP wire
    round trip without needing network or a secret."""
    result = call_tool("paper_rigor_triage_worklist", {"worklist": []})
    assert result["items"] == []


def test_paper_rigor_triage_worklist_missing_key_returns_error_payload(call_tool, monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    worklist = [{"kind": "uncited_empirical_claim", "item": "x", "context": "c", "reason": "r"}]
    result = call_tool("paper_rigor_triage_worklist", {"worklist": worklist})
    assert "error" in result
    assert "GROQ_API_KEY" in result["error"]
