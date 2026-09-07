from app.ai.result import AIResult
from app.ai.schemas import TriageDecision
from app.services.triage_service import TriageService


class FakeAIEngine:
    def triage(self, message: str) -> AIResult:
        return AIResult(
            decision=TriageDecision(
                category="PAYMENT",
                priority="P1",
                summary="Payment was deducted but the order failed.",
                suggested_action="Investigate the payment transaction.",
                needs_human=False,
                confidence=0.95,
            ),
            latency_ms=100.0,
            input_tokens=100,
            output_tokens=50,
            total_tokens=150,
            estimated_cost_usd=0.00008,
        )


def test_triage_service():
    service = TriageService(ai_engine=FakeAIEngine())

    result = service.triage(
        "My payment was deducted but my order failed."
    )

    assert result.decision.category == "PAYMENT"
    assert result.decision.priority == "P1"
    assert result.decision.needs_human is False
    assert result.decision.confidence == 0.95


def test_triage_service_rejects_empty_message():
    service = TriageService(ai_engine=FakeAIEngine())

    try:
        service.triage("   ")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Customer message cannot be empty."