from app.ai.policy import (
    CATEGORIES,
    PRIORITIES,
    CATEGORY_DEFINITIONS,
    PRIORITY_DEFINITIONS,
    TRIAGE_POLICY,
)


def test_categories_are_defined():
    assert len(CATEGORIES) == 10

    for category in CATEGORIES:
        assert category in CATEGORY_DEFINITIONS


def test_priorities_are_defined():
    assert PRIORITIES == ("P0", "P1", "P2", "P3")

    for priority in PRIORITIES:
        assert priority in PRIORITY_DEFINITIONS


def test_policy_contains_core_rules():
    assert "Do not invent facts" in TRIAGE_POLICY
    assert "untrusted data" in TRIAGE_POLICY
    assert "OUT_OF_SCOPE" in TRIAGE_POLICY
    assert "P0" in TRIAGE_POLICY
    assert "P1" in TRIAGE_POLICY
    assert "P2" in TRIAGE_POLICY
    assert "P3" in TRIAGE_POLICY