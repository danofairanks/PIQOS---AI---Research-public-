"""Stateful BIFP audit sessions: record evidence against the protocol
schema in protocol.py, evaluate phase and overall status, persist to
and load from JSON so an audit can be built up across multiple calls
(the realistic shape of a real audit -- phases get evidence over time,
not in one shot).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .protocol import (
    ALL_SECTIONS, META_PROTOCOL, PHASES, SEMANTIC_HYGIENE,
    CriterionStatus, PhaseStatus, get_criterion, get_phase,
)


@dataclass
class CriterionRecord:
    key: str
    status: CriterionStatus = CriterionStatus.UNASSESSED
    evidence: str = ""
    notes: str = ""

    def to_dict(self) -> dict:
        return {"key": self.key, "status": self.status.value,
                "evidence": self.evidence, "notes": self.notes}

    @classmethod
    def from_dict(cls, d: dict) -> "CriterionRecord":
        return cls(key=d["key"], status=CriterionStatus(d["status"]),
                   evidence=d.get("evidence", ""), notes=d.get("notes", ""))


@dataclass
class PhaseRecord:
    number: int
    criteria: dict[str, CriterionRecord]
    applicable: bool = True

    @property
    def status(self) -> PhaseStatus:
        if not self.applicable:
            return PhaseStatus.NOT_APPLICABLE
        statuses = [c.status for c in self.criteria.values()]
        if any(s == CriterionStatus.UNMET for s in statuses):
            return PhaseStatus.FAILED
        if all(s == CriterionStatus.MET for s in statuses):
            return PhaseStatus.PASSED
        if all(s == CriterionStatus.UNASSESSED for s in statuses):
            return PhaseStatus.NOT_STARTED
        return PhaseStatus.IN_PROGRESS

    def to_dict(self) -> dict:
        return {"number": self.number, "applicable": self.applicable,
                "criteria": {k: v.to_dict() for k, v in self.criteria.items()}}

    @classmethod
    def from_dict(cls, d: dict) -> "PhaseRecord":
        return cls(number=d["number"], applicable=d.get("applicable", True),
                   criteria={k: CriterionRecord.from_dict(v) for k, v in d["criteria"].items()})


def _blank_phase_record(phase_number: int, applicable: bool = True) -> PhaseRecord:
    spec = get_phase(phase_number)
    return PhaseRecord(
        number=phase_number, applicable=applicable,
        criteria={c.key: CriterionRecord(key=c.key) for c in spec.criteria},
    )


@dataclass
class AuditSession:
    claim_text: str
    is_timeline_claim: bool = False
    escrowed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    phases: dict[int, PhaseRecord] = field(default_factory=dict)
    heuristic_flags: list[dict] = field(default_factory=list)

    @classmethod
    def new(cls, claim_text: str, *, is_timeline_claim: bool = False, escrowed: bool = False) -> "AuditSession":
        session = cls(claim_text=claim_text, is_timeline_claim=is_timeline_claim, escrowed=escrowed)
        for spec in PHASES:
            applicable = (not spec.timeline_only) or is_timeline_claim
            session.phases[spec.number] = _blank_phase_record(spec.number, applicable=applicable)
        session.phases[META_PROTOCOL.number] = _blank_phase_record(META_PROTOCOL.number)
        session.phases[SEMANTIC_HYGIENE.number] = _blank_phase_record(SEMANTIC_HYGIENE.number)
        return session

    def record(self, phase_number: int, criterion_key: str, met: bool, *,
               evidence: str = "", notes: str = "") -> None:
        """Record an assessment. Raises KeyError for an unknown
        phase/criterion (fail loudly rather than silently no-op on a typo)."""
        get_criterion(phase_number, criterion_key)  # validates existence
        record = self.phases[phase_number].criteria[criterion_key]
        record.status = CriterionStatus.MET if met else CriterionStatus.UNMET
        record.evidence = evidence
        record.notes = notes

    def add_heuristic_flags(self, flags: list[dict]) -> None:
        self.heuristic_flags.extend(flags)

    def phase_status(self, phase_number: int) -> PhaseStatus:
        return self.phases[phase_number].status

    @property
    def core_phase_numbers(self) -> list[int]:
        """Phase 0-6, excluding meta-protocol/semantic-hygiene sections
        (§3.9-3.10 govern the audit process itself, not the claim's
        pass/fail resolution -- see README for the reasoning)."""
        return [p.number for p in PHASES]

    @property
    def overall_resolution(self) -> str:
        """Protocol §3.7's own binary resolution categories: Sustained,
        Falsified, or Indeterminate, with escrowed stakes defaulting to
        Falsified rather than Indeterminate when not fully Sustained
        (§3.7: 'defaults to falsified for escrowed stakes').

        Only Phase 0-6 (excluding Phase 6 when the claim is not a
        timeline claim) count toward this resolution.
        """
        applicable = [self.phases[n] for n in self.core_phase_numbers
                      if self.phases[n].applicable]
        statuses = [p.status for p in applicable]
        if any(s == PhaseStatus.FAILED for s in statuses):
            return "Falsified"
        if all(s == PhaseStatus.PASSED for s in statuses):
            return "Sustained"
        return "Falsified" if self.escrowed else "Indeterminate"

    @property
    def protocol_integrity_resolution(self) -> str:
        """Separate from the claim's own resolution: did the audit
        process itself follow the Meta-Protocol (§3.9) and Semantic
        Hygiene Amendment (§3.10)? An audit can find a claim Sustained
        while its own process integrity is compromised (e.g. no
        cooling-off period observed) -- that is a real, reportable
        condition, not something to fold into the claim's verdict.
        """
        sections = [self.phases[META_PROTOCOL.number], self.phases[SEMANTIC_HYGIENE.number]]
        statuses = [p.status for p in sections]
        if any(s == PhaseStatus.FAILED for s in statuses):
            return "compromised"
        if all(s == PhaseStatus.PASSED for s in statuses):
            return "intact"
        return "incomplete"

    def to_dict(self) -> dict:
        return {
            "claim_text": self.claim_text,
            "is_timeline_claim": self.is_timeline_claim,
            "escrowed": self.escrowed,
            "created_at": self.created_at,
            "phases": {str(n): p.to_dict() for n, p in self.phases.items()},
            "heuristic_flags": self.heuristic_flags,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "AuditSession":
        session = cls(
            claim_text=d["claim_text"],
            is_timeline_claim=d.get("is_timeline_claim", False),
            escrowed=d.get("escrowed", False),
            created_at=d.get("created_at", ""),
            heuristic_flags=d.get("heuristic_flags", []),
        )
        session.phases = {int(n): PhaseRecord.from_dict(p) for n, p in d["phases"].items()}
        return session

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "AuditSession":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
