from fastapi import FastAPI

from app.api.routes import router
from app.models.database import Base, engine
from app.models.triage import TriageRecord


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Frontline AI",
    description="AI-powered customer support triage system",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(router)