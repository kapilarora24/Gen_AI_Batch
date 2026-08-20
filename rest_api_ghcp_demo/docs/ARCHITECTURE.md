# Architecture

## Project Structure

```
rest_api_ghcp_demo/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI app factory and middleware setup
│   ├── config.py                 # Configuration and settings
│   │
│   ├── api/                      # API endpoints
│   │   ├── __init__.py
│   │   └── v1/                   # API version 1
│   │       ├── __init__.py
│   │       └── routes/
│   │           ├── __init__.py
│   │           └── products.py   # Product endpoints
│   │
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   └── product_service.py    # Product service
│   │
│   ├── models/                   # Domain models
│   │   ├── __init__.py
│   │   └── product.py            # Product domain model
│   │
│   └── schemas/                  # Pydantic request/response schemas
│       ├── __init__.py
│       └── product.py            # Product schemas
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest configuration and fixtures
│   │
│   ├── unit/                     # Unit tests
│   │   ├── __init__.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── test_product_service.py
│   │   └── api/
│   │       ├── __init__.py
│   │       └── test_products_routes.py
│   │
│   ├── integration/              # Integration tests
│   │   ├── __init__.py
│   │   └── test_products_api.py
│   │
│   └── e2e/                      # End-to-end tests
│       ├── __init__.py
│       └── test_products_e2e.py
│
├── docs/                         # Documentation
│   ├── API_SPEC.md              # API specification
│   ├── ARCHITECTURE.md          # This file
│   ├── SETUP.md                 # Setup instructions
│   └── README.md                # Project README
│
├── .gitignore                    # Git ignore rules
├── .env                          # Environment variables
├── pyproject.toml                # Project configuration and dependencies
├── pytest.ini                    # Pytest configuration
├── ruff.toml                     # Ruff linter configuration
├── mypy.ini                      # MyPy type checking configuration
├── main.py                       # Entry point for running the app
└── README.md                     # Root README
```

---

## Architecture Overview

### Layered Architecture

The application follows a **layered architecture** pattern:

```
┌─────────────────────────────────────────┐
│         HTTP Client / Browser            │
└────────────────┬────────────────────────┘
                 │
┌─────────────────▼────────────────────────┐
│       API Routes (FastAPI)                │
│    /api/v1/products endpoints            │
│    - Request validation                  │
│    - HTTP status codes                   │
│    - Response formatting                 │
└────────────────┬────────────────────────┘
                 │
┌─────────────────▼────────────────────────┐
│    Services (Business Logic)              │
│    ProductService                        │
│    - CRUD operations                     │
│    - Business rules                      │
│    - Data validation                     │
└────────────────┬────────────────────────┘
                 │
┌─────────────────▼────────────────────────┐
│    Models (Domain Entities)               │
│    Product                               │
│    - Core business data                  │
│    - Data representation                 │
└────────────────┬────────────────────────┘
                 │
┌─────────────────▼────────────────────────┐
│   Static Data Storage (In-Memory)        │
│    _products: dict[int, Product]         │
└─────────────────────────────────────────┘
```

### Layer Descriptions

#### 1. **API Routes Layer** (`app/api/v1/routes/products.py`)
- **Responsibility**: Handle HTTP requests and responses
- **Includes**:
  - Request validation using Pydantic schemas
  - HTTP status code management
  - Error handling and exception mapping
  - Response formatting
- **Dependencies**: FastAPI, Pydantic schemas, ProductService

#### 2. **Services Layer** (`app/services/product_service.py`)
- **Responsibility**: Business logic and data operations
- **Includes**:
  - CRUD operations
  - Data validation
  - Business rules enforcement
  - Data access logic
- **Dependencies**: Domain models
- **Note**: Currently uses in-memory storage; easily replaceable with database

#### 3. **Models Layer** (`app/models/product.py`)
- **Responsibility**: Domain entity representation
- **Includes**:
  - Core business data structure
  - Domain logic methods
  - Data type definitions
- **Dependencies**: None (core layer)

#### 4. **Schemas Layer** (`app/schemas/product.py`)
- **Responsibility**: Request/response validation
- **Includes**:
  - Pydantic BaseModels
  - Field validation
  - Automatic OpenAPI documentation
- **Dependencies**: Pydantic

---

## Design Patterns

### 1. **Service Pattern**
The `ProductService` class encapsulates all business logic and data operations. This allows:
- Easy testing of business logic independently
- Clear separation of concerns
- Simple replacement of data storage implementation

### 2. **Dependency Injection**
Routes depend on the `ProductService`, making it easy to:
- Mock the service in tests
- Replace the service implementation
- Add cross-cutting concerns

### 3. **Repository Pattern (Simulated)**
The `ProductService._products` dictionary acts as a repository, providing:
- Abstraction of data storage
- Easy transition to database implementation
- Consistent data access interface

### 4. **Factory Pattern**
The `create_app()` function in `main.py` follows the factory pattern for creating configured FastAPI applications.

---

## Technology Stack

### Core Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running FastAPI

### Testing
- **pytest**: Testing framework
- **pytest-asyncio**: Async test support
- **httpx**: HTTP client for testing

### Code Quality
- **Black**: Code formatter
- **Ruff**: Fast Python linter
- **MyPy**: Static type checker

---

## Data Flow

### Create Product Flow
```
Client Request (POST /api/v1/products)
    ↓
FastAPI Route Validation (ProductCreate schema)
    ↓
ProductService.create_product()
    ├─ Validate input (name, price, stock)
    ├─ Create Product instance
    ├─ Store in _products dict
    └─ Return Product
    ↓
Route returns ProductResponse
    ↓
Client Response (201 Created)
```

### Get Product Flow
```
Client Request (GET /api/v1/products/{id})
    ↓
FastAPI Route
    ↓
ProductService.get_product_by_id(id)
    ├─ Validate ID
    ├─ Look up in _products dict
    └─ Return Product or None
    ↓
Route returns ProductResponse or 404
    ↓
Client Response
```

---

## Middleware & Cross-Cutting Concerns

### 1. **CORS Middleware**
- Allows requests from all origins
- In production, restrict to specific domains

### 2. **Request Logging Middleware**
- Logs all incoming requests with:
  - HTTP method and path
  - Client IP address
  - Response status code
  - Request duration

### 3. **Health Check Endpoint**
- `/api/v1/health` provides system status
- Useful for monitoring and load balancers

### 4. **Global Exception Handler**
- Catches `ValueError` exceptions
- Returns 400 Bad Request with error message
- Provides consistent error responses

---

## Configuration Management

The `Settings` class (`app/config.py`) uses Pydantic `BaseSettings` to:
- Load configuration from environment variables
- Provide default values
- Validate configuration on startup
- Support `.env` file loading

### Configurable Settings
```python
- app_name: Application name
- app_version: API version
- app_description: API description
- host: Server host
- port: Server port
- debug: Debug mode
- reload: Auto-reload on file changes
- log_level: Logging level
```

---

## Testing Strategy

### Unit Tests (`tests/unit/`)
- Test individual components in isolation
- Mock dependencies
- Fast execution
- High coverage
- Examples:
  - `ProductService` methods
  - Route handlers

### Integration Tests (`tests/integration/`)
- Test components working together
- Real `TestClient` without mocking
- Realistic workflows
- Examples:
  - Complete CRUD workflows
  - Multiple component interactions

### End-to-End Tests (`tests/e2e/`)
- Test realistic user scenarios
- Full system behavior
- Complex workflows
- Examples:
  - Product lifecycle management
  - Inventory management scenarios
  - Product discovery workflows

### Test Fixtures
Common fixtures in `conftest.py`:
- `app`: Fresh FastAPI app instance
- `client`: Test client for making requests
- `product_service`: Isolated service instance
- `reset_product_service`: Automatic state reset between tests

---

## Error Handling Strategy

### Input Validation
- Pydantic validates request schemas
- Returns 422 for invalid request format
- Returns 400 for business logic validation errors

### Business Logic Validation
- `ProductService` validates data before operations
- Raises `ValueError` for validation failures
- Routes catch exceptions and return appropriate HTTP status

### HTTP Error Responses
- 400 Bad Request: Validation errors
- 404 Not Found: Resource not found
- 500 Internal Server Error: Uncaught exceptions

---

## Scalability & Future Enhancements

### Current Limitations
1. In-memory storage (data lost on restart)
2. Single-threaded data access
3. No authentication/authorization
4. No rate limiting

### Future Enhancements
1. **Database Integration**
   - Replace `_products` dict with database
   - Add SQLAlchemy ORM
   - Implement transactions

2. **Authentication**
   - Add JWT token authentication
   - Role-based access control (RBAC)

3. **Advanced Features**
   - Product categories
   - Customer reviews and ratings
   - Order management
   - Inventory tracking

4. **Performance**
   - Add caching (Redis)
   - Database indexing
   - Query optimization

5. **Operations**
   - Structured logging
   - Distributed tracing
   - Metrics and monitoring
   - API versioning management

---

## Deployment

### Development
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Docker
See `Dockerfile` for containerization.

---

## Type Safety

### Static Type Checking
- All functions have type annotations
- `mypy` performs static type checking
- Pydantic provides runtime type validation

### Validation
- Input: Pydantic schemas validate request data
- Output: Pydantic models ensure consistent responses
- Logic: Type hints catch errors early

---

## Code Standards

### Style
- **Code Formatter**: Black (100 character line length)
- **Linter**: Ruff (checks PEP 8 and more)

### Documentation
- Docstrings: Google-style docstrings
- Type hints: Full type annotations
- Comments: High-level logic explanations

### Testing
- Minimum coverage: 80%
- All public functions have tests
- Tests use `@pytest.mark` for organization

---

## Security Considerations

### Current State
- No authentication
- CORS allows all origins
- No rate limiting
- No input sanitization (Pydantic provides basic validation)

### Recommendations for Production
1. Implement authentication (JWT)
2. Restrict CORS to known origins
3. Add rate limiting
4. Use HTTPS/TLS
5. Sanitize all inputs
6. Add request/response logging for audit trails
7. Implement CRSF protection if using sessions
