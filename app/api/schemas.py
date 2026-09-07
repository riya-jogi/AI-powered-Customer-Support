from pydantic import BaseModel, Field

from app.ai.schemas import TriageDecision


class TriageRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000,
        description="Raw customer message to triage.",
    )


class TriageResponse(TriageDecision):
    pass