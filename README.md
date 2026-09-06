# E-commerce Backend API 🛒

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Production-grade **REST API** for e-commerce operations with complete product catalog, order management, and inventory tracking. Built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy** following industry best practices.

## 🎯 Key Features

✅ **Product Catalog** - Full CRUD operations with filtering and pagination
✅ **Order Management** - Complete order lifecycle with status tracking
✅ **Inventory Tracking** - Real-time stock management with validation
✅ **Category System** - Hierarchical product organization
✅ **Shopping Cart** - Persistent cart with quantity management
✅ **Type Safety** - Full type hints and Pydantic validation
✅ **Production Ready** - Docker, PostgreSQL, comprehensive testing
✅ **CI/CD Pipeline** - Automated testing and deployment

## 🚀 Quick Start

### Docker (Recommended)
```bash
docker-compose up --build
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Local Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn src.main:app --reload
```

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/products` | List products (paginated, filterable) |
| `POST` | `/api/v1/products` | Create product |
| `GET` | `/api/v1/products/{id}` | Get product details |
| `PUT` | `/api/v1/products/{id}` | Update product |
| `DELETE` | `/api/v1/products/{id}` | Delete product |
| `GET` | `/api/v1/categories` | List categories |
| `POST` | `/api/v1/categories` | Create category |
| `GET` | `/api/v1/orders` | List orders |
| `POST` | `/api/v1/orders` | Create order |
| `GET` | `/api/v1/orders/{id}` | Get order details |
| `PUT` | `/api/v1/orders/{id}/status` | Update order status |
| `GET` | `/api/v1/cart` | Get shopping cart |
| `POST` | `/api/v1/cart/items` | Add to cart |
| `DELETE` | `/api/v1/cart/items/{id}` | Remove from cart |

## 💾 Database Schema

### Products Table
- `id` - Primary key
- `name` - Product name (unique, indexed)
- `description` - Product description
- `price` - Product price (Decimal)
- `stock_quantity` - Available units
- `category_id` - Category reference
- `sku` - Stock Keeping Unit (unique)
- `created_at`, `updated_at` - Timestamps

### Orders Table
- `id` - Primary key
- `order_number` - Unique order identifier
- `total_amount` - Order total
- `status` - pending, processing, shipped, delivered
- `customer_name` - Customer info
- `created_at`, `updated_at` - Timestamps

### OrderItems Table
- `id` - Primary key
- `order_id` - Order reference
- `product_id` - Product reference
- `quantity` - Quantity ordered
- `unit_price` - Price at time of order

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=term-missing

# Specific test
pytest tests/test_products.py::TestProductCRUD::test_create_product -v
```

**Coverage:** 95%+ with comprehensive test suite

## 🐳 Docker Deployment

```bash
# Build image
docker build -t ecommerce-api:latest .

# Run with PostgreSQL
docker-compose up --build

# Run single container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/ecommerce \
  ecommerce-api:latest
```

## 🔧 Development

### Code Quality
```bash
black src tests          # Format
flake8 src tests         # Lint
mypy src                 # Type check
pytest tests/ --cov      # Test with coverage
```

## 📊 Example Requests

### Create Product
```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "stock_quantity": 50,
    "category_id": 1,
    "sku": "LAPTOP-001"
  }'
```

### Create Order
```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "items": [
      {"product_id": 1, "quantity": 2}
    ]
  }'
```

## 🏗️ Project Structure

```
ecommerce-backend-api/
├── src/
│   ├── main.py           # FastAPI app
│   ├── config.py         # Configuration
│   ├── database.py       # Database setup
│   ├── models.py         # ORM models
│   ├── schemas.py        # Pydantic schemas
│   ├── services.py       # Business logic
│   └── routes/           # API endpoints
├── tests/                # Test suite
├── Dockerfile            # Container
├── docker-compose.yml    # Local dev
├── pyproject.toml        # Project config
└── README.md             # This file
```

## ✅ Production Checklist

- [x] Type hints throughout
- [x] Input validation (Pydantic)
- [x] Error handling
- [x] Database indexing
- [x] Connection pooling
- [x] Comprehensive tests
- [x] Docker containerization
- [x] CI/CD pipeline
- [x] Environment configuration
- [x] Logging and monitoring hooks

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 👨‍💻 Author

**Fernando Godoi**
- GitHub: [@fergodoii94](https://github.com/fergodoii94)
- Email: fergodoi94@gmail.com

**Status:** ✅ Production Ready
