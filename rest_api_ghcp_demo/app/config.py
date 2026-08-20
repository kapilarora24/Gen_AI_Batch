"""
Application configuration.

Settings for the FastAPI application.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Product Management API"
    app_version: str = "1.0.0"
    app_description: str = "Production-ready REST API for managing products"

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    reload: bool = True

    # Logging
    log_level: str = "INFO"

    class Config:
        """Pydantic settings configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
