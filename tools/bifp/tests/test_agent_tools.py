import json

from bifp.agent_tools import (
    bifp_attach_scan_to_audit, bifp_generate_report, bifp_get_status,
    bifp_list_phases, bifp_record_criterion, bifp_scan_text, bifp_start_audit,
)


def test_bifp_list_phases_is_json_safe_and_complete():
    schema = bifp_list_phases()
    json.dumps(schema)  # must not raise
    numbers = {s["number"] for s in schema["sections"]}
    assert numbers == {0, 1, 2, 3, 4, 5, 6, -1, -2}


def test_start_audit_and_get_status_roundtrip(tmp_path):
    path = str(tmp_path / "audit.json")
    result = bifp_start_audit(path, "test claim", is_timeline_claim=False)
    assert result["overall_resolution"] == "Indeterminate"
    status = bifp_get_status(path)
    assert status["claim_text"] == "test claim"


def test_get_status_missing_file_returns_error_dict_not_exception():
    result = bifp_get_status("/nonexistent/path/audit.json")
    assert "error" in result


def test_record_criterion_full_flow(tmp_path):
    path = str(tmp_path / "audit.json")
    bifp_start_audit(path, "test claim")
    result = bifp_record_criterion(path, 5, "no_status_dismissal", False,
                                    evidence="matched heuristic scan")
    assert result["overall_resolution"] == "Falsified"
    assert result["phases"]["5"] == "failed"


def test_record_criterion_unknown_key_returns_error(tmp_path):
    path = str(tmp_path / "audit.json")
    bifp_start_audit(path, "test claim")
    result = bifp_record_criterion(path, 5, "not_a_real_key", True)
    assert "error" in result


def test_scan_text_standalone_json_safe():
    result = bifp_scan_text("we're working on it")
    json.dumps(result)  # must not raise
    assert result["provisionalization"]["flagged"] is True


def test_attach_scan_to_audit_persists_flags(tmp_path):
    path = str(tmp_path / "audit.json")
    bifp_start_audit(path, "test claim")
    bifp_attach_scan_to_audit(path, "we're working on it, that's just a hot take")

    from bifp.audit import AuditSession
    session = AuditSession.load(path)
    assert len(session.heuristic_flags) == 3  # one per scanner


def test_generate_report_returns_markdown(tmp_path):
    path = str(tmp_path / "audit.json")
    bifp_start_audit(path, "test claim")
    result = bifp_generate_report(path)
    assert "markdown" in result
    assert "BIFP Audit Report" in result["markdown"]


def test_generate_report_missing_audit_returns_error():
    result = bifp_generate_report("/nonexistent/audit.json")
    assert "error" in result
