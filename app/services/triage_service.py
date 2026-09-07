from sqlalchemy.orm import Session

from app.ai.engine import AIEngine
from app.ai.result import AIResult
from app.models.triage import TriageRecord


class TriageService:
    def __init__(self, ai_engine: AIEngine | None = None) -> None:
        self.ai_engine = ai_engine or AIEngine()

    def triage(
        self,
        message: str,
        db: Session,
    ) -> AIResult:

        if not message or not message.strip():
            raise ValueError("Customer message cannot be empty.")

        result = self.ai_engine.triage(message)

        record = TriageRecord(
            customer_message=message,
            category=result.decision.category,
            priority=result.decision.priority,
            summary=result.decision.summary,
            suggested_action=result.decision.suggested_action,
            needs_human=result.decision.needs_human,
            confidence=result.decision.confidence,
            latency_ms=result.latency_ms,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            total_tokens=result.total_tokens,
            estimated_cost_usd=result.estimated_cost_usd,
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return result