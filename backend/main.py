"""
SRM Guide Bot - FastAPI Backend
Main application entry point
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn

# ---- Optional SlowAPI (rate limiting) ----
SLOWAPI_AVAILABLE = True
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    from slowapi.middleware import SlowAPIMiddleware
except Exception:
    SLOWAPI_AVAILABLE = False
    Limiter = None
    _rate_limit_exceeded_handler = None
    get_remote_address = None
    RateLimitExceeded = Exception
    SlowAPIMiddleware = None

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.database import init_db, close_db
from app.core.redis import init_redis, close_redis
from app.core.celery import init_celery
from app.api.v1.api import api_router  # this router also handles slowapi-optional
from app.core.middleware import (
    RequestLoggingMiddleware,
    ResponseTimeMiddleware,
    SecurityHeadersMiddleware
)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize rate limiter (if available)
limiter = Limiter(key_func=get_remote_address) if SLOWAPI_AVAILABLE else None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("🚀 Starting SRM Guide Bot Backend...")

    await init_db()
    logger.info("✅ Database initialized")

    await init_redis()
    logger.info("✅ Redis initialized")

    init_celery()
    logger.info("✅ Celery initialized")

    yield

    logger.info("🛑 Shutting down SRM Guide Bot Backend...")

    await close_db()
    logger.info("✅ Database connections closed")

    await close_redis()
    logger.info("✅ Redis connections closed")


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="SRM Guide Bot API",
        description="Intelligent AI Assistant for SRM University - Comprehensive API for admissions, courses, campus life, and more",
        version="2.0.0",
        docs_url="/api/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/api/redoc" if settings.ENVIRONMENT != "production" else None,
        openapi_url="/api/openapi.json" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan
    )

    # Rate limiting (only if SlowAPI is installed)
    if SLOWAPI_AVAILABLE and limiter:
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        app.add_middleware(SlowAPIMiddleware)
        logger.info("🛡️  SlowAPI rate limiting enabled")
    else:
        logger.warning("⚠️  SlowAPI not installed; rate limiting is disabled")

    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )

    # Custom middleware
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(ResponseTimeMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    # Routes
    app.include_router(api_router, prefix="/api/v1")

    # Health
    @app.get("/health", tags=["Health"])
    async def health_check():
        return {
            "status": "healthy",
            "service": "SRM Guide Bot API",
            "version": "2.0.0",
            "environment": settings.ENVIRONMENT
        }

    # Root
    @app.get("/", tags=["Root"])
    async def root():
        return {
            "message": "Welcome to SRM Guide Bot API",
            "version": "2.0.0",
            "description": "Intelligent AI Assistant for SRM University",
            "docs": "/api/docs",
            "health": "/health"
        }

    # Exception handlers
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": True, "message": exc.detail, "status_code": exc.status_code}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation Error: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": True, "message": "Validation error", "details": exc.errors()}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": True, "message": "Internal server error", "status_code": 500}
        )

    return app


app = create_application()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )
