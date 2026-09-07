from fastapi import FastAPI

app = FastAPI(
    title="AI-powered Customer Support",
    description="AI-powered customer support triage system",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }