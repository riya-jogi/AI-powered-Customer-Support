import pytest
from pydantic import ValidationError

from app.ai.schemas import TriageDecision


def test_valid_triage_decision():
    decision = TriageDecision(
        category="PAYMENT",
        priority="P1",
        summary="Payment was deducted but the order failed.",
        suggested_action="Verify the payment and order status.",
        needs_human=False,
        confidence=0.94,
    )

    assert decision.category == "PAYMENT"
    assert decision.priority == "P1"
    assert decision.needs_human is False
    assert decision.confidence == 0.94


def test_invalid_priority():
    with pytest.raises(ValidationError):
        TriageDecision(
            category="PAYMENT",
            priority="URGENT",
            summary="Payment issue.",
            suggested_action="Investigate payment.",
            needs_human=False,
            confidence=0.90,
        )


def test_invalid_category():
    with pytest.raises(ValidationError):
        TriageDecision(
            category="RANDOM",
            priority="P2",
            summary="Some issue.",
            suggested_action="Investigate.",
            needs_human=False,
            confidence=0.80,
        )


def test_invalid_confidence():
    with pytest.raises(ValidationError):
        TriageDecision(
            category="PAYMENT",
            priority="P1",
            summary="Payment issue.",
            suggested_action="Investigate.",
            needs_human=False,
            confidence=1.5,
        )


def test_empty_summary():
    with pytest.raises(ValidationError):
        TriageDecision(
            category="PAYMENT",
            priority="P1",
            summary="   ",
            suggested_action="Investigate.",
            needs_human=False,
            confidence=0.90,
        )