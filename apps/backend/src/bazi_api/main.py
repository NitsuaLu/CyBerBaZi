"""BaZi API — FastAPI application entry point.

Run with: uvicorn bazi_api.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bazi_api.config import settings
from bazi_api.routers import paipan, analysis

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="八字排盘算命 REST API",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(paipan.router)
app.include_router(analysis.router)


@app.get("/api/v1/health", tags=["健康检查"])
def health():
    return {"status": "ok", "version": settings.version}
