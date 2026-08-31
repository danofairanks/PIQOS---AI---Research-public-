import json

from bifp.agent_tools import (
    bifp_attach_rebuttal_judgment, bifp_attach_scan_to_audit, bifp_generate_report,
    bifp_get_closed_path_status, bifp_get_status, bifp_judge_rebuttal, bifp_list_phases,
    bifp_record_criterion, bifp_record_fixture, bifp_scan_closed_path_language,
    bifp_scan_hardcoded_assertion_style, bifp_scan_text, bifp_start_audit,
    bifp_start_closed_path_ledger,
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


def test_closed_path_ledger_full_flow_json_safe(tmp_path):
    path = str(tmp_path / "ledger.json")
    result = bifp_start_closed_path_ledger(path, "generic artifact under test")
    json.dumps(result)
    assert result["closed_path_ratio"] is None

    result = bifp_record_fixture(path, "f1", "asserted", notes="literal constant")
    json.dumps(result)
    assert result["asserted_count"] == 1
    assert result["closed_path_ratio"] == 1.0

    result = bifp_record_fixture(path, "f2", "derived")
    assert result["closed_path_ratio"] == 0.5

    status = bifp_get_closed_path_status(path)
    assert status["flagged_fixture_ids"] == ["f1"]


def test_record_fixture_unknown_derivation_returns_error(tmp_path):
    path = str(tmp_path / "ledger.json")
    bifp_start_closed_path_ledger(path, "x")
    result = bifp_record_fixture(path, "f1", "not_a_real_kind")
    assert "error" in result


def test_get_closed_path_status_missing_file_returns_error_dict():
    result = bifp_get_closed_path_status("/nonexistent/ledger.json")
    assert "error" in result


def test_scan_closed_path_language_standalone_json_safe():
    result = bifp_scan_closed_path_language(
        "The repository was independently cloned and reproduced by a third-party audit."
    )
    json.dumps(result)
    assert result["open_path_signals"]


def test_scan_hardcoded_assertion_style_standalone_json_safe():
    result = bifp_scan_hardcoded_assertion_style('assert result == "ALLOW"')
    json.dumps(result)
    assert len(result["matches"]) == 1


def test_judge_rebuttal_missing_key_returns_error_dict_not_exception(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    result = bifp_judge_rebuttal("claim", "rebuttal")
    assert "error" in result
    assert "GROQ_API_KEY" in result["error"]


def test_judge_rebuttal_standalone_json_safe(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "bifp.rebuttal_judge._call_groq_api",
        lambda payload, api_key: {
            "choices": [{"message": {"content": json.dumps({
                "candidate_read": "addresses_actual_claim", "reasoning": "ok",
                "weakened_restatement_quote": None, "self_reported_confidence": "high",
            })}}]
        },
    )
    result = bifp_judge_rebuttal("claim text", "rebuttal text")
    json.dumps(result)  # must not raise
    assert result["candidate_read"] == "addresses_actual_claim"
    assert result["source"] == "ai_advisory"


def test_attach_rebuttal_judgment_persists_to_ai_advisory_flags(tmp_path, monkeypatch):
    path = str(tmp_path / "audit.json")
    bifp_start_audit(path, "test claim")
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "bifp.rebuttal_judge._call_groq_api",
        lambda payload, api_key: {
            "choices": [{"message": {"content": json.dumps({
                "candidate_read": "weaker_substitute", "reasoning": "narrower target",
                "weakened_restatement_quote": "easier claim", "self_reported_confidence": "medium",
            })}}]
        },
    )
    result = bifp_attach_rebuttal_judgment(path, "the actual claim", "a rebuttal of something easier")
    assert result["flagged"] is True

    from bifp.audit import AuditSession
    session = AuditSession.load(path)
    assert len(session.ai_advisory_flags) == 1
    assert session.heuristic_flags == []  # kept in the separate list, not this one
    assert session.ai_advisory_flags[0]["candidate_read"] == "weaker_substitute"

    # Never sets a criterion outcome -- §3.7's criterion is still unassessed.
    assert session.phases[5].criteria["no_weaker_substitute_rebuttal"].status.value == "unassessed"


def test_attach_rebuttal_judgment_missing_audit_returns_error(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    result = bifp_attach_rebuttal_judgment("/nonexistent/audit.json", "c", "r")
    assert "error" in result


def test_attach_rebuttal_judgment_api_failure_does_not_write_partial_state(tmp_path, monkeypatch):
    path = str(tmp_path / "audit.json")
    bifp_start_audit(path, "test claim")
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    result = bifp_attach_rebuttal_judgment(path, "c", "r")
    assert "error" in result

    from bifp.audit import AuditSession
    session = AuditSession.load(path)
    assert session.ai_advisory_flags == []
