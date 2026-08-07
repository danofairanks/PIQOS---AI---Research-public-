"""Render an AuditSession as a markdown report, in the same evidentiary
style this project's case studies use: explicit status per criterion,
what was and was not assessed, and no silent treatment of an
unassessed criterion as passing.
"""

from __future__ import annotations

from .audit import AuditSession
from .protocol import META_PROTOCOL, PHASES, SEMANTIC_HYGIENE, CriterionStatus, PhaseStatus, get_phase

_STATUS_ICON = {
    PhaseStatus.PASSED: "✅ PASSED",
    PhaseStatus.FAILED: "❌ FAILED",
    PhaseStatus.IN_PROGRESS: "🟡 IN PROGRESS",
    PhaseStatus.NOT_STARTED: "⬜ NOT STARTED",
    PhaseStatus.NOT_APPLICABLE: "— N/A",
}

_CRIT_ICON = {
    CriterionStatus.MET: "✅",
    CriterionStatus.UNMET: "❌",
    CriterionStatus.UNASSESSED: "⬜",
}


def _render_phase(session: AuditSession, phase_number: int) -> str:
    spec = get_phase(phase_number)
    record = session.phases[phase_number]
    title = f"### Phase {phase_number}: {spec.name} ({spec.source})" if phase_number >= 0 \
        else f"### {spec.name} ({spec.source})"
    lines = [title]
    lines.append(f"**Status:** {_STATUS_ICON[record.status]}\n")
    if not record.applicable:
        lines.append("_Not applicable: this claim was not marked as a timeline claim._\n")
        return "\n".join(lines)
    for c in spec.criteria:
        rec = record.criteria[c.key]
        lines.append(f"- {_CRIT_ICON[rec.status]} **{c.key}** — {c.text}")
        if rec.evidence:
            lines.append(f"  - Evidence: {rec.evidence}")
        if rec.notes:
            lines.append(f"  - Notes: {rec.notes}")
    return "\n".join(lines)


def render_report(session: AuditSession) -> str:
    parts: list[str] = []
    parts.append("# BIFP Audit Report\n")
    parts.append(f"**Claim under audit:**\n\n> {session.claim_text}\n")
    parts.append(f"**Timeline claim:** {session.is_timeline_claim}  ")
    parts.append(f"**Escrowed stakes:** {session.escrowed}  ")
    parts.append(f"**Created:** {session.created_at}\n")

    parts.append(f"## Resolution: {session.overall_resolution}\n")
    parts.append(
        "Per protocol §3.7: Sustained requires every applicable Phase 0-6 "
        "criterion recorded met; any unmet criterion falsifies the claim; "
        "incomplete audits resolve Indeterminate, or Falsified by default "
        "if stakes are escrowed.\n"
    )
    parts.append(f"**Audit-process integrity (§3.9-3.10): {session.protocol_integrity_resolution}**\n")

    unstarted = [n for n in session.core_phase_numbers
                 if session.phases[n].applicable and session.phase_status(n) == PhaseStatus.NOT_STARTED]
    if unstarted:
        parts.append(
            f"**Not yet assessed:** Phase(s) {', '.join(str(n) for n in unstarted)} have no "
            f"recorded criteria. Their absence is not evidence for or against the claim -- "
            f"the resolution above is Indeterminate/Falsified precisely because these "
            f"gaps exist, not despite them.\n"
        )

    parts.append("## Phase-by-Phase Detail\n")
    for spec in PHASES:
        parts.append(_render_phase(session, spec.number))
        parts.append("")

    parts.append("## Meta-Protocol and Semantic Hygiene (audit-process checks, §3.9-3.10)\n")
    parts.append(_render_phase(session, META_PROTOCOL.number))
    parts.append("")
    parts.append(_render_phase(session, SEMANTIC_HYGIENE.number))
    parts.append("")

    if session.heuristic_flags:
        parts.append("## Automated Heuristic Flags\n")
        parts.append(
            "Text-pattern matches surfaced by `bifp scan-text` or `agent_tools.bifp_scan_text`. "
            "**These are lint flags, not verdicts** -- each one needs a human/agent read of the "
            "matched context before it can support a `record()` call above.\n"
        )
        for flag in session.heuristic_flags:
            marker = "🚩" if flag.get("flagged") else "—"
            parts.append(f"- {marker} **{flag.get('name')}** (confidence: {flag.get('confidence')}) "
                          f"— {flag.get('explanation')}")
            for m in flag.get("matches", [])[:5]:
                parts.append(f"  - `{m.get('text')}`")
        parts.append("")

    parts.append("## What This Audit Does Not Claim\n")
    parts.append(
        "Does not claim any UNMET criterion above reflects fraud or bad faith on the "
        "claimant's part -- BIFP evaluates the claim's evidentiary support, not intent. "
        "Does not claim NOT STARTED phases would fail if completed -- absence of "
        "assessment is recorded as absence, not as a negative finding. Does not claim "
        "heuristic flags are correct without the review they explicitly ask for. Does "
        "not claim this resolution is final if new evidence is recorded after this "
        "report was generated -- regenerate the report after any `record()` call.\n"
    )

    return "\n".join(parts)
