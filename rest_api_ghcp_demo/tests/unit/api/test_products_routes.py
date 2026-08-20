"""
Unit tests for Product API routes.

Tests for endpoint functionality and HTTP status codes.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
class TestProductEndpointsGet:
    """Tests for GET endpoints."""

    def test_list_products_returns_200(self, client: TestClient):
        """Should return 200 status for list products."""
        response = client.get("/api/v1/products")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_list_products_returns_all(self, client: TestClient):
        """Should return all products."""
        response = client.get("/api/v1/products")
        products = response.json()
        assert len(products) > 0

    def test_list_products_with_skip_and_limit(self, client: TestClient):
        """Should respect skip and limit parameters."""
        response = client.get("/api/v1/products?skip=1&limit=2")
        products = response.json()
        assert len(products) <= 2

    def test_list_products_search_by_name(self, client: TestClient):
        """Should filter products by search query."""
        response = client.get("/api/v1/products?search=Laptop")
        products = response.json()
        assert len(products) == 1
        assert "Laptop" in products[0]["name"]

    def test_get_product_by_valid_id(self, client: TestClient):
        """Should return product for valid ID."""
        response = client.get("/api/v1/products/1")
        assert response.status_code == 200
        product = response.json()
        assert product["id"] == 1
        assert product["name"] == "Laptop"

    def test_get_product_by_invalid_id_returns_404(self, client: TestClient):
        """Should return 404 for non-existent product."""
        response = client.get("/api/v1/products/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_health_check_returns_200(self, client: TestClient):
        """Should return 200 status for health check."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


@pytest.mark.unit
class TestProductEndpointsPost:
    """Tests for POST endpoints."""

    def test_create_product_returns_201(self, client: TestClient):
        """Should return 201 status when creating product."""
        payload = {"name": "New Product", "price": 99.99, "stock": 10}
        response = client.post("/api/v1/products", json=payload)
        assert response.status_code == 201

    def test_create_product_with_valid_data(self, client: TestClient):
        """Should create product with valid data."""
        payload = {
            "name": "New Product",
            "description": "Test description",
            "price": 99.99,
            "stock": 10,
        }
        response = client.post("/api/v1/products", json=payload)
        product = response.json()
        assert product["name"] == "New Product"
        assert product["price"] == 99.99
        assert product["stock"] == 10

    def test_create_product_without_optional_fields(self, client: TestClient):
        """Should create product with only required fields."""
        payload = {"name": "Simple Product", "price": 49.99}
        response = client.post("/api/v1/products", json=payload)
        assert response.status_code == 201
        product = response.json()
        assert product["name"] == "Simple Product"
        assert product["description"] is None
        assert product["stock"] == 0

    def test_create_product_missing_name_returns_422(self, client: TestClient):
        """Should return 422 if name is missing."""
        payload = {"price": 99.99}
        response = client.post("/api/v1/products", json=payload)
        assert response.status_code == 422

    def test_create_product_missing_price_returns_422(self, client: TestClient):
        """Should return 422 if price is missing."""
        payload = {"name": "Product"}
        response = client.post("/api/v1/products", json=payload)
        assert response.status_code == 422

    def test_create_product_invalid_price_returns_400(self, client: TestClient):
        """Should return 400 for invalid price."""
        payload = {"name": "Product", "price": -10.0}
        response = client.post("/api/v1/products", json=payload)
        assert response.status_code == 400

    def test_create_product_empty_name_returns_400(self, client: TestClient):
        """Should return 400 for empty name."""
        payload = {"name": "", "price": 99.99}
        response = client.post("/api/v1/products", json=payload)
        assert response.status_code == 400


@pytest.mark.unit
class TestProductEndpointsPut:
    """Tests for PUT endpoints."""

    def test_update_product_returns_200(self, client: TestClient):
        """Should return 200 status when updating product."""
        payload = {"name": "Updated Laptop"}
        response = client.put("/api/v1/products/1", json=payload)
        assert response.status_code == 200

    def test_update_product_name(self, client: TestClient):
        """Should update product name."""
        payload = {"name": "Updated Product"}
        response = client.put("/api/v1/products/1", json=payload)
        product = response.json()
        assert product["name"] == "Updated Product"

    def test_update_product_price(self, client: TestClient):
        """Should update product price."""
        payload = {"price": 1500.0}
        response = client.put("/api/v1/products/1", json=payload)
        product = response.json()
        assert product["price"] == 1500.0

    def test_update_product_stock(self, client: TestClient):
        """Should update product stock."""
        payload = {"stock": 50}
        response = client.put("/api/v1/products/1", json=payload)
        product = response.json()
        assert product["stock"] == 50

    def test_update_nonexistent_product_returns_404(self, client: TestClient):
        """Should return 404 for non-existent product."""
        payload = {"name": "Updated"}
        response = client.put("/api/v1/products/999", json=payload)
        assert response.status_code == 404

    def test_update_product_invalid_price_returns_400(self, client: TestClient):
        """Should return 400 for invalid price."""
        payload = {"price": -100.0}
        response = client.put("/api/v1/products/1", json=payload)
        assert response.status_code == 400


@pytest.mark.unit
class TestProductEndpointsDelete:
    """Tests for DELETE endpoints."""

    def test_delete_product_returns_204(self, client: TestClient):
        """Should return 204 status when deleting product."""
        response = client.delete("/api/v1/products/1")
        assert response.status_code == 204

    def test_delete_product_removes_product(self, client: TestClient):
        """Should remove product after deletion."""
        client.delete("/api/v1/products/1")
        response = client.get("/api/v1/products/1")
        assert response.status_code == 404

    def test_delete_nonexistent_product_returns_404(self, client: TestClient):
        """Should return 404 for non-existent product."""
        response = client.delete("/api/v1/products/999")
        assert response.status_code == 404
