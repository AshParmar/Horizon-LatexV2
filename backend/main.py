"""
FastAPI Main Application
AI-Driven Recruitment Automation Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.logger import setup_logging
from core.config import settings
from contextlib import asynccontextmanager

# Import API routers
from api import (
    jd,
    pipeline,
    scoring,
    analytics,
    actions,
    integrations,
    enricher,
    health,
    tasks
)

# Import task scheduler
from tasks.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup: Start the task scheduler
    scheduler.start()
    yield
    # Shutdown: Stop the task scheduler
    scheduler.shutdown()


# Initialize FastAPI app
app = FastAPI(
    title="AI Recruitment Platform API",
    description="Backend API for AI-driven recruitment automation",
    version="1.0.0",
    lifespan=lifespan
)

# Setup logging
setup_logging(app)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(jd.router, prefix="/api/v1/jd", tags=["Job Description"])
app.include_router(pipeline.router, prefix="/api/v1/pipeline", tags=["Pipeline"])
app.include_router(scoring.router, prefix="/api/v1/scoring", tags=["Scoring"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(actions.router, prefix="/api/v1/actions", tags=["Actions"])
app.include_router(integrations.router, prefix="/api/v1/integrations", tags=["Integrations"])
app.include_router(enricher.router, prefix="/api/v1/enricher", tags=["Enricher"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Scheduled Tasks"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Recruitment Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
