import json

import pytest

from bifp.closed_path import (
    ClosedPathLedger,
    FixtureRecord,
    scan_for_closed_path_language,
    scan_for_hardcoded_assertion_style,
)


# --- FixtureRecord ---------------------------------------------------------

def test_fixture_record_rejects_unknown_derivation_kind():
    with pytest.raises(ValueError):
        FixtureRecord(fixture_id="f1", outcome_derivation="hand-waved")


def test_fixture_record_round_trips_through_dict():
    r = FixtureRecord(fixture_id="f1", outcome_derivation="asserted", notes="literal constant")
    assert FixtureRecord.from_dict(r.to_dict()) == r


# --- ClosedPathLedger --------------------------------------------------

def test_new_ledger_has_no_ratio_until_something_is_classified():
    ledger = ClosedPathLedger(artifact_label="generic artifact under test")
    assert ledger.closed_path_ratio is None
    assert ledger.asserted_count == 0
    assert ledger.derived_count == 0


def test_ratio_distinguishes_none_from_zero():
    """A ledger with only derived fixtures must report ratio 0.0, not
    None -- None means "nothing classified yet", 0.0 means "everything
    classified is derived". Conflating the two would silently treat a
    genuinely strong result the same as an unchecked one."""
    ledger = ClosedPathLedger(artifact_label="x")
    ledger.add_fixture("f1", "derived")
    ledger.add_fixture("f2", "derived")
    assert ledger.closed_path_ratio == 0.0


def test_ratio_ignores_unknown_fixtures():
    ledger = ClosedPathLedger(artifact_label="x")
    ledger.add_fixture("f1", "asserted")
    ledger.add_fixture("f2", "derived")
    ledger.add_fixture("f3", "unknown")
    ledger.add_fixture("f4", "unknown")
    assert ledger.classified_count == 2
    assert ledger.closed_path_ratio == 0.5


def test_re_recording_a_fixture_replaces_not_duplicates():
    ledger = ClosedPathLedger(artifact_label="x")
    ledger.add_fixture("f1", "asserted")
    ledger.add_fixture("f1", "derived", notes="re-read, was wrong the first time")
    assert len(ledger.fixtures) == 1
    assert ledger.fixtures[0].outcome_derivation == "derived"
    assert ledger.asserted_count == 0


def test_flagged_fixture_ids_only_lists_asserted():
    ledger = ClosedPathLedger(artifact_label="x")
    ledger.add_fixture("f1", "asserted")
    ledger.add_fixture("f2", "derived")
    ledger.add_fixture("f3", "asserted")
    assert set(ledger.flagged_fixture_ids) == {"f1", "f3"}


def test_matches_the_papers_own_specimen_ratio():
    """Regression pin against the one specimen closed_path_confirmation_v1.md
    §4 reports: 5 of 59 fixtures asserted, the remaining 54 derived --
    generic fixture ids here, no identifying detail, matching only the
    published counts."""
    ledger = ClosedPathLedger(artifact_label="redacted specimen, see closed_path_confirmation_v1.md §4")
    for i in range(5):
        ledger.add_fixture(f"asserted-{i}", "asserted")
    for i in range(54):
        ledger.add_fixture(f"derived-{i}", "derived")
    assert ledger.classified_count == 59
    assert ledger.asserted_count == 5
    assert round(ledger.closed_path_ratio, 4) == round(5 / 59, 4)


def test_ledger_round_trips_through_save_and_load(tmp_path):
    path = tmp_path / "ledger.json"
    ledger = ClosedPathLedger(artifact_label="x")
    ledger.add_fixture("f1", "asserted", notes="hand-set literal")
    ledger.save(path)

    loaded = ClosedPathLedger.load(path)
    assert loaded.artifact_label == "x"
    assert loaded.asserted_count == 1
    assert loaded.fixtures[0].notes == "hand-set literal"

    # And the file is genuinely plain JSON, not some opaque format.
    raw = json.loads(path.read_text())
    assert raw["artifact_label"] == "x"


# --- scan_for_closed_path_language -----------------------------------

def test_language_scan_flags_closed_path_phrases():
    text = "The suite runs entirely against in-memory fixtures authored by the repo owner."
    result = scan_for_closed_path_language(text)
    assert result.closed_path_signals
    assert not result.open_path_signals


def test_language_scan_flags_open_path_phrases():
    text = "An independent red team was engaged and the repository was independently reproduced."
    result = scan_for_closed_path_language(text)
    assert result.open_path_signals
    assert not result.closed_path_signals


def test_language_scan_neither_signal_is_not_closed_path_by_default():
    text = "This document describes an unrelated topic entirely."
    result = scan_for_closed_path_language(text)
    assert not result.closed_path_signals
    assert not result.open_path_signals
    d = result.to_dict()
    assert "not closed-path by default" in d["note"]


# --- scan_for_hardcoded_assertion_style --------------------------------

def test_hardcoded_assertion_scan_flags_literal_comparison():
    code = 'assert result == 5\nassert status == "ALLOW"\nassert ok == True'
    matches = scan_for_hardcoded_assertion_style(code)
    assert len(matches) == 3


def test_hardcoded_assertion_scan_does_not_flag_variable_comparison():
    code = "assert result == expected_value\nassert status == compute_expected(input)"
    matches = scan_for_hardcoded_assertion_style(code)
    assert matches == []
