# Setup Guide

## Prerequisites

- Python 3.9 or higher
- pip or uv (package manager)
- Git (for version control)

## Installation

### 1. Clone the Repository

```bash
cd rest_api_ghcp_demo
```

### 2. Create Virtual Environment

Using Python's built-in venv:
```bash
python -m venv .venv
```

Or using uv:
```bash
uv venv
```

### 3. Activate Virtual Environment

**On Windows (PowerShell)**:
```powershell
.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt)**:
```cmd
.venv\Scripts\activate.bat
```

**On macOS/Linux**:
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

Using pip:
```bash
pip install -e ".[dev]"
```

Or using uv:
```bash
uv sync
```

This installs:
- **Core dependencies**: FastAPI, Uvicorn, Pydantic
- **Development dependencies**: pytest, Black, Ruff, MyPy, etc.

## Running the Application

### Development Server

Start the development server with auto-reload:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

### Production Server

Using Gunicorn with Uvicorn workers:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

---

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Types

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# End-to-end tests only
pytest -m e2e

# All tests with verbose output
pytest -v

# Run specific test file
pytest tests/unit/services/test_product_service.py

# Run specific test class
pytest tests/unit/services/test_product_service.py::TestProductServiceGetAll

# Run specific test
pytest tests/unit/services/test_product_service.py::TestProductServiceGetAll::test_get_all_products_returns_list
```

### Test Coverage

Generate HTML coverage report:

```bash
pytest --cov=app --cov-report=html
```

Coverage report will be available in `htmlcov/index.html`

### Run Tests with Different Markers

```bash
# Run only fast tests
pytest -m "not slow"

# Run specific marker
pytest -m integration
```

---

## Code Quality

### Format Code with Black

```bash
black app/ tests/
```

### Lint Code with Ruff

```bash
ruff check app/ tests/
```

Auto-fix issues:
```bash
ruff check --fix app/ tests/
```

### Type Check with MyPy

```bash
mypy app/
```

### Run All Quality Checks

```bash
# Format
black app/ tests/

# Lint and fix
ruff check --fix app/ tests/

# Type check
mypy app/

# Tests
pytest
```

---

## Project Configuration

### pyproject.toml

Main configuration file containing:
- Project metadata
- Dependencies
- Tool configurations (Black, Ruff, MyPy, Pytest)

### pytest.ini

Pytest configuration:
- Test discovery patterns
- Coverage settings
- Marker definitions
- Output formatting

### ruff.toml

Ruff linter configuration:
- Enabled rules
- Ignored rules
- File exclusions

### mypy.ini

MyPy type checker configuration:
- Python version
- Type checking options
- Library-specific overrides

---

## Environment Variables

Create a `.env` file in the project root:

```bash
# Application settings
APP_NAME=Product Management API
APP_VERSION=1.0.0
DEBUG=False

# Server settings
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
```

These variables are loaded automatically by Pydantic Settings.

---

## API Usage Examples

### Using curl

#### List Products
```bash
curl http://localhost:8000/api/v1/products
```

#### Get Product by ID
```bash
curl http://localhost:8000/api/v1/products/1
```

#### Create Product
```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Product",
    "description": "Product description",
    "price": 99.99,
    "stock": 10
  }'
```

#### Update Product
```bash
curl -X PUT http://localhost:8000/api/v1/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 129.99,
    "stock": 15
  }'
```

#### Delete Product
```bash
curl -X DELETE http://localhost:8000/api/v1/products/1
```

#### Search Products
```bash
curl "http://localhost:8000/api/v1/products?search=laptop"
```

#### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# List products
response = requests.get(f"{BASE_URL}/products")
products = response.json()

# Get product
response = requests.get(f"{BASE_URL}/products/1")
product = response.json()

# Create product
data = {
    "name": "New Product",
    "price": 99.99,
    "stock": 10
}
response = requests.post(f"{BASE_URL}/products", json=data)
new_product = response.json()

# Update product
data = {"price": 129.99}
response = requests.put(f"{BASE_URL}/products/1", json=data)
updated = response.json()

# Delete product
response = requests.delete(f"{BASE_URL}/products/1")
```

---

## Docker Setup

### Build Docker Image

```bash
docker build -t product-api:latest .
```

### Run Docker Container

```bash
docker run -p 8000:8000 product-api:latest
```

### Docker Compose

```bash
docker-compose up
```

---

## Troubleshooting

### Virtual Environment Not Activating

**Windows PowerShell**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

### ModuleNotFoundError

Ensure you've activated the virtual environment and installed dependencies:
```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

### Port Already in Use

Run on a different port:
```bash
uvicorn app.main:app --port 8001
```

### pytest Not Found

Ensure dev dependencies are installed:
```bash
pip install -e ".[dev]"
```

### Import Errors in IDE

Configure your IDE to use the virtual environment Python interpreter:
- VS Code: Select interpreter from `.venv`
- PyCharm: Settings → Project → Python Interpreter → `.venv`

---

## Git Workflow

### Initial Setup

```bash
# Initialize git if not already done
git init

# Configure user
git config user.email "your-email@example.com"
git config user.name "Your Name"
```

### Making Changes

```bash
# Create a new branch
git checkout -b feature/feature-name

# Make changes and stage
git add .

# Commit changes
git commit -m "Description of changes"

# Push to remote
git push origin feature/feature-name
```

### Creating a Pull Request

1. Push your branch to GitHub
2. Open a Pull Request
3. Add description of changes
4. Wait for review and CI/CD checks to pass

---

## CI/CD Setup

### GitHub Actions Example

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
    
    - name: Run tests
      run: pytest
    
    - name: Check code quality
      run: |
        black --check app/ tests/
        ruff check app/ tests/
        mypy app/
```

---

## Performance Optimization

### Development Tips

1. **Use `--reload` only in development**: Auto-reload is slower
2. **Use test markers**: Run only relevant tests with `-m` flag
3. **Profile code**: Use Python's `cProfile` for bottlenecks

### Production Tips

1. **Use multiple workers**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker`
2. **Enable caching**: Consider Redis for caching
3. **Database optimization**: Add indexes, optimize queries
4. **Monitor performance**: Use APM tools

---

## Security Best Practices

1. **Never commit `.env` files** with sensitive data
2. **Use environment variables** for secrets
3. **Enable HTTPS** in production
4. **Implement authentication** (JWT)
5. **Restrict CORS** to known origins
6. **Validate all inputs** (already done with Pydantic)
7. **Use rate limiting** in production
8. **Keep dependencies updated**: `pip list --outdated`

---

## Getting Help

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)

### Common Issues
- Check [API_SPEC.md](API_SPEC.md) for endpoint details
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for design patterns

### Debug Logging

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload
```

---

## Project Maintenance

### Update Dependencies

```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade fastapi

# Update all packages
pip install --upgrade pip
pip install -e ".[dev]" --upgrade
```

### Running Linter Fixes

```bash
# Auto-fix issues
black app/ tests/
ruff check --fix app/ tests/
```

### Test Coverage Goals

Aim for 80%+ code coverage:
```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```
