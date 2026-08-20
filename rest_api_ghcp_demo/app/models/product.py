"""
Domain models for Product.

These represent the core business entities.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Product:
    """Product domain model."""

    id: int
    name: str
    description: str | None
    price: float
    stock: int
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
