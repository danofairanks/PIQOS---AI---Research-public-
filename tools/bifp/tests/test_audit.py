import json

import pytest

from bifp.audit import AuditSession
from bifp.protocol import CriterionStatus, PhaseStatus


def test_new_audit_all_phases_not_started_or_na():
    session = AuditSession.new("test claim")
    for n in session.core_phase_numbers:
        if session.phases[n].applicable:
            assert session.phase_status(n) == PhaseStatus.NOT_STARTED
    assert session.phase_status(6) == PhaseStatus.NOT_APPLICABLE  # not a timeline claim


def test_timeline_claim_makes_phase_6_applicable():
    session = AuditSession.new("AGI by 2027", is_timeline_claim=True)
    assert session.phases[6].applicable
    assert session.phase_status(6) == PhaseStatus.NOT_STARTED


def test_record_unknown_phase_raises():
    session = AuditSession.new("test claim")
    with pytest.raises(KeyError):
        session.record(99, "whatever", met=True)


def test_record_unknown_criterion_raises():
    session = AuditSession.new("test claim")
    with pytest.raises(KeyError):
        session.record(1, "not_a_real_criterion", met=True)


def test_phase_passes_only_when_all_criteria_met():
    session = AuditSession.new("test claim")
    phase1_keys = [c.key for c in session.phases[1].criteria.values()]
    for key in phase1_keys[:-1]:
        session.record(1, key, met=True)
    assert session.phase_status(1) == PhaseStatus.IN_PROGRESS
    session.record(1, phase1_keys[-1], met=True)
    assert session.phase_status(1) == PhaseStatus.PASSED


def test_one_unmet_criterion_fails_the_phase():
    session = AuditSession.new("test claim")
    phase1_keys = [c.key for c in session.phases[1].criteria.values()]
    for key in phase1_keys:
        session.record(1, key, met=True)
    session.record(1, phase1_keys[0], met=False)  # revise one to unmet
    assert session.phase_status(1) == PhaseStatus.FAILED


def test_overall_resolution_falsified_on_any_failed_phase():
    session = AuditSession.new("test claim")
    session.record(5, "no_status_dismissal", met=False)
    assert session.overall_resolution == "Falsified"


def test_overall_resolution_indeterminate_when_incomplete_and_not_escrowed():
    session = AuditSession.new("test claim", escrowed=False)
    assert session.overall_resolution == "Indeterminate"


def test_overall_resolution_falsified_when_incomplete_and_escrowed():
    session = AuditSession.new("test claim", escrowed=True)
    assert session.overall_resolution == "Falsified"


def test_overall_resolution_sustained_requires_every_applicable_phase_passed():
    session = AuditSession.new("test claim", is_timeline_claim=False)
    for n in session.core_phase_numbers:
        phase = session.phases[n]
        if not phase.applicable:
            continue
        for key in phase.criteria:
            session.record(n, key, met=True)
    assert session.overall_resolution == "Sustained"


def test_sustained_still_requires_phase_6_when_timeline_claim():
    session = AuditSession.new("test claim", is_timeline_claim=True)
    for n in session.core_phase_numbers:
        phase = session.phases[n]
        if n == 6:
            continue  # deliberately leave Phase 6 unassessed
        for key in phase.criteria:
            session.record(n, key, met=True)
    assert session.overall_resolution != "Sustained"
    session.record(6, "prediction_locked", met=True)
    session.record(6, "stakes_forfeit_on_failure", met=True)
    session.record(6, "no_early_not_wrong", met=True)
    session.record(6, "calibration_tracked", met=True)
    assert session.overall_resolution == "Sustained"


def test_protocol_integrity_independent_of_claim_resolution():
    session = AuditSession.new("test claim")
    # Sustain the claim itself (all core phases passed)...
    for n in session.core_phase_numbers:
        phase = session.phases[n]
        if not phase.applicable:
            continue
        for key in phase.criteria:
            session.record(n, key, met=True)
    assert session.overall_resolution == "Sustained"
    # ...but fail a meta-protocol criterion; claim resolution must not change.
    session.record(-1, "no_ai_as_judge", met=False)
    assert session.overall_resolution == "Sustained"
    assert session.protocol_integrity_resolution == "compromised"


def test_roundtrip_to_dict_from_dict():
    session = AuditSession.new("roundtrip claim", is_timeline_claim=True, escrowed=True)
    session.record(1, "claim_specified", met=True, evidence="e1", notes="n1")
    session.add_heuristic_flags([{"name": "status_dismissal", "flagged": True}])

    session.add_ai_advisory_flags([{"source": "ai_advisory", "candidate_read": "weaker_substitute"}])

    restored = AuditSession.from_dict(json.loads(json.dumps(session.to_dict())))
    assert restored.claim_text == session.claim_text
    assert restored.is_timeline_claim is True
    assert restored.escrowed is True
    assert restored.phases[1].criteria["claim_specified"].status == CriterionStatus.MET
    assert restored.phases[1].criteria["claim_specified"].evidence == "e1"
    assert restored.heuristic_flags == session.heuristic_flags
    assert restored.ai_advisory_flags == session.ai_advisory_flags
    assert restored.overall_resolution == session.overall_resolution


def test_ai_advisory_flags_kept_separate_from_heuristic_flags():
    session = AuditSession.new("claim")
    session.add_heuristic_flags([{"name": "status_dismissal", "flagged": True}])
    session.add_ai_advisory_flags([{"source": "ai_advisory", "candidate_read": "unclear"}])
    assert len(session.heuristic_flags) == 1
    assert len(session.ai_advisory_flags) == 1
    assert session.heuristic_flags[0] != session.ai_advisory_flags[0]


def test_save_and_load_roundtrip(tmp_path):
    session = AuditSession.new("file roundtrip claim")
    session.record(0, "escrow", met=True, evidence="on file")
    path = tmp_path / "audit.json"
    session.save(path)

    loaded = AuditSession.load(path)
    assert loaded.claim_text == "file roundtrip claim"
    assert loaded.phases[0].criteria["escrow"].status == CriterionStatus.MET
