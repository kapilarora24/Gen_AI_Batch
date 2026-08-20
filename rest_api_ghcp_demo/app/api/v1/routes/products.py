"""
Product API routes.

Handles HTTP endpoints for product management.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/api/v1/products", tags=["products"])
service = ProductService()


@router.get("", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
async def list_products(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum items to return"),
    search: Optional[str] = Query(None, description="Search by name or description"),
) -> list[ProductResponse]:
    """List all products with optional pagination and search.

    Args:
        skip: Number of items to skip.
        limit: Maximum number of items to return.
        search: Optional search query.

    Returns:
        List of products.
    """
    if search:
        products = service.search_products(search)
    else:
        products = service.get_all_products()

    return products[skip : skip + limit]


@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_product(product_id: int) -> ProductResponse:
    """Get a product by ID.

    Args:
        product_id: The product ID.

    Returns:
        Product details.

    Raises:
        HTTPException: If product not found.
    """
    product = service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )
    return product


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate) -> ProductResponse:
    """Create a new product.

    Args:
        payload: Product creation data.

    Returns:
        Created product.

    Raises:
        HTTPException: If validation fails.
    """
    try:
        product = service.create_product(
            name=payload.name,
            price=payload.price,
            description=payload.description,
            stock=payload.stock,
        )
        return product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.put(
    "/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK
)
async def update_product(
    product_id: int, payload: ProductUpdate
) -> ProductResponse:
    """Update an existing product.

    Args:
        product_id: The product ID.
        payload: Update data.

    Returns:
        Updated product.

    Raises:
        HTTPException: If product not found or validation fails.
    """
    try:
        product = service.update_product(
            product_id,
            name=payload.name,
            price=payload.price,
            description=payload.description,
            stock=payload.stock,
        )
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found",
            )
        return product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int) -> None:
    """Delete a product.

    Args:
        product_id: The product ID.

    Raises:
        HTTPException: If product not found.
    """
    if not service.delete_product(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )
