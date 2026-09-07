from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.ai.schemas import TriageDecision


class TriageRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000,
        description="Raw customer message to triage.",
    )


class TriageResponse(TriageDecision):
    pass


class TriageHistoryItem(TriageDecision):
    id: int
    customer_message: str
    latency_ms: float
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    estimated_cost_usd: float | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)