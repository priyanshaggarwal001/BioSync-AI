from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(
    title="BioSync AI Health OS",
    version="1.0.0",
    description="AI-powered Health Operating System",
)

app.include_router(api_router)


@app.get("/", tags=["Health Check"])
def root():
    return {
        "message": "Welcome to BioSync AI Health OS 🚀"
    }