"""
Unit tests for ProductService.

Tests for business logic and data operations.
"""

import pytest
from datetime import datetime

from app.services.product_service import ProductService


@pytest.mark.unit
class TestProductServiceGetAll:
    """Tests for retrieving all products."""

    def test_get_all_products_returns_list(self, product_service: ProductService):
        """Should return a list of products."""
        products = product_service.get_all_products()
        assert isinstance(products, list)
        assert len(products) > 0

    def test_get_all_products_sorted_by_id(self, product_service: ProductService):
        """Should return products sorted by ID."""
        products = product_service.get_all_products()
        ids = [p.id for p in products]
        assert ids == sorted(ids)


@pytest.mark.unit
class TestProductServiceGetById:
    """Tests for retrieving a product by ID."""

    def test_get_product_by_valid_id(self, product_service: ProductService):
        """Should return product for valid ID."""
        product = product_service.get_product_by_id(1)
        assert product is not None
        assert product.id == 1
        assert product.name == "Laptop"

    def test_get_product_by_invalid_id_returns_none(self, product_service: ProductService):
        """Should return None for non-existent ID."""
        product = product_service.get_product_by_id(999)
        assert product is None

    def test_get_product_with_zero_id_raises_error(self, product_service: ProductService):
        """Should raise ValueError for zero ID."""
        with pytest.raises(ValueError, match="Product ID must be positive"):
            product_service.get_product_by_id(0)

    def test_get_product_with_negative_id_raises_error(self, product_service: ProductService):
        """Should raise ValueError for negative ID."""
        with pytest.raises(ValueError, match="Product ID must be positive"):
            product_service.get_product_by_id(-1)


@pytest.mark.unit
class TestProductServiceCreate:
    """Tests for creating new products."""

    def test_create_product_successfully(self, product_service: ProductService):
        """Should create a product with valid data."""
        product = product_service.create_product(
            name="Test Product",
            price=99.99,
            description="Test description",
            stock=10,
        )
        assert product.id == 6
        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.description == "Test description"
        assert product.stock == 10

    def test_create_product_with_empty_name_raises_error(self, product_service: ProductService):
        """Should raise ValueError for empty name."""
        with pytest.raises(ValueError, match="Product name cannot be empty"):
            product_service.create_product(name="", price=99.99)

    def test_create_product_with_whitespace_name_raises_error(
        self, product_service: ProductService
    ):
        """Should raise ValueError for whitespace-only name."""
        with pytest.raises(ValueError, match="Product name cannot be empty"):
            product_service.create_product(name="   ", price=99.99)

    def test_create_product_with_zero_price_raises_error(self, product_service: ProductService):
        """Should raise ValueError for zero price."""
        with pytest.raises(ValueError, match="Product price must be greater than 0"):
            product_service.create_product(name="Test", price=0)

    def test_create_product_with_negative_price_raises_error(self, product_service: ProductService):
        """Should raise ValueError for negative price."""
        with pytest.raises(ValueError, match="Product price must be greater than 0"):
            product_service.create_product(name="Test", price=-10.0)

    def test_create_product_with_negative_stock_raises_error(self, product_service: ProductService):
        """Should raise ValueError for negative stock."""
        with pytest.raises(ValueError, match="Stock cannot be negative"):
            product_service.create_product(name="Test", price=99.99, stock=-5)

    def test_create_product_default_stock_is_zero(self, product_service: ProductService):
        """Should default stock to 0."""
        product = product_service.create_product(name="Test", price=99.99)
        assert product.stock == 0

    def test_create_product_sets_timestamps(self, product_service: ProductService):
        """Should set created_at and updated_at timestamps."""
        before_create = datetime.now()
        product = product_service.create_product(name="Test", price=99.99)
        after_create = datetime.now()

        assert before_create <= product.created_at <= after_create
        assert before_create <= product.updated_at <= after_create


@pytest.mark.unit
class TestProductServiceUpdate:
    """Tests for updating products."""

    def test_update_product_name(self, product_service: ProductService):
        """Should update product name."""
        product = product_service.update_product(1, name="Updated Laptop")
        assert product is not None
        assert product.name == "Updated Laptop"

    def test_update_product_price(self, product_service: ProductService):
        """Should update product price."""
        product = product_service.update_product(1, price=1399.99)
        assert product is not None
        assert product.price == 1399.99

    def test_update_product_stock(self, product_service: ProductService):
        """Should update product stock."""
        product = product_service.update_product(1, stock=50)
        assert product is not None
        assert product.stock == 50

    def test_update_product_multiple_fields(self, product_service: ProductService):
        """Should update multiple fields."""
        product = product_service.update_product(1, name="New Laptop", price=1500.0, stock=20)
        assert product.name == "New Laptop"
        assert product.price == 1500.0
        assert product.stock == 20

    def test_update_nonexistent_product_returns_none(self, product_service: ProductService):
        """Should return None for non-existent product."""
        product = product_service.update_product(999, name="Test")
        assert product is None

    def test_update_product_with_empty_name_raises_error(self, product_service: ProductService):
        """Should raise ValueError for empty name."""
        with pytest.raises(ValueError, match="Product name cannot be empty"):
            product_service.update_product(1, name="")

    def test_update_product_with_negative_price_raises_error(self, product_service: ProductService):
        """Should raise ValueError for negative price."""
        with pytest.raises(ValueError, match="Product price must be greater than 0"):
            product_service.update_product(1, price=-100.0)

    def test_update_product_updates_timestamp(self, product_service: ProductService):
        """Should update the updated_at timestamp."""
        original_product = product_service.get_product_by_id(1)
        original_updated_at = original_product.updated_at

        product = product_service.update_product(1, name="Updated")
        assert product.updated_at > original_updated_at


@pytest.mark.unit
class TestProductServiceDelete:
    """Tests for deleting products."""

    def test_delete_existing_product_returns_true(self, product_service: ProductService):
        """Should return True for existing product."""
        result = product_service.delete_product(1)
        assert result is True
        assert product_service.get_product_by_id(1) is None

    def test_delete_nonexistent_product_returns_false(self, product_service: ProductService):
        """Should return False for non-existent product."""
        result = product_service.delete_product(999)
        assert result is False


@pytest.mark.unit
class TestProductServiceSearch:
    """Tests for searching products."""

    def test_search_by_product_name(self, product_service: ProductService):
        """Should find products by name."""
        products = product_service.search_products("Laptop")
        assert len(products) == 1
        assert products[0].name == "Laptop"

    def test_search_by_description(self, product_service: ProductService):
        """Should find products by description."""
        products = product_service.search_products("mechanical")
        assert len(products) == 1
        assert "Mechanical" in products[0].name

    def test_search_case_insensitive(self, product_service: ProductService):
        """Should perform case-insensitive search."""
        products = product_service.search_products("laptop")
        assert len(products) == 1
        assert products[0].name == "Laptop"

    def test_search_empty_query_returns_all(self, product_service: ProductService):
        """Should return all products for empty query."""
        products = product_service.search_products("")
        all_products = product_service.get_all_products()
        assert len(products) == len(all_products)

    def test_search_no_results(self, product_service: ProductService):
        """Should return empty list for no matches."""
        products = product_service.search_products("NonexistentProduct")
        assert len(products) == 0
