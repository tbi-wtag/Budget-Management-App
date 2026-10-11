from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=getattr(settings, "PROJECT_NAME", getattr(settings, "project_name", "Budget Tracker API")),
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "online",
        "app_name": getattr(settings, "PROJECT_NAME", getattr(settings, "project_name", "Budget Tracker API")),
        "environment": getattr(settings, "ENVIRONMENT", getattr(settings, "environment", "development")),
    }


# Register API v1 endpoints
app.include_router(api_router, prefix="/api/v1")