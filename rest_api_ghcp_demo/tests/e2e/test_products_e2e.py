"""
End-to-end tests for Product API.

Tests for realistic user scenarios and full system behavior.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.e2e
class TestProductManagementE2E:
    """End-to-end tests for product management scenarios."""

    def test_complete_product_lifecycle(self, client: TestClient):
        """Test a realistic product management scenario.

        Simulates a user:
        1. Browsing available products
        2. Creating a new product
        3. Modifying the product
        4. Viewing all products again
        """
        # Step 1: Browse available products
        browse_response = client.get("/api/v1/products")
        assert browse_response.status_code == 200
        initial_products = browse_response.json()
        initial_count = len(initial_products)

        # Step 2: Create a new product
        new_product_data = {
            "name": "E2E Test Product - Premium Headphones",
            "description": "High-quality wireless headphones with noise cancellation",
            "price": 299.99,
            "stock": 25,
        }
        create_response = client.post("/api/v1/products", json=new_product_data)
        assert create_response.status_code == 201
        created_product = create_response.json()
        product_id = created_product["id"]

        # Verify product was created correctly
        assert created_product["name"] == "E2E Test Product - Premium Headphones"
        assert created_product["price"] == 299.99
        assert created_product["stock"] == 25
        assert "created_at" in created_product
        assert "updated_at" in created_product

        # Step 3: Modify the product
        # First price adjustment
        price_adjustment = {"price": 279.99}
        update1_response = client.put(f"/api/v1/products/{product_id}", json=price_adjustment)
        assert update1_response.status_code == 200
        updated1 = update1_response.json()
        assert updated1["price"] == 279.99

        # Stock update after sales
        stock_update = {"stock": 20}
        update2_response = client.put(f"/api/v1/products/{product_id}", json=stock_update)
        assert update2_response.status_code == 200
        updated2 = update2_response.json()
        assert updated2["stock"] == 20

        # Step 4: Verify product in listing
        list_response = client.get("/api/v1/products")
        assert list_response.status_code == 200
        all_products = list_response.json()
        assert len(all_products) == initial_count + 1

        # Find our product in the list
        found = False
        for product in all_products:
            if product["id"] == product_id:
                found = True
                assert product["price"] == 279.99
                assert product["stock"] == 20
                break
        assert found

    def test_inventory_management_scenario(self, client: TestClient):
        """Test realistic inventory management workflow."""
        # Check current stock levels
        products_response = client.get("/api/v1/products")
        assert products_response.status_code == 200
        products = products_response.json()

        # Create new product for inventory test
        inventory_test = {
            "name": "Inventory Test - Cables",
            "price": 19.99,
            "stock": 100,
        }
        create_response = client.post("/api/v1/products", json=inventory_test)
        product = create_response.json()
        product_id = product["id"]

        # Simulate sales by reducing stock
        sale_update = {"stock": 95}
        sale_response = client.put(f"/api/v1/products/{product_id}", json=sale_update)
        assert sale_response.status_code == 200

        # Simulate restock
        restock_update = {"stock": 150}
        restock_response = client.put(f"/api/v1/products/{product_id}", json=restock_update)
        assert restock_response.status_code == 200
        restocked = restock_response.json()
        assert restocked["stock"] == 150

    def test_product_search_and_discovery(self, client: TestClient):
        """Test product discovery through various search methods."""
        # Search by name
        search_by_name = client.get("/api/v1/products?search=laptop")
        assert search_by_name.status_code == 200
        results = search_by_name.json()
        assert len(results) > 0

        # List all and paginate
        page1 = client.get("/api/v1/products?skip=0&limit=3")
        assert page1.status_code == 200
        page1_products = page1.json()
        assert len(page1_products) <= 3

        # Get specific product details
        if page1_products:
            first_product_id = page1_products[0]["id"]
            detail_response = client.get(f"/api/v1/products/{first_product_id}")
            assert detail_response.status_code == 200
            details = detail_response.json()
            assert details["id"] == first_product_id

    def test_error_handling_and_edge_cases(self, client: TestClient):
        """Test error handling and edge cases."""
        # Try to get non-existent product
        nonexistent = client.get("/api/v1/products/9999")
        assert nonexistent.status_code == 404

        # Try to delete non-existent product
        delete_nonexistent = client.delete("/api/v1/products/9999")
        assert delete_nonexistent.status_code == 404

        # Try to create with invalid data
        invalid_create = client.post("/api/v1/products", json={"name": "Test", "price": -100})
        assert invalid_create.status_code == 400

        # Try to update with invalid data
        valid_product = client.post("/api/v1/products", json={"name": "Valid", "price": 50.0})
        product_id = valid_product.json()["id"]

        invalid_update = client.put(f"/api/v1/products/{product_id}", json={"price": -50.0})
        assert invalid_update.status_code == 400

    def test_concurrent_product_operations(self, client: TestClient):
        """Test handling multiple product operations in sequence."""
        # Create multiple products
        product_ids = []
        for i in range(5):
            payload = {
                "name": f"Concurrent Test Product {i}",
                "price": 50.0 + i * 10,
                "stock": 10 * (i + 1),
            }
            response = client.post("/api/v1/products", json=payload)
            assert response.status_code == 201
            product_ids.append(response.json()["id"])

        # Update all products
        for product_id in product_ids:
            update = {"stock": 5}
            response = client.put(f"/api/v1/products/{product_id}", json=update)
            assert response.status_code == 200

        # Verify all updates
        for product_id in product_ids:
            response = client.get(f"/api/v1/products/{product_id}")
            assert response.status_code == 200
            assert response.json()["stock"] == 5

        # Delete all products
        for product_id in product_ids:
            response = client.delete(f"/api/v1/products/{product_id}")
            assert response.status_code == 204
