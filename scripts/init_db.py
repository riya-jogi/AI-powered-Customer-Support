from app.models.database import Base, engine
from app.models.triage import TriageRecord


def main():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")


if __name__ == "__main__":
    main()