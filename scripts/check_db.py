from app.models.database import SessionLocal
from app.models.triage import TriageRecord


def main():
    db = SessionLocal()

    try:
        records = db.query(TriageRecord).all()

        print(f"Total records: {len(records)}")

        for record in records:
            print("\nRecord")
            print("=" * 40)
            print(f"ID: {record.id}")
            print(f"Message: {record.customer_message}")
            print(f"Category: {record.category}")
            print(f"Priority: {record.priority}")
            print(f"Human: {record.needs_human}")
            print(f"Confidence: {record.confidence}")
            print(f"Latency: {record.latency_ms:.2f} ms")
            print(f"Cost: {record.estimated_cost_usd}")

    finally:
        db.close()


if __name__ == "__main__":
    main()