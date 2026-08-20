"""
Pytest configuration and shared fixtures.

Provides common fixtures for all test types.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.services.product_service import ProductService


@pytest.fixture(scope="function")
def app():
    """Create a test FastAPI application instance."""
    return create_app()


@pytest.fixture(scope="function")
def client(app):
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_product_service():
    """Reset the product service before each test.

    This ensures each test starts with a fresh state.
    """
    ProductService._products = {}
    ProductService._next_id = 1
    yield
    ProductService._products = {}
    ProductService._next_id = 1


@pytest.fixture(scope="function")
def product_service():
    """Create a fresh product service instance."""
    return ProductService()
