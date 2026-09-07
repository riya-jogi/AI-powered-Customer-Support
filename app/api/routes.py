from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.services.triage_service import TriageService
from app.api.schemas import (
    TriageHistoryItem,
    TriageRequest,
    TriageResponse,
)
from app.models.triage import TriageRecord
router = APIRouter()

triage_service = TriageService()


@router.post(
    "/triage",
    response_model=TriageResponse,
)
@router.get(
    "/triage",
    response_model=list[TriageHistoryItem],
)
def get_triage_history(
    db: Session = Depends(get_db),
) -> list[TriageHistoryItem]:

    records = (
        db.query(TriageRecord)
        .order_by(TriageRecord.created_at.desc())
        .all()
    )

    return records
def triage_customer_message(
    request: TriageRequest,
    db: Session = Depends(get_db),
) -> TriageResponse:

    try:
        result = triage_service.triage(
            request.message,
            db,
        )

        return TriageResponse(
            **result.decision.model_dump()
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable.",
        ) from exc