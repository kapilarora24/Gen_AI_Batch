"""
Pydantic schemas for Product API.

These schemas define the request/response structures for the Product API.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class ProductBase(BaseModel):
    """Base schema for Product with common fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, max_length=1000, description="Product description")
    price: float = Field(..., gt=0, description="Product price")
    stock: int = Field(default=0, ge=0, description="Available stock quantity")


class ProductCreate(ProductBase):
    """Schema for creating a new product."""

    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: Optional[float]) -> Optional[float]:
        """Ensure price is positive if provided."""
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than 0")
        return v


class ProductResponse(ProductBase):
    """Schema for product response."""

    id: int = Field(..., description="Product ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic configuration."""

        from_attributes = True
