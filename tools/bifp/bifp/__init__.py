"""Structured audit tool for the Basin-Immune Falsification Protocol
(BIFP), basin_attractors_v1.md §3.

Quick start::

    from bifp import AuditSession

    session = AuditSession.new("Model X achieves human-level reasoning", escrowed=True)
    session.record(1, "claim_specified", met=True, evidence="paper §2 defines the construct")
    session.record(1, "tested_specified", met=True, evidence="MMLU-Pro, n=12000")
    session.record(1, "validity_match", met=False, notes="benchmark score, not construct-level claim")
    print(session.overall_resolution)  # "Falsified" -- Phase 1 has an unmet criterion

Or from the command line::

    bifp new --audit claim1.json --claim "Model X achieves human-level reasoning"
    bifp record --audit claim1.json --phase 1 --criterion claim_specified --met --evidence "..."
    bifp report --audit claim1.json

Or as agent tool calls (see agent_tools.py and README.md "Wiring this
into an agent")::

    from bifp.agent_tools import bifp_start_audit, bifp_scan_text
"""

from .audit import AuditSession, CriterionRecord, PhaseRecord
from .closed_path import (
    ClosedPathLanguageResult, ClosedPathLedger, FixtureRecord,
    scan_for_closed_path_language, scan_for_hardcoded_assertion_style,
)
from .heuristics import HeuristicResult, scan_text
from .protocol import (
    ALL_SECTIONS, CORE_AXIOM, META_PROTOCOL, PHASES, SEMANTIC_HYGIENE,
    CriterionStatus, PhaseStatus, get_criterion, get_phase,
)
from .report import render_report
from .uncomputed_field import AssignmentSite, FieldTrace, FieldTraceResult, trace_field_assignments

__all__ = [
    "AuditSession", "CriterionRecord", "PhaseRecord",
    "HeuristicResult", "scan_text",
    "ClosedPathLedger", "FixtureRecord", "ClosedPathLanguageResult",
    "scan_for_closed_path_language", "scan_for_hardcoded_assertion_style",
    "AssignmentSite", "FieldTrace", "FieldTraceResult", "trace_field_assignments",
    "ALL_SECTIONS", "CORE_AXIOM", "META_PROTOCOL", "PHASES", "SEMANTIC_HYGIENE",
    "CriterionStatus", "PhaseStatus", "get_criterion", "get_phase",
    "render_report",
]

__version__ = "0.1.0"
