from bifp.audit import AuditSession
from bifp.report import render_report


def test_render_report_includes_claim_and_resolution():
    session = AuditSession.new("Model X reasons independently")
    report = render_report(session)
    assert "Model X reasons independently" in report
    assert "Resolution: Indeterminate" in report


def test_render_report_shows_failed_phase_and_evidence():
    session = AuditSession.new("Model X reasons independently")
    session.record(5, "no_status_dismissal", met=False, evidence="see transcript")
    report = render_report(session)
    assert "Resolution: Falsified" in report
    assert "❌ FAILED" in report
    assert "see transcript" in report


def test_render_report_lists_not_yet_assessed_phases():
    session = AuditSession.new("Model X reasons independently")
    report = render_report(session)
    assert "Not yet assessed" in report


def test_render_report_shows_heuristic_flags_section():
    session = AuditSession.new("Model X reasons independently")
    session.add_heuristic_flags([
        {"name": "status_dismissal", "flagged": True, "confidence": "combo",
         "explanation": "test explanation", "matches": [{"text": "i wrote"}]},
    ])
    report = render_report(session)
    assert "Automated Heuristic Flags" in report
    assert "i wrote" in report


def test_render_report_no_phase_prefix_on_meta_sections():
    session = AuditSession.new("Model X reasons independently")
    report = render_report(session)
    assert "### Phase Meta-Protocol" not in report
    assert "### Meta-Protocol: Substrate Independence" in report


def test_render_report_timeline_claim_shows_phase_6():
    session = AuditSession.new("AGI by 2027", is_timeline_claim=True)
    report = render_report(session)
    assert "### Phase 6: Timeline Escrow" in report
    assert "N/A" not in report.split("### Phase 6")[1].split("###")[0]


def test_render_report_non_timeline_claim_marks_phase_6_na():
    session = AuditSession.new("Model X reasons independently", is_timeline_claim=False)
    report = render_report(session)
    section = report.split("### Phase 6")[1].split("###")[0]
    assert "N/A" in section
