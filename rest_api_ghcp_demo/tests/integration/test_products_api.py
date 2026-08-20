"""
Integration tests for Product API.

Tests for complete workflows and multiple components working together.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestProductWorkflows:
    """Integration tests for complete product management workflows."""

    def test_create_read_update_delete_workflow(self, client: TestClient):
        """Should complete full CRUD workflow."""
        # Create
        create_payload = {
            "name": "Integration Test Product",
            "description": "Test product for workflow",
            "price": 199.99,
            "stock": 5,
        }
        create_response = client.post("/api/v1/products", json=create_payload)
        assert create_response.status_code == 201
        product = create_response.json()
        product_id = product["id"]

        # Read
        get_response = client.get(f"/api/v1/products/{product_id}")
        assert get_response.status_code == 200
        retrieved = get_response.json()
        assert retrieved["name"] == "Integration Test Product"
        assert retrieved["price"] == 199.99

        # Update
        update_payload = {"price": 249.99, "stock": 10}
        update_response = client.put(f"/api/v1/products/{product_id}", json=update_payload)
        assert update_response.status_code == 200
        updated = update_response.json()
        assert updated["price"] == 249.99
        assert updated["stock"] == 10

        # Delete
        delete_response = client.delete(f"/api/v1/products/{product_id}")
        assert delete_response.status_code == 204

        # Verify deletion
        verify_response = client.get(f"/api/v1/products/{product_id}")
        assert verify_response.status_code == 404

    def test_search_and_retrieve_workflow(self, client: TestClient):
        """Should search and retrieve product details."""
        # Search for product
        search_response = client.get("/api/v1/products?search=Keyboard")
        assert search_response.status_code == 200
        products = search_response.json()
        assert len(products) > 0

        # Get details of first result
        product = products[0]
        details_response = client.get(f"/api/v1/products/{product['id']}")
        assert details_response.status_code == 200
        details = details_response.json()
        assert details["id"] == product["id"]

    def test_multiple_products_listing_and_pagination(self, client: TestClient):
        """Should handle multiple products with pagination."""
        # Get all products
        all_response = client.get("/api/v1/products")
        assert all_response.status_code == 200
        all_products = all_response.json()
        initial_count = len(all_products)

        # Create multiple products
        for i in range(3):
            payload = {"name": f"Pagination Test {i}", "price": 99.99}
            response = client.post("/api/v1/products", json=payload)
            assert response.status_code == 201

        # Test pagination
        page1_response = client.get("/api/v1/products?skip=0&limit=5")
        page1 = page1_response.json()
        assert len(page1) <= 5

        page2_response = client.get("/api/v1/products?skip=5&limit=5")
        page2 = page2_response.json()
        # Page 2 may have fewer items

    def test_create_update_multiple_products(self, client: TestClient):
        """Should create and update multiple products independently."""
        # Create two products
        product1_payload = {"name": "Product 1", "price": 100.0, "stock": 10}
        product2_payload = {"name": "Product 2", "price": 200.0, "stock": 20}

        response1 = client.post("/api/v1/products", json=product1_payload)
        response2 = client.post("/api/v1/products", json=product2_payload)

        assert response1.status_code == 201
        assert response2.status_code == 201

        product1 = response1.json()
        product2 = response2.json()

        # Update product 1
        update1_payload = {"price": 150.0}
        update1_response = client.put(f"/api/v1/products/{product1['id']}", json=update1_payload)
        assert update1_response.status_code == 200
        updated1 = update1_response.json()
        assert updated1["price"] == 150.0

        # Verify product 2 unchanged
        verify2_response = client.get(f"/api/v1/products/{product2['id']}")
        assert verify2_response.status_code == 200
        verified2 = verify2_response.json()
        assert verified2["price"] == 200.0

    def test_validation_error_handling(self, client: TestClient):
        """Should properly handle validation errors."""
        # Missing required field
        invalid_payload1 = {"price": 99.99}
        response1 = client.post("/api/v1/products", json=invalid_payload1)
        assert response1.status_code == 422

        # Invalid type
        invalid_payload2 = {"name": "Test", "price": "invalid"}
        response2 = client.post("/api/v1/products", json=invalid_payload2)
        assert response2.status_code == 422

        # Invalid value
        invalid_payload3 = {"name": "Test", "price": -10.0}
        response3 = client.post("/api/v1/products", json=invalid_payload3)
        assert response3.status_code == 400
