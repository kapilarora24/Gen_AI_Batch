"""
FastAPI application initialization and setup.

Main application entry point with middleware and route configuration.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

from app.config import settings
from app.api.v1.routes import products

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI instance.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log all incoming requests."""
        start_time = datetime.now()
        logger.info(
            f"Incoming request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )

        response = await call_next(request)

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(
            f"Request completed: {request.method} {request.url.path} "
            f"- Status: {response.status_code} - Duration: {duration:.2f}s"
        )

        return response

    # Health check endpoint
    @app.get("/api/v1/health", tags=["health"], summary="Health Check")
    async def health_check() -> dict:
        """Check if the API is healthy.

        Returns:
            Health status with timestamp.
        """
        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version,
            "timestamp": datetime.now().isoformat(),
        }

    # Global exception handler
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Handle ValueError exceptions.

        Args:
            request: The request that caused the error.
            exc: The ValueError exception.

        Returns:
            JSON error response.
        """
        logger.error(f"Validation error: {exc}")
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    # Include routers
    app.include_router(products.router)

    logger.info(f"FastAPI application initialized: {settings.app_name}")
    return app


# Create app instance
app = create_app()
