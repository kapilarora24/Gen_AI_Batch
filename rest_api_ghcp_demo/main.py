"""
Entry point for running the FastAPI application.

Start the development server with:
    uvicorn main:app --reload

Or start with specific host/port:
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

Access API documentation:
    - Swagger UI: http://localhost:8000/api/docs
    - ReDoc: http://localhost:8000/api/redoc
"""

import uvicorn

from app.main import app
from app.config import settings

if __name__ == "__main__":
    """Run the FastAPI application."""
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )
