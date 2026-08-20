# API Specification

## Product Management REST API

### Overview
This is a production-ready REST API for managing products with full CRUD operations. The API follows RESTful principles and best practices for API design.

### Base URL
```
http://localhost:8000/api/v1
```

### API Documentation
- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`
- **OpenAPI Schema**: `http://localhost:8000/api/openapi.json`

---

## Endpoints

### 1. Health Check
**Endpoint**: `GET /health`

**Description**: Check if the API is healthy and running.

**Response**: 200 OK
```json
{
  "status": "healthy",
  "service": "Product Management API",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

### 2. List Products
**Endpoint**: `GET /products`

**Description**: Retrieve a list of all products with optional pagination and search.

**Query Parameters**:
- `skip` (integer, optional, default=0): Number of items to skip
- `limit` (integer, optional, default=10, max=100): Maximum items to return
- `search` (string, optional): Search by product name or description

**Response**: 200 OK
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "High-performance laptop for developers",
    "price": 1299.99,
    "stock": 15,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

**Examples**:
```bash
# Get all products
curl http://localhost:8000/api/v1/products

# Paginate: skip first 10, get next 5
curl "http://localhost:8000/api/v1/products?skip=10&limit=5"

# Search for products
curl "http://localhost:8000/api/v1/products?search=laptop"
```

---

### 3. Get Product by ID
**Endpoint**: `GET /products/{product_id}`

**Description**: Retrieve details of a specific product.

**Path Parameters**:
- `product_id` (integer, required): The product ID

**Response**: 200 OK
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "High-performance laptop for developers",
  "price": 1299.99,
  "stock": 15,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Error Response**: 404 Not Found
```json
{
  "detail": "Product with ID 999 not found"
}
```

**Example**:
```bash
curl http://localhost:8000/api/v1/products/1
```

---

### 4. Create Product
**Endpoint**: `POST /products`

**Description**: Create a new product.

**Request Body**:
```json
{
  "name": "Product Name",
  "description": "Optional product description",
  "price": 99.99,
  "stock": 10
}
```

**Required Fields**:
- `name` (string, 1-255 characters)
- `price` (number, > 0)

**Optional Fields**:
- `description` (string, max 1000 characters, default: null)
- `stock` (integer, >= 0, default: 0)

**Response**: 201 Created
```json
{
  "id": 6,
  "name": "Product Name",
  "description": "Optional product description",
  "price": 99.99,
  "stock": 10,
  "created_at": "2024-01-15T10:30:45.123456",
  "updated_at": "2024-01-15T10:30:45.123456"
}
```

**Error Responses**:
- 400 Bad Request: Validation error
- 422 Unprocessable Entity: Missing required fields or invalid types

**Example**:
```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse",
    "price": 49.99,
    "stock": 50
  }'
```

---

### 5. Update Product
**Endpoint**: `PUT /products/{product_id}`

**Description**: Update an existing product. Only provided fields are updated.

**Path Parameters**:
- `product_id` (integer, required): The product ID

**Request Body** (all fields optional):
```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "price": 129.99,
  "stock": 25
}
```

**Response**: 200 OK
```json
{
  "id": 1,
  "name": "Updated Name",
  "description": "Updated description",
  "price": 129.99,
  "stock": 25,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-15T10:30:45.123456"
}
```

**Error Responses**:
- 400 Bad Request: Validation error
- 404 Not Found: Product not found

**Example**:
```bash
curl -X PUT http://localhost:8000/api/v1/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 129.99,
    "stock": 25
  }'
```

---

### 6. Delete Product
**Endpoint**: `DELETE /products/{product_id}`

**Description**: Delete a product.

**Path Parameters**:
- `product_id` (integer, required): The product ID

**Response**: 204 No Content

**Error Response**: 404 Not Found
```json
{
  "detail": "Product with ID 999 not found"
}
```

**Example**:
```bash
curl -X DELETE http://localhost:8000/api/v1/products/1
```

---

## Data Models

### Product
| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique product identifier |
| name | string | Product name (1-255 characters) |
| description | string \| null | Product description (max 1000 characters) |
| price | number | Product price (must be > 0) |
| stock | integer | Available stock quantity (>= 0) |
| created_at | timestamp | When the product was created |
| updated_at | timestamp | When the product was last updated |

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource successfully created |
| 204 | No Content - Successful deletion |
| 400 | Bad Request - Validation error |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Invalid request format |
| 500 | Internal Server Error |

---

## Error Handling

All errors are returned in the following format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Messages
- `"Product with ID {id} not found"` - Requested product doesn't exist
- `"Product name cannot be empty"` - Name is empty or whitespace
- `"Product price must be greater than 0"` - Price is zero or negative
- `"Stock cannot be negative"` - Stock is negative

---

## Pagination

Use `skip` and `limit` parameters for pagination:

```bash
# Get first 10 products
curl "http://localhost:8000/api/v1/products?skip=0&limit=10"

# Get next 10 products
curl "http://localhost:8000/api/v1/products?skip=10&limit=10"
```

---

## Search

Use the `search` parameter to filter products by name or description:

```bash
curl "http://localhost:8000/api/v1/products?search=laptop"
```

The search is case-insensitive and matches partial strings.

---

## Authentication

Currently, this API does not require authentication. In production, implement JWT or API key authentication.

---

## Rate Limiting

Currently, this API does not implement rate limiting. In production, add rate limiting to prevent abuse.

---

## CORS

The API allows requests from all origins. In production, restrict CORS to specific domains.

---

## Versioning

The API uses URL-based versioning. Current version is `v1`.

Future versions will be available at:
- `/api/v2/products`
- `/api/v3/products`
- etc.

---

## Example Usage

### Complete Workflow
```bash
# 1. List all products
curl http://localhost:8000/api/v1/products

# 2. Create a new product
NEW_PRODUCT=$(curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Product",
    "price": 99.99,
    "stock": 10
  }')

PRODUCT_ID=$(echo $NEW_PRODUCT | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

# 3. Get product details
curl http://localhost:8000/api/v1/products/$PRODUCT_ID

# 4. Update the product
curl -X PUT http://localhost:8000/api/v1/products/$PRODUCT_ID \
  -H "Content-Type: application/json" \
  -d '{
    "price": 119.99,
    "stock": 15
  }'

# 5. Search for products
curl "http://localhost:8000/api/v1/products?search=new"

# 6. Delete the product
curl -X DELETE http://localhost:8000/api/v1/products/$PRODUCT_ID
```
