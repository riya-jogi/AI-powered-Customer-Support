from typing import Literal

from pydantic import BaseModel, Field, field_validator


Category = Literal[
    "PAYMENT",
    "BILLING",
    "ORDER",
    "DELIVERY",
    "REFUND",
    "ACCOUNT",
    "TECHNICAL",
    "COMPLAINT",
    "GENERAL_QUERY",
    "OUT_OF_SCOPE",
]


Priority = Literal["P0", "P1", "P2", "P3"]


class TriageDecision(BaseModel):
    category: Category
    priority: Priority
    summary: str = Field(
        min_length=1,
        max_length=500,
        description="Concise summary based only on the customer message.",
    )
    suggested_action: str = Field(
        min_length=1,
        max_length=500,
        description="Recommended next action for the support team.",
    )
    needs_human: bool
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1.",
    )

    @field_validator("summary", "suggested_action")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty.")

        return value