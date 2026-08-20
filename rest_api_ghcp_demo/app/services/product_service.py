"""
Product service layer.

Handles business logic for product operations.
"""

from datetime import datetime
from typing import Optional

from app.models.product import Product


class ProductService:
    """Service for managing products."""

    # Static in-memory storage
    _products: dict[int, Product] = {}
    _next_id: int = 1

    # Initialize with sample data
    @classmethod
    def _initialize_sample_data(cls) -> None:
        """Initialize with sample products."""
        if not cls._products:
            now = datetime.now()
            sample_products = [
                Product(
                    id=1,
                    name="Laptop",
                    description="High-performance laptop for developers",
                    price=1299.99,
                    stock=15,
                    created_at=now,
                    updated_at=now,
                ),
                Product(
                    id=2,
                    name="Mechanical Keyboard",
                    description="RGB mechanical keyboard with hot-swappable switches",
                    price=149.99,
                    stock=50,
                    created_at=now,
                    updated_at=now,
                ),
                Product(
                    id=3,
                    name="Wireless Mouse",
                    description="Ergonomic wireless mouse with precision tracking",
                    price=49.99,
                    stock=100,
                    created_at=now,
                    updated_at=now,
                ),
                Product(
                    id=4,
                    name="Monitor",
                    description="4K ultra-wide monitor for productivity",
                    price=599.99,
                    stock=8,
                    created_at=now,
                    updated_at=now,
                ),
                Product(
                    id=5,
                    name="USB-C Hub",
                    description="7-in-1 USB-C hub with multiple ports",
                    price=79.99,
                    stock=30,
                    created_at=now,
                    updated_at=now,
                ),
            ]
            for product in sample_products:
                cls._products[product.id] = product
            cls._next_id = 6

    def __init__(self) -> None:
        """Initialize the service."""
        self._initialize_sample_data()

    def get_all_products(self) -> list[Product]:
        """Get all products.

        Returns:
            List of all products sorted by ID.
        """
        return sorted(self._products.values(), key=lambda p: p.id)

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get a product by ID.

        Args:
            product_id: The product ID.

        Returns:
            Product if found, None otherwise.

        Raises:
            ValueError: If product_id is invalid.
        """
        if product_id <= 0:
            raise ValueError("Product ID must be positive")
        return self._products.get(product_id)

    def create_product(
        self,
        name: str,
        price: float,
        description: Optional[str] = None,
        stock: int = 0,
    ) -> Product:
        """Create a new product.

        Args:
            name: Product name.
            price: Product price.
            description: Product description.
            stock: Available stock.

        Returns:
            Created product.

        Raises:
            ValueError: If price is invalid or name is empty.
        """
        if not name or not name.strip():
            raise ValueError("Product name cannot be empty")
        if price <= 0:
            raise ValueError("Product price must be greater than 0")
        if stock < 0:
            raise ValueError("Stock cannot be negative")

        product = Product(
            id=self._next_id,
            name=name.strip(),
            description=description,
            price=price,
            stock=stock,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self._products[self._next_id] = product
        self._next_id += 1
        return product

    def update_product(
        self,
        product_id: int,
        name: Optional[str] = None,
        price: Optional[float] = None,
        description: Optional[str] = None,
        stock: Optional[int] = None,
    ) -> Optional[Product]:
        """Update an existing product.

        Args:
            product_id: The product ID.
            name: New product name.
            price: New product price.
            description: New product description.
            stock: New stock quantity.

        Returns:
            Updated product if found, None otherwise.

        Raises:
            ValueError: If validation fails.
        """
        product = self._products.get(product_id)
        if not product:
            return None

        if name is not None:
            if not name.strip():
                raise ValueError("Product name cannot be empty")
            product.name = name.strip()

        if price is not None:
            if price <= 0:
                raise ValueError("Product price must be greater than 0")
            product.price = price

        if description is not None:
            product.description = description

        if stock is not None:
            if stock < 0:
                raise ValueError("Stock cannot be negative")
            product.stock = stock

        product.updated_at = datetime.now()
        return product

    def delete_product(self, product_id: int) -> bool:
        """Delete a product.

        Args:
            product_id: The product ID.

        Returns:
            True if product was deleted, False if not found.
        """
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False

    def search_products(self, query: str) -> list[Product]:
        """Search products by name or description.

        Args:
            query: Search query string.

        Returns:
            List of matching products.
        """
        query_lower = query.lower().strip()
        if not query_lower:
            return self.get_all_products()

        return [
            p
            for p in self._products.values()
            if query_lower in p.name.lower()
            or (p.description and query_lower in p.description.lower())
        ]
