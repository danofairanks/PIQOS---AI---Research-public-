import pytest

from bifp.protocol import ALL_SECTIONS, PHASES, get_criterion, get_phase


def test_phases_numbered_0_through_6():
    assert [p.number for p in PHASES] == [0, 1, 2, 3, 4, 5, 6]


def test_only_phase_6_is_timeline_only():
    assert [p.timeline_only for p in PHASES] == [False, False, False, False, False, False, True]


def test_every_phase_has_criteria():
    for phase in PHASES:
        assert len(phase.criteria) > 0, f"Phase {phase.number} has no criteria"


def test_criterion_keys_unique_within_phase():
    for phase in PHASES:
        keys = [c.key for c in phase.criteria]
        assert len(keys) == len(set(keys)), f"Phase {phase.number} has duplicate criterion keys"


def test_get_phase_and_get_criterion():
    phase5 = get_phase(5)
    assert phase5.name == "Falsification Adjudication"
    crit = get_criterion(5, "no_status_dismissal")
    assert "credentials" in crit.text.lower()


def test_get_phase_unknown_raises():
    with pytest.raises(KeyError):
        get_phase(99)


def test_get_criterion_unknown_raises():
    with pytest.raises(KeyError):
        get_criterion(5, "not_a_real_criterion")


def test_meta_and_semantic_hygiene_present_in_all_sections():
    numbers = {s.number for s in ALL_SECTIONS}
    assert -1 in numbers  # Meta-Protocol
    assert -2 in numbers  # Semantic Hygiene Amendment
