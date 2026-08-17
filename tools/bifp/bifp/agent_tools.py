"""Stable, JSON-in/JSON-out function surface for agent tool-calling.

Every function here takes and returns only plain JSON-serializable
types (str, bool, int, float, dict, list, None) so this module can be
wrapped directly as MCP tool handlers or referenced from a Claude
Skill/agent framework without any adaptation layer. Audits are
identified by filesystem path so state persists naturally across
separate tool calls within (or across) an agent session -- see
README.md "Wiring this into an agent" for how to expose these as
actual MCP tools.

This module is intentionally the ONLY place in the package with this
constraint; `audit.py` and friends are free to use dataclasses/enums
internally. Think of this as the package's tool-calling ABI.
"""

from __future__ import annotations

from .audit import AuditSession
from .heuristics import scan_text
from .protocol import ALL_SECTIONS, CORE_AXIOM
from .rebuttal_judge import DEFAULT_MODEL, RebuttalJudgeError, judge_rebuttal


def bifp_list_phases() -> dict:
    """Return the full BIFP schema: every phase/section, its criteria,
    and whether it only applies to timeline claims. Call this first to
    know what `bifp_record_criterion` accepts."""
    return {
        "core_axiom": CORE_AXIOM,
        "sections": [
            {
                "number": spec.number,
                "name": spec.name,
                "source": spec.source,
                "timeline_only": spec.timeline_only,
                "criteria": [{"key": c.key, "text": c.text, "source": c.source} for c in spec.criteria],
            }
            for spec in ALL_SECTIONS
        ],
    }


def bifp_start_audit(audit_path: str, claim_text: str, *,
                      is_timeline_claim: bool = False, escrowed: bool = False) -> dict:
    """Create a new audit session and persist it to `audit_path` (a
    JSON file this and every other bifp_* call will read/write).
    Returns the initial status snapshot."""
    session = AuditSession.new(claim_text, is_timeline_claim=is_timeline_claim, escrowed=escrowed)
    session.save(audit_path)
    return bifp_get_status(audit_path)


def bifp_record_criterion(audit_path: str, phase: int, criterion_key: str, met: bool, *,
                           evidence: str = "", notes: str = "") -> dict:
    """Record whether one criterion was met, with supporting evidence.
    Raises (as a returned error dict, not an exception) if phase/
    criterion_key don't match the schema -- callers should check
    `error` in the response rather than relying on exceptions
    propagating cleanly across a tool-call boundary."""
    try:
        session = AuditSession.load(audit_path)
        session.record(phase, criterion_key, met, evidence=evidence, notes=notes)
        session.save(audit_path)
    except (KeyError, FileNotFoundError) as exc:
        return {"error": str(exc)}
    return bifp_get_status(audit_path)


def bifp_scan_text(text: str) -> dict:
    """Run all available heuristic scanners (status dismissal,
    provisionalization, prohibited anthropomorphic terms) against a
    piece of text and return the matches. Does not require or modify
    an audit session -- call this on any text you want a first pass
    on before deciding whether it's worth starting a full audit."""
    results = scan_text(text)
    return {name: result.to_dict() for name, result in results.items()}


def bifp_attach_scan_to_audit(audit_path: str, text: str) -> dict:
    """Run `bifp_scan_text` and attach the results to an existing
    audit's record for the final report, without recording any
    criterion outcome (the scan is evidence to review, not an
    automatic pass/fail)."""
    try:
        session = AuditSession.load(audit_path)
    except FileNotFoundError as exc:
        return {"error": str(exc)}
    results = scan_text(text)
    session.add_heuristic_flags([r.to_dict() for r in results.values()])
    session.save(audit_path)
    return {name: result.to_dict() for name, result in results.items()}


def bifp_judge_rebuttal(claim_text: str, rebuttal_text: str, *, model: str = DEFAULT_MODEL) -> dict:
    """Get one AI-generated (Groq) candidate read on §3.7's "no
    weaker-substitute rebuttal" criterion: does `rebuttal_text`
    address `claim_text` as actually made, or a weaker substitute?

    This is advisory only -- see rebuttal_judge.py's module docstring
    on why it does not conflict with §3.9's no_ai_as_judge criterion.
    It never records a criterion outcome. Requires GROQ_API_KEY in the
    environment; returns {"error": ...} rather than raising if it's
    missing or the call fails, matching this module's existing
    tool-calling ABI contract. Does not require or modify an audit
    session -- call this for a quick check before deciding whether to
    attach it to a full audit via `bifp_attach_rebuttal_judgment`."""
    try:
        result = judge_rebuttal(claim_text, rebuttal_text, model=model)
    except RebuttalJudgeError as exc:
        return {"error": str(exc)}
    return result.to_dict()


def bifp_attach_rebuttal_judgment(audit_path: str, claim_text: str, rebuttal_text: str, *,
                                   model: str = DEFAULT_MODEL) -> dict:
    """Run `bifp_judge_rebuttal` and attach the result to an existing
    audit's `ai_advisory_flags`, without recording any criterion
    outcome (same non-authoritative contract as
    `bifp_attach_scan_to_audit` for the deterministic heuristics --
    see that function and rebuttal_judge.py)."""
    try:
        session = AuditSession.load(audit_path)
    except FileNotFoundError as exc:
        return {"error": str(exc)}
    try:
        result = judge_rebuttal(claim_text, rebuttal_text, model=model)
    except RebuttalJudgeError as exc:
        return {"error": str(exc)}
    session.add_ai_advisory_flags([result.to_dict()])
    session.save(audit_path)
    return result.to_dict()


def bifp_get_status(audit_path: str) -> dict:
    """Current phase-by-phase status and overall resolution for an
    existing audit."""
    try:
        session = AuditSession.load(audit_path)
    except FileNotFoundError as exc:
        return {"error": str(exc)}
    return {
        "claim_text": session.claim_text,
        "overall_resolution": session.overall_resolution,
        "protocol_integrity": session.protocol_integrity_resolution,
        "phases": {
            str(n): session.phase_status(n).value
            for n in [spec.number for spec in ALL_SECTIONS]
        },
    }


def bifp_generate_report(audit_path: str) -> dict:
    """Render the full markdown report for an existing audit."""
    from .report import render_report
    try:
        session = AuditSession.load(audit_path)
    except FileNotFoundError as exc:
        return {"error": str(exc)}
    return {"markdown": render_report(session)}
