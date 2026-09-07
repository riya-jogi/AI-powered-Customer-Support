from app.models.triage import TriageRecord


def test_create_triage_record(db_session):
    record = TriageRecord(
        customer_message="My order is late.",
        category="DELIVERY",
        priority="P1",
        summary="The customer's order is delayed.",
        suggested_action="Check the shipment status.",
        needs_human=False,
        confidence=0.91,
        latency_ms=500.0,
        input_tokens=100,
        output_tokens=40,
        total_tokens=140,
        estimated_cost_usd=0.000068,
    )

    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)

    assert record.id is not None
    assert record.category == "DELIVERY"
    assert record.priority == "P1"
    assert record.confidence == 0.91